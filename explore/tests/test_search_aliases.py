"""Abbreviations should find canonical methods ahead of incidental substrings."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest


@unittest.skipUnless(shutil.which('node'), 'Node is needed for the browser search engine')
class SearchAliasTests(unittest.TestCase):
    def test_exact_method_aliases_beat_substrings(self):
        script = Path(__file__).resolve().parents[1] / 'web/explore-search.js'
        entries = [
            {'id': 'sign', 'kind': 'algorithm', 'title': 'Matrix sign iteration'},
            {'id': 'gn-method', 'kind': 'algorithm', 'title': 'Generalized Nystrom', 'aliases': ['GN']},
            {'id': 'early', 'kind': 'algorithm', 'title': 'Early-truncated generalized Nystrom (ETGN)', 'aliases': ['ETGN']},
            {'id': 'late', 'kind': 'algorithm', 'title': 'Late-truncated generalized Nystrom', 'aliases': ['TGN']},
        ]
        code = "const s=require(process.argv[1]).create(JSON.parse(require('fs').readFileSync(0,'utf8'))); process.stdout.write(JSON.stringify(['GN','TGN','ETGN'].map(q=>s(q,'algorithm').entries[0].id)));"
        result = subprocess.run(['node', '-e', code, str(script)], input=json.dumps(entries), text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(result.stdout), ['gn-method', 'late', 'early'])
