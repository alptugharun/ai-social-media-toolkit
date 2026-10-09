from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "creator-frame-studio-pages.yml"


class CreatorFrameStudioPagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_deploys_only_on_main_push_or_manual_dispatch(self):
        self.assertIn("branches:\n      - main", self.source)
        self.assertIn("workflow_dispatch:", self.source)
        self.assertNotIn("pull_request:", self.source)

    def test_permissions_are_narrow(self):
        self.assertIn("contents: read", self.source)
        self.assertIn("pages: write", self.source)
        self.assertIn("id-token: write", self.source)
        self.assertNotIn("contents: write", self.source)
        self.assertNotIn("issues: write", self.source)

    def test_only_creator_frame_studio_is_uploaded(self):
        self.assertIn("path: tools/creator-frame-studio", self.source)
        self.assertNotIn("path: .\n", self.source)

    def test_third_party_actions_are_immutable_pins(self):
        expected = (
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            "actions/configure-pages@45bfe0192ca1faeb007ade9deae92b16b8254a0d",
            "actions/upload-pages-artifact@fc324d3547104276b827a68afc52ff2a11cc49c9",
            "actions/deploy-pages@368f82528645a54fb793d4d04e342629a3f51346",
        )
        for ref in expected:
            with self.subTest(ref=ref):
                self.assertIn(ref, self.source)


if __name__ == "__main__":
    unittest.main()
