"""Snapshot-pinned, proof-free library reading and persistent reading sessions.

This module needs only the Python standard library. MCP is an optional adapter.
"""
from __future__ import annotations

import base64
import argparse
from collections import Counter, defaultdict
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import tomllib
from urllib.parse import quote
import uuid

from search.matrix import Index, ROOT


def packed(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def first_paragraph(text):
    text = re.sub(r'^#+[^\n]*\n', '', text or '').strip()
    return ' '.join(text.split('\n\n')[0].split())


class Documentation:
    """Read exact extraction metadata; source slices require matching file hashes."""

    def __init__(self, data, source=None, state_dir=None):
        self.index = Index(data, semantic=False)
        raw = Path(data).read_bytes()
        if hashlib.sha256(raw).hexdigest() != self.index.fingerprint:
            raise ValueError('Extraction changed during initialization; retry with a stable file')
        self.raw = json.loads(raw)
        self.snapshot = self.index.fingerprint
        self.commit = self.index.commit
        self.source = Path(source).resolve() if source else None
        self.decls = {d['name']: d for d in self.raw['decls'] if not d.get('sorry')}
        self.modules = {m['name']: m for m in self.raw['modules']}
        self.discovery = {d['name'] for d in self.index.decls}
        self.by_module = defaultdict(list)
        for d in self.index.decls:
            self.by_module[d['module']].append(d)
        for ds in self.by_module.values():
            ds.sort(key=lambda d: (d.get('line', 0), d['name']))
        self.callers = defaultdict(lambda: defaultdict(list))
        for d in self.decls.values():
            for field, label in [('typeDeps', 'statement'), ('valueDeps', 'proof_or_value')]:
                for dep in d.get(field, []):
                    self.callers[dep][label].append(d['name'])
        self.synonyms = tomllib.loads((ROOT / 'synonyms.toml').read_text()).get('synonyms', {})
        self.state_dir = Path(state_dir or ROOT / '.docs-state')

    def provenance(self):
        return {'commit': self.commit, 'data_sha256': self.snapshot,
                'discovery_scope': 'Matrix and matrix-related ForMathlib helpers',
                'proofs_included': False}

    def uri(self, kind, name):
        return f'nlalib-docs://{self.snapshot}/{kind}/{quote(name, safe=".")}'

    def source_link(self, module, line=1):
        return (f'https://github.com/NLA-lib/NLAlib/blob/{self.commit}/'
                f'{module.replace(".", "/")}.lean#L{line}')

    def page(self, text, *, key, cursor=None, max_chars=8000, extra=None):
        """Bound the entire JSON response, including envelope/cursor, in Unicode characters.

        Cursors bind to the snapshot and exact rendered content, not just an offset.
        """
        if not 1500 <= max_chars <= 20000:
            raise ValueError('max_chars must be between 1500 and 20000')
        version = digest(key + '\n' + text)
        offset = 0
        if cursor:
            try:
                obj = json.loads(base64.urlsafe_b64decode(cursor.encode()).decode())
                offset = obj['offset']
                if (obj['snapshot'] != self.snapshot or obj['document'] != version or
                        type(offset) is not int or not 0 <= offset <= len(text)):
                    raise ValueError('Cursor belongs to another snapshot, document, or session revision')
            except (ValueError, KeyError, TypeError, UnicodeError) as e:
                raise ValueError('Invalid or stale continuation cursor') from e

        def response(end):
            token = None
            if end < len(text):
                token = base64.urlsafe_b64encode(packed({
                    'snapshot': self.snapshot, 'document': version, 'offset': end}).encode()).decode()
            return {**self.provenance(), **(extra or {}), 'content': text[offset:end],
                    'range': [offset, end], 'total_content_chars': len(text),
                    'complete': end == len(text), 'next_cursor': token}

        lo, hi = offset, min(len(text), offset + max_chars)
        if len(packed(response(lo))) > max_chars:
            raise ValueError('Metadata exceeds response budget; request a larger max_chars')
        # A complete page drops its continuation token. Check it first: that discontinuity
        # otherwise makes binary search unnecessarily split a document that fits in one page.
        if len(text) - offset <= max_chars and len(packed(response(len(text)))) <= max_chars:
            return response(len(text))
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if len(packed(response(mid))) <= max_chars:
                lo = mid
            else:
                hi = mid - 1
        if lo == offset and offset < len(text):
            raise ValueError('Response budget is too small for progress')
        return response(lo)

    def _decl(self, name):
        if name not in self.decls:
            raise ValueError(f'Unknown proved declaration in this snapshot: {name}')
        return self.decls[name]

    def _source_text(self, module):
        if not self.source:
            raise ValueError('Source reading requires --src pointing to matching library sources')
        relative = self.modules[module]['path']
        path = (self.source / relative).resolve()
        if not path.is_relative_to(self.source) or path.suffix != '.lean':
            raise ValueError('Unsafe source path')
        expected = self.raw.get('sourceHashes', {}).get(relative)
        raw = path.read_bytes()
        if not expected or hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError(f'Source hash differs from extraction: {relative}')
        return raw.decode()

    def _api(self, d, *, short=False, links=True):
        doc = d.get('doc') or '(No declaration docstring in extraction.)'
        if short:
            doc = first_paragraph(doc)
            if len(doc) > 450:
                doc = doc[:450] + '… [excerpt; use docs_read_declaration]'
        text = (f"### {d['name']}\n\n{doc}\n\n```lean\n"
                f"{d.get('signature') or '(Signature unavailable in extraction.)'}\n```\n")
        if links:
            text += (f"\nSource: {self.source_link(d['module'], d.get('line', 1))}\n"
                     f"Resource: {self.uri('declaration', d['name'])}\n")
        return text

    def info(self, max_chars=8000):
        text = (f'# NLAlib documentation snapshot\n\nCommit: {self.commit}\n'
                f'Discovery: {len(self.index.decls)} proved Matrix/helper declarations in '
                f'{len(self.by_module)} modules. Exact reads and related declarations may cross '
                'into other public library topics in this extraction.\n\n'
                'Start with docs_catalog, read module overviews, then API pages or exact declarations. '
                'Default readings contain original docstrings and complete extracted signatures, '
                'with proof bodies omitted. A page may end inside a signature: follow next_cursor '
                'before treating it as a complete statement.\n\n'
                'Use docs_context for a selected reading bundle. Save goals, bookmarks, unresolved '
                'questions and agent-authored notes with docs_session. Sessions are pinned to this '
                'exact extraction and survive server restarts. Notes are not verified mathematics.\n\n'
                'This server does not execute Lean or invent theorem summaries. Use your existing '
                'Lean MCP for proof states and application checks. Search and documentation are '
                'candidate evidence, not proof of applicability.\n')
        return self.page(text, key='info', max_chars=max_chars)

    def catalog(self, prefix='NLAlib.Matrix', cursor=None, max_chars=8000):
        prefix = prefix.rstrip('.') or 'NLAlib'
        groups = defaultdict(list)
        for module, ds in self.by_module.items():
            if prefix and not (module == prefix or module.startswith(prefix + '.')):
                continue
            suffix = module[len(prefix):].lstrip('.') if prefix else module
            child = suffix.split('.')[0] if suffix else ''
            group = prefix + ('.' if prefix and child else '') + child
            groups[group].append((module, ds))
        if not groups:
            raise ValueError(f'No discoverable modules under {prefix!r}')
        lines = [f'# Catalog: {prefix or "all discovery topics"}\n']
        for group, entries in sorted(groups.items()):
            leaf = len(entries) == 1 and entries[0][0] == group
            count = sum(len(ds) for _, ds in entries)
            if leaf:
                meta = self.modules.get(group, {})
                summary = first_paragraph(meta.get('doc'))
            else:
                parts = group.split('.')
                summary = f'Modules under {group}.'
            lines.append(f'## {group}\n{summary}\n{len(entries)} module(s), {count} declarations. '
                         f'{"Read with docs_read_module." if leaf else "Browse this prefix with docs_catalog."}\n')
        return self.page('\n'.join(lines), key='catalog:' + prefix, cursor=cursor,
                         max_chars=max_chars, extra={'entries': len(groups)})

    def read_module(self, module, view='overview', kind='', cursor=None, max_chars=8000):
        if module not in self.modules:
            raise ValueError(f'Unknown module: {module}')
        if view not in ('overview', 'prose', 'api'):
            raise ValueError('view must be overview, prose or api')
        ds = [d for d in self.decls.values() if d['module'] == module and (not kind or d['kind'] == kind)]
        ds.sort(key=lambda d: (d.get('line', 0), d['name']))
        meta = self.modules[module]
        text = f'# {module}\n\n' + (meta.get('doc') or '(No module docstring.)')
        text += '\n\nKinds: ' + packed(dict(Counter(d['kind'] for d in ds))) + '\n'
        if view == 'overview':
            text += '\nImports:\n' + '\n'.join('- ' + x for x in meta.get('imports', []))
            text += '\n\nUse view="api" to read all declaration docstrings and signatures.\n'
        elif view == 'prose':
            text += '\n\n' + '\n'.join(f"### {d['name']}\n\n{d.get('doc') or '(No docstring.)'}\n" for d in ds)
        else:
            text += '\n\n' + '\n'.join(self._api(d, links=False) for d in ds)
        return self.page(text, key=f'module:{module}:{view}:{kind}', cursor=cursor,
                         max_chars=max_chars, extra={'declarations': len(ds), 'view': view,
                                                    'source': self.source_link(module),
                                                    'resource': self.uri('module', module)})

    def read_declaration(self, name, view='api', cursor=None, max_chars=8000):
        d = self._decl(name)
        if view == 'api':
            text = self._api(d)
        elif view == 'doc':
            text = f'# {name}\n\n' + (d.get('doc') or '(No docstring.)')
        elif view == 'definition':
            if d['kind'] in ('theorem', 'lemma'):
                raise ValueError('Definition view is for data/predicate definitions; theorem proofs are omitted')
            lines = self._source_text(d['module']).splitlines()
            start, end = d['line'] - 1, d['endLine']
            if not 0 <= start < end <= len(lines):
                raise ValueError('Invalid extraction source range')
            text = self._api(d) + '\n## Definition source (file hash verified)\n\n```lean\n'
            text += '\n'.join(lines[start:end]) + '\n```\n'
        else:
            raise ValueError('view must be api, doc or definition')
        return self.page(text, key=f'declaration:{name}:{view}', cursor=cursor,
                         max_chars=max_chars, extra={'view': view, 'resource': self.uri('declaration', name),
                                                    'definition_source_included': view == 'definition'})

    def search(self, query, module_prefix='', kind='', cursor=None, max_chars=8000):
        expansions = []
        for phrase, alternatives in self.synonyms.items():
            if phrase.lower() in query.lower():
                expansions.extend(alternatives)
        expanded = query + ' ' + ' '.join(expansions)
        hits = self.index.search(expanded, limit=len(self.index.decls), mode='lexical')
        # Keep an exact-name query at the front even when it also triggers vocabulary expansion.
        hits.sort(key=lambda d: d['name'] != query.strip())
        hits = [d for d in hits if (not module_prefix or d['module'] == module_prefix or
                d['module'].startswith(module_prefix + '.')) and (not kind or d['kind'] == kind)][:50]
        text = f'# Search candidates\n\nQuery: {query}\nVocabulary expansion: {", ".join(expansions) or "none"}\n'
        text += ('\nThese are lexical/vocabulary candidates, not LLM conclusions or Lean-checked applications. '
                 'If the right concept is missing, browse its module and try another formulation.\n\n')
        text += '\n'.join(self._api(d, short=True, links=False) for d in hits) or '(No candidates.)'
        return self.page(text, key=f'search:{query}:{module_prefix}:{kind}', cursor=cursor,
                         max_chars=max_chars, extra={'candidates': len(hits), 'candidate_limit': 50})

    def related(self, name, direction='dependencies', edge='statement', cursor=None, max_chars=8000):
        d = self._decl(name)
        if edge not in ('statement', 'proof_or_value', 'both'):
            raise ValueError('edge must be statement, proof_or_value or both')
        fields = [('typeDeps', 'statement'), ('valueDeps', 'proof_or_value')]
        matches = defaultdict(set)
        if direction == 'dependencies':
            for field, label in fields:
                if edge in (label, 'both'):
                    for n in d.get(field, []):
                        matches[n].add(label)
        elif direction == 'callers':
            for _, label in fields:
                if edge in (label, 'both'):
                    for n in self.callers[name][label]:
                        matches[n].add(label)
        else:
            raise ValueError('direction must be dependencies or callers')
        lines = [f'# {direction} of {name}\n\nEdges are direct extracted references, not a completeness or quality judgment.\n']
        for n, labels in sorted(matches.items()):
            lines.append(f'Edges: {", ".join(sorted(labels))}\n')
            if n in self.decls:
                lines.append(self._api(self.decls[n], short=True, links=False))
            else:
                lines.append(f'### {n}\nOutside this extraction; use existing Lean navigation.\n')
        return self.page('\n'.join(lines), key=f'related:{name}:{direction}:{edge}', cursor=cursor,
                         max_chars=max_chars, extra={'related_count': len(matches)})

    def context(self, names, cursor=None, max_chars=8000):
        if not names or len(names) > 20:
            raise ValueError('Provide between 1 and 20 declaration names')
        unique = list(dict.fromkeys(names))
        text = '# Selected mathematical context\n\n' + '\n'.join(self._api(self._decl(n), links=False) for n in unique)
        return self.page(text, key='context:' + packed(unique), cursor=cursor, max_chars=max_chars)

    def _database(self):
        self.state_dir.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(self.state_dir / 'sessions.sqlite3', timeout=10)
        db.execute('CREATE TABLE IF NOT EXISTS sessions '
                   '(id TEXT PRIMARY KEY, snapshot TEXT NOT NULL, payload TEXT NOT NULL)')
        return db

    def session(self, action, session_id='', goal=None, notes=None, bookmarks=None,
                open_questions=None, cursor=None, max_chars=8000):
        if not 1500 <= max_chars <= 20000:
            raise ValueError('max_chars must be between 1500 and 20000')
        if action not in ('create', 'get', 'update', 'list'):
            raise ValueError('action must be create, get, update or list')
        if action in ('get', 'list') and any(x is not None for x in (goal, notes, bookmarks, open_questions)):
            raise ValueError('Read actions do not accept updates')
        with closing(self._database()) as db, db:
            if action in ('create', 'update'):
                db.execute('BEGIN IMMEDIATE')
            if action == 'list':
                records = [json.loads(row[0]) for row in db.execute(
                    'SELECT payload FROM sessions WHERE snapshot=? ORDER BY id', (self.snapshot,))]
                text = '# Reading sessions\n\n' + '\n'.join(
                    f"- {r['id']}: {r['goal'][:160]} ({r['updated_at']})" for r in records)
                return self.page(text, key='sessions:list', cursor=cursor, max_chars=max_chars)
            if action == 'create':
                if session_id or cursor:
                    raise ValueError('New sessions do not accept an id or cursor')
                session_id = str(uuid.uuid4())
                record = {'id': session_id, 'snapshot': self.snapshot, 'commit': self.commit,
                          'goal': '', 'notes': '', 'bookmarks': [], 'open_questions': [], 'revision': 0}
            else:
                row = db.execute('SELECT snapshot,payload FROM sessions WHERE id=?', (session_id,)).fetchone()
                if not row:
                    raise ValueError('Unknown reading session')
                if row[0] != self.snapshot:
                    raise ValueError('Session belongs to another snapshot; restart with its matching extraction')
                record = json.loads(row[1])
            if action in ('create', 'update'):
                if cursor:
                    raise ValueError('Updates do not accept continuation cursors; resume with action=get')
                for key, value in [('goal', goal), ('notes', notes)]:
                    if value is not None:
                        if not isinstance(value, str) or len(value) > 12000:
                            raise ValueError(f'{key} must be a string of at most 12000 characters')
                        record[key] = value
                if bookmarks is not None:
                    if len(bookmarks) > 100:
                        raise ValueError('At most 100 bookmarks per session')
                    for n in bookmarks:
                        self._decl(n)
                    record['bookmarks'] = list(dict.fromkeys(bookmarks))
                if open_questions is not None:
                    if len(open_questions) > 30 or any(len(q) > 1000 for q in open_questions):
                        raise ValueError('At most 30 questions, each at most 1000 characters')
                    record['open_questions'] = open_questions
                record['revision'] += 1
                record['updated_at'] = datetime.now(timezone.utc).isoformat()
                db.execute('INSERT OR REPLACE INTO sessions VALUES (?,?,?)',
                           (session_id, self.snapshot, packed(record)))
            text = (f"# Reading session {session_id}\n\nRevision: {record['revision']}\n"
                    f"\n## Goal\n{record['goal']}\n\n## Agent-authored notes (not verified)\n{record['notes']}\n"
                    '\n## Open questions\n' + '\n'.join('- ' + q for q in record['open_questions']) +
                    '\n\n## Bookmarks\n' + '\n'.join(
                        f'- {n}' for n in record['bookmarks']) +
                    '\n\nUse docs_context on selected bookmarks to reopen exact signatures and docstrings.\n')
            return self.page(text, key=f'session:{session_id}:{record["revision"]}', cursor=cursor,
                             max_chars=max_chars, extra={'session_id': session_id,
                                                        'revision': record['revision']})


def main():
    p = argparse.ArgumentParser(description='Read the mathematical API without proofs; no MCP SDK needed.')
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--src', type=Path)
    p.add_argument('--state-dir', type=Path)
    p.add_argument('--tool', choices=['info', 'catalog', 'read_module', 'read_declaration',
                                     'search', 'related', 'context', 'session'], default='info')
    p.add_argument('--args', default='{}', help='JSON object of tool arguments, including cursor and max_chars')
    a = p.parse_args()
    docs = Documentation(a.data, a.src, a.state_dir)
    try:
        arguments = json.loads(a.args)
        if not isinstance(arguments, dict):
            raise ValueError('--args must be a JSON object')
        print(packed(getattr(docs, a.tool)(**arguments)))
    except (ValueError, TypeError, OSError) as e:
        p.exit(2, f'Documentation request failed: {e}\n')


if __name__ == '__main__':
    main()
