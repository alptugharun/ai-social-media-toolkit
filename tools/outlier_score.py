#!/usr/bin/env python3
"""Rank social posts against a creator's own baseline.

Dependency-free by design. Input CSV columns:
platform,post_id,views,likes,comments,shares,saves

The scorer uses median-normalized engagement and reach so one viral post does not
inflate the baseline. It is a research aid, not a claim about algorithmic ranking.
"""

from __future__ import annotations

import argparse
import csv
import statistics
from pathlib import Path

METRICS = ("views", "likes", "comments", "shares", "saves")
WEIGHTS = {"views": 0.25, "likes": 0.20, "comments": 0.20, "shares": 0.20, "saves": 0.15}


def number(value: str) -> float:
    try:
        return max(0.0, float(value or 0))
    except (TypeError, ValueError):
        return 0.0


def score_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    if not rows:
        return []

    baselines = {}
    for metric in METRICS:
        values = [number(row.get(metric, "0")) for row in rows]
        baselines[metric] = statistics.median(values) or 1.0

    scored = []
    for row in rows:
        ratios = {metric: number(row.get(metric, "0")) / baselines[metric] for metric in METRICS}
        score = sum(min(ratios[m], 10.0) * WEIGHTS[m] for m in METRICS)
        scored.append({
            **row,
            "outlier_score": round(score, 2),
            "view_multiple": round(ratios["views"], 2),
            "engagement_multiple": round(
                sum(ratios[m] for m in ("likes", "comments", "shares", "saves")) / 4, 2
            ),
        })

    return sorted(scored, key=lambda item: float(item["outlier_score"]), reverse=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank social posts against their own median baseline.")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--top", type=int, default=10, help="Number of ranked posts to print")
    args = parser.parse_args()

    with args.csv_file.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    ranked = score_rows(rows)[: max(1, args.top)]
    writer = csv.DictWriter(
        __import__("sys").stdout,
        fieldnames=["rank", "platform", "post_id", "outlier_score", "view_multiple", "engagement_multiple"],
    )
    writer.writeheader()
    for rank, row in enumerate(ranked, 1):
        writer.writerow({"rank": rank, **{k: row.get(k, "") for k in writer.fieldnames if k != "rank"}})


if __name__ == "__main__":
    main()
