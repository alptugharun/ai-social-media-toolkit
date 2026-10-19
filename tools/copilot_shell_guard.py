#!/usr/bin/env python3
"""Narrow Copilot preToolUse guard for selected destructive shell actions.

This is a defense-in-depth check, not a general shell interpreter. Existing
permissions, code review and CI remain mandatory.
"""

from __future__ import annotations

import json
import re
import shlex
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
)


# Only known destructive root/current/parent targets are guarded. This check
# deliberately does not claim to recognize every possible shell expression.
PROTECTED_TARGETS = frozenset({"/", "//", ".", "./", "..", "../", "/.", "/.."})
SHELL_SEPARATORS = frozenset({";", "&&", "||", "|", "&", "(", ")"})


def _shell_args(payload: dict[str, Any]) -> str | None:
    """Extract only the actual command, not descriptive tool metadata.

    Copilot CLI documents toolArgs as a JSON-encoded string. Other hosts may
    pass an already-decoded object, so both shapes are accepted.
    """
    args = payload.get("toolArgs")
    if args is None:
        args = payload.get("tool_input")
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except (ValueError, TypeError):
            return None
    if not isinstance(args, dict):
        return None
    command = args.get("command")
    if not isinstance(command, str) or not command.strip():
        return None
    return command


def _recursive_root_delete(command: str) -> bool:
    """Catch rm's short/long flags regardless of flag order or grouping.

    This is a narrow lexical check; it does not evaluate shell substitutions,
    script files, indirect aliases, or interpreter-specific escape syntax.
    """
    try:
        lex = shlex.shlex(command, posix=True, punctuation_chars=";&|()")
        lex.whitespace_split = True
        tokens = list(lex)
    except ValueError:
        # Refuse uninterpretable input rather than silently assuming it is safe.
        return True

    for index, token in enumerate(tokens):
        if token not in {"rm", "/bin/rm"}:
            continue
        recursive = False
        force = False
        options_ended = False
        target = False
        for arg in tokens[index + 1 :]:
            if arg in SHELL_SEPARATORS:
                break
            if not options_ended and arg == "--":
                options_ended = True
                continue
            if not options_ended and arg == "--recursive":
                recursive = True
                continue
            if not options_ended and arg == "--force":
                force = True
                continue
            if not options_ended and arg.startswith("-") and not arg.startswith("--"):
                recursive = recursive or ("r" in arg[1:] or "R" in arg[1:])
                force = force or "f" in arg[1:]
                continue
            target = target or arg in PROTECTED_TARGETS
        if recursive and force and target:
            return True
    return False


def _deny(reason: str) -> int:
    print(json.dumps({"permissionDecision": "deny", "permissionDecisionReason": reason}))
    return 0


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return _deny("Shell tool blocked because the hook input is not valid JSON.")

    if not isinstance(payload, dict):
        return _deny("Shell tool blocked because the hook input is not an object.")

    tool_name = payload.get("toolName") or payload.get("tool_name")
    if tool_name not in {"bash", "powershell", "shell", "execute"}:
        print("{}")
        return 0

    command = _shell_args(payload)
    if command is None:
        return _deny("Shell tool blocked because its command arguments could not be inspected.")

    for rule_name, pattern in RULES:
        if pattern.search(command):
            return _deny(f"Blocked by repository safety hook ({rule_name}). Use a reversible alternative and human review.")

    if _recursive_root_delete(command):
        return _deny("Blocked by repository safety hook (recursive-root-delete or unparseable shell syntax).")

    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
