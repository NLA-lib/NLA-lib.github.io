"""Generic, proof-free extraction records. No program emitter or execution registry.

Algorithm/result/module associations are discovery metadata. Only a statement's
exact Lean signature supplies formal evidence; source fingerprints identify bytes.
"""
from collections import defaultdict
import gzip
import hashlib
import html
import json
from pathlib import Path
import re
import tomllib
from urllib.parse import quote

from rendering import record_component

BASE = '/explore/'
REPO = 'https://github.com/NLA-lib/NLAlib'
DEF_KINDS = {'def', 'abbrev', 'opaque', 'structure', 'class', 'inductive'}
RESULT = re.compile(r'^\s*Result:\s*(.*?)\s*$', re.M)
ALGORITHM = re.compile(r'^\s*Algorithm:\s*([a-z0-9-]+)(?:\s*\(([^)]+)\))?\s*$', re.M)


def packed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def fingerprint(text):
    return hashlib.sha256(text.encode()).hexdigest()


def api_url(kind, key):
    return BASE + 'api/v1/' + kind + '/' + quote(record_component(key), safe='.') + '.json'


def reference_url(kind, key):
    return BASE + 'library/' + kind + '/' + quote(record_component(key), safe='.') + '/'


def summary(text):
    text = re.sub(r'^(?:Result|Algorithm|Asymptotic):.*$', '', text or '', flags=re.M).strip()
    return ' '.join(text.split('\n\n')[0].split())


def title(text, fallback):
    match = re.search(r'\*\*(.*?)\*\*', text or '', re.S)
    return match[1].rstrip('.').strip() if match else fallback.replace('-', ' ').capitalize()


