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


if __name__ == '__main__':
    unittest.main()
