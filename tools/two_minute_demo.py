#!/usr/bin/env python3
"""Run a dependency-free two-minute proof demo for AI Social Media Toolkit.

The demo uses repository-owned synthetic example data. It does not call external
APIs, publish content, or claim that the sample metrics are real creator results.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
TOOLS = ROOT / "tools"


def run_tool(script: str, *args: str) -> str:
    command = [sys.executable, str(TOOLS / script), *args]
    result = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def parse_csv(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(text.splitlines()))


def own_data_steps(example: str, contract: str, columns: str, script: str, filename: str) -> list[str]:
    base = "https://github.com/alptugharun/ai-social-media-toolkit/blob/main/"
    copy_command = 'python -c "from pathlib import Path; Path(\'../{filename}\').open(\'xb\').write(Path(\'{example}\').read_bytes())"'.format(example=example, filename=filename)
    return [
        "", "### Use your own data", "",
        f"Sample CSV: `{example}`",
        f"Input contract: [{contract}]({base}{contract})", "",
        "Required columns (keep these exact names):", "", "```csv", columns, "```", "",
        "Copy the sample outside the repository. Run this once from the repository root:",
        "", "```bash", copy_command, "```", "",
        f"Edit `../{filename}` with your own data, preserving the header. Then run:",
        "", "```bash",
        f'python tools/{script} "../{filename}" --validate-only',
        f'python tools/{script} "../{filename}" --top 3',
        "```", "",
        "The copy refuses to overwrite an existing file; use another filename if needed.",
        "Output: validation summary, then ranked CSV in the terminal. Scoring never changes input files.",
        f"For errors, open `{contract}`. Do not commit private exports. These are not raw platform-export schemas.",
    ]


def render() -> str:
    opportunities = parse_csv(
        run_tool("signal2content_score.py", str(EXAMPLES / "signal2content-opportunities.csv"), "--top", "3")
    )
    outliers = parse_csv(
        run_tool("outlier_score.py", str(EXAMPLES / "social-outlier-posts.csv"), "--top", "3")
    )

    lines = [
        "# AI Social Media Toolkit — Two-Minute Proof",
        "",
        "> Demo data is synthetic and exists only to show the workflow. It is not Alptuğ Harun\'s real social performance.",
        "",
        "## Proof 1 — Which content opportunity should go first?",
        "",
        "The Signal-to-Content scorer ranks opportunities using explicit evidence, audience-fit, freshness, repeatability, production-ease and saturation inputs.",
        "",
        "| Rank | Opportunity | Score |",
        "| ---: | --- | ---: |",
    ]
    for row in opportunities:
        lines.append("| {rank} | {name} | **{score:.2f}** |".format(rank=row["rank"], name=row["name"], score=float(row["score"])))
    if opportunities:
        top = opportunities[0]
        lines += ["", "**Decision:** start by reviewing **{}**. The score is a prioritization heuristic, not a virality prediction.".format(top["name"])]

    lines += own_data_steps(
        "examples/signal2content-opportunities.csv",
        "docs/CSV-INPUTS.md#content-opportunities",
        "name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation",
        "signal2content_score.py", "opportunities.csv",
    )

    lines += [
        "",
        "## Proof 2 — Which post actually broke the creator\'s baseline?",
        "",
        "The Social Outlier Analyzer compares posts with the median performance of the supplied dataset.",
        "",
        "| Rank | Platform | Post | Outlier score | Views vs median | Engagement vs median |",
        "| ---: | --- | --- | ---: | ---: | ---: |",
    ]
    for row in outliers:
        lines.append(
            "| {rank} | {platform} | {post_id} | **{score:.2f}** | {views:.2f}× | {engagement:.2f}× |".format(
                rank=row["rank"],
                platform=row["platform"],
                post_id=row["post_id"],
                score=float(row["outlier_score"]),
                views=float(row["view_multiple"]),
                engagement=float(row["engagement_multiple"]),
            )
        )
    if outliers:
        winner = outliers[0]
        lines += [
            "",
            "**Decision:** inspect **{}** first. It reached **{:.2f}×** the dataset median views. The next step is qualitative analysis, not blind duplication.".format(winner["post_id"], float(winner["view_multiple"])),
        ]

    lines += own_data_steps(
        "examples/social-outlier-posts.csv",
        "docs/CSV-INPUTS.md#social-posts",
        "platform,post_id,views,likes,comments,shares,saves",
        "outlier_score.py", "posts.csv",
    )

    lines += [
        "",
        "## What this proves",
        "",
        "- The repository contains runnable decision tools, not only prompt files.",
        "- Inputs and scoring logic are inspectable.",
        "- The demo runs without third-party Python packages.",
        "- Results stay separated from claims about future reach, virality or revenue.",
        "",
        "## Try your own data",
        "",
        "Follow the sample, columns, validation command and contract printed directly after each proof.",
        "",
        "For an end-to-end Reels example, continue with examples/workflows/reels-from-outlier.md.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    try:
        report = render()
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or str(exc), file=sys.stderr)
        return exc.returncode or 1
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
