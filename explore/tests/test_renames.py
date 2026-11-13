import json
from pathlib import Path
import tempfile
import unittest
import library as b

FIXTURES = Path(__file__).resolve().parent / 'fixtures' / 'renames'   # copies of the library's maps
SC = 'NLAlib.exists_forall_hasProjectionCostPreserving_of_hasLaw_gaussianMatrix'
OLD = 'NLAlib.integral_comp_eq_integral_integral_of_indepFun'
NEW = 'ProbabilityTheory.IndepFun.integral_comp_eq_integral_integral'


class RenameTests(unittest.TestCase):
    def test_every_map_in_the_directory_is_read(self):
        maps = b.load_rename_maps(FIXTURES)
        self.assertEqual([m[0] for m in maps], ['2026-10-consolidation', '2026-10-sketching-moments'])

    def test_entries_ahead_of_the_data_are_skipped_and_live_names_win(self):
        renamed, changed = b.rename_tables(b.load_rename_maps(FIXTURES), {OLD})
        self.assertEqual((renamed, changed), ({}, {}))   # target absent; old name still a declaration

    def test_renames_chain_across_maps_and_carry_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / '2026-09-a.json').write_text(json.dumps({'renames': [{'old': 'A', 'new': 'B', 'rule': 'N1'}], 'statementChanged': ['B']}))
            (d / '2026-10-b.json').write_text(json.dumps({'renames': [{'old': 'B', 'new': 'C', 'rule': 'N2'}], 'statementChanged': []}))
            renamed, changed = b.rename_tables(b.load_rename_maps(d), {'C'})
        self.assertEqual(renamed, {'A': ['C', False, '2026-09-a'], 'B': ['C', False, '2026-10-b']})
        self.assertEqual(changed, {'C': ['2026-09-a']})

    def test_malformed_map_and_missing_directory_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, '2026-10-x.json').write_text(json.dumps({'renames': [{'old': 'A'}]}))
            with self.assertRaises(ValueError):
                b.load_rename_maps(tmp)
        with self.assertRaises(SystemExit):
            b.load_rename_maps('/nonexistent/renames')
        self.assertEqual(b.load_rename_maps(None), [])


if __name__ == '__main__':
    unittest.main()
