"""The homepage menu (../index.md front matter) and the explorer menu (web/index.html) list the
same pages in the same order, so the two halves of nla-lib.org cannot drift apart."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT.parent / 'index.md'


def homepage_menu():
    front = HOME.read_text().split('---')[1]
    return [(m[1].strip(), m[2].strip()) for m in re.finditer(r'^\s*-\s*([^:\n]+):\s*(\S+)\s*$', front, re.M)]


def explorer_menu():
    nav = re.search(r'<nav class="menu"[^>]*>(.*?)</nav>', (ROOT / 'web' / 'index.html').read_text(), re.S)[1]
    out = []
    for href, label in re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', nav):
        # the explorer's links, as the homepage (one directory up) writes them
        if href == 'https://nla-lib.org/':
            href = './'
        elif not href.startswith('http'):
            href = './explore/' + ('' if href == './' else href)
        out.append((label.strip(), href))
    return out


@unittest.skipUnless(HOME.exists(), 'the homepage is not checked out next to the explorer')
class MenuTests(unittest.TestCase):
    def test_homepage_and_explorer_menus_match(self):
        self.assertEqual(homepage_menu(), explorer_menu())


if __name__ == '__main__':
    unittest.main()
