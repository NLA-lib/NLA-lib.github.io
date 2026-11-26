"""API Gateway HTTP API v2 handler: ORCID sign-in and public researcher profiles."""
import base64
import html
import json
import os
from pathlib import Path
import re
import secrets
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, urlsplit, unquote
import posixpath

from provider import Orcid, ProviderError
from store import Store, LimitReached

SESSION_COOKIE = '__Host-nla_session'
FLOW_COOKIE = '__Host-nla_oauth'
PUBLIC_FIELDS = ('id', 'kind', 'display_name', 'orcid', 'bio', 'affiliation', 'interests', 'website')


class HttpError(Exception):
    def __init__(self, status, message):
        self.status, self.message = status, message


def cookie(name, value='', lifetime=0):
    return f'{name}={value}; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age={lifetime}'


def public_profile(person):
    return {**{key: person.get(key, '') for key in PUBLIC_FIELDS}, 'orcid_verified': True,
            'url': '/people/'+person['id']}


def valid_orcid(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{4}-\d{4}-\d{3}[\dX]', value):
        return False
    raw = value.replace('-', '')
    total = 0
    for digit in raw[:-1]:
        total = (total+int(digit))*2
    result = (12-total%11)%11
    return raw[-1] == ('X' if result == 10 else str(result))


def sign_in_return(value):
    default='/explore/?auth=complete'
    if not isinstance(value,str) or len(value)>2000 or any(ord(c)<33 for c in value) or chr(92) in value:
        return default
    decoded=unquote(value)
    if any(ord(c)<32 for c in decoded) or chr(92) in decoded:
        return default
    try:
        parsed=urlsplit(value)
    except ValueError:
        return default
    if parsed.scheme or parsed.netloc or not parsed.path.startswith('/explore/'):
        return default
    if not (posixpath.normpath(unquote(parsed.path))+'/').startswith('/explore/'):
        return default
    return value


def profile_fields(payload):
    allowed = {'display_name': 200, 'bio': 2000, 'affiliation': 200, 'interests': 500, 'website': 500}
    if not payload or payload.keys()-allowed.keys():
        raise HttpError(400, 'Only display name, biography, affiliation, research interests and website can be changed.')
    result = {}
    for key, value in payload.items():
        if not isinstance(value, str) or len(value)>allowed[key] or '\x00' in value:
            raise HttpError(400, 'Invalid profile field: '+key)
        result[key] = value.strip()
    if 'display_name' in result and not result['display_name']:
        raise HttpError(400, 'A display name is required.')
    if result.get('website'):
        parsed = urlsplit(result['website'])
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or any(c.isspace() for c in result['website']):
            raise HttpError(400, 'Website must be an HTTPS URL without credentials.')
    return result


class Application:
    def __init__(self, store, provider, domain='api.nla-lib.org', frontend='https://nla-lib.org', daily_limit=1000, collaboration=None):
        self.store, self.provider = store, provider
        self.domain, self.frontend = domain, frontend
        self.origin = 'https://'+domain
        self.daily_limit = daily_limit
        self.collaboration = collaboration

    def response(self, status, body, cookies=(), headers=None, content_type='application/json; charset=utf-8'):
        if content_type.startswith('application/json'):
            body = json.dumps(body, separators=(',', ':'))
        return {'statusCode': status, 'headers': {'Content-Type': content_type,
            'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff',
            'Referrer-Policy': 'no-referrer', 'Strict-Transport-Security': 'max-age=31536000',
            'Content-Security-Policy': "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'",
            **(headers or {})}, 'cookies': list(cookies), 'body': body}

    def page(self, title, content, status=200, cookies=()):
        body = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+' · NLA-lib</title><link rel="stylesheet" href="/assets/account.css"></head><body><main><a class="brand" href="'+self.frontend+'/explore/">NLA-lib</a>'+content+'</main></body></html>'
        return self.response(status, body, cookies, content_type='text/html; charset=utf-8')

    def handle(self, event):
        headers = {key.lower(): value for key, value in event.get('headers', {}).items()}
        context = event.get('requestContext', {})
        method = context.get('http', {}).get('method', '')
        path = event.get('rawPath', '')
        try:
            if context.get('domainName') != self.domain:
                raise HttpError(404, 'Use the configured API hostname.')
            if headers.get('origin') and headers['origin'] not in {self.frontend, self.origin}:
                raise HttpError(403, 'Request origin is not allowed.')
            # HTTP API $default routes can forward preflights to the integration.
            # They must not require a session; API Gateway adds the configured CORS headers.
            if method == 'OPTIONS':
                return self.response(204, '', content_type='text/plain; charset=utf-8')
            cookies = SimpleCookie()
            try:
                cookies.load('; '.join(event.get('cookies', [])))
            except Exception:
                raise HttpError(400, 'Invalid cookies.') from None
            token = cookies[SESSION_COOKIE].value if SESSION_COOKIE in cookies else ''
            if len(token)>256:
                raise HttpError(400, 'Invalid session cookie.')
            if path.startswith('/editor-api/'):
                if not self.collaboration:
                    raise HttpError(503, 'Collaboration is not enabled yet.')
                session = self.store.session(token)
                authorization = headers.get('authorization', '')
                if method not in {'GET', 'POST'}:
                    raise HttpError(405, 'Use GET or POST.')
                payload = None
                if method == 'POST':
                    if not authorization:
                        if not session:
                            raise HttpError(401, 'Sign in with ORCID to contribute.')
                        if headers.get('origin') not in {self.frontend, self.origin}:
                            raise HttpError(403, 'A matching Origin header is required.')
                        if not secrets.compare_digest(headers.get('x-csrf-token', ''), session['record']['csrf']):
                            raise HttpError(403, 'Invalid CSRF token. Reload and retry.')
                    if headers.get('content-type', '').split(';')[0].strip() != 'application/json':
                        raise HttpError(400, 'Use application/json.')
                    raw = event.get('body') or '{}'
                    if len(raw)>500000:
                        raise HttpError(413, 'Request is too large.')
                    try:
                        decoded = base64.b64decode(raw, validate=True) if event.get('isBase64Encoded') else raw.encode()
                        if len(decoded)>300000:
                            raise HttpError(413, 'Request is too large.')
                        payload = json.loads(decoded)
                    except HttpError:
                        raise
                    except Exception:
                        raise HttpError(400, 'Invalid JSON.') from None
                    if not isinstance(payload, dict):
                        raise HttpError(400, 'Supply a JSON object.')
                from collaboration import ApiError
                from documents import Conflict
                from publisher import PublishingError
                import yaml
                try:
                    result = self.collaboration.handle(method, path.removeprefix('/editor-api/'),
                        event.get('rawQueryString', ''), payload, session, authorization)
                    return self.response(200, result)
                except ApiError as error:
                    raise HttpError(error.status, error.message) from None
                except Conflict as error:
                    raise HttpError(409, str(error)) from None
                except PublishingError as error:
                    raise HttpError(409, str(error)) from None
                except yaml.YAMLError:
                    raise HttpError(400, 'Invalid YAML header.') from None
                except ValueError as error:
                    raise HttpError(400, str(error)) from None
                except (TypeError, KeyError):
                    # Do not echo malformed input or parser snippets containing user text.
                    raise HttpError(400, 'Invalid content or request fields. Check the source, entry IDs and required fields.') from None
            if method == 'GET' and path == '/health':
                return self.response(200, {'ok': True, 'service': 'nla-lib-auth', 'features': ['orcid-sign-in', 'profiles', 'signin-return'] + (['editing', 'discussions', 'reactions'] if self.collaboration else []) + (['external-proof-required'] if getattr(self.collaboration,'proof_policy',None) else []) + (['bibliography-editing'] if getattr(self.collaboration,'bibliography_editing',False) else [])})
            if method == 'GET' and path == '/auth/login':
                self.store.login_limit(context.get('http', {}).get('sourceIp', 'unknown'), self.daily_limit)
                state, browser = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
                query=parse_qs(event.get('rawQueryString',''),keep_blank_values=True)
                requested=query.get('return_to',[])
                return_to=sign_in_return(requested[0]) if len(requested)==1 else '/explore/?auth=complete'
                self.store.create_flow(state, browser, return_to)
                return self.response(302, '', [cookie(FLOW_COOKIE, browser, 600)],
                    {'Location': self.provider.authorization_url(state)}, 'text/plain; charset=utf-8')
            if method == 'GET' and path == '/auth/callback':
                query = parse_qs(event.get('rawQueryString', ''), keep_blank_values=True)
                state = query.get('state', [])
                browser = cookies[FLOW_COOKIE].value if FLOW_COOKIE in cookies else ''
                if len(state)!=1 or not re.fullmatch(r'[A-Za-z0-9_-]{32,128}', state[0]) or not re.fullmatch(r'[A-Za-z0-9_-]{32,128}', browser):
                    raise HttpError(400, 'This sign-in request expired or is invalid. Start sign-in again.')
                flow=self.store.consume_flow(state[0],browser)
                if not flow:
                    raise HttpError(400, 'This sign-in request expired or is invalid. Start sign-in again.')
                if 'error' in query:
                    raise HttpError(400, 'ORCID sign-in was declined. You can start again when ready.')
                codes = query.get('code', [])
                if len(codes)!=1 or not 1<=len(codes[0])<=512 or any(c.isspace() for c in codes[0]):
                    raise HttpError(400, 'The ORCID authorization code is missing or invalid.')
                identity = self.provider.exchange(codes[0])
                if not valid_orcid(identity.get('orcid')) or not isinstance(identity.get('name', ''), str):
                    raise HttpError(502, 'ORCID returned an invalid researcher identity. Start sign-in again.')
                person = self.store.ensure_person(identity['orcid'], identity.get('name', ''))
                if person.get('status') != 'active':
                    raise HttpError(403, 'This account is suspended.')
                session, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
                self.store.create_session(session, person['id'], csrf)
                self.store.delete_session(token)
                return self.response(302, '', [cookie(SESSION_COOKIE, session, 43200), cookie(FLOW_COOKIE)],
                    {'Location': self.frontend+sign_in_return(flow.get('return_to'))}, 'text/plain; charset=utf-8')
            if method == 'GET' and path.startswith('/assets/'):
                assets = {'/assets/account.js': ('account.js', 'application/javascript; charset=utf-8'),
                          '/assets/account.css': ('account.css', 'text/css; charset=utf-8')}
                if path not in assets:
                    raise HttpError(404, 'Not found.')
                filename, mime = assets[path]
                return self.response(200, Path(__file__).with_name(filename).read_text(), content_type=mime)
            if method == 'GET' and path == '/account':
                return self.page('Your profile', '<h1>Your researcher profile</h1><div id="account" role="status">Loading your profile…</div><script src="/assets/account.js" defer></script>')
            profile = re.fullmatch(r'/(profiles|people)/([a-f0-9-]{36})', path)
            if method == 'GET' and profile:
                person = self.store.person(profile[2])
                if not person or person.get('status') != 'active':
                    raise HttpError(404, 'Profile not found.')
                if profile[1] == 'profiles':
                    return self.response(200, {'profile': public_profile(person)})
                if self.collaboration:
                    return self.response(302, '', headers={'Location': self.frontend+'/explore/community/?profile='+person['id']})
                content = '<h1>'+html.escape(person['display_name'])+'</h1><p>'+html.escape(person.get('affiliation', ''))+'</p><p class="bio">'+html.escape(person.get('bio', ''))+'</p><p>Research interests: '+html.escape(person.get('interests', ''))+'</p><p><a href="https://orcid.org/'+person['orcid']+'">ORCID '+person['orcid']+'</a> · Authenticated ORCID iD</p>'
                if person.get('website'):
                    content += '<p><a rel="noopener noreferrer" href="'+html.escape(person['website'], quote=True)+'">Website</a></p>'
                return self.page(person['display_name'], content)
            if path not in {'/me', '/me/profile', '/auth/logout'}:
                raise HttpError(404, 'Not found.')
            session = self.store.session(token)
            if not session:
                return self.response(401, {'error': 'Sign in with ORCID to continue.'}, [cookie(SESSION_COOKIE)])
            if method == 'GET' and path == '/me':
                return self.response(200, {'profile': public_profile(session['person']),
                    'role': session['person']['role'], 'csrf_token': session['record']['csrf'],
                    'features': ['profiles']})
            if method != 'POST' or path not in {'/me/profile', '/auth/logout'}:
                raise HttpError(405, 'Method not allowed.')
            if headers.get('origin') not in {self.frontend, self.origin}:
                raise HttpError(403, 'A matching Origin header is required.')
            if not secrets.compare_digest(headers.get('x-csrf-token', ''), session['record']['csrf']):
                raise HttpError(403, 'Invalid CSRF token. Reload your profile and retry.')
            if headers.get('content-type', '').split(';')[0].strip() != 'application/json':
                raise HttpError(400, 'Use application/json.')
            raw = event.get('body') or '{}'
            if len(raw)>20000:
                raise HttpError(413, 'Request is too large.')
            try:
                payload = json.loads(base64.b64decode(raw, validate=True) if event.get('isBase64Encoded') else raw)
            except Exception:
                raise HttpError(400, 'Invalid JSON.') from None
            if not isinstance(payload, dict):
                raise HttpError(400, 'Supply a JSON object.')
            if path == '/auth/logout':
                self.store.delete_session(token)
                self.store.audit(session['person']['id'], 'signed_out')
                return self.response(200, {'signed_out': True}, [cookie(SESSION_COOKIE)])
            person = self.store.update_profile(session['person']['id'], profile_fields(payload))
            return self.response(200, {'profile': public_profile(person)})
        except LimitReached:
            return self.response(429, {'error': 'Request limit reached. Try again later.'}, headers={'Retry-After': '3600'})
        except HttpError as error:
            return self.error(path, error.status, error.message)
        except ProviderError:
            print(json.dumps({'event': 'orcid_exchange_failed', 'request_id': context.get('requestId', '')}))
            return self.error(path, 502, 'ORCID sign-in could not be completed. Start again or try later.')
        except Exception as error:
            # Log only the category and request ID: request URLs, cookies and secrets stay out.
            print(json.dumps({'event': 'request_failed', 'category': type(error).__name__, 'request_id': context.get('requestId', '')}))
            return self.error(path, 503, 'The sign-in service is temporarily unavailable. Try again later.')

    def error(self, path, status, message):
        if path == '/auth/callback':
            return self.page('Sign-in could not complete', '<h1>Sign-in could not complete</h1><p>'+html.escape(message)+'</p><p><a href="/auth/login">Try ORCID sign-in again</a></p>', status, [cookie(FLOW_COOKIE)])
        return self.response(status, {'error': message})


_application = None


def handler(event, context):
    global _application
    if _application is None:
        import boto3
        domain = os.environ['API_DOMAIN']
        auth_store = Store(boto3.resource('dynamodb').Table(os.environ['TABLE_NAME']))
        from collaboration import Collaboration
        from documents import Documents
        from publisher import Publisher
        publisher = Publisher(boto3.client('secretsmanager'), os.environ['GITHUB_APP_SECRET_ARN']) if os.environ.get('GITHUB_APP_SECRET_ARN') else None
        community = Collaboration(auth_store, Documents(auth_store.table), publisher=publisher)
        _application = Application(auth_store,
            Orcid(boto3.client('secretsmanager'), os.environ['ORCID_SECRET_ARN'], os.environ['ORCID_CLIENT_ID'],
                  'https://'+domain+'/auth/callback'), domain, os.environ['FRONTEND_ORIGIN'],
            int(os.environ.get('LOGIN_DAILY_LIMIT', '1000')), collaboration=community)
    return _application.handle(event)
