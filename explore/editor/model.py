"""Structured local editorial objects. Published files and Lean evidence stay read-only."""
from __future__ import annotations
import copy
import hashlib
import html
import json
import re
import shlex
import sqlite3
import uuid
from datetime import datetime, timezone
from urllib.parse import urlsplit
import yaml

from content_pages import Explorer, Page, STATEMENT, markdown, slug, load_pages
from bibliography import references_panel
from editor.identities import IdentityStore, PERSON
from notation import diagnostics as notation_diagnostics, policy as notation_policy

REACTIONS = [('👍', 'Helpful'), ('❤️', 'Love'), ('🎉', 'Celebrate'), ('👀', 'Following'),
             ('🤔', 'Thinking'), ('💡', 'Idea'), ('🙏', 'Thanks'), ('✅', 'Checked'),
             ('❓', 'Question'), ('🧮', 'Mathematics'), ('🚧', 'Work in progress'), ('🚀', 'Exciting')]

REFERENCE = re.compile(r'^\{\{ statement:([a-z0-9-]+) \}\}[ \t]*$', re.M)
MAX_BODY = 120_000

def packed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def digest(value):
    return hashlib.sha256(packed(value).encode()).hexdigest()

def identity(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'https://nla-lib.org/editor/' + value))

class Conflict(ValueError):
    pass

