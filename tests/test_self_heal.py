import unittest

from tools.self_heal import classify


class SelfHealTests(unittest.TestCase):
    def test_ambiguous_github_403_is_not_blindly_retried(self):
        d = classify(
            "GitHub API error: 403 Forbidden\n##[error]Process completed with exit code 2.",
            workflow="GitHub Opportunity Radar",
            run_id="123",
            run_attempt=1,
        )
        self.assertEqual(d.classification, "github-api-403")
        self.assertFalse(d.retryable)
        self.assertFalse(d.probe_retry_safe)
        self.assertEqual(d.confidence, "medium")
        self.assertEqual(len(d.fingerprint), 12)

    def test_secondary_rate_limit_is_not_blindly_retried(self):
        log = (
            "GitHub API error: 403 Forbidden; endpoint=/search/repositories; "
            "category=secondary-rate-limit; remaining=21"
        )
        first = classify(log, workflow="GitHub Opportunity Radar", run_id="40490105926")
        second = classify(
            log.replace("remaining=21", "remaining=19"),
            workflow="GitHub Opportunity Radar",
            run_id="40490105926",
            run_attempt=2,
        )
        other_run = classify(log, workflow="GitHub Opportunity Radar", run_id="40490105927")
        self.assertEqual(first.classification, "github-api-rate-limit")
        self.assertEqual(first.confidence, "high")
        self.assertFalse(first.retryable)
        self.assertFalse(first.probe_retry_safe)
        self.assertEqual(first.fingerprint, second.fingerprint)
        self.assertNotEqual(first.fingerprint, other_run.fingerprint)

    def test_primary_rate_limit_is_not_blindly_retried(self):
        d = classify(
            "GitHub API error: 403 Forbidden; endpoint=/search/repositories; "
            "category=primary-rate-limit; remaining=0; reset=1790000000",
            workflow="GitHub Opportunity Radar",
            run_id="321",
        )
        self.assertEqual(d.classification, "github-api-rate-limit")
        self.assertFalse(d.retryable)

    def test_non_rate_limited_server_error_remains_retryable(self):
        d = classify("HTTP 503 Service Unavailable", workflow="Maps & Local Intelligence Radar")
        self.assertEqual(d.classification, "transient-network-or-http")
        self.assertTrue(d.retryable)

    def test_github_403_retries_are_one_incident_per_workflow_run(self):
        workflow = "GitHub Opportunity Radar"
        run_id = "40313193969"
        failures = [
            "2026-10-26T11:12:08.4331080Z GitHub API error: 403 Forbidden\n"
            "##[error]Process completed with exit code 2.",
            "2026-10-26T11:14:13.5494406Z radar Generate report "
            "GitHub API error: 403 Forbidden\n"
            "##[error]Process completed with exit code 2.",
            "2026-10-26T11:17:05.7108770Z radar Generate report "
            "GitHub API error: 403 Forbidden\n"
            "##[error]Process completed with exit code 2.",
        ]
        incidents = [
            classify(log, workflow=workflow, run_id=run_id, run_attempt=attempt)
            for attempt, log in enumerate(failures, 1)
        ]
        self.assertTrue(all(d.classification == "github-api-403" for d in incidents))
        self.assertEqual(len({d.fingerprint for d in incidents}), 1)
        other_run = classify(failures[0], workflow=workflow, run_id="40313193970")
        other_workflow = classify(failures[0], workflow="Different Workflow", run_id=run_id)
        self.assertNotEqual(incidents[0].fingerprint, other_run.fingerprint)
        self.assertNotEqual(incidents[0].fingerprint, other_workflow.fingerprint)

    def test_readiness_failure_is_not_blindly_retried(self):
        d = classify(
            "READINESS FAIL: Top-level workflow permissions must remain read-only.\n"
            "Process completed with exit code 1.",
            workflow="Validate Agent Skills",
        )
        self.assertEqual(d.classification, "quality-gate-regression")
        self.assertEqual(d.confidence, "high")
        self.assertFalse(d.retryable)
        self.assertFalse(d.probe_retry_safe)

    def test_docs_validation_failure_is_not_blindly_retried(self):
        d = classify(
            "DOCS VALIDATION FAIL\n- README.md:12: broken relative link: missing.md",
            workflow="Validate Agent Skills",
        )
        self.assertEqual(d.classification, "quality-gate-regression")
        self.assertFalse(d.retryable)

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


    def test_successful_test_name_containing_fails_is_not_error_evidence(self):
        d = classify(
            "validate (windows-2025) Run installer tests 2026-10-11T21:03:01Z "
            "test_missing_tool_fails (test_mcp_smoke_client.MCPSmokeClientTests.test_missing_tool_fails) ... ok\n"
            "FAILED (failures=1)\n"
            "FAIL: test_real_regression\n"
            "AssertionError: expected true",
            workflow="Validate Agent Skills",
        )
        self.assertEqual(d.classification, "test-regression")
        self.assertTrue(all("test_missing_tool_fails" not in line for line in d.evidence))

    def test_same_failed_test_set_dedupes_across_changed_runner_noise(self):
        first = classify(
            "validate (windows-2025) Run installer tests 2026-10-17T11:13:00Z "
            "test_initial_signing_uploads_once_without_replace (suite.Tests.test_initial_signing_uploads_once_without_replace) ... FAIL\n"
            "FAIL: test_initial_signing_uploads_once_without_replace\n"
            "AssertionError: 1 != 0\n"
            "FAIL: test_partial_signatures_fail_closed_without_upload\n"
            "AssertionError: expected message A\n"
            "FAIL: test_rerun_preserves_all_existing_bundles\n"
            "AssertionError: expected message B\n"
            "FAILED (failures=3)",
            workflow="Validate Agent Skills",
        )
        second = classify(
            "validate (windows-2025) Run installer tests 2026-10-17T11:38:07Z "
            "test_rerun_preserves_all_existing_bundles (suite.Tests.test_rerun_preserves_all_existing_bundles) ... FAIL\n"
            "Traceback (most recent call last):\n"
            "FAIL: test_rerun_preserves_all_existing_bundles\n"
            "AssertionError: changed downstream text\n"
            "FAIL: test_initial_signing_uploads_once_without_replace\n"
            "AssertionError: different launcher text\n"
            "FAIL: test_partial_signatures_fail_closed_without_upload\n"
            "FAILED (failures=3)",
            workflow="Validate Agent Skills",
        )
        self.assertEqual(first.classification, "test-regression")
        self.assertEqual(first.fingerprint, second.fingerprint)

    def test_different_failed_test_sets_get_different_fingerprints(self):
        one = classify(
            "FAIL: test_release_asset_license\nAssertionError: missing LICENSE\nFAILED (failures=1)",
            workflow="Validate Agent Skills",
        )
        two = classify(
            "FAIL: test_release_asset_checksum\nAssertionError: checksum mismatch\nFAILED (failures=1)",
            workflow="Validate Agent Skills",
        )
        self.assertNotEqual(one.fingerprint, two.fingerprint)

    def test_matrix_prefixes_produce_same_test_regression_fingerprint(self):
        base = (
            "test_missing_tool_fails (suite.TestCase.test_missing_tool_fails) ... ok\n"
            "FAIL: test_real_regression\n"
            "AssertionError: expected true\n"
            "FAILED (failures=1)"
        )
        windows = "validate (windows-2025) Run installer tests 2026-10-11T21:03:01Z " + base
        ubuntu = "validate (ubuntu-26.04) Run installer tests 2026-10-11T21:03:02Z " + base
        a = classify(windows, workflow="Validate Agent Skills")
        b = classify(ubuntu, workflow="Validate Agent Skills")
        self.assertEqual(a.classification, "test-regression")
        self.assertEqual(a.fingerprint, b.fingerprint)


if __name__ == "__main__":
    unittest.main()
