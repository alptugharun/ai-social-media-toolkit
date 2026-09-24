#!/usr/bin/env python3
"""Small Places Aggregate API market scanner.

Uses the official Places Aggregate REST endpoint.
The tool prints the live response and does not persist Google Maps content.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Sequence

ENDPOINT = "https://areainsights.googleapis.com/v1:computeInsights"


def parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def build_payload(
    latitude: float,
    longitude: float,
    radius: float,
    included_types: Sequence[str],
    primary_types: Sequence[str] | None = None,
    min_rating: float | None = None,
    max_rating: float | None = None,
    mode: str = "count",
    operating_status: Sequence[str] | None = None,
) -> dict:
    if not included_types and not primary_types:
        raise ValueError("At least one included type or primary type is required.")
    if radius <= 0:
        raise ValueError("Radius must be greater than zero.")
    if not -90 <= latitude <= 90:
        raise ValueError("Latitude must be between -90 and 90.")
    if not -180 <= longitude <= 180:
        raise ValueError("Longitude must be between -180 and 180.")
    if min_rating is not None and not 0 <= min_rating <= 5:
        raise ValueError("min_rating must be between 0 and 5.")
    if max_rating is not None and not 0 <= max_rating <= 5:
        raise ValueError("max_rating must be between 0 and 5.")
    if min_rating is not None and max_rating is not None and min_rating > max_rating:
        raise ValueError("min_rating cannot exceed max_rating.")

    insights = ["INSIGHT_COUNT"]
    if mode == "places":
        insights.append("INSIGHT_PLACES")
    elif mode != "count":
        raise ValueError("mode must be 'count' or 'places'.")

    type_filter: dict[str, list[str]] = {}
    if included_types:
        type_filter["includedTypes"] = list(included_types)
    if primary_types:
        type_filter["includedPrimaryTypes"] = list(primary_types)

    filters: dict = {
        "locationFilter": {
            "circle": {
                "latLng": {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "radius": radius,
            }
        },
        "typeFilter": type_filter,
    }

    statuses = list(operating_status or ["OPERATING_STATUS_OPERATIONAL"])
    if statuses:
        filters["operatingStatus"] = statuses

    if min_rating is not None or max_rating is not None:
        rating_filter: dict[str, float] = {}
        if min_rating is not None:
            rating_filter["minRating"] = min_rating
        if max_rating is not None:
            rating_filter["maxRating"] = max_rating
        filters["ratingFilter"] = rating_filter

    return {"insights": insights, "filter": filters}


def call_api(payload: dict, api_key: str) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "User-Agent": "ai-social-media-toolkit-places-market-scan/0.1",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query official Google Places Aggregate insights for a circular market area."
    )
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lng", type=float, required=True)
    parser.add_argument("--radius", type=float, required=True, help="Circle radius in meters")
    parser.add_argument("--types", default="", help="Comma-separated included place types")
    parser.add_argument(
        "--primary-types",
        default="",
        help="Comma-separated included primary place types",
    )
    parser.add_argument("--min-rating", type=float)
    parser.add_argument("--max-rating", type=float)
    parser.add_argument("--mode", choices=["count", "places"], default="count")
    parser.add_argument(
        "--operating-status",
        default="OPERATING_STATUS_OPERATIONAL",
        help="Comma-separated Places Aggregate operating-status enums",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request payload without calling Google",
    )
    args = parser.parse_args()

    try:
        payload = build_payload(
            latitude=args.lat,
            longitude=args.lng,
            radius=args.radius,
            included_types=parse_csv(args.types),
            primary_types=parse_csv(args.primary_types),
            min_rating=args.min_rating,
            max_rating=args.max_rating,
            mode=args.mode,
            operating_status=parse_csv(args.operating_status),
        )
    except ValueError as exc:
        print(f"Invalid request: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        print(
            "GOOGLE_MAPS_API_KEY is required unless --dry-run is used.",
            file=sys.stderr,
        )
        return 2

    try:
        result = call_api(payload, api_key)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"Google API error {exc.code}: {detail}", file=sys.stderr)
        return 3
    except Exception as exc:
        print(f"Request failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 4

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
