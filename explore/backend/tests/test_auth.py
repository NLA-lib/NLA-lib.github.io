import contextlib
import io
import json
from pathlib import Path
import secrets
import sys
import unittest
from unittest.mock import Mock
from urllib.parse import parse_qs, urlsplit
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import Application, SESSION_COOKIE, FLOW_COOKIE, valid_orcid
from provider import ProviderError
from store import fingerprint, LimitReached, Store
from botocore.exceptions import ClientError

ORCID='0000-0002-1825-0097'

class MemoryStore:
    def __init__(self):self.now=1000;self.flows={};self.sessions={};self.people={};self.audits=[];self.limited=False
    def login_limit(self,*args):
        if self.limited:raise LimitReached()
    def create_flow(self,state,browser,return_to='/explore/?auth=complete'):self.flows[state]=(browser,self.now+600,return_to)
    def consume_flow(self,state,browser):
        flow=self.flows.get(state)
        if not flow or flow[0]!=browser or flow[1]<=self.now:return False
        del self.flows[state];return {'return_to':flow[2]}
    def ensure_person(self,orcid,name):
        self.people.setdefault('person-a',{'id':'person-a','kind':'person','orcid':orcid,'display_name':name,'role':'contributor','status':'active','bio':'','website':'','interests':'','affiliation':''})
        return self.people['person-a']
    def person(self,key):return self.people.get(key)
    def create_session(self,token,person,csrf):self.sessions[token]={'person_id':person,'csrf':csrf,'expires_at':self.now+43200}
    def session(self,token):
        row=self.sessions.get(token)
        if not row or row['expires_at']<=self.now:return None
        person=self.people[row['person_id']]
        if person['status']!='active':return None
        return {'record':row,'person':person}
    def delete_session(self,token):self.sessions.pop(token,None)
    def update_profile(self,person,fields):self.people[person].update(fields);return self.people[person]
    def audit(self,person,action):self.audits.append((person,action))

