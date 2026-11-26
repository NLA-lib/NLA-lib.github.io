"""Dense program discovery and evidence, using the authored pages themselves.

Set NLA_DENSE_DATA and NLA_DENSE_SOURCE to a matching published extraction and
source archive to additionally check every linked declaration against Lean.
No extraction snapshot is copied into the repository.
"""
import json
import os
from pathlib import Path
import unittest

from content_pages import load_pages, MODEL_BLOCK
from statement_sources import STATEMENT


CONTENT = Path(__file__).resolve().parents[1] / 'content'
PROGRAMS = {
    'lu/standard': {'exact'},
    'lu/blocked': {'exact'},
    'plu/standard': {'exact', 'standard'},
    'plu/threshold': {'exact'},
    'plu/scaled': {'exact'},
    'pluq/complete-pivoting': {'exact', 'standard'},
    'pluq/rook-pivoting': {'exact', 'standard'},
    'cholesky/right-looking': {'exact', 'standard', 'finite-range'},
    'cholesky/semidefinite': {'exact'},
    'cholesky/blocked': {'exact'},
    'pivoted-cholesky/diagonal-pivoting': {'exact'},
    'ldl/standard': {'exact'},
}
METHODS = {key.split('/')[0] for key in PROGRAMS}


class DensePageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = load_pages(CONTENT)

    def test_dense_programs_are_discoverable_from_factorizations_and_systems(self):
        factorization = self.pages['task:matrix-factorizations']
        systems = self.pages['task:linear-systems']
        factor_methods = {method for group in factorization.meta['groups'] for method in group['algorithms']}
        system_methods = {method for group in systems.meta['groups'] for method in group['algorithms']}
        self.assertLessEqual(METHODS, factor_methods)
        self.assertLessEqual({'lu', 'plu', 'pluq', 'cholesky', 'ldl'}, system_methods)
        for method in METHODS:
            with self.subTest(method=method):
                page = self.pages['algorithm:' + method]
                self.assertIn('{{ generated:implementations }}', page.body)
                self.assertIn('matrix-factorizations', page.meta['tasks'])
        for identity in PROGRAMS:
            with self.subTest(program=identity):
                self.assertIn('implementation:' + identity, self.pages)

    def test_ready_programs_present_reviewed_models_in_reader_order(self):
        for identity, models in PROGRAMS.items():
            with self.subTest(program=identity):
                page = self.pages['implementation:' + identity]
                self.assertEqual(page.meta['status'], 'ready')
                self.assertEqual({model['id'] for model in page.meta['arithmetic_models']}, models)
                headings = ['Algorithm', 'Model of arithmetic', 'Operations and Storage', 'Accuracy', 'Not yet presented']
                positions = [page.body.index('## ' + heading) for heading in headings]
                self.assertEqual(positions, sorted(positions))
                self.assertIn('{{ generated:arithmetic-model-selector }}', page.body)
                if len(models) > 1:
                    self.assertEqual({match[1] for match in MODEL_BLOCK.finditer(page.body)}, models)
                self.assertNotRegex(page.body.lower(), r'preview requires|will be filled|pseudocode will|details to be added')
                # A ready page must explain instructions and have formal evidence;
                # a model badge alone does not establish a program contract.
                self.assertRegex(page.body, r'(?m)^```')
                self.assertTrue(any(match[1] == 'theorem' and match[2] in {'decl', 'result'}
                                    for match in STATEMENT.finditer(page.body)))


@unittest.skipUnless(os.environ.get('NLA_DENSE_DATA') and os.environ.get('NLA_DENSE_SOURCE'),
                     'set NLA_DENSE_DATA and NLA_DENSE_SOURCE for published-evidence checks')
class DensePublishedEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from build import validate_sources, whole_definitions
        cls.data = json.loads(Path(os.environ['NLA_DENSE_DATA']).read_text())
        # Checks all extraction-time module hashes, not merely the linked files.
        if not validate_sources(cls.data, Path(os.environ['NLA_DENSE_SOURCE'])):
            raise AssertionError('Dense evidence requires fingerprint-verified sources')
        whole_definitions(cls.data['decls'], Path(os.environ['NLA_DENSE_SOURCE']))
        cls.declarations = {declaration['name']: declaration for declaration in cls.data['decls']}
        cls.pages = load_pages(CONTENT)

    def test_all_program_listings_have_verified_definition_bodies(self):
        for identity in PROGRAMS:
            page = self.pages['implementation:' + identity]
            with self.subTest(program=identity):
                self.assertIn('{{ generated:implementation-source }}', page.body)
                names = page.meta['implementation_declarations']
                self.assertTrue(names)
                for name in names:
                    declaration = self.declarations[name]
                    self.assertNotEqual(declaration['kind'], 'theorem')
                    self.assertFalse(declaration['sorry'])
                    self.assertTrue(declaration['_definition_source_verified'])
                    self.assertIn(':=', declaration['statement'])
                    self.assertGreater(len(declaration['statement']), len(declaration['signature'].split(':')[0]))

    def test_every_authored_dense_declaration_exists_and_has_no_admission(self):
        for identity in PROGRAMS:
            page = self.pages['implementation:' + identity]
            for match in STATEMENT.finditer(page.body):
                kind, source_kind, name = match[1], match[2], match[3]
                if source_kind != 'decl':
                    continue
                with self.subTest(program=identity, declaration=name):
                    declaration = self.declarations[name]
                    self.assertFalse(declaration['sorry'])
                    self.assertTrue(declaration['signature'])
                    if kind == 'theorem':
                        self.assertEqual(declaration['kind'], 'theorem')

    def test_rounding_and_singular_variants_link_their_actual_execution_contracts(self):
        contracts = {
            'plu/standard': 'NLAlib.LU.Rounded.factorPartial_meets',
            'pluq/complete-pivoting': 'NLAlib.LU.Rounded.factorComplete_meets',
            'pluq/rook-pivoting': 'NLAlib.LU.Rounded.factorRook_meets',
            'cholesky/right-looking': 'NLAlib.Cholesky.rightLooking_meets_relative',
            'pivoted-cholesky/diagonal-pivoting': 'NLAlib.Cholesky.PivotedCertification.algorithm_checked',
            'ldl/standard': 'NLAlib.LDL.Certification.algorithm_checked',
        }
        for identity, contract in contracts.items():
            with self.subTest(program=identity):
                page = self.pages['implementation:' + identity]
                self.assertIn('decl:' + contract, page.body)
                signature = self.declarations[contract]['signature']
                self.assertTrue('.Meets I' in signature or '.Checked ' in signature)


if __name__ == '__main__':
    unittest.main()
