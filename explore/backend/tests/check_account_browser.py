"""Browser smoke with a simulated ORCID provider; never contacts real ORCID or AWS."""
from pathlib import Path
import sys,time,argparse
from http.cookies import SimpleCookie
from urllib.parse import urlsplit,parse_qs
sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_auth import MemoryStore,ORCID
from app import Application
from playwright.sync_api import expect,sync_playwright
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--chromium');args=parser.parse_args()
class Provider:
 def authorization_url(self,state):return 'https://orcid.test/mock?state='+state
 def exchange(self,code):return {'orcid':ORCID,'name':'Browser Researcher'}
class BrowserStore(MemoryStore):
 def ensure_person(self,orcid,name):
  person=super().ensure_person(orcid,name);person['id']='bd1b60c5-31cf-4844-a836-70ab42848937';self.people[person['id']]=person;return person
app=Application(BrowserStore(),Provider())
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=args.chromium,args=['--no-sandbox']);context=browser.new_context();page=context.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
 def route(request_route):
  request=request_route.request;parsed=urlsplit(request.url)
  if parsed.netloc=='nla-lib.org':
   if parsed.path.endswith('collaboration-config.json'):return request_route.fulfill(content_type='application/json',body=__import__('json').dumps({**__import__('json').loads((ROOT.parent/'web/collaboration-config.json').read_text()),'enabled':True}))
   if parsed.path.endswith('collaboration.js'):return request_route.fulfill(content_type='application/javascript; charset=utf-8',body=(ROOT.parent/'web/collaboration.js').read_text())
   return request_route.fulfill(content_type='text/html',body='<html><head><meta charset="utf-8"></head><body><main>Explorer</main><footer class="site-footer-links"></footer><script src="/explore/collaboration.js"></script></body></html>')
  if parsed.netloc!='api.nla-lib.org':return request_route.abort()
  headers=request.all_headers();origin=headers.get('origin');cors={'Access-Control-Allow-Origin':origin or 'https://nla-lib.org','Access-Control-Allow-Credentials':'true','Access-Control-Allow-Headers':'Content-Type,X-CSRF-Token','Access-Control-Allow-Methods':'GET,POST,OPTIONS'}
  event={'rawPath':parsed.path,'rawQueryString':parsed.query,'headers':headers,'cookies':headers.get('cookie','').split('; ') if headers.get('cookie') else [],'body':request.post_data,'requestContext':{'domainName':parsed.netloc,'http':{'method':request.method,'sourceIp':'192.0.2.2'}}}
  result=app.handle(event)
  print(request.method,parsed.netloc,parsed.path,result['statusCode'],flush=True)
  for raw in result['cookies']:
   values=SimpleCookie();values.load(raw)
   for name,value in values.items():
    if value['max-age']=='0':context.clear_cookies(name=name,domain='api.nla-lib.org')
    else:context.add_cookies([{'name':name,'value':value.value,'url':'https://api.nla-lib.org/','secure':True,'httpOnly':True,'sameSite':'Lax','expires':time.time()+int(value['max-age'])}])
  request_route.fulfill(status=result['statusCode'],headers={**result['headers'],**cors},body=result['body'])
 context.route('**/*',route)
 target='/explore/theory/matrix-norms/?model=exact#discussion'
 page.goto('https://nla-lib.org'+target);expect(page.get_by_role('link',name='Sign in with ORCID')).to_be_visible();expect(page.get_by_role('link',name='Sign in with ORCID')).to_have_attribute('href',__import__('re').compile(r'^https://api\.nla-lib\.org/auth/login\?return_to='))
 # Provision a session through the real callback handler with a simulated provider.
 # Unit tests cover redirects; the browser checks the actual account/CORS/cookie UI.
 def event(path,query='',cookies=()):return {'rawPath':path,'rawQueryString':query,'headers':{},'cookies':list(cookies),'requestContext':{'domainName':'api.nla-lib.org','http':{'method':'GET','sourceIp':'192.0.2.2'}}}
 login=app.handle(event('/auth/login','return_to='+__import__('urllib.parse',fromlist=['quote']).quote(target,safe='')));state=parse_qs(urlsplit(login['headers']['Location']).query)['state'][0];flow=login['cookies'][0].split(';')[0]
 callback=app.handle(event('/auth/callback','state='+state+'&code=simulated',[flow]));assert callback['statusCode']==302;assert callback['headers']['Location']=='https://nla-lib.org'+target
 values=SimpleCookie();values.load(callback['cookies'][0]);name=next(iter(values));value=values[name]
 context.add_cookies([{'name':name,'value':value.value,'url':'https://api.nla-lib.org/','secure':True,'httpOnly':True,'sameSite':'Lax','expires':time.time()+43200}])
 page.goto('about:blank') # Simulate leaving the Explorer for ORCID before returning.
 page.goto(callback['headers']['Location']);expect(page.get_by_role('link',name='Browser Researcher · My profile')).to_be_visible();page.get_by_role('link',name='Browser Researcher · My profile').click();expect(page.get_by_label('Display name',exact=True)).to_have_value('Browser Researcher');page.get_by_label('About you',exact=True).fill('Researching matrix algorithms.');page.get_by_role('button',name='Save profile').click();expect(page.get_by_role('status')).to_have_text('Profile saved.');page.get_by_role('link',name='View public profile').click();expect(page.get_by_role('heading',name='Browser Researcher')).to_be_visible();expect(page.locator('.bio')).to_have_text('Researching matrix algorithms.');page.goto('https://api.nla-lib.org/account');page.get_by_role('button',name='Sign out',exact=True).click();expect(page.get_by_role('link',name='Sign in with ORCID')).to_be_visible();assert not errors,errors;browser.close();print('Browser smoke passed: cross-origin session, profile update, public profile, logout; provider simulated.')