class AuthTests(unittest.TestCase):
    def setUp(self):
        self.store=MemoryStore();self.provider=Mock();self.provider.authorization_url.side_effect=lambda state:'https://orcid.org/oauth/authorize?state='+state
        self.provider.exchange.return_value={'orcid':ORCID,'name':'Ada Example'}
        self.app=Application(self.store,self.provider)
    def request(self,path,method='GET',cookies=(),headers=None,body=None,query=''):
        return self.app.handle({'rawPath':path,'rawQueryString':query,'headers':headers or {},'cookies':list(cookies),'body':json.dumps(body) if body is not None else None,'requestContext':{'domainName':'api.nla-lib.org','requestId':'test-request','http':{'method':method,'sourceIp':'192.0.2.1'}}})
    def start(self):
        response=self.request('/auth/login');self.assertEqual(response['statusCode'],302)
        return next(iter(self.store.flows)),response['cookies'][0].split(';')[0]
    def login(self):
        state,browser=self.start();response=self.request('/auth/callback',cookies=[browser],query='state='+state+'&code=example-code');self.assertEqual(response['statusCode'],302)
        token=response['cookies'][0].split(';')[0]
        me=json.loads(self.request('/me',cookies=[token])['body'])
        return token,me,response
    def write(self,path,token,me,body,**overrides):
        headers={'origin':'https://nla-lib.org','x-csrf-token':me['csrf_token'],'content-type':'application/json',**overrides}
        return self.request(path,'POST',[token],headers,body)
    def test_preflight_requires_no_session_but_still_rejects_foreign_origins(self):
        response=self.request('/auth/logout','OPTIONS',headers={'origin':'https://nla-lib.org','access-control-request-method':'POST','access-control-request-headers':'content-type,x-csrf-token'})
        self.assertEqual(response['statusCode'],204)
        self.assertEqual(response['body'],'')
        self.assertFalse(self.store.sessions)
        self.assertEqual(self.request('/auth/logout','OPTIONS',headers={'origin':'https://evil.test'})['statusCode'],403)

    def test_login_session_and_cookie_properties(self):
        token,me,response=self.login();self.assertEqual(me['role'],'contributor');self.assertTrue(me['profile']['orcid_verified']);self.assertEqual(me['profile']['orcid'],ORCID)
        cookie=response['cookies'][0]
        for flag in ['__Host-','Secure','HttpOnly','SameSite=Lax','Path=/','Max-Age=43200']:self.assertIn(flag,cookie)
        self.assertNotIn('Domain=',cookie);self.assertEqual(response['headers']['Location'],'https://nla-lib.org/explore/?auth=complete')
        self.assertEqual(self.request('/me')['statusCode'],401)
    def test_signin_returns_to_the_original_page_and_ignores_callback_override(self):
        from urllib.parse import urlencode
        target='/explore/algorithms/conjugate-gradient/?model=exact#discussion'
        response=self.request('/auth/login',query=urlencode({'return_to':target}))
        self.assertEqual(response['statusCode'],302)
        state=next(iter(self.store.flows));browser=response['cookies'][0].split(';')[0]
        callback=self.request('/auth/callback',cookies=[browser],query=urlencode({'state':state,'code':'x','return_to':'https://evil.test'}))
        self.assertEqual(callback['headers']['Location'],'https://nla-lib.org'+target)
        self.assertEqual(self.request('/auth/callback',cookies=[browser],query=urlencode({'state':state,'code':'x'}))['statusCode'],400)

    def test_signin_accepts_the_canonical_homepage_with_query_and_fragment(self):
        from app import sign_in_return
        self.assertEqual(sign_in_return('/?q=Chebyshev#results'),'/?q=Chebyshev#results')
        self.assertEqual(sign_in_return('/'),'/')

    def test_signin_rejects_external_and_malformed_return_destinations(self):
        from app import sign_in_return
        for target in ['https://evil.test/explore/','//evil.test/explore/','/explore/../../evil','/explore/\\evil','/explore/%0d%0aLocation:evil','/account','/explore/%2e%2e/outside']:
            self.assertEqual(sign_in_return(target),'/explore/?auth=complete',target)

    def test_state_is_browser_bound_one_time_and_expiring(self):
        state,browser=self.start();query='state='+state+'&code=example-code'
        self.assertEqual(self.request('/auth/callback',query=query)['statusCode'],400)
        self.assertEqual(self.request('/auth/callback',cookies=[FLOW_COOKIE+'='+secrets.token_urlsafe(32)],query=query)['statusCode'],400)
        self.provider.exchange.assert_not_called()
        self.assertEqual(self.request('/auth/callback',cookies=[browser],query=query)['statusCode'],302)
        self.assertEqual(self.request('/auth/callback',cookies=[browser],query=query)['statusCode'],400)
        self.provider.exchange.assert_called_once()
        state,browser=self.start();self.store.now+=600
        self.assertEqual(self.request('/auth/callback',cookies=[browser],query='state='+state+'&code=x')['statusCode'],400)
    def test_decline_and_duplicate_parameters_never_exchange(self):
        for suffix in ['&error=access_denied','&code=x&code=y']:
            state,browser=self.start();response=self.request('/auth/callback',cookies=[browser],query='state='+state+suffix);self.assertEqual(response['statusCode'],400)
        self.provider.exchange.assert_not_called()
    def test_csrf_origin_json_and_profile_allowlist(self):
        token,me,_=self.login()
        for headers in [{'origin':'https://evil.test'},{'x-csrf-token':'wrong'},{'origin':''}]:
            self.assertEqual(self.write('/me/profile',token,me,{'bio':'Change'},**headers)['statusCode'],403)
        self.assertEqual(self.write('/me/profile',token,me,{'bio':'Change'},**{'content-type':'text/plain'})['statusCode'],400)
        for fields in [{'role':'admin'},{'orcid':'0000-0000-0000-0000'},{'status':'active'},{'website':'javascript:alert(1)'},{'website':'https://user:password@example.org'}]:
            self.assertEqual(self.write('/me/profile',token,me,fields)['statusCode'],400)
        response=self.write('/me/profile',token,me,{'bio':'Research notes','affiliation':'Example University'});self.assertEqual(response['statusCode'],200)
        profile=json.loads(response['body'])['profile'];self.assertEqual(profile['bio'],'Research notes');self.assertNotIn('csrf',profile);self.assertNotIn('status',profile)
    def test_sessions_expire_revoke_and_respect_suspension(self):
        token,me,_=self.login();self.assertEqual(self.write('/auth/logout',token,me,{})['statusCode'],200);self.assertEqual(self.request('/me',cookies=[token])['statusCode'],401)
        token,me,_=self.login();self.store.people['person-a']['status']='suspended';self.assertEqual(self.request('/me',cookies=[token])['statusCode'],401)
        self.store.people['person-a']['status']='active';self.store.now+=43200;self.assertEqual(self.request('/me',cookies=[token])['statusCode'],401)
    def test_provider_failure_does_not_leak_codes_or_tokens(self):
        state,browser=self.start();self.provider.exchange.side_effect=ProviderError('CLIENT_SECRET_ACCESS_TOKEN_PRIVATE')
        output=io.StringIO()
        with contextlib.redirect_stdout(output):response=self.request('/auth/callback',cookies=[browser],query='state='+state+'&code=PRIVATE_CODE')
        self.assertEqual(response['statusCode'],502)
        for secret in ['CLIENT_SECRET_ACCESS_TOKEN_PRIVATE','PRIVATE_CODE',state]:self.assertNotIn(secret,response['body']+output.getvalue())
    def test_login_quota_and_fixed_callback_target(self):
        self.store.limited=True;self.assertEqual(self.request('/auth/login')['statusCode'],429);self.assertFalse(self.store.flows)
        self.store.limited=False;token,me,response=self.login();self.assertEqual(response['headers']['Location'],'https://nla-lib.org/explore/?auth=complete')
    def test_invalid_orcid_never_creates_account(self):
        self.assertTrue(valid_orcid(ORCID));self.assertFalse(valid_orcid('0000-0002-1825-0098'));self.assertFalse(valid_orcid('https://orcid.org/'+ORCID))
        state,browser=self.start();self.provider.exchange.return_value={'orcid':'0000-0002-1825-0098','name':'bad'}
        self.assertEqual(self.request('/auth/callback',cookies=[browser],query='state='+state+'&code=x')['statusCode'],502);self.assertFalse(self.store.people)

