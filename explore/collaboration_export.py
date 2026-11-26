"""Public, read-only editorial snapshots consumed by the hosted collaboration API."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import copy
import yaml

from editor.model import Catalog, digest, identity


def git_blob(text):
    raw = text.encode()
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def export(site, content):
    site, content = Path(site), Path(content)
    catalog = Catalog(site, content)
    root = site / 'api/v1/editor'
    (root / 'objects').mkdir(parents=True, exist_ok=True)
    index = []
    generated = {}
    placements = {}
    for pid, page in catalog.pages.items():
        for sid in re.findall(r"\{\{ statement:([a-z0-9-]+) \}\}", catalog.objects[pid]["body_markdown"]):
            placements.setdefault(sid, []).append({"title": page.meta["title"], "url": page.url})
    for oid, obj in catalog.objects.items():
        obj = copy.deepcopy(obj)
        evidence = obj['evidence']
        materializable = evidence['type'] in {'library-result','library-declaration'}
        source = evidence.get('source') if obj['type'] == 'page' else evidence.get('source_file')
        editable = (isinstance(source, str) and evidence.get('key') != 'index:library') or materializable
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
        if materializable:
            obj['title']=' '.join(obj['title'].split())
            declaration=catalog.explorer.records['declarations'][evidence['declaration']]
            from rendering import split_notes
            body,_=split_notes(declaration.get('docstring',''))
            body=re.sub(r'^(?:Result|Algorithm):[^\n]*$', '', body, flags=re.M).strip()
            if evidence['type']=='library-result':
                body=re.sub(r'^\*\*[^*]+\*\*\s*[,;:.]?\s*', '', body).strip() or body
            obj['body_markdown']=body
            obj['references']=[]
            identifier='entry-'+oid
            kind='definition' if obj['statement_kind']=='definition' else 'result' if evidence.get('admission_reported') else 'theorem'
            binding=('result:'+evidence['result']) if evidence.get('result') else ('decl:'+evidence['declaration'])
            document='---\n'+yaml.safe_dump({'kind':'statement','id':identifier,'uid':oid},sort_keys=False)+'---\n::: '+kind+' '+binding+' name='+json.dumps(obj['title'],ensure_ascii=False)+'\n'+body.rstrip()+'\n:::\n'
            state.update(source_path='explore/content/statements/'+identifier+'.md',source_markdown=document,source_sha=None,
                         revision=digest(obj),baseline=digest(obj),materializable=True,
                         reference_links={'editorial':[],'inherited':declaration.get('references',[])})
        elif editable:
            text = (content / source).read_text()
            state.update(source_path='explore/content/'+source, source_markdown=text, source_sha=git_blob(text))
        if editable and not materializable:
            (root / 'objects' / (oid+'.json')).write_text(json.dumps(state, ensure_ascii=False, separators=(',', ':')))
        else:
            generated.setdefault(oid[:2], {})[oid] = state
        index.append({'id': oid, 'title': obj['title'], 'type': obj['type'], 'editable': editable, 'url': url,
                      'statement_id': evidence.get('statement_id')})
        paths={site / 'index.html' if url=='/' else site / url.removeprefix('/explore/') / 'index.html'}
        if obj['type']=='statement':paths.add(site / 'statements' / oid / 'index.html')
        if evidence.get('declaration') and catalog.declarations.get(evidence['declaration'])==oid:
            paths.add(site / catalog.explorer.records['declarations'][evidence['declaration']]['url'].removeprefix('/explore/') / 'index.html')
        result_key=evidence.get('result') or (evidence.get('source_key') if evidence.get('source_kind')=='result' else None)
        if result_key and catalog.links.get(result_key)==oid:
            paths.add(site / catalog.explorer.records['results'][result_key]['url'].removeprefix('/explore/') / 'index.html')
        for file in paths:
            if file.is_file():
                text = file.read_text()
                attribute = 'data-editor-page' if obj['type'] == 'page' else 'data-editor-statement'
                if evidence['type']=='authored':
                    text=re.sub(r' data-editor-(?:statement|readonly)="[^"]*"','',text)
                if 'data-editor-page=' not in text and 'data-editor-statement=' not in text:
                    flags = f' {attribute}="{oid}"' + ('' if editable else ' data-editor-readonly="true"')
                    text = text.replace('<main id="content">', '<main id="content"'+flags+'>')
                    file.write_text(text)
    for key,record in sorted(catalog.explorer.references.items()):
        source=content/'references'/(key+'.bib')
        if not source.is_file():continue
        oid=identity('reference:'+key);text=source.read_text()
        obj={'id':oid,'type':'reference','title':key+' — '+record.get('title',''),'bibtex':text,
             'record':record,'evidence':{'type':'bibliography','reference_key':key}}
        state={'object':obj,'revision':digest(obj),'baseline':digest(obj),'editable':True,
               'url':'/explore/references/#reference-'+key,'source_path':'explore/content/references/'+key+'.bib',
               'source_markdown':text,'document_markdown':text,'source_sha':git_blob(text),'used_by':[],'dependencies':{}}
        (root/'objects'/(oid+'.json')).write_text(json.dumps(state,ensure_ascii=False,separators=(',',':')))
        index.append({'id':oid,'title':obj['title'],'type':'reference','editable':True,'url':state['url'],'reference_key':key})
    (root / 'generated').mkdir(exist_ok=True)
    for shard, states in generated.items():
        (root / 'generated' / (shard+'.json')).write_text(json.dumps(states, ensure_ascii=False, separators=(',', ':')))
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
