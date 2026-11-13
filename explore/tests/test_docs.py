"""Documentation retrieval must stay proof-free, bounded, and tied to its source snapshot."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from search.docs import Documentation, packed


class DocumentationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.module = 'NLAlib.Matrix.Norms.Spectral'
        self.relative = 'NLAlib/Matrix/Norms/Spectral.lean'
        self.source = self.root / self.relative
        self.source.parent.mkdir(parents=True)
        self.source.write_text('def toyNorm (x : Nat) : Nat := x + 17\n'
                               'theorem toyBound (x : Nat) : x ≤ x := by\n'
                               '  exact SENTINEL_PROOF_BODY\n')
        self.data = self.root / 'data.json'
        self.raw = {'schema': 1, 'commit': 'a' * 40,
                    'modules': [{'name': self.module, 'path': self.relative,
                                 'doc': '# Spectral norm\n\nAn operator norm.\n\n## Main results\n* toyBound',
                                 'imports': ['Mathlib.Data.Nat.Basic']},
                                {'name': 'NLAlib.LowRank.Demo', 'path': 'NLAlib/LowRank/Demo.lean',
                                 'doc': '# A consumer', 'imports': [self.module]}],
                    'sourceHashes': {self.relative: hashlib.sha256(self.source.read_bytes()).hexdigest()},
                    'decls': [
                        {'name': 'NLAlib.toyNorm', 'kind': 'def', 'module': self.module,
                         'doc': 'A norm used for a test.', 'signature': 'toyNorm (x : Nat) : Nat',
                         'line': 1, 'endLine': 1, 'typeDeps': [], 'valueDeps': [], 'sorry': False},
                        {'name': "NLAlib.toyBound'", 'kind': 'theorem', 'module': self.module,
                         'doc': 'A bound for the norm. ' + ('\\mathbb{R} “quoted” αβγ\n' * 250),
                         'signature': 'toyBound (x : Nat) : x ≤ x', 'line': 2, 'endLine': 3,
                         'typeDeps': ['NLAlib.toyNorm'], 'valueDeps': ['NLAlib.toyNorm'], 'sorry': False},
                        {'name': 'NLAlib.consumer', 'kind': 'theorem', 'module': 'NLAlib.LowRank.Demo',
                         'doc': 'Uses an existing matrix bound.', 'signature': 'consumer : True',
                         'line': 1, 'endLine': 1, 'typeDeps': [], 'valueDeps': ["NLAlib.toyBound'"],
                         'sorry': False},
                        {'name': 'NLAlib.admitted', 'kind': 'theorem', 'module': self.module,
                         'signature': 'admitted : False', 'line': 5, 'endLine': 5, 'sorry': True}]}
        self.data.write_text(json.dumps(self.raw))
        self.docs = Documentation(self.data, self.root, self.root / 'state')

    def collect(self, fn, **kwargs):
        out, cursor = [], None
        for _ in range(100):
            page = fn(cursor=cursor, max_chars=1500, **kwargs)
            self.assertLessEqual(len(packed(page)), 1500)
            self.assertEqual(page['range'][1] - page['range'][0], len(page['content']))
            self.assertFalse(page['proofs_included'])
            out.append(page['content'])
            cursor = page['next_cursor']
            if cursor is None:
                self.assertTrue(page['complete'])
                return ''.join(out)
        self.fail('Pagination did not terminate')

    def test_module_api_never_loads_theorem_proof(self):
        text = self.collect(self.docs.read_module, module=self.module, view='api')
        self.assertIn('toyBound (x : Nat) : x ≤ x', text)
        self.assertNotIn('SENTINEL_PROOF_BODY', text)
        self.assertNotIn('x + 17', text)
        self.assertNotIn('admitted : False', text)

    def test_exact_signature_and_docstrings_survive_pagination(self):
        text = self.collect(self.docs.read_declaration, name="NLAlib.toyBound'")
        self.assertIn(self.raw['decls'][1]['doc'], text)
        self.assertIn(self.raw['decls'][1]['signature'], text)

    def test_source_statement_retains_scoped_arguments_in_api_and_bundles(self):
        fixtures = json.loads((Path(__file__).parent / 'fixtures' / 'scoped-statements.json').read_text())
        for d in fixtures:
            d.update(doc='Scoped hypothesis regression.', sorry=False, line=1, endLine=1,
                     typeDeps=[], valueDeps=[])
            self.docs.decls[d['name']] = d
            self.docs.modules.setdefault(d['module'], {'path': d['module'].replace('.', '/') + '.lean'})
            with self.subTest(name=d['name']):
                for render, kwargs in [(self.docs.read_declaration, {'name': d['name']}),
                                       (self.docs.context, {'names': [d['name']]}),
                                       (self.docs.read_module, {'module': d['module'], 'view': 'api'})]:
                    text = self.collect(render, **kwargs)
                    self.assertIn(d['statement'], text)
                    self.assertIn('implicit arguments may be omitted', text)
                    self.assertIn('Source statement (in its module context)', text)
                    self.assertNotIn('SENTINEL_PROOF_BODY', text)

    def test_missing_source_statement_is_labeled_signature_only(self):
        for value in (None, ''):
            d = self.docs.decls['NLAlib.toyNorm']
            d['statement'] = value
            text = self.collect(self.docs.read_declaration, name=d['name'])
            self.assertIn(d['signature'], text)
            self.assertIn('Source statement unavailable', text)
            self.assertIn('implicit arguments may be omitted', text)
        d['signature'] = None
        self.assertIn('Statement and signature unavailable',
                      self.collect(self.docs.read_declaration, name=d['name']))
        d['statement'] = 'def toyNorm (x : Nat) : Nat'
        self.assertIn(d['statement'], self.collect(self.docs.read_declaration, name=d['name']))

    def test_document_that_fits_without_cursor_is_returned_in_one_page(self):
        text = 'x' * 1050
        page = self.docs.page(text, key='fits-without-cursor', max_chars=1500)
        self.assertLessEqual(len(packed(page)), 1500)
        self.assertTrue(page['complete'])
        self.assertEqual(page['content'], text)

    def test_prose_view_returns_human_documentation_without_lean_signatures(self):
        text = self.collect(self.docs.read_module, module=self.module, view='prose')
        self.assertIn('A bound for the norm.', text)
        self.assertIn("NLAlib.toyBound'", text)
        self.assertNotIn('toyBound (x : Nat)', text)
        self.assertNotIn('```lean', text)
        self.assertNotIn('SENTINEL_PROOF_BODY', text)

    def test_cursor_rejects_other_document_and_snapshot(self):
        cursor = self.docs.read_declaration("NLAlib.toyBound'", max_chars=1500)['next_cursor']
        with self.assertRaises(ValueError):
            self.docs.read_declaration('NLAlib.toyNorm', cursor=cursor)
        self.raw['date'] = 'changed extraction'
        self.data.write_text(json.dumps(self.raw))
        other = Documentation(self.data, self.root)
        with self.assertRaises(ValueError):
            other.read_declaration("NLAlib.toyBound'", cursor=cursor)

    def test_definition_requires_matching_source_bytes(self):
        r = self.docs.read_declaration('NLAlib.toyNorm', 'definition')
        self.assertIn('x + 17', r['content'])
        self.assertTrue(r['definition_source_included'])
        self.source.write_text(self.source.read_text() + '\n-- changed')
        with self.assertRaisesRegex(ValueError, 'Source hash differs'):
            self.docs.read_declaration('NLAlib.toyNorm', 'definition')

    def test_theorem_definition_view_refused(self):
        with self.assertRaisesRegex(ValueError, 'theorem proofs'):
            self.docs.read_declaration("NLAlib.toyBound'", 'definition')

    def test_missing_source_and_missing_declaration_fail_explicitly(self):
        with self.assertRaisesRegex(ValueError, 'requires --src'):
            Documentation(self.data).read_declaration('NLAlib.toyNorm', 'definition')
        with self.assertRaises(ValueError):
            self.docs.read_declaration('NLAlib.admitted')

    def test_dependencies_distinguish_statement_from_proof(self):
        r = self.docs.related('NLAlib.toyNorm', 'callers', 'both')
        self.assertIn('proof_or_value, statement', r['content'])
        r = self.docs.related("NLAlib.toyBound'", 'callers', 'proof_or_value')
        self.assertIn('NLAlib.consumer', r['content'])
        self.assertIn('consumer : True', r['content'])

    def test_catalog_discovery_and_explicit_cross_layer_read(self):
        self.assertIn('NLAlib.Matrix.Norms', self.docs.catalog()['content'])
        self.assertIn('NLAlib.Matrix', self.docs.catalog('')['content'])
        self.assertIn('NLAlib.consumer', self.docs.read_declaration('NLAlib.consumer')['content'])
        self.assertNotIn('NLAlib.consumer', self.docs.search('consumer')['content'])

    def test_bundle_is_only_requested_context(self):
        r = self.docs.context(['NLAlib.toyNorm'])
        self.assertIn('toyNorm (x : Nat)', r['content'])
        self.assertNotIn('toyBound', r['content'])

    def test_session_persists_across_restart_and_respects_snapshot(self):
        r = self.docs.session('create', goal='Find a norm bound', notes='Candidate only',
                              bookmarks=['NLAlib.toyNorm'], open_questions=['Which assumptions?'])
        session_id = r['session_id']
        fresh = Documentation(self.data, self.root, self.root / 'state')
        resumed = fresh.session('get', session_id)
        self.assertIn('Candidate only', resumed['content'])
        self.assertIn('not verified', resumed['content'])
        self.assertIn('Which assumptions?', resumed['content'])
        self.assertIn(session_id, fresh.session('list')['content'])
        self.raw['date'] = 'another extraction'
        self.data.write_text(json.dumps(self.raw))
        with self.assertRaisesRegex(ValueError, 'another snapshot'):
            Documentation(self.data, self.root, self.root / 'state').session('get', session_id)

    def test_invalid_update_does_not_erase_existing_session(self):
        r = self.docs.session('create', notes='Keep this')
        with self.assertRaises(ValueError):
            self.docs.session('update', r['session_id'], bookmarks=['missing'])
        self.assertIn('Keep this', self.docs.session('get', r['session_id'])['content'])

    def test_session_cursor_invalidated_by_update(self):
        r = self.docs.session('create', notes='A long note. ' * 900, max_chars=1500)
        self.docs.session('update', r['session_id'], notes='Revised')
        with self.assertRaises(ValueError):
            self.docs.session('get', r['session_id'], cursor=r['next_cursor'])

    def test_bad_budget_has_no_session_side_effect(self):
        with self.assertRaises(ValueError):
            self.docs.session('create', notes='Must not be stored', max_chars=50)
        self.assertFalse((self.root / 'state').exists())

    def test_source_symlink_cannot_escape_root(self):
        outside = self.root / 'outside'
        outside.mkdir()
        target = outside / 'file.lean'
        target.write_bytes(self.source.read_bytes())
        self.source.unlink()
        self.source.symlink_to(target)
        # Re-root narrowly so the symlink target is outside the configured source root.
        self.docs.source = self.root / 'NLAlib'
        self.docs.modules[self.module]['path'] = 'Matrix/Norms/Spectral.lean'
        with self.assertRaisesRegex(ValueError, 'Unsafe source path'):
            self.docs.read_declaration('NLAlib.toyNorm', 'definition')
