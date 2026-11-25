import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock
from urllib.error import HTTPError
sys.path[:0]=[str(Path(__file__).resolve().parents[i]) for i in (1,2)]
from app import Application, SESSION_COOKIE
from collaboration import Collaboration, ApiError
from content import markdown, preview
from documents import Conflict, Documents
from publisher import Publisher, PublishingError

OID='11111111-1111-4111-8111-111111111111'
PERSON={'id':'22222222-2222-4222-8222-222222222222','kind':'person','display_name':'Ada','orcid':'0000-0002-1825-0097','status':'active','role':'contributor'}
EDITOR=dict(PERSON,id='33333333-3333-4333-8333-333333333333',display_name='Editor',role='trusted_editor')
SOURCE='---\nkind: theory\nid: norms\ntitle: Matrix norms\n---\nOriginal exposition.\n'

class MemoryDocuments:
 def __init__(self):self.rows={}
 def get(self,pk,sk):return copy.deepcopy(self.rows.get((pk,sk)))
 def many(self,keys):return {key:self.get(*key) for key in keys if self.get(*key)}
 def query(self,pk,prefix,limit=100,cursor=None,reverse=False):
  keys=sorted([k for k in self.rows if k[0]==pk and k[1].startswith(prefix)],reverse=reverse)
  if cursor:keys=[k for k in keys if (k[1]<cursor if reverse else k[1]>cursor)]
  page=keys[:limit]
  return [{k:v for k,v in copy.deepcopy(self.rows[key]).items() if k!='_version'} for key in page],page[-1][1] if len(keys)>limit else None
 def commit(self,changes):
  seen=set()
  for pk,sk,value,expected in changes:
   if (pk,sk) in seen:raise AssertionError('Duplicate transaction item')
   seen.add((pk,sk))
   if (self.rows.get((pk,sk)) or {}).get('_version')!=expected:raise Conflict('Concurrent edit')
  for pk,sk,value,expected in changes:
   if value is None:self.rows.pop((pk,sk),None)
   else:self.rows[(pk,sk)]=dict(copy.deepcopy(value),_version=(expected or 0)+1)

class MemorySnapshot:
 def __init__(self):self.row={'object':{'id':OID,'type':'page','title':'Matrix norms','summary':'','body_markdown':'Original exposition.','evidence':{'type':'page'}},'source_markdown':SOURCE,'document_markdown':SOURCE,'source_path':'explore/content/theory/norms.md','source_sha':'blob-sha','revision':'baseline-token','baseline':'baseline-token','editable':True,'url':'/explore/theory/norms/'}
 def get(self,oid):
  if oid!=OID:raise HTTPError('https://example.test',404,'not found',{},None)
  return copy.deepcopy(self.row)
 def index(self):return [{'id':OID,'title':'Matrix norms','type':'page','statement_id':None}]
 def references(self):return {}
class Auth:
 def __init__(self):self.people={x['id']:copy.deepcopy(x) for x in (PERSON,EDITOR)}
 def person(self,pid):return self.people.get(pid)
 def limit(self,*args):pass
 def session(self,token):return {'person':self.people[PERSON['id']],'record':{'csrf':'secret'}} if token=='valid' else None

