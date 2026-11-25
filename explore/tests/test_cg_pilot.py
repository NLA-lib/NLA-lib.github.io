"""Fail closed when the inspected core source drifts or a statement is absent."""
from pathlib import Path
import hashlib
import subprocess
import tempfile
import unittest

import json

from cg_pilot import ROUNDED, Sources, rounded_declarations
from cg_presentation import coverage_note, mathematics


class CorePreviewTests(unittest.TestCase):
    def test_source_links_require_identical_published_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = 'theorem result : True := by\n  trivial\n'
            (root / 'Example.lean').write_text(content)
            subprocess.run(['git', 'init', '-q', tmp], check=True)
            subprocess.run(['git', '-C', tmp, 'add', 'Example.lean'], check=True)
            subprocess.run(['git', '-C', tmp, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                            'commit', '-qm', 'Example'], check=True)
            revision = subprocess.check_output(['git', '-C', tmp, 'rev-parse', 'HEAD'], text=True).strip()
            subprocess.run(['git', '-C', tmp, 'update-ref', 'refs/remotes/origin/feature', revision], check=True)
            source = Sources(root, root).declaration('Example.lean', 'result')
            self.assertIn('/blob/' + revision + '/Example.lean#L1', source['github_url'])
            (root / 'Example.lean').write_text(content + '-- unpublished\n')
            self.assertIsNone(Sources(root, root).declaration('Example.lean', 'result')['github_url'])
            digest = hashlib.sha256((root / 'Example.lean').read_bytes()).hexdigest()
            self.assertIsNone(Sources(root, root, revision, {'Example.lean': digest})
                              .declaration('Example.lean', 'result')['github_url'])

    def test_archive_source_links_require_the_extraction_fingerprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            content = 'theorem result : True := by\n  trivial\n'
            (Path(tmp) / 'Example.lean').write_text(content)
            revision = 'a' * 40
            source = Sources(tmp, tmp, revision, {'Example.lean': hashlib.sha256(content.encode()).hexdigest()})
            self.assertIn('/blob/' + revision, source.declaration('Example.lean', 'result')['github_url'])
            self.assertIsNone(Sources(tmp, tmp, revision, {'Example.lean': 'wrong'}).declaration('Example.lean', 'result')['github_url'])

    def test_vector_notation_keeps_polynomials_and_probability_fonts(self):
        source = r'$A x=b,\quad p(0)=1,\quad \mathbf{P},\quad \mathbb{P}$'
        self.assertEqual(mathematics(source), source)
        for authored in [r'$\widehat x$',r'$\mathbf A\mathbf x=\mathbf b$',r'$\operatorname*{arg\,min} x$']:
            self.assertEqual(mathematics(authored),authored)

    def test_statements_exclude_proofs_and_preserve_line_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'Example.lean'
            path.write_text('namespace Example\n\ntheorem result (n : Nat) : n = n := by\n  rfl\n\n/-- Next declaration. -/\ndef next := 1\n')
            sources = Sources(tmp, tmp)
            statement = sources.declaration('Example.lean', 'result')
            self.assertEqual(statement['line'], 3)
            self.assertEqual(statement['text'], 'theorem result (n : Nat) : n = n')
            self.assertEqual(statement['url'], 'https://github.com/NLA-lib/nlalib')
            self.assertIsNone(statement['github_url'])
            self.assertEqual(len(sources.files['Example.lean']['sha256']), 64)
            with self.assertRaisesRegex(ValueError, 'Missing theorem'):
                sources.declaration('Example.lean', 'absent')
            with self.assertRaisesRegex(ValueError, 'Missing theorem'):
                sources.declaration('Example.lean', 'next')

    def test_coverage_note_names_only_rounded_results_of_the_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = Path(tmp) / 'api/v1/declarations'
            records.mkdir(parents=True)
            self.assertEqual(rounded_declarations(tmp, 'pcg'), [])
            name = ROUNDED['pcg'][1]
            (records / (name + '.json')).write_text(json.dumps({'record': {'id': name, 'url': '/explore/library/declarations/' + name + '/'}}))
            found = rounded_declarations(tmp, 'pcg')
            self.assertEqual([d['name'] for d in found], [name])
            self.assertEqual(rounded_declarations(tmp, 'reorth'), [])
        absent, present = coverage_note([]), coverage_note(found)
        # The note describes the page. It never says that the library has no rounded theorem.
        for note in [absent, present]:
            self.assertIn('No rounded execution theorem is presented for this variant', note)
            self.assertNotIn('has no rounded', note)
        self.assertNotIn('<ul>', absent)
        self.assertIn('href="/explore/library/declarations/' + name + '/"><code>' + name.removeprefix('NLAlib.') + '</code>', present)
