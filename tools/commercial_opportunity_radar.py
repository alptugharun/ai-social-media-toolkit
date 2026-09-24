#!/usr/bin/env python3
"""Commercial opportunity radar for an open-source creator/marketing toolkit.

Uses public GitHub metadata and repository search as evidence proxies.
It does not claim exact search volume, customer demand, revenue or virality.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import time
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

USER_AGENT = "ai-social-media-toolkit-commercial-radar/0.1"
SELF_REPO = "alptugharun/ai-social-media-toolkit"

LANES = [
    ("agentic-workflows", "github agentic workflows"),
    ("ai-marketing-skills", "ai marketing skills"),
    ("self-hosted-ai", "self hosted ai tool"),
    ("marketing-automation", "marketing automation ai open source"),
    ("creator-tools", "creator tools ai open source"),
    ("local-seo", "local seo ai automation"),
    ("b2b-intelligence", "b2b intelligence ai open source"),
    ("github-marketplace", "github marketplace app ai"),
    ("open-source-saas", "open source saas ai"),
    ("local-business-ai", "local business intelligence ai"),
]

REFERENCE_REPOS = [
    "github/gh-aw",
    "githubnext/agentics",
    "ericosiu/ai-marketing-skills",
    "eracle/OpenOutreach",
    "n8n-io/self-hosted-ai-starter-kit",
    "langgenius/dify",
]

CANDIDATES = [
    {
        "name": "local-business-intelligence-cloud",
        "query": "local business intelligence saas ai",
        "lane": "local-business-ai",
        "buyer": 100,
        "recurring": 100,
        "proof": 95,
        "distribution": 85,
        "feasibility": 80,
        "monetization": 100,
        "job": "Managed multi-client local business intelligence and recurring reporting.",
    },
    {
        "name": "creator-ops-workspace",
        "query": "creator ops workspace ai",
        "lane": "creator-tools",
        "buyer": 90,
        "recurring": 95,
        "proof": 90,
        "distribution": 90,
        "feasibility": 75,
        "monetization": 90,
        "job": "Hosted workspace that turns creator research into repeatable content operations.",
    },
    {
        "name": "b2b-signal-to-offer-briefs",
        "query": "b2b market intelligence report automation ai",
        "lane": "b2b-intelligence",
        "buyer": 95,
        "recurring": 95,
        "proof": 90,
        "distribution": 75,
        "feasibility": 90,
        "monetization": 95,
        "job": "Recurring evidence-backed niche opportunity briefs for a narrow B2B buyer.",
    },
    {
        "name": "maps-local-content-gap-report",
        "query": "local content gap maps seo report",
        "lane": "local-seo",
        "buyer": 100,
        "recurring": 90,
        "proof": 95,
        "distribution": 80,
        "feasibility": 90,
        "monetization": 95,
        "job": "Turn permitted local/owned business signals into a recurring content-gap report.",
    },
    {
        "name": "agentic-workflow-pack",
        "query": "agentic workflow pack github",
        "lane": "agentic-workflows",
        "buyer": 80,
        "recurring": 70,
        "proof": 100,
        "distribution": 100,
        "feasibility": 90,
        "monetization": 70,
        "job": "Reusable GitHub Agentic Workflow pack for creator and agency repository operations.",
    },
    {
        "name": "implementation-as-a-service",
        "query": "ai automation implementation agency open source",
        "lane": "marketing-automation",
        "buyer": 100,
        "recurring": 75,
        "proof": 90,
        "distribution": 70,
        "feasibility": 100,
        "monetization": 100,
        "job": "Paid installation, customization and support around the free toolkit.",
    },
    {
        "name": "mapwrapped-premium-companion",
        "query": "location history wrapped map app",
        "lane": "creator-tools",
        "buyer": 70,
        "recurring": 55,
        "proof": 100,
        "distribution": 100,
        "feasibility": 70,
        "monetization": 75,
        "job": "Local-first MapWrapped product with premium themes, exports and physical/digital companions.",
    },
    {
        "name": "github-marketplace-app",
        "query": "marketing automation github app marketplace",
        "lane": "github-marketplace",
        "buyer": 80,
        "recurring": 90,
        "proof": 85,
        "distribution": 100,
        "feasibility": 55,
        "monetization": 90,
        "job": "Productized GitHub App with free and paid workflow tiers.",
    },
    {
        "name": "github-sponsors-maintainer-model",
        "query": "github sponsors ai automation open source",
        "lane": "open-source-saas",
        "buyer": 55,
        "recurring": 65,
        "proof": 70,
        "distribution": 90,
        "feasibility": 100,
        "monetization": 60,
        "job": "Fund public maintenance and requested integrations through sponsor support.",
    },
]


@dataclass
class Lane:
    slug: str
    query: str
    total_count: int
    top_stars: int
    median_stars_per_day: float
    demand_score: float = 0.0


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


def search_repositories(query: str, token: str | None, per_page: int = 5) -> dict:
    time.sleep(2.1)  # keep GitHub Search API calls below per-minute limits
    params = urllib.parse.urlencode(
        {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": str(per_page),
        }
    )
    return fetch_json(f"https://api.github.com/search/repositories?{params}", token)


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


def research_lanes(token: str | None, now: datetime) -> list[Lane]:
    cutoff = (now - timedelta(days=365)).date().isoformat()
    lanes: list[Lane] = []

    for slug, phrase in LANES:
        data = search_repositories(
            f'{phrase} in:name,description,readme created:>={cutoff} archived:false',
            token,
            per_page=5,
        )
        items = data.get("items", [])
        velocities = [
            stars_per_day(item.get("stargazers_count", 0), item["created_at"], now)
            for item in items
        ]
        lanes.append(
            Lane(
                slug=slug,
                query=phrase,
                total_count=int(data.get("total_count", 0)),
                top_stars=max([item.get("stargazers_count", 0) for item in items], default=0),
                median_stars_per_day=round(statistics.median(velocities), 2) if velocities else 0.0,
            )
        )

    velocity_scores = scale([lane.median_stars_per_day for lane in lanes], log=True)
    star_scores = scale([lane.top_stars for lane in lanes], log=True)

    for index, lane in enumerate(lanes):
        lane.demand_score = round(
            0.60 * velocity_scores[index] + 0.40 * star_scores[index],
            1,
        )

    return sorted(lanes, key=lambda lane: lane.demand_score, reverse=True)


def reference_repositories(token: str | None) -> list[dict]:
    rows = []
    for full_name in REFERENCE_REPOS:
        try:
            data = fetch_json(f"https://api.github.com/repos/{full_name}", token)
            rows.append(
                {
                    "full_name": full_name,
                    "stars": int(data.get("stargazers_count", 0)),
                    "forks": int(data.get("forks_count", 0)),
                    "updated_at": data.get("updated_at", ""),
                    "url": data.get("html_url", f"https://github.com/{full_name}"),
                }
            )
        except Exception as exc:
            rows.append({"full_name": full_name, "error": type(exc).__name__})
    return rows


def self_repo_readiness(token: str | None) -> dict:
    repo = fetch_json(f"https://api.github.com/repos/{SELF_REPO}", token)

    funding = False
    try:
        fetch_json(f"https://api.github.com/repos/{SELF_REPO}/contents/.github/FUNDING.yml", token)
        funding = True
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise

    releases = fetch_json(f"https://api.github.com/repos/{SELF_REPO}/releases?per_page=5", token)

    return {
        "stars": int(repo.get("stargazers_count", 0)),
        "forks": int(repo.get("forks_count", 0)),
        "subscribers": int(repo.get("subscribers_count", 0)),
        "has_discussions": bool(repo.get("has_discussions", False)),
        "has_pages": bool(repo.get("has_pages", False)),
        "funding_configured": funding,
        "release_count_sample": len(releases) if isinstance(releases, list) else 0,
    }


def score_candidates(token: str | None, lanes: list[Lane]) -> list[dict]:
    lane_map = {lane.slug: lane for lane in lanes}
    rows = []

    for candidate in CANDIDATES:
        data = search_repositories(
            f'{candidate["query"]} in:name,description,readme archived:false',
            token,
            per_page=3,
        )
        rows.append(
            {
                **candidate,
                "direct_supply": int(data.get("total_count", 0)),
                "top_competitors": [
                    {
                        "full_name": item["full_name"],
                        "stars": int(item.get("stargazers_count", 0)),
                        "url": item.get("html_url", ""),
                    }
                    for item in data.get("items", [])
                ],
            }
        )

    supply_scores = scale([row["direct_supply"] for row in rows], log=True)

    for index, row in enumerate(rows):
        gap = 100.0 - supply_scores[index]
        demand = lane_map[row["lane"]].demand_score

        score = (
            0.25 * demand
            + 0.20 * row["buyer"]
            + 0.15 * row["recurring"]
            + 0.15 * row["proof"]
            + 0.10 * row["distribution"]
            + 0.10 * row["feasibility"]
            + 0.05 * row["monetization"]
        )

        # Direct-supply gap acts as a bounded bonus rather than replacing buyer clarity.
        score += 0.10 * gap
        score = min(score, 100.0)

        row["gap_score"] = round(gap, 1)
        row["score"] = round(score, 1)

    return sorted(rows, key=lambda row: row["score"], reverse=True)


def render_report(
    now: datetime,
    lanes: list[Lane],
    references: list[dict],
    readiness: dict,
    candidates: list[dict],
) -> str:
    lines = [
        "# Commercial Opportunity Radar",
        "",
        f"Generated: **{now.strftime('%Y-%m-%d %H:%M UTC')}**",
        "",
        "> This is a prioritization report, not a revenue forecast. GitHub search result counts are supply proxies, not search volume.",
        "",
        "## Current Repository Commercial Readiness",
        "",
        f'- Stars: **{readiness["stars"]}**',
        f'- Forks: **{readiness["forks"]}**',
        f'- Subscribers: **{readiness["subscribers"]}**',
        f'- Discussions enabled: **{readiness["has_discussions"]}**',
        f'- GitHub Pages enabled: **{readiness["has_pages"]}**',
        f'- FUNDING.yml configured: **{readiness["funding_configured"]}**',
        f'- Releases in latest sample: **{readiness["release_count_sample"]}**',
        "",
        "Interpretation rule: do not add monetization friction merely because a capability exists. Adoption evidence comes first.",
        "",
        "## Reference Repositories",
        "",
        "| Repository | Stars | Forks | Updated |",
        "| --- | ---: | ---: | --- |",
    ]

    for row in references:
        if "error" in row:
            lines.append(f'| {row["full_name"]} | ? | ? | fetch error: {row["error"]} |')
        else:
            lines.append(
                f'| [{row["full_name"]}]({row["url"]}) | {row["stars"]:,} | {row["forks"]:,} | {row["updated_at"]} |'
            )

    lines.extend(
        [
            "",
            "## Demand / Supply Proxies",
            "",
            "| Theme | GitHub result count | Median stars/day in recent top sample | Demand score |",
            "| --- | ---: | ---: | ---: |",
        ]
    )

    for lane in lanes:
        lines.append(
            f"| {lane.query} | {lane.total_count:,} | {lane.median_stars_per_day:.2f} | {lane.demand_score:.1f} |"
        )

    lines.extend(
        [
            "",
            "## Commercial Candidates",
            "",
            "| Candidate | Job | Direct-supply proxy | Gap | Score |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )

    for row in candidates:
        lines.append(
            f'| `{row["name"]}` | {row["job"]} | {row["direct_supply"]:,} | {row["gap_score"]:.1f} | **{row["score"]:.1f}** |'
        )

    if candidates:
        best = candidates[0]
        lines.extend(
            [
                "",
                "## Top Commercial Test",
                "",
                f'**{best["name"]}**',
                "",
                f'- Job: {best["job"]}',
                f'- Heuristic score: {best["score"]:.1f}/100',
                f'- Direct-supply proxy: {best["direct_supply"]:,} GitHub repository results',
                "- Recommended validation: produce one useful free artifact, define one paid deeper deliverable, and measure real requests before building a large SaaS layer.",
            ]
        )

    lines.extend(
        [
            "",
            "## Monetization Ladder",
            "",
            "1. implementation / customization service",
            "2. paid recurring report",
            "3. hosted convenience / multi-client workspace",
            "4. premium companion assets",
            "5. GitHub Sponsors after real public value",
            "6. GitHub Marketplace distribution after productization",
            "7. enterprise support only after repeatable demand",
            "",
            "## Agentic Automation Upgrade",
            "",
            "GitHub Agentic Workflows are a future optional layer for AI-authored repository tasks. Keep deterministic radars as the default until a supported agent credential and repository secret are intentionally configured.",
            "",
            "## Guardrails",
            "",
            "- no restricted-platform scraping",
            "- no mass unsolicited outreach",
            "- no fabricated revenue / customer claims",
            "- no auto-pricing or financial commitments",
            "- no automatic sponsorship acceptance",
            "- no auto-publishing low-quality products",
            "- human approval before external commercial action",
            "",
            "## Evidence Limits",
            "",
            "- Stars are distribution / interest signals, not customer revenue.",
            "- Search result counts are supply proxies, not demand volume.",
            "- Candidate scores are heuristics for prioritization.",
            "- Public repo Actions can automate research, but commercial delivery must still respect platform, privacy and anti-spam rules.",
            "",
        ]
    )

    return "\n".join(lines)


def run(output: Path, token: str | None) -> int:
    now = datetime.now(timezone.utc)

    try:
        lanes = research_lanes(token, now)
        references = reference_repositories(token)
        readiness = self_repo_readiness(token)
        candidates = score_candidates(token, lanes)
    except urllib.error.HTTPError as exc:
        print(f"GitHub API error {exc.code}: {exc.reason}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Commercial radar failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_report(now, lanes, references, readiness, candidates),
        encoding="utf-8",
    )
    print(f"Wrote {output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the commercial opportunity radar.")
    parser.add_argument("--output", default="commercial-opportunity-radar.md")
    args = parser.parse_args()
    return run(Path(args.output), os.environ.get("GITHUB_TOKEN"))


if __name__ == "__main__":
    raise SystemExit(main())
