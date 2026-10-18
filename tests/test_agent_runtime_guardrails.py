from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".github" / "hooks" / "repository-safety.json"
AGENT = ROOT / ".github" / "agents" / "ai-runtime-auditor.agent.md"
GUARD = ROOT / "tools" / "copilot_shell_guard.py"
SKILL = ROOT / "skills" / "agent-skill-safety-auditor" / "SKILL.md"


class AgentRuntimeGuardrailTests(unittest.TestCase):
    def test_hook_manifest_is_narrow_and_cross_platform(self) -> None:
        data = json.loads(HOOK.read_text(encoding="utf-8"))
        self.assertEqual(data["version"], 1)
        entries = data["hooks"]["preToolUse"]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["type"], "command")
        self.assertEqual(entry["matcher"], "bash|powershell")
        self.assertIn("copilot_shell_guard.py", entry["bash"])
        self.assertIn("copilot_shell_guard.py", entry["powershell"])
        self.assertLessEqual(entry["timeoutSec"], 5)

    def test_guard_exists_and_has_bounded_policy_surface(self) -> None:
        text = GUARD.read_text(encoding="utf-8")
        self.assertIn("RULES:", text)
        self.assertIn("permissionDecision", text)
        self.assertIn("permissionDecisionReason", text)
        self.assertNotIn("requests.", text)
        self.assertNotIn("urllib.", text)

    def test_runtime_auditor_is_read_only_by_contract(self) -> None:
        text = AGENT.read_text(encoding="utf-8")
        self.assertIn("name: AI Runtime Auditor", text)
        self.assertIn("  - read", text)
        self.assertIn("  - execute", text)
        self.assertNotIn("  - edit", text)
        self.assertIn("Do not edit files", text)

    def test_safety_skill_covers_modern_runtime_surfaces(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "custom-agent profiles",
            "Hooks are deterministic code execution surfaces",
            "Agent plugins",
            "Sandbox and long-running agents",
            "Runtime Evidence Ladder",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
