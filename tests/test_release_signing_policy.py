from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "sign-release-assets.yml"


class ReleaseSigningPolicyTests(unittest.TestCase):
    def setUp(self):
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_signing_workflow_uses_oidc_and_narrow_write_permission(self):
        self.assertIn("id-token: write", self.text)
        self.assertIn("contents: write", self.text)
        self.assertIn("permissions:\n  contents: read", self.text)

    def test_sigstore_action_is_immutable_and_release_assets_are_preserved(self):
        self.assertIn(
            "sigstore/gh-action-sigstore-python@790bc6befb9d733738f18d8f895854b453640ec9",
            self.text,
        )
        self.assertIn("--pattern '*.zip'", self.text)
        self.assertIn("--pattern 'SHA256SUMS.txt'", self.text)
        self.assertIn("*.sigstore.json", self.text)
        self.assertIn("--clobber", self.text)

    def test_workflow_supports_current_and_future_releases(self):
        self.assertIn("release:\n    types: [published]", self.text)
        self.assertIn("workflow_dispatch:", self.text)
        self.assertIn("github.event.release.tag_name", self.text)


if __name__ == "__main__":
    unittest.main()
