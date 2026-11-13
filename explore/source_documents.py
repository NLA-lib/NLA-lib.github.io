"""Source guide references and mathematical module moves; never execution aliases."""
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
from urllib.parse import quote, unquote, urlsplit

from rendering import record_component

BASE = '/explore/'
REPO = 'https://github.com/NLA-lib/NLAlib'
LINK = re.compile(r'\[[^\]]*\]\(([^\s)]+)\)')


def guide_id(path):
    return re.sub(r'[^a-z0-9]+', '-', PurePosixPath(path).stem.lower()).strip('-')


def resolve_path(source_path, link):
    url = urlsplit(html.unescape(link))
    if url.scheme or url.netloc or not url.path:
        return None
    path = posixpath.normpath(posixpath.join(posixpath.dirname(source_path), unquote(url.path)))
    if path.startswith('../') or path.startswith('/'):
        return None
    return path


def guide_records(pages, source, snapshot):
    records = {}
    if not source:
        return records
    root = Path(source).resolve()
    paths = {path for p in pages.values() for path in p.meta.get('source_guides', [])}
    for path in sorted(paths):
        target = (root / path).resolve()
        if not target.is_relative_to(root) or not path.startswith('docs/algorithms/') or target.suffix != '.md':
            raise ValueError('unsafe source guide path: ' + path)
        if not target.is_file():
            continue  # An older, matching snapshot need not contain a newer guide.
        data = target.read_bytes()
        text = data.decode('utf-8')
        digest = hashlib.sha256(data).hexdigest()
        heading = re.search(r'^#\s+(.+)$', text, re.M)
        identifier = guide_id(path)
        if identifier in records:
            raise ValueError('duplicate source guide identity: ' + identifier)
        source_url = None
        if snapshot['versioned']:
            committed = subprocess.run(['git', '-C', str(root), 'show', snapshot['commit'] + ':' + path], capture_output=True)
            if committed.returncode == 0 and hashlib.sha256(committed.stdout).hexdigest() == digest:
                source_url = REPO + '/blob/' + snapshot['commit'] + '/' + path
        records[identifier] = {'id': identifier, 'title': heading[1] if heading else identifier,
            'url': BASE + 'library/guides/' + identifier + '/', 'markdown': text,
            'source': {'path': path, 'sha256': digest, 'url': source_url,
                       'kind': 'published-source' if source_url else 'working-tree-source'},
            'links': []}
        for match in LINK.finditer(text):
            linked = resolve_path(path, match[1])
            if linked:
                resolved = (root / linked).resolve()
                if not resolved.is_relative_to(root) or not resolved.is_file():
                    raise ValueError(f'source guide {path}: missing local link {match[1]}')
                records[identifier]['links'].append({'path': linked, 'fragment': urlsplit(match[1]).fragment})
    return records


def module_moves(path, modules):
    if not path:
        return {}
    data = json.loads(Path(path).read_text())
    moved = {}
    for old, spec in data.get('mathematical_module_moves', {}).items():
        destinations = spec.get('modules', [])
        if not destinations or not all(isinstance(name, str) and name in modules for name in destinations):
            raise ValueError(f'module move {old}: destination absent from extraction')
        if old not in modules:
            moved[old] = {'modules': destinations, 'note': spec.get('note', ''),
                'url': BASE + 'library/module-moves/' + quote(record_component(old), safe='.') + '/',
                'scope': 'mathematical relocation; not an alias for retired execution APIs'}
    return moved


def rewrite_links(markup, source_path, modules, guides, source_url=None):
    """Local source links use current references, never a dirty tree's base revision."""
    module_paths = {m.get('path', name.replace('.', '/') + '.lean'): (m.get('source') or {}).get('url') or m['url']
                    for name, m in modules.items()}
    guide_paths = {g['source']['path']: g['url'] for g in guides.values()}

    def replace(match):
        href, label = match.groups()
        path = resolve_path(source_path, href)
        if path is None:
            return match[0]
        destination = module_paths.get(path) or guide_paths.get(path)
        if destination:
            return '<a href="' + html.escape(destination, quote=True) + '">' + label + '</a>'
        # Full published-source links remain appropriate for other documentation.
        if source_url:
            from urllib.parse import urljoin
            destination = urljoin(source_url, html.unescape(href))
            return '<a href="' + html.escape(destination, quote=True) + '">' + label + '</a>'
        # The unpublished file is not a web page; keep its label without a broken link.
        return '<span title="Working-tree source: ' + html.escape(path, quote=True) + '">' + label + '</span>'

    return re.sub(r'<a href="([^"]+)">(.*?)</a>', replace, markup, flags=re.S)
