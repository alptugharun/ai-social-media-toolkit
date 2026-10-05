#!/usr/bin/env python3
"""Static, local-first risk review for MCP stdio configuration.

This tool does not launch servers, contact the network, or prove runtime safety.
It inspects configuration shape and reports bounded heuristics.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

SECRET_RE = re.compile(r"(token|secret|password|passwd|api[_-]?key|credential|private[_-]?key|auth)", re.I)
URL_RE = re.compile(r"https?://", re.I)
ABS_PATH_RE = re.compile(r"^(?:[A-Za-z]:[\\/]|/)")
SHELLS = {"bash", "bash.exe", "sh", "sh.exe", "zsh", "zsh.exe", "fish", "fish.exe", "cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "pwsh.exe"}
RUNNERS = {"npx", "npx.cmd", "npx.exe", "uvx", "uvx.exe", "pipx", "pipx.exe", "bunx", "bunx.exe", "pnpx", "pnpx.cmd", "pnpx.exe"}
SHELL_FLAGS = {"-c", "/c", "-command", "-encodedcommand"}
BROAD_PATHS = {"/", "~", "/home", "/users", "c:\\", "c:/"}

SEVERITY_SCORE = {"info": 0, "low": 1, "medium": 2, "high": 3}


class InspectorError(ValueError):
    pass


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    remediation: str


@dataclass(frozen=True)
class ServerReport:
    name: str
    command: str
    args: list[str]
    env_keys: list[str]
    risk: str
    findings: list[Finding]


def load_config(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise InspectorError(f"Could not read valid UTF-8 JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise InspectorError("Top-level MCP config must be a JSON object.")
    return data


def server_map(data: dict[str, Any]) -> dict[str, Any]:
    for key in ("mcpServers", "servers"):
        value = data.get(key)
        if isinstance(value, dict):
            return value
    # Accept a single server object for CI/tests and small snippets.
    if "command" in data:
        return {"server": data}
    raise InspectorError("No MCP server map found. Expected 'mcpServers', 'servers', or a single server object.")


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(x, (str, int, float, bool)) for x in value):
        raise InspectorError("Server 'args' must be a list of scalar values.")
    return [str(x) for x in value]


def _redact_url(value: str) -> str:
    try:
        parts = urlsplit(value)
    except ValueError:
        return value
    if parts.scheme.lower() not in {"http", "https"}:
        return value

    netloc = parts.netloc
    if "@" in netloc:
        host = netloc.rsplit("@", 1)[1]
        netloc = "<redacted-userinfo>@" + host

    query = []
    for key, val in parse_qsl(parts.query, keep_blank_values=True):
        query.append((key, "<redacted>" if SECRET_RE.search(key) else val))
    return urlunsplit((parts.scheme, netloc, parts.path, urlencode(query), parts.fragment))


def _redact_args(args: list[str]) -> list[str]:
    redacted: list[str] = []
    redact_next = False
    for arg in args:
        if redact_next:
            redacted.append("<redacted>")
            redact_next = False
            continue

        if URL_RE.search(arg):
            redacted.append(_redact_url(arg))
            continue

        if "=" in arg:
            key, value = arg.split("=", 1)
            if SECRET_RE.search(key):
                redacted.append(key + "=<redacted>")
                continue

        if arg.startswith("-") and SECRET_RE.search(arg):
            redacted.append(arg)
            redact_next = True
            continue

        redacted.append(arg)
    return redacted


def _is_broad_path(value: str) -> bool:
    raw = value.strip().replace("\\", "/").lower()
    if raw == "/":
        return True
    normalized = raw.rstrip("/")
    if normalized in {"", ".", ".."}:
        return False
    if normalized in {"~", "/home", "/users"}:
        return True
    return bool(re.fullmatch(r"[a-z]:", normalized))


def inspect_server(name: str, raw: Any) -> ServerReport:
    if not isinstance(raw, dict):
        raise InspectorError(f"Server '{name}' must be an object.")

    command = str(raw.get("command", "")).strip()
    if not command:
        raise InspectorError(f"Server '{name}' has no command.")

    args = _string_list(raw.get("args"))
    env = raw.get("env") or {}
    if not isinstance(env, dict):
        raise InspectorError(f"Server '{name}' env must be an object.")

    env_keys = sorted(str(k) for k in env)
    findings: list[Finding] = []
    cmd_name = Path(command.replace("\\", "/")).name.lower()
    lowered = [a.lower() for a in args]
    reported_args = _redact_args(args)

    if cmd_name in SHELLS:
        findings.append(Finding(
            "high", "shell-execution",
            f"Server is launched through a general-purpose shell: {cmd_name}.",
            "Prefer launching the MCP executable directly; remove shell indirection unless it is strictly required."
        ))

    if any(a in SHELL_FLAGS for a in lowered):
        findings.append(Finding(
            "high", "shell-command-flag",
            "Arguments contain a shell command/evaluation flag.",
            "Replace inline shell evaluation with a direct executable + explicit argument list."
        ))

    secret_keys = [k for k in env_keys if SECRET_RE.search(k)]
    if secret_keys:
        findings.append(Finding(
            "medium", "sensitive-env",
            "Configuration references sensitive environment variable names: " + ", ".join(secret_keys) + ". Values are intentionally not displayed.",
            "Use the narrowest token scopes, prefer host secret stores/environment injection, and never commit secret values."
        ))

    if any(URL_RE.search(a) for a in args):
        findings.append(Finding(
            "medium", "network-target",
            "Arguments contain an HTTP(S) target, so the configured server may depend on network access.",
            "Verify the destination, data boundary and authentication scope before enabling the server."
        ))

    path_args = [a for a in args if ABS_PATH_RE.search(a)]
    broad = [a for a in path_args if _is_broad_path(a)]
    if broad:
        findings.append(Finding(
            "high", "broad-filesystem-path",
            "Arguments appear to expose a broad filesystem root: " + ", ".join(broad) + ".",
            "Scope filesystem access to the smallest project/workspace directory required."
        ))
    elif path_args:
        findings.append(Finding(
            "low", "filesystem-path",
            "Arguments contain absolute filesystem paths.",
            "Confirm each path is required and avoid parent/home/root directories when a narrower workspace path works."
        ))

    if cmd_name in RUNNERS:
        findings.append(Finding(
            "low", "package-runner",
            f"Server is launched through package runner '{cmd_name}'.",
            "For repeatable installs, prefer an exact package version and record the expected executable/version."
        ))
        if "-y" in lowered or "--yes" in lowered:
            findings.append(Finding(
                "medium", "auto-install",
                "Package runner is allowed to auto-confirm installation.",
                "Pin the package version and consider installing it explicitly before host startup."
            ))

    unpinned = []
    for a in args:
        if a.startswith("-") or URL_RE.search(a):
            continue
        if cmd_name == "npx" and re.match(r"^(?:@[^/]+/)?[^@/]+$", a):
            unpinned.append(a)
        elif cmd_name in {"uvx", "pipx"} and re.match(r"^[A-Za-z0-9_.-]+$", a):
            unpinned.append(a)
    if unpinned:
        findings.append(Finding(
            "medium", "unpinned-package",
            "Package runner appears to reference an unpinned package: " + ", ".join(unpinned[:3]) + ".",
            "Pin an exact reviewed version for reproducible host configuration."
        ))

    if not findings:
        findings.append(Finding(
            "info", "no-obvious-static-risk",
            "No obvious high-risk pattern was found in this configuration snippet.",
            "Still verify the upstream package, runtime behavior, requested host permissions and first tool call."
        ))

    risk = max((f.severity for f in findings), key=lambda s: SEVERITY_SCORE[s])
    return ServerReport(name=name, command=command, args=reported_args, env_keys=env_keys, risk=risk, findings=findings)


def inspect_config(data: dict[str, Any]) -> list[ServerReport]:
    servers = server_map(data)
    if not servers:
        raise InspectorError("MCP server map is empty.")
    return [inspect_server(str(name), raw) for name, raw in sorted(servers.items())]


def render_text(reports: list[ServerReport]) -> str:
    lines = [
        "MCP Permission Inspector",
        "STATIC CONFIG REVIEW — not a runtime safety guarantee",
        "",
    ]
    for report in reports:
        lines.append(f"[{report.risk.upper()}] {report.name}")
        lines.append(f"  command: {report.command}")
        lines.append(f"  args: {json.dumps(report.args, ensure_ascii=False)}")
        lines.append(f"  env keys: {', '.join(report.env_keys) if report.env_keys else '(none)'}")
        for finding in report.findings:
            lines.append(f"  - {finding.severity.upper()} {finding.code}: {finding.message}")
            lines.append(f"    fix: {finding.remediation}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="Path to a JSON MCP configuration.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit machine-readable JSON.")
    parser.add_argument("--fail-on", choices=("medium", "high"), help="Return exit code 3 when this risk level or higher is present.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        reports = inspect_config(load_config(args.config))
    except InspectorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.as_json:
        print(json.dumps([asdict(r) for r in reports], indent=2, ensure_ascii=False))
    else:
        print(render_text(reports), end="")

    if args.fail_on:
        threshold = SEVERITY_SCORE[args.fail_on]
        if any(SEVERITY_SCORE[r.risk] >= threshold for r in reports):
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
