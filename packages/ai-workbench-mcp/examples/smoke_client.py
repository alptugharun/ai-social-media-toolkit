#!/usr/bin/env python3
"""Run one deterministic smoke check against the installed AI Workbench MCP."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys

COMMAND = "alptugharun-ai-workbench-mcp"
PROTOCOL_VERSION = "2025-06-18"
EXPECTED_TOOLS = {"list_prompts", "render_prompt", "get_assistant"}


def build_messages() -> list[dict]:
    return [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": PROTOCOL_VERSION},
        },
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    ]


def parse_output(stdout: str) -> tuple[dict, dict]:
    lines = [line for line in stdout.splitlines() if line.strip()]
    if len(lines) != 2:
        raise ValueError(f"expected 2 JSON-RPC responses, got {len(lines)}")
    initialized, listed = (json.loads(line) for line in lines)
    return initialized, listed


def verify(initialized: dict, listed: dict) -> list[str]:
    server = initialized.get("result", {}).get("serverInfo", {})
    if server.get("name") != "alptugharun-ai-workbench-mcp":
        raise ValueError(f"unexpected server name: {server.get('name')!r}")

    tools = listed.get("result", {}).get("tools")
    if not isinstance(tools, list):
        raise ValueError("tools/list did not return a tool list")

    names = {tool.get("name") for tool in tools}
    if names != EXPECTED_TOOLS:
        raise ValueError(f"unexpected tools: {sorted(str(name) for name in names)}")

    for tool in tools:
        annotations = tool.get("annotations", {})
        expected = {
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
        for key, value in expected.items():
            if annotations.get(key) is not value:
                raise ValueError(f"{tool.get('name')}: unexpected {key}")

    return sorted(names)


def main() -> int:
    executable = shutil.which(COMMAND)
    if not executable:
        print(
            f"MCP SMOKE FAIL: {COMMAND!r} is not installed or not on PATH.",
            file=sys.stderr,
        )
        return 2

    payload = "\n".join(json.dumps(message) for message in build_messages()) + "\n"
    try:
        result = subprocess.run(
            [executable],
            input=payload,
            text=True,
            capture_output=True,
            timeout=10,
            encoding="utf-8",
        )
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"MCP SMOKE FAIL: could not run server: {exc}", file=sys.stderr)
        return 2

    if result.returncode != 0:
        print(
            f"MCP SMOKE FAIL: server exited {result.returncode}: {result.stderr.strip()}",
            file=sys.stderr,
        )
        return result.returncode or 2

    try:
        initialized, listed = parse_output(result.stdout)
        names = verify(initialized, listed)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"MCP SMOKE FAIL: {exc}", file=sys.stderr)
        return 1

    print("MCP SMOKE PASS")
    print(f"- server: {initialized['result']['serverInfo']['name']}")
    print(f"- version: {initialized['result']['serverInfo']['version']}")
    print(f"- tools: {', '.join(names)}")
    print("- side-effects: read-only contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
