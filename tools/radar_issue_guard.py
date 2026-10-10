from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


EXPECTED_TITLE = "GitHub Opportunity Radar — latest"
EXPECTED_AUTHOR = "github-actions[bot]"
EXPECTED_LABEL = "growth-radar"
EXPECTED_ISSUE_NUMBER = 7


def validate_issue(issue: dict[str, Any], expected_number: int = EXPECTED_ISSUE_NUMBER) -> list[str]:
    errors: list[str] = []

    number = issue.get("number")
    title = issue.get("title")
    state = str(issue.get("state", "")).lower()
    author = (issue.get("author") or {}).get("login")
    labels = {
        label.get("name")
        for label in (issue.get("labels") or [])
        if isinstance(label, dict)
    }

    if number != expected_number:
        errors.append(f"expected issue #{expected_number}, got #{number}")
    if title != EXPECTED_TITLE:
        errors.append(f"unexpected title: {title!r}")
    if state != "open":
        errors.append(f"expected open issue, got {state or 'missing'}")
    if author != EXPECTED_AUTHOR:
        errors.append(f"unexpected author: {author!r}")
    if EXPECTED_LABEL not in labels:
        errors.append(f"missing required label: {EXPECTED_LABEL}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail closed unless the canonical GitHub Opportunity Radar issue is verified."
    )
    parser.add_argument("issue_json", type=Path)
    parser.add_argument("--issue-number", type=int, default=EXPECTED_ISSUE_NUMBER)
    args = parser.parse_args()

    issue = json.loads(args.issue_json.read_text(encoding="utf-8"))
    errors = validate_issue(issue, expected_number=args.issue_number)

    if errors:
        print("Refusing to update a non-canonical radar issue:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 2

    print(f"Verified canonical radar issue #{args.issue_number}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
