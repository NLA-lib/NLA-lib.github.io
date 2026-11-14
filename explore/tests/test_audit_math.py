"""Named-math coverage must follow rendered evidence and documented source changes."""
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from audit_math import audit_math


class MathCoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.source = Path(self.tmp.name)
        (self.source / 'NLAlib').mkdir()
        (self.source / 'NLAlib.lean').write_text('import NLAlib.Alpha\n')
        (self.source / 'NLAlib/Alpha.lean').write_text('/-- A bound.\nResult: bound\n-/\n/-- A method.\nAlgorithm: sample-method\n-/\n')
        paths = ['NLAlib.lean', 'NLAlib/Alpha.lean']
        self.data = {'commit': 'a' * 40, 'modules': [{'name': p[:-5].replace('/', '.'), 'path': p} for p in paths],
                     'sourceHashes': {p: hashlib.sha256((self.source / p).read_bytes()).hexdigest() for p in paths},
                     'decls': [{'name': 'N.bound', 'doc': 'A bound.\nResult: bound', 'signature': 'N.bound : True'},
                               {'name': 'N.method', 'doc': 'A method.\nAlgorithm: sample-method', 'signature': 'N.method : Nat'}]}
        self.page = SimpleNamespace(kind='algorithm', meta={'id': 'sample', 'library_algorithm': 'sample-method'},
                                    body='{{ generated:results }}', url='/explore/algorithms/sample/')
        records = {'results': {'bound': {'primary': 'N.bound'}},
                   'declarations': {'N.bound': {'results': ['bound']}, 'N.method': {'results': []}},
                   'modules': {'NLAlib': {}, 'NLAlib.Alpha': {}}}
        self.explorer = SimpleNamespace(pages={'algorithm:sample': self.page}, records=records, selection=lambda p: (['bound'], []))

    def test_unused_metadata_does_not_count_as_visible_math(self):
        self.assertEqual(audit_math(self.explorer, self.data, self.source)['issues'], [])
        self.page.body = 'An introduction with no results section.'
        result = audit_math(self.explorer, self.data, self.source)
        self.assertIn('unplaced named results', {i['check'] for i in result['issues']})

    def test_source_bound_component_accounts_for_a_tagged_method(self):
        self.page.meta.pop('library_algorithm')
        self.page.body += '\n::: definition decl:N.method name="Component"\nA checked interface.\n:::'
        self.assertEqual(audit_math(self.explorer, self.data, self.source)['issues'], [])

    def test_disappearing_declaration_requires_a_resolved_rename(self):
        baseline = {'commit': 'b' * 40, 'decls': [{'name': 'N.old', 'doc': 'Result: bound', 'signature': 'N.old : True'}]}
        result = audit_math(self.explorer, self.data, self.source, baseline=baseline)
        self.assertIn('unaccounted removed declaration', {i['check'] for i in result['issues']})
        renames = self.source / 'renames'
        renames.mkdir()
        (renames / 'math.json').write_text(json.dumps({'renames': [{'old': 'N.old', 'new': 'N.bound'}], 'statementChanged': ['N.bound']}))
        result = audit_math(self.explorer, self.data, self.source, baseline=baseline, renames=renames)
        self.assertEqual(result['issues'], [])
        self.assertTrue(result['continuity']['renamed_declarations'][0]['statement_changed'])

    def test_published_results_require_explicit_retirement_evidence(self):
        published = self.source / 'published'
        api = published / 'api/v1'
        (api / 'declarations').mkdir(parents=True)
        (api / 'results').mkdir()
        (api / 'manifest.json').write_text(json.dumps({'snapshot': {'commit': 'b' * 40}}))
        (api / 'declarations/N.legacy.json').write_text(json.dumps({'record': {
            'id': 'N.legacy', 'module': 'NLAlib.Legacy', 'kind': 'theorem'}}))
        (api / 'results/old-runtime.json').write_text(json.dumps({'record': {
            'id': 'old-runtime', 'declarations': ['N.legacy']}}))
        renames = self.source / 'renames'
        renames.mkdir()
        mapping = renames / '2026-11-ops-modules.json'
        mapping.write_text(json.dumps({'from_commit': 'b' * 40, 'retired_modules': ['NLAlib.Legacy']}))
        result = audit_math(self.explorer, self.data, self.source, renames=renames, published_baseline=published)
        self.assertEqual(result['issues'], [])
        self.assertEqual(len(result['published_baseline']['retired_execution_result_groups']), 1)
        mapping.write_text(json.dumps({'from_commit': 'b' * 40, 'retired_modules': []}))
        result = audit_math(self.explorer, self.data, self.source, renames=renames, published_baseline=published)
        self.assertIn('unaccounted published result IDs', {i['check'] for i in result['issues']})
