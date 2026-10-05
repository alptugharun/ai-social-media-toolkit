#!/usr/bin/env python3
"""Static, local-first risk review for MCP client configuration.

This tool does not launch servers, contact the network, or prove runtime safety.
It inspects configuration shape and reports bounded heuristics.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

CREDENTIAL_KEY_RE = re.compile(r"(token|secret|password|passwd|api[_-]?key|credential|private[_-]?key|access[_-]?key|database[_-]?url|dsn|connection[_-]?string|cookie|authorization)", re.I)
PLACEHOLDER_RE = re.compile(r"^(?:\$\{[^}]+\}|\$[A-Za-z_][A-Za-z0-9_]*|%[A-Za-z_][A-Za-z0-9_]*%)$")
HEADER_PLACEHOLDER_RE = re.compile(r"^(?:(?:Bearer|Basic|Token)\s+)?(?:\$\{[^}]+\}|\$[A-Za-z_][A-Za-z0-9_]*|%[A-Za-z_][A-Za-z0-9_]*%)$", re.I)
EXECUTION_ENV_KEYS = {
    "LD_PRELOAD", "LD_LIBRARY_PATH", "DYLD_INSERT_LIBRARIES",
    "DYLD_LIBRARY_PATH", "NODE_OPTIONS", "PYTHONPATH", "PYTHONSTARTUP",
    "RUBYOPT", "PERL5OPT", "BASH_ENV", "ENV", "PROMPT_COMMAND",
}
MAX_CONFIG_BYTES = 5_000_000
MAX_SERVERS = 10_000
MAX_ARGS_PER_SERVER = 10_000
URL_RE = re.compile(r"https?://", re.I)
ABS_PATH_RE = re.compile(r"^(?:[A-Za-z]:[\\/]|/)")
SHELLS = {"bash", "bash.exe", "sh", "sh.exe", "zsh", "zsh.exe", "fish", "fish.exe", "cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "pwsh.exe"}
RUNNERS = {"npx", "npx.cmd", "npx.exe", "uvx", "uvx.exe", "pipx", "pipx.exe", "bunx", "bunx.exe", "pnpx", "pnpx.cmd", "pnpx.exe"}
SHELL_FLAGS = {"-c", "/c", "-command", "-encodedcommand"}
SHELL_META_ARGS = {"&&", "||", ";", "|"}
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
    transport: str
    command: str | None
    url: str | None
    args: list[str]
    env_keys: list[str]
    header_keys: list[str]
    risk: str
    findings: list[Finding]


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise InspectorError(f"Duplicate JSON key is ambiguous: {key!r}.")
        obj[key] = value
    return obj


def load_config(path: Path) -> dict[str, Any]:
    try:
        size = path.stat().st_size
        if size > MAX_CONFIG_BYTES:
            raise InspectorError(
                f"Config is too large ({size} bytes); limit is {MAX_CONFIG_BYTES} bytes."
            )
        data = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_no_duplicate_keys,
        )
    except InspectorError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise InspectorError(f"Could not read valid UTF-8 JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise InspectorError("Top-level MCP config must be a JSON object.")
    return data


def server_map(data: dict[str, Any]) -> dict[str, Any]:
    for key in ("mcpServers", "servers", "context_servers"):
        value = data.get(key)
        if isinstance(value, dict):
            if len(value) > MAX_SERVERS:
                raise InspectorError(
                    f"MCP server map has {len(value)} entries; limit is {MAX_SERVERS}."
                )
            return value
    if "command" in data or "url" in data:
        return {"server": data}
    raise InspectorError(
        "No MCP server map found. Expected 'mcpServers', 'servers', "
        "'context_servers', or a single server object with command/url."
    )


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(
        isinstance(x, (str, int, float, bool)) for x in value
    ):
        raise InspectorError("Server 'args' must be a list of scalar values.")
    if len(value) > MAX_ARGS_PER_SERVER:
        raise InspectorError(
            f"Server args contain {len(value)} entries; limit is {MAX_ARGS_PER_SERVER}."
        )
    return [str(x) for x in value]


def _mapping(value: Any, label: str, name: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise InspectorError(f"Server '{name}' {label} must be an object.")
    return value


def _redact_url(value: str) -> str:
    try:
        parts = urlsplit(value)
    except ValueError:
        return "<invalid-url>"
    if parts.scheme.lower() not in {"http", "https"}:
        return value

    netloc = parts.netloc
    if "@" in netloc:
        netloc = "<redacted-userinfo>@" + netloc.rsplit("@", 1)[1]

    query = [
        (key, "<redacted>" if CREDENTIAL_KEY_RE.search(key) else val)
        for key, val in parse_qsl(parts.query, keep_blank_values=True)
    ]
    return urlunsplit(
        (parts.scheme, netloc, parts.path, urlencode(query), parts.fragment)
    )


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
            key, _value = arg.split("=", 1)
            if CREDENTIAL_KEY_RE.search(key):
                redacted.append(key + "=<redacted>")
                continue

        if arg.startswith("-") and CREDENTIAL_KEY_RE.search(arg):
            redacted.append(arg)
            redact_next = True
            continue

        redacted.append(arg)
    return redacted


def _is_placeholder(value: Any) -> bool:
    return isinstance(value, str) and bool(
        PLACEHOLDER_RE.fullmatch(value.strip())
    )


def _is_header_placeholder(value: Any) -> bool:
    return isinstance(value, str) and bool(
        HEADER_PLACEHOLDER_RE.fullmatch(value.strip())
    )


def _credential_keys(mapping: dict[str, Any]) -> list[str]:
    return sorted(
        str(key) for key in mapping if CREDENTIAL_KEY_RE.search(str(key))
    )


def _hardcoded_credential_keys(
    mapping: dict[str, Any],
    *,
    header_mode: bool = False,
) -> list[str]:
    result: list[str] = []
    for key, value in mapping.items():
        if not CREDENTIAL_KEY_RE.search(str(key)):
            continue
        if value in (None, ""):
            continue
        placeholder = (
            _is_header_placeholder(value)
            if header_mode
            else _is_placeholder(value)
        )
        if placeholder:
            continue
        result.append(str(key))
    return sorted(result)


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


def _runner_family(cmd_name: str) -> str:
    for suffix in (".cmd", ".exe"):
        if cmd_name.endswith(suffix):
            return cmd_name[: -len(suffix)]
    return cmd_name


def _looks_unpinned_package(runner: str, arg: str) -> bool:
    if not arg or arg.startswith("-") or arg == "<redacted>" or URL_RE.search(arg):
        return False

    if runner in {"npx", "bunx", "pnpx"}:
        if arg.endswith("@latest"):
            return True
        if arg.startswith("@"):
            return arg.count("@") == 1
        return "@" not in arg

    if runner in {"uvx", "pipx"}:
        if arg.endswith("@latest"):
            return True
        if "==" in arg:
            return False
        if re.search(r"@[0-9][A-Za-z0-9_.+-]*$", arg):
            return False
        return bool(re.fullmatch(r"[A-Za-z0-9_.-]+", arg))

    return False


def _is_loopback_hostname(hostname: str | None) -> bool:
    if not hostname:
        return False
    host = hostname.strip("[]").lower()
    if host in {"localhost", "ip6-localhost"}:
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def inspect_server(name: str, raw: Any) -> ServerReport:
    if not isinstance(raw, dict):
        raise InspectorError(f"Server '{name}' must be an object.")

    command = str(raw.get("command", "")).strip() or None
    url = str(raw.get("url", "")).strip() or None
    if not command and not url:
        raise InspectorError(f"Server '{name}' has neither command nor url.")

    args = _string_list(raw.get("args"))
    env = _mapping(raw.get("env"), "env", name)
    headers = _mapping(raw.get("headers"), "headers", name)
    env_keys = sorted(str(k) for k in env)
    header_keys = sorted(str(k) for k in headers)
    reported_args = _redact_args(args)
    findings: list[Finding] = []

    transport_hint = str(
        raw.get("transport") or raw.get("type") or ""
    ).strip().lower()
    if command and url:
        transport = transport_hint or "mixed"
        findings.append(
            Finding(
                "medium",
                "mixed-transport-config",
                "Configuration contains both a local command and a remote URL.",
                "Confirm which transport the client uses and remove the unused launch path.",
            )
        )
    elif url:
        transport = transport_hint or "http"
    else:
        transport = transport_hint or "stdio"

    cmd_name = (
        Path(command.replace("\\", "/")).name.lower() if command else ""
    )
    runner = _runner_family(cmd_name)
    lowered = [arg.lower() for arg in reported_args]

    if cmd_name in SHELLS:
        findings.append(
            Finding(
                "high",
                "shell-execution",
                f"Server is launched through a general-purpose shell: {cmd_name}.",
                "Prefer launching the MCP executable directly; remove shell indirection unless strictly required.",
            )
        )

    if any(arg in SHELL_FLAGS for arg in lowered):
        findings.append(
            Finding(
                "high",
                "shell-command-flag",
                "Arguments contain a shell command/evaluation flag.",
                "Replace inline shell evaluation with a direct executable and explicit argument list.",
            )
        )

    meta_args = sorted({arg for arg in reported_args if arg in SHELL_META_ARGS})
    if meta_args and cmd_name not in SHELLS:
        findings.append(
            Finding(
                "medium",
                "shell-metacharacter-argument",
                "Arguments contain shell metacharacters: " + ", ".join(meta_args) + ".",
                "They are normally literal argv values; verify the host/launcher never concatenates them into a shell command.",
            )
        )

    dangerous_env_keys = sorted(
        key for key in env_keys if key.upper() in EXECUTION_ENV_KEYS
    )
    if dangerous_env_keys:
        findings.append(
            Finding(
                "high",
                "execution-env-injection",
                "Environment keys can alter process/module loading: "
                + ", ".join(dangerous_env_keys)
                + ". Values are never displayed.",
                "Remove execution-influencing environment overrides unless they are explicitly required and reviewed.",
            )
        )

    env_credential_keys = _credential_keys(env)
    hardcoded_env = _hardcoded_credential_keys(env)
    if hardcoded_env:
        findings.append(
            Finding(
                "high",
                "hardcoded-env-credential",
                "Sensitive environment keys contain literal values: "
                + ", ".join(hardcoded_env)
                + ". Values are never displayed.",
                "Replace literal credentials with placeholders/host secret storage and rotate real exposed credentials.",
            )
        )
    elif env_credential_keys:
        findings.append(
            Finding(
                "medium",
                "sensitive-env-boundary",
                "Configuration references sensitive environment keys: "
                + ", ".join(env_credential_keys)
                + ". Values are never displayed.",
                "Use least-privilege, short-lived credentials and keep secret values outside committed config.",
            )
        )

    header_credential_keys = _credential_keys(headers)
    hardcoded_headers = _hardcoded_credential_keys(headers, header_mode=True)
    if hardcoded_headers:
        findings.append(
            Finding(
                "high",
                "hardcoded-header-credential",
                "Sensitive HTTP header keys contain literal values: "
                + ", ".join(hardcoded_headers)
                + ". Values are never displayed.",
                "Use placeholders/OAuth/host secret storage instead of literal credentials in configuration.",
            )
        )
    elif header_credential_keys:
        findings.append(
            Finding(
                "medium",
                "sensitive-header-boundary",
                "Configuration references sensitive HTTP header keys: "
                + ", ".join(header_credential_keys)
                + ". Values are never displayed.",
                "Verify token audience/scope and prefer short-lived credentials.",
            )
        )

    reported_url: str | None = None
    if url:
        reported_url = _redact_url(url)
        try:
            parts = urlsplit(url)
        except ValueError:
            parts = None

        if (
            parts is None
            or parts.scheme.lower() not in {"http", "https"}
            or not parts.hostname
        ):
            findings.append(
                Finding(
                    "high",
                    "invalid-remote-url",
                    "Remote MCP URL is not a valid HTTP(S) endpoint.",
                    "Use a valid HTTPS endpoint, or loopback HTTP only for local development.",
                )
            )
        elif parts.scheme.lower() == "http" and not _is_loopback_hostname(
            parts.hostname
        ):
            findings.append(
                Finding(
                    "high",
                    "cleartext-remote",
                    "Remote MCP endpoint uses cleartext HTTP outside loopback.",
                    "Use HTTPS for non-loopback remote MCP endpoints.",
                )
            )
        elif parts.scheme.lower() == "http":
            findings.append(
                Finding(
                    "low",
                    "loopback-http",
                    "Remote MCP endpoint uses HTTP on loopback.",
                    "Keep it loopback-only; use HTTPS when traffic leaves the local machine.",
                )
            )
        else:
            findings.append(
                Finding(
                    "medium",
                    "remote-network-boundary",
                    "Configuration connects to a remote HTTPS MCP endpoint.",
                    "Verify endpoint ownership, authentication, requested scopes and data handling before connecting.",
                )
            )

    if any(URL_RE.search(arg) for arg in reported_args):
        findings.append(
            Finding(
                "medium",
                "network-target-argument",
                "Arguments contain an HTTP(S) target, so the local launcher may bridge to a network service.",
                "Verify the destination, authentication boundary and data flow before enabling the server.",
            )
        )

    path_args = [arg for arg in reported_args if ABS_PATH_RE.search(arg)]
    broad = [arg for arg in path_args if _is_broad_path(arg)]
    if broad:
        findings.append(
            Finding(
                "high",
                "broad-filesystem-path",
                "Arguments appear to expose a broad filesystem root: "
                + ", ".join(broad)
                + ".",
                "Scope filesystem access to the smallest project/workspace directory required.",
            )
        )
    elif path_args:
        findings.append(
            Finding(
                "low",
                "filesystem-path",
                "Arguments contain absolute filesystem paths.",
                "Confirm each path is required and avoid parent/home/root directories when a narrower workspace works.",
            )
        )

    if runner in {"npx", "uvx", "pipx", "bunx", "pnpx"}:
        findings.append(
            Finding(
                "low",
                "package-runner",
                f"Server is launched through package runner '{cmd_name}'.",
                "For repeatable installs, prefer an exact reviewed package version.",
            )
        )
        if "-y" in lowered or "--yes" in lowered:
            findings.append(
                Finding(
                    "medium",
                    "auto-install",
                    "Package runner is allowed to auto-confirm installation.",
                    "Pin the package version and consider installing it explicitly before host startup.",
                )
            )

        package_arg = None
        if not any(flag in lowered for flag in SHELL_FLAGS):
            package_arg = next(
                (
                    arg
                    for arg in reported_args
                    if arg
                    and not arg.startswith("-")
                    and arg != "<redacted>"
                    and not URL_RE.search(arg)
                ),
                None,
            )
        unpinned = (
            [package_arg]
            if package_arg is not None
            and _looks_unpinned_package(runner, package_arg)
            else []
        )
        if unpinned:
            findings.append(
                Finding(
                    "medium",
                    "unpinned-package",
                    "Package runner appears to reference an unpinned package: "
                    + ", ".join(unpinned[:3])
                    + ".",
                    "Pin an exact reviewed version for reproducible host configuration.",
                )
            )

    if not findings:
        findings.append(
            Finding(
                "info",
                "no-obvious-static-risk",
                "No obvious high-risk pattern was found in this configuration snippet.",
                "Still verify upstream source/version, runtime behavior, host permissions and the first tool call.",
            )
        )

    risk = max(
        (finding.severity for finding in findings),
        key=lambda severity: SEVERITY_SCORE[severity],
    )
    return ServerReport(
        name=name,
        transport=transport,
        command=command,
        url=reported_url,
        args=reported_args,
        env_keys=env_keys,
        header_keys=header_keys,
        risk=risk,
        findings=findings,
    )


def inspect_config(data: dict[str, Any]) -> list[ServerReport]:
    servers = server_map(data)
    if not servers:
        raise InspectorError("MCP server map is empty.")
    return [inspect_server(str(name), raw) for name, raw in sorted(servers.items())]


def render_text(reports: list[ServerReport]) -> str:
    lines = [
        "MCP Permission Inspector",
        "STATIC CONFIG REVIEW - not a runtime safety guarantee",
        "",
    ]
    for report in reports:
        lines.append(f"[{report.risk.upper()}] {report.name} ({report.transport})")
        if report.command:
            lines.append(f"  command: {report.command}")
        if report.url:
            lines.append(f"  url: {report.url}")
        if report.args:
            lines.append(
                f"  args: {json.dumps(report.args, ensure_ascii=False)}"
            )
        lines.append(
            f"  env keys: {', '.join(report.env_keys) if report.env_keys else '(none)'}"
        )
        lines.append(
            f"  header keys: {', '.join(report.header_keys) if report.header_keys else '(none)'}"
        )
        for finding in report.findings:
            lines.append(
                f"  - {finding.severity.upper()} {finding.code}: "
                f"{finding.message}"
            )
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
