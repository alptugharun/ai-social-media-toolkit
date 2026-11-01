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


# Git accepts global options before the subcommand. Recognize common literal
# forms without claiming to parse aliases, variables, or the entire shell.
GIT_GLOBAL_FLAG = (
    r"(?:-C(?:\s+\S+|\S+)|-c(?:\s+\S+|\S+)"
    r"|--(?:git-dir|work-tree|namespace|config-env)(?:=\S+|\s+\S+)"
    r"|--(?:no-pager|bare|no-replace-objects))"
)
GIT_COMMAND = r"\bgit(?:\s+" + GIT_GLOBAL_FLAG + r")*\s+"


RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "force-push",
        re.compile(GIT_COMMAND + r"push\b[^\n;&|]*(?:--force(?:-with-lease)?|-f)(?=\s|=|[;&|)]|$)", re.IGNORECASE),
    ),
    (
        "hard-reset",
        re.compile(GIT_COMMAND + r"reset\b[^\n;&|]*\s--hard(?=\s|[;&|)]|$)", re.IGNORECASE),
    ),
    (
        "release-clobber",
        re.compile(r"\bgh\s+release\s+upload\b[^\n;&|]*--clobber(?=\s|[;&|)]|$)", re.IGNORECASE),
    ),
    (
        "delete-protected-branch",
        re.compile(GIT_COMMAND + r"push\b[^\n;&|]*--delete\s+(?:main|master)(?=\s|[;&|)]|$)", re.IGNORECASE),
    ),
    (
        "delete-local-protected-branch",
        re.compile(GIT_COMMAND + r"branch\s+-D\s+(?:main|master)(?=\s|[;&|)]|$)", re.IGNORECASE),
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




# Git accepts deletion flags before the remote name and empty-source refspecs.
# A leading + on a push refspec is another force-push form without --force.
PROTECTED_REMOTE_BRANCHES = frozenset({"main", "master", "refs/heads/main", "refs/heads/master"})


def _destructive_push_refspec(command: str) -> str | None:
    """Inspect literal Git push arguments without executing or expanding them.

    Tokenizing one shell segment also detects quoted refspecs and prevents
    flags in a subsequent shell command from affecting this decision.
    """
    for match in re.finditer(GIT_COMMAND + r"push\b", command, re.IGNORECASE):
        tail = re.split(r"[\n;&|]", command[match.end():], maxsplit=1)[0]
        try:
            args = shlex.split(tail)
        except ValueError:
            return "unparseable-git-push"

        # Both modes can remove remote refs; --mirror also forces updates.
        # Check parsed tokens, not a cross-command regex, to avoid treating
        # a subsequent shell echo as part of the git push argument list.
        if "--mirror" in args:
            return "mirror-push"
        if "--prune" in args:
            return "prune-push"
        if any(arg.startswith("+") and len(arg) > 1 for arg in args):
            return "force-push"
        if any(arg.startswith(":") and arg[1:] in PROTECTED_REMOTE_BRANCHES for arg in args):
            return "delete-protected-branch"
        if ("--delete" in args or "-d" in args) and any(
            arg in PROTECTED_REMOTE_BRANCHES for arg in args
        ):
            return "delete-protected-branch"
    return None


def _destructive_local_branch_delete(command: str) -> str | None:
    """Guard literal deletion of protected local branches, including -d and -D.

    Examine only the branch subcommand's own shell segment; text belonging to
    a later command must not be interpreted as a target branch.
    """
    for match in re.finditer(GIT_COMMAND + r"branch\b", command, re.IGNORECASE):
        tail = re.split(r"[\n;&|]", command[match.end():], maxsplit=1)[0]
        try:
            args = shlex.split(tail)
        except ValueError:
            return "unparseable-git-branch"

        short_flags = set(
            "".join(arg[1:] for arg in args if arg.startswith("-") and not arg.startswith("--"))
        )
        deleting = bool({"d", "D"} & short_flags) or "--delete" in args
        if deleting and any(arg in {"main", "master"} for arg in args):
            return "delete-local-protected-branch"
    return None


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

    push_rule = _destructive_push_refspec(command)
    if push_rule is not None:
        return _deny(f"Blocked by repository safety hook ({push_rule}). Use a reversible alternative and human review.")

    branch_rule = _destructive_local_branch_delete(command)
    if branch_rule is not None:
        return _deny(f"Blocked by repository safety hook ({branch_rule}). Use a reversible alternative and human review.")

    if _recursive_root_delete(command):
        return _deny("Blocked by repository safety hook (recursive-root-delete or unparseable shell syntax).")

    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
