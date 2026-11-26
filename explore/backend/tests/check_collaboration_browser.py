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
 def get(self,oid):
  file=args.site/'api/v1/editor/objects'/f'{oid}.json'
  if file.is_file():return json.loads(file.read_text())
  shard=args.site/'api/v1/editor/generated'/f'{oid[:2]}.json'
  result=json.loads(shard.read_text()).get(oid) if shard.is_file() else None
  if result is None:
   from urllib.error import HTTPError
   raise HTTPError('https://nla-lib.org',404,'missing',{},None)
  return result
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
 tool('Edit page');expect(dialog().get_by_label('Live preview',exact=True)).to_be_visible();body=dialog().get_by_label('Page Markdown',exact=True);original=body.input_value();assert original.startswith('---\nuid:')
 body.fill(original+'\n\n## Browser workflow check\n\nLet $\\mathbf{A}^{\\mathsf{T}}$ be the transpose.\n')
 expect(dialog().locator('.editor-preview')).to_contain_text('Browser workflow check');expect(dialog().locator('.katex-error')).to_have_count(0)
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
 # Generated Lean prose is editable while its formal statement remains fixed.
 records=Snapshot().index();editable={x['id'] for x in records if x.get('statement_id')}
 generated=next(x for x in json.loads((args.site/'api/v1/statements.json').read_text())['statements'] if x['id'] not in editable)
 page.goto('https://nla-lib.org'+generated['url'],wait_until='domcontentloaded')
 expect(page.locator('main #discussion .primer-discussion')).to_be_visible()
 expect(page.locator('.site-header-row').get_by_role('button',name='Add statement',exact=True)).to_have_count(0)
 expect(page.locator('.theorem-statement + .theorem-formal')).to_have_count(1)
 expect(page.locator('.verification-status')).to_have_count(0)
 page.get_by_label('Page actions',exact=True).click();expect(page.locator('.page-tools-menu').get_by_role('button',name='Edit statement',exact=True)).to_have_count(1)
 page.get_by_label('Page actions',exact=True).click()
 # Reproduce the reported CG entry and verify preview updates without a toggle.
 import uuid
 cg_id=str(uuid.uuid5(uuid.NAMESPACE_URL,'https://nla-lib.org/editor/result:cg-galerkin-formula'))
 page.goto('https://nla-lib.org/explore/statements/'+cg_id+'/',wait_until='domcontentloaded')
 tool('Edit statement');expect(dialog().get_by_label('Live preview',exact=True)).to_be_visible()
 statement_body=dialog().get_by_label('Statement · Markdown and LaTeX',exact=True)
 statement_body.fill(statement_body.input_value()+'\n\nLive CG preview check.')
 expect(dialog().locator('.editor-preview')).to_contain_text('Live CG preview check.')
 click(dialog(),'Changes');expect(dialog().locator('.editor-diff')).to_contain_text('Live CG preview check.');expect(dialog().get_by_label('Live preview',exact=True)).to_be_visible()
 page.screenshot(path='/tmp/nlalib-cg-editor-preview.png',full_page=False)
 with page.expect_navigation(wait_until='domcontentloaded'):click(dialog(),'Close')
 # Add an unlinked result directly; a proof URL is mandatory for submission.
 tool('Add statement');expect(dialog().get_by_label('Live preview',exact=True)).to_be_visible()
 dialog().get_by_label('Title',exact=True).fill('Browser external result')
 dialog().get_by_label('Statement · Markdown and LaTeX',exact=True).fill('A result with an externally hosted proof.')
 dialog().get_by_label('Explanation of this change',exact=True).fill('Add a result with a natural-language proof.')
 click(dialog(),'Submit for review');expect(dialog().locator('.editor-message')).to_contain_text('external natural-language proof')
 expect(dialog().locator('.editor-preview')).to_contain_text('No linked Lean statement.')
 click(dialog(),'Add proof reference');dialog().get_by_label('Reference label',exact=True).fill('External proof')
 dialog().get_by_label('HTTPS link',exact=True).fill('https://example.org/proof.pdf')
 click(dialog(),'Submit for review');expect(dialog().locator('.editor-message')).to_contain_text('Submitted for review')
 with page.expect_navigation(wait_until='domcontentloaded'):click(dialog(),'Close')
 # Frontend bibliography: structured typography, downloads, private drafts and review.
 page.goto('https://nla-lib.org/explore/references/',wait_until='domcontentloaded')
 with page.expect_download() as complete:page.get_by_role('link',name='Download the complete bibliography (BibTeX)',exact=True).click()
 assert complete.value.suggested_filename=='nla-lib-references.bib'
 row=page.locator('[data-reference-id="HornJohnson2013"]')
 expect(row.locator('.reference-authors')).to_be_visible();expect(row.locator('cite.reference-title')).to_have_css('font-style','italic')
 expect(row.locator('.reference-publisher')).to_have_css('font-style','normal')
 assert not row.locator('.reference-authors a').count()
 row.get_by_role('link',name='BibTeX',exact=True).click()
 citation=dialog().get_by_label('BibTeX citation',exact=True)
 expect(citation).to_have_attribute('readonly','');assert '@book{HornJohnson2013' in citation.input_value()
 context.grant_permissions(['clipboard-read','clipboard-write']);click(dialog(),'Copy BibTeX')
 expect(dialog().locator('.editor-message')).to_contain_text('BibTeX copied.')
 assert page.evaluate('navigator.clipboard.readText()')==citation.input_value()
 click(dialog(),'Close')
 page.screenshot(path='/tmp/nlalib-bibliography-formatted.png',full_page=False)
 click(row,'Edit');citation=dialog().get_by_label('BibTeX',exact=True)
 citation.fill(citation.input_value().replace('Matrix Analysis','Matrix Analysis (browser edit)'))
 expect(dialog().get_by_label('Live preview',exact=True)).to_contain_text('browser edit')
 click(dialog(),'Save draft');expect(dialog().locator('.editor-message')).to_contain_text('Private draft saved')
 dialog().get_by_label('Explanation of this change',exact=True).fill('Correct the bibliographic title for browser QA.')
 click(dialog(),'Submit for review');expect(dialog().locator('.editor-message')).to_contain_text('Submitted for review')
 click(dialog(),'View submission');expect(dialog()).to_contain_text('Matrix Analysis (browser edit)')
 page.screenshot(path='/tmp/nlalib-bibliography-editor.png',full_page=False)
 page.goto('https://nla-lib.org/explore/references/',wait_until='domcontentloaded')
 expect(page.locator('[data-reference-id="HornJohnson2013"]')).not_to_contain_text('browser edit')
 page.get_by_role('link',name='My profile',exact=True).click();expect(page.locator('.page-title')).to_have_text('Editor');expect(page.locator('#profile-content')).to_contain_text('Authenticated ORCID')
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path='/tmp/nlalib-platform-mobile.png',full_page=True)
 assert not errors,errors
 assert not failures,failures
 browser.close();print('Hosted browser checks passed: private draft, safe mathematical preview, submission/diff, unchanged publication, editor approval, reactions, discussion, public profile, mobile. No external requests.')
