#!/usr/bin/env python3
"""Validate public Markdown navigation without making network requests."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SKIP_PREFIXES = ("#", "http://", "https://", "mailto:", "tel:", "plugin:", "app:", "sandbox:", "data:")


def markdown_files() -> list[Path]:
    ignored = {".git", ".venv", "venv", "node_modules", "dist", "build"}
    files = []
    for path in ROOT.rglob("*.md"):
        parts = path.relative_to(ROOT).parts
        if any(part in ignored for part in parts):
            continue
        files.append(path)
    return files


def visible_lines(path: Path) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    fence: str | None = None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None:
            result.append((number, line))
    return result


def clean_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if " " in target and not target.startswith(("http://", "https://")):
        first, rest = target.split(" ", 1)
        if rest.lstrip().startswith(("\"", "\'", "(")):
            target = first
    return unquote(target)


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    last_heading: tuple[str, int] | None = None
    only_blank_since_heading = False
    for line_no, line in visible_lines(path):
        heading = HEADING_RE.match(line)
        if heading:
            normalized = re.sub(r"\s+", " ", heading.group(2).strip().lower())
            if last_heading and only_blank_since_heading and last_heading[0] == normalized:
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_no}: duplicate consecutive heading {heading.group(2).strip()!r}"
                )
            last_heading = (normalized, line_no)
            only_blank_since_heading = True
        elif line.strip():
            last_heading = None
            only_blank_since_heading = False
        elif last_heading:
            only_blank_since_heading = True

        for match in LINK_RE.finditer(line):
            target = clean_target(match.group(1))
            if not target or target.startswith(SKIP_PREFIXES) or target.startswith("/"):
                continue
            path_part = target.split("#", 1)[0].split("?", 1)[0]
            if not path_part:
                continue
            resolved = (path.parent / path_part).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)}:{line_no}: relative link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}:{line_no}: broken relative link: {target}")
    return errors


def run() -> list[str]:
    errors: list[str] = []
    for path in markdown_files():
        errors.extend(validate_file(path))
    return errors


def main() -> int:
    errors = run()
    if errors:
        print("DOCS VALIDATION FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"DOCS VALIDATION PASS: {len(markdown_files())} Markdown files checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
