#!/usr/bin/env python3
"""Pinterest visibility and opportunity radar.

Uses public GitHub repository metadata plus the official Pinterest Trends API
when accessible. It never invents Pinterest trend data.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

USER_AGENT = "ai-social-media-toolkit-pinterest-radar/0.1"

GITHUB_LANES = [
    ("pinterest-api", "pinterest api automation"),
    ("pinterest-trends", "pinterest trends api"),
    ("pinterest-analytics", "pinterest analytics api"),
    ("pinterest-scheduler", "pinterest scheduler open source"),
    ("pinterest-marketing", "pinterest marketing automation"),
    ("visual-search", "visual search creator tool"),
]

REFERENCE_REPOS = [
    "trypostit/trypost",
    "hevalhazalkurt/PinPy",
    "clugtu/pinterest-mcp",
    "what-name/pinterest-mcp",
]

DEFAULT_REGIONS = ["US", "GB", "CA", "AU", "TR"]


@dataclass
class Lane:
    slug: str
    query: str
    total_count: int
    top_stars: int
    median_stars_per_day: float
    demand_score: float = 0.0


def http_request(url: str, token: str | None = None) -> urllib.request.Request:
    headers = {
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return urllib.request.Request(url, headers=headers)


def fetch_json(url: str, token: str | None = None):
    with urllib.request.urlopen(http_request(url, token), timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def github_search(query: str, token: str | None, per_page: int = 5) -> dict:
    params = urllib.parse.urlencode(
        {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": str(per_page),
        }
    )
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        f"https://api.github.com/search/repositories?{params}",
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def github_repo(full_name: str, token: str | None) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        f"https://api.github.com/repos/{full_name}",
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


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


def research_github_lanes(token: str | None, now: datetime) -> list[Lane]:
    cutoff = (now - timedelta(days=365)).date().isoformat()
    lanes: list[Lane] = []

    for slug, phrase in GITHUB_LANES:
        data = github_search(
            f'{phrase} in:name,description,readme created:>={cutoff} archived:false',
            token,
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
                median_stars_per_day=round(statistics.median(velocities), 2)
                if velocities
                else 0.0,
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


def fetch_reference_repos(token: str | None) -> list[dict]:
    rows = []
    for full_name in REFERENCE_REPOS:
        try:
            data = github_repo(full_name, token)
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
            rows.append({"full_name": full_name, "error": type(exc).__name__})
    return rows


def trend_score(row: dict) -> float:
    wow = float(row.get("pct_growth_wow") or 0.0)
    mom = float(row.get("pct_growth_mom") or 0.0)
    yoy = float(row.get("pct_growth_yoy") or 0.0)

    wow = max(min(wow, 10000.0), -10000.0)
    mom = max(min(mom, 10000.0), -10000.0)
    yoy = max(min(yoy, 10000.0), -10000.0)

    return round(0.50 * wow + 0.30 * mom + 0.20 * yoy, 1)


def fetch_pinterest_trends(
    regions: list[str],
    pinterest_token: str | None,
    limit: int,
) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    warnings: list[str] = []

    for region in regions:
        url = (
            "https://api.pinterest.com/v5/trends/keywords/"
            f"{urllib.parse.quote(region)}/top/growing?limit={limit}"
        )
        try:
            data = fetch_json(url, pinterest_token)
            trends = data.get("trends", []) if isinstance(data, dict) else []
            for rank, trend in enumerate(trends, start=1):
                rows.append(
                    {
                        "region": region,
                        "rank": rank,
                        "keyword": trend.get("keyword", ""),
                        "pct_growth_wow": trend.get("pct_growth_wow"),
                        "pct_growth_mom": trend.get("pct_growth_mom"),
                        "pct_growth_yoy": trend.get("pct_growth_yoy"),
                        "time_series": trend.get("time_series") or {},
                        "score": trend_score(trend),
                    }
                )
        except urllib.error.HTTPError as exc:
            warnings.append(f"{region}: Pinterest Trends API returned HTTP {exc.code}.")
        except Exception as exc:
            warnings.append(f"{region}: Pinterest Trends API unavailable ({type(exc).__name__}).")

    return sorted(rows, key=lambda row: row["score"], reverse=True), warnings


def fmt_pct(value) -> str:
    if isinstance(value, (int, float)):
        return f"{value:+.0f}%"
    return "n/a"


def render_report(
    now: datetime,
    regions: list[str],
    trends: list[dict],
    warnings: list[str],
    lanes: list[Lane],
    references: list[dict],
    token_present: bool,
) -> str:
    api_status = "connected / accessible" if trends else "no live trend rows returned"

    lines = [
        "# Pinterest Visibility Radar",
        "",
        f"Generated: **{now.strftime('%Y-%m-%d %H:%M UTC')}**",
        "",
        "> Live Pinterest trend numbers are included only when the official Trends API returns them. No trend values are fabricated.",
        "",
        "## API Status",
        "",
        f"- Configured regions: **{', '.join(regions)}**",
        f"- Pinterest token present in runtime: **{token_present}**",
        f"- Live Trends status: **{api_status}**",
        "",
    ]

    if warnings:
        lines.append("### Access / Region Notes")
        lines.extend([f"- {warning}" for warning in warnings])
        lines.append("")

    lines.append("## Live Growing Keywords")
    lines.append("")

    if trends:
        lines.extend(
            [
                "| Rank | Keyword | Region | WoW | MoM | YoY | Growth score |",
                "| ---: | --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in trends[:30]:
            lines.append(
                f'| {row["rank"]} | {row["keyword"]} | {row["region"]} | '
                f'{fmt_pct(row["pct_growth_wow"])} | {fmt_pct(row["pct_growth_mom"])} | '
                f'{fmt_pct(row["pct_growth_yoy"])} | {row["score"]:.1f} |'
            )
    else:
        lines.append(
            "No authenticated/live Trends rows were available on this run. "
            "Treat all downstream content ideas as hypotheses until Pinterest trend evidence is available."
        )

    lines.extend(
        [
            "",
            "## Pinterest Tool / Automation Ecosystem",
            "",
            "| Repository | Stars | Forks | Updated | Capability signal |",
            "| --- | ---: | ---: | --- | --- |",
        ]
    )

    for row in references:
        if "error" in row:
            lines.append(f'| {row["full_name"]} | ? | ? | fetch error | unavailable |')
        else:
            description = row["description"].replace("|", "\\|")
            lines.append(
                f'| [{row["full_name"]}]({row["url"]}) | {row["stars"]:,} | '
                f'{row["forks"]:,} | {row["updated_at"]} | {description} |'
            )

    lines.extend(
        [
            "",
            "## Open-Source Demand / Supply Proxies",
            "",
            "| Lane | Recent repository results | Median stars/day | Demand score |",
            "| --- | ---: | ---: | ---: |",
        ]
    )

    for lane in lanes:
        lines.append(
            f"| {lane.query} | {lane.total_count:,} | "
            f"{lane.median_stars_per_day:.2f} | {lane.demand_score:.1f} |"
        )

    lines.extend(
        [
            "",
            "## Visibility Decisions",
            "",
            "- Generic bulk-pinning or scheduler clones are not the primary opportunity.",
            "- Prioritize evidence-backed keyword clusters, original visual systems and destination match.",
            "- Use pinterest-growth-engine after selecting a real opportunity.",
            "- Connect account analytics next so winner expansion can use real impressions, saves and outbound clicks.",
            "- Keep publishing human-reviewed until API access, board mapping and destination checks are explicitly configured.",
            "",
            "## Next Content Cluster Contract",
            "",
            "For every selected opportunity create:",
            "",
            "1. Hero Pin",
            "2. Educational Pin",
            "3. Checklist Pin",
            "4. Comparison Pin",
            "5. Seasonal variant",
            "6. Search-led variant",
            "7. Visual-discovery variant",
            "",
            "Each needs a keyword intent, visual direction, destination URL and KPI.",
            "",
            "## Evidence Limits",
            "",
            "- GitHub repository result counts are ecosystem/supply proxies, not Pinterest search volume.",
            "- A missing Pinterest API result is not evidence that no trend exists.",
            "- Growth percentages are only reported when returned by Pinterest.",
            "- Low competition does not prove an idea is unique.",
            "",
            "Research method: references/PINTEREST-AUTOMATION-PLAYBOOK.md",
            "",
        ]
    )

    return "\n".join(lines)


def run(output: Path, github_token: str | None, pinterest_token: str | None) -> int:
    now = datetime.now(timezone.utc)
    regions = [
        item.strip().upper()
        for item in os.environ.get(
            "PINTEREST_REGIONS",
            ",".join(DEFAULT_REGIONS),
        ).split(",")
        if item.strip()
    ]

    try:
        limit = int(os.environ.get("PINTEREST_TRENDS_LIMIT", "10"))
    except ValueError:
        limit = 10
    limit = max(1, min(limit, 50))

    try:
        lanes = research_github_lanes(github_token, now)
        references = fetch_reference_repos(github_token)
    except Exception as exc:
        print(f"GitHub evidence collection failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    trends, warnings = fetch_pinterest_trends(regions, pinterest_token, limit)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_report(
            now,
            regions,
            trends,
            warnings,
            lanes,
            references,
            bool(pinterest_token),
        ),
        encoding="utf-8",
    )
    print(f"Wrote {output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the Pinterest visibility radar.")
    parser.add_argument("--output", default="pinterest-visibility-radar.md")
    args = parser.parse_args()

    return run(
        Path(args.output),
        os.environ.get("GITHUB_TOKEN"),
        os.environ.get("PINTEREST_ACCESS_TOKEN"),
    )


if __name__ == "__main__":
    raise SystemExit(main())