class CollaborationTests(unittest.TestCase):
 def setUp(self):
  self.db=MemoryDocuments();self.auth=Auth();self.snapshot=MemorySnapshot();self.api=Collaboration(self.auth,self.db,self.snapshot,clock=lambda:1000000)
 def call(self,path,method='GET',payload=None,person=PERSON,query='',token=''):
  return self.api.handle(method,path,query,payload,{'person':person,'record':{'csrf':'csrf'}} if person else None,token)
 def proposal(self):return {'idempotency_key':'request-key-1','explanation':'Clarify the hypothesis','changes':[{'operation':'update_page','id':OID,'base_revision':'baseline-token','fields':{'document_markdown':SOURCE.replace('Original exposition.','Clearer exposition.')}}]}
 def test_drafts_are_private_and_conflict_checked(self):
  request={'base_revision':'baseline-token','draft_revision':None,'fields':self.proposal()['changes'][0]['fields']}
  draft=self.call('objects/'+OID+'/draft','POST',request)
  self.assertEqual(self.call('objects/'+OID)['draft']['draft_revision'],draft['draft_revision'])
  self.assertIsNone(self.call('objects/'+OID,person=EDITOR)['draft']);self.assertIsNone(self.call('objects/'+OID,person=None)['draft'])
  with self.assertRaises(Conflict):self.call('objects/'+OID+'/draft','POST',request)
  self.snapshot.row['revision']='new-published-source';request['draft_revision']=draft['draft_revision']
  with self.assertRaises(Conflict):self.call('objects/'+OID+'/draft','POST',request)
 def test_submission_is_idempotent_and_never_changes_published_content(self):
  request=self.proposal();result=self.call('proposals','POST',request)
  self.assertEqual(result['id'],self.call('proposals','POST',request)['id']);self.assertEqual(self.snapshot.row['document_markdown'],SOURCE)
  request['explanation']='Different request'
  with self.assertRaises(Conflict):self.call('proposals','POST',request)
  request=self.proposal();request['actor_id']=EDITOR['id']
  with self.assertRaises(ValueError):self.call('proposals','POST',request)
 def test_revision_privacy_and_review_roles(self):
  result=self.call('proposals','POST',self.proposal());rid=result['revisions'][OID];outsider=dict(PERSON,id='outsider')
  with self.assertRaises(ApiError):self.call('objects/'+OID,query='revision='+rid,person=outsider)
  with self.assertRaises(ApiError):self.call('proposals/'+result['id']+'/review','POST',{'decision':'approve','message':''})
  self.call('proposals/'+result['id']+'/review','POST',{'decision':'approve','message':'Checked'},person=EDITOR)
  with self.assertRaises(ApiError):self.call('proposals/'+result['id']+'/publish','POST',{},person=EDITOR)
  self.assertEqual(self.call('proposals/'+result['id'],person=EDITOR)['status'],'approved')
  self.assertFalse(any(x['id']==rid for x in self.call('objects/'+OID+'/history',person=outsider)['revisions']))
 def test_publication_is_retryable_and_preserves_old_revision(self):
  result=self.call('proposals','POST',self.proposal());pid=result['id']
  self.call('proposals/'+pid+'/review','POST',{'decision':'approve','message':''},person=EDITOR)
  publisher=Mock();publisher.open.return_value={'number':1,'url':'https://github.com/example','head':'head'};publisher.merge.side_effect=[{'merged':False},{'merged':True,'sha':'new-commit'}];self.api.publisher=publisher
  self.assertEqual(self.call('proposals/'+pid+'/publish','POST',{},person=EDITOR)['status'],'awaiting_checks')
  self.assertEqual(self.call('proposals/'+pid+'/publish','POST',{},person=EDITOR)['status'],'published')
  self.call('proposals/'+pid+'/publish','POST',{},person=EDITOR);publisher.open.assert_called_once();self.assertEqual(publisher.merge.call_count,2)
  self.assertIn('Clearer',self.call('objects/'+OID,person=None,query='revision='+result['revisions'][OID])['document_markdown'])
  self.snapshot.row['revision']='new-baseline'
  self.assertEqual(self.call('objects/'+OID,person=None,query='revision=baseline-token')['document_markdown'],SOURCE)
 def test_comments_parent_binding_and_safe_math(self):
  text='<script>alert(1)</script> $\\mathbf{A}^{\\mathsf{T}}$'
  result=self.call('objects/'+OID+'/feedback','POST',{'kind':'comment','body':text,'parent_id':None})
  self.call('objects/'+OID+'/feedback','POST',{'kind':'suggestion','body':'Add a reference','parent_id':result['id']})
  discussion=self.call('objects/'+OID+'/feedback',person=None);self.assertEqual(discussion['count'],2)
  original=next(x for x in discussion['items'] if x['id']==result['id']);self.assertNotIn('<script>',original['html']);self.assertIn('class="math"',original['html'])
  with self.assertRaises(ValueError):self.call('objects/'+OID+'/feedback','POST',{'kind':'comment','body':'x','parent_id':'other-entry-comment'})
  self.assertEqual(self.call('activity',query='ids='+OID)['objects'][OID]['count'],2)
 def test_reactions_are_idempotent_per_actor(self):
  for _ in range(2):self.call('objects/'+OID+'/reaction','POST',{'emoji':'👍','active':True})
  self.call('objects/'+OID+'/reaction','POST',{'emoji':'👍','active':True},person=EDITOR)
  self.assertEqual(self.call('objects/'+OID+'/reaction')['reactions'][0]['count'],2)
  self.call('objects/'+OID+'/reaction','POST',{'emoji':'👍','active':False})
  self.assertFalse(self.call('objects/'+OID+'/reaction')['reactions'][0]['reacted'])
 def test_notifications_and_scoped_owned_revocable_bots(self):
  self.call('objects/'+OID+'/follow','POST',{'active':True});self.call('objects/'+OID+'/feedback','POST',{'kind':'comment','body':'A question','parent_id':None},person=EDITOR)
  inbox=self.call('notifications');self.assertEqual(inbox['unread'],1);self.call('notifications/read','POST',{'id':inbox['items'][0]['id']});self.assertEqual(self.call('notifications')['unread'],0)
  self.assertEqual(self.call('notifications',person=EDITOR)['unread'],0)
  bot=self.call('bots','POST',{'display_name':'Proof helper','bio':'Find references','scopes':['feedback']});header='Bearer '+bot['token']
  self.call('objects/'+OID+'/feedback','POST',{'kind':'comment','body':'A bot suggestion','parent_id':None},person=None,token=header)
  with self.assertRaises(ApiError):self.call('me/workspace',person=None,token=header)
  with self.assertRaises(ApiError):self.call('proposals','POST',self.proposal(),person=None,token=header)
  self.call('bots/'+self.call('bots')['bots'][0]['token_id']+'/revoke','POST',{})
  with self.assertRaises(ApiError):self.call('objects/'+OID+'/feedback','POST',{'kind':'comment','body':'x','parent_id':None},person=None,token=header)
 def test_content_identity_and_yaml_guards(self):
  for document in [SOURCE.replace('id: norms','id: other'),SOURCE.replace('title: Matrix norms','title: &alias Matrix norms\nsummary: *alias')]:
   with self.assertRaises(ValueError):preview(self.snapshot,self.snapshot.row,{'document_markdown':document})
  self.snapshot.row['editable']=False
  with self.assertRaises(ValueError):preview(self.snapshot,self.snapshot.row,{'document_markdown':SOURCE})
  self.assertNotIn('href="javascript:',markdown('[bad](javascript:alert(1))'))
 def test_http_requires_session_origin_and_csrf(self):
  app=Application(self.auth,Mock(),collaboration=self.api)
  def request(method='GET',headers=None,cookie=True):return app.handle({'rawPath':'/editor-api/objects/'+OID+'/reaction','headers':headers or {},'cookies':[SESSION_COOKIE+'=valid'] if cookie else [],'body':'{"emoji":"👍","active":true}','requestContext':{'domainName':'api.nla-lib.org','http':{'method':method}}})
  self.assertEqual(request()['statusCode'],200);self.assertEqual(request('POST',cookie=False)['statusCode'],401);self.assertEqual(request('POST')['statusCode'],403)
  headers={'origin':'https://nla-lib.org','x-csrf-token':'wrong','content-type':'application/json'};self.assertEqual(request('POST',headers)['statusCode'],403)
  headers['x-csrf-token']='secret';self.assertEqual(request('POST',headers)['statusCode'],200)
  headers['origin']='https://evil.test';self.assertEqual(request('POST',headers)['statusCode'],403)

