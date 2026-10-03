import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
CONTRACTS = ROOT / "evals" / "skill-contracts.json"


class SkillEvaluationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(CONTRACTS.read_text(encoding="utf-8"))
        cls.cases = cls.data["cases"]
        cls.skill_names = sorted(
            path.parent.name for path in SKILLS_ROOT.glob("*/SKILL.md")
        )

    def test_contract_file_is_explicitly_not_runtime_evidence(self):
        self.assertEqual(self.data["schema_version"], 1)
        self.assertIn("not runtime model evaluation", self.data["status"].lower())

    def test_every_skill_has_exactly_one_contract(self):
        contract_skills = [case["skill"] for case in self.cases]
        self.assertEqual(sorted(contract_skills), self.skill_names)
        self.assertEqual(len(contract_skills), len(set(contract_skills)))

    def test_case_ids_are_unique_and_human_readable(self):
        ids = [case["id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case_id in ids:
            self.assertRegex(case_id, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

    def test_every_contract_has_actionable_acceptance_and_rejection_criteria(self):
        required = {"id", "skill", "prompt", "must_include", "must_not", "notes"}
        for case in self.cases:
            self.assertEqual(set(case), required, case["id"])
            self.assertGreaterEqual(len(case["prompt"].strip()), 30, case["id"])
            self.assertGreaterEqual(len(case["must_include"]), 3, case["id"])
            self.assertGreaterEqual(len(case["must_not"]), 2, case["id"])
            self.assertTrue(all(item.strip() for item in case["must_include"]))
            self.assertTrue(all(item.strip() for item in case["must_not"]))
            self.assertGreaterEqual(len(case["notes"].strip()), 20, case["id"])

    def test_contracts_do_not_encode_fake_success(self):
        forbidden = ("passed in production", "100% compatible", "guaranteed viral", "guaranteed revenue")
        claimed_text = [self.data["status"]]
        for case in self.cases:
            claimed_text.extend(
                [
                    case["prompt"],
                    case["notes"],
                    *case["must_include"],
                ]
            )
        serialized = "\n".join(claimed_text).lower()
        for phrase in forbidden:
            self.assertNotIn(phrase, serialized)


if __name__ == "__main__":
    unittest.main()