def make_records(data, pages, *, overrides=None, bibliography=None, rename_maps=(), source=None, module_map=None):
    if data.get('schema', 1) != 1:
        raise ValueError(f"unsupported extraction schema {data.get('schema')!r}")
    overrides, bibliography = overrides or {}, bibliography or {}
    snapshot = dict(data.get('_provenance', {}))
    snapshot.setdefault('commit', data.get('commit'))
    snapshot.setdefault('date', data.get('date'))
    snapshot.setdefault('extraction_sha256', fingerprint(packed({k: v for k, v in data.items() if not k.startswith('_')})))
    snapshot.setdefault('fingerprint_kind', 'canonical-json')
    snapshot.setdefault('source_hashes_checked', False)
    snapshot.setdefault('toolchain', None)
    dirty = data.get('dirty', snapshot.get('dirty', False))
    if not isinstance(dirty, bool):
        raise ValueError('extraction dirty flag must be a boolean')
    snapshot['dirty'] = dirty
    if dirty:
        snapshot['base_commit'] = data.get('base_commit') or snapshot.get('commit')
        snapshot['commit'] = None
        snapshot['date'] = None
    snapshot['versioned'] = bool(re.fullmatch(r'[0-9a-f]{40}', snapshot.get('commit') or ''))
    snapshot['kind'] = 'published-snapshot' if snapshot['versioned'] else 'working-tree-preview'
    records = {kind: {} for kind in ['declarations', 'results', 'algorithms', 'tasks', 'modules', 'guides']}
    originals = {d['name']: d for d in data['decls']}
    if len(originals) != len(data['decls']):
        raise ValueError('duplicate declaration identity in extraction')
    callers, value_callers = defaultdict(set), defaultdict(set)
    grouped, algorithm_members = defaultdict(set), defaultdict(list)
    result_aliases = {key: cfg['merge_into'] for key, cfg in overrides.items() if cfg.get('merge_into')}

    def resolve_result(key):
        seen = set()
        while key in result_aliases:
            if key in seen:
                raise ValueError('cycle in result aliases: ' + key)
            seen.add(key)
            key = result_aliases[key]
        return key

    for key in result_aliases:
        resolve_result(key)
    for declaration in data['decls']:
        name = declaration['name']
        for dependency in declaration.get('typeDeps', []):
            callers[dependency].add(name)
        for dependency in declaration.get('valueDeps', []):
            value_callers[dependency].add(name)
        for match in RESULT.finditer(declaration.get('doc') or ''):
            for rid in re.findall(r'[a-z0-9]+(?:-[a-z0-9]+)*', match[1]):
                grouped[resolve_result(rid)].add(name)
        for match in ALGORITHM.finditer(declaration.get('doc') or ''):
            algorithm_members[match[1]].append({'declaration': name, 'role': match[2] or 'declaration'})
    declaration_results = defaultdict(list)
    for rid, names in grouped.items():
        for name in names:
            declaration_results[name].append(rid)
    renamed, changed = rename_tables(rename_maps, set(originals))
    for name, original in originals.items():
        module = original['module']
        path = module.replace('.', '/') + '.lean'
        signature = original.get('signature') or ''
        citations = [{'key': m[1], 'locator': m[2] or '', **bibliography.get(m[1], {})}
                     for m in re.finditer(r'\[([A-Z][A-Za-z]+\d{4}[a-z]?)(?:,\s*([^\]]*))?\]', original.get('doc') or '')]
        records['declarations'][name] = {
            'id': name, 'kind': original['kind'], 'url': reference_url('declarations', name),
            'module': module, 'import': 'import ' + module,
            'signature': signature, 'signature_sha256': fingerprint(signature),
            'statement': signature if original['kind'] == 'theorem' else original.get('statement') or signature,
            'docstring': original.get('doc') or '', 'summary': summary(original.get('doc')),
            'admission_reported': bool(original.get('sorry')),
            'statement_dependencies': original.get('typeDeps', []),
            'proof_or_value_dependencies': original.get('valueDeps', []),
            'statement_callers': sorted(callers[name]), 'proof_or_value_callers': sorted(value_callers[name]),
            'results': sorted(declaration_results[name]), 'references': citations,
            'statement_changed': changed.get(name, []),
            'source': {'path': path, 'line': original.get('line'), 'end_line': original.get('endLine'),
                       'sha256': data.get('sourceHashes', {}).get(path),
                       'url': f"{REPO}/blob/{snapshot['commit']}/{path}#L{original.get('line') or 1}" if snapshot['versioned'] else None},
        }
    for rid, names in grouped.items():
        cfg = overrides.get(rid, {})
        primary = cfg.get('primary')
        if primary and primary not in names:
            raise ValueError(f'result {rid}: primary declaration {primary} is absent from this result')
        primary = primary or min(names, key=lambda n: (bool(originals[n].get('sorry')), originals[n]['kind'] != 'theorem', n))
        records['results'][rid] = {
            'id': rid, 'title': cfg.get('title') or title(originals[primary].get('doc'), rid),
            'url': reference_url('results', rid), 'primary': primary, 'declarations': sorted(names),
            'forms': [], 'aliases': cfg.get('aliases', []),
            'admission_reported': all(bool(originals[n].get('sorry')) for n in names),
        }
    editorial_algorithms = {}
    for page in sorted(pages.values(), key=lambda p: p.kind != 'algorithm'):
        aid = page.meta.get('library_algorithm')
        if aid:
            editorial_algorithms.setdefault(aid, page)
    for aid in sorted(set(algorithm_members) | set(editorial_algorithms)):
        page = editorial_algorithms.get(aid)
        members = algorithm_members[aid]
        member_names = {member['declaration'] for member in members}
        prefixes = page.meta.get('result_prefixes', [aid]) if page else [aid]
        results = {rid for rid, r in records['results'].items()
                   if any(rid == prefix or rid.startswith(prefix + '-') for prefix in prefixes)
                   or any(member_names.intersection(originals[n].get('typeDeps', [])) or n in member_names for n in r['declarations'])}
        records['algorithms'][aid] = {
            'id': aid, 'title': page.meta['title'] if page else title(originals[members[0]['declaration']].get('doc'), aid),
            'url': page.url if page else reference_url('algorithms', aid),
            'members': members, 'results': sorted(results),
            'aliases': page.meta.get('search_aliases', []) if page else [],
            'associations': 'discovery metadata; not execution evidence',
        }
    for page in pages.values():
        if page.kind != 'task':
            continue
        aids = [p.meta['library_algorithm'] for p in pages.values()
                if p.kind == 'algorithm' and p.meta.get('library_algorithm') and page.meta['id'] in p.meta.get('tasks', [])]
        records['tasks'][page.meta['id']] = {
            'id': page.meta['id'], 'title': page.meta['title'], 'url': page.url,
            'summary': page.meta.get('summary', ''), 'algorithms': sorted(aids),
            'results': sorted({rid for aid in aids for rid in records['algorithms'][aid]['results']}),
            'definitions': sorted({m['declaration'] for aid in aids for m in records['algorithms'][aid]['members']}),
        }
    for module in data.get('modules', []):
        name = module['name']
        doc = module.get('doc') or ''
        heading = re.search(r'^#\s+(.+)$', doc, re.M)
        records['modules'][name] = {'id': name, 'title': heading[1] if heading else name,
            'summary': doc, 'url': reference_url('modules', name), 'imports': module.get('imports', []),
            'path': module.get('path', name.replace('.', '/') + '.lean'),
            'source': {'url': f"{REPO}/blob/{snapshot['commit']}/{module['path']}" if snapshot['versioned'] else None},
            'declarations': sorted(n for n, d in originals.items() if d['module'] == name)}
    for name, declaration in records['declarations'].items():
        if declaration['module'] in records['modules']:
            continue
        records['modules'].setdefault(declaration['module'], {'id': declaration['module'], 'title': declaration['module'],
            'summary': '', 'url': reference_url('modules', declaration['module']), 'imports': [],
            'declarations': sorted(n for n, d in originals.items() if d['module'] == declaration['module'])})
    from source_documents import guide_records, module_moves
    records['guides'] = guide_records(pages, source, snapshot)
    moves = module_moves(module_map, records['modules'])
    guide_paths = {guide['source']['path']: guide['id'] for guide in records['guides'].values()}
    for aid, page in editorial_algorithms.items():
        records['algorithms'][aid]['guides'] = [guide_paths[path] for path in page.meta.get('source_guides', []) if path in guide_paths]
    return {'schema_version': 1, 'snapshot': snapshot, 'records': records, 'module_moves': moves,
            'renamed': renamed, 'result_aliases': {old: resolve_result(old) for old in result_aliases}}


