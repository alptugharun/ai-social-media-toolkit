from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "learning" / "AI-BUILDER-LAB.md"


class AIBuilderLabDocsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = DOC.read_text(encoding="utf-8")

    def test_required_learning_sections_exist(self):
        for heading in (
            "## Lab 1 — Prompt engineering",
            "## Lab 2 — Assistant design",
            "## Lab 3 — Agent Skill",
            "## Lab 4 — MCP",
            "## Lab 5 — Plugin design",
            "## Lab 6 — Bot/API development",
            "## Lab 7 — Automation",
            "## Failure log",
            "## Final release gate",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, self.text)

    def test_documented_local_commands_match_existing_entry_points(self):
        for command in (
            "python tools/first_run_check.py",
            "python tools/ai_workbench.py render evidence-brief --example",
            "python tools/ai_workbench.py export evidence-desk --target chatgpt",
            "python -m unittest discover -s packages/ai-workbench-mcp/tests -v",
            'python -m unittest discover -s tests -p "test_mcp_distribution_package.py" -v',
            'python -m unittest discover -s tests -p "test_mcp_smoke_client.py" -v',
            "python tools/release_readiness.py",
        ):
            with self.subTest(command=command):
                self.assertIn(command, self.text)

    def test_referenced_repository_paths_exist(self):
        for relative in (
            "tools/first_run_check.py",
            "tools/ai_workbench.py",
            "tools/install_skills.py",
            "learning/AI-BUILDER-PATH.md",
            "skills/plugin-mcp-architect/SKILL.md",
            "prompts/assistants/plugin-mcp-architect.md",
            "prompts/automation/approval-gated-workflow.md",
            "automation-recipes/README.md",
            "packages/ai-workbench-mcp/tests/test_public_tools.py",
            "tests/test_mcp_distribution_package.py",
            "tests/test_mcp_smoke_client.py",
        ):
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).exists(), relative)

    def test_evidence_boundaries_are_explicit(self):
        for statement in (
            "A registry listing proves distribution metadata. It does not prove universal host compatibility.",
            "These are instruction blueprints. They do not create, publish or configure hosted assistants by themselves.",
            "This repository teaches the first five patterns and how to test them. It does not claim to train a foundation model.",
        ):
            with self.subTest(statement=statement):
                self.assertIn(statement, self.text)


if __name__ == "__main__":
    unittest.main()
