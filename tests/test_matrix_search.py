"""Offline regressions for retrieval; optional real Lean integration checks."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from search.matrix import Index, check_candidate, conclusion, evaluate, shape


class MatrixSearchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data = Path(self.tmp.name) / 'data.json'
        self.data.write_text(json.dumps({'schema': 1, 'commit': 'a' * 40, 'decls': [
            {'name': 'NLAlib.specNorm_mul_le', 'kind': 'theorem', 'module': 'NLAlib.Matrix.Norms.Spectral',
             'signature': 'NLAlib.specNorm_mul_le (A B : Matrix n n ℝ) : specNorm (A * B) ≤ specNorm A * specNorm B',
             'doc': 'The spectral norm is submultiplicative.', 'line': 10, 'sorry': False},
            {'name': 'NLAlib.specNorm_nonneg', 'kind': 'theorem', 'module': 'NLAlib.Matrix.Norms.Spectral',
             'signature': 'NLAlib.specNorm_nonneg (A : Matrix n n ℝ) : 0 ≤ specNorm A',
             'doc': 'The spectral norm is nonnegative.', 'line': 20, 'sorry': False},
            {'name': 'NLAlib.deferred', 'kind': 'theorem', 'module': 'NLAlib.Matrix.Norms.Spectral',
             'signature': 'deferred : False', 'doc': 'A deferred theorem.', 'line': 30, 'sorry': True},
            {'name': 'NLAlib.other', 'kind': 'theorem', 'module': 'NLAlib.Probability.Other',
             'signature': 'other : False', 'doc': 'Outside the prototype.', 'line': 1, 'sorry': False}
        ]}))
        self.index = Index(self.data, semantic=False)

    def test_renamed_variables_rank_the_same_declaration_first(self):
        for goal in ['specNorm (A * B) ≤ specNorm A * specNorm B',
                     'specNorm (X * Y) ≤ specNorm X * specNorm Y',
                     'specNorm (U₁ * V₂) ≤ specNorm U₁ * specNorm V₂']:
            hits = self.index.search(goal, mode='lexical')
            self.assertEqual(hits[0]['name'], 'NLAlib.specNorm_mul_le')
            self.assertIn('unverified', hits[0]['reasons'][-1])

    def test_repeated_variables_are_not_collapsed(self):
        self.assertNotEqual(shape('f X X'), shape('f X Y'))
        self.assertNotEqual(shape('0 ≤ norm X'), shape('1 ≤ norm X'))
        self.assertNotEqual(shape('X : ℝ'), shape('X : ℂ'))

    def test_binder_colons_do_not_hide_conclusion(self):
        self.assertEqual(conclusion('f.{u} {n : Type u} [Fintype n] (x : n) : x = x'), 'x = x')

    def test_empty_query_and_unknown_mode(self):
        self.assertEqual(self.index.search(' ', mode='lexical'), [])
        with self.assertRaises(ValueError):
            self.index.search('x', mode='unknown')

    def test_scaffolds_and_other_layers_excluded(self):
        self.assertEqual(len(self.index.decls), 2)

    def test_snapshot_links_and_no_silent_semantic_fallback(self):
        hit = self.index.search('NLAlib.specNorm_mul_le', mode='lexical')[0]
        self.assertIn('/' + 'a' * 40 + '/', hit['source'])
        self.assertEqual(hit['verification'], 'not checked')
        with self.assertRaises(ValueError):
            self.index.search('spectral norm', mode='semantic')

    def test_benchmark_unknown_targets_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(self.index, [{'id': 'bad', 'query': 'rank zero', 'expected': ['missing']}])

    def test_primed_declaration_names_are_valid(self):
        process = Mock(returncode=0)
        process.communicate.return_value = (json.dumps({'severity': 'information',
            'data': "'matrixSearchVerified' depends on axioms: [propext]"}), '')
        with patch('search.matrix.subprocess.Popen', return_value=process):
            r = check_candidate('.', {'name': "NLAlib.rangeProjector_mul_rangeProjector_of_range_le'",
                                      'module': 'NLAlib.Matrix.Basic.Projector'}, 'True')
        self.assertEqual(r['status'], 'checked against local build')

    def test_admitted_or_custom_axiom_results_rejected(self):
        for axiom in ['sorryAx', 'untrustedAxiom']:
            process = Mock(returncode=0)
            process.communicate.return_value = (json.dumps({'severity': 'information',
                'data': f"'matrixSearchVerified' depends on axioms: [{axiom}]"}), '')
            with patch('search.matrix.subprocess.Popen', return_value=process):
                r = check_candidate('.', {'name': 'candidate', 'module': 'Module'}, 'True')
            self.assertEqual(r['status'], 'not established')


@unittest.skipUnless(os.environ.get('MATRIX_SEARCH_LEAN_REPO'), 'Set MATRIX_SEARCH_LEAN_REPO for Lean checks')
class LeanIntegrationTests(unittest.TestCase):
    repo = os.environ.get('MATRIX_SEARCH_LEAN_REPO')
    candidate = {'name': 'NLAlib.specNorm_mul_le', 'module': 'NLAlib.Matrix.Norms.Spectral'}

    def test_arbitrary_variable_names(self):
        r = check_candidate(self.repo, self.candidate,
                            'NLAlib.specNorm (leftMatrix * rightMatrix) ≤ '
                            'NLAlib.specNorm leftMatrix * NLAlib.specNorm rightMatrix',
                            '(leftMatrix rightMatrix : Matrix (Fin 2) (Fin 2) ℝ)')
        self.assertEqual(r['status'], 'checked against local build', r)

    def test_reordered_hypotheses(self):
        candidate = {'name': 'le_trans', 'module': 'NLAlib.Matrix.Norms.Spectral'}
        r = check_candidate(self.repo, candidate, 'first ≤ third',
                            '(first second third : ℝ) (hSecond : second ≤ third) '
                            '(hFirst : first ≤ second)')
        self.assertEqual(r['status'], 'checked against local build', r)

    def test_reordered_matrix_hypotheses(self):
        candidate = {'name': 'Matrix.IsHermitian.add', 'module': 'NLAlib.Matrix.Spectral.Eigenvalues'}
        r = check_candidate(self.repo, candidate, '(firstMatrix + secondMatrix).IsHermitian',
                            '(firstMatrix secondMatrix : Matrix (Fin 2) (Fin 2) ℝ) '
                            '(hSecond : secondMatrix.IsHermitian) (hFirst : firstMatrix.IsHermitian)')
        self.assertEqual(r['status'], 'checked against local build', r)

    def test_false_goal_not_verified(self):
        r = check_candidate(self.repo, self.candidate, 'NLAlib.specNorm X < 0',
                            '(X : Matrix (Fin 2) (Fin 2) ℝ)')
        self.assertEqual(r['status'], 'not established', r)

    def test_local_assumption_cannot_masquerade_as_candidate_application(self):
        r = check_candidate(self.repo, self.candidate, 'False', '(h : False)')
        self.assertEqual(r['status'], 'not established', r)


if __name__ == '__main__':
    unittest.main()
