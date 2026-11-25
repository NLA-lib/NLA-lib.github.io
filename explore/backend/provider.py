"""Fixed-issuer ORCID OAuth adapter. Provider tokens are not retained."""
import json
import time
from authlib.integrations.requests_client import OAuth2Session


class ProviderError(Exception):
    pass


class Orcid:
    issuer = 'https://orcid.org'

    def __init__(self, secrets_client, secret_arn, client_id, callback):
        self.secrets_client, self.secret_arn = secrets_client, secret_arn
        self.client_id, self.callback = client_id, callback
        self.cached = None
        self.cached_at = 0

    def credentials(self):
        if self.cached is None or time.monotonic()-self.cached_at > 300:
            response = self.secrets_client.get_secret_value(SecretId=self.secret_arn)
            data = json.loads(response['SecretString'])
            if data.get('client_id') != self.client_id or not isinstance(data.get('client_secret'), str) or not data['client_secret']:
                raise ProviderError('configuration')
            self.cached, self.cached_at = data, time.monotonic()
        return self.cached

    def authorization_url(self, state):
        with OAuth2Session(self.client_id, scope='/authenticate', redirect_uri=self.callback) as session:
            url, _ = session.create_authorization_url(self.issuer+'/oauth/authorize', state=state)
            return url

    def exchange(self, code):
        credentials = self.credentials()
        try:
            with OAuth2Session(self.client_id, credentials['client_secret'], scope='/authenticate',
                              redirect_uri=self.callback, token_endpoint_auth_method='client_secret_post') as session:
                token = session.fetch_token(self.issuer+'/oauth/token', code=code,
                    grant_type='authorization_code', timeout=10, allow_redirects=False,
                    headers={'Accept': 'application/json'})
            if not token.get('access_token') or '/authenticate' not in token.get('scope', '').split():
                raise ProviderError('identity')
            return {'orcid': token.get('orcid'), 'name': token.get('name', '')}
        except ProviderError:
            raise
        except Exception:
            # Never propagate a token, client secret, provider response or callback URL.
            raise ProviderError('exchange') from None
