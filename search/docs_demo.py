"""Scripted MCP browsing/restart smoke test; not an LLM search-quality benchmark."""
from __future__ import annotations

import argparse
import asyncio
from contextlib import asynccontextmanager
from datetime import timedelta
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@asynccontextmanager
async def connect(data, source, state):
    args = [str(Path(__file__).with_name('docs_server.py').resolve()), '--data', str(data.resolve()),
            '--state-dir', str(state.resolve())]
    if source:
        args += ['--src', str(source.resolve())]
    async with stdio_client(StdioServerParameters(command=sys.executable, args=args)) as (read, write):
        async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=20)) as client:
            await client.initialize()
            yield client


async def run(data, source, state):
    calls = []

    async def call(client, name, arguments):
        result = await client.call_tool(name, arguments)
        if result.isError:
            raise RuntimeError(result.content[0].text)
        text = result.content[0].text
        budget = arguments.get('max_chars', 8000)
        if len(text) > budget:
            raise AssertionError('Response exceeded its character budget')
        page = json.loads(text)
        calls.append({'tool': name, 'returned_chars': len(text), 'budget_chars': budget,
                      'complete': page['complete']})
        return page

    async with connect(data, source, state) as client:
        info = await call(client, 'docs_info', {})
        arguments = {'prefix': 'NLAlib.Matrix.Pseudoinverse', 'max_chars': 4000}
        while True:
            page = await call(client, 'docs_catalog', arguments)
            if not page['next_cursor']:
                break
            arguments['cursor'] = page['next_cursor']
        overview = await call(client, 'docs_read_module', {'module': 'NLAlib.Matrix.Pseudoinverse.Pinv'})
        if 'NLAlib.pinv_pinv' not in overview['content']:
            raise AssertionError('Expected pseudoinverse involution missing from module overview')
        await call(client, 'docs_read_declaration', {'name': 'NLAlib.pinv_pinv'})
        if source:
            await call(client, 'docs_read_declaration', {'name': 'NLAlib.pinv', 'view': 'definition'})
        await call(client, 'docs_related', {'name': 'NLAlib.pinv_pinv', 'direction': 'callers',
                                           'edge': 'both', 'max_chars': 3000})
        saved = await call(client, 'docs_session', {
            'action': 'create', 'goal': 'Does applying the generalized inverse twice recover the matrix?',
            'bookmarks': ['NLAlib.pinv', 'NLAlib.pinv_pinv'],
            'notes': 'Found the candidate in the module overview. No concrete Lean application checked.',
            'open_questions': ['Instantiate the exact lemma in the intended proof context.']})
        session_id = saved['session_id']

    # New OS process and MCP connection: the previous server's Python memory is gone.
    async with connect(data, source, state) as client:
        restored = await call(client, 'docs_session', {'action': 'get', 'session_id': session_id})
        if 'No concrete Lean application checked' not in restored['content']:
            raise AssertionError('Reading state did not survive restart')
        await call(client, 'docs_context', {'names': ['NLAlib.pinv_pinv'], 'max_chars': 3000})
    return {'scripted_walkthrough': True, 'llm_quality_evaluated': False,
            'commit': info['commit'], 'data_sha256': info['data_sha256'],
            'candidate': 'NLAlib.pinv_pinv', 'lean_application_checked': False,
            'session_id': session_id, 'restart_recovery': True,
            'total_returned_chars': sum(c['returned_chars'] for c in calls), 'calls': calls}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--src', type=Path)
    p.add_argument('--state-dir', type=Path, default=Path(__file__).resolve().parents[1] / '.docs-state')
    a = p.parse_args()
    print(json.dumps(asyncio.run(run(a.data, a.src, a.state_dir)), indent=2))


if __name__ == '__main__':
    main()
