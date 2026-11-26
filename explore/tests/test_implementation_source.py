"""Implementation listings require verified definitions and never expose theorem proofs."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import yaml
import build
import library
from content_pages import Explorer, load_pages


class ImplementationSourceTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.source = self.root / 'src'
        self.source.mkdir()
        self.header = 'def program (a b c d e f g h i j k l m n : Nat) : String'
        text = ('namespace N\n' + self.header + ' := "<script>not executable HTML</script>"\n'
                'theorem claim : True := by trivial\nend N\n')
        (self.source / 'N.lean').write_text(text)
        self.data = {'schema': 1, 'commit': 'a' * 40,
                     'modules': [{'name': 'N', 'path': 'N.lean', 'doc': '', 'imports': []}],
                     'sourceHashes': {'N.lean': hashlib.sha256(text.encode()).hexdigest()},
                     'decls': [
                         {'name': 'N.program', 'module': 'N', 'kind': 'def', 'line': 2, 'endLine': 2,
                          'statement': self.header, 'signature': 'N.program : String',
                          'doc': 'A source-backed program.\nAlgorithm: method'},
                         {'name': 'N.claim', 'module': 'N', 'kind': 'theorem', 'line': 3, 'endLine': 3,
                          'statement': 'theorem claim : True := by SENTINEL_PROOF',
                          'signature': 'N.claim : True', 'doc': 'A theorem.'}]}
        self.assertTrue(build.validate_sources(self.data, self.source))
        self.data['_provenance'] = {'source_hashes_checked': True}
        build.whole_definitions(self.data['decls'], self.source)
        self.content = self.root / 'content'
        self.content.mkdir()
        self.page('method.md', {'kind': 'algorithm', 'id': 'method', 'title': 'Method'},
                  '{{ generated:implementations }}')
        self.page('implementation.md', {'kind': 'implementation', 'id': 'standard', 'algorithm': 'method',
                  'title': 'Actual program', 'status': 'ready',
                  'implementation_declarations': ['N.program']}, '{{ generated:implementation-source }}')
        self.site = self.root / 'site'
        model = library.make_records(self.data, load_pages(self.content), source=self.source)
        library.publish(model, self.site)
        (self.site / 'index.html').write_text('<html><body><main id="content"></main></body></html>')
        self.explorer = Explorer(self.site, self.content)
        self.implementation = self.explorer.pages['implementation:method/standard']

    def page(self, filename, metadata, body):
        (self.content / filename).write_text('---\n' + yaml.safe_dump(metadata) + '---\n' + body)

    def test_listing_shows_definition_and_pinned_source_with_html_escaped(self):
        result = self.explorer.generated('implementation-source', self.implementation)
        self.assertIn('Lean implementation', result)
        self.assertIn(self.header, result)
        self.assertIn(':=', result)
        self.assertIn('&lt;script&gt;not executable HTML&lt;/script&gt;', result)
        self.assertNotIn('<script>', result)
        self.assertIn('/blob/' + 'a' * 40 + '/N.lean#L2', result)

    def test_definition_evidence_shows_body_but_theorems_never_expose_proofs(self):
        definition = self.explorer.records['declarations']['N.program']
        self.assertTrue(definition['source']['definition_verified'])
        self.assertIn('Definition from verified source', self.explorer.evidence(definition))
        theorem = self.explorer.records['declarations']['N.claim']
        self.assertNotIn('SENTINEL_PROOF', json.dumps(theorem))
        theorem['statement'] = 'theorem claim : True := by SENTINEL_PROOF'
        theorem['source']['definition_verified'] = True
        self.assertNotIn('SENTINEL_PROOF', self.explorer.evidence(theorem))

    def test_missing_unverified_or_admitted_source_rejects_ready_listing(self):
        definition = self.explorer.records['declarations']['N.program']
        for change in [{'source': {'url': None, 'definition_verified': False}},
                       {'admission_reported': True}, {'statement': self.header}]:
            original = copy.deepcopy(definition)
            definition.update(change)
            with self.assertRaisesRegex(ValueError, 'Verified definition source required'):
                self.explorer.generated('implementation-source', self.implementation)
            definition.clear()
            definition.update(original)
        self.implementation.meta['implementation_declarations'] = ['N.unknown']
        with self.assertRaisesRegex(ValueError, 'Unknown implementation declaration'):
            self.explorer.generated('implementation-source', self.implementation)
        self.implementation.meta['implementation_declarations'] = ['N.claim']
        with self.assertRaisesRegex(ValueError, 'Verified definition source required'):
            self.explorer.generated('implementation-source', self.implementation)

    def test_full_prefix_and_module_fingerprint_required_before_enrichment(self):
        raw = copy.deepcopy(self.data)
        raw['decls'][0]['statement'] = self.header + ' MISMATCH_AFTER_THE_FIRST_FORTY_CHARACTERS'
        raw['decls'][0]['_definition_source_verified'] = True
        self.assertEqual(build.whole_definitions(raw['decls'], self.source), 0)
        self.assertNotIn('_definition_source_verified', raw['decls'][0])
        (self.source / 'N.lean').write_text('namespace N\ndef program := "different"\nend N\n')
        with self.assertRaisesRegex(ValueError, 'source hash mismatch'):
            build.validate_sources(self.data, self.source)

    def test_unchecked_snapshot_cannot_promote_definition_to_verified_source(self):
        self.data['_provenance']['source_hashes_checked'] = False
        model = library.make_records(self.data, load_pages(self.content))
        self.assertFalse(model['records']['declarations']['N.program']['source']['definition_verified'])

    def test_selectors_are_nonempty_unique_and_owned_by_implementation(self):
        for names in [[], 'N.program', ['N.program', 'N.program'], [None]]:
            self.page('implementation.md', {'kind': 'implementation', 'id': 'standard', 'algorithm': 'method',
                      'title': 'Actual program', 'implementation_declarations': names}, '')
            with self.assertRaisesRegex(ValueError, 'implementation_declarations'):
                load_pages(self.content)
        self.page('implementation.md', {'kind': 'algorithm', 'id': 'other', 'title': 'Other',
                  'implementation_declarations': ['N.program']}, '')
        with self.assertRaisesRegex(ValueError, 'implementation_declarations'):
            load_pages(self.content)
