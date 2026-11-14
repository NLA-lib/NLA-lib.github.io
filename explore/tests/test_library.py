"""The Markdown pipeline consumes extraction metadata without an execution registry."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

import build
import library
from content_pages import load_pages


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.content = self.root / 'content'
        self.content.mkdir()
        for name in ['algorithms', 'theory', 'library', 'search']:
            self.page(name + '.md', f'kind: index\nid: {name}\ntitle: {name.title()}', '')
        self.page('index.md', 'kind: home\nid: home\ntitle: Explorer', '{{ generated:entry-points }}')
        self.page('method.md', 'kind: algorithm\nid: method\ntitle: Method\nlibrary_algorithm: method',
                  '{{ generated:results }}')
        self.data = {'schema': 1, 'commit': 'a' * 40, 'date': '2026-11-13',
            'modules': [{'name': 'N', 'path': 'N.lean', 'doc': '# A module', 'imports': ['Mathlib']}],
            'decls': [
                {'name': 'N.method', 'module': 'N', 'kind': 'def', 'signature': 'N.method : Nat',
                 'statement': 'def method := 7', 'doc': '**Method.**\nAlgorithm: method', 'line': 1},
                {'name': 'N.bound', 'module': 'N', 'kind': 'theorem', 'signature': 'N.bound (n : Nat) : n ≤ n',
                 'statement': 'N.bound := by SENTINEL_PROOF', 'doc': '**A bound.**\nResult: bound',
                 'typeDeps': ['N.method'], 'valueDeps': ['N.proofHelper'], 'line': 2},
                {'name': 'N.proofHelper', 'module': 'N', 'kind': 'theorem', 'signature': 'N.proofHelper : True', 'line': 3}]}

    def page(self, path, front, body):
        (self.content / path).write_text('---\n' + front + '\n---\n\n' + body)

    def model(self, **options):
        return library.make_records(self.data, load_pages(self.content), **options)

    def test_exact_signatures_dependencies_fingerprints_and_proof_separation(self):
        model = self.model()
        d = model['records']['declarations']['N.bound']
        self.assertEqual(d['signature'], self.data['decls'][1]['signature'])
        self.assertEqual(d['signature_sha256'], hashlib.sha256(d['signature'].encode()).hexdigest())
        self.assertEqual(d['statement'], d['signature'])
        self.assertNotIn('SENTINEL_PROOF', json.dumps(d))
        self.assertEqual(d['statement_dependencies'], ['N.method'])
        self.assertEqual(d['proof_or_value_dependencies'], ['N.proofHelper'])
        self.assertEqual(model['records']['declarations']['N.method']['statement_callers'], ['N.bound'])
        self.assertIn('/blob/' + 'a' * 40 + '/N.lean#L2', d['source']['url'])
        self.assertEqual(model['records']['algorithms']['method']['results'], ['bound'])
        self.assertNotIn('implementations', model['records'])
        self.assertNotIn('bounds', model['records'])

    def test_no_commit_never_manufactures_source_links_and_admissions_stay_visible(self):
        self.data['commit'] = None
        self.data['decls'][1]['sorry'] = True
        model = self.model()
        self.assertFalse(model['snapshot']['versioned'])
        d = model['records']['declarations']['N.bound']
        self.assertTrue(d['admission_reported'])
        self.assertIsNone(d['source']['url'])

    def test_dirty_metadata_cannot_publish_new_paths_under_its_base_commit(self):
        self.data['dirty'] = True
        self.data['decls'][1]['module'] = 'N.NewModule'
        model = self.model()
        self.assertFalse(model['snapshot']['versioned'])
        self.assertEqual(model['snapshot']['kind'], 'working-tree-preview')
        self.assertIsNone(model['snapshot']['commit'])
        self.assertEqual(model['snapshot']['base_commit'], 'a' * 40)
        self.assertIsNone(model['records']['declarations']['N.bound']['source']['url'])
        with patch.object(build, 'load_toml', return_value={}):
            build.build(self.data, {}, self.root / 'site', content=self.content)
        self.assertIn('working-tree preview', (self.root / 'site/index.html').read_text())
        self.data['dirty'] = 'false'
        with self.assertRaisesRegex(ValueError, 'dirty flag'):
            self.model()

    def test_result_aliases_primary_validation_and_rename_redirects(self):
        self.data['decls'][1]['doc'] = '**A bound.**\nResult: old-bound'
        model = self.model(overrides={'old-bound': {'merge_into': 'bound'}, 'bound': {'primary': 'N.bound'}},
            rename_maps=[('rename', [{'old': 'N.old', 'new': 'N.bound'}], ['N.bound'])])
        out = self.root / 'site'
        library.publish(model, out)
        links = json.loads((out / 'api/v1/legacy-links.json').read_text())
        self.assertEqual(links['results']['old-bound'], links['results']['bound'])
        self.assertEqual(links['declarations']['N.old'], links['declarations']['N.bound'])
        self.assertEqual(model['records']['declarations']['N.bound']['statement_changed'], ['rename'])
        self.assertIn('/library/declarations/N.bound/', (out / 'library/declarations/N.old/index.html').read_text())
        self.assertIn('/library/results/bound/', (out / 'library/results/old-bound/index.html').read_text())
        self.assertFalse((out / 'library/declarations/N.bound/index.html').exists())
        with self.assertRaisesRegex(ValueError, 'primary declaration'):
            self.model(overrides={'old-bound': {'primary': 'N.missing'}})
        with self.assertRaisesRegex(ValueError, 'cycle'):
            self.model(overrides={'a': {'merge_into': 'b'}, 'b': {'merge_into': 'a'}})

    def test_operator_names_are_single_components_after_http_decoding(self):
        names = ['N.«opsIdx_/_»', 'N.«opsIdx_%2F_»', 'N.«back\\slash»']
        self.data['decls'].extend(dict(name=n, module='N', kind='def', signature=n + ' : Nat') for n in names)
        out = self.root / 'site'
        model = self.model()
        library.publish(model, out)
        index = json.loads((out / 'api/v1/index.json').read_text())['declarations']
        for name in names:
            path = out / unquote(urlsplit(index[name]).path).removeprefix('/explore/')
            self.assertEqual(path.parent, out / 'api/v1/declarations')
            self.assertEqual(json.loads(path.read_text())['record']['id'], name)
        self.assertNotEqual(library.record_component(names[0]), library.record_component(names[1]))

    def test_old_execution_deletion_and_no_registry_do_not_change_the_new_pipeline(self):
        old = {'name': 'NLAlib.Computation.old', 'module': 'N', 'kind': 'def',
               'signature': 'old : Computation.Prog Unit Unit 0 0', 'doc': 'Algorithm: method'}
        for ds in [self.data['decls'] + [old], self.data['decls']]:
            data = copy.deepcopy(self.data)
            data['decls'] = ds
            out = self.root / 'site'
            with patch.object(build, 'load_toml', return_value={}):
                build.build(data, {}, out, content=self.content)
            self.assertTrue((out / 'algorithms/method/index.html').is_file())
            self.assertFalse((out / 'data.json').exists())
            self.assertFalse((out / 'app.js').exists())
            self.assertFalse((out / 'algorithms/ladder.json').exists())
            self.assertIn('location.replace', (out / 'catalog/index.html').read_text())
            self.assertNotIn('app.js', (out / 'index.html').read_text())

    def test_source_hashes_fail_closed_without_target_files(self):
        (self.root / 'N.lean').write_text('def method := 7\n')
        self.data['sourceHashes'] = {'N.lean': hashlib.sha256((self.root / 'N.lean').read_bytes()).hexdigest()}
        self.assertTrue(build.validate_sources(self.data, self.root))
        (self.root / 'N.lean').write_text('def method := 8\n')
        with self.assertRaisesRegex(ValueError, 'source hash mismatch'):
            build.validate_sources(self.data, self.root)
        self.assertFalse((self.root / 'docs/targets.toml').exists())

    def test_curated_guides_and_module_moves_remain_separate_from_method_analysis(self):
        self.data['dirty'] = True
        (self.root / 'N.lean').write_text('def method := 7\n')
        guide = self.root / 'docs/algorithms/Method.md'
        guide.parent.mkdir(parents=True)
        guide.write_text('# Method guide\n\n[The implementation](../../N.lean).\n')
        self.page('method.md', 'kind: algorithm\nid: method\ntitle: Method\nlibrary_algorithm: method\n'
                  'source_guides: [docs/algorithms/Method.md]', '{{ generated:source-guides }}')
        moves = self.root / 'module-map.json'
        moves.write_text(json.dumps({'mathematical_module_moves': {'Old.Math': {'modules': ['N'], 'note': 'Pure mathematics moved.'}}}))
        out = self.root / 'site'
        with patch.object(build, 'load_toml', return_value={}):
            model = build.build(self.data, {}, out, content=self.content, src=self.root, module_map=moves)
        record = model['records']['guides']['method']
        self.assertIsNone(record['source']['url'])
        self.assertEqual(record['source']['sha256'], hashlib.sha256(guide.read_bytes()).hexdigest())
        method = (out / 'algorithms/method/index.html').read_text()
        self.assertIn('/explore/library/guides/method/', method)
        self.assertNotIn('The implementation', method)
        self.assertIn('href="/explore/library/modules/N/"', (out / 'library/guides/method/index.html').read_text())
        self.assertEqual((out / 'library/guides/method/source.md').read_bytes(), guide.read_bytes())
        self.assertIn('Retired execution APIs are not restored', (out / 'library/module-moves/Old.Math/index.html').read_text())
        self.assertNotIn('Old.Math', model['records']['modules'])
        self.assertIn('/explore/library/module-moves/Old.Math/',
                      (out / 'library/modules/Old.Math/index.html').read_text())
        links = json.loads((out / 'api/v1/legacy-links.json').read_text())
        self.assertEqual(links['modules']['Old.Math'], '/explore/library/module-moves/Old.Math/')
        moves.write_text(json.dumps({'mathematical_module_moves': {'Old.Math': {'modules': ['Missing']}}}))
        with self.assertRaisesRegex(ValueError, 'destination absent'):
            library.make_records(self.data, load_pages(self.content), source=self.root, module_map=moves)


if __name__ == '__main__':
    unittest.main()
