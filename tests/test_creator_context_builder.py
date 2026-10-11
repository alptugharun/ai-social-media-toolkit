from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CreatorContextBuilderContractTests(unittest.TestCase):
    def test_skill_defines_provenance_and_privacy_boundaries(self):
        text = (ROOT / "skills" / "creator-context-builder" / "SKILL.md").read_text(encoding="utf-8")
        for token in ("VERIFIED", "PREFERENCE", "OBSERVED", "HYPOTHESIS"):
            self.assertIn(token, text)
        self.assertIn("passwords", text)
        self.assertIn("API keys", text)
        self.assertIn("Stale / Recheck List", text)

    def test_creator_ops_routes_missing_personal_context_to_builder(self):
        text = (ROOT / "skills" / "creator-ops" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("creator-context-builder", text)
        self.assertIn("Do not block source-only research", text)

    def test_shared_template_exposes_evidence_labels(self):
        text = (ROOT / "references" / "CREATOR-CONTEXT-TEMPLATE.md").read_text(encoding="utf-8")
        self.assertIn("Evidence Labels", text)
        self.assertIn("Stale / recheck list", text)
        self.assertIn("Never store passwords", text)


if __name__ == "__main__":
    unittest.main()
