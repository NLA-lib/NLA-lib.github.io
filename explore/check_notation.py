#!/usr/bin/env python3
"""Check authored math; --expressions feeds the vendored KaTeX compiler in CI."""
import argparse
import json
from pathlib import Path
from notation import diagnostics, math_spans, policy

def collect(content):
    rules=policy();expressions=[];issues=[]
    for file in sorted(content.rglob('*.md')):
        text=file.read_text();key=file.relative_to(content).as_posix()
        for issue in diagnostics(text,rules.get(key)):
            issues.append({'path':key,**issue})
        for start,end,tex,display in math_spans(text)[0]:
            expressions.append({'path':key,'line':text.count('\n',0,start)+1,'tex':tex,'display':display})
    return expressions,issues

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--expressions',action='store_true');args=parser.parse_args()
    expressions,issues=collect(Path(__file__).with_name('content'))
    if args.expressions:print(json.dumps({'expressions':expressions,'issues':issues}));raise SystemExit(0)
    for issue in issues:print(f"{issue['path']}:{issue['line']}: {issue['severity']}: {issue['message']}")
    print(f'{len(expressions)} authored equations; {sum(i["severity"]=="error" for i in issues)} blocking notation errors.')
    raise SystemExit(any(issue['severity']=='error' for issue in issues))
