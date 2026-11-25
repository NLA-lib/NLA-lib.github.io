"""Run the real hosted overlay against the real API handler with in-memory AWS adapters.

All network requests are intercepted; this never contacts AWS, GitHub or ORCID.
"""
import argparse
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_collaboration import Auth, MemoryDocuments, PERSON, EDITOR
from collaboration import Collaboration
from app import Application
from playwright.sync_api import sync_playwright,expect

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--site',required=True,type=Path);parser.add_argument('--chromium',required=True)
args=parser.parse_args();ROOT=Path(__file__).resolve().parents[2]
class Snapshot:
 def get(self,oid):return json.loads((args.site/'api/v1/editor/objects'/f'{oid}.json').read_text())
 def index(self):return json.loads((args.site/'api/v1/editor/index.json').read_text())['objects']
 def references(self):return json.loads((args.site/'api/v1/references.json').read_text())['references']
class BrowserAuth(Auth):
 def session(self,token):
  person=PERSON if token=='valid' else EDITOR if token=='editor' else None
  return {'person':person,'record':{'csrf':'csrf'}} if person else None
 def update_profile(self,pid,fields):self.people[pid].update(fields);return self.people[pid]
auth=BrowserAuth();documents=MemoryDocuments();community=Collaboration(auth,documents,Snapshot());app=Application(auth,None,collaboration=community)
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path=args.chromium,args=['--no-sandbox']);context=browser.new_context(viewport={'width':1440,'height':1080})
 page=context.new_page();errors=[];failures=[];page.on('pageerror',lambda error:errors.append(str(error)));page.on('dialog',lambda dialog:dialog.accept())
 def intercept(route):
  request=route.request;parsed=urlsplit(request.url)
  if parsed.hostname=='api.nla-lib.org':
   headers=request.all_headers();origin=headers.get('origin','https://nla-lib.org')
   event={'rawPath':parsed.path,'rawQueryString':parsed.query,'headers':headers,'cookies':headers.get('cookie','').split('; '),'body':request.post_data,
          'requestContext':{'domainName':'api.nla-lib.org','http':{'method':request.method,'sourceIp':'192.0.2.1'}}}
   result=app.handle(event)
   if result['statusCode']>=400:failures.append((request.method,parsed.path,result['statusCode'],result['body']))
   route.fulfill(status=result['statusCode'],body=result['body'],headers={**result['headers'],'Access-Control-Allow-Origin':origin,'Access-Control-Allow-Credentials':'true','Access-Control-Allow-Headers':'Content-Type,X-CSRF-Token','Access-Control-Allow-Methods':'GET,POST,OPTIONS'});return
  if parsed.hostname!='nla-lib.org':route.abort();return
  root=args.site if parsed.path.startswith('/explore/') else ROOT.parent
  relative=parsed.path.removeprefix('/explore/') if root==args.site else parsed.path.lstrip('/')
  file=root/relative
  if file.is_dir():file=file/'index.html'
  if not file.is_file():route.fulfill(status=404,body='Not found');return
  import mimetypes
  route.fulfill(body=file.read_bytes(),content_type=mimetypes.guess_type(file.name)[0] or 'application/octet-stream')
 context.route('**/*',intercept)
 def signin(value):context.add_cookies([{'name':'__Host-nla_session','value':value,'url':'https://api.nla-lib.org/','secure':True,'httpOnly':True,'sameSite':'Lax'}])
 def dialog():return page.locator('dialog[open]').last
 def click(scope,label):scope.get_by_role('button',name=label,exact=True).click()
 def tool(label):page.get_by_label('Page actions',exact=True).click();click(page.locator('.page-tools-menu'),label)
 signin('valid');url='https://nla-lib.org/explore/theory/matrix-norms/'
 assert page.goto(url,wait_until='domcontentloaded').status==200
 expect(page.get_by_role('button',name='My contributions',exact=True)).to_be_visible()
 tool('Edit page');body=dialog().get_by_label('Page Markdown',exact=True);original=body.input_value();assert original.startswith('---\nuid:')
 body.fill(original+'\n\n## Browser workflow check\n\nLet $\\mathbf{A}^{\\mathsf{T}}$ be the transpose.\n')
 click(dialog(),'Preview');expect(dialog().locator('.editor-preview')).to_contain_text('Browser workflow check');expect(dialog().locator('.katex-error')).to_have_count(0)
 click(dialog(),'Save draft');expect(dialog().locator('.editor-message')).to_contain_text('Private draft saved')
 with page.expect_navigation(wait_until='domcontentloaded'):click(dialog(),'Close')
 tool('Edit page');expect(dialog().get_by_label('Page Markdown',exact=True)).to_contain_text('')
 assert 'Browser workflow check' in dialog().get_by_label('Page Markdown',exact=True).input_value()
 dialog().get_by_label('Explanation of this change',exact=True).fill('Clarify notation for the transpose.')
 click(dialog(),'Submit for review');expect(dialog().locator('.editor-message')).to_contain_text('Submitted for review')
 click(dialog(),'View submission');expect(dialog()).to_contain_text('submitted');expect(dialog()).to_contain_text('Browser workflow check')
 page.screenshot(path='/tmp/nlalib-platform-submission.png',full_page=False)
 page.goto(url,wait_until='domcontentloaded');expect(page.locator('main')).not_to_contain_text('Browser workflow check')
 signin('editor');page.reload(wait_until='domcontentloaded');click(page,'Review contributions')
 click(dialog(),'Clarify notation for the transpose.');click(dialog(),'Approve');expect(dialog()).to_contain_text('approved');expect(dialog()).to_contain_text('GitHub App is connected')
 assert next(v for (pk,sk),v in documents.rows.items() if pk.startswith('PROPOSAL#'))['status']=='approved'
 page.goto(url,wait_until='domcontentloaded');card=page.locator('.statement-overview').first
 expect(card.locator('[data-discussion-count]')).to_be_visible();expect(card.get_by_role('button',name='Add reaction',exact=True)).to_have_count(0)
 card.locator('summary a').first.click();expect(page.locator('.theorem-statement')).to_be_visible()
 reactions=page.locator('.theorem-reaction-slot');click(reactions,'Add reaction');click(dialog(),'React with 👍 · Helpful');expect(reactions.get_by_role('button',name='👍 Helpful, 1 reaction',exact=True)).to_be_visible()
 discussion=page.locator('#discussion');expect(discussion.locator('.primer-discussion')).to_be_visible()
 discussion.get_by_label('Message · Markdown and LaTeX',exact=True).fill('Could we cite a source for $\\mathbf{A}$?');click(discussion,'Comment')
 expect(discussion.locator('.comment-message')).to_have_count(1);expect(discussion.locator('.katex-error')).to_have_count(0)
 page.screenshot(path='/tmp/nlalib-platform-theorem.png',full_page=False)
 # Generated Lean results also support discussion while their source stays read-only.
 records=Snapshot().index();editable={x['id'] for x in records if x['editable']}
 generated=next(x for x in json.loads((args.site/'api/v1/statements.json').read_text())['statements'] if x['id'] not in editable)
 page.goto('https://nla-lib.org'+generated['url'],wait_until='domcontentloaded')
 expect(page.locator('main[data-editor-readonly] #discussion .primer-discussion')).to_be_visible()
 page.get_by_label('Page actions',exact=True).click();expect(page.locator('.page-tools-menu').get_by_role('button',name='Edit statement',exact=True)).to_have_count(0)
 page.get_by_label('Page actions',exact=True).click()
 page.get_by_role('link',name='My profile',exact=True).click();expect(page.locator('.page-title')).to_have_text('Editor');expect(page.locator('#profile-content')).to_contain_text('Authenticated ORCID')
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path='/tmp/nlalib-platform-mobile.png',full_page=True)
 assert not errors,errors
 assert not failures,failures
 browser.close();print('Hosted browser checks passed: private draft, safe mathematical preview, submission/diff, unchanged publication, editor approval, reactions, discussion, public profile, mobile. No external requests.')
