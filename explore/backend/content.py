"""Read published editorial snapshots; validate proposed source without modifying Git."""
import copy
import difflib
import hashlib
import html
import json
import re
import shlex
import time
import uuid
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlsplit

import yaml
from markdown_it import MarkdownIt
from notation import math_spans, diagnostics
from bibtex import one_reference, citation_html

MAX_BODY = 120_000
UUID = r'[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}'
REACTIONS = [('👍', 'Helpful'), ('❤️', 'Love'), ('🎉', 'Celebrate'), ('👀', 'Following'),
             ('🤔', 'Thinking'), ('💡', 'Idea'), ('🙏', 'Thanks'), ('✅', 'Checked'),
             ('❓', 'Question'), ('🧮', 'Mathematics'), ('🚧', 'Work in progress'), ('🚀', 'Exciting')]
MD = MarkdownIt('commonmark', {'html': False}).disable('image')
BLOCK = re.compile(r'^::: (theorem|definition|result|conjecture)(?: (result|decl):([^\s]+))?([^\n]*)\n(.*?)\n:::\s*$', re.S)


def packed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(packed(value).encode()).hexdigest()


def markdown(text):
    if re.search(r'EXPLORERMATHISLAND\d+END', text):
        raise ValueError('Reserved renderer token in Markdown')
    islands, chunks, cursor = [], [], 0
    for start, end, tex, display in math_spans(text)[0]:
        chunks.extend([text[cursor:start], 'EXPLORERMATHISLAND'+str(len(islands))+'END'])
        islands.append('<span class="math'+(' display' if display else '')+'">'+html.escape(tex.strip())+'</span>')
        cursor = end
    chunks.append(text[cursor:])
    return re.sub(r'EXPLORERMATHISLAND(\d+)END', lambda m: islands[int(m[1])], MD.render(''.join(chunks)))


def header(document):
    if not isinstance(document, str) or len(document.encode()) > MAX_BODY:
        raise ValueError('Markdown must be at most 120 KB')
    match = re.fullmatch(r'---\n(.*?)\n---\n(.*)', document, re.S)
    if not match:
        raise ValueError('Keep the YAML header between --- lines')
    # Reject YAML aliases before constructing potentially expanding structures.
    if any(isinstance(t, (yaml.tokens.AliasToken, yaml.tokens.AnchorToken)) for t in yaml.scan(match[1])):
        raise ValueError('YAML anchors and aliases are not supported')
    meta = yaml.safe_load(match[1])
    if not isinstance(meta, dict) or any(not isinstance(k, str) for k in meta):
        raise ValueError('Invalid YAML metadata')
    # JSON-only values keep DynamoDB/API serialization predictable.
    try:
        json.dumps(meta)
    except (ValueError, TypeError):
        raise ValueError('Use plain strings, lists and objects in YAML') from None
    return meta, match[2]


class Snapshot:
    base = 'https://nla-lib.org/explore/api/v1/'
    def __init__(self):
        self.cache = {}

    def fetch(self, path):
        now = time.monotonic()
        if path in self.cache and self.cache[path][0] > now:
            return copy.deepcopy(self.cache[path][1])
        request = Request(self.base+path, headers={'User-Agent': 'NLA-lib-collaboration/1'})
        with urlopen(request, timeout=8) as response:
            if response.geturl() != self.base+path:
                raise ValueError('Unexpected snapshot redirect')
            raw = response.read(12_000_001)
        if len(raw) > 12_000_000:
            raise ValueError('Snapshot exceeds limit')
        result = json.loads(raw)
        if len(self.cache) > 128:
            self.cache.clear()
        self.cache[path] = (now+60, result)
        return copy.deepcopy(result)

    def get(self, oid):
        if not isinstance(oid, str) or not re.fullmatch(UUID, oid):
            raise ValueError('Invalid entry ID')
        try:
            return self.fetch('editor/objects/'+oid+'.json')
        except HTTPError as error:
            if error.code!=404:
                raise
            # Generated Lean entries share bounded shards rather than adding one
            # deployment file per declaration to the already large static site.
            result=self.fetch('editor/generated/'+oid[:2]+'.json').get(oid)
            if result is None:
                raise error
            return result

    def index(self):
        return self.fetch('editor/index.json')['objects']

    def references(self):
        return self.fetch('references.json')['references']


