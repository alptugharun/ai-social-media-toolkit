import io
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import ai_workbench
import prompt_mcp_server as mcp


def req(method, params=None, rpc_id=1):
    return dict(jsonrpc='2.0', id=rpc_id, method=method, params=params or {})


class MCPTests(unittest.TestCase):
    def setUp(self):
        self.catalog = ai_workbench.load_catalog()
        self.server = mcp.CatalogServer(self.catalog)
    def initialize(self):
        answer = self.server.handle(req('initialize', {'protocolVersion': '2025-06-18'}))
        self.server.handle({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        return answer
    def test_initialize_negotiates_version(self):
        answer = self.initialize()
        self.assertEqual(answer['result']['protocolVersion'], '2025-06-18')
    def test_unknown_version_offers_supported_version(self):
        answer = self.server.handle(req('initialize', {'protocolVersion': '2099-01-01'}))
        self.assertIn(answer['result']['protocolVersion'], mcp.VERSIONS)
    def test_init_requires_version(self):
        self.assertIn('error', self.server.handle(req('initialize')))
    def test_tools_require_completed_handshake(self):
        self.assertIn('error', self.server.handle(req('tools/list')))
    def test_list_returns_three_read_only_tools(self):
        self.initialize()
        tools = self.server.handle(req('tools/list'))['result']['tools']
        self.assertEqual(len(tools), 3)
        self.assertTrue(all(t['annotations']['readOnlyHint'] for t in tools))
        for tool in tools:
            annotations = tool['annotations']
            self.assertTrue(annotations.get('title'), tool['name'])
            self.assertEqual(set(annotations), {'title', 'readOnlyHint', 'destructiveHint', 'idempotentHint', 'openWorldHint'})
            self.assertTrue(annotations['readOnlyHint'])
            self.assertFalse(annotations['destructiveHint'])
            self.assertTrue(annotations['idempotentHint'])
            self.assertFalse(annotations['openWorldHint'])
    def test_catalog_tool(self):
        self.initialize()
        result = self.server.handle(req('tools/call', {'name': 'list_prompts', 'arguments': {}}))['result']
        self.assertFalse(result['isError'])
        self.assertEqual(len(json.loads(result['content'][0]['text'])['prompts']), 12)
    def test_render_tool(self):
        self.initialize()
        entry = self.catalog['prompts'][0]
        result = self.server.handle(req('tools/call', {'name': 'render_prompt', 'arguments': {'id': entry['id'], 'variables': entry['example']}}))['result']
        self.assertFalse(result['isError'])
        self.assertIn('S1', result['content'][0]['text'])
    def test_tool_never_accepts_file_path(self):
        self.initialize()
        result = self.server.handle(req('tools/call', {'name': 'get_assistant', 'arguments': {'id': '../../secrets'}}))['result']
        self.assertTrue(result['isError'])
    def test_unknown_tool_returns_error_content(self):
        self.initialize()
        result = self.server.handle(req('tools/call', {'name': 'run_shell', 'arguments': {'command': 'whoami'}}))['result']
        self.assertTrue(result['isError'])
    def test_nonobject_arguments_rejected(self):
        self.initialize()
        result = self.server.handle(req('tools/call', {'name': 'render_prompt', 'arguments': []}))['result']
        self.assertTrue(result['isError'])
    def test_notification_has_no_response(self):
        self.assertIsNone(self.server.handle({'jsonrpc': '2.0', 'method': 'notifications/cancelled'}))
    def test_invalid_messages_return_protocol_error(self):
        for message in ([], None, {'jsonrpc':'1.0'}, {'jsonrpc':'2.0','id':True,'method':'ping'}):
            self.assertIn('error', self.server.handle(message))
    def test_unknown_method_rejected(self):
        self.initialize()
        self.assertEqual(self.server.handle(req('delete_files'))['error']['code'], -32601)
    def test_stdio_parse_error(self):
        out = io.StringIO()
        self.assertEqual(mcp.serve(io.StringIO('broken\n'), out, self.catalog), 0)
        self.assertEqual(json.loads(out.getvalue())['error']['code'], -32700)
    def test_line_size_limit_closes_transport(self):
        out = io.StringIO()
        code = mcp.serve(io.StringIO('x' * (mcp.LINE_LIMIT + 1)), out, self.catalog)
        self.assertEqual(code, 2)
    def test_real_stdio_subprocess(self):
        messages = [req('initialize', {'protocolVersion':'2025-06-18'}),
                    {'jsonrpc':'2.0','method':'notifications/initialized'}, req('tools/list', rpc_id=2)]
        result = subprocess.run([sys.executable, str(ROOT / 'tools/prompt_mcp_server.py')], input='\n'.join(json.dumps(m) for m in messages)+'\n', text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(len(json.loads(lines[1])['result']['tools']), 3)


if __name__ == '__main__':
    unittest.main()