class Catalog:
    def __init__(self, site, content):
        self.explorer = Explorer(site, content)
        self.objects = {}
        self.pages = {}
        self.routes = {}
        self.origins = {}
        self.links = {}
        self.declarations = {}
        self.statement_references = {}
        for key, record in self.explorer.records['results'].items():
            decl = self.explorer.records['declarations'][record['primary']]
            oid = identity('result:' + key)
            self.links[key] = oid
            self.objects[oid] = self.statement(oid, record['title'], decl.get('docstring', ''),
                {'type': 'library-result', 'result': key, 'declaration': decl['id'],
                 'signature': decl['signature'], 'source': decl.get('source', {}),
                 'admission_reported': decl.get('admission_reported', False)})
            self.declarations.setdefault(decl['id'], oid)
        for key, decl in self.explorer.records['declarations'].items():
            if key in self.declarations:
                continue
            oid = identity('declaration:' + key)
            self.declarations[key] = oid
            self.objects[oid] = self.statement(oid, key, decl.get('docstring', ''),
                {'type': 'library-declaration', 'declaration': key, 'signature': decl['signature'],
                 'source': decl.get('source', {}), 'admission_reported': decl.get('admission_reported', False)},
                kind='result' if decl['kind'] == 'theorem' else 'definition')
        for page in self.explorer.pages.values():
            oid = page.meta.get('uid') or identity(page.key)
            occurrences = {}
            def replace(match):
                kind, source_kind, source_key, options, body = match.groups()
                opts = dict(token.split('=', 1) for token in shlex.split(options))
                locator = opts.get('id') or ':'.join([kind, source_kind or '', source_key or '', opts.get('name', '') if not source_key else ''])
                occurrences[locator] = occurrences.get(locator, 0) + 1
                sid = identity(page.key + ':' + locator + ':' + str(occurrences[locator]))
                shared = page.statement_imports.get(match.start())
                if shared:
                    sid = shared.uid
                evidence = {'type': 'authored', 'page': page.key, 'source_kind': source_kind,
                            'source_key': source_key, 'block_kind': kind, 'options': options}
                if shared:
                    evidence.pop('page')
                    evidence.update(statement_id=shared.id, source_file=str(shared.source.relative_to(self.explorer.content)))
                    self.statement_references[sid] = list(shared.references)
                    if shared.formalization_status:evidence['formalization_status']=shared.formalization_status
                    if shared.review_status:evidence['review_status']=shared.review_status
                if source_kind:
                    record = (self.explorer.records['results'][source_key] if source_kind == 'result' else None)
                    decl = self.explorer.records['declarations'][record['primary'] if record else source_key]
                    evidence.update(declaration=decl['id'], signature=decl['signature'], source=decl.get('source', {}),
                                    admission_reported=decl.get('admission_reported', False))
                title = opts.get('name') or (self.explorer.records['results'][source_key]['title'] if source_kind == 'result' else source_key) or 'Definition'
                self.objects[sid] = self.statement(sid, title, body, evidence, kind='definition' if kind == 'definition' else 'conjecture' if kind == 'conjecture' else 'result')
                if shared:
                    self.objects[sid]['proofs'] = list(shared.proofs)
                return '{{ statement:' + sid + ' }}\n'
            body = STATEMENT.sub(replace, page.body)
            self.objects[oid] = {'id': oid, 'type': 'page', 'title': page.meta['title'],
                'summary': page.meta.get('summary', ''), 'body_markdown': body,
                'evidence': {'type': 'page', 'key': page.key, 'source': str(page.source.relative_to(self.explorer.content))}}
            self.pages[oid] = page
            self.routes[page.url] = oid
        # A first edit of extracted prose creates a shared file without requiring
        # a page import. Register it immediately and preserve the generated UUID.
        for shared in self.explorer.shared_statements.values():
            if self.objects.get(shared.uid, {}).get('evidence', {}).get('source_file'):
                continue
            kind, source_kind, source_key, options, body = STATEMENT.fullmatch(shared.block).groups()
            opts = dict(token.split('=',1) for token in shlex.split(options))
            evidence = {'type':'authored','source_kind':source_kind,'source_key':source_key,
                'block_kind':kind,'options':options,'statement_id':shared.id,
                'source_file':str(shared.source.relative_to(self.explorer.content))}
            if shared.formalization_status:evidence['formalization_status']=shared.formalization_status
            if shared.review_status:evidence['review_status']=shared.review_status
            if source_kind:
                declaration_key = self.explorer.records['results'][source_key]['primary'] if source_kind=='result' else source_key
                decl=self.explorer.records['declarations'][declaration_key]
                evidence.update(declaration=decl['id'],signature=decl['signature'],source=decl.get('source',{}),admission_reported=decl.get('admission_reported',False))
                self.declarations[declaration_key]=shared.uid
            title=opts.get('name') or source_key or 'Result'
            obj=self.statement(shared.uid,title,body,evidence,kind='definition' if kind=='definition' else 'conjecture' if kind=='conjecture' else 'result')
            obj['proofs']=list(shared.proofs)
            self.objects[shared.uid]=obj
            self.statement_references[shared.uid]=list(shared.references)
        # A unique curated shared formulation also supplies the generated result.
        shared_by_result = {}
        for obj in self.objects.values():
            evidence = obj['evidence']
            if evidence.get('statement_id') and evidence.get('source_kind') == 'result':
                shared_by_result.setdefault(evidence['source_key'], []).append(obj['id'])
        for key, ids in shared_by_result.items():
            if len(ids) == 1:
                self.links[key] = ids[0]
                self.declarations[self.explorer.records['results'][key]['primary']] = ids[0]
        for oid, obj in self.objects.items():
            self.origins[oid] = digest(obj)

    @staticmethod
    def statement(oid, title, body, evidence, kind='result'):
        return {'id': oid, 'type': 'statement', 'title': title, 'body_markdown': body,
                'statement_kind': kind, 'proofs': [], 'evidence': evidence}

    def document(self, obj):
        if 'document_markdown' in obj:
            return obj['document_markdown']
        page = self.pages[obj['id']]
        original = page.source.read_text()
        if obj == self.objects[obj['id']]:
            return original
        header = re.fullmatch(r'---\n(.*?)\n---\n(.*)', original, re.S)
        meta = dict(obj.get('page_metadata') or yaml.safe_load(header[1]))
        meta.update(title=obj['title'], summary=obj['summary'])
        def readable(match):
            item = self.objects.get(match[1], {})
            return '{{ statement:' + item.get('evidence', {}).get('statement_id', match[1]) + ' }}'
        return '---\n' + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + '---\n' + REFERENCE.sub(readable, obj['body_markdown'])

    def validate(self, original, fields, known):
        if not isinstance(fields, dict):
            raise ValueError('fields must be an object')
        if original['type'] == 'page' and 'document_markdown' in fields:
            document = fields['document_markdown']
            if set(fields) != {'document_markdown'} or not isinstance(document, str) or len(document.encode()) > MAX_BODY:
                raise ValueError('Supply one Markdown document, at most 120 KB')
            match = re.fullmatch(r'---\n(.*?)\n---\n(.*)', document, re.S)
            if not match:
                raise ValueError('Keep the page YAML header between --- lines')
            page = self.pages[original['id']]
            meta = yaml.safe_load(match[1])
            if not isinstance(meta, dict) or any(meta.get(k) != page.meta.get(k) for k in ['kind', 'id', 'uid', 'algorithm']):
                raise ValueError('The page identity (kind, id, algorithm) must stay unchanged')
            # Reuse the existing graph/schema checks, without changing source files.
            # UUID references to newly created local statements are rendered by this editor.
            local_body = match[2]
            aliases = {o['evidence']['statement_id']: sid for sid, o in known.items() if o.get('evidence', {}).get('statement_id')}
            def resolve(reference):
                sid = aliases.get(reference[1], reference[1])
                if sid not in known or known[sid]['type'] != 'statement':
                    raise ValueError('Unknown statement reference: ' + reference[1])
                return '{{ statement:' + sid + ' }}'
            body = REFERENCE.sub(resolve, local_body)
            validation_document = document[:match.start(2)] + REFERENCE.sub('', local_body)
            validated = load_pages(self.explorer.content, {page.source: validation_document})[page.key]
            obj = self.validate(original, {'title': meta['title'], 'summary': meta.get('summary', ''), 'body_markdown': body}, known)
            obj.update(document_markdown=document, page_metadata=validated.meta)
            packed(obj)
            return obj
        allowed = {'title', 'body_markdown', 'summary'} if original['type'] == 'page' else {'title', 'body_markdown', 'statement_kind', 'proofs', 'references'}
        if set(fields) - allowed:
            raise ValueError('Unsupported fields: ' + ', '.join(sorted(set(fields) - allowed)))
        obj = {**original, **fields}
        if original['type'] == 'page':
            obj.pop('document_markdown', None)
        for field in ('title', 'body_markdown', *(['summary'] if original['type'] == 'page' else [])):
            if not isinstance(obj.get(field), str) or len(obj[field].encode()) > (500 if field == 'title' else MAX_BODY):
                raise ValueError(f'Invalid or oversized {field}')
        if not obj['title'].strip():
            raise ValueError('A title is required')
        body = obj['body_markdown']
        if re.search(r'(?:EXPLORERGENERATEDBLOCK|EXPLORERMATHISLAND|EDITORSTATEMENTISLAND)\d+END', body):
            raise ValueError('Reserved renderer token in Markdown')
        if original['type'] == 'page':
            refs = REFERENCE.findall(body)
            if len(refs) != len(set(refs)):
                raise ValueError('A statement can only be placed once on a page')
            if any(sid not in known or known[sid]['type'] != 'statement' for sid in refs):
                raise ValueError('Unknown statement reference')
            if re.search(r'^::: (?:theorem|definition)\b', body, re.M):
                raise ValueError('Edit statements using their cards or create a result, then insert its reference')
            if '{{ statement:' in REFERENCE.sub('', body):
                raise ValueError('Malformed statement reference; preserve the reference exactly')
        else:
            citations = obj.get('references', [])
            if not isinstance(citations, list) or len(citations) > 50:
                raise ValueError('At most 50 shared references are allowed')
            for citation in citations:
                if not isinstance(citation, dict) or set(citation) != {'key', 'locator'} or citation['key'] not in self.explorer.references or not isinstance(citation['locator'], str) or len(citation['locator']) > 2000:
                    raise ValueError('Choose a shared reference key and a short locator')
            if obj.get('statement_kind') not in {'result', 'conjecture', 'definition'}:
                raise ValueError('Unknown statement kind')
            if original.get('evidence', {}).get('declaration') and obj['statement_kind'] != original['statement_kind']:
                raise ValueError('The kind of an existing Lean-linked statement is fixed')
            proofs = obj.get('proofs')
            if not isinstance(proofs, list) or len(proofs) > 20:
                raise ValueError('At most 20 proof references are allowed')
            for proof in proofs:
                if not isinstance(proof, dict) or set(proof) != {'label', 'url', 'locator'}:
                    raise ValueError('Proof references require label, url and locator')
                if any(not isinstance(v, str) or len(v) > 2000 for v in proof.values()):
                    raise ValueError('Invalid proof reference')
                url = urlsplit(proof['url'])
                if url.scheme != 'https' or not url.hostname or url.username or url.password or any(c.isspace() for c in proof['url']):
                    raise ValueError('Proof references require an HTTPS URL without credentials')
            if REFERENCE.search(body) or re.search(r'^:::|\{\{\s*generated:', body, re.M):
                raise ValueError('Statements contain Markdown and mathematics, not generated blocks')
        return obj

    def notation_issues(self, obj):
        source = obj.get('evidence',{}).get('source_file')
        if obj['type']=='page':
            source=self.pages[obj['id']].source.relative_to(self.explorer.content).as_posix()
        return notation_diagnostics(obj['body_markdown'],notation_policy().get(source))

    def render_statement(self, obj, revised=False):
        evidence = obj['evidence']
        declaration = self.explorer.records['declarations'].get(evidence.get('declaration'))
        text = obj['body_markdown']
        if evidence['type'] == 'library-result':
            from rendering import split_notes
            text, _ = split_notes(text)
            text = re.sub(r'^(?:Result|Algorithm):[^\n]*$', '', text, flags=re.M).strip()
            text = re.sub(r'^\*\*[^*]+\*\*\s*[,;:.]?\s*', '', text).strip() or text
        kind = 'Definition' if obj['statement_kind'] == 'definition' else 'Statement' if evidence.get('admission_reported') else 'Theorem' if declaration else obj['statement_kind'].capitalize()
        citations = list((declaration or {}).get('references', [])) + obj.get('references', self.statement_references.get(obj['id'], []))
        return self.explorer.detail_layout(obj['title'], markdown(text), kind, obj['id'], declaration,
            citations, obj['proofs'], 'Local revision · mathematical review needs reassessment' if revised else '')

    def references_html(self, obj):
        decl = self.explorer.records['declarations'].get(obj['evidence'].get('declaration'), {})
        return references_panel(list(decl.get('references', [])) + obj.get('references', self.statement_references.get(obj['id'], [])), self.explorer.references)

    def overview(self, obj, revised=False):
        evidence = obj['evidence']
        text = obj['body_markdown']
        if evidence['type'] == 'library-result':
            from rendering import split_notes
            text, _ = split_notes(text)
            text = re.sub(r'^(?:Result|Algorithm):[^\n]*$', '', text, flags=re.M).strip()
            text = re.sub(r'^\*\*[^*]+\*\*\s*[,;:.]?\s*', '', text).strip() or text
        label = 'Definition' if obj['statement_kind'] == 'definition' else 'Statement' if evidence.get('admission_reported') else 'Theorem' if evidence.get('declaration') else obj['statement_kind'].capitalize()
        options = dict(token.split('=', 1) for token in shlex.split(evidence.get('options', '')))
        anchor = options.get('id') or ((evidence.get('block_kind', 'theorem') + '-' + slug(evidence.get('source_key') or evidence.get('result'))) if evidence.get('source_key') or evidence.get('result') else None)
        body = markdown(text)
        card = self.explorer.overview_card(obj['title'], body, obj['id'], label, anchor)
        return card + ('<p class="editor-status">Local revision · review needs reassessment</p>' if revised else '')

    def render_page(self, obj, lookup):
        page = self.pages[obj['id']]
        slots = []
        def reference(match):
            item = lookup(match[1])
            slots.append(self.overview(item['object'], item['revision'] != item['baseline']))
            return 'EDITORSTATEMENTISLAND' + str(len(slots) - 1) + 'END'
        body = REFERENCE.sub(reference, obj['body_markdown'])
        authored = {lookup(sid)['object']['evidence'].get('declaration') for sid in REFERENCE.findall(obj['body_markdown'])}
        # Generated statements use the same local objects everywhere they occur.
        original = self.explorer.result_reference
        def generated(key):
            if self.explorer.records['results'][key]['primary'] in authored:
                return ''
            item = lookup(self.links[key])
            return self.overview(item['object'], item['revision'] != item['baseline'])
        self.explorer.result_reference = generated
        original_overview = self.explorer.result_overview
        self.explorer.result_overview = generated
        try:
            rendered = self.explorer.render_body(Page(page.source, {**obj.get('page_metadata', page.meta), 'title': obj['title'], 'summary': obj['summary']}, body))
        finally:
            self.explorer.result_reference = original
            self.explorer.result_overview = original_overview
        return re.sub(r'(?:<p>)?EDITORSTATEMENTISLAND(\d+)END(?:</p>)?', lambda m: slots[int(m[1])], rendered)

