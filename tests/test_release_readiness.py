import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import release_readiness as rr


class ReleaseReadinessTests(unittest.TestCase):
    def test_repository_readiness_contract_passes(self):
        checks = rr.run()
        self.assertIn("mcp-hints:complete", checks)
        self.assertIn("mcp-name-test-coverage:complete", checks)
        self.assertIn("citation-metadata:complete", checks)
        self.assertTrue(any(item.startswith("workflow-top-level-readonly:") for item in checks))

    def test_all_public_mcp_tools_have_explicit_boolean_hints(self):
        tools = rr.load_tools_literal()
        for tool in tools:
            annotations = tool["annotations"]
            self.assertEqual(rr.REQUIRED_HINTS, rr.REQUIRED_HINTS & set(annotations))
            for hint in rr.REQUIRED_HINTS:
                self.assertIs(type(annotations[hint]), bool)

    def test_cli_is_machine_checkable(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "release_readiness.py")],
            text=True,
            capture_output=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("READINESS PASS\n"))
        self.assertIn("external-reputation:not-asserted", result.stdout)


if __name__ == "__main__":
    unittest.main()
