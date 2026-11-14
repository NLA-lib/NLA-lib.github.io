"""Audit all named mathematics, tagged methods, modules, and snapshot continuity.

Only visible curated statements count as placements. All exported public declarations
must retain their generated Library record. Source hashes and tags are checked against
one matching checkout; private/auxiliary constants are outside the extraction's scope.
"""
import argparse
from collections import defaultdict
import hashlib
import html
import json
from pathlib import Path
import re
import tomllib

from audit_organization import visible_results
from content_pages import Explorer, STATEMENT
from rendering import record_component

RESULT_TAG = re.compile(r'^[ \t]*Result:[ \t]*([^\n]*)', re.M)
ALGORITHM_TAG = re.compile(r'^\s*Algorithm:\s*([a-z0-9-]+)(?:\s*\([^)]*\))?\s*$', re.M)


def tags(text):
    return {tag for match in RESULT_TAG.finditer(text or '')
            for tag in re.findall(r'[a-z0-9]+(?:-[a-z0-9]+)*', match[1].split('-/')[0])}


def audit_math(explorer, data, source, *, baseline=None, renames=None, published_baseline=None):
    source = Path(source)
    issues = []
    overrides = tomllib.loads(Path(__file__).with_name('results.toml').read_text())
    def canonical(key):
        seen = set()
        while overrides.get(key, {}).get('merge_into'):
            if key in seen:
                raise ValueError('result alias cycle')
            seen.add(key)
            key = overrides[key]['merge_into']
        return key
    placements = defaultdict(list)
    method_placements = defaultdict(set)
    declarations = {d['name']: d for d in data['decls']}
    tagged_methods = defaultdict(set)
    for declaration in data['decls']:
        for match in ALGORITHM_TAG.finditer(declaration.get('doc') or ''):
            tagged_methods[match[1]].add(declaration['name'])
    for page in explorer.pages.values():
        for rid in visible_results(explorer, page):
            placements[canonical(rid)].append(page.url)
        if page.meta.get('library_algorithm'):
            method_placements[page.meta['library_algorithm']].add(page.url)
        if page.kind == 'algorithm' and page.meta['id'] in tagged_methods:
            method_placements[page.meta['id']].add(page.url)
        bound = {m[3] for m in STATEMENT.finditer(page.body) if m[2] == 'decl'}
        for method, members in tagged_methods.items():
            if bound.intersection(members):
                method_placements[method].add(page.url)
    paths = {m['path'] for m in data['modules']}
    source_paths = {str(p.relative_to(source)) for p in (source / 'NLAlib').rglob('*.lean')}
    # Some extractor revisions include the import-only root aggregator, others
    # enumerate only the source modules below NLAlib/. Scan its tags either way.
    if 'NLAlib.lean' in paths:
        source_paths.add('NLAlib.lean')
    unexported = sorted(source_paths - paths)
    missing_sources = sorted(paths - source_paths)
    mismatches = [path for path in sorted(paths) if not (source / path).is_file() or
                  hashlib.sha256((source / path).read_bytes()).hexdigest() != data.get('sourceHashes', {}).get(path)]
    source_tags = set().union(*(tags((source / path).read_text()) for path in sorted(source_paths)))
    if (source / 'NLAlib.lean').is_file():
        source_tags.update(tags((source / 'NLAlib.lean').read_text()))
    extracted_tags = set().union(*(tags(d.get('doc') or '') for d in data['decls']))
    missing_tags = sorted(source_tags - extracted_tags)
    unknown_tags = sorted({canonical(t) for t in extracted_tags} - explorer.records['results'].keys())
    missing_declarations = sorted(declarations.keys() - explorer.records['declarations'].keys())
    missing_modules = sorted(m['name'] for m in data['modules'] if m['name'] not in explorer.records['modules'])
    unplaced = sorted(explorer.records['results'].keys() - placements.keys())
    unplaced_methods = sorted(tagged_methods.keys() - method_placements.keys())
    missing_rendered_evidence = []
    if getattr(explorer, 'site', None):
        rendered = {}
        for rid, urls in placements.items():
            primary = explorer.records['results'][rid]['primary']
            signature = explorer.records['declarations'][primary]['signature']
            present = False
            for url in urls:
                if url not in rendered:
                    path = explorer.site / url.removeprefix('/explore/') / 'index.html'
                    rendered[url] = html.unescape(path.read_text()) if path.is_file() else ''
                if signature and signature in rendered[url]:
                    present = True
                    break
            if not present:
                missing_rendered_evidence.append(rid)
    for label, values in [('unexported source modules', unexported), ('missing source files', missing_sources),
                          ('source hash mismatches', mismatches), ('unextracted Result tags', missing_tags),
                          ('unindexed Result tags', unknown_tags), ('missing public declarations', missing_declarations),
                          ('missing module records', missing_modules), ('unplaced named results', unplaced),
                          ('missing rendered theorem evidence', missing_rendered_evidence),
                          ('unplaced tagged methods', unplaced_methods)]:
        if values:
            issues.append({'check': label, 'items': values})
    continuity = None
    if baseline:
        old = {d['name']: d for d in baseline['decls']}
        renamed = {}
        changed = set()
        for path in sorted(Path(renames).glob('*.json')) if renames else []:
            mapping = json.loads(path.read_text())
            for item in mapping.get('renames', []):
                renamed[item['old']] = item['new']
            changed.update(mapping.get('statementChanged', []))
        removed = []
        for name in sorted(old.keys() - declarations.keys()):
            target, seen = name, set()
            while target in renamed and target not in seen:
                seen.add(target)
                target = renamed[target]
            resolved = target in declarations
            removed.append({'old': name, 'new': target if resolved else None,
                            'statement_changed': target in changed})
            if not resolved:
                issues.append({'check': 'unaccounted removed declaration', 'items': [name]})
            elif getattr(explorer, 'site', None) and not (explorer.site / 'library/declarations' / record_component(name) / 'index.html').is_file():
                issues.append({'check': 'missing renamed canonical URL', 'items': [name]})
        old_tags = set().union(*(tags(d.get('doc') or '') for d in baseline['decls']))
        lost_tags = sorted({canonical(t) for t in old_tags} - explorer.records['results'].keys())
        if lost_tags:
            issues.append({'check': 'lost baseline result IDs', 'items': lost_tags})
        changed_named = [name for name in sorted(old.keys() & declarations.keys())
                         if tags(old[name].get('doc') or '') and old[name].get('signature') != declarations[name].get('signature')]
        bound_names = set()
        for page in explorer.pages.values():
            for statement in STATEMENT.finditer(page.body):
                if statement[2] == 'decl':
                    bound_names.add(statement[3])
                elif statement[2] == 'result':
                    bound_names.add(explorer.records['results'][statement[3]]['primary'])
        changed_authored = [name for name in sorted(bound_names & old.keys() & declarations.keys())
                            if old[name].get('signature') != declarations[name].get('signature')]
        continuity = {'baseline_commit': baseline.get('commit') or baseline.get('base_commit'),
                      'new_result_tags': sorted(extracted_tags - old_tags), 'lost_result_tags': lost_tags,
                      'renamed_declarations': removed, 'changed_named_signatures': changed_named,
                      'authored_bindings_with_changed_signature': changed_authored}
    published = None
    if published_baseline:
        old_api = Path(published_baseline) / 'api/v1'
        manifest = json.loads((old_api / 'manifest.json').read_text())
        old_commit = manifest['snapshot']['commit']
        module_map = json.loads((Path(renames) / '2026-11-ops-modules.json').read_text())
        retired = set(module_map['retired_modules']) if module_map['from_commit'] == old_commit else set()
        reconciliation = json.loads(Path(__file__).with_name('legacy_math_reconciliation.json').read_text())
        dispositions = reconciliation['declarations'] if reconciliation['from_commit'] == old_commit else {}
        old_decls = {d['id']: d for path in (old_api / 'declarations').glob('*.json')
                     for d in [json.loads(path.read_text())['record']]}
        old_results = {r['id']: r for path in (old_api / 'results').glob('*.json')
                       for r in [json.loads(path.read_text())['record']]}
        retired_results, unknown_results = [], []
        for rid in sorted(old_results):
            if canonical(rid) in explorer.records['results']:
                continue
            modules = {old_decls[name]['module'] for name in old_results[rid]['declarations']}
            if modules and modules <= retired:
                retired_results.append({'id': rid, 'modules': sorted(modules)})
            else:
                unknown_results.append(rid)
        if unknown_results:
            issues.append({'check': 'unaccounted published result IDs', 'items': unknown_results})
        renamed_published = {}
        for path in Path(renames).glob('*.json'):
            for entry in json.loads(path.read_text()).get('renames', []):
                renamed_published[entry['old']] = entry['new']
        retired_decls, renamed_decls, rewritten, helpers, unknown = [], [], [], [], []
        for name in sorted(old_decls.keys() - declarations.keys()):
            old = old_decls[name]
            disposition = dispositions.get(name, {})
            if old['module'] in retired:
                retired_decls.append(name)
            elif renamed_published.get(name) in declarations:
                renamed_decls.append({'old': name, 'new': renamed_published[name]})
            elif disposition.get('old_module') == old['module'] and disposition.get('old_kind') == old['kind']:
                entry = {'old': name, **disposition}
                if disposition['status'] == 'rewritten-interface' and all(n in declarations for n in disposition['current']):
                    rewritten.append(entry)
                elif disposition['status'] in {'syntax-helper', 'generated-helper'}:
                    helpers.append(entry)
                else:
                    unknown.append(name)
            else:
                unknown.append(name)
        if unknown:
            issues.append({'check': 'unaccounted published declarations', 'items': unknown})
        published = {'commit': old_commit, 'result_groups': len(old_results),
                     'retained_result_groups': len(old_results) - len(retired_results) - len(unknown_results),
                     'retired_execution_result_groups': retired_results, 'unaccounted_result_ids': unknown_results,
                     'public_declarations': len(old_decls), 'retained_public_declarations': len(old_decls.keys() & declarations.keys()),
                     'retired_execution_declarations': len(retired_decls), 'renamed_declarations': renamed_decls,
                     'rewritten_math_interfaces': rewritten, 'syntax_or_generated_helpers': helpers,
                     'unaccounted_declarations': unknown}
    return {'snapshot_commit': data.get('commit'), 'counts': {'source_modules': len(source_paths),
            'public_declarations': len(declarations), 'raw_result_ids': len(extracted_tags),
            'indexed_result_groups': len(explorer.records['results']), 'curated_result_groups': len(placements),
            'tagged_methods': len(tagged_methods), 'placed_tagged_methods': len(method_placements.keys() & tagged_methods.keys())},
            'continuity': continuity, 'published_baseline': published, 'issues': issues,
            'result_placements': {k: sorted(set(v)) for k, v in sorted(placements.items())},
            'method_placements': {k: sorted(v) for k, v in sorted(method_placements.items())}}