def publish(model, out, synonyms=None):
    out = Path(out)
    api = out / 'api/v1'
    api.mkdir(parents=True, exist_ok=True)
    directory = {}
    for kind, records in model['records'].items():
        (api / kind).mkdir(exist_ok=True)
        directory[kind] = {}
        for key, record in records.items():
            directory[kind][key] = api_url(kind, key)
            envelope = {'schema_version': 1, 'snapshot': model['snapshot'], 'record_type': kind, 'record': record}
            (api / kind / (record_component(key) + '.json')).write_text(packed(envelope) + '\n')
    (api / 'index.json').write_text(packed(directory) + '\n')
    entries = []
    for kind in ['declarations', 'results', 'algorithms', 'guides']:
        for key, record in model['records'][kind].items():
            names = ([key] if kind == 'declarations' else record['declarations'] if kind == 'results'
                     else [m['declaration'] for m in record['members']] if kind == 'algorithms' else [])
            text = '\n'.join(' '.join(str(model['records']['declarations'][name].get(field, '')) for field in ['id','module','signature','docstring']) for name in names)
            entries.append({'id': key, 'kind': record.get('kind', kind[:-1]), 'title': record.get('title', key),
                'summary': record.get('summary', ''), 'module': record.get('module', ''), 'url': record['url'],
                'record': directory[kind][key], 'search_text': text + ' ' + ' '.join(record.get('aliases', [])) + ' ' + record.get('markdown', ''),
                'admission_reported': record.get('admission_reported', False)})
    search = packed({'schema_version': 1, 'snapshot': model['snapshot'], 'synonyms': synonyms or {}, 'entries': entries})
    (api / 'search-index.json').write_text(search)
    (api / 'search-index.json.gz').write_bytes(gzip.compress(search.encode(), mtime=0))
    legacy = {kind: {key: record['url'] for key, record in model['records'][kind].items()}
              for kind in ['declarations', 'results', 'algorithms', 'modules']}
    legacy['result_focus'] = {}
    for old, new in model['result_aliases'].items():
        if new in legacy['results']:
            legacy['results'][old] = legacy['results'][new]
    for old, (new, _, _) in model['renamed'].items():
        legacy['declarations'][old] = legacy['declarations'][new]
    for old, move in model.get('module_moves', {}).items():
        legacy['modules'][old] = move['url']
    (api / 'legacy-links.json').write_text(packed(legacy) + '\n')
    (api / 'module-moves.json').write_text(packed({'schema_version': 1, 'snapshot': model['snapshot'],
                                                'moves': model.get('module_moves', {})}) + '\n')
    manifest = {'schema_version': 1, 'snapshot': model['snapshot'],
        'records': BASE + 'api/v1/index.json', 'search': BASE + 'api/v1/search-index.json',
        'schema': BASE + 'api/v1/schema.json', 'counts': {kind: len(rs) for kind, rs in model['records'].items()},
        'evidence_policy': 'Tags and associations are discovery metadata, not execution or resource certification. Exact signatures and source fingerprints are preserved.'}
    (api / 'manifest.json').write_text(packed(manifest) + '\n')
    schema = {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'type': 'object',
        'required': ['schema_version', 'snapshot', 'record_type', 'record'],
        'properties': {'schema_version': {'const': 1},
            'snapshot': {'type': 'object', 'required': ['commit', 'extraction_sha256', 'versioned'],
                'properties': {'commit': {'type': ['string', 'null']},
                    'extraction_sha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'},
                    'source_hashes_checked': {'type': 'boolean'}, 'versioned': {'type': 'boolean'}}},
            'record_type': {'enum': list(model['records'])}, 'record': {'type': 'object', 'required': ['id']}}}
    schema['allOf'] = [{'if': {'properties': {'record_type': {'const': 'declarations'}}},
        'then': {'properties': {'record': {'required': ['signature', 'signature_sha256', 'module', 'import',
            'statement_dependencies', 'proof_or_value_dependencies', 'statement_callers',
            'proof_or_value_callers', 'admission_reported', 'source']}}}}]
    (api / 'schema.json').write_text(packed(schema) + '\n')
    # Keep old names and hash links working without retaining the retired app.
    for kind in ['declarations', 'results', 'modules']:
        redirects = dict(legacy[kind])
        for old, destination in redirects.items():
            write_redirect(out / kind / record_component(old) / 'index.html', destination)
            if kind == 'modules' and old in model.get('module_moves', {}):
                write_redirect(out / 'library/modules' / record_component(old) / 'index.html', destination)
    write_redirect(out / 'catalog/index.html', BASE + 'library/modules/')
    write_redirect(out / 'rates/index.html', BASE + 'library/results/')
    return model


