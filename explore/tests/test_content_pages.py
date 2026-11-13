"""The Markdown/metadata boundary owns routes, associations, and source fidelity."""
import json
from pathlib import Path
import tempfile
import unittest

import yaml
from content_pages import Explorer, load_pages, markdown, statement_links


class MarkdownExplorerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.content = self.root / 'content'
        self.site = self.root / 'site'
        self.site.mkdir()
        self.content.mkdir()
        (self.site / 'index.html').write_text('<!doctype html><html><head><title>Test</title></head><body class="explore-pages" data-search-version="old"><main id="content">Old explorer</main></body></html>')
        self.api = self.site / 'api/v1'
        self.api.mkdir(parents=True)
        declaration = {'id': 'N.bound', 'kind': 'theorem', 'module': 'N', 'results': ['bound'],
                       'signature': 'N.bound (n : Nat) : n ≤ n', 'docstring': 'A useful bound.',
                       'summary': 'A useful bound.', 'admission_reported': False,
                       'source': {'url': 'https://github.com/NLA-lib/nlalib'}}
        self.records = {
            'declarations': {'N.bound': declaration},
            'results': {'bound': {'id': 'bound', 'title': 'A useful bound', 'primary': 'N.bound', 'declarations': ['N.bound']}},
            'algorithms': {'lanczos': {'id': 'lanczos', 'results': ['bound']}},
            'modules': {'N': {'id': 'N', 'title': 'N', 'summary': '', 'declarations': ['N.bound']}},
            'tasks': {'eigenvalues': {'id': 'eigenvalues', 'results': ['bound'], 'definitions': []}},
        }
        for kind, records in self.records.items():
            (self.api / kind).mkdir()
            for key, record in records.items():
                (self.api / kind / (key + '.json')).write_text(json.dumps({'record': record}))
        (self.api / 'search-index.json').write_text(json.dumps({'entries': [
            {'id': 'lanczos', 'kind': 'algorithm', 'title': 'Lanczos', 'search_text': 'spectral compression', 'url': '/old/'}]}))
        for key in ['algorithms', 'theory', 'library']:
            self.page(key + '.md', kind='index', id=key, title=key.title())
        self.page('eigenvalues.md', '{{ generated:algorithms }}', kind='task', id='eigenvalues', title='Eigenvalues')
        self.page('functions.md', '{{ generated:algorithms }}', kind='task', id='functions', title='Matrix functions')
        self.page('spectral.md', '{{ generated:used-by }}', kind='theory', id='spectral', title='Spectral theory')
        self.page('lanczos.md', '{{ generated:implementations }}\n\n{{ generated:applications }}', kind='algorithm', id='lanczos', title='Lanczos',
                  tasks=['eigenvalues', 'functions'], theory=['spectral'], library_algorithm='lanczos')
        self.page('fa.md', '{{ generated:components }}', kind='algorithm', id='lanczos-fa', title='Lanczos FA', uses=['lanczos'])
        self.page('ordinary.md', 'Pseudocode will go here.', kind='implementation', id='ordinary', algorithm='lanczos', title='Ordinary Lanczos', status='placeholder')

    def page(self, path, body='Some authored prose.', **meta):
        (self.content / path).write_text('---\n' + yaml.safe_dump(meta) + '---\n' + body)

    def test_overlapping_tasks_share_one_algorithm_and_compositions_link_back(self):
        explorer = Explorer(self.site, self.content)
        explorer.build()
        canonical = '/explore/algorithms/lanczos/'
        for task in ['eigenvalues', 'functions']:
            page = (self.site / 'tasks' / task / 'index.html').read_text()
            self.assertIn('href="' + canonical + '"', page)
        page = (self.site / 'algorithms/lanczos/index.html').read_text()
        self.assertIn('/algorithms/lanczos/implementations/ordinary/', page)
        self.assertIn('/algorithms/lanczos-fa/', page)
        self.assertIn('Placeholder', (self.site / 'algorithms/lanczos/implementations/ordinary/index.html').read_text())
        self.assertIn(canonical, (self.site / 'theory/spectral/index.html').read_text())

    def test_authored_statement_uses_exact_library_evidence_and_rebuild_is_idempotent(self):
        body = '::: theorem result:bound name="Readable bound"\nThe editable bound is $n\\le n$.\n:::'
        self.page('statement.md', body, kind='theory', id='bound', title='A bound')
        for _ in range(2):
            Explorer(self.site, self.content).build()
        page = (self.site / 'theory/bound/index.html').read_text()
        self.assertIn('The editable bound', page)
        self.assertIn('N.bound (n : Nat) : n ≤ n', page)
        self.assertIn('https://github.com/NLA-lib/nlalib', page)
        entries = json.loads((self.api / 'search-index.json').read_text())['entries']
        lanczos = [e for e in entries if e['url'] == '/explore/algorithms/lanczos/']
        self.assertEqual(len(lanczos), 1)
        self.assertIn('spectral compression', lanczos[0]['search_text'])
        self.page('statement.md', body.replace('editable bound', 'revised prose'), kind='theory', id='bound', title='A bound')
        Explorer(self.site, self.content).build()
        self.assertIn('revised prose', (self.site / 'theory/bound/index.html').read_text())

    def test_family_contains_methods_and_methods_own_implementations(self):
        self.page('family.md', '{{ generated:algorithms }}', kind='family', id='krylov',
                  title='Krylov methods', tasks=['eigenvalues'])
        self.page('eigenvalues.md', '{{ generated:families }}\n\n{{ generated:algorithms }}',
                  kind='task', id='eigenvalues', title='Eigenvalues')
        self.page('lanczos.md', '{{ generated:implementations }}\n\n{{ generated:families }}',
                  kind='algorithm', id='lanczos', title='Lanczos', families=['krylov'],
                  tasks=['eigenvalues', 'functions'])
        self.page('ordinary.md', '{{ generated:mathematical-method }}', kind='implementation',
                  id='ordinary', algorithm='lanczos', title='Ordinary Lanczos')
        Explorer(self.site, self.content).build()
        task = (self.site / 'tasks/eigenvalues/index.html').read_text()
        self.assertIn('/explore/families/krylov/', task)
        self.assertNotIn('/explore/algorithms/lanczos/', task)
        other_task = (self.site / 'tasks/functions/index.html').read_text()
        self.assertIn('/explore/algorithms/lanczos/', other_task)
        family = (self.site / 'families/krylov/index.html').read_text()
        self.assertIn('/explore/algorithms/lanczos/', family)
        self.assertNotIn('/implementations/', family)
        method = (self.site / 'algorithms/lanczos/index.html').read_text()
        self.assertIn('/algorithms/lanczos/implementations/ordinary/', method)
        implementation = (self.site / 'algorithms/lanczos/implementations/ordinary/index.html').read_text()
        self.assertIn('href="/explore/algorithms/lanczos/"', implementation)
        old = (self.site / 'algorithms/lanczos/variants/ordinary/index.html').read_text()
        self.assertIn('location.search+location.hash', old)

    def test_unknown_relationship_and_duplicate_route_are_rejected(self):
        self.page('bad.md', kind='algorithm', id='bad', title='Bad', tasks=['missing'])
        with self.assertRaisesRegex(ValueError, 'unknown tasks'):
            load_pages(self.content)
        (self.content / 'bad.md').unlink()
        self.page('duplicate.md', kind='algorithm', id='lanczos', title='Duplicate')
        with self.assertRaisesRegex(ValueError, 'duplicate identity or route'):
            load_pages(self.content)

    def test_unsourced_wrong_kind_admitted_and_unknown_statements_are_rejected(self):
        for block, error in [
            ('::: theorem name="Unproved"\nA claim.\n:::', 'must name a library'),
            ('::: definition decl:N.bound\nA definition.\n:::', 'kind disagrees'),
            ('::: theorem result:missing\nA claim.\n:::', 'Unknown result'),
        ]:
            self.page('bad.md', block, kind='theory', id='bad', title='Bad')
            with self.assertRaisesRegex(ValueError, error):
                Explorer(self.site, self.content).build()
        d = self.records['declarations']['N.bound']
        d['admission_reported'] = True
        (self.api / 'declarations/N.bound.json').write_text(json.dumps({'record': d}))
        self.page('bad.md', '::: theorem decl:N.bound\nA claim.\n:::', kind='theory', id='bad', title='Bad')
        with self.assertRaisesRegex(ValueError, 'admitted declaration'):
            Explorer(self.site, self.content).build()

    def test_markdown_supports_code_math_and_nested_lists(self):
        rendered = markdown('1. First\n   - Nested\n\n`$literal$` and $Ax=b$.')
        self.assertIn('<ol>', rendered)
        self.assertIn('<ul>', rendered)
        self.assertIn('<code>$literal$</code>', rendered)
        self.assertIn('\\mathbf{A}\\mathbf{x}=\\mathbf{b}', rendered)

    def test_statements_have_stable_links_and_distinguish_arithmetic_models(self):
        body = ''.join('<section data-cg-model="' + model + '"><article class="explorer-card cg-result" '
                       'aria-label="Theorem (Convergence)"><p>A bound.</p></article></section>'
                       for model in ['exact', 'relative'])
        linked = statement_links(body)
        for model in ['exact', 'relative']:
            identifier = model + '-theorem-convergence'
            self.assertIn('id="' + identifier + '"', linked)
            self.assertIn('href="?model=' + model + '#' + identifier + '"', linked)
        self.page('statement.md', '## Guarantees\n\n::: theorem result:bound name="Readable bound"\nA bound.\n:::',
                  kind='theory', id='bound', title='Bound')
        Explorer(self.site, self.content).build()
        page = (self.site / 'theory/bound/index.html').read_text()
        self.assertIn('<details class="explorer-section" open id="section-guarantees">', page)
        self.assertIn('href="#theorem-bound"', page)
