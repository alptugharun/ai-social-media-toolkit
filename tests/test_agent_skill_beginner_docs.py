from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EN = ROOT / "docs" / "AGENT-SKILLS-FROM-ZERO.md"
TR = ROOT / "docs" / "AGENT-SKILLS-FROM-ZERO_TR.md"


class AgentSkillBeginnerDocsTests(unittest.TestCase):
    def setUp(self):
        self.skill_names = sorted(
            path.name for path in SKILLS.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        )
        self.en = EN.read_text(encoding="utf-8")
        self.tr = TR.read_text(encoding="utf-8")

    def test_every_installable_skill_is_documented_in_both_languages(self):
        self.assertEqual(19, len(self.skill_names))
        for name in self.skill_names:
            self.assertIn(f"## {name}", self.en, name)
            self.assertIn(f"## {name}", self.tr, name)

    def test_guides_explain_use_result_and_limit(self):
        en_lower = self.en.lower()
        self.assertIn("expected result", en_lower)
        self.assertIn("limit", en_lower)
        self.assertIn("first request", en_lower)

        self.assertIn("**Beklenen sonuç:**", self.tr)
        self.assertIn("**Sınır:**", self.tr)
        self.assertIn("**İlk talep:**", self.tr)

    def test_quick_map_contains_every_skill(self):
        en_tail = self.en.split("# Quick decision map", 1)[1]
        tr_tail = self.tr.split("# Hızlı seçim", 1)[1]
        for name in self.skill_names:
            self.assertIn(name, en_tail)
            self.assertIn(name, tr_tail)


if __name__ == "__main__":
    unittest.main()
