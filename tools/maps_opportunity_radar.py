#!/usr/bin/env python3
"""Evidence-aware Maps + local-intelligence opportunity radar.

Uses public GitHub repository search as a demand/supply proxy.
It does not claim exact search volume, novelty, virality or revenue.
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

USER_AGENT = "ai-social-media-toolkit-maps-opportunity-radar/0.1"

LANES = [
    ("google-maps-mcp", "google maps mcp"),
    ("google-maps-agent-skills", "google maps agent skills"),
    ("google-places-mcp", "google places mcp"),
    ("google-business-profile", "google business profile api"),
    ("local-seo-maps", "local seo google maps"),
    ("local-rank-tracker", "local rank tracker maps"),
    ("places-aggregate", "places aggregate api"),
    ("geospatial-agent", "geospatial ai agent"),
    ("street-view-ai", "street view ai"),
    ("chatgpt-maps", "google maps chatgpt"),
    ("claude-maps", "google maps claude"),
    ("creator-location", "creator location scout"),
    ("timeline-takeout", "google maps timeline takeout"),
    ("maplibre-mcp", "maplibre mcp"),
]

REFERENCE_REPOS = [
    "googlemaps/agent-skills",
    "cablate/mcp-google-map",
    "AgriciDaniel/codex-seo",
]

CANDIDATES = [
    {
        "name": "local-business-intelligence-agent",
        "query": "local business intelligence agent maps",
        "lane": "google-business-profile",
        "fit": 100,
        "proof": 95,
        "compliance": 90,
        "distribution": 85,
        "job": "Turn permitted local and owned business signals into market, content and agency decisions.",
    },
    {
        "name": "creator-location-scout",
        "query": "creator location scout maps ai",
        "lane": "creator-location",
        "fit": 100,
        "proof": 90,
        "compliance": 90,
        "distribution": 90,
        "job": "Find shoot-ready locations and turn them into routes and content production plans.",
    },
    {
        "name": "local-content-gap-engine",
        "query": "local content gap business profile ai",
        "lane": "local-seo-maps",
        "fit": 100,
        "proof": 95,
        "compliance": 95,
        "distribution": 85,
        "job": "Turn owned search/review signals into local content opportunities.",
    },
    {
        "name": "sponsor-scout-local",
        "query": "local sponsor creator business scout ai",
        "lane": "creator-location",
        "fit": 95,
        "proof": 80,
        "compliance": 80,
        "distribution": 90,
        "job": "Create a human-reviewed local creator/business partnership shortlist.",
    },
    {
        "name": "places-aggregate-market-gap",
        "query": "places aggregate market gap",
        "lane": "places-aggregate",
        "fit": 90,
        "proof": 100,
        "compliance": 95,
        "distribution": 80,
        "job": "Use official aggregate place counts to compare category density across areas.",
    },
    {
        "name": "maps-policy-guard",
        "query": "google maps api policy guard agent skill",
        "lane": "google-maps-agent-skills",
        "fit": 95,
        "proof": 90,
        "compliance": 100,
        "distribution": 85,
        "job": "Review map-agent designs for scraping, storage, attribution and authorization risks.",
    },
    {
        "name": "mapwrapped-local-history",
        "query": "google maps timeline wrapped location history",
        "lane": "timeline-takeout",
        "fit": 75,
        "proof": 100,
        "compliance": 95,
        "distribution": 100,
        "job": "Turn a user's own exported location history into private, shareable year-in-review stories.",
    },
    {
        "name": "review-anomaly-explorer",
        "query": "google reviews anomaly detection",
        "lane": "google-business-profile",
        "fit": 85,
        "proof": 85,
        "compliance": 80,
        "distribution": 85,
        "job": "Flag review-pattern anomalies without accusing reviewers or businesses of fraud.",
    },
    {
        "name": "generic-google-maps-mcp",
        "query": "google maps mcp",
        "lane": "google-maps-mcp",
        "fit": 35,
        "proof": 80,
        "compliance": 90,
        "distribution": 75,
        "job": "Expose generic place search, routing and geocoding endpoints to an LLM.",
        "generic_penalty": 30,
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


def fetch_json(url: str, token: str | None = None) -> dict:
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
    days = max((now - created).total_seconds() / 86400.0, 1.0)
    return stars / days


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

    velocity_scores = scale([x.median_stars_per_day for x in lanes], log=True)
    star_scores = scale([x.top_stars for x in lanes], log=True)
    for index, lane in enumerate(lanes):
        lane.demand_score = round(0.6 * velocity_scores[index] + 0.4 * star_scores[index], 1)

    return sorted(lanes, key=lambda x: x.demand_score, reverse=True)


def fetch_reference_repos(token: str | None) -> list[dict]:
    rows: list[dict] = []
    for full_name in REFERENCE_REPOS:
        try:
            data = fetch_json(f"https://api.github.com/repos/{full_name}", token)
            rows.append(
                {
                    "full_name": full_name,
                    "stars": int(data.get("stargazers_count", 0)),
                    "forks": int(data.get("forks_count", 0)),
                    "updated_at": data.get("updated_at", ""),
                    "description": data.get("description") or "",
                    "url": data.get("html_url", f"https://github.com/{full_name}"),
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "full_name": full_name,
                    "error": type(exc).__name__,
                }
            )
    return rows


def score_candidates(token: str | None, lanes: list[Lane]) -> list[dict]:
    lane_map = {lane.slug: lane for lane in lanes}
    rows: list[dict] = []

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
            + 0.20 * gap
            + 0.20 * row["fit"]
            + 0.15 * row["proof"]
            + 0.15 * row["compliance"]
            + 0.05 * row["distribution"]
        )
        score -= row.get("generic_penalty", 0)
        row["gap_score"] = round(gap, 1)
        row["score"] = round(max(score, 0.0), 1)

    return sorted(rows, key=lambda row: row["score"], reverse=True)


def render_report(
    now: datetime,
    lanes: list[Lane],
    references: list[dict],
    candidates: list[dict],
) -> str:
    lines: list[str] = [
        "# Maps & Local Intelligence Radar",
        "",
        f"Generated: **{now.strftime('%Y-%m-%d %H:%M UTC')}**",
        "",
        "> This report uses GitHub demand/supply proxies. It does **not** guarantee novelty, virality, users, sponsorship or revenue.",
        "",
        "## Official Capability Baseline",
        "",
        "- Google Maps Platform has official Agent Skills.",
        "- Google Maps Grounding Lite provides managed MCP grounding for place search, weather and routing.",
        "- Places Aggregate API supports aggregate place-count / Place-ID insight workflows.",
        "- Google Business Profile APIs can support authorized business-performance and review workflows.",
        "",
        "Official capability references are documented in `references/MAPS-AI-OPPORTUNITY-PLAYBOOK.md` and must be re-checked before production releases.",
        "",
        "## Open-Source Reference Repositories",
        "",
        "| Repository | Stars | Forks | Last metadata update |",
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
            "## Candidate Gaps",
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
                "## Top Prototype Candidate",
                "",
                f'**{best["name"]}**',
                "",
                f'- Job: {best["job"]}',
                f'- Heuristic score: {best["score"]:.1f}/100',
                f'- Direct-supply proxy: {best["direct_supply"]:,} GitHub repository results for the configured query',
                "- Gate: inspect the closest repositories and run the Maps Policy Guard before implementation.",
            ]
        )

    lines.extend(
        [
            "",
            "## Build / Do Not Build",
            "",
            "**Build toward:** workflow intelligence, creator/location scouting, local content gaps, permitted aggregate market analysis, authorized Business Profile intelligence, policy-aware agent skills.",
            "",
            "**Do not build as the primary wedge:** another generic Google Maps MCP wrapper, scraped Maps lead databases, hidden Street View harvesting, automatic mass outreach, fake-review systems or sensitive-trait inference.",
            "",
            "## Human Review Gate",
            "",
            "- [ ] Official Google docs re-checked",
            "- [ ] Strong direct competitors inspected",
            "- [ ] Maps Policy Guard passed",
            "- [ ] No scraping dependency",
            "- [ ] No prohibited persistent Maps-content database",
            "- [ ] No guaranteed virality or revenue claim",
            "- [ ] Human approval before publishing a new skill/product",
            "",
            "## Evidence Limits",
            "",
            "- GitHub result counts are supply proxies, not search volume.",
            "- Stars/day is a simplified velocity proxy based on current stars and repository age.",
            "- Low direct supply does not prove that an idea is globally unique.",
            "- API terms and product capabilities can change; verify current official documentation before shipping.",
            "",
        ]
    )

    return "\n".join(lines)


def run(output: Path, token: str | None) -> int:
    now = datetime.now(timezone.utc)
    try:
        lanes = research_lanes(token, now)
        references = fetch_reference_repos(token)
        candidates = score_candidates(token, lanes)
    except urllib.error.HTTPError as exc:
        print(f"GitHub API error {exc.code}: {exc.reason}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Radar failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(now, lanes, references, candidates), encoding="utf-8")
    print(f"Wrote {output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the Maps + local-intelligence opportunity radar.")
    parser.add_argument("--output", default="maps-opportunity-radar.md")
    args = parser.parse_args()
    return run(Path(args.output), os.environ.get("GITHUB_TOKEN"))


if __name__ == "__main__":
    raise SystemExit(main())
