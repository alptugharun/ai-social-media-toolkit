from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "two_minute_demo.py"

spec = importlib.util.spec_from_file_location("two_minute_demo", MODULE_PATH)
demo = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(demo)


class TwoMinuteDemoTests(unittest.TestCase):
    def test_render_contains_both_proof_sections(self):
        report = demo.render()
        self.assertIn("Which content opportunity should go first?", report)
        self.assertIn("Which post actually broke the creator\'s baseline?", report)
        self.assertIn("synthetic", report.lower())

    def test_render_keeps_known_demo_decisions(self):
        report = demo.render()
        self.assertIn("Pinterest seasonal visual series", report)
        self.assertIn("reel-004", report)
        self.assertIn("3.94×", report)

    def test_render_contains_ranked_rows(self):
        report = demo.render()
        self.assertIn("| 1 |", report)
        self.assertIn("×", report)

    def test_cli_emits_utf8(self):
        result = subprocess.run([sys.executable, str(MODULE_PATH)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Alptuğ Harun", result.stdout)
        self.assertIn("3.94×", result.stdout)


if __name__ == "__main__":
    unittest.main()
