from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "plugin.json"
SKILLS = ROOT / "skills"
CASES = ROOT / "evals" / "plugin-submission-cases.json"
BUILDER = ROOT / "tools" / "build_plugin_bundle.py"

EXPECTED_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
EXPECTED_SKILL_COUNT = 18
EXTRA_RESOURCES = {
    "learning/AI-BUILDER-PATH.md",
    "integrations/README.md",
    "prompts/assistants/plugin-mcp-architect.md",
}


def frontmatter_field(text: str, field: str) -> str | None:
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None
    normalized = text.replace("\r\n", "\n")
    _, frontmatter, _ = normalized.split("---", 2)
    match = re.search(rf"(?m)^{re.escape(field)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


class PluginPackageTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.skill_dirs = sorted(
            path for path in SKILLS.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        )

    def test_portable_manifest_identity_is_explicit(self):
        self.assertEqual(EXPECTED_SCHEMA, self.manifest["$schema"])
        self.assertRegex(self.manifest["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertRegex(self.manifest["version"], r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
        self.assertGreaterEqual(len(self.manifest["description"].strip()), 40)
        self.assertEqual("MIT", self.manifest["license"])

    def test_current_plugin_is_intentionally_skills_only(self):
        self.assertFalse((ROOT / "mcp.json").exists())
        self.assertTrue((ROOT / "packages" / "ai-workbench-mcp").is_dir())
        self.assertIn("skills-only plugin", (ROOT / "PLUGIN-GUIDE.md").read_text(encoding="utf-8"))

    def test_all_18_skills_are_discoverable_and_self_identifying(self):
        self.assertEqual(EXPECTED_SKILL_COUNT, len(self.skill_dirs))
        for skill_dir in self.skill_dirs:
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertEqual(skill_dir.name, frontmatter_field(text, "name"), skill_dir.name)
            description = frontmatter_field(text, "description")
            self.assertIsNotNone(description, skill_dir.name)
            self.assertGreaterEqual(len(description.strip()), 30, skill_dir.name)

    def test_submission_preparation_has_five_positive_and_three_negative_cases(self):
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertIn("not runtime", payload["status"].lower())
        self.assertEqual(5, len(payload["positive_cases"]))
        self.assertEqual(3, len(payload["negative_cases"]))
        ids = [
            case["id"]
            for group in ("positive_cases", "negative_cases")
            for case in payload[group]
        ]
        self.assertEqual(len(ids), len(set(ids)))
        for group in ("positive_cases", "negative_cases"):
            for case in payload[group]:
                self.assertGreaterEqual(len(case["prompt"].strip()), 30)
                self.assertGreaterEqual(len(case["expected"].strip()), 30)

    def test_builder_creates_narrow_reproducible_plugin_zip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            out = Path(temp_dir) / "plugin.zip"
            result = subprocess.run(
                [sys.executable, str(BUILDER), "--output", str(out)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("PLUGIN BUNDLE PASS", result.stdout)
            self.assertTrue(out.is_file())

            with zipfile.ZipFile(out) as archive:
                names = set(archive.namelist())
                bundled_manifest = json.loads(archive.read("plugin.json"))

            self.assertEqual(self.manifest["version"], bundled_manifest["version"])
            for skill_dir in self.skill_dirs:
                self.assertIn(f"skills/{skill_dir.name}/SKILL.md", names)
            self.assertTrue(EXTRA_RESOURCES.issubset(names))
            self.assertFalse(any(name.startswith(".git") for name in names))
            self.assertFalse(any(name.startswith(".github/") for name in names))
            self.assertFalse(any(name.startswith("tests/") for name in names))
            self.assertFalse(any("__pycache__" in name for name in names))
            self.assertNotIn("mcp.json", names)

    def test_plugin_architect_external_resources_are_in_bundle_allowlist(self):
        text = (SKILLS / "plugin-mcp-architect" / "SKILL.md").read_text(encoding="utf-8")
        linked = set(
            match.replace("\\", "/")
            for match in re.findall(r"\.\./\.\./([^\s)]+)", text)
        )
        self.assertEqual(EXTRA_RESOURCES, linked)


if __name__ == "__main__":
    unittest.main()