def fresh_reference(source):
    key,record=one_reference(source)
    oid=str(uuid.uuid5(uuid.NAMESPACE_URL,'https://nla-lib.org/editor/reference:'+key))
    obj={'id':oid,'type':'reference','title':key+' — '+record['title'],'bibtex':source,'record':record,
         'evidence':{'type':'bibliography','reference_key':key}}
    return {'object':obj,'revision':None,'editable':True,'source_sha':None,'source_markdown':'',
            'source_path':'explore/content/references/'+key+'.bib','url':'/explore/references/#reference-'+key}


def validate(snapshot, state, fields):
    obj = copy.deepcopy(state['object'])
    if not state.get('editable'):
        raise ValueError('This entry comes from Lean. Propose a correction in its discussion.')
    if not isinstance(fields, dict) or not fields:
        raise ValueError('Supply editable fields')
    source = state.get('source_markdown', '')
    if obj['type']=='reference':
        if set(fields)!={'bibtex'}:raise ValueError('Reference edits require one bibtex field')
        key,record=one_reference(fields['bibtex'],obj['evidence']['reference_key'])
        document=fields['bibtex'].strip()+'\n'
        obj.update(title=key+' — '+record['title'],bibtex=document,record=record)
        return obj,document
    if obj['type'] == 'page':
        if set(fields) != {'document_markdown'}:
            raise ValueError('Page edits require the complete document_markdown')
        document = fields['document_markdown']
        meta, body = header(document)
        original, _ = header(source)
        if '\x00' in document:
            raise ValueError('NUL characters are not supported')
        for key in ('kind', 'id', 'uid', 'algorithm'):
            if meta.get(key) != original.get(key):
                raise ValueError('The page identity must stay unchanged: '+key)
        if set(meta)-set(original)-{'summary', 'search_aliases'}:
            raise ValueError('Unknown page metadata')
        for key in ('title', 'summary'):
            if key in meta and (not isinstance(meta[key], str) or len(meta[key]) > 2000):
                raise ValueError('Invalid '+key)
        if not meta.get('title', '').strip():
            raise ValueError('A title is required')
        # Structural/graph metadata remains source-maintained for this first release.
        for key in original.keys()-{'title', 'summary', 'search_aliases'}:
            if meta.get(key) != original[key]:
                raise ValueError('Edit exposition here; structural metadata requires source review: '+key)
        aliases = meta.get('search_aliases', [])
        if not isinstance(aliases, list) or len(aliases)>50 or any(not isinstance(x,str) or len(x)>200 for x in aliases):
            raise ValueError('Invalid search aliases')
        if re.search(r'^:::\s+(?:theorem|definition|result|conjecture)\b',body,re.M):
            raise ValueError('Use Add statement to create a mathematical statement, then insert its shared reference.')
        imports = re.findall(r'^\{\{\s*statement:([a-z0-9-]+)\s*\}\}[ \t]*$', body, re.M)
        if imports:
            aliases={x['id']:x['statement_id'] for x in snapshot.index() if x.get('statement_id')}
            known=set(aliases.values())
            resolved=[aliases.get(x,x) for x in imports]
            if any(x not in known for x in resolved) or len(resolved)!=len(set(resolved)):
                raise ValueError('Choose an existing shared statement. Lean-only entries must first receive an editorial statement file.')
            body=re.sub(r'^(\{\{\s*statement:)([a-z0-9-]+)(\s*\}\}[ \t]*)$',lambda m:m[1]+aliases.get(m[2],m[2])+m[3],body,flags=re.M)
            document=document[:document.index('\n---\n')+5]+body
        if '{{ statement:' in re.sub(r'^\{\{\s*statement:[a-z0-9-]+\s*\}\}[ \t]*$', '', body, flags=re.M):
            raise ValueError('Malformed statement import')
        obj.update(title=meta['title'], summary=meta.get('summary',''), body_markdown=body, document_markdown=document)
    else:
        allowed = {'title', 'body_markdown', 'statement_kind', 'proofs', 'references'}
        if set(fields)-allowed:
            raise ValueError('Unsupported statement fields')
        obj.update(fields)
        if obj.get('statement_kind') not in {'result','conjecture','definition'}:
            raise ValueError('Invalid statement kind')
        if obj['evidence'].get('declaration') and obj['statement_kind'] != state['object']['statement_kind']:
            raise ValueError('The kind of a Lean-linked statement cannot be changed')
        if not isinstance(obj.get('title'),str) or not 1<=len(obj['title'].strip())<=500 or any(ord(c)<32 for c in obj['title']):
            raise ValueError('A title of at most 500 characters is required')
        body=obj.get('body_markdown')
        if not isinstance(body,str) or len(body.encode())>MAX_BODY or '\x00' in body:
            raise ValueError('Invalid statement Markdown')
        if re.search(r'^:::|\{\{\s*(?:statement|generated):',body,re.M):
            raise ValueError('Statements cannot contain imports or generated blocks')
        refs=obj.get('references',[])
        if not isinstance(refs,list) or len(refs)>50:
            raise ValueError('At most 50 references are allowed')
        known=snapshot.references()
        for ref in refs:
            if not isinstance(ref,dict) or set(ref)!={'key','locator'} or ref['key'] not in known or not isinstance(ref['locator'],str) or len(ref['locator'])>2000:
                raise ValueError('Invalid shared reference')
        proofs=obj.get('proofs',[])
        if not isinstance(proofs,list) or len(proofs)>20:
            raise ValueError('At most 20 external proof references are allowed')
        for proof in proofs:
            if not isinstance(proof,dict) or set(proof)!={'label','url','locator'} or any(not isinstance(v,str) or len(v)>2000 for v in proof.values()):
                raise ValueError('Invalid proof reference')
            url=urlsplit(proof['url'])
            if url.scheme!='https' or not url.hostname or url.username or url.password or any(c.isspace() for c in proof['url']):
                raise ValueError('Proof links require an HTTPS URL without credentials')
        if source:
            meta, block=header(source)
            match=BLOCK.fullmatch(block.strip())
            if not match:
                raise ValueError('Statement source is not editable')
            kind, source_kind, key, options, _=match.groups()
            options=dict(x.split('=',1) for x in shlex.split(options))
            options['name']=obj['title']
            binding=(' '+source_kind+':'+key) if source_kind else ''
            if not obj['evidence'].get('declaration'):
                kind=obj['statement_kind']
            option_text=' '.join(k+'='+json.dumps(v,ensure_ascii=False) for k,v in options.items())
        else:
            meta={'kind':'statement','id':'result-'+obj['id'],'uid':obj['id']}
            kind=obj['statement_kind'];binding='';option_text='name='+json.dumps(obj['title'],ensure_ascii=False)
        meta.update(references=refs,proofs=proofs)
        if body != state['object'].get('body_markdown'):
            meta['review_status']='needs_reassessment' if source else 'unreviewed'
            if obj['evidence'].get('declaration'):meta['formalization_status']='needs_reassessment'
        document='---\n'+yaml.safe_dump(meta,sort_keys=False,allow_unicode=True)+'---\n::: '+kind+binding+' '+option_text+'\n'+body.rstrip()+'\n:::\n'
    if re.search(r'(?:EXPLORERGENERATEDBLOCK|EXPLORERMATHISLAND|EDITORSTATEMENTISLAND)\d+END',body):
        raise ValueError('Reserved renderer token')
    if len(document.encode())>MAX_BODY:
        raise ValueError('Source exceeds 120 KB')
    return obj, document


