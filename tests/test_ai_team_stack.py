from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "ai_team_stack.py"
CATALOG = ROOT / "resources" / "ai-team-stack.json"

spec = importlib.util.spec_from_file_location("ai_team_stack", TOOL)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class AITeamStackTests(unittest.TestCase):
    def test_catalog_validates(self):
        data = module.load_catalog()
        self.assertGreaterEqual(len(data["items"]), 12)
        self.assertEqual(set(data["lanes"]), {"coding_core", "creator_core"})

    def test_each_lane_has_five_unique_items(self):
        data = module.load_catalog()
        for lane in data["lanes"].values():
            self.assertEqual(len(lane["items"]), 5)
            self.assertEqual(len(set(lane["items"])), 5)

    def test_no_stale_star_counts_are_baked_into_catalog(self):
        raw = CATALOG.read_text(encoding="utf-8").lower()
        self.assertNotIn('"stars"', raw)
        self.assertNotIn("stargazers_count", raw)

    def test_runtime_evidence_is_explicit_for_maintainer_mcp(self):
        data = module.load_catalog()
        items = {item["id"]: item for item in data["items"]}
        self.assertEqual(items["ai-workbench-mcp"]["evidence"], "maintainer_runtime_verified")
        self.assertIn("read-only", items["ai-workbench-mcp"]["layer"].lower())

    def test_cli_check_passes(self):
        run = subprocess.run(
            [sys.executable, str(TOOL), "check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=20,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("PASS:", run.stdout)

    def test_build_ui_creates_self_contained_page(self):
        data = module.load_catalog()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "stack.html"
            module.build_ui(data, output)
            page = output.read_text(encoding="utf-8")
            self.assertIn("Verified AI Team Stack", page)
            self.assertIn("github-mcp", page)
            self.assertNotIn("__CATALOG__", page)

    def test_cli_recommend_returns_five(self):
        run = subprocess.run(
            [sys.executable, str(TOOL), "recommend", "--lane", "coding_core", "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=20,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        payload = json.loads(run.stdout)
        self.assertEqual(len(payload["items"]), 5)


if __name__ == "__main__":
    unittest.main()