def markdown_report(result):
    counts = result['counts']
    lines = ['# Mathematical coverage audit', '', f'Source snapshot: `{result["snapshot_commit"]}`.', '',
             'Scope: every local source module, every exported public declaration, every `Result:` ID, and every `Algorithm:` discovery tag. Private and generated auxiliary constants are excluded by the Lean extractor.', '',
             '## Coverage', '']
    lines += [f'- {key.replace("_", " ")}: {value}' for key, value in counts.items()]
    lines += ['', f'{len(result["issues"])} unresolved audit checks.', '',
              'A result counts only when a statement is authored on a page or a generated results slot actually renders it. A metadata selector alone does not count. Multiple names for the same primary declaration can share one displayed statement.', '']
    continuity = result['continuity']
    if continuity:
        lines += ['## Snapshot continuity', '', f'{len(continuity["new_result_tags"])} new named results; {len(continuity["lost_result_tags"])} lost baseline result IDs.', '']
        for rename in continuity['renamed_declarations']:
            lines += [f'- `{rename["old"]}` → `{rename["new"]}`' + ('; statement changed explicitly in the rename map.' if rename['statement_changed'] else '; documented rename.')]
        lines += ['', 'These are documented replacements, not a claim that the old and new statements are identical.', '',
                  'Named declarations whose signatures changed:', '']
        lines += ['- `' + name + '`' for name in continuity['changed_named_signatures']]
        lines += ['', 'Authored statement bindings whose signatures changed:', '']
        lines += ['- `' + name + '`' for name in continuity['authored_bindings_with_changed_signature']] or []
        if not continuity['authored_bindings_with_changed_signature']:
            lines += ['None.']
    published = result.get('published_baseline')
    if published:
        lines += ['', '## Original published explorer', '', f'Baseline: `{published["commit"]}`.', '',
                  f'{published["retained_result_groups"]} named mathematical result groups remain present. '
                  f'{len(published["retired_execution_result_groups"])} old execution-result groups were retired by the explicit Ops module migration map. '
                  f'{len(published["unaccounted_result_ids"])} published result IDs are unaccounted for.', '',
                  f'Of {published["public_declarations"]} old public records: {published["retained_public_declarations"]} retain their names; '
                  f'{published["retired_execution_declarations"]} belong to retired execution modules; '
                  f'{len(published["renamed_declarations"])} have documented renames; '
                  f'{len(published["rewritten_math_interfaces"])} are explicitly rewritten math interfaces; '
                  f'{len(published["syntax_or_generated_helpers"])} are syntax or generated helpers. '
                  f'{len(published["unaccounted_declarations"])} are unaccounted for.', '',
                  'Rewritten interfaces, not unchanged aliases:', '']
        for entry in published['rewritten_math_interfaces']:
            lines += ['- `' + entry['old'] + '` → ' + ', '.join('`' + n + '`' for n in entry['current']) + '. ' + entry['reason']]
        lines += ['', 'Retired execution-result IDs:', '', ', '.join('`' + entry['id'] + '`' for entry in published['retired_execution_result_groups']) + '.', '',
                  'The retired entries are not represented as guarantees of the new Ops programs. Their recorded retirement is distinct from losing a mathematical result.']
    lines += ['', '## Findings addressed', '',
              '- Refresh the stale extraction before importing the newer source statements; all source hashes must match.',
              '- Add ordinary, early-truncated, and late-truncated GN navigation and abbreviation search.',
              '- Restore mathematical results that existed only in unused metadata selections, including further exact CG results.',
              '- Add canonical pages for previously missing projection, stationary, polar, sign, and Hessenberg methods.',
              '- Put shared algebra, spectral structure, matrix equations, finite-precision Krylov analysis, and low-rank structural lemmas on scoped theory pages.',
              '- Retain checked shifted-QR interfaces and its current source guide without inventing a simplified execution or cost theorem.', '',
              '## Remaining presentation limits', '',
              'Coverage is not a mathematical equivalence review of every prose statement. Some pages still use source-documented expandable results rather than editorial explanations. Outline implementation pages still need readable pseudocode and numerical/resource summaries; discovery tags never certify those programs by themselves.', '',
              'See the separate [implementation presentation review](implementation-presentation-audit.md) for confirmed gaps between indexed coverage and headline guarantees. Passing this audit does not close those presentation gaps.', '',
              '## Result placements', '']
    for rid, urls in result['result_placements'].items():
        lines += [f'- `{rid}`: ' + ', '.join(f'[{url}]({url})' for url in urls)]
    if result['issues']:
        lines += ['', '## Unresolved checks', '', '```json', json.dumps(result['issues'], indent=2), '```']
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', required=True, type=Path)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--extraction', required=True, type=Path)
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--published-baseline', type=Path, help='Saved published explorer directory containing api/v1')
    parser.add_argument('--renames', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    if args.published_baseline and not args.renames:
        parser.error('--published-baseline requires --renames for retirement and rename evidence')
    explorer = Explorer(args.site, Path(__file__).parent / 'content')
    result = audit_math(explorer, json.loads(args.extraction.read_text()), args.source,
                        baseline=json.loads(args.baseline.read_text()) if args.baseline else None, renames=args.renames,
                        published_baseline=args.published_baseline)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(markdown_report(result))
    if args.json:
        args.json.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'counts': result['counts'], 'issues': result['issues']}, indent=2))
    raise SystemExit(bool(result['issues']))


if __name__ == '__main__':
    main()
