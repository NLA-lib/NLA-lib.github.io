"""Promote the built Explorer landing page to /; preserve existing nested URLs."""
import argparse
from pathlib import Path
import re

MARKER='data-explorer-home-redirect'
REDIRECT='''<!doctype html>
<html lang="en" data-explorer-home-redirect><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NLA-lib</title><link rel="canonical" href="https://nla-lib.org/">
<script>location.replace('/'+location.search+location.hash)</script>
<noscript><meta http-equiv="refresh" content="0;url=/"></noscript>
</head><body><p><a href="/">Open NLA-lib</a></p></body></html>
'''

def assemble(site):
    site=Path(site);source=site/'explore/index.html';target=site/'index.html'
    if not (site/'about/index.html').is_file():raise ValueError('Copy the About page and shared assets before assembling the site.')
    home=source.read_text()
    if MARKER in home:
        if not target.is_file() or MARKER in target.read_text():raise ValueError('The original Explorer homepage is missing; rebuild before assembling.')
        return
    if '<main' not in home or 'data-root="/explore/"' not in home:raise ValueError('Expected a built Explorer landing page with absolute asset paths.')
    home=re.sub(r'<title>.*?</title>','<title>NLA-lib</title>',home,flags=re.S)
    home=re.sub(r'<link\b[^>]*rel="canonical"[^>]*>','',home)
    home=home.replace('</head>','<link rel="canonical" href="https://nla-lib.org/"></head>',1)
    target.write_text(home)
    source.write_text(REDIRECT)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--site',required=True,type=Path)
    assemble(parser.parse_args().site)
