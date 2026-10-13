#!/usr/bin/env python3
"""Read-only lexical rewrite review. Not semantic fact checking or AI detection.

Python 3.10+, standard library only. Exit: 0=no tracked change, 1=review,
2=input/configuration error. Source strings are omitted unless explicitly shown.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata
from typing import Sequence

MAX_BYTES = 256 * 1024
MAX_LOCKS = 32
MAX_LOCK_LENGTH = 500
LIMIT = (
    "Lexical comparison only: unchanged tokens do not prove unchanged meaning, "
    "correct facts, preserved attribution, or safe publication. Review the full text."
)
# URL comparison is deliberately literal. A changed query string merits review.
URL = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
# Conservative support, not a multilingual numeric parser. Formatting changes
# are reported rather than guessed equivalent (e.g. 1,500 versus 1.500).
NUMBER = re.compile(
    r"(?<!\w)(?:[$€£₺%][ \t]*)?[vV]?[+\-−]?\d+"
    r"(?:[.,:/\-–]\d+)*"
    r"(?:[ \t]*(?:%|‰|TL|TRY|USD|EUR|GBP|kg|km|cm|mm|mg|ml|g|"
    r"saniye|dakika|saat|gün|seconds?|minutes?|hours?|days?|sn|dk))?"
    r"(?!\w)", re.IGNORECASE
)


def normalize(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("Expected text strings.")
    if len(text) > MAX_BYTES or len(text.encode("utf-8")) > MAX_BYTES:
        raise ValueError("Each input must be at most 256 KiB of UTF-8 text.")
    if "\x00" in text:
        raise ValueError("NUL bytes are not accepted; use plain UTF-8 text.")
    text = unicodedata.normalize("NFC", text.removeprefix("\ufeff"))
    if not text.strip():
        raise ValueError("Both drafts must contain text.")
    return text


def token_counts(text: str) -> dict[str, Counter[str]]:
    urls = list(URL.finditer(text))
    # Keep offsets unchanged; numbers inside URLs are not a second finding.
    chars = list(text)
    url_counts: Counter[str] = Counter()
    for match in urls:
        token = match.group().rstrip(".,;!?)")
        if token:
            url_counts[token] += 1
        chars[match.start():match.end()] = " " * (match.end() - match.start())
    return {"url": url_counts, "numeric": Counter(m.group() for m in NUMBER.finditer("".join(chars)))}


def compare(before: str, after: str, locks: Sequence[str] = (), *, show_values: bool = False) -> dict:
    """Report lexical deltas and exact protected-span occurrence changes.

    Locks must exist in the original. They are literal and case-sensitive.
    No network, model calls, source modification, or silent auto-correction.
    """
    before, after = normalize(before), normalize(after)
    if isinstance(locks, (str, bytes)) or len(locks) > MAX_LOCKS:
        raise ValueError("Provide at most 32 separate exact protected spans.")
    clean_locks: list[str] = []
    for lock in locks:
        if not isinstance(lock, str) or not lock.strip() or len(lock) > MAX_LOCK_LENGTH:
            raise ValueError("Each protected span must contain 1–500 characters.")
        lock = unicodedata.normalize("NFC", lock)
        if "\x00" in lock or lock not in before:
            raise ValueError("A protected span is absent from the original; check its exact spelling.")
        if lock not in clean_locks:
            clean_locks.append(lock)
    old, new = token_counts(before), token_counts(after)
    old["locked_text"] = Counter({x: before.count(x) for x in clean_locks})
    new["locked_text"] = Counter({x: after.count(x) for x in clean_locks})
    findings = []
    for kind in ("numeric", "url", "locked_text"):
        for token in sorted(set(old[kind]) | set(new[kind])):
            left, right = old[kind][token], new[kind][token]
            if left == right:
                continue
            item = {"id": len(findings) + 1, "kind": kind, "before_count": left, "after_count": right}
            if show_values:
                item["value"] = token
            findings.append(item)
    return {
        "schema_version": 1,
        "status": "REVIEW_REQUIRED" if findings else "NO_TRACKED_CHANGE",
        "findings": findings,
        "tracked": {"numeric_before": sum(old["numeric"].values()), "urls_before": sum(old["url"].values()), "protected_spans": len(clean_locks)},
        "values_included": bool(show_values),
        "limitation": LIMIT,
    }


def read_text(path: Path) -> str:
    # Reject directories and special files. Does not claim filesystem sandboxing.
    if not path.is_file() or path.is_symlink():
        raise ValueError("Input must be an existing regular file, not a directory or symlink.")
    with path.open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Input exceeds 256 KiB; compare one section at a time.")
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("Input must use UTF-8 encoding.") from exc


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare rewrite tokens locally; this is not a truth or AI-authorship detector.")
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--lock", action="append", default=[], help="Exact protected text from the original; repeat as needed. Never pass secrets.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--show-values", action="store_true", help="Include literal findings. Use only with non-sensitive examples; logs may capture output.")
    args = parser.parse_args(argv)
    try:
        report = compare(read_text(args.before), read_text(args.after), args.lock, show_values=args.show_values)
    except (ValueError, OSError) as exc:
        # Do not echo source paths, protected text or OSError filenames.
        message = str(exc) if isinstance(exc, ValueError) else "Unable to read an input file. Check local permissions."
        print(json.dumps({"status": "INPUT_ERROR", "message": message}, ensure_ascii=True), file=sys.stderr)
        return 2
    if args.format == "json":
        # ASCII escaping makes output independent of Windows console encoding.
        print(json.dumps(report, ensure_ascii=True, indent=2))
    else:
        print(report["status"])
        print("Changed items:", len(report["findings"]))
        for item in report["findings"]:
            suffix = " " + json.dumps(item["value"], ensure_ascii=True) if args.show_values else ""
            print(f"- #{item['id']} {item['kind']}: {item['before_count']} -> {item['after_count']}{suffix}")
        print(LIMIT)
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
