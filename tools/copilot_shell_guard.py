#!/usr/bin/env python3
"""GitHub Copilot preToolUse guard for a small set of destructive shell actions.

The hook is intentionally narrow. It does not try to parse arbitrary shell
syntax or replace GitHub permissions, branch protection, review, or CI.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any


RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "force-push",
        re.compile(r"\bgit\s+push\b[^\n]*(?:--force(?:-with-lease)?|-f)(?:\s|=|$)", re.IGNORECASE),
    ),
    (
        "hard-reset",
        re.compile(r"\bgit\s+reset\s+--hard(?:\s|$)", re.IGNORECASE),
    ),
    (
        "release-clobber",
        re.compile(r"\bgh\s+release\s+upload\b[^\n]*--clobber(?:\s|$)", re.IGNORECASE),
    ),
    (
        "delete-protected-branch",
        re.compile(r"\bgit\s+push\b[^\n]*--delete\s+(?:main|master)(?:\s|$)", re.IGNORECASE),
    ),
    (
        "delete-local-protected-branch",
        re.compile(r"\bgit\s+branch\s+-D\s+(?:main|master)(?:\s|$)", re.IGNORECASE),
    ),
    (
        "remote-script-pipe",
        re.compile(r"\b(?:curl|wget)\b[^\n|]*\|\s*(?:sudo\s+)?(?:sh|bash|zsh)\b", re.IGNORECASE),
    ),
    (
        "powershell-download-exec",
        re.compile(r"\b(?:Invoke-WebRequest|iwr)\b[^\n|]*\|\s*(?:Invoke-Expression|iex)\b", re.IGNORECASE),
    ),
    (
        "recursive-root-delete",
        re.compile(r"\brm\s+-[A-Za-z]*r[A-Za-z]*f[A-Za-z]*\s+(?:/|\.|\.\.)(?:\s|$)", re.IGNORECASE),
    ),
)


def _strings(value: Any, *, depth: int = 0) -> list[str]:
    if depth > 8:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(_strings(item, depth=depth + 1))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(_strings(item, depth=depth + 1))
        return result
    return []


def _deny(reason: str) -> int:
    print(
        json.dumps(
            {
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        )
    )
    return 0


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return _deny("Shell tool blocked because the preToolUse payload could not be inspected.")

    if not isinstance(payload, dict):
        return _deny("Shell tool blocked because the preToolUse payload is not an object.")

    tool_name = payload.get("toolName") or payload.get("tool_name")
    if tool_name not in {"bash", "powershell", "shell", "execute"}:
        print("{}")
        return 0

    tool_args = payload.get("toolArgs")
    if tool_args is None:
        tool_args = payload.get("tool_input")

    command = "\n".join(_strings(tool_args)).strip()
    if not command:
        return _deny("Shell tool blocked because its command arguments could not be inspected.")

    for rule_name, pattern in RULES:
        if pattern.search(command):
            return _deny(
                f"Blocked by repository safety hook ({rule_name}). "
                "Use a reversible alternative or obtain explicit human approval outside the agent."
            )

    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
