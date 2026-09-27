#!/usr/bin/env python3
"""Generate a focus and traction report for the repository.

The report uses public GitHub metadata as weak adoption signals and deliberately
separates internal activity from external proof.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = "alptugharun/ai-social-media-toolkit"
OWNER = "alptugharun"
USER_AGENT = "ai-social-media-toolkit-focus-traction/0.1"


def request(url: str, token: str | None = None) -> urllib.request.Request:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return urllib.request.Request(url, headers=headers)


def fetch_json(url: str, token: str | None = None):
    with urllib.request.urlopen(request(url, token), timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def collect(token: str | None) -> dict:
    repo = fetch_json(f"https://api.github.com/repos/{REPO}", token)

    releases = fetch_json(
        f"https://api.github.com/repos/{REPO}/releases?per_page=20", token
    )
    issues = fetch_json(
        f"https://api.github.com/repos/{REPO}/issues?state=all&per_page=100", token
    )
    contributors = fetch_json(
        f"https://api.github.com/repos/{REPO}/contributors?per_page=100", token
    )

    real_issues = [item for item in issues if "pull_request" not in item]
    def is_external_human(user: dict) -> bool:
        login = (user or {}).get("login", "").lower()
        user_type = (user or {}).get("type", "")
        return (
            bool(login)
            and login != OWNER.lower()
            and not login.endswith("[bot]")
            and user_type.lower() != "bot"
        )

    external_issue_count = sum(
        1
        for item in real_issues
        if is_external_human(item.get("user") or {})
    )
    external_contributors = [
        item
        for item in contributors
        if is_external_human(item)
    ]

    return {
        "stars": int(repo.get("stargazers_count", 0)),
        "forks": int(repo.get("forks_count", 0)),
        "subscribers": int(repo.get("subscribers_count", 0)),
        "open_issues": int(repo.get("open_issues_count", 0)),
        "release_count": len(releases) if isinstance(releases, list) else 0,
        "external_issue_count_sample": external_issue_count,
        "external_contributor_count_sample": len(external_contributors),
        "has_discussions": bool(repo.get("has_discussions", False)),
        "pushed_at": repo.get("pushed_at", ""),
    }


def focus_state(metrics: dict) -> tuple[str, list[str]]:
    proof = 0
    reasons: list[str] = []

    if metrics["stars"] > 1:
        proof += 1
        reasons.append("more than the creator's initial star signal is visible")
    if metrics["forks"] > 0:
        proof += 1
        reasons.append("at least one fork is visible")
    if metrics["external_issue_count_sample"] > 0:
        proof += 1
        reasons.append("external issue participation is visible")
    if metrics["external_contributor_count_sample"] > 0:
        proof += 2
        reasons.append("external contributor activity is visible")
    if metrics["release_count"] > 0:
        proof += 1
        reasons.append("the repository has release packaging")

    if proof >= 4:
        return "SCALE WHAT WORKS", reasons
    if proof >= 2:
        return "VALIDATE WEDGE", reasons
    return "BUILD PROOF", reasons


def render(metrics: dict) -> str:
    now = datetime.now(timezone.utc)
    state, reasons = focus_state(metrics)

    lines = [
        "# Traction & Focus Watch",
        "",
        f"Generated: **{now.strftime('%Y-%m-%d %H:%M UTC')}**",
        "",
        "> GitHub activity is not treated as revenue or product-market fit. This report separates internal shipping from external adoption proof.",
        "",
        "## Current Public Signals",
        "",
        "| Signal | Current value | Interpretation |",
        "| --- | ---: | --- |",
        f'| Stars | {metrics["stars"]} | weak interest / discovery signal |',
        f'| Forks | {metrics["forks"]} | reuse / experimentation signal when non-zero |',
        f'| Subscribers | {metrics["subscribers"]} | watch signal |',
        f'| Open issues | {metrics["open_issues"]} | activity signal; not automatically external adoption |',
        f'| Releases | {metrics["release_count"]} | packaging / distribution signal |',
        f'| External issues in latest sample | {metrics["external_issue_count_sample"]} | external participation signal |',
        f'| External contributors in latest sample | {metrics["external_contributor_count_sample"]} | stronger external adoption signal |',
        "",
        f"## Focus State: **{state}**",
        "",
    ]

    if reasons:
        lines.append("Observed proof signals:")
        lines.extend([f"- {reason}" for reason in reasons])
    else:
        lines.append(
            "No strong external proof signal is visible in the sampled GitHub metadata yet."
        )

    lines.extend(
        [
            "",
            "## Build Decision",
            "",
        ]
    )

    if state == "BUILD PROOF":
        lines.extend(
            [
                "- Prefer improving existing skills over adding new lanes.",
                "- Prioritize quick starts, working examples, demos and case studies.",
                "- Push distribution and real-user testing before expanding the skill count.",
                "- Keep Pinterest, Maps and commercial research as supporting creator-ops lanes unless one earns stronger external proof.",
            ]
        )
    elif state == "VALIDATE WEDGE":
        lines.extend(
            [
                "- Identify the workflow creating the strongest repeated external use.",
                "- Run a narrow user / buyer test around that workflow.",
                "- Measure repeat usage before building a hosted product.",
                "- Merge or deprioritize weak adjacent lanes.",
            ]
        )
    else:
        lines.extend(
            [
                "- Package the strongest proven workflow more deeply.",
                "- Add hosted convenience only where repeated use is visible.",
                "- Consider Marketplace / Sponsors / SaaS only around the proven wedge.",
                "- Continue pruning duplicate or weak lanes.",
            ]
        )

    lines.extend(
        [
            "",
            "## Commercial Path",
            "",
            "**GitHub proof / open core → implementation service → productized recurring service → paid intelligence/reporting → hosted workspace/SaaS**",
            "",
            "## Expansion Gate",
            "",
            "Before adding a new skill or product lane:",
            "",
            "1. Can an existing skill handle most of the job?",
            "2. Is there external demand or a clearly identified buyer?",
            "3. Can the first proof be measured?",
            "4. Does it strengthen creator operations rather than dilute positioning?",
            "5. What existing lane becomes lower priority if this is added?",
            "",
            "## Evidence Limits",
            "",
            "- Commit count is internal activity, not adoption.",
            "- Skill count is product breadth, not product-market fit.",
            "- Stars and forks are weak public signals and should not be translated into revenue claims.",
            "- External usage, repeat usage and buyer validation remain stronger proof.",
            "",
            "Research method: references/FOCUS-TRACTION-PLAYBOOK.md",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="traction-focus-report.md")
    args = parser.parse_args()

    try:
        metrics = collect(os.environ.get("GITHUB_TOKEN"))
    except Exception as exc:
        print(f"traction collection failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(metrics), encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
