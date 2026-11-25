#!/usr/bin/env python3
"""Loopback-only editing prototype. Never writes content files or publishes to GitHub."""
from __future__ import annotations
import argparse
from functools import partial
import html
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import secrets
import threading
from urllib.parse import parse_qs, unquote, urlsplit

from editor.model import Catalog, Conflict, Store, packed, digest, REACTIONS
from editor.identities import PERSON
from content_pages import markdown
from rendering import inline_title
from cg_presentation import mathematics

API = '/explore/editor-api/'
ASSETS = Path(__file__).parent / 'editor'

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Requests may contain local revision IDs, but never log payloads or session keys.
        super().log_message(fmt, *args)

    @property
    def application(self):
        return self.server.application

    def reply(self, data, status=200, content_type='application/json; charset=utf-8'):
        raw = data if isinstance(data, bytes) else (packed(data) if content_type.startswith('application/json') else data).encode()
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(raw)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'same-origin')
        self.end_headers()
        try:
            self.wfile.write(raw)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def trusted(self, mutate=False):
        host = self.headers.get('Host')
        if host not in {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}:
            return False
        origin = 'http://' + host
        if not mutate and not urlsplit(self.path).path.startswith(API) and self.headers.get('Sec-Fetch-Mode') == 'navigate':
            return True
        request_origin = self.headers.get('Origin')
        if request_origin and request_origin != origin:
            return False
        if self.headers.get('Sec-Fetch-Site') in {'cross-site', 'same-site'}:
            return False
        if mutate and not self.headers.get('Authorization') and self.headers.get('X-Editor-Session') != self.server.session_key:
            return False
        return True

    def do_GET(self):
        if not self.trusted():
            return self.reply({'error': 'Use the printed loopback origin'}, 403)
        path = urlsplit(self.path).path
        if path.startswith(API):
            return self.api('GET')
        profile = re.fullmatch(r'/explore/people/([a-z0-9-]+)/', path)
        if profile:
            try:
                with self.server.lock:
                    actor = self.application.actor(profile[1])
                    body = '<div class="page-heading"><h1 class="page-title">' + html.escape(actor['display_name']) + '</h1></div><div id="profile-content"></div>'
                    page = re.sub(r'<main id="content"[^>]*>.*?</main>', lambda _: '<main id="content" data-profile-id="' + profile[1] + '">' + body + '</main>', self.application.catalog.explorer.template, flags=re.S)
                    page = re.sub(r'<title>.*?</title>', lambda _: '<title>' + html.escape(actor['display_name']) + ' · NLA-lib</title>', page)
                    page = page if '/explore/editor-assets/editor.js' in page else page.replace('</head>', '<link rel="stylesheet" href="/explore/editor-assets/editor.css"><script defer src="/explore/editor-assets/editor.js"></script></head>')
                return self.reply(page, content_type='text/html; charset=utf-8')
            except KeyError:
                return self.reply({'error': 'Unknown profile'}, 404)
        detail = re.fullmatch(r'/explore/statements/([a-f0-9-]{36})/', path)
        if detail and detail[1] in self.application.catalog.objects:
            try:
                with self.server.lock:
                    state = self.application.get(detail[1])
                    if state['object']['type'] != 'statement':
                        return self.reply({'error': 'Not a statement'}, 404)
                    body = self.application.preview(state['object'])
                    body = '<div class="page-heading"><h1 class="page-title">' + inline_title(mathematics(state['object']['title'])) + '</h1></div>' + body
                    template = self.application.catalog.explorer.template
                    page = re.sub(r'<main id="content"[^>]*>.*?</main>', lambda _: '<main id="content" data-statement-detail="' + detail[1] + '" data-editor-statement="' + detail[1] + '">' + body + '</main>', template, flags=re.S)
                    page = re.sub(r'<title>.*?</title>', lambda _: '<title>' + html.escape(state['object']['title']) + ' · NLA-lib</title>', page)
                    page = page if '/explore/editor-assets/editor.js' in page else page.replace('</head>', '<link rel="stylesheet" href="/explore/editor-assets/editor.css"><script defer src="/explore/editor-assets/editor.js"></script></head>')
                return self.reply(page, content_type='text/html; charset=utf-8')
            except Conflict as error:
                return self.reply({'error': str(error)}, 409)
        if path.startswith('/explore/editor-assets/'):
            name = path.removeprefix('/explore/editor-assets/')
            if re.fullmatch(r'emoji/(?:1f44d|2764|1f389|1f440|1f914|1f4a1|1f64f|2705|2753|1f9ee|1f6a7|1f680|1f642)\.svg', name):
                return self.reply((ASSETS / name).read_text(), content_type='image/svg+xml; charset=utf-8')
            if name not in {'editor.js', 'editor.css', 'discussion.js', 'discussion.css', 'discussion.js.LEGAL.txt'}:
                return self.reply({'error': 'Not found'}, 404)
            return self.reply((ASSETS / name).read_text(), content_type='text/javascript; charset=utf-8' if name.endswith('.js') else 'text/css; charset=utf-8')
        if not path.startswith('/explore/'):
            public = {'/': 'index.html', '/design/': 'design/index.html', '/design': 'design/index.html', '/design/routines.html': 'design/routines.html', '/favicon.ico': 'favicon.ico', '/apple-touch-icon.png': 'apple-touch-icon.png'}
            relative = public.get(path)
            if relative is None and re.fullmatch(r'/(?:css|font|vendor)/[A-Za-z0-9_./-]+\.(?:css|js|woff2?|ttf|svg|png)', path):
                relative = path.lstrip('/')
            if relative:
                root = Path(__file__).resolve().parent.parent
                target = (root / relative).resolve()
                if target.is_relative_to(root) and target.is_file():
                    return self.reply(target.read_bytes(), content_type=self.guess_type(str(target)))
            return self.reply({'error': 'Not found'}, 404)
        # Only built public assets are served, never repository sources or the database.
        relative = unquote(path.removeprefix('/explore/')) if path.startswith('/explore/') else None
        if relative is None:
            return self.reply({'error': 'Not found'}, 404)
        root = self.application.catalog.explorer.site.resolve()
        file = (root / relative).resolve()
        if not file.is_relative_to(root) or any(part.startswith('.') for part in Path(relative).parts):
            return self.reply({'error': 'Not found'}, 404)
        if file.is_dir():
            file /= 'index.html'
        if file.suffix == '.html' and file.is_file():
            try:
                with self.server.lock:
                    text = file.read_text()
                    oid = None if path.startswith('/explore/library/') else self.application.catalog.routes.get(path if path.endswith('/') else path + '/')
                    if oid:
                        state = self.application.get(oid)
                        obj = state['object']
                        body = self.application.preview(obj)
                        body = '<div class="page-heading"><h1 class="page-title">' + inline_title(mathematics(obj['title'])) + '</h1></div>' + body
                        text = re.sub(r'<main id="content"[^>]*>.*?</main>', lambda _: '<main id="content" data-editor-page="' + oid + '">' + body + '</main>', text, flags=re.S)
                    else:
                        library_page = self.application.catalog.routes.get(path)
                        if library_page:
                            text = text.replace('<main id="content">', '<main id="content" data-editor-readonly="true" data-editor-page="' + library_page + '">')
                        routes = {}
                        for collection, mapping in [('results', self.application.catalog.links), ('declarations', self.application.catalog.declarations)]:
                            for key, sid in mapping.items():
                                record = self.application.catalog.explorer.records[collection][key]
                                routes[record['url']] = sid
                        sid = routes.get(path)
                        if sid:
                            text = text.replace('<main id="content">', '<main id="content" data-editor-readonly="true" data-editor-statement="' + sid + '">')
                    text = text if '/explore/editor-assets/editor.js' in text else text.replace('</head>', '<link rel="stylesheet" href="/explore/editor-assets/editor.css"><script defer src="/explore/editor-assets/editor.js"></script></head>')
                return self.reply(text, content_type='text/html; charset=utf-8')
            except Conflict as error:
                return self.reply({'error': str(error)}, 409)
        return super().do_GET()

    def translate_path(self, path):
        return super().translate_path(urlsplit(path).path.removeprefix('/explore'))

    def list_directory(self, path):
        self.send_error(404)
        return None

    def do_POST(self):
        if not self.trusted(mutate=True):
            return self.reply({'error': 'Same-origin editor session required'}, 403)
        if not urlsplit(self.path).path.startswith(API):
            return self.reply({'error': 'Not found'}, 404)
        self.api('POST')

    def api(self, method):
        try:
            with self.server.lock:
                store = self.application
                path = urlsplit(self.path).path.removeprefix(API)
                query = parse_qs(urlsplit(self.path).query)
                actor_id, bot = PERSON, None
                authorization = self.headers.get('Authorization')
                if authorization:
                    bot = store.authenticate_bot(authorization.removeprefix('Bearer ')) if authorization.startswith('Bearer ') else None
                    if not bot:
                        return self.reply({'error': 'Invalid or revoked bot token'}, 401)
                    actor_id = bot['actor']['id']
                    if method == 'GET' and (path in {'bootstrap','bots','notifications','me/workspace','proposals','feedback'} or path.endswith('/draft') or path.endswith('/follow')):
                        return self.reply({'error': 'Private person data is unavailable to bots'}, 403)
                    if method == 'POST':
                        scope = 'proposals' if path == 'proposals' else 'feedback' if path == 'feedback/preview' or path.endswith('/feedback') else 'reactions' if path.endswith('/reaction') else None
                        if not scope or scope not in bot['scopes']:
                            return self.reply({'error': 'This token does not permit that action'}, 403)
                payload = None
                if method == 'POST':
                    if not self.headers.get('Content-Type', '').startswith('application/json'):
                        raise ValueError('Use application/json')
                    length = int(self.headers.get('Content-Length', '0'))
                    if not 0 < length <= 500_000:
                        return self.reply({'error': 'Request exceeds 500 KB or is empty'}, 413)
                    payload = json.loads(self.rfile.read(length))
                    if not isinstance(payload, dict):
                        raise ValueError('Expected a JSON object')
                if method == 'GET' and path == 'bootstrap':
                    return self.reply({'session': self.server.session_key, 'mode': 'local', 'schema_version': 1, 'person': store.actor(), 'reaction_options': [{'emoji': e, 'label': label} for e, label in REACTIONS]})
                if method == 'POST' and path == 'me/profile':
                    return self.reply(store.update_profile(payload))
                profile = re.fullmatch(r'profiles/([a-z0-9-]+)', path)
                if method == 'GET' and profile:
                    return self.reply(store.profile(profile[1], max(0,int(query.get('cursor',['0'])[0]))))
                if path == 'bots':
                    return self.reply({'bots': store.bots()} if method == 'GET' else store.create_bot(payload))
                revoke = re.fullmatch(r'bots/([a-z0-9-]+)/revoke', path)
                if method == 'POST' and revoke:
                    return self.reply(store.revoke_bot(revoke[1]))
                if method == 'GET' and path == 'notifications':
                    return self.reply(store.inbox(max(0,int(query.get('cursor',['0'])[0]))))
                if method == 'POST' and path == 'notifications/read':
                    if set(payload) != {'id'} or not isinstance(payload['id'],str):
                        raise ValueError('Supply a notification id')
                    with store.db:
                        store.db.execute("UPDATE notifications SET read_at=datetime('now') WHERE id=? AND person_id=?", (payload['id'],PERSON))
                    return self.reply({'read': True})
                if method == 'GET' and path == 'me/workspace':
                    def item(oid):
                        obj=store.get(oid)['object']
                        url=store.catalog.explorer.statement_url(oid) if obj['type']=='statement' else store.catalog.pages[oid].url
                        return {'id':oid,'title':obj['title'],'url':url}
                    return self.reply({'drafts':[item(row[0]) for row in store.db.execute('SELECT object_id FROM drafts')], 'following':[item(row[0]) for row in store.db.execute('SELECT object_id FROM subscriptions WHERE person_id=?',(PERSON,))]})
                following = re.fullmatch(r'objects/([a-z0-9-]+)/follow', path)
                if following:
                    if method == 'POST':
                        if set(payload) != {'active'}:
                            raise ValueError('Supply active')
                        return self.reply(store.follow(following[1],payload['active']))
                    return self.reply({'following': bool(store.db.execute('SELECT 1 FROM subscriptions WHERE person_id=? AND object_id=?',(PERSON,following[1])).fetchone())})
                if method == 'GET' and path == 'schema':
                    return self.reply(json.loads((ASSETS / 'proposal.schema.json').read_text()))
                if method == 'GET' and path == 'references':
                    search = query.get('q', [''])[0].casefold()
                    return self.reply({'references': [{'key': key, **record} for key, record in self.application.catalog.explorer.references.items() if search in (key + ' ' + record.get('text', '')).casefold()]})
                if method == 'POST' and path == 'feedback/preview':
                    if set(payload) != {'body'} or not isinstance(payload['body'], str) or len(payload['body']) > 10000:
                        raise ValueError('Supply at most 10000 characters of Markdown')
                    return self.reply({'html': markdown(payload['body'])})
                if method == 'GET' and path == 'proposals':
                    # Recovery remains available even if upstream source changes invalidate a local head.
                    cursor = max(0, int(query.get('cursor', ['0'])[0]))
                    rows = list(store.db.execute('SELECT response FROM proposals ORDER BY rowid LIMIT 101 OFFSET ?', (cursor,)))
                    return self.reply({'proposals': [json.loads(row['response']) for row in rows[:100]], 'next_cursor': cursor + 100 if len(rows) > 100 else None})
                if method == 'GET' and path == 'activity':
                    ids = query.get('ids',[''])[0].split(',')
                    if not 1 <= len(ids) <= 200 or any(not re.fullmatch(r'[a-z0-9-]{1,64}',oid) for oid in ids):
                        raise ValueError('Supply 1–200 entry IDs')
                    return self.reply({'objects': {oid: {'count': store.discussion_count(oid), 'reactions': store.reactions(oid,actor_id)} for oid in ids}})
                if method == 'GET' and path == 'objects':
                    limit = max(1, min(200, int(query.get('limit', ['100'])[0])))
                    cursor = max(0, int(query.get('cursor', ['0'])[0]))
                    search = query.get('q', [''])[0].casefold()
                    kind = query.get('type', [None])[0]
                    overrides = {row['object_id']: json.loads(row['payload']) for row in store.db.execute('SELECT h.object_id,r.payload FROM heads h JOIN revisions r ON h.revision_id=r.id')}
                    objects = [{'id': oid, 'type': obj['type'], 'title': overrides.get(oid, obj)['title']} for oid, obj in store.catalog.objects.items()]
                    objects = sorted((o for o in objects if (not kind or o['type'] == kind) and search in o['title'].casefold()), key=lambda o: (o['title'].casefold(), o['id']))
                    return self.reply({'objects': objects[cursor:cursor + limit], 'next_cursor': cursor + limit if cursor + limit < len(objects) else None})
                if method == 'GET' and path == 'feedback':
                    cursor = max(0, int(query.get('cursor', ['0'])[0]))
                    items = [dict(row) for row in store.db.execute('SELECT * FROM feedback ORDER BY rowid DESC LIMIT 101 OFFSET ?', (cursor,))]
                    for item in items[:100]:
                        obj = store.catalog.objects[item['object_id']]  # Labels use the current entry; keep the original revision_id for provenance.
                        item.update(title=obj['title'], evidence=obj['evidence'])
                    return self.reply({'items': items[:100], 'next_cursor': cursor + 100 if len(items) > 100 else None})
                if method == 'POST' and path == 'proposals':
                    return self.reply(store.propose(payload, actor_id))
                if method == 'POST' and path == 'preview':
                    if set(payload) != {'fields'}:
                        raise ValueError('Preview requires fields')
                    original = Catalog.statement('new', 'New result', '', {'type': 'local'})
                    obj = store.catalog.validate(original, payload['fields'], store.catalog.objects)
                    return self.reply({'html': store.preview(obj), 'diff': self.diff(original, obj), 'diagnostics':store.catalog.notation_issues(obj)})
                match = re.fullmatch(r'objects/([a-z0-9-]+)(?:/(history|draft|preview|feedback|reaction))?', path)
                if not match:
                    return self.reply({'error': 'Unknown endpoint'}, 404)
                oid, action = match.groups()
                state = store.get(oid, query.get('revision', [None])[0])
                if method == 'GET':
                    if action == 'history':
                        return self.reply({'revisions': store.history(oid)})
                    if action == 'feedback':
                        if query.get('summary') == ['1']:
                            return self.reply({'count': store.discussion_count(oid)})
                        return self.reply(store.discussion(oid, actor_id))
                    if action == 'reaction':
                        return self.reply({'reactions': store.reactions(oid, actor_id)})
                    if action is None:
                        draft = None if bot else store.db.execute('SELECT * FROM drafts WHERE object_id=?', (oid,)).fetchone()
                        dependencies = state['dependencies']
                        lookup = lambda sid: store.get(sid, dependencies.get(sid))
                        state['html'] = store.preview(state['object'], lookup if query.get('revision') else None)
                        state['url'] = store.catalog.explorer.statement_url(oid) if state['object']['type'] == 'statement' else store.catalog.pages[oid].url
                        if state['object']['type'] == 'page':
                            state['document_markdown'] = store.catalog.document(state['object'])
                        else:
                            evidence = state['object']['evidence']
                            state['reference_links'] = {
                                'inherited': store.catalog.explorer.records['declarations'].get(evidence.get('declaration'), {}).get('references', []),
                                'editorial': state['object'].get('references', store.catalog.statement_references.get(oid, []))}
                        state['draft'] = {'object': json.loads(draft['payload']), 'base_revision': draft['base_revision'], 'draft_revision': digest([draft['base_revision'], draft['payload']])} if draft else None
                        if state['draft'] and state['object']['type'] == 'page':
                            state['draft']['document_markdown'] = store.catalog.document(state['draft']['object'])
                        state['used_by'] = [{'id': pid, 'title': store.get(pid)['object']['title'], 'url': page.url} for pid, page in store.catalog.pages.items() if '{{ statement:' + oid + ' }}' in store.get(pid)['object']['body_markdown']]
                        if state['object']['evidence'].get('result'):
                            key = state['object']['evidence']['result']
                            state['used_by'].append({'title': 'Library result', 'url': store.catalog.explorer.records['results'][key]['url']})
                        return self.reply(state)
                if method == 'POST':
                    if action == 'draft':
                        if not {'base_revision', 'fields'} <= payload.keys() or payload.keys() - {'base_revision', 'fields', 'draft_revision'}:
                            raise ValueError('Draft requires base_revision, fields and an optional draft_revision')
                        return self.reply(store.draft(oid, payload['base_revision'], payload['fields'], payload.get('draft_revision')))
                    if action == 'preview':
                        if set(payload) != {'fields'}:
                            raise ValueError('Preview requires fields')
                        obj = store.catalog.validate(state['object'], payload['fields'], store.catalog.objects)
                        return self.reply({'html': store.preview(obj), 'diff': self.diff(state['object'], obj), 'diagnostics':store.catalog.notation_issues(obj)})
                    if action == 'feedback':
                        return self.reply(store.feedback(oid, payload, actor_id))
                    if action == 'reaction':
                        if set(payload) != {'emoji', 'active'}:
                            raise ValueError('Supply emoji and active')
                        return self.reply(store.react(oid, payload['emoji'], payload['active'], actor_id))
                return self.reply({'error': 'Unsupported method'}, 405)
        except Conflict as error:
            return self.reply({'error': str(error), 'code': 'revision_conflict'}, 409)
        except KeyError as error:
            return self.reply({'error': str(error)}, 404)
        except (ValueError, TypeError, AttributeError) as error:
            return self.reply({'error': str(error)}, 400)
        except Exception:
            # Keep local paths and database details out of browser responses.
            import traceback
            traceback.print_exc()
            return self.reply({'error': 'Local editor error; see server log'}, 500)

    def diff(self, before, after):
        import difflib
        def lines(obj):
            if obj['type'] == 'page':
                return self.application.catalog.document(obj).splitlines()
            return ('# ' + obj['title'] + '\n' + obj.get('summary', '') + '\n\n' + obj['body_markdown'] + '\n\n' + json.dumps(obj.get('proofs', []), ensure_ascii=False, indent=2)).splitlines()
        return '\n'.join(difflib.unified_diff(lines(before), lines(after), fromfile='Current revision', tofile='Proposed revision', lineterm='')) if before != after else 'No changes.'