class PublisherTests(unittest.TestCase):
 def test_allowlisted_paths(self):
  for path in ['.github/workflows/deploy.yml','explore/content/../backend/app.py','explore/content/theory/x.lean']:
   with self.assertRaises(PublishingError):Publisher.path(path)
  self.assertEqual(Publisher.path('explore/content/theory/matrix-norms.md'),'explore/content/theory/matrix-norms.md')
 def test_merge_waits_for_checks_and_uses_guarded_squash(self):
  publisher=Publisher(Mock(),'secret');publisher.request=Mock(side_effect=[{'merged':False,'head':{'sha':'head'}},{'check_runs':[{'name':'test','status':'in_progress','conclusion':None}]},{'total_count':0}])
  self.assertFalse(publisher.merge({'number':1,'head':'head'})['merged']);self.assertFalse(any(x.args[0]=='PUT' for x in publisher.request.call_args_list))
  publisher.request=Mock(side_effect=[{'merged':False,'head':{'sha':'head'}},{'check_runs':[{'name':'test','status':'completed','conclusion':'success'},{'name':'Published content build','status':'completed','conclusion':'success'}]},{'total_count':0},{'merged':True,'sha':'squash'}])
  self.assertTrue(publisher.merge({'number':1,'head':'head'})['merged']);self.assertEqual(publisher.request.call_args.args[2],{'merge_method':'squash','sha':'head'})
 def test_stale_source_fails_before_any_git_write(self):
  publisher=Publisher(Mock(),'secret');publisher.request=Mock(side_effect=[[],{'object':{'sha':'base'}},{'tree':{'sha':'tree'}},{'sha':'changed'}])
  with self.assertRaises(PublishingError):publisher.open({'id':'proposal'},[{'source_path':'explore/content/theory/norms.md','base_source_sha':'old'}])
  self.assertFalse(any(x.args[0]=='POST' for x in publisher.request.call_args_list))

class DynamoWireTests(unittest.TestCase):
 def test_transaction_is_serialized_once(self):
  import boto3
  table=boto3.resource('dynamodb',region_name='us-west-2',aws_access_key_id='test',aws_secret_access_key='test').Table('TestTable');captured=[]
  class Done(Exception):pass
  def inspect(params,**kwargs):captured.append(json.loads(params['body']));raise Done()
  table.meta.client.meta.events.register('before-call.dynamodb.TransactWriteItems',inspect)
  with self.assertRaises(Done):Documents(table).commit([('ENTRY#one','META',{'count':1},None)])
  item=captured[0]['TransactItems'][0]['Put']['Item'];self.assertEqual(item['pk'],{'S':'ENTRY#one'});self.assertEqual(item['version'],{'N':'1'});self.assertEqual(json.loads(item['body']['S']),{'count':1})

