"""The Explorer homepage moves without breaking old entry or asset URLs."""
from pathlib import Path
import tempfile
import unittest
from assemble_site import assemble, MARKER

class SiteAssemblyTests(unittest.TestCase):
    def setUp(self):
        folder=tempfile.TemporaryDirectory();self.addCleanup(folder.cleanup);self.site=Path(folder.name)
        (self.site/'explore/theory').mkdir(parents=True);(self.site/'about').mkdir()
        (self.site/'about/index.html').write_text('<h1>About NLA-lib</h1>')
        self.home='<html><head><title>Explorer</title></head><body data-root="/explore/"><a class="site-brand" href="/">NLA-lib</a><main>Explore mathematics</main><script src="/explore/explore.js"></script></body></html>'
        (self.site/'explore/index.html').write_text(self.home)
        (self.site/'explore/theory/index.html').write_text('Theory remains here')
    def test_root_homepage_preserves_nested_urls_and_about(self):
        assemble(self.site)
        root=(self.site/'index.html').read_text();redirect=(self.site/'explore/index.html').read_text()
        self.assertIn('<title>NLA-lib</title>',root);self.assertIn('Explore mathematics',root)
        self.assertIn('src="/explore/explore.js"',root);self.assertNotIn(MARKER,root)
        self.assertIn(MARKER,redirect);self.assertIn("location.search+location.hash",redirect)
        self.assertIn('content="0;url=/"',redirect)
        self.assertEqual((self.site/'explore/theory/index.html').read_text(),'Theory remains here')
        self.assertIn('About NLA-lib',(self.site/'about/index.html').read_text())
    def test_assembly_can_repeat_without_turning_homepage_into_redirect(self):
        assemble(self.site);original=(self.site/'index.html').read_bytes();assemble(self.site)
        self.assertEqual((self.site/'index.html').read_bytes(),original)
    def test_missing_about_fails_before_replacing_homepage(self):
        (self.site/'about/index.html').unlink()
        with self.assertRaises(ValueError):assemble(self.site)
        self.assertEqual((self.site/'explore/index.html').read_text(),self.home)