class Store(IdentityStore):
    """Local SQLite persistence; portable proposals are the eventual backend boundary."""
    def __init__(self, catalog, database):
        self.catalog = catalog
        self.db = sqlite3.connect(database, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
            PRAGMA foreign_keys=ON;
            CREATE TABLE IF NOT EXISTS revisions(id TEXT PRIMARY KEY, object_id TEXT NOT NULL,
              parent TEXT NOT NULL, origin TEXT NOT NULL, payload TEXT NOT NULL, explanation TEXT NOT NULL,
              created_at TEXT NOT NULL, proposal_id TEXT NOT NULL, dependencies TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS revision_object ON revisions(object_id, created_at);
            CREATE TABLE IF NOT EXISTS heads(object_id TEXT PRIMARY KEY, revision_id TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS drafts(object_id TEXT PRIMARY KEY, base_revision TEXT NOT NULL, payload TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS proposals(key TEXT PRIMARY KEY, request TEXT NOT NULL, response TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS feedback(id TEXT PRIMARY KEY, object_id TEXT NOT NULL, kind TEXT NOT NULL,
              body TEXT NOT NULL, parent_id TEXT, created_at TEXT NOT NULL, revision_id TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS reactions(object_id TEXT PRIMARY KEY, reaction TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS emoji_reactions(object_id TEXT NOT NULL, emoji TEXT NOT NULL,
              PRIMARY KEY(object_id,emoji));
        ''')
        self.db.execute("INSERT OR IGNORE INTO emoji_reactions SELECT object_id, CASE reaction WHEN 'helpful' THEN '👍' WHEN 'interesting' THEN '💡' WHEN 'needs-attention' THEN '❓' END FROM reactions WHERE reaction IN ('helpful','interesting','needs-attention')")
        self.db.execute('DELETE FROM reactions')
        self.db.commit()
        self.init_identities()
        self.db.execute('CREATE TABLE IF NOT EXISTS actor_reactions(object_id TEXT NOT NULL, emoji TEXT NOT NULL, actor_id TEXT NOT NULL, PRIMARY KEY(object_id,emoji,actor_id))')
        self.db.execute('INSERT OR IGNORE INTO actor_reactions SELECT object_id,emoji,? FROM emoji_reactions', (PERSON,))
        self.db.execute('DELETE FROM emoji_reactions')
        self.db.commit()
        for row in self.db.execute("SELECT r.payload FROM heads h JOIN revisions r ON r.id=h.revision_id"):
            obj = json.loads(row['payload'])
            if obj['id'] not in catalog.objects and obj.get('evidence', {}).get('type') == 'local':
                catalog.objects[obj['id']] = obj
                catalog.origins[obj['id']] = 'local'

    def get(self, oid, revision=None):
        if oid not in self.catalog.objects:
            raise KeyError('Unknown object')
        baseline = self.catalog.origins[oid]
        if revision is None:
            head = self.db.execute('SELECT revision_id FROM heads WHERE object_id=?', (oid,)).fetchone()
            revision = head[0] if head else baseline
        if revision == baseline:
            if baseline == 'local':
                raise KeyError('A new local statement has no source baseline')
            obj = copy.deepcopy(self.catalog.objects[oid])
            refs = set(REFERENCE.findall(obj['body_markdown'])) | set(self.catalog.links.values()) if obj['type'] == 'page' else set()
            return {'object': obj, 'revision': baseline, 'baseline': baseline, 'dependencies': {sid: self.catalog.origins[sid] for sid in refs}}
        row = self.db.execute('SELECT * FROM revisions WHERE id=? AND object_id=?', (revision, oid)).fetchone()
        if row is None:
            raise KeyError('Unknown revision')
        if row['origin'] != baseline:
            raise Conflict('Published source changed since this local revision. Export your work and reconcile it before continuing.')
        return {'object': json.loads(row['payload']), 'revision': revision, 'baseline': baseline,
                'dependencies': json.loads(row['dependencies']), 'explanation': row['explanation'], 'created_at': row['created_at']}

    def history(self, oid):
        self.get(oid)
        baseline = [] if self.catalog.origins[oid] == 'local' else [{'id': self.catalog.origins[oid], 'explanation': 'Source / prototype baseline', 'baseline': True}]
        return baseline + [{**dict(row), 'attribution': self.attribution('revision', row['id'])} for row in self.db.execute('SELECT id, parent, explanation, created_at, proposal_id FROM revisions WHERE object_id=? ORDER BY rowid', (oid,))]

    def draft(self, oid, base_revision, fields, draft_revision=None):
        head = self.get(oid)
        if head['revision'] != base_revision:
            raise Conflict('This object has changed. Your text is preserved in the editor; compare with the latest revision.')
        previous = self.db.execute('SELECT base_revision,payload FROM drafts WHERE object_id=?', (oid,)).fetchone()
        previous_revision = digest(list(previous)) if previous else None
        if previous_revision != draft_revision:
            raise Conflict('This draft changed in another editor. Your text is preserved here; reopen and reconcile the drafts.')
        obj = self.catalog.validate(head['object'], fields, self.catalog.objects)
        self.preview(obj)
        with self.db:
            self.db.execute('INSERT OR REPLACE INTO drafts VALUES(?,?,?)', (oid, base_revision, packed(obj)))
        return {'object': obj, 'base_revision': base_revision, 'draft_revision': digest([base_revision, packed(obj)])}

    def preview(self, obj, lookup=None):
        return self.catalog.render_page(obj, lookup or self.get) if obj['type'] == 'page' else self.catalog.render_statement(obj, True)

    def propose(self, request, actor_id=PERSON):
        if not isinstance(request, dict) or set(request) != {'idempotency_key', 'explanation', 'changes'}:
            raise ValueError('A proposal requires idempotency_key, explanation and changes')
        key, explanation, changes = (request[k] for k in ('idempotency_key', 'explanation', 'changes'))
        if not isinstance(key, str) or not 1 <= len(key) <= 100:
            raise ValueError('Invalid idempotency key')
        previous = self.db.execute('SELECT * FROM proposals WHERE key=?', (key,)).fetchone()
        if previous:
            previous_actor = json.loads(previous['response']).get('actor_id', PERSON)
            if previous_actor != actor_id:
                raise Conflict('Idempotency key belongs to another actor')
            if previous['request'] != packed(request):
                raise Conflict('Idempotency key was already used for a different proposal')
            return json.loads(previous['response'])
        if not isinstance(explanation, str) or not 3 <= len(explanation.strip()) <= 2000:
            raise ValueError('Explain the change in 3–2000 characters')
        if not isinstance(changes, list) or not 1 <= len(changes) <= 20:
            raise ValueError('A proposal contains 1–20 changes')
        known = dict(self.catalog.objects)
        updates = {}
        for change in changes:
            if not isinstance(change, dict) or set(change) != {'operation', 'id', 'base_revision', 'fields'}:
                raise ValueError('Each change requires operation, id, base_revision and fields')
            oid = change['id']
            if not isinstance(oid, str) or oid in updates:
                raise ValueError('Each object may be changed once per proposal')
            if change['operation'] == 'create_statement':
                if oid in known or not re.fullmatch(r'[a-f0-9-]{36}', oid) or change['base_revision'] is not None:
                    raise ValueError('A new statement needs a fresh UUID and a null base revision')
                original = Catalog.statement(oid, 'New result', '', {'type': 'local'})
                baseline = 'local'
            else:
                current = self.get(oid)
                if change['operation'] != 'update_' + current['object']['type']:
                    raise ValueError('Unsupported operation for this object')
                if current['revision'] != change['base_revision']:
                    raise Conflict('Revision conflict: reload and compare with the latest version before saving')
                original, baseline = current['object'], current['baseline']
            known[oid] = self.catalog.validate(original, change['fields'], {**known, **{c['id']: Catalog.statement(c['id'], 'New result', '', {'type': 'local'}) for c in changes if c.get('operation') == 'create_statement'}})
            updates[oid] = {'object': known[oid], 'revision': str(uuid.uuid4()), 'baseline': baseline, 'dependencies': {}}
        lookup = lambda oid: updates[oid] if oid in updates else self.get(oid)
        for oid, item in updates.items():
            errors=[issue for issue in self.catalog.notation_issues(item['object']) if issue['severity']=='error']
            if errors:
                raise ValueError('Mathematical notation: '+ '; '.join('line '+str(issue['line'])+': '+issue['message'] for issue in errors[:5]))
            self.preview(item['object'], lookup)
            if item['object']['type'] == 'page':
                dependencies = set(REFERENCE.findall(item['object']['body_markdown'])) | set(self.catalog.links.values())
                item['dependencies'] = {sid: lookup(sid)['revision'] for sid in dependencies}
        proposal_id, now = str(uuid.uuid4()), datetime.now(timezone.utc).isoformat()
        response = {'actor_id': actor_id, 'id': proposal_id, 'status': 'saved_locally', 'revisions': {oid: item['revision'] for oid, item in updates.items()}, 'proposal': request}
        with self.db:
            for oid, item in updates.items():
                self.db.execute('INSERT INTO revisions VALUES(?,?,?,?,?,?,?,?,?)', (item['revision'], oid, next(c['base_revision'] or 'local' for c in changes if c['id'] == oid), item['baseline'], packed(item['object']), explanation.strip(), now, proposal_id, packed(item['dependencies'])))
                self.credit('revision', item['revision'], oid, actor_id)
                self.db.execute('INSERT OR REPLACE INTO heads VALUES(?,?)', (oid, item['revision']))
                self.db.execute('DELETE FROM drafts WHERE object_id=?', (oid,))
            self.db.execute('INSERT INTO proposals VALUES(?,?,?)', (key, packed(request), packed(response)))
        for oid, item in updates.items():
            if oid not in self.catalog.objects:
                self.catalog.objects[oid] = item['object']
                self.catalog.origins[oid] = 'local'
        return response

    def feedback(self, oid, fields, actor_id=PERSON):
        current = self.get(oid)
        if set(fields) != {'kind', 'body', 'parent_id'} or fields['kind'] not in {'comment', 'suggestion', 'mathematical-error', 'reference-request', 'formalization-request', 'generalization'}:
            raise ValueError('Invalid feedback kind or fields')
        if not isinstance(fields['body'], str) or not 1 <= len(fields['body'].strip()) <= 10000:
            raise ValueError('Feedback requires 1–10000 characters')
        parent = fields['parent_id']
        if parent is not None and not self.db.execute('SELECT 1 FROM feedback WHERE id=? AND object_id=?', (parent, oid)).fetchone():
            raise ValueError('Reply must reference feedback on this object')
        fid = str(uuid.uuid4())
        with self.db:
            self.db.execute('INSERT INTO feedback VALUES(?,?,?,?,?,?,?)', (fid, oid, fields['kind'], fields['body'].strip(), parent, datetime.now(timezone.utc).isoformat(), current['revision']))
            self.credit('comment', fid, oid, actor_id)
        return {'id': fid}

    def discussion(self, oid, actor_id=PERSON):
        self.get(oid)
        items = [dict(row) for row in self.db.execute('SELECT * FROM feedback WHERE object_id=? ORDER BY rowid', (oid,))]
        for item in items:
            item['html'] = markdown(item['body'])
            item['attribution'] = self.attribution('comment', item['id'])
        return {'items': items, 'count': len(items), 'reactions': self.reactions(oid,actor_id)}

    def discussion_count(self, oid):
        self.get(oid)
        return self.db.execute('SELECT count(*) FROM feedback WHERE object_id=?', (oid,)).fetchone()[0]

    def reactions(self, oid, actor_id=PERSON):
        self.get(oid)
        rows = list(self.db.execute('SELECT emoji,actor_id FROM actor_reactions WHERE object_id=?', (oid,)))
        return [{'emoji': emoji, 'label': label, 'count': sum(r['emoji']==emoji for r in rows),
                 'reacted': any(r['emoji']==emoji and r['actor_id']==actor_id for r in rows)}
                for emoji,label in REACTIONS if any(r['emoji']==emoji for r in rows)]

    def react(self, oid, emoji, active, actor_id=PERSON):
        self.get(oid)
        if emoji not in dict(REACTIONS) or not isinstance(active, bool):
            raise ValueError('Choose a supported emoji and an explicit active boolean')
        self.actor(actor_id)
        with self.db:
            if active:
                self.db.execute('INSERT OR IGNORE INTO actor_reactions VALUES(?,?,?)', (oid,emoji,actor_id))
            else:
                self.db.execute('DELETE FROM actor_reactions WHERE object_id=? AND emoji=? AND actor_id=?', (oid,emoji,actor_id))
        return {'reactions': self.reactions(oid,actor_id)}
