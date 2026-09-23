#!/usr/bin/env python3
"""Rank content opportunities with a transparent, editable heuristic.

CSV input columns:
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation

All numeric inputs are 0-100.

Score:
0.30*evidence_strength
+ 0.25*audience_fit
+ 0.20*freshness
+ 0.15*repeatability
+ 0.10*production_ease
- 0.15*saturation

The final score is clamped to 0-100.

This is a prioritization heuristic, not a prediction model.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

FIELDS = (
    "evidence_strength",
    "audience_fit",
    "freshness",
    "repeatability",
    "production_ease",
    "saturation",
)


def bounded_number(value: str, field: str) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be numeric, got {value!r}") from exc
    if not 0 <= number <= 100:
        raise ValueError(f"{field} must be between 0 and 100, got {number}")
    return number


def score_row(row: dict[str, str]) -> float:
    values = {field: bounded_number(row[field], field) for field in FIELDS}
    score = (
        0.30 * values["evidence_strength"]
        + 0.25 * values["audience_fit"]
        + 0.20 * values["freshness"]
        + 0.15 * values["repeatability"]
        + 0.10 * values["production_ease"]
        - 0.15 * values["saturation"]
    )
    return max(0.0, min(100.0, score))


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header")
        required = {"name", *FIELDS}
        missing = required.difference(reader.fieldnames)
        if missing:
            raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
        return list(reader)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rank trend/content opportunities with the Signal to Content heuristic."
    )
    parser.add_argument("csv_file", type=Path, help="Input CSV file")
    parser.add_argument(
        "--top",
        type=int,
        default=0,
        help="Return only the top N rows (0 = all)",
    )
    args = parser.parse_args()

    try:
        rows = load_rows(args.csv_file)
        scored = [(row, score_row(row)) for row in rows]
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    scored.sort(key=lambda item: item[1], reverse=True)
    if args.top > 0:
        scored = scored[: args.top]

    writer = csv.writer(sys.stdout)
    writer.writerow(["rank", "name", "score"])
    for rank, (row, score) in enumerate(scored, start=1):
        writer.writerow([rank, row["name"], f"{score:.2f}"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
