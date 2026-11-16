"""List the results whose headline declaration still needs a decision.

A result with several declarations needs an explicit `primary` in `results.toml`; without
one the build falls back to the first theorem by name. A headline whose signature carries a
size as an index type still needs an integer-size corollary. This reads the records of a
built site and judges no mathematics.
"""
import argparse
import json
from pathlib import Path

from library import primary_report


def load_records(site):
    api = Path(site) / 'api/v1'
    return {kind: {record['id']: record for record in
                   (json.loads(path.read_text())['record'] for path in (api / kind).glob('*.json'))}
            for kind in ['results', 'declarations']}


def report(summary):
    unchosen, index_typed = summary['unchosen'], summary['index_typed']
    lines = [f'# Results with several declarations and no explicit primary ({len(unchosen)})', '']
    for row in unchosen:
        lines.append(f'{row["id"]} ({len(row["declarations"])} declarations)')
        lines.extend(('  * ' if name == row['primary'] else '    ') + name for name in row['declarations'])
    lines += ['', '`*` marks the fallback: the first theorem by name.', '',
              f'# Headlines whose sizes are index types ({len(index_typed)})', '']
    lines.extend(f'{row["id"]}: {row["primary"]}' + ('' if row['explicit'] or len(row['declarations']) < 2 else ' (fallback primary)')
                 for row in index_typed)
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, required=True)
    parser.add_argument('--report', type=Path, help='write the full list here instead of printing it')
    parser.add_argument('--strict', action='store_true', help='fail while a result has no explicit primary')
    args = parser.parse_args()
    summary = primary_report(load_records(args.site))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report(summary))
    else:
        print(report(summary))
    print(f'Primary audit: {summary["results"]} results, {summary["multiple"]} with several declarations, '
          f'{len(summary["unchosen"])} without an explicit primary, '
          f'{len(summary["index_typed"])} headlines with index-typed sizes')
    raise SystemExit(bool(args.strict and summary['unchosen']))


if __name__ == '__main__':
    main()
