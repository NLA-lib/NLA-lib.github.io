#!/usr/bin/env python3
"""Build Markdown pages and generic library records from a pinned Lean extraction.

There is no program emitter, target-registry input, legacy application, or inferred
execution certificate. Markdown owns navigation; extraction metadata owns formal API.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil
import sys

import library
from library import DEF_KINDS, parse_bib

ROOT = Path(__file__).resolve().parent
SHARED = ROOT.parent


def build(data, bib, out, *, content=None, src=None, core_src=None, renames_dir=None, module_map=None):
    import content_pages
    pages = content_pages.load_pages(content or ROOT / 'content')
    model = library.make_records(data, pages, overrides=load_toml('results.toml'), bibliography=bib,
                                 rename_maps=library.load_rename_maps(renames_dir), source=src, module_map=module_map)
    out = Path(out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for asset in ['explore.css', 'explore.js', 'explore-search.js', 'cg-pilot.css', 'cg-pilot.js']:
        shutil.copyfile(ROOT / 'web' / asset, out / asset)
    for directory in ['font', 'vendor']:
        shutil.copytree(SHARED / directory, out / directory)
    (out / 'css').mkdir()
    shutil.copyfile(SHARED / 'css/site.css', out / 'css/site.css')
    library.publish(model, out, load_toml('synonyms.toml').get('synonyms', {}))
    shell = (ROOT / 'web/template.html').read_text()
    for token, path in {'site_css':'css/site.css', 'explore_css':'explore.css', 'cards_css':'cg-pilot.css',
                        'search_js':'explore-search.js', 'explore_js':'explore.js', 'cards_js':'cg-pilot.js',
                        'search_version':'api/v1/search-index.json'}.items():
        shell = shell.replace('{{' + token + '}}', hashlib.sha256((out / path).read_bytes()).hexdigest()[:12])
    shell = shell.replace('{{snapshot}}', model['snapshot']['extraction_sha256'])
    commit_label = 'working-tree preview' if model['snapshot']['dirty'] else (model['snapshot'].get('commit') or 'unversioned')[:12]
    shell = shell.replace('{{commit}}', html.escape(commit_label))
    (out / 'index.html').write_text(shell)
    if not core_src and src and (Path(src) / 'NLAlib/Krylov/CG/HSCG/Carried/FinitePrecision/Standard.lean').is_file():
        core_src = Path(src)
    if core_src:
        import cg_pilot
        same_snapshot = src and Path(core_src).resolve() == Path(src).resolve()
        cg_pilot.build(out, core_src,
                       published_revision=model['snapshot'].get('commit') if same_snapshot else None,
                       source_hashes=data.get('sourceHashes') if same_snapshot else None)
    content_pages.build(out, content or ROOT / 'content')
    print(f"Generic library: {len(model['records']['modules'])} modules, {len(model['records']['declarations'])} declarations, "
          f"{len(model['records']['results'])} result groups -> {out}")
    return model


def load_toml(name):
    import tomllib
    path = ROOT / name
    return tomllib.loads(path.read_text()) if path.exists() else {}

def whole_definitions(decls, src):
    """The data's `statement` stops at `:=`, which for a theorem leaves out only the proof; for a
    definition it leaves out the definition itself. Take a definition's whole text from the
    library source (its lines `line`..`endLine`, from where its statement starts), wherever the
    source agrees with the statement; elsewhere the statement stays as it is."""
    files, n = {}, 0
    for d in decls:
        if d['kind'] not in DEF_KINDS or not d.get('statement') or not d.get('line'):
            continue
        path = Path(src) / (d['module'].replace('.', '/') + '.lean')
        if path not in files:
            files[path] = path.read_text().split('\n') if path.exists() else None
        if not files[path]:
            continue
        text = '\n'.join(files[path][d['line'] - 1:d['endLine']]).rstrip()
        k = text.find(d['statement'].split('\n')[0].strip())
        if k >= 0 and text[k:].startswith(d['statement'].strip()[:40]) and len(text) - k > len(d['statement']):
            d['statement'] = text[k:]
            n += 1
    return n


def validate_sources(data, src):
    """Verify extraction-time bytes before trusting source line ranges, including tarballs."""
    hashes = data.get('sourceHashes')
    if hashes is None:
        print('warning: legacy data has no sourceHashes; skipping definition body enrichment',
              file=sys.stderr)
        return False
    expected = {m['path'] for m in data['modules']}
    if not isinstance(hashes, dict) or set(hashes) != expected:
        raise ValueError('sourceHashes must cover exactly all listed modules')
    for d in data.get('decls', []):
        path = d['module'].replace('.', '/') + '.lean'
        if path not in hashes:
            raise ValueError(f'sourceHashes missing declaration module: {path}')
    root = Path(src).resolve()
    for name, digest in hashes.items():
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or not path.parts or path.suffix != '.lean':
            raise ValueError(f'unsafe source path: {name}')
        full = (root / path).resolve()
        if not full.is_relative_to(root):
            raise ValueError(f'unsafe source path: {name}')
        if not full.is_file() or hashlib.sha256(full.read_bytes()).hexdigest() != digest:
            raise ValueError(f'source hash mismatch: {name}')
    return True



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=ROOT / 'data/explore-data.json')
    parser.add_argument('--bib', type=Path)
    parser.add_argument('--out', type=Path, default=ROOT / 'site')
    parser.add_argument('--src', type=Path, help='matching source checkout/archive, for fingerprint-verified definition bodies')
    parser.add_argument('--content', type=Path, default=ROOT / 'content')
    parser.add_argument('--core-src', type=Path, help='explicit working Ops source preview; otherwise use matching extracted sources')
    parser.add_argument('--renames', type=Path, help='library declaration rename maps')
    parser.add_argument('--module-map', type=Path, help='explicit mathematical module relocations; not retired execution aliases')
    args = parser.parse_args()
    raw = args.data.read_bytes()
    data = json.loads(raw)
    data['_provenance'] = {'commit': data.get('commit'), 'date': data.get('date'),
        'extraction_sha256': hashlib.sha256(raw).hexdigest(), 'fingerprint_kind': 'file-bytes',
        'source_hashes_checked': False, 'toolchain': None}
    if args.src and validate_sources(data, args.src):
        data['_provenance']['source_hashes_checked'] = True
        toolchain = args.src / 'lean-toolchain'
        if toolchain.is_file():
            data['_provenance']['toolchain'] = toolchain.read_text().strip()
        whole_definitions(data['decls'], args.src)
    build(data, parse_bib(args.bib), args.out, content=args.content, src=args.src,
          core_src=args.core_src, renames_dir=args.renames, module_map=args.module_map)


if __name__ == '__main__':
    main()
