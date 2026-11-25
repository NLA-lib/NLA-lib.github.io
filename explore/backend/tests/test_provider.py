import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock,patch
from urllib.parse import parse_qs,urlsplit
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from authlib.integrations.requests_client import OAuth2Session
from requests import Response
from requests.adapters import BaseAdapter
from provider import Orcid,ProviderError

class Adapter(BaseAdapter):
    def __init__(self,status=200):self.requests=[];self.status=status
    def send(self,request,**kwargs):
        self.requests.append((request,kwargs));response=Response();response.status_code=self.status;response.url=request.url
        response.headers['Content-Type']='application/json'
        if self.status==307:response.headers['Location']='https://evil.test/token'
        response._content=json.dumps({'access_token':'private-token','token_type':'bearer','scope':'/authenticate','orcid':'0000-0002-1825-0097','name':'Ada Example'}).encode()
        return response
    def close(self):pass

class ProviderTests(unittest.TestCase):
    def provider(self):
        client=Mock();client.get_secret_value.return_value={'SecretString':json.dumps({'client_id':'APP-TEST','client_secret':'private-client-secret'})}
        return Orcid(client,'arn:test','APP-TEST','https://api.nla-lib.org/auth/callback')
    def test_library_exchange_uses_fixed_https_endpoint_and_form_credentials(self):
        adapter=Adapter()
        class Session(OAuth2Session):
            def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.mount('https://',adapter)
        provider=self.provider()
        with patch('provider.OAuth2Session',Session):identity=provider.exchange('test-code')
        self.assertEqual(identity['orcid'],'0000-0002-1825-0097');self.assertEqual(set(identity),{'orcid','name'})
        request,options=adapter.requests[0];self.assertEqual(request.url,'https://orcid.org/oauth/token')
        body=parse_qs(request.body);self.assertEqual(body['client_secret'],['private-client-secret']);self.assertEqual(body['code'],['test-code']);self.assertEqual(options['timeout'],10)
        self.assertNotIn('private-client-secret',request.url)
    def test_token_exchange_does_not_follow_redirects(self):
        adapter=Adapter(307)
        class Session(OAuth2Session):
            def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.mount('https://',adapter)
        with patch('provider.OAuth2Session',Session):
            with self.assertRaises(ProviderError):self.provider().exchange('code')
        self.assertEqual(len(adapter.requests),1)
    def test_authorization_scope_and_client_id(self):
        url=self.provider().authorization_url('browser-state');parts=urlsplit(url);query=parse_qs(parts.query)
        self.assertEqual(parts.netloc,'orcid.org');self.assertEqual(query['scope'],['/authenticate']);self.assertEqual(query['state'],['browser-state']);self.assertNotIn('client_secret',query)

if __name__=='__main__':unittest.main()
