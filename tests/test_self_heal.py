import unittest

from tools.self_heal import classify


class SelfHealTests(unittest.TestCase):
    def test_github_403_is_bounded_retry_candidate(self):
        d = classify(
            "GitHub API error: 403 Forbidden\n##[error]Process completed with exit code 2.",
            workflow="GitHub Opportunity Radar",
            run_id="123",
            run_attempt=1,
        )
        self.assertEqual(d.classification, "github-api-403")
        self.assertTrue(d.retryable)
        self.assertEqual(len(d.fingerprint), 12)

    def test_assertion_failure_is_not_blindly_retried(self):
        d = classify(
            "FAIL: test_parse_trending\nAssertionError: 0 != 1234\nFAILED (failures=1)",
            workflow="Validate Agent Skills",
        )
        self.assertEqual(d.classification, "test-regression")
        self.assertFalse(d.retryable)

    def test_unknown_failure_can_be_probed_once_by_policy(self):
        d = classify(
            "strange new provider response: frobnicator unavailable",
            workflow="Pinterest Visibility Radar",
        )
        self.assertEqual(d.classification, "unknown")
        self.assertFalse(d.retryable)
        self.assertTrue(d.probe_retry_safe)

    def test_permission_failure_is_persistent(self):
        d = classify(
            "Resource not accessible by integration",
            workflow="Automation Health Watch",
        )
        self.assertEqual(d.classification, "auth-or-permission")
        self.assertFalse(d.retryable)


if __name__ == "__main__":
    unittest.main()
