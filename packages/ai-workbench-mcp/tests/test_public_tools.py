from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SRC = PACKAGE_ROOT / "src"
sys.path.insert(0, str(SRC))

from ai_workbench_mcp import server


def req(method: str, params=None, rpc_id: int = 1) -> dict:
    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "method": method,
        "params": params or {},
    }


class PublicMCPToolNameTests(unittest.TestCase):
    def initialized_server(self) -> server.CatalogServer:
        instance = server.CatalogServer(server.load_catalog())
        instance.handle(req("initialize", {"protocolVersion": "2025-06-18"}))
        instance.handle({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return instance

    def test_list_prompts(self):
        result = self.initialized_server().handle(
            req("tools/call", {"name": "list_prompts", "arguments": {}})
        )["result"]
        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertTrue(payload["prompts"])
        self.assertTrue(payload["assistants"])

    def test_render_prompt(self):
        catalog = server.load_catalog()
        prompt = catalog["prompts"][0]
        result = self.initialized_server().handle(
            req(
                "tools/call",
                {
                    "name": "render_prompt",
                    "arguments": {
                        "id": prompt["id"],
                        "variables": prompt["example"],
                    },
                },
            )
        )["result"]
        self.assertFalse(result["isError"])
        self.assertTrue(result["content"][0]["text"].strip())

    def test_get_assistant(self):
        assistant_id = server.load_catalog()["assistants"][0]["id"]
        result = self.initialized_server().handle(
            req(
                "tools/call",
                {
                    "name": "get_assistant",
                    "arguments": {
                        "id": assistant_id,
                        "target": "chatgpt",
                    },
                },
            )
        )["result"]
        self.assertFalse(result["isError"])
        self.assertIn("## Instructions", result["content"][0]["text"])


if __name__ == "__main__":
    unittest.main()
