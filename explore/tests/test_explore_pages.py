"""Execution evidence, formal API fidelity and canonical routes are separate contracts."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

import explore_pages as E
from test_build import b, decl


class ExplorePagesTests(unittest.TestCase):
    def declarations(self):
        return [
            decl('N.spec', 'The specification.\nAlgorithm: cg (specification)', kind='def',
                 signature='N.spec : Nat → Nat'),
            decl('N.run', 'An abstract run.\nAlgorithm: cg (run model)', kind='structure',
                 signature='N.run : Type'),
            decl('N.program', 'A tree.\nAlgorithm: cg', kind='def',
                 signature='N.program : Computation.Prog Unit Unit 1 2'),
            decl('N.abstractBound', 'Conditional bound.\nResult: cg-abstract',
                 signature='N.abstractBound (r : N.run) : True', typeDeps=['N.run']),
            decl('N.execution', 'Successful execution of the tree.',
                 signature='N.execution : ∃ r : N.run, Exec N.program r',
                 typeDeps=['N.program', 'N.run']),
            decl('N.output', 'Output guarantee for the tree.',
                 signature='N.output : Correct N.program', typeDeps=['N.program']),
            decl('N.γ_bound\'', 'A supporting lemma without a Result tag.',
                 signature="N.γ_bound' {α : Type} [Inhabited α] (n : Nat) : n ≤ n"),
        ]

    def connection(self, ds):
        by_name = {d['name']: d for d in ds}
        return {'id': 'cg-rounded', 'algorithm': 'cg', 'program': 'N.program',
                'run_model': 'N.run', 'execution_theorem': 'N.execution',
                'output_theorems': ['N.output'], 'arithmetic': 'scalar rounding contract',
                'access_model': 'stored entries', 'scope': 'Explicit input assumptions.',
                'external_services': 'Scalar arithmetic and ROM.',
                'signatures': {n: E.fingerprint(by_name[n]['signature'])
                               for n in ['N.execution', 'N.output']}}

    def build(self, ds, config=None, commit=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        out = Path(tmp.name) / 'site'
        cfg = {'explore.toml': config or {}}
        with patch.object(b, 'load_toml', side_effect=lambda name: cfg.get(name, {})):
            b.build({'decls': copy.deepcopy(ds), 'commit': commit,
                     'modules': [{'name': 'NLAlib.Test', 'path': 'NLAlib/Test.lean'}]}, {}, out)
        return out

    def record(self, out, kind, name):
        return json.loads((out / 'api/v1' / kind / (name + '.json')).read_text())

    def test_abstract_bound_and_program_do_not_create_execution_claim(self):
        out = self.build(self.declarations())
        record = self.record(out, 'algorithms', 'cg')['record']
        self.assertEqual(record['implementations'], [])
        page = (out / 'algorithms/conjugate-gradient/index.html').read_text()
        self.assertIn('No execution connection is recorded', page)
        self.assertIn('cg-abstract', page)

    def test_result_heading_typesets_math_and_escapes_text(self):
        ds = self.declarations()
        ds[3]['doc'] = '**A bound for $k\\varepsilon \\le 1/100$ and <unsafe>.**\nResult: cg-abstract'
        out = self.build(ds)
        page = (out / 'results/cg-abstract/index.html').read_text()
        self.assertIn('<h2 class="page-title">A bound for <span class="math">k\\varepsilon \\le 1/100</span> and &lt;unsafe&gt;', page)

    def test_reviewed_program_connection_is_explicit_and_complete(self):
        ds = self.declarations()
        connection = self.connection(ds)
        connection['service_definitions'] = [{'text': 'Scalar arithmetic', 'declaration': 'N.run'}]
        out = self.build(ds, {'implementations': [connection]})
        i = self.record(out, 'implementations', 'cg-rounded')['record']
        self.assertEqual(i['execution_theorem'], 'N.execution')
        self.assertEqual(i['output_theorems'], ['N.output'])
        self.assertEqual(i['evidence'], 'reviewed-statement-link')
        self.assertNotIn('signatures', i)
        page = (out / 'algorithms/conjugate-gradient/index.html').read_text()
        self.assertIn('<a href="/explore/declarations/N.run/">Scalar arithmetic</a>', page)

    def test_stale_missing_admitted_or_non_theorem_evidence_rejected(self):
        for failure in ['changed', 'missing', 'admitted', 'not-theorem', 'no-program', 'no-run']:
            ds = self.declarations()
            connection = self.connection(ds)
            if failure == 'changed': ds[4]['signature'] += ' CHANGED'
            if failure == 'missing': ds.pop(5)
            if failure == 'admitted': ds[4]['sorry'] = True
            if failure == 'not-theorem': ds[4]['kind'] = 'def'
            if failure == 'no-program': ds[4]['typeDeps'] = ['N.run']
            if failure == 'no-run': ds[4]['typeDeps'] = ['N.program']
            with self.subTest(failure=failure), self.assertRaises(ValueError):
                self.build(ds, {'implementations': [connection]})

    def test_signatures_and_unicode_routes_survive_without_javascript(self):
        ds = self.declarations()
        out = self.build(ds, commit='a' * 40)
        name = "N.γ_bound'"
        envelope = self.record(out, 'declarations', name)
        record = envelope['record']
        self.assertEqual(record['signature'], ds[-1]['signature'])
        self.assertEqual(record['import'], 'import NLAlib.Test')
        path = unquote(urlsplit(record['url']).path).removeprefix('/explore/')
        page = (out / path / 'index.html').read_text()
        self.assertIn('Inhabited α', page)
        self.assertIn('Structured JSON record', page)
        self.assertIn('a' * 40, page)
        self.assertNotIn('proof_body', record)

    def test_unversioned_records_never_manufacture_source_links(self):
        out = self.build(self.declarations())
        env = self.record(out, 'declarations', 'N.spec')
        self.assertFalse(env['snapshot']['versioned'])
        self.assertIsNone(env['record']['source']['url'])
        self.assertEqual(len(env['snapshot']['extraction_sha256']), 64)

    def test_supporting_lemmas_remain_indexed_and_dependencies_are_separate(self):
        ds = self.declarations()
        ds[4]['valueDeps'] = ['N.output']
        out = self.build(ds)
        d = self.record(out, 'declarations', 'N.execution')['record']
        self.assertEqual(d['statement_dependencies'], ['N.program', 'N.run'])
        self.assertEqual(d['proof_or_value_dependencies'], ['N.output'])
        index = json.loads((out / 'api/v1/search-index.json').read_text())
        self.assertIn("N.γ_bound'", [x['id'] for x in index['entries']])
        self.assertIn('N.execution', self.record(out, 'declarations', 'N.program')['record']['statement_callers'])
        output = self.record(out, 'declarations', 'N.output')['record']
        self.assertIn('N.execution', output['proof_or_value_callers'])
        self.assertNotIn('N.execution', output['statement_callers'])
        page = (out / 'declarations/N.output/index.html').read_text()
        self.assertIn('Used in statement types (0)', page)
        self.assertIn('Used in proofs or definitions (1)', page)
        self.assertIn('No direct uses recorded in this snapshot.', page)

    def test_registered_guarantees_share_a_program_and_parameterized_target_is_retained(self):
        ds = self.declarations()
        out = self.build(ds)
        site = json.loads((out / 'data.json').read_text())
        common = {'target': 0, 'precomputed': [], 'reviewed': '2026-11-04', 'count': None, 'result': None}
        site['algorithms']['pages']['cg']['cost'] = [
            {**common, 'name': 'N.target', 'model': 'matrix-free', 'trees': ['N.program'], 'proof': 4},
            {**common, 'name': 'N.probTarget', 'model': 'matrix-free, with draws', 'trees': ['N.program'], 'proof': 5},
            {**common, 'name': 'N.familyTarget', 'model': 'stored entries, COO', 'trees': [], 'proof': 4},
        ]
        model = E.make_records({'decls': ds, 'modules': []}, site, {})
        implementations = list(model['records']['implementations'].values())
        self.assertEqual(len(implementations), 2)
        ordinary = next(i for i in implementations if i['program'])
        self.assertEqual(ordinary['targets'], ['N.target', 'N.probTarget'])
        self.assertEqual(ordinary['output_theorems'], ['N.execution', 'N.output'])
        family = next(i for i in implementations if not i['program'])
        self.assertEqual(family['target'], 'N.familyTarget')

    def test_result_and_algorithm_can_belong_to_multiple_categories(self):
        ds = self.declarations()
        out = self.build(ds)
        site = json.loads((out / 'data.json').read_text())
        site['collections'] = [
            {'id': key, 'title': key, 'description': '', 'groups': [
                {'entries': [{'type': 'r', 'rid': 'cg-abstract'}]}]}
            for key in ['linear-systems', 'lower-bounds']]
        model = E.make_records({'decls': ds, 'modules': []}, site, {})
        results = model['records']['results']
        self.assertEqual(results['cg-abstract']['categories'], ['linear-systems', 'lower-bounds'])
        self.assertEqual(model['records']['algorithms']['cg']['categories'], ['linear-systems', 'lower-bounds'])
        for category in ['linear-systems', 'lower-bounds']:
            self.assertIn('cg-abstract', model['records']['tasks'][category]['results'])
        self.assertEqual(results['cg-abstract']['url'], '/explore/results/cg-abstract/')

    def test_output_variant_uses_subject_not_comparison_operand(self):
        ds = [decl('NLAlib.rsvd', 'RSVD.\nAlgorithm: randomized-svd', kind='def'),
              decl('NLAlib.generalizedNystrom', 'GN.\nAlgorithm: generalized-nystrom', kind='def'),
              decl('N.lateRSVD', 'A bound.\nResult: rsvd-bound', typeDeps=['NLAlib.rsvd']),
              decl('N.lateGN', 'A comparison.\nResult: gn-bound',
                   typeDeps=['NLAlib.generalizedNystrom', 'NLAlib.rsvd']),
              decl('N.rsi', 'A composed method.\nResult: rsi-bound', typeDeps=['NLAlib.rsvd'])]
        out = self.build(ds)
        site = json.loads((out / 'data.json').read_text())
        for d in site['decls']:
            if d['n'] in {'N.lateRSVD', 'N.lateGN'}:
                d['fc'] = {'algorithm': 'RSVD' if d['n'] == 'N.lateRSVD' else 'GN', 'output': 'late'}
            if d['n'] == 'N.rsi':
                d['fc'] = {'algorithm': 'RSI', 'output': 'plain'}
        model = E.make_records({'decls': ds, 'modules': []}, site, {})
        algorithms = model['records']['algorithms']
        self.assertEqual(algorithms['randomized-svd']['output_variants'][0]['declarations'], ['N.lateRSVD'])
        self.assertEqual(algorithms['generalized-nystrom']['output_variants'][0]['declarations'], ['N.lateGN'])
        self.assertEqual(algorithms['rsi']['url'], '/explore/algorithms/rsi/')
        self.assertEqual(algorithms['rsi']['statement_declarations'], ['N.rsi'])
        self.assertEqual(algorithms['rsi']['members'], [])


if __name__ == '__main__':
    unittest.main()
