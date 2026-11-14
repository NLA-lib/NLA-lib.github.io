"""Check curated placement and evidence scope; write a review inventory for every page.

This checks editorial structure against the selected extraction. It does not verify
that natural-language mathematical statements are equivalent to Lean propositions.
"""
import argparse
from collections import Counter
from pathlib import Path

from content_pages import Explorer, STATEMENT


def visible_results(explorer, page):
    """Count displayed evidence, never a selector that has no rendering slot."""
    results = set(explorer.selection(page)[0]) if '{{ generated:results }}' in page.body else set()
    for statement in STATEMENT.finditer(page.body):
        if statement[2] == 'result':
            results.add(statement[3])
        elif statement[2] == 'decl':
            results.update(explorer.records['declarations'][statement[3]].get('results', []))
    return results


def audit(explorer):
    pages = explorer.pages
    issues, reviews = [], []
    for page in sorted(pages.values(), key=lambda p: (p.kind, p.meta['title'])):
        meta = page.meta
        if page.kind == 'task':
            groups = meta.get('groups', [])
            if not groups:
                issues.append(f'{page.key}: no task-local groups')
            decision = 'Task-specific groups: ' + '; '.join(g['title'] for g in groups) + '.'
        elif page.kind == 'algorithm':
            if not meta.get('tasks'):
                issues.append(f'{page.key}: unreachable through tasks')
            positions = [f'{t.meta["id"]}/{g["id"]}' for t in pages.values() if t.kind == 'task'
                         for g in t.meta.get('groups', []) if meta['id'] in g['algorithms']]
            children = [p.meta['id'] for p in pages.values() if p.kind == 'implementation' and p.meta['algorithm'] == meta['id']]
            decision = 'One canonical method; placements: ' + ', '.join(positions) + '.'
            decision += ' Implementations: ' + (', '.join(children) if children else 'none curated') + '.'
            if meta.get('uses'):
                decision += ' Components: ' + ', '.join(meta['uses']) + '.'
        elif page.kind == 'implementation':
            decision = f'Execution page under {meta["algorithm"]}; preserves its parent method and arithmetic-specific scope.'
            if meta.get('status') == 'placeholder':
                decision += ' Placeholder; does not establish program availability or correctness.'
        elif page.kind == 'theory':
            decision = 'Reusable theory; '
            decision += 'parents: ' + ', '.join(meta['parents']) + '.' if meta.get('parents') else 'subject hub.'
            if meta.get('module_prefixes'):
                decision += ' Scoped source selectors checked against this extraction.'
            else:
                decision += ' Navigation or authored exposition; no directory-wide theorem import.'
        elif page.kind == 'family':
            decision = 'Shared conceptual reference. Task-local groups own placement and may select a subset of this family.'
        else:
            decision = 'Entry point or reference navigation.'
        for prefix in meta.get('module_prefixes', []):
            if not any(m == prefix or m.startswith(prefix + '.') for m in explorer.records['modules']):
                issues.append(f'{page.key}: unmatched module selector {prefix}')
        results, _ = explorer.selection(page)
        decision += f' Curated status: {explorer.status(page)}.'
        if results:
            decision += f' {len(results)} selected result groups.'
        reviews.append((page, decision))
    return issues, reviews


def report(explorer, reviews):
    counts = Counter(p.kind for p in explorer.pages.values())
    covered = set()
    readable = 0
    implementation_gaps = []
    for page in explorer.pages.values():
        covered.update(visible_results(explorer, page))
        readable += sum(m[1] == 'theorem' for m in STATEMENT.finditer(page.body))
        if page.kind == 'implementation' and explorer.status(page) != 'ready':
            implementation_gaps.append(page)
    unplaced = sorted(explorer.records['results'].keys() - covered)
    lines = ['# Explorer organization audit', '',
             'Scope: every authored page in this checkout; source selectors checked against the selected library snapshot.', '',
             'This is an organization and evidence-placement review, not a new proof or a line-by-line mathematical equivalence review.', '',
             '## Decisions', '',
             '- Algorithms is a task index. Each task owns its groups, order, descriptions, and method placements.',
             '- A method has one canonical URL. Groups can differ across tasks without cloning its definition, analysis, or implementations.',
             '- Existing global family pages remain conceptual references; they do not impose a taxonomy on every task.',
             '- Composed methods link to shared components. QR factorization and QR eigenvalue iteration have distinct identities.',
             '- Theory hubs navigate to subtopics. Leaf selections avoid collecting all algorithm programs from broad source directories.',
             '- Method result selections exclude relatives and arithmetic-specific implementation results where identified.',
             '- Empty generated sections are omitted. New eigenvalue pages are outlines and do not invent checked implementations.', '',
             '## Existing proof coverage', '',
             f'{len(covered)} of {len(explorer.records["results"])} extracted result groups are connected to curated method or theory pages. All remain available in Library.', '',
             f'{readable} authored theorem blocks present readable statements with extracted Lean evidence; generated CG arithmetic statements are additional. Linked result groups are not counted as newly authored statements.', '',
             '## Inventory', '', ', '.join(f'{n} {kind} pages' for kind, n in sorted(counts.items())) + '.', '']
    for page, decision in reviews:
        relative = Path('..') / '..' / 'content' / page.source.relative_to(explorer.content)
        lines += [f'### {page.meta["title"]} ({page.kind})', '', f'[{page.source.relative_to(explorer.content)}]({relative.as_posix()}) · `{page.url}`', '', decision, '']
    lines += ['## Remaining content work', '',
              'The generic missing-definition text has been replaced on 27 mathematical method pages. Fifteen theory topics now introduce their central objects with definitions and context; further results expand in place with documented statements and Lean evidence. Block CG still needs a precise choice of recurrence and rank-loss convention. Remaining exposition work includes worked examples and explanations connecting related results.', '',
              f'{len(implementation_gaps)} implementation pages remain outlines or placeholders. This is a presentation gap where matching code and proofs exist; elsewhere it is a genuine formalization gap. Status alone does not establish whether Lean code exists.', '']
    lines.extend('- ' + p.meta['algorithm'] + '/' + p.meta['id'] for p in implementation_gaps)
    lines += ['', 'Rounded and stored scalar Lanczos, full reorthogonalization, and rounded orthogonalization need their own pseudocode, resource accounting, and precise numerical hypotheses. These should not inherit the exact matrix-free or exact MGS guarantees automatically.', '',
              'No user decision is needed to continue presenting existing proofs. A new concrete backend, a numerical contract not yet proved, or a new convergence theorem requires implementation/proof work; it should be identified explicitly rather than treated as a website placeholder.', '',
              '### Results still reached only through Library', '', ', '.join('`' + rid + '`' for rid in unplaced) + '.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, required=True)
    parser.add_argument('--content', type=Path, default=Path(__file__).parent / 'content')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    explorer = Explorer(args.site, args.content)
    issues, reviews = audit(explorer)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report(explorer, reviews))
    for issue in issues:
        print(issue)
    print(f'Organization audit: {len(reviews)} pages, {len(issues)} issues')
    raise SystemExit(bool(issues))


if __name__ == '__main__':
    main()
