"""Exercise the actual MCP stdio wire protocol, not just decorated Python functions."""
import importlib.util
from datetime import timedelta
import json
from pathlib import Path
import sys
import unittest

SDK_AVAILABLE = importlib.util.find_spec('mcp') is not None
ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(SDK_AVAILABLE, 'Install search/requirements-docs.txt for MCP integration tests')
class DocumentationMCPTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import test_docs
        self.fixture = test_docs.DocumentationTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def parameters(self):
        from mcp import StdioServerParameters
        return StdioServerParameters(command=sys.executable, args=[
            str(ROOT / 'search' / 'docs_server.py'), '--data', str(self.fixture.data),
            '--src', str(self.fixture.root), '--state-dir', str(self.fixture.root / 'state')])

    async def test_discovery_reading_resources_prompt_and_budgets(self):
        from mcp import ClientSession
        from mcp.client.stdio import stdio_client
        async with stdio_client(self.parameters()) as (read, write):
            async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=15)) as client:
                await client.initialize()
                tools = await client.list_tools()
                self.assertEqual({t.name for t in tools.tools}, {
                    'docs_info', 'docs_catalog', 'docs_read_module', 'docs_read_declaration',
                    'docs_search', 'docs_related', 'docs_context', 'docs_session'})
                for tool in tools.tools:
                    self.assertEqual(tool.annotations.readOnlyHint, tool.name != 'docs_session')
                r = await client.call_tool('docs_catalog', {})
                self.assertFalse(r.isError)
                self.assertIsNone(r.structuredContent)  # Do not duplicate context in two formats.
                self.assertIn('NLAlib.Matrix.Norms', json.loads(r.content[0].text)['content'])
                cursor, content = None, ''
                for _ in range(100):
                    r = await client.call_tool('docs_read_declaration', {
                        'name': "NLAlib.toyBound'", 'max_chars': 1500, 'cursor': cursor})
                    self.assertFalse(r.isError)
                    self.assertLessEqual(len(r.content[0].text), 1500)
                    page = json.loads(r.content[0].text)
                    content += page['content']
                    cursor = page['next_cursor']
                    if cursor is None:
                        break
                else:
                    self.fail('MCP pagination did not terminate')
                self.assertIn(self.fixture.raw['decls'][1]['signature'], content)
                self.assertNotIn('SENTINEL_PROOF_BODY', content)
                uri = self.fixture.docs.uri('declaration', "NLAlib.toyBound'")
                resource = await client.read_resource(uri)
                self.assertIn("NLAlib.toyBound'", json.loads(resource.contents[0].text)['content'])
                templates = await client.list_resource_templates()
                self.assertEqual(len(templates.resourceTemplates), 2)
                prompts = await client.list_prompts()
                self.assertEqual(prompts.prompts[0].name, 'find_existing_lemma')
                prompt = await client.get_prompt('find_existing_lemma', {'question': 'Bound an operator norm'})
                self.assertIn('Bound an operator norm', prompt.messages[0].content.text)

    async def test_sessions_survive_server_restart(self):
        from mcp import ClientSession
        from mcp.client.stdio import stdio_client
        async with stdio_client(self.parameters()) as (read, write):
            async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=15)) as client:
                await client.initialize()
                result = await client.call_tool('docs_session', {
                    'action': 'create', 'goal': 'Reuse an existing norm result',
                    'bookmarks': ['NLAlib.toyNorm'], 'notes': 'Still a candidate, not verified.'})
                self.assertFalse(result.isError)
                session_id = json.loads(result.content[0].text)['session_id']
        async with stdio_client(self.parameters()) as (read, write):
            async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=15)) as client:
                await client.initialize()
                result = await client.call_tool('docs_session', {'action': 'get', 'session_id': session_id})
                self.assertFalse(result.isError)
                page = json.loads(result.content[0].text)
                self.assertIn('Reuse an existing norm result', page['content'])
                self.assertIn('Still a candidate', page['content'])
                result = await client.call_tool('docs_context', {'names': ['NLAlib.toyNorm']})
                self.assertIn('toyNorm (x : Nat)', json.loads(result.content[0].text)['content'])

    async def test_errors_are_explicit_without_returning_proof_or_wrong_source(self):
        from mcp import ClientSession
        from mcp.client.stdio import stdio_client
        async with stdio_client(self.parameters()) as (read, write):
            async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=15)) as client:
                await client.initialize()
                for arguments in [{'name': 'missing'}, {'name': "NLAlib.toyBound'", 'view': 'definition'},
                                  {'name': 'NLAlib.toyNorm', 'max_chars': 50}]:
                    r = await client.call_tool('docs_read_declaration', arguments)
                    self.assertTrue(r.isError)
                    self.assertNotIn('SENTINEL_PROOF_BODY', str(r))
                self.fixture.source.write_text('changed source')
                r = await client.call_tool('docs_read_declaration', {'name': 'NLAlib.toyNorm', 'view': 'definition'})
                self.assertTrue(r.isError)
                self.assertIn('Source hash differs', r.content[0].text)


if __name__ == '__main__':
    unittest.main()
