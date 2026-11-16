"""Every menu on nla-lib.org lists the same pages in the same order: the homepage's and the design
page's (the `menu:` front matter of ../index.md and ../design/index.md) and the explorer's
(web/template.html), so the halves of the site cannot drift apart."""
import posixpath
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT.parent


def resolve(href, page_dir):
    """A menu link as a path from the top of the site (`./`, `./explore/rates/`), or the URL."""
    if href == 'https://nla-lib.org/':
        return './'
    if href.startswith('http'):
        return href
    path = (posixpath.normpath(href).lstrip('/') or '.') if href.startswith('/') else posixpath.normpath(posixpath.join(page_dir, href))
    return './' if path == '.' else f'./{path}/'


def markdown_menu(source, page_dir):
    front = source.read_text().split('---')[1]
    return [(m[1].strip(), resolve(m[2].strip(), page_dir))
            for m in re.finditer(r'^\s*-\s*([^:\n]+):\s*(\S+)\s*$', front, re.M)]


def explorer_menu():
    nav = re.search(r'<nav class="menu"[^>]*>(.*?)</nav>', (ROOT / 'web' / 'template.html').read_text(), re.S)[1]
    return [(label.strip(), resolve(href, 'explore'))
            for href, label in re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', nav)]


@unittest.skipUnless((SITE / 'index.md').exists(), 'the homepage is not checked out around the explorer')
class MenuTests(unittest.TestCase):
    def test_every_menu_lists_the_same_pages(self):
        home = markdown_menu(SITE / 'index.md', '.')
        self.assertEqual(home, explorer_menu())
        self.assertEqual(home, markdown_menu(SITE / 'design' / 'index.md', 'design'))



class GroupSummaryLayoutTests(unittest.TestCase):
    def test_group_summary_wraps_below_the_title_of_the_flex_label(self):
        # The disclosure label is a flex row with the marker pushed right. The summary needs a
        # line of its own after the title and the marker, at a specificity above that row's.
        row = (ROOT / 'web' / 'explore.css').read_text()
        self.assertIn('.explore-pages details > summary { cursor: pointer; list-style: none; display: flex;', row)
        css = (ROOT / 'web' / 'cg-pilot.css').read_text()
        self.assertIn('.explore-pages .task-group > summary { flex-wrap: wrap;', css)
        self.assertIn('.explore-pages .task-group > summary > h2 { flex: 1 1 0; }', css)
        self.assertIn('.explore-pages .task-group > summary::after { order: 1; }', css)
        self.assertRegex(css, r'\.explore-pages \.task-group-summary \{ order: 2; flex: 0 0 100%; margin: 0;')

if __name__ == '__main__':
    unittest.main()