def write_redirect(path, destination):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('<!doctype html><meta charset="utf-8"><title>Page moved</title><script>location.replace(' +
                   json.dumps(destination) + '+location.search+location.hash)</script><p><a href="' +
                   html.escape(destination, quote=True) + '">Continue to the library</a>.</p>')


def load_rename_maps(directory):
    """Read every `<YYYY-MM>-<topic>.json` rename map of NLAlib's docs/renames/ (CONTRIBUTING N12):
    `{"renames": [{"old", "new", "rule", "removed"?}], "statementChanged": [names]}`, in file-name
    (date) order. Returns `[(map name, renames, statementChanged)]`; no directory is no maps."""
    if not directory:
        return []
    directory = Path(directory)
    if not directory.is_dir():
        raise SystemExit(f'rename-map directory {directory} does not exist')
    maps = []
    for path in sorted(directory.glob('*.json')):
        raw = json.loads(path.read_text())
        renames, changed = raw.get('renames', []), raw.get('statementChanged', [])
        if not isinstance(raw, dict) or not isinstance(renames, list) or not isinstance(changed, list):
            raise ValueError(f'{path.name}: not a rename map')
        for r in renames:
            if not isinstance(r, dict) or not all(isinstance(r.get(k), str) and r[k] for k in ('old', 'new')):
                raise ValueError(f'{path.name}: a rename needs "old" and "new"')
        if not all(isinstance(n, str) for n in changed):
            raise ValueError(f'{path.name}: statementChanged lists names')
        maps.append((path.stem, renames, changed))
    return maps