class DynamoStoreTests(unittest.TestCase):
    def test_atomic_state_consumption_enforces_binding_and_expiry(self):
        table=Mock();table.delete_item.return_value={'Attributes':{'pk':'state'}};store=Store(table,clock=lambda:1000)
        self.assertTrue(store.consume_flow('state-token','browser-token'))
        kwargs=table.delete_item.call_args.kwargs
        self.assertEqual(kwargs['ConditionExpression'],'browser_hash=:browser AND expires_at > :now')
        self.assertEqual(kwargs['ExpressionAttributeValues'],{':browser':fingerprint('browser-token'),':now':1000})
        self.assertEqual(kwargs['Key']['pk'],'STATE#'+fingerprint('state-token'))
        table.delete_item.side_effect=ClientError({'Error':{'Code':'ConditionalCheckFailedException'}},'DeleteItem')
        self.assertFalse(store.consume_flow('state-token','browser-token'))
    def test_raw_session_tokens_are_not_stored(self):
        table=Mock();store=Store(table,clock=lambda:1000);store.create_session('PRIVATE_SESSION','person','csrf')
        session=table.put_item.call_args_list[0].kwargs['Item'];self.assertNotIn('PRIVATE_SESSION',json.dumps(session));self.assertEqual(session['expires_at'],44200)
        table.get_item.return_value={'Item':{'expires_at':999,'person_id':'person'}}
        self.assertIsNone(store.session('PRIVATE_SESSION'))
    def test_quota_conditional_failure(self):
        table=Mock();table.update_item.side_effect=ClientError({'Error':{'Code':'ConditionalCheckFailedException'}},'UpdateItem')
        with self.assertRaises(LimitReached):Store(table).login_limit('192.0.2.1')

if __name__=='__main__':unittest.main()
