"""Guard against independently updated, incompatible CodeQL Action steps.

Regression: on 2026-10-13 the separate CodeQL init/analyze Dependabot
pull requests each failed with a mixed 4.38.2/4.38.3 configuration.
This tests source pins, not a live CodeQL analysis or Dependabot service.
"""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
DEPENDABOT = ROOT / ".github" / "dependabot.yml"

ACTION_USE = re.compile(
    r"^\s*uses:\s*github/codeql-action/([^@\s#]+)@([^\s#]+)",
    re.MULTILINE,
)


class CodeQLActionPinConsistencyTests(unittest.TestCase):
    def test_every_codeql_action_uses_one_full_commit_pin(self):
        actions = []
        for path in sorted((*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml"))):
            for kind, revision in ACTION_USE.findall(path.read_text(encoding="utf-8")):
                with self.subTest(workflow=path.name, action=kind):
                    self.assertRegex(revision, r"^[0-9a-f]{40}$")
                actions.append((path.name, kind, revision))
        self.assertTrue({"init", "analyze", "upload-sarif"}.issubset(
            {kind for _, kind, _ in actions}
        ), actions)
        self.assertEqual(1, len({sha for _, _, sha in actions}), actions)

    def test_dependabot_groups_codeql_action_steps(self):
        text = DEPENDABOT.read_text(encoding="utf-8")
        self.assertRegex(
            text,
            r'(?m)^    groups:\n      codeql-actions:\n'
            r'        patterns:\n          - "github/codeql-action/\*"\s*$',
        )


if __name__ == "__main__":
    unittest.main()
