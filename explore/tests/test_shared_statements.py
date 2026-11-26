"""Shared Markdown is a source identity, not a copy owned by a containing page."""
import json
import unittest
import test_content_pages as fixtures
from content_pages import Explorer, load_pages
from editor.model import Catalog, Store, REFERENCE
from audit_organization import visible_results

class SharedStatementTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.MarkdownExplorerTests()
        self.fixture.setUp(); self.addCleanup(self.fixture.doCleanups)
        self.content = self.fixture.content
        (self.content / 'statements').mkdir()
        self.uid = 'cae1a020-244f-4a71-9387-f73f7c5141e2'
        self.write_statement()
        for name in ['one', 'two']:
            self.fixture.page(name + '.md', 'Connecting prose.\n\n{{ statement:shared-bound }}\n\n{{ generated:results }}', kind='theory', id=name, title=name.title(), result_ids=['bound'])

    def write_statement(self, body='A shared $n\\le n$ statement.'):
        (self.content / 'statements' / 'bound.md').write_text('---\nkind: statement\nid: shared-bound\nuid: ' + self.uid + '\n---\n\n::: theorem result:bound name="Shared bound"\n' + body + '\n:::\n')

    def test_import_is_rendered_once_with_lean_evidence_and_audit_placement(self):
        explorer = Explorer(self.fixture.site, self.content); explorer.build()
        for name in ['one', 'two']:
            page = explorer.pages['theory:' + name]
            self.assertIn('{{ statement:shared-bound }}', page.source_body)
            self.assertEqual(visible_results(explorer, page), {'bound'})
            rendered = (self.fixture.site / 'theory' / name / 'index.html').read_text()
            self.assertEqual(rendered.count('A shared'), 1)
            self.assertNotIn('N.bound (n : Nat)', rendered)
            self.assertIn('N.bound (n : Nat)', (self.fixture.site / 'statements' / self.uid / 'index.html').read_text())
            self.assertIn('id="theorem-bound"', rendered)
        registry = json.loads((self.fixture.api / 'editorial-statements.json').read_text())
        self.assertEqual(registry['statements'][0]['uid'], self.uid)
        self.assertEqual(set(registry['statements'][0]['used_by']), {'/explore/theory/one/', '/explore/theory/two/'})

    def test_commentary_stays_outside_claim_and_is_preserved_by_editor(self):
        self.write_statement('A shared $n\\le n$ statement.\n\nNote: A useful interpretation with $n$ and a [link](/explore/).')
        Explorer(self.fixture.site, self.content).build()
        detail = (self.fixture.site / 'statements' / self.uid / 'index.html').read_text()
        claim_end = detail.index('</section>', detail.index('class="theorem-statement'))
        self.assertNotIn('A useful interpretation', detail[:claim_end])
        self.assertGreater(detail.index('class="statement-commentary"'), claim_end)
        self.assertEqual(detail.count('A useful interpretation'), 1)
        self.assertIn('href="/explore/"', detail[claim_end:])
        library = (self.fixture.site / 'library/results/bound/index.html').read_text()
        self.assertGreater(library.index('class="statement-commentary"'), library.index('</article>'))
        for name in ['one', 'two']:
            overview = (self.fixture.site / 'theory' / name / 'index.html').read_text()
            self.assertIn('A shared', overview)
            self.assertNotIn('A useful interpretation', overview)
        catalog = Catalog(self.fixture.site, self.content)
        obj = catalog.objects[self.uid]
        self.assertIn('Note: A useful interpretation', obj['body_markdown'])
        preview = catalog.render_statement(obj)
        self.assertGreater(preview.index('class="statement-commentary"'), preview.index('</section>'))
        self.assertNotIn('A useful interpretation', catalog.overview(obj))

    def test_source_and_local_edits_propagate_across_pages_with_one_history(self):
        Explorer(self.fixture.site, self.content).build()
        before = json.loads((self.fixture.api / 'editorial-pages.json').read_text())
        self.write_statement('Updated shared statement.')
        Explorer(self.fixture.site, self.content).build()
        after = json.loads((self.fixture.api / 'editorial-pages.json').read_text())
        catalog = Catalog(self.fixture.site, self.content); store = Store(catalog, ':memory:'); self.addCleanup(store.db.close)
        for name in ['one', 'two']:
            pid = catalog.routes['/explore/theory/' + name + '/']
            self.assertEqual(REFERENCE.findall(store.get(pid)['object']['body_markdown']), [self.uid])
            previous = next(p for p in before['pages'] if p['id'] == name)
            current = next(p for p in after['pages'] if p['id'] == name)
            self.assertEqual(previous['source_sha256'], current['source_sha256'])
            self.assertNotEqual(previous['resolved_body_sha256'], current['resolved_body_sha256'])
        current = store.get(self.uid)
        store.propose({'idempotency_key': 'shared-edit', 'explanation': 'Clarify the shared statement.', 'changes': [{'operation': 'update_statement', 'id': self.uid, 'base_revision': current['revision'], 'fields': {'body_markdown': 'One shared edit.'}}]})
        for name in ['one', 'two']:
            obj = store.get(catalog.routes['/explore/theory/' + name + '/'])['object']
            self.assertIn('One shared edit.', store.preview(obj))
        self.assertEqual(len(store.history(self.uid)), 2)

    def test_unknown_duplicate_and_nested_imports_fail_closed(self):
        for body in ['{{ statement:missing }}', '{{ statement:../../secret }}', '{{ statement:shared-bound }}\n\n{{ statement:shared-bound }}']:
            self.fixture.page('bad.md', body, kind='theory', id='bad', title='Bad')
            with self.assertRaises(ValueError): load_pages(self.content)
            (self.content / 'bad.md').unlink()
        duplicate = self.content / 'statements' / 'duplicate.md'
        duplicate.write_text((self.content / 'statements' / 'bound.md').read_text().replace('id: shared-bound', 'id: another-bound'))
        with self.assertRaisesRegex(ValueError, 'duplicate'): load_pages(self.content)
        duplicate.unlink(); self.write_statement('{{ statement:shared-bound }}')
        with self.assertRaisesRegex(ValueError, 'nested'): load_pages(self.content)

    def test_code_examples_are_literal_and_file_rename_keeps_identity(self):
        self.fixture.page('example.md', '```markdown\n{{ statement:missing }}\n```', kind='theory', id='example', title='Example')
        page = load_pages(self.content)['theory:example']
        self.assertIn('{{ statement:missing }}', page.body)
        self.assertFalse(page.statement_imports)
        (self.content / 'statements' / 'bound.md').rename(self.content / 'statements' / 'renamed.md')
        pages = load_pages(self.content)
        self.assertEqual(next(iter(pages['theory:one'].statement_imports.values())).uid, self.uid)

    def test_whole_page_markdown_roundtrips_metadata_and_shared_imports(self):
        Explorer(self.fixture.site, self.content).build()
        catalog = Catalog(self.fixture.site, self.content)
        store = Store(catalog, ':memory:'); self.addCleanup(store.db.close)
        pid = catalog.routes['/explore/theory/one/']; state = store.get(pid)
        source = self.content / 'one.md'; original = source.read_text()
        self.assertEqual(catalog.document(state['object']), original)
        document = original.replace('title: One', 'title: Revised theory page') + '\nConnecting exposition edited as Markdown.\n'
        proposal = {'idempotency_key': 'whole-page', 'explanation': 'Improve the connecting exposition.', 'changes': [{'operation': 'update_page', 'id': pid, 'base_revision': state['revision'], 'fields': {'document_markdown': document}}]}
        store.propose(proposal)
        current = store.get(pid)
        self.assertEqual(catalog.document(current['object']), document)
        self.assertEqual(current['object']['title'], 'Revised theory page')
        self.assertIn('Connecting exposition edited', store.preview(current['object']))
        self.assertIn('A shared', store.preview(current['object']))
        self.assertEqual(source.read_text(), original)
        with self.assertRaises(ValueError):
            catalog.validate(current['object'], {'document_markdown': document.replace('id: one', 'id: renamed')}, catalog.objects)

    def test_multiple_emoji_reactions_are_persistent_idempotent_and_targeted(self):
        Explorer(self.fixture.site, self.content).build()
        catalog = Catalog(self.fixture.site, self.content)
        database = self.fixture.root / 'emoji.sqlite3'
        store = Store(catalog, database); self.addCleanup(store.db.close)
        pid = catalog.routes['/explore/theory/one/']
        store.react(self.uid, '👍', True); store.react(self.uid, '👍', True)
        store.react(self.uid, '🎉', True); store.react(pid, '👀', True)
        self.assertEqual([r['emoji'] for r in store.reactions(self.uid)], ['👍', '🎉'])
        self.assertTrue(all(r['count'] == 1 and r['reacted'] for r in store.reactions(self.uid)))
        store.react(self.uid, '👍', False)
        self.assertEqual([r['emoji'] for r in store.reactions(self.uid)], ['🎉'])
        reopened = Store(Catalog(self.fixture.site, self.content), database); self.addCleanup(reopened.db.close)
        self.assertEqual([r['emoji'] for r in reopened.reactions(pid)], ['👀'])
        self.assertEqual([r['emoji'] for r in reopened.reactions(self.uid)], ['🎉'])
        with self.assertRaises(ValueError): store.react(self.uid, '<script>', True)

    def test_theorem_details_share_one_bibliography_and_keep_overviews_simple(self):
        reference = {'text': 'A. Researcher. Shared matrix result. 2025.', 'url': 'https://doi.org/10.1000/test'}
        (self.content / 'references.json').write_text(json.dumps({'schema_version': 1, 'references': {'Researcher2025': reference}}))
        source = self.content / 'statements/bound.md'
        source.write_text(source.read_text().replace('uid: ' + self.uid, 'uid: ' + self.uid + '\nreferences:\n- key: Researcher2025\n  locator: Theorem 2'))
        explorer = Explorer(self.fixture.site, self.content); explorer.build()
        detail = (self.fixture.site / 'statements' / self.uid / 'index.html').read_text()
        self.assertIn('N.bound (n : Nat)', detail)
        self.assertIn('<section class="statement-references" id="references"><h2>References</h2>', detail)
        self.assertIn('Shared matrix result', detail)
        self.assertIn('Theorem 2', detail)
        registry = json.loads((self.fixture.api / 'references.json').read_text())
        self.assertEqual(registry['references']['Researcher2025'], reference)
        for name in ['one', 'two']:
            overview = (self.fixture.site / 'theory' / name / 'index.html').read_text()
            self.assertIn('/explore/statements/' + self.uid + '/', overview)
            self.assertNotIn('Shared matrix result', overview)
            self.assertNotIn('cg-evidence', overview)
        catalog = Catalog(self.fixture.site, self.content); store = Store(catalog, ':memory:'); self.addCleanup(store.db.close)
        root = store.feedback(self.uid, {'kind': 'comment', 'body': 'A question.', 'parent_id': None})
        store.feedback(self.uid, {'kind': 'comment', 'body': 'A reply.', 'parent_id': root['id']})
        self.assertEqual(store.discussion_count(self.uid), 2)
        self.assertEqual(store.discussion(self.uid)['items'][1]['parent_id'], root['id'])
        with self.assertRaises(ValueError):
            catalog.validate(store.get(self.uid)['object'], {'references': [{'key': 'Unknown2025', 'locator': ''}]}, catalog.objects)

    def test_definition_has_own_page_and_context_links_are_not_dependencies(self):
        uid='4043a771-b174-4857-802d-a398532453f5'
        (self.content/'statements/norm.md').write_text('---\nkind: statement\nid: test-norm\nuid: '+uid+'\n---\n\n::: definition name="Test norm"\nFor $A$, define $N(A)$.\n:::\n')
        self.fixture.page('one.md','{{ statement:test-norm }}\n\n{{ statement:shared-bound }}',kind='theory',id='one',title='One',result_ids=['bound'])
        Explorer(self.fixture.site,self.content).build()
        theorem=(self.fixture.site/'statements'/self.uid/'index.html').read_text()
        definition=(self.fixture.site/'statements'/uid/'index.html').read_text()
        self.assertNotIn('<h2>Definitions</h2>',theorem)
        self.assertIn('<details class="statement-context"><summary><h2>Related results</h2>',theorem)
        self.assertIn('Definition.</p>',definition)
        self.assertIn('N(A)',definition)
        self.assertIn('<h2>Related results</h2>',definition)
        self.assertIn('href="/explore/statements/'+self.uid+'/">Shared bound</a>',definition)

    def test_lean_links_use_resolved_dependencies_and_avoid_shadowed_or_ambiguous_names(self):
        explorer=Explorer(self.fixture.site,self.content)
        for name in ['N.norm','Other.norm','N.space']:
            explorer.records['declarations'][name]={'id':name,'kind':'def','url':'/explore/library/declarations/'+name+'/'}
        declaration={'id':'N.bound','statement_dependencies':['N.norm','N.space'],
                     'signature':'N.bound (x : Nat) : norm x = N.space x'}
        rendered=explorer.linked_signature(declaration)
        self.assertIn('href="/explore/library/declarations/N.norm/"',rendered)
        self.assertIn('>norm</a> x',rendered)
        declaration['statement_dependencies'].append('Other.norm')
        ambiguous=explorer.linked_signature(declaration)
        self.assertNotIn('>norm</a>',ambiguous)
        declaration['signature']='N.bound (norm : Nat) : norm = 0'
        self.assertNotIn('<a ',explorer.linked_signature(declaration))
        declaration['signature']='N.bound : "N.norm" = "N.norm"'
        self.assertNotIn('<a ',explorer.linked_signature(declaration))
