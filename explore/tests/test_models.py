"""Model facts come from signature hypotheses, the certificate record, or an extraction field."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import build
import library
import models
from content_pages import load_pages

STD, EXACT, BLAS = 'NLAlib.Ops.StdModel', 'NLAlib.Ops.ExactModel', 'NLAlib.Ops.IsBlas1'
LINE = ' hyps=2 uniform=yes confined=yes charged=no budget=manifest work=closed scratch=manifest'


class DetectorTests(unittest.TestCase):
    def test_binders_are_the_named_explicit_hypotheses_before_the_conclusion(self):
        signature = ('N.t {K : Type} [Inhabited K] (M : Ops.Machine K) (u : ℝ)\n  (hM :\n    Ops.StdModel u id M)\n'
                     '  (h : ∀ (d : ℕ), dom d → 0 < f d) :\n  ∃ x, (y : Ops.ExactModel id M) → x = 0')
        self.assertEqual(models.binders(signature),
                         ['Ops.Machine K', 'ℝ', 'Ops.StdModel u id M', '∀ (d : ℕ), dom d → 0 < f d'])
        self.assertEqual(models.binders('N.c : Nat'), [])
        self.assertEqual(models.binders(None), [])

    def test_a_hypothesis_needs_the_dependency_and_an_unambiguous_printed_head(self):
        signature = 'N.t (M : Ops.Machine ℝ) (hM : Ops.StdModel u id M) : True'
        self.assertTrue(models.assumes(signature, [STD], STD))
        self.assertFalse(models.assumes(signature, [], STD))
        self.assertFalse(models.assumes(signature, [STD, 'Other.Ops.StdModel'], STD))
        # In the conclusion, under a negation or inside another hypothesis it is not assumed.
        for other in ['N.t : Ops.StdModel 0 id M', 'N.t (h : ¬Ops.StdModel u id M) : True',
                      'N.t (h : ∀ M, Ops.StdModel u id M → P M) : True', 'N.t {h : Ops.StdModel u id M} : True']:
            self.assertFalse(models.assumes(other, [STD], STD), other)

    def test_exact_arithmetic_is_an_exact_machine_or_the_exact_scheme(self):
        scheme = ['NLAlib.Ops.Standard.Model', 'NLAlib.Ops.Standard.Scheme']
        exact = 'N.a (model : Ops.Standard.Model P n) (hExact : model.scheme = Ops.Standard.Scheme.exact) : Ops.Algorithm model.access S'
        self.assertTrue(models.exact_arithmetic('N.t (hE : Ops.ExactModel id M) : True', [EXACT]))
        self.assertTrue(models.exact_arithmetic(exact, scheme))
        self.assertFalse(models.exact_arithmetic('N.t (s : Ops.Standard.Scheme) : s = Ops.Standard.Scheme.exact', scheme))
        self.assertFalse(models.exact_arithmetic('N.t (h : Ops.ExactModel.toStd x) : True', [EXACT]))
        # A model built on the exact machine is not unfolded: no fact.
        self.assertFalse(models.exact_arithmetic('N.a : Ops.Algorithm (Ops.ExactBlas.model P cost) S', ['NLAlib.Ops.ExactBlas.model']))

    def test_standard_model_is_a_std_model_hypothesis_or_a_standard_operation_model(self):
        scheme = ['NLAlib.Ops.Standard.Model', 'NLAlib.Ops.Standard.Scheme']
        self.assertTrue(models.standard_model('N.t (hM : Ops.StdModel u id M) : True', [STD]))
        self.assertTrue(models.standard_model('N.a (model : Ops.Standard.Model P n) : Ops.Algorithm model.access S', scheme))
        self.assertFalse(models.standard_model(
            'N.a (model : Ops.Standard.Model P n) (h : model.scheme = Ops.Standard.Scheme.exact) : True', scheme))
        self.assertFalse(models.standard_model('N.t (h : Ops.ExactModel id M) : Ops.StdModel 0 id M', [STD, EXACT]))

    def test_relative_error_blas_matvec_primitive_and_tape_law_are_hypotheses(self):
        self.assertTrue(models.relative_error_blas('N.t (hB : Ops.IsBlas1 dec ε ok I) : True', [BLAS]))
        self.assertFalse(models.relative_error_blas('N.t (hB : Ops.IsExactBlas1 dec ok I) : True', ['NLAlib.Ops.IsExactBlas1']))
        self.assertTrue(models.matvec_primitive('N.t (hA : Ops.IsMatvec dec A δ I) : True', ['NLAlib.Ops.IsMatvec']))
        self.assertTrue(models.matvec_primitive('N.t (hA : Ops.IsExactMatvec dec A I) : True', ['NLAlib.Ops.IsExactMatvec']))
        self.assertTrue(models.matvec_primitive('N.a (model : Ops.Standard.Model P n) : True', ['NLAlib.Ops.Standard.Model']))
        self.assertFalse(models.matvec_primitive('N.t (h : Ops.StdModel u id M) : True', [STD]))
        self.assertTrue(models.tape_law('N.t (h : Ops.IsTapeLaw law P ξ) : True', ['NLAlib.Ops.IsTapeLaw']))
        self.assertFalse(models.tape_law('N.t : ∃ P ξ, Ops.IsTapeLaw law P ξ', ['NLAlib.Ops.IsTapeLaw']))
        self.assertFalse(models.tape_law('N.t (μ : Measure Ω) [IsProbabilityMeasure μ] : True', []))

    def test_certificate_lines_parse_strictly(self):
        lines = models.parse_certificates('N.a' + LINE + '\n\nN.b hyps=0 uniform=no confined=yes charged=yes '
                                          'budget=closed work=manifest scratch=closed\n')
        self.assertEqual(lines['N.a'], {'hyps': 2, 'uniform': True, 'confined': True, 'charged': False,
                                        'budget': 'manifest', 'work': 'closed', 'scratch': 'manifest'})
        self.assertFalse(lines['N.b']['uniform'])
        for bad in ['N.a hyps=2 uniform=yes', 'N.a' + LINE.replace('closed', 'polynomial'),
                    'N.a' + LINE + ' kernel=yes', 'N.a' + LINE + '\nN.a' + LINE, 'N.a' + LINE.replace('hyps=2', 'hyps=two')]:
            with self.assertRaisesRegex(ValueError, 'unrecognized certificate line'):
                models.parse_certificates(bad)

    def test_work_and_uniform_come_from_the_certificate_only(self):
        line = models.certificate({}, models.parse_certificates('N.a' + LINE)['N.a'])
        self.assertEqual(models.work_bound(line), 'closed')
        self.assertTrue(models.uniform_model(line))
        self.assertEqual(line['source'], models.CERTIFICATES)
        self.assertIsNone(models.certificate({}))
        self.assertIsNone(models.work_bound(None))
        self.assertFalse(models.uniform_model(None))
        # A model without a recorded Uniform instance gets no access fact: that is not an oracle.
        other = models.certificate({}, {**line, 'uniform': False, 'work': 'manifest'})
        found, _ = models.facts({'signature': 'N.a : Ops.Algorithm M S', 'typeDeps': [models.ALGORITHM]}, other)
        self.assertEqual(models.tags(found), ['work:manifest'])

    def test_extraction_fields_are_read_when_present_and_silent_when_absent(self):
        original = {'signature': 'N.a : Ops.Algorithm M S', 'typeDeps': [models.ALGORITHM]}
        self.assertEqual(models.facts(original), ([], None))
        ops = {'hyps': 0, 'uniform': True, 'confined': True, 'charged': True, 'budget': 'closed', 'work': 'closed',
               'scratch': 'closed', 'arithmetic': 'exact', 'oracle': False, 'kernels': ['NLAlib.ShiftedQR.EigenvalueKernelOp'],
               'sampling': True}
        found, line = models.facts({**original, 'ops': ops}, {'hyps': 0, 'uniform': False, 'confined': True, 'charged': True,
                                                             'budget': 'manifest', 'work': 'manifest', 'scratch': 'manifest'})
        # The line computed with the declaration replaces the recorded one.
        self.assertEqual(line['source'], 'extraction')
        self.assertEqual(models.tags(found), ['arithmetic:exact', 'access:uniform', 'access:kernel',
                                              'randomness:sampling', 'work:closed'])
        self.assertTrue(all(f['evidence'] == 'extraction' for f in found))
        self.assertEqual(models.tags(models.facts({**original, 'ops': {'oracle': True}})[0]), ['access:oracle'])
        # Malformed or unknown values establish nothing.
        for bad in [{'arithmetic': 'rounded'}, {'kernels': []}, {'kernels': 'all'}, {'oracle': 'yes'}, {'sampling': 1},
                    {'work': 'closed'}, 'closed']:
            self.assertEqual(models.facts({**original, 'ops': bad}), ([], None), bad)
        # A signature hypothesis is preferred to the reported arithmetic of the model.
        rounded = {'signature': 'N.a (hM : Ops.StdModel u id M) : Ops.Algorithm M S', 'typeDeps': [STD], 'ops': {'arithmetic': 'exact'}}
        self.assertEqual(models.tags(models.facts(rounded)[0]), ['arithmetic:standard'])

    def test_every_fact_has_a_badge(self):
        original = {'signature': 'N.t (hE : Ops.ExactModel id M) (hM : Ops.StdModel u id M) (hB : Ops.IsBlas1 dec ε ok I) '
                                 '(hA : Ops.IsMatvec dec A δ I) (hT : Ops.IsTapeLaw law P ξ) : True',
                    'typeDeps': [EXACT, STD, BLAS, 'NLAlib.Ops.IsMatvec', 'NLAlib.Ops.IsTapeLaw'],
                    'ops': {'kernels': ['N.K'], 'sampling': True}}
        found, _ = models.facts(original, models.parse_certificates('N.t' + LINE)['N.t'])
        self.assertEqual(models.tags(found), ['arithmetic:exact', 'arithmetic:standard', 'arithmetic:relative-error',
                                              'access:uniform', 'access:oracle', 'access:kernel',
                                              'randomness:tape-law', 'randomness:sampling', 'work:closed'])
        for fact in found:
            label, tip = models.FACTS[fact['facet']][fact['value']]
            self.assertTrue(label and tip)
        self.assertEqual(set(models.FACTS), set(models.FACETS))


class ModelRecordTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.content = self.root / 'content'
        self.content.mkdir()
        for name in ['algorithms', 'theory', 'library']:
            (self.content / (name + '.md')).write_text(f'---\nkind: index\nid: {name}\ntitle: {name.title()}\n---\n\n')
        (self.content / 'search.md').write_text('---\nkind: index\nid: search\ntitle: Search\n---\n\n{{ generated:search }}')
        (self.content / 'index.md').write_text('---\nkind: home\nid: home\ntitle: Explorer\n---\n\n{{ generated:entry-points }}')
        (self.content / 'method.md').write_text('---\nkind: algorithm\nid: method\ntitle: Method\nresult_ids: [run]\n---\n\n{{ generated:results }}')
        self.source = self.root / 'src'
        (self.source / 'scripts').mkdir(parents=True)
        self.data = {'schema': 1, 'commit': 'a' * 40, 'date': '2026-11-16',
            '_provenance': {'source_hashes_checked': True},
            'modules': [{'name': 'N', 'path': 'N.lean', 'doc': '', 'imports': []}],
            'decls': [
                {'name': 'N.certificate', 'module': 'N', 'kind': 'def', 'line': 1, 'doc': 'A certificate.',
                 'signature': 'N.certificate (M : Ops.Machine ℝ) (u : ℝ) (hM : Ops.StdModel u id M) : Ops.Algorithm (N.model M) N.spec',
                 'statement': 'def certificate := sorry', 'typeDeps': [models.ALGORITHM, STD]},
                {'name': 'N.run', 'module': 'N', 'kind': 'theorem', 'line': 2, 'doc': '**A run.**\nResult: run',
                 'signature': 'N.run (M : Ops.Machine ℝ) (hE : Ops.ExactModel id M) : True', 'typeDeps': [EXACT]},
                {'name': 'N.plain', 'module': 'N', 'kind': 'theorem', 'line': 3, 'doc': 'Plain mathematics.',
                 'signature': 'N.plain (n : ℕ) : n ≤ n'}]}

    def record(self, text):
        (self.source / models.CERTIFICATES).write_text(text)

    def make(self):
        return library.make_records(self.data, load_pages(self.content), source=self.source)

    def test_records_search_entries_pages_and_filters_carry_the_facts(self):
        self.record('N.certificate' + LINE + '\n')
        site = self.root / 'site'
        with patch.object(build, 'load_toml', return_value={}), contextlib.redirect_stdout(io.StringIO()):
            build.build(self.data, {}, site, content=self.content, src=self.source)
        read = lambda path: json.loads((site / 'api/v1' / path).read_text())
        certificate = read('declarations/N.certificate.json')['record']
        self.assertEqual(models.tags(certificate['model_facts']), ['arithmetic:standard', 'access:uniform', 'work:closed'])
        self.assertEqual(certificate['certificate']['hyps'], 2)
        self.assertEqual(certificate['certificate']['source'], models.CERTIFICATES)
        plain = read('declarations/N.plain.json')['record']
        self.assertEqual((plain['model_facts'], plain['certificate']), ([], None))
        # A result carries the facts of its headline declaration.
        self.assertEqual(models.tags(read('results/run.json')['record']['model_facts']), ['arithmetic:exact'])
        entries = {e['id']: e for e in read('search-index.json')['entries']}
        self.assertEqual(entries['N.certificate']['facets'], ['arithmetic:standard', 'access:uniform', 'work:closed'])
        self.assertEqual(entries['run']['facets'], ['arithmetic:exact'])
        self.assertNotIn('facets', entries['N.plain'])
        self.assertEqual(read('manifest.json')['certificate_record']['certificates'], 1)
        page = (site / 'library/declarations/N.certificate/index.html').read_text()
        for label in ['Standard model, unit roundoff u', 'Uniform model', 'Work: closed']:
            self.assertIn('>' + label + '</span>', page)
        self.assertNotIn('explorer-badge', (site / 'library/declarations/N.plain/index.html').read_text())
        self.assertIn('>Exact arithmetic</span>', (site / 'library/results/run/index.html').read_text())
        self.assertIn('>Exact arithmetic</span>', (site / 'algorithms/method/index.html').read_text())
        # The search page offers exactly the facts that occur.
        search = (site / 'search/index.html').read_text()
        self.assertIn('<select name="arithmetic" data-facet="arithmetic"><option value="">Any</option>'
                      '<option value="exact">Exact arithmetic</option><option value="standard">', search)
        self.assertIn('<select name="work" data-facet="work"><option value="">Any</option><option value="closed">Work: closed</option></select>', search)
        self.assertNotIn('data-facet="randomness"', search)
        self.assertNotIn('value="manifest"', search)

    def test_certificate_record_fails_closed(self):
        # A record naming something that is not a certificate of this extraction is not used.
        # Nor is a record in another format, such as one without the `work` field.
        for text in ['N.absent' + LINE, 'N.certificate' + LINE + '\nN.run' + LINE, 'N.plain' + LINE,
                     'N.certificate' + LINE.replace(' work=closed', '')]:
            self.record(text + '\n')
            with contextlib.redirect_stderr(io.StringIO()) as warning:
                model = self.make()
            self.assertIn('flags are not used', warning.getvalue())
            self.assertFalse(model['certificate_record']['used'])
            self.assertEqual(models.tags(model['records']['declarations']['N.certificate']['model_facts']), ['arithmetic:standard'])
        # Unverified sources: the record is not read at all.
        self.record('N.certificate' + LINE + '\n')
        self.data['_provenance']['source_hashes_checked'] = False
        model = self.make()
        self.assertIsNone(model['certificate_record'])
        self.assertIsNone(model['records']['declarations']['N.certificate']['certificate'])
        # No record in the source: signature facts only.
        self.data['_provenance']['source_hashes_checked'] = True
        (self.source / models.CERTIFICATES).unlink()
        self.assertEqual(models.tags(self.make()['records']['declarations']['N.certificate']['model_facts']), ['arithmetic:standard'])

    @unittest.skipUnless(shutil.which('node'), 'Node is needed for the browser search engine')
    def test_search_filters_require_every_chosen_fact(self):
        script = Path(__file__).resolve().parents[1] / 'web/explore-search.js'
        entries = [
            {'id': 'N.closed', 'kind': 'def', 'title': 'Counted solver', 'facets': ['arithmetic:standard', 'work:closed']},
            {'id': 'N.manifest', 'kind': 'def', 'title': 'Solver', 'facets': ['arithmetic:standard', 'work:manifest']},
            {'id': 'N.plain', 'kind': 'theorem', 'title': 'Solver bound'},
        ]
        code = ("const s=require(process.argv[1]).create(JSON.parse(require('fs').readFileSync(0,'utf8')));"
                "const ids=r=>r.entries.map(e=>e.id);"
                "process.stdout.write(JSON.stringify([ids(s('solver')),ids(s('solver','',['arithmetic:standard'])),"
                "ids(s('solver','',['arithmetic:standard','work:closed'])),ids(s('','',['work:manifest'])),"
                "ids(s('','def',['arithmetic:standard'])),ids(s('')),ids(s('solver','theorem',['work:closed']))]));")
        result = subprocess.run(['node', '-e', code, str(script)], input=json.dumps(entries), text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(result.stdout), [
            ['N.closed', 'N.manifest', 'N.plain'], ['N.closed', 'N.manifest'], ['N.closed'], ['N.manifest'],
            ['N.closed', 'N.manifest'], [], []])
