"""Exercise the exact read-only release metadata program, not a remote service."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/publish-v0.3.0-alpha.1.yml"
ASSETS = (
    "agent-skills-v0.3.0-alpha.1.zip",
    "creator-context-builder-v0.3.0-alpha.1.zip",
    "creator-frame-studio-v0.3.0-alpha.1.zip",
    "ai-social-media-toolkit-plugin-0.6.0.zip",
    "SHA256SUMS.txt",
)


class FrozenReleaseDeliveryTests(unittest.TestCase):
    def metadata(self):
        return {
            "tag_name": "v0.3.0-alpha.1", "draft": False,
            "assets": [{"name": name, "state": "uploaded", "size": 123} for name in ASSETS],
        }

    def run_gate(self, data):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        source = workflow.split("# BEGIN RELEASE METADATA CHECK\n", 1)[1].split("# END RELEASE METADATA CHECK", 1)[0]
        source = textwrap.dedent(source)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "release-metadata.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            original = path.read_bytes()
            result = subprocess.run([sys.executable, "-c", source], cwd=folder, capture_output=True, text=True, timeout=10)
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual([p.name for p in Path(folder).iterdir()], ["release-metadata.json"])
            return result

    def test_published_release_metadata(self):
        result = self.run_gate(self.metadata())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PUBLISHED RELEASE METADATA PASS", result.stdout)
        self.assertIn("do not verify checksums", result.stdout)

    def test_wrong_tag_fails(self):
        data = self.metadata(); data["tag_name"] = "v9.0.0"
        self.assertNotEqual(self.run_gate(data).returncode, 0)

    def test_draft_fails(self):
        data = self.metadata(); data["draft"] = True
        self.assertNotEqual(self.run_gate(data).returncode, 0)

    def test_missing_asset_fails(self):
        data = self.metadata(); data["assets"].pop()
        self.assertNotEqual(self.run_gate(data).returncode, 0)

    def test_empty_or_invalid_asset_size_fails(self):
        for invalid in (0, -1, "123", True, None):
            with self.subTest(size=invalid):
                data = self.metadata(); data["assets"][0]["size"] = invalid
                self.assertNotEqual(self.run_gate(data).returncode, 0)

    def test_unfinished_upload_fails(self):
        data = self.metadata(); data["assets"][0]["state"] = "new"
        self.assertNotEqual(self.run_gate(data).returncode, 0)

    def test_duplicate_asset_fails(self):
        data = self.metadata(); data["assets"].append(copy.deepcopy(data["assets"][0]))
        self.assertNotEqual(self.run_gate(data).returncode, 0)

    def test_optional_signatures_do_not_break_metadata_check(self):
        data = self.metadata(); data["assets"].append({"name": "SHA256SUMS.txt.sigstore.json", "state": "uploaded", "size": 456})
        self.assertEqual(self.run_gate(data).returncode, 0)

    def test_historical_workflow_cannot_publish(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("contents: read", text)
        for forbidden in ("contents: write", "id-token: write", "gh release create", "gh release upload", "--clobber", "git push"):
            self.assertNotIn(forbidden, text)

    def test_bilingual_helper_routes_from_entrypoints(self):
        for entry in (ROOT / "START-HERE.md", ROOT / "tools/README.md"):
            text = entry.read_text(encoding="utf-8")
            self.assertIn("brand-voice-humanizer/README.md", text)
            self.assertIn("brand-voice-humanizer/README_TR.md", text)
            self.assertIn("v0.3.0-alpha.1", text)
        for path in ("skills/brand-voice-humanizer/README.md", "skills/brand-voice-humanizer/README_TR.md"):
            self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
