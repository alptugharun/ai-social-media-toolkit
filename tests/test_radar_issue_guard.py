import unittest

from tools.radar_issue_guard import EXPECTED_TITLE, validate_issue


def valid_issue():
    return {
        "number": 7,
        "title": EXPECTED_TITLE,
        "state": "OPEN",
        "author": {"login": "github-actions[bot]"},
        "labels": [{"name": "growth-radar"}],
    }


class RadarIssueGuardTests(unittest.TestCase):
    def test_accepts_canonical_bot_owned_issue(self):
        self.assertEqual(validate_issue(valid_issue()), [])

    def test_rejects_human_owned_issue(self):
        issue = valid_issue()
        issue["author"] = {"login": "alptugharun"}
        self.assertIn("unexpected author", " ".join(validate_issue(issue)))

    def test_rejects_wrong_title(self):
        issue = valid_issue()
        issue["title"] = "🧪 Real User Lab #1 — 10 independent first-run reports wanted"
        self.assertIn("unexpected title", " ".join(validate_issue(issue)))

    def test_rejects_wrong_issue_number(self):
        issue = valid_issue()
        issue["number"] = 178
        self.assertIn("expected issue #7", " ".join(validate_issue(issue)))

    def test_rejects_missing_growth_radar_label(self):
        issue = valid_issue()
        issue["labels"] = [{"name": "feedback"}]
        self.assertIn("missing required label", " ".join(validate_issue(issue)))


if __name__ == "__main__":
    unittest.main()