def require_external_proof(obj):
    if obj.get('type')!='statement' or obj.get('statement_kind')!='result':return
    evidence=obj.get('evidence',{})
    if evidence.get('declaration') and not evidence.get('admission_reported'):return
    for proof in obj.get('proofs',[]):
        if not isinstance(proof,dict) or not isinstance(proof.get('url'),str):continue
        try:url=urlsplit(proof['url'])
        except ValueError:continue
        if url.scheme=='https' and url.hostname and not url.username and not url.password and not any(c.isspace() for c in proof['url']):return
    raise ValueError('This result has no Lean proof. Add an HTTPS link under Proof references before submitting or publishing. Definitions and conjectures are exempt.')


def render_object(obj):
    return citation_html(obj['record']) if obj['type']=='reference' else markdown(obj['body_markdown'])


def preview(snapshot, state, fields):
    obj, document=validate(snapshot,state,fields)
    body=obj.get('body_markdown','')
    if obj['type']=='page':
        # Generated content is immutable; label its source placeholder in preview.
        body=re.sub(r'^\{\{\s*(?:statement|generated):.*?\}\}[ \t]*$',
                    lambda m:'\n`'+m[0]+'`\n',body,flags=re.M)
    return {'object':obj,'document_markdown':document,'html':render_object(obj) if obj['type']=='reference' else markdown(body),
        'diff':''.join(difflib.unified_diff(state.get('source_markdown','').splitlines(True),document.splitlines(True),fromfile='Published',tofile='Proposed')),
        'diagnostics':diagnostics(body,None)}