def rename_tables(maps, names):
    """`(renamed, changed)` for the declarations in `names`. `renamed[old]` is `[new, removed, map]`
    with `new` followed through later maps to a declaration that exists (an old name that is still a
    declaration is not redirected, and an entry whose target is not in the data is skipped: the map
    may be ahead of the published library); `changed[name]` lists the maps that changed its
    statement, and a name that was renamed afterwards carries them over."""
    step = {}
    for stem, renames, _ in maps:
        for r in renames:
            step[r['old']] = (r['new'], bool(r.get('removed')), stem)
    renamed = {}
    for old, (new, removed, stem) in step.items():
        if old in names:
            continue
        seen = {old}
        while new not in names and new in step and new not in seen:
            seen.add(new)
            new, more, _ = step[new]
            removed = removed or more
        if new in names:
            renamed[old] = [new, removed, stem]
    changed = defaultdict(list)
    for stem, _, listed in maps:
        for n in listed:
            changed[n].append(stem)
    for old, (new, _, _) in step.items():
        # statementChanged lists new names; keep the note on a name that a later map renamed
        if old in changed and renamed.get(old):
            for stem in changed[old]:
                if stem not in changed[renamed[old][0]]:
                    changed[renamed[old][0]].append(stem)
    return renamed, {n: v for n, v in changed.items() if n in names}



ACCENTS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303", "c": "\u0327", "v": "\u030c"}

def tex_accents(s):
    """`in{\\'e}galit{\\'e}`, `\\"o`, `\\c{c}` -> the accented letters."""
    import unicodedata
    s = re.sub(r'\\([\'`^"~]|[cv](?=[{ ]))\s*\{?(\w)\}?', lambda m: unicodedata.normalize(
        'NFC', m.group(2) + ACCENTS[m.group(1)]), s)
    for cmd, ch in (('AA', 'Å'), ('aa', 'å'), ('ss', 'ß'), ('o', 'ø'), ('O', 'Ø'), ('l', 'ł')):
        s = re.sub(r'\\' + cmd + r'(?![a-zA-Z])\s?', ch, s)
    return s.replace('--', '–')


def parse_bib(path):
    """A minimal BibTeX reader: key -> {text, url}."""
    if not path or not Path(path).exists():
        return {}
    src = Path(path).read_text()
    out = {}
    for m in re.finditer(r'@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}', src, re.S):
        kind, key, body = m.groups()
        fields = {}
        for f in re.finditer(r'(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}', body):
            fields[f.group(1).lower()] = re.sub(r'[{}]', '', tex_accents(' '.join(f.group(2).split())))
        authors = [a.strip() for a in fields.get('author', '').split(' and ') if a.strip()]
        names = []
        for a in authors:
            if ',' in a:
                last, first = [x.strip() for x in a.split(',', 1)]
                names.append(f'{first} {last}')
            else:
                names.append(a)
        who = ', '.join(names[:-1]) + (' and ' if len(names) > 1 else '') + (names[-1] if names else '')
        venue = fields.get('journal') or fields.get('booktitle') or fields.get('publisher') or ''
        if fields.get('series') and kind == 'book':
            venue = f"{fields['series']} {fields.get('volume', '')}".strip() + (f", {fields['publisher']}" if fields.get('publisher') else '')
        year = fields.get('year', '')
        if year and venue.endswith(year):
            year = ''                         # `booktitle = {Surveys in Combinatorics, 1989}`
        text = f"{who}. {fields.get('title', '')}. {venue}{', ' if venue and year else ''}{year}."
        url = fields.get('url') or (f"https://doi.org/{fields['doi']}" if fields.get('doi') else
                                    f"https://arxiv.org/abs/{fields['eprint']}" if fields.get('eprint') else None)
        out[key] = {'text': ' '.join(text.split()).replace(' .', '.'), 'url': url}
    return out
