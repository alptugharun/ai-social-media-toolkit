from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "tools" / "install_skills.py"


class InstallerTests(unittest.TestCase):
    def create_source_repo(self, root: Path) -> None:
        for name in ("alpha-skill", "beta-skill"):
            skill_dir = root / "skills" / name
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: test skill\nlicense: MIT\n---\n",
                encoding="utf-8",
            )

    def run_installer(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INSTALLER), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_project_target_installs_selected_skill(self) -> None:
        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as project_tmp:
            source = Path(source_tmp)
            project = Path(project_tmp)
            self.create_source_repo(source)

            result = self.run_installer(
                "--repo-root", str(source),
                "--target", "gemini",
                "--scope", "project",
                "--project-root", str(project),
                "--skill", "alpha-skill",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(
                (project / ".gemini" / "skills" / "alpha-skill" / "SKILL.md").is_file()
            )
            self.assertFalse(
                (project / ".gemini" / "skills" / "beta-skill").exists()
            )

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as dest_tmp:
            source = Path(source_tmp)
            destination = Path(dest_tmp) / "skills-target"
            self.create_source_repo(source)

            result = self.run_installer(
                "--repo-root", str(source),
                "--destination", str(destination),
                "--dry-run",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(destination.exists())

    def test_existing_skill_requires_force(self) -> None:
        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as dest_tmp:
            source = Path(source_tmp)
            destination = Path(dest_tmp) / "skills-target"
            self.create_source_repo(source)

            first = self.run_installer(
                "--repo-root", str(source),
                "--destination", str(destination),
                "--skill", "alpha-skill",
            )
            second = self.run_installer(
                "--repo-root", str(source),
                "--destination", str(destination),
                "--skill", "alpha-skill",
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 3)
            self.assertIn("already exists", second.stderr)

    def test_force_replaces_existing_skill(self) -> None:
        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as dest_tmp:
            source = Path(source_tmp)
            destination = Path(dest_tmp) / "skills-target"
            self.create_source_repo(source)

            target = destination / "alpha-skill"
            target.mkdir(parents=True)
            (target / "old.txt").write_text("old", encoding="utf-8")

            result = self.run_installer(
                "--repo-root", str(source),
                "--destination", str(destination),
                "--skill", "alpha-skill",
                "--force",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "SKILL.md").is_file())
            self.assertFalse((target / "old.txt").exists())


if __name__ == "__main__":
    unittest.main()
