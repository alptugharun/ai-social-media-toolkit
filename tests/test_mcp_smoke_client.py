import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SMOKE_PATH = ROOT / "packages" / "ai-workbench-mcp" / "examples" / "smoke_client.py"

spec = importlib.util.spec_from_file_location("mcp_smoke_client", SMOKE_PATH)
smoke = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(smoke)


class MCPSmokeClientTests(unittest.TestCase):
    def valid_responses(self):
        initialized = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "serverInfo": {
                    "name": "alptugharun-ai-workbench-mcp",
                    "version": "0.1.0a1",
                }
            },
        }
        tools = []
        for name in sorted(smoke.EXPECTED_TOOLS):
            tools.append(
                {
                    "name": name,
                    "annotations": {
                        "readOnlyHint": True,
                        "destructiveHint": False,
                        "idempotentHint": True,
                        "openWorldHint": False,
                    },
                }
            )
        listed = {"jsonrpc": "2.0", "id": 2, "result": {"tools": tools}}
        return initialized, listed

    def test_messages_complete_initialization_before_listing(self):
        messages = smoke.build_messages()
        self.assertEqual(messages[0]["method"], "initialize")
        self.assertEqual(messages[1]["method"], "notifications/initialized")
        self.assertEqual(messages[2]["method"], "tools/list")

    def test_valid_read_only_contract_passes(self):
        initialized, listed = self.valid_responses()
        self.assertEqual(smoke.verify(initialized, listed), sorted(smoke.EXPECTED_TOOLS))

    def test_missing_tool_fails(self):
        initialized, listed = self.valid_responses()
        listed["result"]["tools"].pop()
        with self.assertRaisesRegex(ValueError, "unexpected tools"):
            smoke.verify(initialized, listed)

    def test_unsafe_annotation_fails(self):
        initialized, listed = self.valid_responses()
        listed["result"]["tools"][0]["annotations"]["destructiveHint"] = True
        with self.assertRaisesRegex(ValueError, "destructiveHint"):
            smoke.verify(initialized, listed)

    def test_parse_requires_two_responses(self):
        with self.assertRaisesRegex(ValueError, "expected 2"):
            smoke.parse_output('{"jsonrpc":"2.0"}\n')


if __name__ == "__main__":
    unittest.main()