def make_server(site, content, database, port=0):
    app = Store(Catalog(site, content), database)
    # Build topic relationships once before accepting requests, not on first navigation.
    app.catalog.explorer.statement_context('')
    if str(database) != ':memory:':
        Path(database).chmod(0o600)
    server = ThreadingHTTPServer(('127.0.0.1', port), partial(Handler, directory=str(Path(site).resolve())))
    server.application = app
    server.lock = threading.RLock()
    server.session_key = secrets.token_urlsafe(32)
    server.origin = f'http://127.0.0.1:{server.server_port}'
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', required=True, type=Path, help='Built Explorer directory containing api/v1')
    parser.add_argument('--content', type=Path, default=Path(__file__).parent / 'content')
    parser.add_argument('--database', type=Path, default=Path.home() / '.local/share/nlalib-editor/prototype.sqlite3')
    parser.add_argument('--port', type=int, default=8082)
    args = parser.parse_args()
    if not (args.site / 'api/v1/search-index.json').is_file():
        parser.error('Build the Explorer first; see editor/README.md')
    if args.database.resolve().is_relative_to(args.site.resolve()):
        parser.error('Keep the private database outside the served website directory')
    args.database.parent.mkdir(parents=True, exist_ok=True)
    server = make_server(args.site, args.content, args.database, args.port)
    print(f'Local editor: {server.origin}/explore/', flush=True)
    print(f'Local database: {args.database}. Nothing is published or committed.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        server.application.db.close()

if __name__ == '__main__':
    main()
