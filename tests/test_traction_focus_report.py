import unittest

from tools.traction_focus_report import focus_state, render


class TractionFocusReportTests(unittest.TestCase):
    def test_build_proof_for_low_external_signals(self):
        metrics = {
            "stars": 1,
            "forks": 0,
            "subscribers": 1,
            "open_issues": 4,
            "release_count": 0,
            "external_issue_count_sample": 0,
            "external_contributor_count_sample": 0,
            "has_discussions": False,
            "pushed_at": "2026-09-27T00:00:00Z",
        }
        state, _ = focus_state(metrics)
        self.assertEqual(state, "BUILD PROOF")

    def test_bot_activity_is_not_described_as_external_adoption(self):
        metrics = {
            "stars": 1,
            "forks": 0,
            "subscribers": 1,
            "open_issues": 4,
            "release_count": 0,
            "external_issue_count_sample": 0,
            "external_contributor_count_sample": 0,
            "has_discussions": False,
            "pushed_at": "2026-09-27T00:00:00Z",
        }
        state, reasons = focus_state(metrics)
        self.assertEqual(state, "BUILD PROOF")
        self.assertEqual(reasons, [])

    def test_report_separates_activity_from_adoption(self):
        metrics = {
            "stars": 1,
            "forks": 0,
            "subscribers": 1,
            "open_issues": 4,
            "release_count": 0,
            "external_issue_count_sample": 0,
            "external_contributor_count_sample": 0,
            "has_discussions": False,
            "pushed_at": "2026-09-27T00:00:00Z",
        }
        report = render(metrics)
        self.assertIn("Commit count is internal activity, not adoption.", report)
        self.assertIn("Prefer improving existing skills over adding new lanes.", report)
        self.assertIn("implementation service", report)


if __name__ == "__main__":
    unittest.main()
