#!/usr/bin/env python3
"""Route GitHub issue/Conversation events to a persistent support inbox.

No model call, comment, code change or merge is performed. Untrusted text is not
executed, forwarded or printed. The separate operator reads the live thread.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

REPOSITORY = "alptugharun/ai-social-media-toolkit"
REPOSITORY_ID = 1383006854
OWNER = "alptugharun"
INBOX_LABEL = "support:inbox"
TEST_TITLE = "Support intake self-test (internal, not a user report)"
TEST_MARKER = "<!-- community-intake-internal-test -->"
MAX_BYTES = 1_048_576
BASE = f"/repos/{REPOSITORY}"


class IntakeError(Exception):
    """Public-safe failure without request bodies or credentials."""


class ApiError(IntakeError):
    def __init__(self, status: int):
        self.status = status
        super().__init__(f"GitHub API HTTP {status}; no automatic retry or permission change")


def object_value(value):
    return value if isinstance(value, dict) else {}


def positive_integer(value):
    return type(value) is int and value > 0


def human_user(value):
    user = object_value(value)
    login = user.get("login", "")
    return (
        user.get("type") == "User"
        and isinstance(login, str)
        and re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", login) is not None
    )


def plan_event(event_name: str, event: dict) -> dict:
    """Pure decision function; does not inspect or interpret comment instructions."""
    event = object_value(event)
    repo = object_value(event.get("repository"))
    if (repo.get("full_name") != REPOSITORY or repo.get("id") != REPOSITORY_ID
            or repo.get("private") is not False):
        return {"status": "SKIP", "reason": "repository-out-of-scope"}
    if event_name not in {"issues", "issue_comment"}:
        return {"status": "SKIP", "reason": "unsupported-event"}
    actions = {"opened", "edited", "reopened"} if event_name == "issues" else {"created", "edited"}
    if event.get("action") not in actions:
        return {"status": "SKIP", "reason": "unsupported-action"}
    issue = object_value(event.get("issue"))
    number = issue.get("number")
    if not positive_integer(number):
        return {"status": "SKIP", "reason": "invalid-issue-number"}
    if issue.get("locked") is not False:
        return {"status": "SKIP", "reason": "locked-or-unknown-thread"}
    sender = object_value(event.get("sender"))
    source = issue if event_name == "issues" else object_value(event.get("comment"))
    author = object_value(source.get("user"))
    if not human_user(sender) or not human_user(author):
        return {"status": "SKIP", "reason": "bot-or-unknown-actor"}
    internal_test = (
        event_name == "issues"
        and sender.get("login", "").lower() == OWNER
        and author.get("login", "").lower() == OWNER
        and issue.get("title") == TEST_TITLE
        and TEST_MARKER in str(issue.get("body", ""))
    )
    if not internal_test and (sender.get("login", "").lower() == OWNER
                              or author.get("login", "").lower() == OWNER):
        return {"status": "SKIP", "reason": "maintainer-event"}
    source_id = source.get("id")
    if not positive_integer(source_id):
        return {"status": "SKIP", "reason": "invalid-source-id"}
    # Only identifiers are logged, never user text, URLs, credentials or email.
    return {
        "status": "ROUTE", "issue_number": number,
        "source_kind": event_name, "source_id": source_id,
        "internal_test": internal_test,
    }


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise IntakeError("Redirect refused; token was not forwarded")


class GitHubApi:
    def __init__(self, token: str):
        if not token:
            raise IntakeError("GITHUB_TOKEN is missing; no write attempted")
        self.token = token
        self.opener = build_opener(NoRedirect())

    def request(self, method: str, path: str, payload=None):
        # Restrict the interface to the single inbox label and issue reads/labels.
        label_path = f"{BASE}/labels/{quote(INBOX_LABEL, safe='')}"
        issue_path = re.fullmatch(re.escape(BASE) + r"/issues/[1-9][0-9]*(/labels)?", path)
        allowed = (
            (method == "GET" and (path == label_path or bool(issue_path)))
            or (method == "POST" and path == f"{BASE}/labels" and payload == {
                "name": INBOX_LABEL, "color": "1D76DB",
                "description": "Routed to support; label does not mean unresolved or verified",
            })
            or (method == "POST" and bool(issue_path) and path.endswith("/labels")
                and payload == {"labels": [INBOX_LABEL]})
        )
        if not allowed:
            raise IntakeError("Operation is outside the intake allowlist")
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request("https://api.github.com" + path, data=data, method=method, headers={
            "Authorization": "Bearer " + self.token,
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "ai-social-media-toolkit-community-intake",
        })
        try:
            with self.opener.open(request, timeout=20) as response:
                raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise IntakeError("GitHub response exceeded the size limit")
            return json.loads(raw)
        except HTTPError as exc:
            raise ApiError(exc.code) from None
        except (URLError, TimeoutError, OSError):
            raise IntakeError("GitHub request failed; check the run without sharing credentials") from None
        except (UnicodeError, json.JSONDecodeError):
            raise IntakeError("GitHub returned invalid JSON") from None


def label_names(issue):
    labels = object_value(issue).get("labels", [])
    if not isinstance(labels, list):
        raise IntakeError("Invalid labels response")
    return {item.get("name") for item in labels if isinstance(item, dict)}


def route(plan: dict, api) -> dict:
    if plan.get("status") != "ROUTE":
        return plan
    number = plan.get("issue_number")
    if not positive_integer(number):
        raise IntakeError("Invalid issue number")
    path = f"{BASE}/issues/{number}"
    current = object_value(api.request("GET", path))
    if current.get("number") != number:
        raise IntakeError("Live thread did not match the event")
    if current.get("locked") is not False:
        return {**plan, "status": "SKIP", "reason": "thread-now-locked"}
    if INBOX_LABEL in label_names(current):
        return {**plan, "status": "ALREADY_ROUTED"}
    label_path = f"{BASE}/labels/{quote(INBOX_LABEL, safe='')}"
    try:
        api.request("GET", label_path)
    except ApiError as exc:
        if exc.status != 404:
            raise
        try:
            api.request("POST", f"{BASE}/labels", {
                "name": INBOX_LABEL, "color": "1D76DB",
                "description": "Routed to support; label does not mean unresolved or verified",
            })
        except ApiError as created:
            if created.status != 422:
                raise
            # A concurrent first event may have created the same label.
            api.request("GET", label_path)
    try:
        api.request("POST", path + "/labels", {"labels": [INBOX_LABEL]})
    except IntakeError:
        # An ambiguous response is read back, never blindly posted again.
        if INBOX_LABEL in label_names(api.request("GET", path)):
            return {**plan, "status": "ROUTED_READBACK"}
        raise
    after = object_value(api.request("GET", path))
    if INBOX_LABEL not in label_names(after):
        raise IntakeError("Inbox label was not confirmed by read-back")
    return {**plan, "status": "ROUTED_VERIFIED"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event-file", type=Path, default=None)
    parser.add_argument("--event-name", default=None)
    parser.add_argument("--apply", action="store_true", help="Apply only inside the authorized GitHub workflow")
    args = parser.parse_args()
    try:
        if args.apply and (os.getenv("GITHUB_ACTIONS") != "true"
                           or os.getenv("GITHUB_REPOSITORY") != REPOSITORY
                           or args.event_file is not None or args.event_name is not None):
            raise IntakeError("Apply requires the repository's native GitHub event context")
        event_path = args.event_file or Path(os.getenv("GITHUB_EVENT_PATH", "/nonexistent-event"))
        if event_path.stat().st_size > MAX_BYTES:
            raise IntakeError("Event exceeded the size limit")
        event = json.loads(event_path.read_text(encoding="utf-8"))
        plan = plan_event(args.event_name or os.getenv("GITHUB_EVENT_NAME", ""), event)
        result = route(plan, GitHubApi(os.getenv("GITHUB_TOKEN", ""))) if args.apply and plan["status"] == "ROUTE" else plan
        print(json.dumps({"mode": "apply" if args.apply else "dry-run", **result}, sort_keys=True))
        return 0
    except (IntakeError, OSError, ValueError, TypeError) as exc:
        # Do not expose parser excerpts, raw payloads or user-controlled strings.
        message = str(exc) if isinstance(exc, IntakeError) else "Invalid or unavailable event file"
        print("community-intake: " + message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
