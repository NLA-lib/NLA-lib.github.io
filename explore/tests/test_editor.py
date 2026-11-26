"""Local editor boundary: revision safety, atomic proposals and untrusted content."""
import copy
import json
from pathlib import Path
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import uuid

import test_content_pages as fixtures
from content_pages import Explorer
from editor.model import Catalog, Conflict, Store, REFERENCE
from editor_server import make_server
from rendering import prose_html

class EditorTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.MarkdownExplorerTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.page('statement.md', 'Before.\n\n::: theorem result:bound name="Readable bound"\nOriginal $n\\le n$.\n:::\n\nAfter.\n\n{{ generated:results }}', kind='theory', id='bound', title='A bound', result_ids=['bound'])
        Explorer(self.fixture.site, self.fixture.content).build()
        self.catalog = Catalog(self.fixture.site, self.fixture.content)
        self.store = Store(self.catalog, self.fixture.root / 'editor.sqlite3')
        self.addCleanup(self.store.db.close)
        self.pid = self.catalog.routes['/explore/theory/bound/']
        self.sid = REFERENCE.findall(self.store.get(self.pid)['object']['body_markdown'])[0]

    def proposal(self, oid=None, **fields):
        oid = oid or self.sid
        state = self.store.get(oid)
        return {'idempotency_key': str(uuid.uuid4()), 'explanation': 'Clarify the hypotheses.',
                'changes': [{'operation': 'update_' + state['object']['type'], 'id': oid, 'base_revision': state['revision'], 'fields': fields or {'body_markdown': 'Revised $n\\le n$.'}}]}

    def test_page_editor_has_statement_references_and_preserves_reading_view(self):
        page = self.store.get(self.pid)['object']
        self.assertNotIn('Original $', page['body_markdown'])
        self.assertIn('{{ statement:', page['body_markdown'])
        rendered = self.store.preview(page)
        self.assertEqual(rendered.count('Original'), 1)
        self.assertIn('data-statement-id="' + self.sid + '"', rendered)
        self.assertNotIn('N.bound (n : Nat)', rendered)
        self.assertIn('N.bound (n : Nat)', self.store.preview(self.store.get(self.sid)['object']))
        self.assertIn('Before.', rendered)
        self.assertIn('After.', rendered)

    def test_draft_does_not_create_revision_or_modify_sources(self):
        path = self.fixture.content / 'statement.md'
        source = path.read_bytes()
        current = self.store.get(self.sid)
        self.store.draft(self.sid, current['revision'], {'body_markdown': 'Draft only.'})
        self.assertEqual(len(self.store.history(self.sid)), 1)
        self.assertEqual(self.store.get(self.sid)['revision'], current['revision'])
        self.assertEqual(path.read_bytes(), source)
        self.assertEqual(self.store.db.execute('SELECT count(*) FROM drafts').fetchone()[0], 1)

    def test_revisions_are_idempotent_conflicts_do_not_overwrite_and_history_restores(self):
        proposal = self.proposal()
        before = self.store.get(self.sid)
        response = self.store.propose(proposal)
        self.assertEqual(self.store.propose(proposal), response)
        self.assertEqual(len(self.store.history(self.sid)), 2)
        conflict = copy.deepcopy(proposal); conflict['idempotency_key'] = str(uuid.uuid4())
        with self.assertRaises(Conflict): self.store.propose(conflict)
        with self.assertRaises(Conflict): self.store.draft(self.sid, before['revision'], {'body_markdown': 'Stale draft'})
        restore = self.proposal(body_markdown=before['object']['body_markdown'])
        self.store.propose(restore)
        self.assertEqual(len(self.store.history(self.sid)), 3)
        old = self.store.get(self.sid, response['revisions'][self.sid])
        self.assertEqual(old['object']['body_markdown'], 'Revised $n\\le n$.')
        self.assertEqual(self.store.get(self.sid)['object']['body_markdown'], before['object']['body_markdown'])

    def test_invalid_multi_object_proposal_is_atomic(self):
        proposal = self.proposal()
        second = self.proposal(self.pid, body_markdown='{{ generated:unknown }}')['changes'][0]
        proposal['changes'].append(second)
        with self.assertRaises(ValueError): self.store.propose(proposal)
        self.assertEqual(len(self.store.history(self.sid)), 1)
        self.assertEqual(self.store.db.execute('SELECT count(*) FROM proposals').fetchone()[0], 0)

    def test_two_editors_cannot_silently_replace_each_others_draft(self):
        current = self.store.get(self.sid)
        saved = self.store.draft(self.sid, current['revision'], {'body_markdown': 'First draft'})
        with self.assertRaises(Conflict):
            self.store.draft(self.sid, current['revision'], {'body_markdown': 'Second editor'})
        newer = self.store.draft(self.sid, current['revision'], {'body_markdown': 'First editor continues'}, saved['draft_revision'])
        with self.assertRaises(Conflict):
            self.store.draft(self.sid, current['revision'], {'body_markdown': 'Stale draft'}, saved['draft_revision'])
        self.assertNotEqual(saved['draft_revision'], newer['draft_revision'])

    def test_new_external_result_and_page_can_be_saved_together_and_reopened(self):
        sid = str(uuid.uuid4())
        proposal = self.proposal(self.pid, body_markdown='New exposition.\n\n{{ statement:' + sid + ' }}')
        proposal['changes'].append({'operation': 'create_statement', 'id': sid, 'base_revision': None, 'fields': {
            'title': 'An external result', 'body_markdown': 'A result with $x=1$.', 'proofs': [
                {'label': 'Paper', 'url': 'https://doi.org/10.1000/example', 'locator': 'Theorem 2, version 1'}]}})
        response = self.store.propose(proposal)
        html = self.store.preview(self.store.get(self.pid)['object'])
        self.assertIn('An external result', html)
        self.assertIn('No linked Lean statement.', self.store.preview(self.store.get(sid)['object']))
        self.assertNotIn('N.bound (', html)
        reopened = Store(Catalog(self.fixture.site, self.fixture.content), self.fixture.root / 'editor.sqlite3')
        self.addCleanup(reopened.db.close)
        self.assertEqual(reopened.get(sid)['object']['title'], 'An external result')
        self.assertEqual(reopened.get(self.pid)['revision'], response['revisions'][self.pid])

    def test_page_revision_pins_statement_versions(self):
        response = self.store.propose(self.proposal(self.pid, title='Revised page'))
        old_page = self.store.get(self.pid, response['revisions'][self.pid])
        self.store.propose(self.proposal(body_markdown='A newer statement.'))
        pinned = self.store.preview(old_page['object'], lambda sid: self.store.get(sid, old_page['dependencies'].get(sid)))
        self.assertIn('Original', pinned)
        self.assertNotIn('A newer statement', pinned)
        self.assertIn('A newer statement', self.store.preview(self.store.get(self.pid)['object']))

    def test_source_change_is_detected_after_restart(self):
        self.store.propose(self.proposal())
        path = self.fixture.content / 'statement.md'
        path.write_text(path.read_text().replace('Original', 'Upstream edit'))
        reopened = Store(Catalog(self.fixture.site, self.fixture.content), self.fixture.root / 'editor.sqlite3')
        self.addCleanup(reopened.db.close)
        with self.assertRaises(Conflict): reopened.get(self.sid)

    def test_agent_cannot_change_evidence_paths_or_provide_unsafe_proofs(self):
        for fields in [{'evidence': {'signature': 'False'}}, {'path': '.github/workflows/test.yml'},
                       {'proofs': [{'label': 'Unsafe', 'url': 'javascript:alert(1)', 'locator': ''}]}]:
            with self.assertRaises(ValueError): self.store.propose(self.proposal(**fields))
        rendered = self.store.preview(self.catalog.validate(self.store.get(self.sid)['object'], {'body_markdown': '<script>alert(1)</script>\n\n[bad](javascript:alert(1))'}, self.catalog.objects))
        self.assertNotIn('<script>', rendered)
        self.assertNotIn('href="javascript:', rendered)
        self.assertNotIn('href=', prose_html('[bad](javascript:alert)'))

    def test_feedback_is_versioned_and_reply_cannot_cross_objects(self):
        item = self.store.feedback(self.sid, {'kind': 'mathematical-error', 'body': 'Check $n=0$.', 'parent_id': None})
        with self.assertRaises(ValueError): self.store.feedback(self.pid, {'kind': 'comment', 'body': 'Wrong target', 'parent_id': item['id']})
        self.store.feedback(self.sid, {'kind': 'comment', 'body': 'A reply.', 'parent_id': item['id']})
        discussion = self.store.discussion(self.sid)
        self.assertEqual(len(discussion['items']), 2)
        self.assertEqual(discussion['items'][0]['revision_id'], self.store.get(self.sid)['revision'])
        self.assertIn('class="math"', discussion['items'][0]['html'])

    def test_http_origin_session_security_and_agent_workflow(self):
        server = make_server(self.fixture.site, self.fixture.content, ':memory:')
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), server.application.db.close()))
        def request(path, payload=None, headers=None):
            raw = None if payload is None else json.dumps(payload).encode()
            req = Request(server.origin + '/explore/editor-api/' + path, data=raw,
                          headers={'Content-Type': 'application/json', **(headers or {})})
            with urlopen(req) as response: return json.load(response)
        session = request('bootstrap')['session']
        alias = 'localhost:' + str(server.server_port)
        self.assertEqual(request('bootstrap', headers={'Host': alias, 'Origin': 'http://' + alias})['mode'], 'local')
        navigation = Request(server.origin + '/explore/theory/bound/', headers={'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'navigate'})
        with urlopen(navigation) as response:
            self.assertEqual(response.status, 200)
        with self.assertRaises(HTTPError) as error: request('proposals', self.proposal())
        self.assertEqual(error.exception.code, 403)
        with self.assertRaises(HTTPError) as error: request('bootstrap', headers={'Origin': 'https://evil.example'})
        self.assertEqual(error.exception.code, 403)
        response = request('proposals', self.proposal(), {'X-Editor-Session': session})
        self.assertEqual(response['status'], 'saved_locally')
        state = request('objects/' + self.sid)
        self.assertIn('Revised', state['html'])
        with urlopen(server.origin + '/explore/theory/bound/') as response:
            page = response.read().decode()
        self.assertIn('Revised', page)
        self.assertIn('/explore/editor-assets/editor.js', page)
        self.assertNotIn('Original', page)
        self.assertEqual(request('schema')['title'], 'NLA-lib local editorial proposal v1')

if __name__ == '__main__':
    unittest.main()

class IdentityTests(unittest.TestCase):
    setUp = EditorTests.setUp
    proposal = EditorTests.proposal

    def test_profile_bot_ownership_and_immutable_attribution(self):
        from editor.identities import PERSON
        bot = self.store.create_bot({'display_name':'Reference helper','bio':'Checks references','scopes':['feedback','proposals']})
        bid = bot['bot']['id']
        self.assertEqual(bot['bot']['owner_id'], PERSON)
        self.assertEqual(self.store.authenticate_bot(bot['token'])['actor']['id'],bid)
        stored=[dict(row) for row in self.store.db.execute('SELECT * FROM bot_tokens')]
        self.assertNotIn(bot['token'],json.dumps(stored))
        comment=self.store.feedback(self.sid,{'kind':'comment','body':'A bot suggestion.','parent_id':None},bid)
        revision=self.store.propose(self.proposal(),bid)
        self.assertEqual(self.store.discussion(self.sid)['items'][0]['attribution']['actor']['id'],bid)
        self.assertEqual(self.store.history(self.sid)[-1]['attribution']['responsible_person']['id'],PERSON)
        self.assertEqual(len(self.store.profile(PERSON)['activities']),2)
        self.assertEqual(len(self.store.profile(bid)['activities']),2)
        self.store.update_profile({'display_name':'Ada Example','bio':'Numerical linear algebra'})
        self.assertEqual(self.store.attribution('comment',comment['id'])['responsible_person']['display_name'],'Ada Example')
        self.store.revoke_bot(bot['token_id'])
        self.assertIsNone(self.store.authenticate_bot(bot['token']))
        self.assertEqual(self.store.attribution('revision',next(iter(revision['revisions'].values())))['actor']['id'],bid)
        with self.assertRaises(ValueError): self.store.update_profile({'website':'javascript:alert(1)'})
        with self.assertRaises(ValueError): self.store.create_bot({'display_name':'Spoof','bio':'','scopes':['admin']})

    def test_notifications_following_self_suppression_and_actor_reactions(self):
        from editor.identities import now
        self.store.follow(self.sid,True)
        with self.store.db:
            self.store.db.execute('INSERT INTO actors VALUES(?,?,?,?,?)',('other-researcher','person',None,json.dumps({'display_name':'Another researcher'}),now()))
        self.store.feedback(self.sid,{'kind':'comment','body':'A question.','parent_id':None},'other-researcher')
        self.assertEqual(self.store.inbox()['unread'],1)
        self.store.feedback(self.sid,{'kind':'comment','body':'My own reply.','parent_id':None})
        self.assertEqual(self.store.inbox()['unread'],1)
        self.store.react(self.sid,'👍',True)
        self.store.react(self.sid,'👍',True,'other-researcher')
        self.assertEqual(self.store.reactions(self.sid)[0]['count'],2)
        self.store.react(self.sid,'👍',False)
        self.assertFalse(self.store.reactions(self.sid)[0]['reacted'])
        self.assertEqual(self.store.reactions(self.sid)[0]['count'],1)
        self.store.follow(self.sid,False)
        self.store.feedback(self.sid,{'kind':'comment','body':'Another question.','parent_id':None},'other-researcher')
        self.assertEqual(self.store.inbox()['unread'],1)

    def test_bot_http_scopes_private_data_and_revocation(self):
        server=make_server(self.fixture.site,self.fixture.content,self.fixture.root/'bot-http.sqlite3')
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        self.addCleanup(server.application.db.close);self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        bot=server.application.create_bot({'display_name':'Scoped bot','bio':'Comments only','scopes':['feedback']})
        def call(path,payload=None):
            headers={'Authorization':'Bearer '+bot['token']}
            if payload is not None:headers['Content-Type']='application/json'
            request=Request(server.origin+'/explore/editor-api/'+path,data=json.dumps(payload).encode() if payload is not None else None,headers=headers)
            with urlopen(request) as response:return json.load(response)
        response=call('objects/'+self.sid+'/feedback',{'kind':'comment','body':'Scoped comment.','parent_id':None})
        self.assertIn('id',response)
        self.assertEqual(call('objects/'+self.sid+'/feedback')['items'][0]['attribution']['actor']['id'],bot['bot']['id'])
        for path,payload in [('bootstrap',None),('notifications',None),('me/workspace',None),('bots',None),('me/profile',{'display_name':'Spoof'}),('proposals',self.proposal()),('objects/'+self.sid+'/reaction',{'emoji':'👍','active':True})]:
            with self.assertRaises(HTTPError) as error:call(path,payload)
            self.assertEqual(error.exception.code,403,path)
        state=server.application.get(self.sid)
        server.application.draft(self.sid,state['revision'],{'body_markdown':'A private draft.'})
        self.assertIsNone(call('objects/'+self.sid)['draft'])
        server.application.revoke_bot(bot['token_id'])
        with self.assertRaises(HTTPError) as error:call('objects/'+self.sid)
        self.assertEqual(error.exception.code,401)

    def test_invalid_notation_can_be_drafted_but_not_submitted(self):
        state=self.store.get(self.sid)
        self.store.draft(self.sid,state['revision'],{'body_markdown':'Unfinished $x^{2$'})
        with self.assertRaisesRegex(ValueError,'Mathematical notation'):
            self.store.propose(self.proposal(body_markdown='Unfinished $x^{2$'))
        self.assertEqual(self.store.get(self.sid)['revision'],state['revision'])
