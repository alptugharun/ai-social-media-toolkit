#!/usr/bin/env python3
"""Evidence-aware GitHub opportunity radar.

Uses only Python's standard library and public GitHub endpoints.
It does not claim exact GitHub search volume. Search result counts are
treated as supply / competition proxies, while stars, freshness and
Trending overlap are treated as demand proxies.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

USER_AGENT = "ai-social-media-toolkit-github-opportunity-radar/0.1"

LANES = [
    ("agent-skills", "agent skills"),
    ("ai-agents", "AI agents"),
    ("mcp", "MCP server"),
    ("claude-code", "Claude Code"),
    ("github-copilot", "GitHub Copilot"),
    ("cursor-agent", "Cursor agent"),
    ("codex", "Codex agent"),
    ("creator-tools", "creator tools"),
    ("social-automation", "social media automation"),
    ("content-repurposing", "content repurposing"),
    ("pinterest", "Pinterest automation"),
    ("influencer-marketing", "influencer marketing"),
    ("short-form-video", "short form video"),
    ("brand-voice", "brand voice AI"),
    ("comment-analysis", "comment analysis AI"),
]

SKILL_CANDIDATES = [
    {
        "name": "brand-voice-regression-test",
        "query": "brand voice regression AI",
        "lane": "brand-voice",
        "job": "Detect brand-voice drift across batches of AI-assisted content.",
    },
    {
        "name": "content-decay-refresh",
        "query": "content decay refresh AI",
        "lane": "content-repurposing",
        "job": "Find aging evergreen assets and generate evidence-backed refresh plans.",
    },
    {
        "name": "proof-to-case-study",
        "query": "case study generator evidence metrics AI",
        "lane": "creator-tools",
        "job": "Turn evidence, metrics and source material into claim-safe case studies.",
    },
    {
        "name": "cross-platform-cannibalization-auditor",
        "query": "cross platform content cannibalization",
        "lane": "social-automation",
        "job": "Detect duplicate or competing content across social and web surfaces.",
    },
    {
        "name": "sponsor-readiness-auditor",
        "query": "creator sponsorship readiness audit",
        "lane": "influencer-marketing",
        "job": "Audit a creator's proof, positioning and media assets before brand outreach.",
    },
    {
        "name": "visual-trend-translator",
        "query": "visual trend translator brand AI",
        "lane": "creator-tools",
        "job": "Translate visual trends into original brand-safe execution directions.",
    },
    {
        "name": "hook-experiment-designer",
        "query": "hook A B test social content AI",
        "lane": "short-form-video",
        "job": "Create measurable hook hypotheses and platform-native A/B test plans.",
    },
    {
        "name": "local-business-demand-to-content",
        "query": "local business reviews content ideas AI",
        "lane": "social-automation",
        "job": "Convert reviews, FAQs and local demand signals into content opportunities.",
    },
    {
        "name": "agent-skill-gap-miner",
        "query": "agent skill gap discovery",
        "lane": "agent-skills",
        "job": "Find high-demand, low-direct-supply Agent Skill opportunities.",
    },
]


@dataclass
class LaneResult:
    slug: str
    query: str
    total_count: int
    top_stars: int
    median_stars_per_day: float
    trending_hits: int
    top_repos: list[dict]
    demand_score: float = 0.0
    competition_score: float = 0.0
    opportunity_score: float = 0.0


def request(url: str, token: str | None = None) -> urllib.request.Request:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return urllib.request.Request(url, headers=headers)


def fetch_json(url: str, token: str | None = None) -> dict:
    with urllib.request.urlopen(request(url, token), timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=25) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_trending(html: str) -> list[dict]:
    repos: list[dict] = []
    for block in re.findall(r"<article[^>]*Box-row[^>]*>(.*?)</article>", html, flags=re.S | re.I):
        match = re.search(r'href="/([^"/]+/[^"/]+)"', block)
        if not match:
            continue
        full_name = match.group(1).strip()
        stars_today_match = re.search(r"([\d,]+)\s+stars?\s+today", block, flags=re.I)
        stars_today = int(stars_today_match.group(1).replace(",", "")) if stars_today_match else 0
        repos.append({"full_name": full_name, "stars_today": stars_today})
    return repos


def stars_per_day(stars: int, created_at: str, now: datetime) -> float:
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    age_days = max((now - created).total_seconds() / 86400.0, 1.0)
    return stars / age_days


def scale(values: Iterable[float], *, log: bool = False) -> list[float]:
    vals = list(values)
    if not vals:
        return []
    transformed = [math.log1p(max(v, 0.0)) if log else float(v) for v in vals]
    low = min(transformed)
    high = max(transformed)
    if math.isclose(low, high):
        return [50.0 for _ in transformed]
    return [100.0 * (v - low) / (high - low) for v in transformed]


def score_lanes(lanes: list[LaneResult]) -> None:
    velocity = scale([x.median_stars_per_day for x in lanes], log=True)
    stars = scale([x.top_stars for x in lanes], log=True)
    competition = scale([x.total_count for x in lanes], log=True)

    for idx, lane in enumerate(lanes):
        trend_score = min(100.0, lane.trending_hits * 50.0)
        lane.demand_score = round(
            0.45 * velocity[idx] + 0.35 * stars[idx] + 0.20 * trend_score,
            1,
        )
        lane.competition_score = round(competition[idx], 1)
        gap_score = 100.0 - lane.competition_score
        lane.opportunity_score = round(0.80 * lane.demand_score + 0.20 * gap_score, 1)


def search_repositories(query: str, token: str | None, per_page: int = 5) -> dict:
    params = urllib.parse.urlencode(
        {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": str(per_page),
        }
    )
    return fetch_json(f"https://api.github.com/search/repositories?{params}", token)


def research_lanes(token: str | None, now: datetime, trending_names: set[str]) -> list[LaneResult]:
    cutoff = (now - timedelta(days=90)).date().isoformat()
    results: list[LaneResult] = []

    for slug, phrase in LANES:
        query = f'{phrase} in:name,description,readme created:>={cutoff} archived:false'
        data = search_repositories(query, token)
        items = data.get("items", [])

        repo_rows = []
        velocities = []
        for item in items:
            spd = stars_per_day(item.get("stargazers_count", 0), item["created_at"], now)
            velocities.append(spd)
            repo_rows.append(
                {
                    "full_name": item["full_name"],
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", ""),
                    "stars_per_day": round(spd, 1),
                    "url": item.get("html_url", ""),
                }
            )

        results.append(
            LaneResult(
                slug=slug,
                query=phrase,
                total_count=int(data.get("total_count", 0)),
                top_stars=max([x["stars"] for x in repo_rows], default=0),
                median_stars_per_day=round(statistics.median(velocities), 1) if velocities else 0.0,
                trending_hits=sum(1 for x in repo_rows if x["full_name"] in trending_names),
                top_repos=repo_rows,
            )
        )

    score_lanes(results)
    return sorted(results, key=lambda x: x.opportunity_score, reverse=True)


def research_skill_candidates(token: str | None, lanes: list[LaneResult]) -> list[dict]:
    lane_map = {x.slug: x for x in lanes}
    raw: list[dict] = []

    for candidate in SKILL_CANDIDATES:
        query = f'{candidate["query"]} in:name,description,readme archived:false'
        data = search_repositories(query, token, per_page=3)
        items = data.get("items", [])
        raw.append(
            {
                **candidate,
                "result_count": int(data.get("total_count", 0)),
                "top_competitors": [
                    {
                        "full_name": item["full_name"],
                        "stars": item.get("stargazers_count", 0),
                        "url": item.get("html_url", ""),
                    }
                    for item in items
                ],
            }
        )

    comp_scores = scale([x["result_count"] for x in raw], log=True)
    for idx, row in enumerate(raw):
        novelty_proxy = round(100.0 - comp_scores[idx], 1)
        lane = lane_map[row["lane"]]
        score = 0.65 * lane.opportunity_score + 0.35 * novelty_proxy
        row["novelty_proxy"] = novelty_proxy
        row["score"] = round(score, 1)

    return sorted(raw, key=lambda x: x["score"], reverse=True)


def md_escape(value: str) -> str:
    return value.replace("|", "\|").replace("\n", " ")


def render_report(now: datetime, trending: list[dict], lanes: list[LaneResult], candidates: list[dict], warnings: list[str]) -> str:
    lines: list[str] = []
    lines.append("# GitHub Opportunity Radar")
    lines.append("")
    lines.append(f"Generated: **{now.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}**")
    lines.append("")
    lines.append("> This report uses demand and supply proxies. It does **not** claim exact GitHub search volume or guaranteed virality.")
    lines.append("")

    if warnings:
        lines.append("## Data Warnings")
        lines.extend([f"- {w}" for w in warnings])
        lines.append("")

    lines.append("## Current Trending Signal")
    if trending:
        lines.append("| Repository | Stars today |")
        lines.append("| --- | ---: |")
        for item in sorted(trending, key=lambda x: x["stars_today"], reverse=True)[:12]:
            lines.append(f'| [{md_escape(item["full_name"])}](https://github.com/{item["full_name"]}) | {item["stars_today"]:,} |')
    else:
        lines.append("Trending HTML could not be parsed on this run. Search-based evidence is still included.")
    lines.append("")

    lines.append("## Demand / Supply Proxies")
    lines.append("| Theme | Recent search results | Median stars/day (top sample) | Trending overlap | Demand | Opportunity |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for lane in lanes:
        lines.append(
            f"| {md_escape(lane.query)} | {lane.total_count:,} | {lane.median_stars_per_day:.1f} | "
            f"{lane.trending_hits} | {lane.demand_score:.1f} | **{lane.opportunity_score:.1f}** |"
        )
    lines.append("")

    lines.append("## Fast-Rising Repositories in Relevant Lanes")
    shown = set()
    count = 0
    for lane in lanes:
        for repo in lane.top_repos:
            if repo["full_name"] in shown:
                continue
            shown.add(repo["full_name"])
            lines.append(
                f'- **[{repo["full_name"]}]({repo["url"]})** — {repo["stars"]:,} stars, '
                f'{repo["stars_per_day"]:.1f} stars/day since creation; lane: {lane.query}.'
            )
            count += 1
            if count >= 12:
                break
        if count >= 12:
            break
    lines.append("")

    lines.append("## Skill Gap Candidates")
    lines.append("| Candidate | Job-to-be-done | Direct-supply proxy | Novelty proxy | Score |")
    lines.append("| --- | --- | ---: | ---: | ---: |")
    for row in candidates:
        lines.append(
            f'| `{row["name"]}` | {md_escape(row["job"])} | {row["result_count"]:,} | '
            f'{row["novelty_proxy"]:.1f} | **{row["score"]:.1f}** |'
        )
    lines.append("")

    lines.append("### Top Prototype Recommendation")
    if candidates:
        best = candidates[0]
        lines.append(f'**{best["name"]}**')
        lines.append("")
        lines.append(f'- **Job:** {best["job"]}')
        lines.append(f'- **Direct-supply proxy:** {best["result_count"]:,} GitHub repository search results for the configured query.')
        lines.append(f'- **Opportunity score:** {best["score"]:.1f}/100 heuristic.')
        lines.append("- **Gate:** inspect the closest competitors before implementation; a low result count is not proof that nobody has built the idea.")
    lines.append("")

    lines.append("## Packaging Checklist for the Next Release")
    lines.extend(
        [
            "- [ ] One-sentence outcome above the fold",
            "- [ ] One-command install or copy path",
            "- [ ] First useful result in under a few minutes",
            "- [ ] Real example input and output",
            "- [ ] Measurable acceptance criteria or benchmark where possible",
            "- [ ] Cross-agent compatibility documented",
            "- [ ] Dependencies, API keys and privacy behavior explicit",
            "- [ ] License, security and contribution paths clear",
            "- [ ] Original wording and implementation",
            "- [ ] Human review before publishing a new skill",
        ]
    )
    lines.append("")

    lines.append("## Monetization Readiness")
    lines.append("- Keep the core public artifact genuinely useful.")
    lines.append("- Track stars, forks, installs where measurable, external mentions and website referrals.")
    lines.append("- Once usage appears, test GitHub Sponsors, implementation support, consulting, workshops or premium companion assets.")
    lines.append("- Do not treat stars as revenue or promise income.")
    lines.append("")

    lines.append("## Evidence Limits")
    lines.append("- GitHub does not expose exact public repository-search-volume data; result counts are treated as supply proxies.")
    lines.append("- Stars/day is calculated from current stars divided by repository age, not historical daily star events.")
    lines.append("- GitHub Trending is a fresh but short-lived signal.")
    lines.append("- Opportunity and novelty scores are heuristics for prioritization, not predictions.")
    lines.append("")
    lines.append("Source playbook: `references/GITHUB-GROWTH-PLAYBOOK.md`")
    return "\\n".join(lines) + "\\n"


def run(output: Path, token: str | None) -> int:
    now = datetime.now(timezone.utc)
    warnings: list[str] = []

    trending: list[dict] = []
    try:
        trending = parse_trending(fetch_text("https://github.com/trending?since=daily"))
    except Exception as exc:
        warnings.append(f"Trending fetch failed: {type(exc).__name__}")

    trending_names = {x["full_name"] for x in trending}

    try:
        lanes = research_lanes(token, now, trending_names)
        candidates = research_skill_candidates(token, lanes)
    except urllib.error.HTTPError as exc:
        print(f"GitHub API error: {exc.code} {exc.reason}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Radar failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(now, trending, lanes, candidates, warnings), encoding="utf-8")
    print(f"Wrote {output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an evidence-aware GitHub opportunity report.")
    parser.add_argument("--output", default="github-opportunity-radar.md", help="Markdown output path")
    args = parser.parse_args()
    return run(Path(args.output), os.environ.get("GITHUB_TOKEN"))


if __name__ == "__main__":
    raise SystemExit(main())
