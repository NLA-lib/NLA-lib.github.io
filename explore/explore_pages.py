"""Canonical static Explore pages and proof-free, snapshot-pinned agent records.

The existing builder owns statement curation, facets and rate validation. This module
projects that same data into pages; it does not infer execution guarantees from tags.
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import gzip
import html
import json
from pathlib import Path
import posixpath
import re
from urllib.parse import quote, unquote
from facets import ALGORITHM_DEFS, OUTPUTS


BASE = '/explore/'
ALGORITHM_SLUGS = {'cg': 'conjugate-gradient', 'pcg': 'preconditioned-conjugate-gradient'}
TASK_SLUGS = {'low-rank-one-two-pass': 'low-rank-approximation',
              'estimation': 'trace-estimation', 'matrix': 'matrix-analysis'}


def packed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def fingerprint(signature):
    return hashlib.sha256((signature or '').encode()).hexdigest()


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def record_component(key):
    """One physical path component; URL quoting adds the HTTP encoding separately."""
    component = str(key).replace('%', '%25').replace('/', '%2F').replace('\\', '%5C')
    return component.replace('.', '%2E') if component in {'.', '..'} else component


def route(kind, key=''):
    return BASE + kind + ('/' + quote(record_component(key), safe='.') if key else '') + '/'


def declaration_url(name):
    return route('declarations', name)


def make_records(raw, site, config):
    """Normalized records. Inferred associations are distinct from reviewed evidence."""
    source = {d['name']: d for d in raw['decls']}
    decls = site['decls']
    names = {d['n']: d for d in decls}
    snapshot = dict(raw.get('_provenance', {}))
    snapshot.setdefault('commit', raw.get('commit'))
    snapshot.setdefault('date', raw.get('date'))
    snapshot.setdefault('extraction_sha256', fingerprint(packed({
        k: v for k, v in raw.items() if not k.startswith('_')})))
    snapshot.setdefault('fingerprint_kind', 'canonical-json')
    snapshot.setdefault('source_hashes_checked', False)
    snapshot.setdefault('toolchain', None)
    snapshot['versioned'] = bool(re.fullmatch(r'[0-9a-f]{40}', snapshot.get('commit') or ''))
    records = {'declarations': {}, 'results': {}, 'algorithms': {}, 'tasks': {},
               'theory': {}, 'modules': {}, 'implementations': {}, 'bounds': {}, 'guarantees': {}}
    callers = defaultdict(list)
    value_callers = defaultdict(list)
    for d in raw['decls']:
        for dep in d.get('typeDeps', []):
            callers[dep].append(d['name'])
        for dep in d.get('valueDeps', []):
            value_callers[dep].append(d['name'])
    for d in decls:
        original = source[d['n']]
        path = original['module'].replace('.', '/') + '.lean'
        records['declarations'][d['n']] = {
            'id': d['n'], 'kind': d['k'], 'url': declaration_url(d['n']),
            'module': d['m'], 'import': 'import ' + d['m'],
            'signature': original.get('signature') or '',
            'signature_sha256': fingerprint(original.get('signature')),
            'statement': original.get('statement') or original.get('signature') or '',
            'docstring': original.get('doc') or '', 'summary': d.get('fs') or '',
            'admission_reported': bool(original.get('sorry')),
            'statement_dependencies': original.get('typeDeps', []),
            'proof_or_value_dependencies': original.get('valueDeps', []),
            'statement_callers': sorted(callers[d['n']]),
            'proof_or_value_callers': sorted(value_callers[d['n']]),
            'results': d['r'], 'facets': d.get('fc', {}),
            'references': [{'key': key, 'locator': locator, **site['bib'].get(key, {})}
                           for key, locator in d.get('ci', [])],
            'source': {'path': path, 'line': d['l'], 'end_line': d['e'],
                       'sha256': raw.get('sourceHashes', {}).get(path),
                       'url': (f"{site['repo']}/blob/{snapshot['commit']}/{path}#L{d['l'] or 1}"
                               if snapshot['versioned'] else None)},
        }
    for rid, r in site['results'].items():
        records['results'][rid] = {
            'id': rid, 'title': r['title'], 'url': route('results', rid),
            'declarations': [decls[i]['n'] for i in r['decls']],
            'primary': decls[r['overview']]['n'],
            'forms': [{'overview': decls[f['overview']]['n'],
                       'explicit': decls[f['explicit']]['n']} for f in r['forms']],
        }
    owned_labels = {ALGORITHM_DEFS[decls[m['i']]['n']][0]
                    for a in site['algorithms']['pages'].values() for m in a['members']
                    if decls[m['i']]['n'] in ALGORITHM_DEFS}
    for aid, a in site['algorithms']['pages'].items():
        title = a['title']
        # An unconfigured algorithm uses its documented bold name when available.
        if title in {decls[m['i']]['n'].rsplit('.', 1)[-1] for m in a['members']}:
            first = a.get('first', a['members'][0]['i'])
            documented = re.search(r'\*\*(.+?)\*\*', source[decls[first]['n']].get('doc') or '', re.S)
            if documented:
                title = documented[1].rstrip('.').strip()
                title = title[:1].upper() + title[1:]
        records['algorithms'][aid] = {
            'id': aid, 'title': title,
            'url': route('algorithms', ALGORITHM_SLUGS.get(aid, aid)),
            'facet': a['facet'],
            'members': [{'declaration': decls[m['i']]['n'], 'role': m['role']} for m in a['members']],
            'results': sorted(set(sum(a['sections'].values(), []))),
            'implementations': [], 'associations': 'discovery metadata; not execution evidence',
        }
        members = {decls[m['i']]['n'] for m in a['members']}
        labels = {ALGORITHM_DEFS[name][0] for name in members if name in ALGORITHM_DEFS}
        forms = defaultdict(list)
        for name, d in records['declarations'].items():
            output, label = d['facets'].get('output'), d['facets'].get('algorithm')
            if (d['kind'] == 'theorem' and output in OUTPUTS and label
                    and members.intersection(d['statement_dependencies'])
                    and (label in labels or label not in owned_labels)
                    and (output != 'plain' or label not in labels)):
                forms[label, output].append(name)
        variants = records['algorithms'][aid]['output_variants'] = []
        for (label, output), declarations in forms.items():
            key = output if label in labels else slug(label) + '-' + output
            title = OUTPUTS[output].capitalize() if label in labels else label[:1].upper() + label[1:] + (' · ' + OUTPUTS[output] if output != 'plain' else '')
            variants.append({'id': key, 'title': title, 'output': output, 'algorithm': label,
                             'composition': label not in labels,
                             'url': records['algorithms'][aid]['url'] + '#output-' + key,
                             'declarations': declarations})
        variants.sort(key=lambda v: (v['algorithm'] not in labels, v['algorithm'].casefold(),
                                     v['output'] != 'plain', v['output']))
        # Registered exact targets explicitly name their trees. A cost-only program tag
        # never supplies an execution connection. Retain the complete target statement.
        for c in a['cost']:
            if c['proof'] is None:
                continue
            if decls[c['proof']]['s']:
                raise ValueError(f'registered execution proof has an admitted dependency: {c["name"]}')
            for tree in c['trees'] or [None]:
                proof = decls[c['proof']]['n']
                existing = next((r for r in records['implementations'].values()
                                 if tree and r['algorithm'] == aid and r['program'] == tree
                                 and r['evidence'] == 'registered-target-proof'), None)
                if existing:
                    existing['targets'].append(c['name'])
                    existing['output_theorems'].append(proof)
                    continue
                iid = aid + '--' + slug(tree or c['name'])
                records['implementations'][iid] = {
                    'id': iid, 'algorithm': aid, 'program': tree,
                    'arithmetic': ('rounding contract specified by target' if 'rounded' in c['model'] else 'exact arithmetic'),
                    'access_model': c['model'], 'target': c['name'], 'targets': [c['name']],
                    'execution_theorem': proof, 'output_theorems': [proof],
                    'run_model': None, 'precomputed_inputs': c['precomputed'],
                    'evidence': 'registered-target-proof',
                    'scope': 'The target statement fixes inputs, output, arithmetic, counts and memory.',
                    'external_services': ('Exact scalar arithmetic; matrix oracle; random tape where drawn.'
                                          if 'matrix-free' in c['model'] else
                                          'Exact scalar arithmetic and input reads; random tape where drawn. No successful matrix-oracle call.'),
                    'service_definitions': [
                        {'text': label, 'declaration': 'NLAlib.Computation.' + name}
                        for label, name in ([('Exact scalar arithmetic', 'exactSem'),
                                             ('matrix oracle', 'matOracle'), ('random tape', 'exactInterp')]
                                            if 'matrix-free' in c['model'] else
                                            [('Exact scalar arithmetic', 'exactSem'),
                                             ('input reads', 'storedInterp'), ('random tape', 'storedInterp')])
                        if 'NLAlib.Computation.' + name in names],
                }
                if 'rounded' in c['model']:
                    records['implementations'][iid]['external_services'] = 'Scalar semantics, oracle and kernel services, and random tape, as specified by the registered target.'
                    records['implementations'][iid]['service_definitions'] = [
                        {'text': label, 'declaration': 'NLAlib.Computation.' + name}
                        for label, name in [('Scalar semantics', 'ScalarSem'),
                                            ('oracle and kernel services', 'Interp'), ('random tape', 'Interp')]
                        if 'NLAlib.Computation.' + name in names]
                records['algorithms'][aid]['implementations'].append(iid)

    # A distinct method named by theorem facets is a peer, even when its expression uses
    # another algorithm's definition (for example a filtered test matrix).
    compositions = defaultdict(list)
    for aid, algorithm in list(records['algorithms'].items()):
        for form in algorithm['output_variants']:
            if form['composition']:
                compositions[form['algorithm']].append((aid, form))
        algorithm['output_variants'] = [v for v in algorithm['output_variants'] if not v['composition']]
    for label, forms in compositions.items():
        aid = slug(label)
        if aid in records['algorithms']:
            continue
        statements = sorted({name for _, form in forms for name in form['declarations']})
        variants = []
        for output, title in OUTPUTS.items():
            declarations = sorted({name for _, form in forms if form['output'] == output
                                   for name in form['declarations']})
            if declarations and output != 'plain':
                variants.append({'id': output, 'title': title.capitalize(), 'output': output,
                                 'algorithm': label, 'composition': False,
                                 'url': route('algorithms', aid) + '#output-' + output,
                                 'declarations': declarations})
        records['algorithms'][aid] = {
            'id': aid, 'title': label[:1].upper() + label[1:], 'url': route('algorithms', aid),
            'facet': label, 'members': [], 'implementations': [],
            'results': sorted({rid for name in statements for rid in records['declarations'][name]['results']}),
            'output_variants': variants,
            'statement_declarations': sorted({name for _, form in forms if form['output'] == 'plain'
                                              for name in form['declarations']}),
            'related_algorithms': sorted({base for base, _ in forms}),
            'representation': 'composition in theorem statements',
            'associations': 'discovery metadata; not execution evidence',
        }

    # Optional reviewed links: absent from an older snapshot -> not recorded. A partial
    # or changed link -> fail rather than quietly preserving an implementation claim.
    for item in config.get('implementations', []):
        evidence = [item['execution_theorem'], *item.get('output_theorems', [])]
        if not any(n in names for n in evidence):
            continue
        for n in [item['program'], item['run_model'], *evidence]:
            if n not in names:
                raise ValueError(f'implementation {item["id"]}: missing declaration {n}')
            if names[n]['s']:
                raise ValueError(f'implementation {item["id"]}: admitted declaration {n}')
        for service in item.get('service_definitions', []):
            if service['declaration'] not in names:
                raise ValueError(f'implementation {item["id"]}: missing service definition {service["declaration"]}')
        if item['algorithm'] not in records['algorithms']:
            raise ValueError(f'implementation {item["id"]}: unknown algorithm')
        for n in evidence:
            if source[n]['kind'] != 'theorem':
                raise ValueError(f'implementation {item["id"]}: evidence is not a theorem: {n}')
            if fingerprint(source[n].get('signature')) != item['signatures'].get(n):
                raise ValueError(f'implementation {item["id"]}: review changed signature: {n}')
            if item['program'] not in source[n].get('typeDeps', []):
                raise ValueError(f'implementation {item["id"]}: statement does not name program: {n}')
        if item['run_model'] not in source[item['execution_theorem']].get('typeDeps', []):
            raise ValueError(f'implementation {item["id"]}: statement does not name run model')
        iid = item['id']
        if iid in records['implementations']:
            raise ValueError(f'duplicate implementation id: {iid}')
        records['implementations'][iid] = {k: v for k, v in item.items() if k != 'signatures'}
        records['implementations'][iid]['evidence'] = 'reviewed-statement-link'
        records['algorithms'][item['algorithm']]['implementations'].append(iid)

    family_task = {'embeddings': 'sketching', 'low-rank-one-two-pass': 'low-rank-approximation',
                   'low-rank-krylov': 'low-rank-approximation', 'regression': 'least-squares',
                   'trace-estimation': 'trace-estimation'}
    for guarantee in site['rates']['guarantees']:
        records['guarantees'][guarantee['id']] = {
            'id': guarantee['id'], 'title': guarantee['title'],
            'description': guarantee.get('description', ''),
            'definitions': [d['declaration'] for d in guarantee.get('definitions', [])],
        }
    for group in site['rates']['groups']:
        records['guarantees'].setdefault(group['id'], {
            'id': group['id'], 'title': group['title'], 'description': '', 'definitions': []})
    for c in site['collections']:
        tid = TASK_SLUGS.get(c['id'], c['id'])
        refs = [e for g in c['groups'] for e in g['entries']]
        results = sorted({e['rid'] for e in refs if e['type'] == 'r'})
        definitions = sorted({decls[e['i']]['n'] for e in refs if e['type'] == 'd'})
        related = [aid for aid, a in records['algorithms'].items()
                   if set(a['results']) & set(results) or
                   any(m['declaration'] in definitions for m in a['members'])]
        ordered = []
        for group in c['groups']:
            for entry in group['entries']:
                for aid in related:
                    algorithm = records['algorithms'][aid]
                    matches = (entry['rid'] in algorithm['results'] if entry['type'] == 'r' else
                               any(m['declaration'] == decls[entry['i']]['n'] for m in algorithm['members']))
                    if matches and aid not in ordered:
                        ordered.append(aid)
        related = ordered + [aid for aid in related if aid not in ordered]
        groups = []
        for group in c['groups']:
            group_definitions = {decls[e['i']]['n'] for e in group['entries'] if e['type'] == 'd'}
            group_results = {e['rid'] for e in group['entries'] if e['type'] == 'r'}
            if group.get('id', 'other') != 'other':
                for algorithm in records['algorithms'].values():
                    if any(m['declaration'] in group_definitions for m in algorithm['members']):
                        group_results.update(set(algorithm['results']) & set(results))
            groups.append({'id': group.get('id', 'other'), 'title': group.get('title', 'Results'), 'results': sorted(group_results)})
        classified = {rid for group in groups if group['id'] != 'other' for rid in group['results']}
        for group in groups:
            if group['id'] == 'other':
                group['results'] = [rid for rid in group['results'] if rid not in classified]
        records['tasks'][tid] = {'id': tid, 'title': c['title'], 'description': c['description'],
                                'summary': config.get('tasks', {}).get(tid, {}).get('summary', ''),
                                'url': route(tid), 'results': results,
                                'definitions': definitions, 'algorithms': related, 'bounds': [],
                                'result_groups': groups,
                                'bounds_layout': config.get('tasks', {}).get(tid, {}).get('bounds_layout', 'resources')}
    for tid, spec in config.get('tasks', {}).items():
        prefixes = spec.get('include_modules', [])
        if not prefixes:
            continue
        def in_topic(module):
            return any(module == prefix or module.startswith(prefix + '.') for prefix in prefixes)
        results = sorted(rid for rid, result in records['results'].items()
                         if any(in_topic(names[n]['m']) for n in result['declarations']))
        definitions = sorted(n for n, d in names.items() if in_topic(d['m'])
                             and d['k'] in {'def', 'abbrev', 'structure', 'class', 'inductive'}
                             and d.get('role') != 'support')
        if not results and not definitions:
            continue
        related = [aid for aid, a in records['algorithms'].items()
                   if set(a['results']) & set(results)
                   or any(m['declaration'] in definitions for m in a['members'])]
        records['tasks'][tid] = {'id': tid, 'title': spec['title'], 'description': spec['summary'],
                                'summary': spec['summary'], 'url': route(tid), 'results': results,
                                'definitions': definitions, 'algorithms': related, 'bounds': []}
    for i, row in enumerate(site['rates']['entries']):
        categories = [key for key, task in records['tasks'].items() if row.get('result') in task['results']]
        tid = family_task.get(row['family']) or next(iter(categories), 'other-bounds')
        if tid not in records['tasks']:
            records['tasks'][tid] = {'id': tid, 'title': 'Other bounds', 'description': '',
                                     'summary': 'Additional resource bounds not yet assigned to a task.',
                                     'url': route(tid), 'results': [], 'definitions': [],
                                     'algorithms': [], 'bounds': []}
        name = decls[row['overview']]['n']
        bid = row.get('id') or name
        if tid not in categories:
            categories.append(tid)
        records['bounds'][bid] = {
            'id': bid, 'task': tid, 'categories': categories, 'theorem': name, 'result': row.get('result'),
            'family': row['family'], 'facets': row.get('c', {}),
            'resources': row.get('resources', []), 'notes': row.get('notes') or '',
            'review_status': row['status'], 'kind': row.get('kind', 'rate'),
            'lower': row.get('lower', []), 'pairs_with': row.get('pairs_with'),
            'guarantee': row.get('group'),
        }
        for category in categories:
            records['tasks'][category]['bounds'].append(bid)
    for key, result in records['results'].items():
        result['categories'] = [tid for tid, task in records['tasks'].items() if key in task['results']]
    for key, algorithm in records['algorithms'].items():
        algorithm['categories'] = [tid for tid, task in records['tasks'].items() if key in task['algorithms']]
    for topic in site['topics']:
        mods = [n for n, m in site['modules'].items() if m['topic'] == topic['id']]
        if mods:
            key = slug(topic['id'])
            records['theory'][key] = {'id': key, 'title': topic['title'], 'description': topic['blurb'],
                                     'url': route('theory', key), 'modules': mods}
    for t in config.get('theory', []):
        mods = [n for n in site['modules'] if any(n.startswith(p) for p in t['prefixes'])]
        if mods:
            records['theory'][t['id']] = {'id': t['id'], 'title': t['title'],
                                         'description': t['description'], 'url': route('theory', t['id']),
                                         'modules': mods}
    all_modules = dict(site['modules'])
    for d in decls:
        all_modules.setdefault(d['m'], {'title': d['m'], 'summary': '', 'imports': []})
    for name, m in all_modules.items():
        records['modules'][name] = {'id': name, 'title': m['title'], 'summary': m['summary'],
                                    'url': route('modules', name), 'imports': m['imports'],
                                    'declarations': [d['n'] for d in decls if d['m'] == name]}
    return {'schema_version': 1, 'snapshot': snapshot, 'records': records}


def inline_title(text):
    """Titles share the same safe math/code markup in headings and links."""
    parts = re.split(r'(\$\$.*?\$\$|\$[^$\n]+\$|`[^`]+`)', text)
    return ''.join('<span class="math">' + html.escape(p.strip('$')) + '</span>' if p.startswith('$')
                   else '<code>' + html.escape(p[1:-1]) + '</code>' if p.startswith('`')
                   else html.escape(p) for p in parts)


class Pages:
    def __init__(self, model, site, out, prose):
        self.model, self.site, self.out, self.prose = model, site, Path(out), prose
        self.records = model['records']
        self.decls = {d['n']: d for d in site['decls']}
        self.versions = {name: hashlib.sha256((self.out / name).read_bytes()).hexdigest()[:12]
                         for name in ['css/site.css', 'style.css', 'explore.css', 'explore.js', 'explore-search.js', 'api/v1/search-index.json']}

    def link(self, kind, key, label=None):
        r = self.records[kind][key]
        text = label or r.get('title') or key
        return f'<a href="{html.escape(r["url"], quote=True)}">{inline_title(text)}</a>'

    def markdown(self, text, module=None):
        rendered = self.prose(text or '', self.decls)
        rendered = re.sub(r'href="#d/([^\"]+)"', lambda m:
                          f'href="{declaration_url(unquote(m[1]))}"', rendered)
        def local_link(match):
            target = html.unescape(match[1])
            if target.rstrip('/').removeprefix('./') == 'rates':
                return f'href="{BASE}"'
            if module and target.endswith('.lean'):
                path = posixpath.normpath(posixpath.dirname(module.replace('.', '/')) + '/' + target)
                name = path.removesuffix('.lean').replace('/', '.')
                if name in self.records['modules']:
                    return f'href="{self.records["modules"][name]["url"]}"'
            return match[0]
        return re.sub(r'href="([^\"]+)"', local_link, rendered)

    def listing(self, kind, keys):
        items = []
        for key in keys:
            if key not in self.records[kind]:
                continue
            item = self.link(kind, key)
            if kind == 'algorithms' and self.records[kind][key].get('output_variants'):
                item += '<ul class="entry-list algorithm-variants">' + ''.join(
                    '<li><a href="' + v['url'] + '">' + html.escape(v['title']) + '</a></li>'
                    for v in self.records[kind][key]['output_variants']) + '</ul>'
            items.append('<li>' + item + '</li>')
        return '<ul class="entry-list">' + ''.join(items) + '</ul>'

    def write(self, path, title, body, record=None):
        depth = len(Path(path).parts) if path else 0
        root = '../' * depth or './'
        snap = self.model['snapshot']
        metadata = ''
        if record:
            kind, key = record
            api = f'api/v1/{kind}/{quote(record_component(key), safe=".")}.json'
            metadata = f'<p class="record-link"><a href="{BASE + api}">Structured JSON record</a></p>'
        nav = '<a href="/">Home</a><a href="/explore/" class="here" aria-current="page">Explorer</a><a href="/design/">Design</a><a href="https://github.com/NLA-lib/nlalib">GitHub</a>'
        page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape('NLA-lib · Explorer' + (' · ' + title if path else ''))}</title><meta name="description" content="{html.escape(title, quote=True)} — statements, assumptions and formal proof building blocks in NLAlib.">
<link rel="canonical" href="https://nla-lib.org/explore/{quote(path, safe='/.') + '/' if path else ''}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="{root}css/site.css?v={self.versions['css/site.css']}">
<link rel="stylesheet" href="{root}style.css?v={self.versions['style.css']}"><link rel="stylesheet" href="{root}explore.css?v={self.versions['explore.css']}">
<link rel="stylesheet" href="{root}vendor/katex/katex.min.css">
<script defer src="{root}vendor/katex/katex.min.js"></script><script defer src="{root}explore-search.js?v={self.versions['explore-search.js']}"></script><script defer src="{root}explore.js?v={self.versions['explore.js']}"></script>
</head><body class="explore-pages" data-root="{root}" data-snapshot="{snap['extraction_sha256']}" data-search-version="{self.versions['api/v1/search-index.json']}"><a class="skip-link" href="#content">Skip to content</a>
<div id="contentContainer" class="page-wrap"><header><h1>NLA-lib Explorer</h1><nav class="menu" aria-label="Site">{nav}</nav>
<form id="site-search" action="{BASE}search/" role="search"{' hidden' if path == 'search' else ''}><label class="visually-hidden" for="site-query">Search the library</label>
<div class="search-line"><input id="site-query" name="q" type="search" placeholder="Search theorems and definitions"><button>Search</button></div></form><div id="quick-search" class="quick-search" hidden></div></header>
<main id="content">{('<h2 class="page-title">' + inline_title(title) + '</h2>') if path else ''}{body}{metadata}</main>
<footer>Library snapshot <code>{html.escape((snap.get('commit') or 'unversioned')[:12])}</code> ·
<a href="{BASE}api/v1/manifest.json">Snapshot and data manifest</a> · <a href="{BASE}catalog/">Source catalogue and dependency graphs</a></footer></div>
</body></html>'''
        target = self.out / path / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)

    def declaration(self, name):
        d = self.records['declarations'][name]
        brief = self.decls[name]
        body = '<p class="eyebrow">' + html.escape(d['kind']) + ' · ' + self.link('modules', d['module']) + '</p>'
        if d['admission_reported']:
            body += '<p class="notice">This extraction reports an admitted dependency. Do not treat it as a completed proof.</p>'
        body += self.markdown(brief.get('stmt') or d['docstring'], d['module'])
        body += '<h2>Formal API</h2><p>All assumptions and typeclasses are retained in this extracted signature.</p>'
        body += f'<pre id="signature"><code>{html.escape(d["signature"])}</code></pre>'
        body += f'<pre id="import"><code>{html.escape(d["import"])}</code></pre>'
        if d['kind'] != 'theorem' and d['statement'] != d['signature']:
            body += '<details><summary>Definition and hypothesis fields</summary><pre class="definition"><code>' + html.escape(d['statement']) + '</code></pre></details>'
        if d['source']['url']:
            body += f'<p><a href="{html.escape(d["source"]["url"], quote=True)}">Source at this library commit</a></p>'
        if brief.get('no'):
            body += '<h2>Notes and restrictions</h2>' + self.markdown('\n\n'.join(brief['no']), d['module'])
        if brief.get('rel'):
            body += '<h2>Related API</h2>' + self.markdown('\n\n'.join(brief['rel']), d['module'])
        body += '<h2>Related results</h2>' + self.listing('results', d['results'])
        for key, label, explanation in [
                ('statement_dependencies', 'Statement dependencies', 'Declarations directly referenced in this declaration’s Lean type.'),
                ('proof_or_value_dependencies', 'Proof or definition dependencies', 'Declarations directly referenced in this declaration’s proof or definition body.')]:
            dependencies = [name for name in d[key] if name in self.records['declarations']]
            body += f'<details id="{key.replace("_", "-")}"><summary>{label} ({len(dependencies)})</summary><p>{explanation}</p>'
            body += self.listing('declarations', dependencies) if dependencies else '<p>No direct dependencies recorded in this snapshot.</p>'
            body += '</details>'
        for key, label, explanation in [
                ('statement_callers', 'Used in statement types', 'These declarations directly reference this declaration in their Lean types.'),
                ('proof_or_value_callers', 'Used in proofs or definitions', 'These declarations directly reference this declaration in their proof or definition bodies.')]:
            users = [name for name in d[key] if name in self.records['declarations']]
            body += f'<details><summary>{label} ({len(users)})</summary><p>{explanation} Indirect uses are not expanded.</p>'
            body += self.listing('declarations', users) if users else '<p>No direct uses recorded in this snapshot.</p>'
            body += '</details>'
        cites = brief.get('ci') or []
        if cites:
            body += '<h2>Literature references</h2><p>The formal statement may generalize or otherwise differ from the cited source; inspect its assumptions and notes.</p><ul class="entry-list">'
            for key, label in cites:
                ref = self.site['bib'].get(key, {})
                body += '<li>' + html.escape(key + (', ' + label if label else '') + '. ' + ref.get('text', ''))
                if ref.get('url'):
                    body += ' <a href="' + html.escape(ref['url'], quote=True) + '">Publication</a>'
                body += '</li>'
            body += '</ul>' + self.markdown('\n\n'.join(brief.get('cn') or []))
        self.write('declarations/' + record_component(name), name, body, ('declarations', name))

    def result(self, rid):
        r = self.records['results'][rid]
        body = '<p>Each statement below retains its own assumptions and arithmetic model.</p>'
        for name in r['declarations']:
            d = self.records['declarations'][name]
            body += '<section><h2>' + self.link('declarations', name) + '</h2>'
            body += self.markdown(self.decls[name].get('stmt') or '', d['module'])
            body += '<p>' + self.link('declarations', name, 'Full signature, import and related lemmas') + '</p></section>'
        self.write('results/' + rid, r['title'], body, ('results', rid))

    def implementation(self, iid):
        i = self.records['implementations'][iid]
        def definition_link(name):
            return self.link('declarations', name, name.removeprefix('NLAlib.'))
        services = {ref['text']: ref['declaration'] for ref in i.get('service_definitions', [])}
        service_pattern = '(' + '|'.join(re.escape(text) for text in sorted(services, key=len, reverse=True)) + ')'
        services_html = ''.join(self.link('declarations', services[part], part) if part in services else html.escape(part)
                                for part in re.split(service_pattern, i['external_services'])) if services else html.escape(i['external_services'])
        rows = [('Execution theorem', definition_link(i['execution_theorem'])),
                ('Supplied services', services_html)]
        outputs = [name for name in i['output_theorems'] if name != i['execution_theorem']]
        if outputs:
            rows.append(('Output theorems', '<br>'.join(definition_link(name) for name in outputs)))
        if i.get('targets'):
            rows.append(('Registered statements', '<br>'.join(definition_link(name) for name in i['targets'])))
        if i.get('run_model'):
            rows.append(('Run interface', definition_link(i['run_model'])))
        arithmetic = i['arithmetic'][:1].upper() + i['arithmetic'][1:]
        return '<details class="implementation implementation-details"><summary><span>' + html.escape(arithmetic) + '</span><span class="implementation-action">Proof and assumptions</span></summary><div class="implementation-panel"><dl>' + ''.join(
            f'<dt>{label}</dt><dd>{value}</dd>' for label, value in rows) + '</dl>' + self.markdown(i['scope']) + '</div></details>'

    def algorithm(self, aid):
        a = self.records['algorithms'][aid]
        primary = next((m['declaration'] for m in a['members'] if m['role'] == 'specification'), None)
        if primary is None:
            primary = next((m['declaration'] for m in a['members'] if m['role'] == 'definition'), None)
        body = self.markdown(self.decls[primary].get('stmt') or '') if primary else ''
        if a.get('representation'):
            body += '<p>This method is expressed as a composition in the library. Its formal mathematical statements are listed below.</p>'
        body += '<h2>Implementations</h2><p>Each program lists its arithmetic models. Expand a model for assumptions and proof links.</p>'
        groups = defaultdict(list)
        for iid in a['implementations']:
            item = self.records['implementations'][iid]
            groups[item['program'] or iid].append(iid)
        for ids in groups.values():
            item = self.records['implementations'][ids[0]]
            name = item['program']
            title = self.link('declarations', name, name.removeprefix('NLAlib.')) if name else 'Parameterized program family'
            body += '<section class="implementation-program"><h3>' + title + ' <span class="muted">' + html.escape(item['access_model']) + '</span></h3><div class="arithmetic-models">'
            body += ''.join(self.implementation(iid) for iid in ids) + '</div></section>'
        if not groups:
            body += '<p class="notice">No execution connection is recorded for this algorithm in this snapshot. Mathematical analysis remains available below.</p>'
        body += '<h2>Mathematical specification and analysis</h2><ul class="entry-list">'
        for m in a['members']:
            if m['role'] == 'program':
                continue
            body += '<li>' + self.link('declarations', m['declaration']) + ' <span class="muted">' + html.escape(m['role']) + '</span></li>'
        body += '</ul>'
        if a.get('statement_declarations'):
            body += self.listing('declarations', a['statement_declarations'])
        body += '<h2>Compare bounds</h2><ul class="entry-list">'
        for t in self.records['tasks'].values():
            if aid in t['algorithms']:
                body += '<li><a href="' + t['url'] + '#bounds">' + inline_title(t['title']) + '</a></li>'
        body += '</ul>'
        for variant in a['output_variants']:
            body += '<details class="category-section"><summary><h2 id="output-' + variant['id'] + '">' + html.escape(variant['title']) + ' output</h2></summary>' + self.listing('declarations', variant['declarations']) + '</details>'
        body += '<h2>Related mathematical results</h2>' + self.listing('results', a['results'])
        body += '<p>Membership in this list is for discovery; it does not assert a connection to every implementation above.</p>'
        self.write('algorithms/' + ALGORITHM_SLUGS.get(aid, aid), a['title'], body, ('algorithms', aid))

    def task(self, tid):
        t = self.records['tasks'][tid]
        description = t['description'].replace('[Rates page](rates/)', '[bounds below](#bounds)')
        body = self.markdown(description) + '<details class="category-section"><summary><h2 id="algorithms">Algorithms</h2></summary>' + self.listing('algorithms', t['algorithms']) + '</details>'
        bounds = [self.records['bounds'][k] for k in t['bounds']]
        grouped_results = t.get('bounds_layout') == 'result_groups'
        if grouped_results:
            body += '<details class="category-section"><summary><h2 id="bounds">Results and bounds</h2></summary>'
            for group in t['result_groups']:
                if group['results']:
                    body += '<details class="bound-group"><summary><h3 class="bound-title">' + inline_title(group['title']) + '</h3></summary>' + self.listing('results', group['results']) + '</details>'
            body += '</details>'
        elif bounds:
            body += '<details class="category-section"><summary><h2 id="bounds">Compare bounds</h2></summary><p>Expand a bound for its assumptions and formal statement. Resource summaries are editorial; their review status is shown. Different guarantees and statistics need not be comparable.</p>'
            for gid in dict.fromkeys(r['guarantee'] for r in bounds):
                group = [r for r in bounds if r['guarantee'] == gid]
                guarantee = self.records['guarantees'].get(gid)
                body += '<details class="bound-group" data-bound-group><summary><h3 class="bound-title">' + inline_title(guarantee['title'] if guarantee else 'Additional bounds') + '</h3></summary>'
                if guarantee:
                    body += '<div class="bound-guarantee">' + self.markdown(guarantee['description']) + '</div>'
                for r in group:
                    d = self.decls[r['theorem']]
                    facets = r['facets']
                    label = ' · '.join(str(facets[k]) for k in ['algorithm', 'law', 'output'] if facets.get(k))
                    if not label:
                        label = d.get('nm') or (self.records['results'].get(r['result']) or {}).get('title') or 'Bound'
                    if r['kind'] == 'lower':
                        label = 'Lower bound · ' + label
                    body += '<details class="bound-entry" data-bound data-facets="' + html.escape(packed(facets), quote=True) + '"><summary><span class="bound-summary"><strong>' + inline_title(label) + '</strong>'
                    for resource in r['resources']:
                        body += '<span class="bound-size">' + inline_title(resource['label']) + ': ' + inline_title(resource['bound']) + '</span>'
                    body += '</span></summary><div class="bound-body">'
                    if r['notes']:
                        body += '<div class="bound-assumptions">' + self.markdown(r['notes']) + '</div>'
                    body += self.markdown(d.get('stmt') or '', d['m'])
                    source = facets.get('source') or ''
                    body += '<p class="bound-source">' + self.link('declarations', r['theorem'], 'Formal statement and source')
                    if source:
                        body += ' · ' + html.escape(source)
                    if r['review_status'] != 'reviewed':
                        body += ' · Summary awaiting review'
                    body += '</p></div></details>'
                body += '</details>'
            body += '</details>'
        else:
            body += '<p>No resource-summary rows are recorded here. The results below include explicit bounds and conditional analysis.</p>'
        if not grouped_results:
            body += '<details class="category-section"><summary><h2>Results and explicit bounds</h2></summary>' + self.listing('results', t['results']) + '</details>'
        body += '<details class="category-section"><summary><h2>Definitions and proof building blocks</h2></summary>' + self.listing('declarations', t['definitions']) + '</details>'
        self.write(tid, t['title'], body, ('tasks', tid))
        self.redirect('bounds/' + tid, t['url'])

    def redirect(self, path, destination):
        target = self.out / path / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Explorer</title><link rel="canonical" href="https://nla-lib.org' + destination + '"><script>location.replace(' + json.dumps(destination) + '+location.search+location.hash)</script><p><a href="' + destination + '">Continue to Explorer</a></p></html>')

    def render(self):
        r = self.records
        tasks = '<ul class="entry-list category-list">' + ''.join('<li>' + self.link('tasks', key) + '</li>' for key in r['tasks']) + '</ul>'
        self.write('', 'NLA-lib Explorer', '<p class="lead">Definitions, algorithms and bounds, organized by topic.</p>' + tasks)
        self.redirect('bounds', BASE)
        for kind, title in [('algorithms', 'Algorithms'), ('theory', 'Mathematical theory'), ('modules', 'Source modules')]:
            self.write(kind, title, self.listing(kind, r[kind]))
        self.write('search', 'Search the library', '<p>Search names, mathematical descriptions and signatures. Search retrieves candidates; Lean checks whether a candidate solves your goal.</p><form id="library-search"><label for="query">Question, symbol or Lean name</label><input id="query" name="q" type="search"><label for="kind">Kind</label><select id="kind" name="kind"><option value="">All</option><option>theorem</option><option>def</option><option>structure</option><option>result</option><option>algorithm</option></select><button>Search</button></form><p id="search-status" role="status"></p><ol id="search-results"></ol><button type="button" id="more-results" hidden>More results</button><noscript><p>Use the <a href="../modules/">module index</a> to browse without JavaScript.</p></noscript>')
        for name in r['declarations']:
            self.declaration(name)
        for rid in r['results']:
            self.result(rid)
        for aid in r['algorithms']:
            self.algorithm(aid)
        for tid in r['tasks']:
            self.task(tid)
        for key, t in r['theory'].items():
            self.write('theory/' + key, t['title'], self.markdown(t['description']) + self.listing('modules', t['modules']), ('theory', key))
        for name, m in r['modules'].items():
            self.write('modules/' + name, m['title'], self.markdown(m['summary'], name) + '<h2>Public API</h2>' + self.listing('declarations', m['declarations']) + '<h2>Imports</h2>' + self.listing('modules', m['imports']), ('modules', name))


def publish(model, site, out, prose):
    out = Path(out)
    records = model['records']
    api = out / 'api/v1'
    api.mkdir(parents=True, exist_ok=True)
    directory = {}
    for kind, rs in records.items():
        (api / kind).mkdir(exist_ok=True)
        directory[kind] = {}
        for key, record in rs.items():
            url = BASE + f'api/v1/{kind}/{quote(record_component(key), safe=".")}.json'
            directory[kind][key] = url
            envelope = {'schema_version': 1, 'snapshot': model['snapshot'], 'record_type': kind, 'record': record}
            (api / kind / (record_component(key) + '.json')).write_text(packed(envelope) + '\n')
    (api / 'index.json').write_text(packed(directory) + '\n')
    entries = []
    def declaration_text(name):
        declaration = records['declarations'][name]
        module = records['modules'].get(declaration['module'], {})
        return '\n'.join([declaration['module'], declaration['signature'], declaration['docstring'], module.get('title', ''),
                          *(ref['key'] + ' ' + ref.get('text', '') for ref in declaration['references'])])
    for kind in ['declarations', 'results', 'algorithms']:
        for key, r in records[kind].items():
            names = ([key] if kind == 'declarations' else r['declarations'] if kind == 'results'
                     else [member['declaration'] for member in r['members']])
            search_text = '\n'.join(declaration_text(name) for name in names)
            if kind == 'algorithms':
                search_text += '\n' + '\n'.join(declaration_text(name)
                    for variant in r['output_variants'] for name in variant['declarations'])
                search_text += '\n' + '\n'.join(declaration_text(name) for name in r.get('statement_declarations', []))
                search_text += '\n' + ' '.join(site['algorithms']['pages'].get(key, {}).get('aliases', []))
            # Retrieval needs terms, not repeated prose or complete formatted signatures.
            # Full signatures remain in the declaration records and pages.
            search_text = ' '.join(dict.fromkeys(re.findall(r'\w+', search_text.lower())))
            entries.append({'id': key, 'kind': r.get('kind', kind[:-1]), 'title': r.get('title', key),
                            'search_text': search_text,
                            'summary': r.get('summary', '')[:300],
                            'module': r.get('module'), 'url': r['url'], 'record': directory[kind][key],
                            'admission_reported': r.get('admission_reported', False)})
    (api / 'search-index.json').write_text(packed({'schema_version': 1, 'snapshot': model['snapshot'], 'synonyms': site.get('synonyms', {}), 'entries': entries}) + '\n')
    (api / 'search-index.json.gz').write_bytes(gzip.compress((api / 'search-index.json').read_bytes(), mtime=0))
    legacy = {'results': {rid: r['url'] for rid, r in records['results'].items()},
              'result_focus': {rid: declaration_url(site['decls'][i]['n']) for rid, i in site.get('aliasFocus', {}).items()},
              'declarations': {n: r['url'] for n, r in records['declarations'].items()},
              'algorithms': {aid: r['url'] for aid, r in records['algorithms'].items()},
              'modules': {n: r['url'] for n, r in records['modules'].items()}}
    for old, new in site.get('resultAlias', {}).items():
        if new in legacy['results']:
            legacy['results'][old] = legacy['results'][new]
    for old, value in site.get('renamed', {}).items():
        if value[0] in legacy['declarations']:
            legacy['declarations'][old] = legacy['declarations'][value[0]]
    (api / 'legacy-links.json').write_text(packed(legacy) + '\n')
    manifest = {'schema_version': 1, 'snapshot': model['snapshot'],
                'records': BASE + 'api/v1/index.json', 'search': BASE + 'api/v1/search-index.json',
                'schema': BASE + 'api/v1/schema.json',
                'counts': {k: len(v) for k, v in records.items()},
                'evidence_policy': 'Associations are discovery aids. Implementation links require registered targets or reviewed, fingerprinted theorem statements. Fingerprints detect change; they are not proofs of the editorial interpretation.'}
    (api / 'manifest.json').write_text(packed(manifest) + '\n')
    schema = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        'title': 'NLAlib Explore record envelope', 'type': 'object',
        'required': ['schema_version', 'snapshot', 'record_type', 'record'],
        'properties': {
            'schema_version': {'const': 1},
            'snapshot': {'type': 'object', 'required': ['commit', 'extraction_sha256', 'versioned'],
                         'properties': {'commit': {'type': ['string', 'null']},
                                        'extraction_sha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'},
                                        'versioned': {'type': 'boolean'},
                                        'source_hashes_checked': {'type': 'boolean'},
                                        'toolchain': {'type': ['string', 'null']}}},
            'record_type': {'enum': list(records)},
            'record': {'type': 'object', 'required': ['id'],
                       'properties': {'id': {'type': 'string'}}},
        },
        'allOf': [{
            'if': {'properties': {'record_type': {'const': 'declarations'}}},
            'then': {'properties': {'record': {'required': [
                'signature', 'import', 'module', 'statement_dependencies',
                'proof_or_value_dependencies', 'statement_callers', 'proof_or_value_callers', 'admission_reported', 'source']}}},
        }, {
            'if': {'properties': {'record_type': {'const': 'implementations'}}},
            'then': {'properties': {'record': {'required': [
                'program', 'algorithm', 'execution_theorem', 'arithmetic', 'access_model', 'evidence']}}},
        }],
    }
    (api / 'schema.json').write_text(packed(schema) + '\n')
    Pages(model, site, out, prose).render()


PROSE_SPAN = re.compile(r'(`+)(.+?)\1|\$\$(.+?)\$\$|\$([^$\n]+?)\$', re.S)
LEAN_NAME = re.compile(r"^[A-Za-z_][\w'.]*$")


def prose_html(text, names=(), missing=None):
    """A prose page (`pages/<name>.md`) as HTML, for readers without the library's docstrings.

    The Markdown is the subset the app's `md` reads: `#` headings (`#` is the page's h2, `##` an h3),
    paragraphs, `-` and `1.` lists, fenced code blocks (shown as `pre.lean`), **bold**, *italic*, [links](url) and `code`. A backticked library name
    (`rsvd` or `NLAlib.rsvd`) links to its declaration, `#d/<name>`, which opens in the panel; other
    backticked words that look like names are appended to `missing`, so a rename shows in the build
    log. Maths in `$…$` and `$$…$$` stays TeX, escaped, in `.math` spans (`.math.display` for
    displays) that `web/app.js` typesets with KaTeX."""
    def inline(src):
        slots = []

        def keep(markup):
            slots.append(markup)
            return f'\x00{len(slots) - 1}\x00'

        def lift(m):
            if m[2] is not None:
                code = m[2].strip()
                full = code if code in names else 'NLAlib.' + code if 'NLAlib.' + code in names else None
                if full:
                    return keep(f'<a href="#d/{quote(full)}"><code>{html.escape(code)}</code></a>')
                if missing is not None and LEAN_NAME.match(code):
                    missing.append(code)
                return keep(f'<code>{html.escape(code)}</code>')
            if m[3] is not None:
                return keep(f'<span class="math display">{html.escape(m[3].strip(), quote=False)}</span>')
            return keep(f'<span class="math">{html.escape(m[4], quote=False)}</span>')

        s = html.escape(PROSE_SPAN.sub(lift, src), quote=False)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'(?<![*\w])\*([^*\s](?:[^*]*[^*\s])?)\*(?!\*)', r'<em>\1</em>', s)
        s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)',
                   lambda m: f'<a href="{m[2].replace(chr(34), "&quot;")}">{m[1]}</a>', s)
        return re.sub(r'\x00(\d+)\x00', lambda m: slots[int(m[1])], s)

    fences = []

    def fence(m):
        fences.append(m[1])
        return f'\n\n\x01{len(fences) - 1}\x01\n\n'

    text = re.sub(r'^```[^\n]*\n(.*?)\n?^```[ \t]*$', fence, text.replace('\r', ''), flags=re.S | re.M)
    out = []
    for block in re.split(r'\n[ \t]*\n', text.strip()):
        if not block.strip():
            continue
        code = re.fullmatch(r'\s*\x01(\d+)\x01\s*', block)
        if code:
            out.append(f'<pre class="lean">{html.escape(fences[int(code[1])], quote=False)}</pre>')
            continue
        lines = block.split('\n')
        head = re.match(r'(#{1,4})\s+(.*)$', lines[0])
        if head:
            tag = f'h{len(head[1]) + 1}'
            out.append(f'<{tag}>{inline(head[2])}</{tag}>')
            lines = lines[1:]
            if not lines:
                continue
        bullet = r'\s*-\s+' if re.match(r'\s*-\s+', lines[0]) else r'\s*\d+\.\s+'
        if re.match(bullet, lines[0]):
            items = []
            for line in lines:
                if re.match(bullet, line):
                    items.append(re.sub('^' + bullet, '', line))
                else:
                    items[-1] += ' ' + line.strip()
            tag = 'ul' if '-' in bullet else 'ol'
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(t)}</li>' for t in items) + f'</{tag}>')
            continue
        para = ' '.join(line.strip() for line in lines)
        display = re.fullmatch(r'\$\$((?:(?!\$\$).)+)\$\$', para, re.S)
        if display:
            out.append(f'<div class="math display">{html.escape(display[1].strip(), quote=False)}</div>')
        else:
            out.append(f'<p>{inline(para)}</p>')
    return '\n'.join(out)