class AdditionalSecurityTests(unittest.TestCase):
 setUp=CollaborationTests.setUp
 call=CollaborationTests.call
 proposal=CollaborationTests.proposal
 def test_bots_do_not_inherit_private_drafts_even_when_their_owner_is_signed_in(self):
  self.call('objects/'+OID+'/draft','POST',{'base_revision':'baseline-token','draft_revision':None,'fields':self.proposal()['changes'][0]['fields']})
  bot=self.call('bots','POST',{'display_name':'Bot','bio':'','scopes':['proposals']})
  state=self.call('objects/'+OID,person=None,token='Bearer '+bot['token'])
  self.assertIsNone(state['draft'])
 def test_reports_require_moderation_role_and_preserve_original_in_audit(self):
  comment=self.call('objects/'+OID+'/feedback','POST',{'kind':'comment','body':'Original discussion text','parent_id':None})
  self.call('objects/'+OID+'/report','POST',{'comment_id':comment['id'],'reason':'Abusive text'})
  with self.assertRaises(ApiError):self.call('moderation')
  admin=dict(EDITOR,role='admin')
  report=self.call('moderation',person=admin)['items'][0]
  self.call('moderation/resolve','POST',{'id':report['id'],'action':'hide_comment'},person=admin)
  self.assertTrue(self.call('objects/'+OID+'/feedback')['items'][0]['hidden'])
  audits=[v for (pk,sk),v in self.db.rows.items() if pk=='MODERATION' and sk.startswith('AUDIT#')]
  self.assertEqual(audits[0]['comment']['body'],'Original discussion text')
 def test_suspending_owner_invalidates_bot_without_waiting_for_token_expiry(self):
  bot=self.call('bots','POST',{'display_name':'Bot','bio':'','scopes':['feedback']})
  self.auth.people[PERSON['id']]['status']='suspended'
  with self.assertRaises(ApiError):self.call('objects/'+OID,person=None,token='Bearer '+bot['token'])

class NewEntryTests(unittest.TestCase):
 setUp=CollaborationTests.setUp
 call=CollaborationTests.call
 proposal=CollaborationTests.proposal
 def test_new_informal_result_and_page_placement_are_one_atomic_proposal(self):
  import tempfile
  from statement_sources import load_statements
  oid='55555555-5555-4555-8555-555555555555'
  payload=self.proposal()
  payload['changes'][0]['fields']['document_markdown']=SOURCE+'\n{{ statement:'+oid+' }}\n'
  payload['changes'].append({'operation':'create_statement','id':oid,'base_revision':None,'fields':{
   'title':'An external conjecture','statement_kind':'conjecture','body_markdown':'Suppose $n>0$.',
   'references':[],'proofs':[{'label':'Versioned argument','url':'https://arxiv.org/abs/1234.5678v2','locator':'Conjecture 1'}]}})
  result=self.call('proposals','POST',payload)
  self.assertEqual(len(result['revisions']),2)
  revision=self.db.get('ENTRY#'+oid,'REV#'+result['revisions'][oid])
  page=self.db.get('ENTRY#'+OID,'REV#'+result['revisions'][OID])
  self.assertIn('{{ statement:result-'+oid+' }}',page['document_markdown'])
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'statements').mkdir();(root/'statements/new.md').write_text(revision['document_markdown'])
   statement=load_statements(root)['result-'+oid]
   self.assertEqual(statement.uid,oid);self.assertEqual(statement.review_status,'unreviewed');self.assertEqual(statement.proofs[0]['locator'],'Conjecture 1')

class SnapshotTests(unittest.TestCase):
 def test_generated_entries_use_bounded_shards_without_changing_their_ids(self):
  from content import Snapshot
  snapshot=Snapshot();missing=HTTPError('https://nla-lib.org',404,'missing',{},None)
  snapshot.fetch=Mock(side_effect=[missing,{OID:{'object':{'id':OID},'editable':False}}])
  self.assertEqual(snapshot.get(OID)['object']['id'],OID)
  self.assertEqual(snapshot.fetch.call_args.args[0],'editor/generated/11.json')
 def test_snapshot_errors_other_than_missing_files_do_not_trigger_fallback(self):
  from content import Snapshot
  snapshot=Snapshot();snapshot.fetch=Mock(side_effect=HTTPError('https://nla-lib.org',503,'unavailable',{},None))
  with self.assertRaises(HTTPError):snapshot.get(OID)
  self.assertEqual(snapshot.fetch.call_count,1)
