import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
PACKAGE_ROOT = ROOT / "packages" / "ai-workbench-mcp"
PACKAGE_SRC = PACKAGE_ROOT / "src"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(PACKAGE_SRC))

import ai_workbench as root_workbench
from ai_workbench_mcp import __version__
from ai_workbench_mcp import server as packaged


def req(method, params=None, rpc_id=1):
    return {"jsonrpc": "2.0", "id": rpc_id, "method": method, "params": params or {}}


class MCPDistributionPackageTests(unittest.TestCase):
    def initialized_server(self):
        server = packaged.CatalogServer(packaged.load_catalog())
        server.handle(req("initialize", {"protocolVersion": "2025-06-18"}))
        server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return server

    def test_list_prompts_tool_by_name(self):
        server = self.initialized_server()
        result = server.handle(
            req("tools/call", {"name": "list_prompts", "arguments": {}})
        )["result"]
        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertTrue(payload["prompts"])
        self.assertTrue(payload["assistants"])

    def test_render_prompt_tool_by_name(self):
        server = self.initialized_server()
        entry = packaged.load_catalog()["prompts"][0]
        result = server.handle(
            req(
                "tools/call",
                {
                    "name": "render_prompt",
                    "arguments": {"id": entry["id"], "variables": entry["example"]},
                },
            )
        )["result"]
        self.assertFalse(result["isError"])
        self.assertTrue(result["content"][0]["text"].strip())

    def test_get_assistant_tool_by_name(self):
        server = self.initialized_server()
        assistant_id = packaged.load_catalog()["assistants"][0]["id"]
        result = server.handle(
            req(
                "tools/call",
                {
                    "name": "get_assistant",
                    "arguments": {"id": assistant_id, "target": "chatgpt"},
                },
            )
        )["result"]
        self.assertFalse(result["isError"])
        self.assertIn("## Instructions", result["content"][0]["text"])

    def test_package_metadata_is_explicit_and_prerelease(self):
        metadata = tomllib.loads((PACKAGE_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        project = metadata["project"]
        self.assertEqual(project["name"], "alptugharun-ai-workbench-mcp")
        self.assertEqual(project["version"], __version__)
        self.assertEqual(project["requires-python"], ">=3.10")
        self.assertEqual(
            project["scripts"]["alptugharun-ai-workbench-mcp"],
            "ai_workbench_mcp.server:main",
        )

    def test_build_backend_uses_patched_setuptools(self):
        metadata = tomllib.loads((PACKAGE_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        build_requires = metadata["build-system"]["requires"]
        setuptools_pins = [item for item in build_requires if item.startswith("setuptools==")]
        self.assertEqual(1, len(setuptools_pins), build_requires)
        version = tuple(int(part) for part in setuptools_pins[0].split("==", 1)[1].split("."))
        self.assertGreaterEqual(
            version,
            (83, 0, 0),
            "setuptools <83.0.0 is affected by GHSA-h35f-9h28-mq5c / CVE-2026-59890",
        )

    def test_registry_ownership_marker_matches_planned_server_name(self):
        readme = (PACKAGE_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "<!-- mcp-name: io.github.alptugharun/ai-workbench-mcp -->",
            readme,
        )
        self.assertFalse((PACKAGE_ROOT / "server.json").exists())

    def test_bundled_catalog_exactly_matches_workbench_source(self):
        root_catalog = root_workbench.load_catalog()
        package_catalog = packaged.load_catalog()
        self.assertEqual(root_catalog, package_catalog)

    def test_every_packaged_tool_has_complete_explicit_hints(self):
        required = {"readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint"}
        self.assertEqual(3, len(packaged.TOOLS))
        for tool in packaged.TOOLS:
            annotations = tool["annotations"]
            self.assertTrue(required <= set(annotations), tool["name"])
            self.assertTrue(annotations["readOnlyHint"], tool["name"])
            self.assertFalse(annotations["destructiveHint"], tool["name"])
            self.assertTrue(annotations["idempotentHint"], tool["name"])
            self.assertFalse(annotations["openWorldHint"], tool["name"])
            for hint in required:
                self.assertIs(type(annotations[hint]), bool)

    def test_packaged_server_imports_no_network_or_process_modules(self):
        tree = ast.parse((PACKAGE_SRC / "ai_workbench_mcp" / "server.py").read_text(encoding="utf-8"))
        allowed = {"json", "re", "sys", "importlib", "typing"}
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertTrue(imported <= allowed | {"__future__"}, imported)

    def test_all_prompt_examples_render(self):
        catalog = packaged.load_catalog()
        for entry in catalog["prompts"]:
            rendered = packaged.render_prompt(entry, entry["example"])
            self.assertIsInstance(rendered, str)
            self.assertTrue(rendered.strip())
            self.assertNotRegex(rendered, r"\{\{[a-z_]+\}\}")

    def test_assistant_targets_are_explicit(self):
        server = packaged.CatalogServer(packaged.load_catalog())
        server.handle(req("initialize", {"protocolVersion": "2025-06-18"}))
        server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"})
        assistant_id = packaged.load_catalog()["assistants"][0]["id"]
        for target in ("chatgpt", "claude", "gemini", "grok", "skill"):
            result = server.handle(
                req(
                    "tools/call",
                    {"name": "get_assistant", "arguments": {"id": assistant_id, "target": target}},
                )
            )["result"]
            self.assertFalse(result["isError"], target)
            self.assertTrue(result["content"][0]["text"].strip())
        bad = server.handle(
            req(
                "tools/call",
                {"name": "get_assistant", "arguments": {"id": assistant_id, "target": "unknown"}},
            )
        )["result"]
        self.assertTrue(bad["isError"])

    def test_real_stdio_handshake_from_source_package(self):
        messages = [
            req("initialize", {"protocolVersion": "2025-06-18"}),
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            req("tools/list", rpc_id=2),
        ]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PACKAGE_SRC) + os.pathsep + env.get("PYTHONPATH", "")
        result = subprocess.run(
            [sys.executable, "-m", "ai_workbench_mcp.server"],
            input="\n".join(json.dumps(message) for message in messages) + "\n",
            text=True,
            capture_output=True,
            timeout=10,
            env=env,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        lines = result.stdout.splitlines()
        self.assertEqual(2, len(lines))
        initialize = json.loads(lines[0])
        tools = json.loads(lines[1])
        self.assertEqual(__version__, initialize["result"]["serverInfo"]["version"])
        self.assertEqual(3, len(tools["result"]["tools"]))


if __name__ == "__main__":
    unittest.main()
