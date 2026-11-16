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
import rendering
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

    NOTED = ('**A bound.** For every $n$, $n \\le C n$.\nHere $C = 1$.\n\n[Key2020, Theorem 1], verbatim.\n\n'
             'Note: tight for $n = 0$.\nGeneral form: `N.general`.\n\nSecond NOTE_SENTINEL paragraph.\n\n'
             'Asymptotic: n\nResult: bound')

    def test_docstring_without_notes_block_is_unchanged(self):
        for doc in ['', '**A bound.**\nResult: bound', 'First.\n\nSee the Note: inside a line.\n\nNotes: plural.\nNote: not a paragraph start.']:
            self.assertEqual(rendering.split_notes(doc), (doc, ''))
        self.assertEqual(rendering.split_notes(None), ('', ''))
        self.assertEqual(rendering.notes_html('', str), '')
        d = self.model()['records']['declarations']['N.bound']
        self.assertEqual(d['docstring_statement'], d['docstring'])
        self.assertEqual((d['docstring_notes'], d['summary']), ('', '**A bound.**'))
        with patch.object(build, 'load_toml', return_value={}):
            build.build(self.data, {}, self.root / 'site', content=self.content)
        page = (self.root / 'site/library/declarations/N.method/index.html').read_text()
        self.assertIn('<p class="eyebrow">Library · def</p><p><strong>Method.</strong> Algorithm: method</p><pre>', page)
        for page in ['library/declarations/N.bound', 'library/results/bound', 'algorithms/method']:
            self.assertNotIn('explorer-notes', (self.root / 'site' / page / 'index.html').read_text())

    def test_notes_block_is_separated_from_the_statement_everywhere(self):
        statement, notes = rendering.split_notes(self.NOTED)
        self.assertEqual(statement, self.NOTED.split('\n\nNote:')[0] + '\n\nAsymptotic: n\nResult: bound')
        self.assertEqual(notes, 'Note: tight for $n = 0$.\nGeneral form: `N.general`.\n\nSecond NOTE_SENTINEL paragraph.')
        self.data['decls'][1]['doc'] = self.NOTED
        with patch.object(build, 'load_toml', return_value={}):
            model = build.build(self.data, {}, self.root / 'site', content=self.content)
        d = model['records']['declarations']['N.bound']
        self.assertEqual(d['docstring'], self.NOTED)
        self.assertEqual((d['docstring_statement'], d['docstring_notes']), (statement, notes))
        self.assertEqual(d['summary'], '**A bound.** For every $n$, $n \\le C n$. Here $C = 1$.')
        self.assertEqual(d['results'], ['bound'])
        self.assertEqual(d['references'][0]['key'], 'Key2020')
        site = self.root / 'site'
        search = json.loads((site / 'api/v1/search-index.json').read_text())['entries']
        entry = next(e for e in search if e['id'] == 'N.bound')
        self.assertIn('NOTE_SENTINEL', entry['search_text'])
        self.assertNotIn('NOTE_SENTINEL', entry['summary'])
        for page in ['library/declarations/N.bound', 'library/results/bound', 'algorithms/method']:
            text = (site / page / 'index.html').read_text()
            before, block = text.split('<details class="explorer-disclosure explorer-notes"><summary>Notes</summary>')
            self.assertEqual(text.count('NOTE_SENTINEL'), 1, page)
            self.assertNotIn('tight for', before)
            self.assertNotIn('Note:', text)
            self.assertIn('<div class="explorer-notes-body"><p>tight for <span class="math">n = 0</span>.', block)
            self.assertIn('NOTE_SENTINEL', block.split('</details>')[0])
            self.assertIn('Here <span class="math">C = 1</span>.', before)
        for page in ['library/declarations/N.bound', 'algorithms/method']:
            before = (site / page / 'index.html').read_text().split('explorer-notes')[0]
            self.assertIn('[Key2020, Theorem 1], verbatim.', before)
        # The statement link stays with the Lean details, not with the notes.
        method = (site / 'algorithms/method/index.html').read_text()
        self.assertLess(method.index('N.bound (n : Nat)'), method.index('statement-permalink'))

    def test_primary_is_marked_explicit_or_fallback_and_reported(self):
        self.data['decls'] += [
            {'name': 'N.a_general', 'module': 'N', 'kind': 'theorem', 'doc': '**General.**\nResult: bound sized',
             'signature': 'N.a_general {k : Type} [Fintype k] [Nonempty k] : 0 < Fintype.card k'},
            {'name': 'N.sized', 'module': 'N', 'kind': 'theorem', 'doc': 'Result: sized', 'signature': 'N.sized {k : ℕ} : k ≤ k'}]
        self.assertTrue(library.index_typed_sizes('theorem t [Nonempty k] : True'))
        self.assertTrue(library.index_typed_sizes('t : Fintype.card k = 2'))
        for signature in ['N.sized {k : ℕ} (hk : 0 < k) : k ≤ k', 'Nonempty (Fin n)', '', None]:
            self.assertFalse(library.index_typed_sizes(signature))
        fallback = self.model()['records']
        self.assertEqual((fallback['results']['bound']['primary'], fallback['results']['bound']['primary_explicit']), ('N.a_general', False))
        self.assertTrue(fallback['declarations']['N.a_general']['index_typed_sizes'])
        self.assertFalse(fallback['declarations']['N.bound']['index_typed_sizes'])
        summary = library.primary_report(fallback)
        self.assertEqual((summary['results'], summary['multiple']), (2, 2))
        self.assertEqual([(r['id'], r['primary'], r['declarations']) for r in summary['unchosen']],
                         [('bound', 'N.a_general', ['N.a_general', 'N.bound']), ('sized', 'N.a_general', ['N.a_general', 'N.sized'])])
        self.assertEqual([r['id'] for r in summary['index_typed']], ['bound', 'sized'])
        overrides = {'bound': {'primary': 'N.bound'}, 'sized': {'primary': 'N.a_general'}}
        chosen = self.model(overrides=overrides)['records']
        self.assertEqual((chosen['results']['bound']['primary'], chosen['results']['bound']['primary_explicit']), ('N.bound', True))
        summary = library.primary_report(chosen)
        self.assertEqual(summary['unchosen'], [])
        self.assertEqual([(r['id'], r['explicit']) for r in summary['index_typed']], [('sized', True)])
        import audit_primaries
        listing = audit_primaries.report(library.primary_report(fallback))
        self.assertIn('bound (2 declarations)\n  * N.a_general\n    N.bound\n', listing)
        self.assertIn('sized: N.a_general (fallback primary)', listing)

    def test_result_and_declaration_pages_mark_the_headline_and_index_typed_sizes(self):
        self.data['decls'] += [
            {'name': 'N.a_general', 'module': 'N', 'kind': 'theorem', 'doc': '**General.**\nResult: bound',
             'signature': 'N.a_general {k : Type} [Fintype k] [Nonempty k] : 0 < Fintype.card k'},
            {'name': 'N.sized', 'module': 'N', 'kind': 'theorem', 'doc': 'Result: sized',
             'signature': 'N.sized {k : Type} [Fintype k] : 0 ≤ Fintype.card k'}]
        site = self.root / 'site'
        headline = '<span class="explorer-badge explorer-badge-headline" title="The headline statement of this result.">Headline'
        general = '>General form: sizes are index types</span>'
        for overrides, mark in [({'bound': {'primary': 'N.bound'}}, headline + '</span>'), ({}, '>Headline (provisional)</span>')]:
            with patch.object(build, 'load_toml', return_value=overrides):
                build.build(self.data, {}, site, content=self.content)
            page = (site / 'library/results/bound/index.html').read_text()
            first, others = page.split('<h3 class="explorer-other-forms">Other forms</h3>')
            primary, other = ('N.bound', 'N.a_general') if overrides else ('N.a_general', 'N.bound')
            self.assertIn('(' + primary + ')', first)
            self.assertIn(mark, first)
            self.assertNotIn('(' + other + ')', first)
            self.assertIn('(' + other + ')', others)
            self.assertNotIn('>Headline', others)
            self.assertEqual(page.count(general), 1)
            self.assertIn(general, others if overrides else first)
            self.assertIn('is the number of elements of the index type k', page)
        # A single declaration is its result's headline and needs no "other forms".
        page = (site / 'library/results/sized/index.html').read_text()
        self.assertIn(headline + '</span>', page)
        self.assertIn(general, page)
        self.assertNotIn('Other forms', page)
        self.assertIn(headline + ' of sized</span>', (site / 'library/declarations/N.sized/index.html').read_text())
        self.assertIn('>Headline of bound (provisional)</span>', (site / 'library/declarations/N.a_general/index.html').read_text())
        plain = (site / 'library/declarations/N.bound/index.html').read_text()
        self.assertNotIn('explorer-badge', plain)
        self.assertNotIn('explorer-badge', (site / 'library/declarations/N.method/index.html').read_text())
        # Generated result lists show the primary; they flag only its index-typed sizes.
        method = (site / 'algorithms/method/index.html').read_text()
        self.assertEqual(method.count(general), 1)
        self.assertNotIn('>Headline', method)


if __name__ == '__main__':
    unittest.main()
