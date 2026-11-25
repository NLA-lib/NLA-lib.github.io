"""File-backed statements imported by identity, never by arbitrary filesystem paths."""
from dataclasses import dataclass
from pathlib import Path
import re
import uuid

from markdown_it import MarkdownIt
import yaml

STATEMENT = re.compile(r'^::: (theorem|definition|result|conjecture)(?: (result|decl):([^\s]+))?([^\n]*)\n(.*?)\n:::\s*$', re.M | re.S)
IMPORT = re.compile(r'^\{\{\s*statement:([a-z0-9][a-z0-9-]*)\s*\}\}[ \t]*$', re.M)

@dataclass(frozen=True)
class SharedStatement:
    source: Path
    id: str
    uid: str
    block: str
    references: tuple = ()
    proofs: tuple = ()
    review_status: str = ''
    formalization_status: str = ''


def load_statements(content):
    root = Path(content) / 'statements'
    statements, identities = {}, set()
    for file in sorted(root.rglob('*.md')):
        if file.name == 'README.md':
            continue
        match = re.fullmatch(r'---\n(.*?)\n---\n(.*)', file.read_text(), re.S)
        if not match:
            raise ValueError(f'{file}: expected statement front matter')
        meta = yaml.safe_load(match[1])
        if not isinstance(meta, dict) or not {'kind', 'id', 'uid'} <= meta.keys() or meta.keys() - {'kind', 'id', 'uid', 'references', 'proofs', 'review_status', 'formalization_status'} or meta['kind'] != 'statement':
            raise ValueError(f'{file}: statement metadata requires kind: statement, id and uid')
        identifier, uid = meta['id'], meta['uid']
        if not isinstance(identifier, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', identifier):
            raise ValueError(f'{file}: invalid statement id')
        try:
            if str(uuid.UUID(uid)) != uid:
                raise ValueError('noncanonical UUID')
        except (ValueError, TypeError, AttributeError):
            raise ValueError(f'{file}: uid must be a canonical UUID') from None
        if identifier in statements or uid in identities:
            raise ValueError(f'{file}: duplicate statement id or uid')
        block = match[2].strip()
        parsed = list(STATEMENT.finditer(block))
        if len(parsed) != 1 or parsed[0].span() != (0, len(block)):
            raise ValueError(f'{file}: expected exactly one theorem or definition block')
        if re.search(r'\{\{\s*(?:statement|generated):', block):
            raise ValueError(f'{file}: statement imports and generated blocks cannot be nested')
        references = meta.get('references', [])
        if not isinstance(references, list) or any(not isinstance(r, dict) or set(r) != {'key', 'locator'} or not all(isinstance(v, str) for v in r.values()) for r in references):
            raise ValueError(f'{file}: references require key and locator')
        proofs = meta.get('proofs', [])
        from urllib.parse import urlsplit
        if not isinstance(proofs, list) or len(proofs)>20:
            raise ValueError(f'{file}: invalid proof references')
        for proof in proofs:
            if not isinstance(proof, dict) or set(proof)!={'label','url','locator'} or any(not isinstance(v,str) or len(v)>2000 for v in proof.values()):
                raise ValueError(f'{file}: invalid proof reference')
            url=urlsplit(proof['url'])
            if url.scheme!='https' or not url.hostname or url.username or url.password or any(c.isspace() for c in proof['url']):
                raise ValueError(f'{file}: proof references require HTTPS URLs without credentials')
        for status in ('review_status','formalization_status'):
            if meta.get(status,'') not in {'','unreviewed','needs_reassessment','expert_reviewed','formally_stated','formally_proved'}:
                raise ValueError(f'{file}: invalid {status}')
        statements[identifier] = SharedStatement(file, identifier, uid, block, tuple(references), tuple(proofs), meta.get('review_status',''), meta.get('formalization_status',''))
        identities.add(uid)
    return statements


def expand_imports(body, statements):
    """Expand standalone references; retain source associations for the editor.

    Fenced/indented code examples remain literal. Statements cannot import other
    statements, so include cycles are impossible.
    """
    lines = body.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    code = [(offsets[t.map[0]], offsets[t.map[1]]) for t in MarkdownIt('commonmark').parse(body)
            if t.type in {'fence', 'code_block'}]
    chunks, imports, cursor, length = [], {}, 0, 0
    seen = set()
    for match in IMPORT.finditer(body):
        if any(start <= match.start() < end for start, end in code):
            continue
        identifier = match[1]
        if identifier not in statements:
            raise ValueError('Unknown statement import: ' + identifier)
        item = statements[identifier]
        if item.uid in seen:
            raise ValueError('Duplicate statement import on one page: ' + identifier)
        seen.add(item.uid)
        prefix = body[cursor:match.start()]
        chunks.append(prefix); length += len(prefix)
        imports[length] = item
        chunks.append(item.block); length += len(item.block)
        cursor = match.end()
    chunks.append(body[cursor:])
    # Reject malformed import directives outside code instead of publishing broken placeholders.
    for number, line in enumerate(lines):
        if any(start <= offsets[number] < end for start, end in code):
            continue
        if re.match(r'^\{\{\s*statement:', line) and not IMPORT.fullmatch(line.rstrip('\n')):
            raise ValueError('Malformed statement import: ' + line.strip())
    return ''.join(chunks), imports
