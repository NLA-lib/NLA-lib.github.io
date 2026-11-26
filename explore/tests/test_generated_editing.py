"""Extracted prose can acquire a shared editorial file without changing its identity."""
import importlib.util
import json
from pathlib import Path
import unittest

import test_content_pages as fixtures
from content_pages import Explorer
from collaboration_export import export
from editor.model import Catalog, identity

spec=importlib.util.spec_from_file_location('hosted_content_for_tests',Path(__file__).resolve().parents[1]/'backend/content.py')
hosted=importlib.util.module_from_spec(spec);spec.loader.exec_module(hosted)

class GeneratedEditingTests(unittest.TestCase):
    def setUp(self):
        self.fixture=fixtures.MarkdownExplorerTests();self.fixture.setUp();self.addCleanup(self.fixture.doCleanups)
        for collection in ('results','declarations'):
            for file in (self.fixture.api/collection).glob('*.json'):
                data=json.loads(file.read_text());record=data['record']
                record['url']='/explore/library/'+collection+'/'+record['id']+'/'
                if collection=='results':record['title']='A $\\mathbf{Q}$ basis\nformula'
                file.write_text(json.dumps(data))
        Explorer(self.fixture.site,self.fixture.content).build()
        export(self.fixture.site,self.fixture.content)
        self.oid=identity('result:bound')
        self.state=json.loads((self.fixture.api/'editor/generated'/(self.oid[:2]+'.json')).read_text())[self.oid]

    def test_generated_edit_is_a_new_file_with_the_same_formal_link_and_uid(self):
        self.assertTrue(self.state['editable']);self.assertIsNone(self.state['source_sha'])
        self.assertNotIn('\n',self.state['object']['title'])
        class Snapshot:
            def references(_):return {}
        result=hosted.preview(Snapshot(),self.state,{'body_markdown':'Revised readable $n\\le n$ statement.'})
        destination=self.fixture.content/'statements'/('entry-'+self.oid+'.md')
        destination.parent.mkdir(exist_ok=True);destination.write_text(result['document_markdown'])
        catalog=Catalog(self.fixture.site,self.fixture.content)
        obj=catalog.objects[self.oid]
        self.assertEqual(obj['body_markdown'],'Revised readable $n\\le n$ statement.')
        self.assertEqual(obj['title'],self.state['object']['title'])
        self.assertEqual(obj['evidence']['declaration'],'N.bound')
        self.assertEqual(catalog.links['bound'],self.oid)
        self.assertEqual(obj['evidence']['source_file'],'statements/entry-'+self.oid+'.md')
        explorer=Explorer(self.fixture.site,self.fixture.content);explorer.build()
        for relative in ['statements/'+self.oid+'/index.html','library/results/bound/index.html','library/declarations/N.bound/index.html']:
            self.assertIn('Revised readable',(self.fixture.site/relative).read_text())
        self.assertEqual(explorer.records['declarations']['N.bound']['signature'],'N.bound (n : Nat) : n ≤ n')

    def test_generated_snapshots_stay_sharded_and_offer_editing_on_detail_pages(self):
        self.assertFalse((self.fixture.api/'editor/objects'/(self.oid+'.json')).exists())
        self.assertIn(self.oid,json.loads((self.fixture.api/'editor/generated'/(self.oid[:2]+'.json')).read_text()))
        for relative in ['statements/'+self.oid+'/index.html','library/results/bound/index.html']:
            text=(self.fixture.site/relative).read_text()
            self.assertIn('data-editor-statement="'+self.oid+'"',text)
            self.assertNotIn('data-editor-readonly="true"',text)

    def test_unlinked_statement_is_searchable_and_clearly_not_lean_verified(self):
        uid='88888888-8888-4888-8888-888888888888'
        directory=self.fixture.content/'statements';directory.mkdir(exist_ok=True)
        (directory/'unlinked.md').write_text('---\nkind: statement\nid: unlinked\nuid: '+uid+'\n---\n::: conjecture name="Standalone conjecture"\nA deliberately unproved statement.\n:::\n')
        explorer=Explorer(self.fixture.site,self.fixture.content);explorer.build()
        page=(self.fixture.site/'statements'/uid/'index.html').read_text()
        self.assertIn('Not Lean-verified',page);self.assertNotIn('Lean proof linked',page)
        entries=json.loads((self.fixture.api/'search-index.json').read_text())['entries']
        self.assertTrue(any(x['id']==uid and x['url']=='/explore/statements/'+uid+'/' for x in entries))
        explorer=Explorer(self.fixture.site,self.fixture.content);explorer.build()
        entries=json.loads((self.fixture.api/'search-index.json').read_text())['entries']
        self.assertEqual(sum(x['id']==uid for x in entries),1)

    def test_changed_readable_wording_is_not_badged_as_a_verified_translation(self):
        explorer=Explorer(self.fixture.site,self.fixture.content)
        declaration=explorer.records['declarations']['N.bound']
        self.assertIn('Lean link needs reassessment',explorer.verification_badge(declaration,True))
        self.assertIn('Lean proof linked',explorer.verification_badge(declaration,False))
        declaration['admission_reported']=True
        self.assertIn('Not Lean-verified',explorer.verification_badge(declaration,False))
