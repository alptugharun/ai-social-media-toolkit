#!/usr/bin/env python3
"""Validate the human-facing prompt library without third-party dependencies."""

from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_FIELDS = {
    "id", "title", "category", "version", "complexity", "interaction", "models",
}

REQUIRED_HEADINGS = [
    "## Overview",
    "## Use When",
    "## Do Not Use When",
    "## Required Inputs",
    "## Copy/Paste Prompt",
    "## Expected Output",
    "## Quality Gate",
    "## Example Input",
    "## Troubleshooting",
    "## Next Step",
]


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing frontmatter start")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("missing frontmatter end") from exc

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def validate_prompt(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    try:
        fields = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]

    missing = sorted(REQUIRED_FIELDS - set(fields))
    if missing:
        errors.append("missing frontmatter fields: " + ", ".join(missing))

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")

    if "```text" not in text:
        errors.append("missing copyable text block")

    return errors


def prompt_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*.md")
        if path.name not in {"README.md", "PROMPT-STANDARD.md"}
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("prompts"))
    args = parser.parse_args()

    files = prompt_files(args.root)
    if not files:
        print("error: no prompt files found")
        return 2

    failed = False
    for path in files:
        errors = validate_prompt(path)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
