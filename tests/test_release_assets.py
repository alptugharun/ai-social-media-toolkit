from __future__ import annotations

import hashlib
import posixpath
import re
import tempfile
import unittest
import zipfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_release_assets as bra


class ReleaseAssetTests(unittest.TestCase):
    def build(self, parent: Path) -> Path:
        out = parent / "assets"
        bra.build_release_assets(ROOT, out, "v0.3.0-alpha.1")
        return out

    def test_builder_creates_measureable_release_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            out = self.build(Path(temp))
            names = {p.name for p in out.iterdir()}
            self.assertEqual(
                {
                    "agent-skills-v0.3.0-alpha.1.zip",
                    "creator-context-builder-v0.3.0-alpha.1.zip",
                    "creator-frame-studio-v0.3.0-alpha.1.zip",
                    "ai-social-media-toolkit-plugin-0.6.0.zip",
                    "SHA256SUMS.txt",
                },
                names,
            )

    def test_skills_bundle_contains_every_skill_and_context_references(self):
        with tempfile.TemporaryDirectory() as temp:
            out = self.build(Path(temp))
            with zipfile.ZipFile(out / "agent-skills-v0.3.0-alpha.1.zip") as archive:
                names = set(archive.namelist())
            skill_names = {
                p.name for p in (ROOT / "skills").iterdir()
                if p.is_dir() and (p / "SKILL.md").is_file()
            }
            self.assertEqual(19, len(skill_names))
            for name in skill_names:
                self.assertIn(f"skills/{name}/SKILL.md", names)
            self.assertIn("references/CREATOR-CONTEXT-TEMPLATE.md", names)
            self.assertIn("references/EVIDENCE-POLICY.md", names)
            for required in (
                "skills/LICENSE",
                "LICENSE.md",
                "THIRD-PARTY-NOTICES.md",
                "docs/INSTALLATION.md",
                "docs/AGENT-SKILLS-FROM-ZERO.md",
                "docs/AGENT-SKILLS-FROM-ZERO_TR.md",
                "docs/HOW-TO-USE-EVERYTHING.md",
                "examples/CREATOR-CONTEXT-EXAMPLE.md",
            ):
                self.assertIn(required, names)

    def test_context_builder_asset_is_narrow(self):
        with tempfile.TemporaryDirectory() as temp:
            out = self.build(Path(temp))
            with zipfile.ZipFile(out / "creator-context-builder-v0.3.0-alpha.1.zip") as archive:
                names = set(archive.namelist())
            self.assertIn("creator-context-builder/SKILL.md", names)
            self.assertIn("LICENSE", names)
            self.assertFalse(any(name.startswith("creator-ops/") for name in names))

    def test_frame_studio_asset_is_offline_app_without_tests(self):
        with tempfile.TemporaryDirectory() as temp:
            out = self.build(Path(temp))
            with zipfile.ZipFile(out / "creator-frame-studio-v0.3.0-alpha.1.zip") as archive:
                names = set(archive.namelist())
            for required in (
                "creator-frame-studio/index.html",
                "creator-frame-studio/app.js",
                "creator-frame-studio/styles.css",
                "creator-frame-studio/README.md",
            ):
                self.assertIn(required, names)
            self.assertIn("creator-frame-studio/LICENSE", names)
            self.assertFalse(any("/tests/" in name for name in names))

    def test_skills_bundle_readme_local_links_resolve_inside_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            out = self.build(Path(temp))
            with zipfile.ZipFile(out / "agent-skills-v0.3.0-alpha.1.zip") as archive:
                names = set(archive.namelist())
                readme = archive.read("skills/README.md").decode("utf-8")
            local_targets = re.findall(r"\]\((\.\./[^)#]+)(?:#[^)]+)?\)", readme)
            self.assertTrue(local_targets)
            for target in local_targets:
                normalized = posixpath.normpath(posixpath.join("skills", target))
                self.assertFalse(normalized.startswith("../"), target)
                self.assertIn(normalized, names, target)

    def test_zip_outputs_are_reproducible(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            first = self.build(base / "one")
            second = self.build(base / "two")
            for name in (
                "agent-skills-v0.3.0-alpha.1.zip",
                "creator-context-builder-v0.3.0-alpha.1.zip",
                "creator-frame-studio-v0.3.0-alpha.1.zip",
                "ai-social-media-toolkit-plugin-0.6.0.zip",
            ):
                a = hashlib.sha256((first / name).read_bytes()).hexdigest()
                b = hashlib.sha256((second / name).read_bytes()).hexdigest()
                self.assertEqual(a, b, name)


if __name__ == "__main__":
    unittest.main()
