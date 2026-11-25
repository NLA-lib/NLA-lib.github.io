"""Public, read-only editorial snapshots consumed by the hosted collaboration API."""
import hashlib
import json
from pathlib import Path
import re
import shutil

from editor.model import Catalog


def git_blob(text):
    raw = text.encode()
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def export(site, content):
    site, content = Path(site), Path(content)
    catalog = Catalog(site, content)
    root = site / 'api/v1/editor'
    (root / 'objects').mkdir(parents=True, exist_ok=True)
    index = []
    placements = {}
    for pid, page in catalog.pages.items():
        for sid in re.findall(r"\{\{ statement:([a-z0-9-]+) \}\}", catalog.objects[pid]["body_markdown"]):
            placements.setdefault(sid, []).append({"title": page.meta["title"], "url": page.url})
    for oid, obj in catalog.objects.items():
        evidence = obj['evidence']
        source = evidence.get('source') if obj['type'] == 'page' else evidence.get('source_file')
        editable = isinstance(source, str) and evidence.get('key') != 'index:library'
        url = catalog.pages[oid].url if obj['type'] == 'page' else '/explore/statements/'+oid+'/'
        if evidence['type'].startswith('library-'):
            collection = 'results' if evidence['type'] == 'library-result' else 'declarations'
            key = evidence.get('result') or evidence.get('declaration')
            url = catalog.explorer.records[collection][key]['url']
        state = {'object': obj, 'revision': catalog.origins[oid], 'baseline': catalog.origins[oid],
                 'editable': editable, 'url': url, 'used_by': [], 'dependencies': {}}
        if obj['type'] == 'page':
            state['document_markdown'] = catalog.document(obj)
            state['object']['page_metadata'] = catalog.pages[oid].meta
        if obj['type'] == 'statement':
            obj['references'] = catalog.statement_references.get(oid, [])
            state['used_by'] = placements.get(oid, [])
        if editable:
            text = (content / source).read_text()
            state.update(source_path='explore/content/'+source, source_markdown=text, source_sha=git_blob(text))
        (root / 'objects' / (oid+'.json')).write_text(json.dumps(state, ensure_ascii=False, separators=(',', ':')))
        index.append({'id': oid, 'title': obj['title'], 'type': obj['type'], 'editable': editable, 'url': url,
                      'statement_id': evidence.get('statement_id')})
        paths={site / url.removeprefix('/explore/') / 'index.html'}
        if obj['type']=='statement':paths.add(site / 'statements' / oid / 'index.html')
        for file in paths:
            if file.is_file():
                text = file.read_text()
                attribute = 'data-editor-page' if obj['type'] == 'page' else 'data-editor-statement'
                if 'data-editor-page=' not in text and 'data-editor-statement=' not in text:
                    flags = f' {attribute}="{oid}"' + ('' if editable else ' data-editor-readonly="true"')
                    text = text.replace('<main id="content">', '<main id="content"'+flags+'>')
                    file.write_text(text)
    (root / 'index.json').write_text(json.dumps({'schema_version': 1, 'objects': index}, ensure_ascii=False, separators=(',', ':')))
    shutil.copytree(Path(__file__).parent / 'editor', site / 'editor-assets',
                    ignore=shutil.ignore_patterns('node_modules', '__pycache__', 'discussion', '*.py', '*.md'), dirs_exist_ok=True)
    shell = (site / 'index.html').read_text()
    community = site / 'community'
    community.mkdir(exist_ok=True)
    shell = re.sub(r'<main id="content"[^>]*>.*?</main>', '<main id="content" data-community="true"><div class="page-heading"><h1 class="page-title">Researcher profile</h1></div><div id="profile-content"></div></main>', shell, flags=re.S)
    (community / 'index.html').write_text(shell)
    asset_version=hashlib.sha256((site / 'editor-assets/editor.js').read_bytes()+(site / 'editor-assets/editor.css').read_bytes()+(site / 'editor-assets/discussion.js').read_bytes()).hexdigest()[:12]
    # The overlay is enabled by the hosted service's health/bootstrap capabilities.
    for file in site.rglob('*.html'):
        text = file.read_text()
        if '<main id="content"' in text and '/editor-assets/editor.js' not in text:
            text = text.replace('</head>', '<link rel="stylesheet" href="/explore/editor-assets/editor.css?v='+asset_version+'"><script defer src="/explore/editor-assets/editor.js?v='+asset_version+'"></script></head>')
            file.write_text(text)
    print(f'Collaboration snapshots: {len(index)} objects, {sum(x["editable"] for x in index)} editable')
