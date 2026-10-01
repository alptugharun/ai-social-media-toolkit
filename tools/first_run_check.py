#!/usr/bin/env python3
"""Run the same no-key checks a first-time user should be able to reproduce."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(*args: str) -> str:
    completed = subprocess.run(
        [PYTHON, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Command failed: {PYTHON} {' '.join(args)}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed.stdout


def check(label: str, condition: bool) -> None:
    if not condition:
        raise RuntimeError(f"{label}: expected condition was not met")
    print(f"PASS  {label}")


def main() -> int:
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10+ is required")

    catalog = run("tools/ai_workbench.py", "list")
    check("catalog loads", "evidence-brief" in catalog and "evidence-desk" in catalog)

    rendered = run("tools/ai_workbench.py", "render", "evidence-brief", "--example")
    check("example prompt renders", "S1" in rendered and "S2" in rendered)

    with tempfile.TemporaryDirectory() as tmp:
        request = Path(tmp) / "request.txt"
        request.write_text(rendered, encoding="utf-8")
        preview = run(
            "tools/ai_workbench.py",
            "ask",
            "--provider",
            "xai",
            "--model",
            "demo-model",
            "--input",
            str(request),
        )
        payload = json.loads(preview)
        check(
            "API path stays offline by default",
            payload.get("mode") == "preview" and payload.get("network_called") is False,
        )

        install = run(
            "tools/install_skills.py",
            "--target",
            "agents",
            "--scope",
            "project",
            "--project-root",
            tmp,
            "--skill",
            "creator-ops",
            "--dry-run",
        )
        check("skill install has a dry-run path", "creator-ops" in install)

    for target in ("chatgpt", "claude", "gemini", "grok"):
        exported = run("tools/ai_workbench.py", "export", "evidence-desk", "--target", target)
        check(f"{target} assistant export", len(exported.strip()) > 100)

    demo = run("tools/two_minute_demo.py")
    check("two-minute proof runs", "Two-Minute Proof" in demo and "reel-004" in demo)

    print("\nFIRST-RUN CHECK: PASS")
    print("No API key, network call, account login or third-party Python package was required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
