#!/usr/bin/env python3
"""Browse a small, evidence-labeled AI team stack without network access."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "resources" / "ai-team-stack.json"
SOURCE_TYPES = {"official", "vendor", "community", "maintainer"}
EVIDENCE = {"repo_verified", "maintainer_runtime_verified", "local_ci_verified"}


class StackError(ValueError):
    """User-actionable catalog/CLI error."""


def load_catalog(path: Path = CATALOG_PATH) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise StackError(f"Could not read a valid UTF-8 catalog: {exc}") from exc
    validate_catalog(data)
    return data


def validate_catalog(data: dict[str, Any]) -> None:
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise StackError("Unsupported catalog schema.")

    items = data.get("items")
    lanes = data.get("lanes")
    levels = data.get("evidence_levels")
    if not isinstance(items, list) or not items:
        raise StackError("Catalog requires items.")
    if not isinstance(lanes, dict) or not lanes:
        raise StackError("Catalog requires lanes.")
    if not isinstance(levels, dict) or set(levels) != EVIDENCE:
        raise StackError("Evidence levels do not match the supported contract.")

    ids: set[str] = set()
    repos: set[str] = set()
    required = {
        "id", "name", "repo", "source_type", "role", "layer", "use_when",
        "avoid_when", "first_result", "permission_note", "cost_note",
        "evidence", "install_reference"
    }
    for item in items:
        if not isinstance(item, dict) or not required.issubset(item):
            raise StackError("Every catalog item must satisfy the item contract.")
        item_id = item["id"]
        if not isinstance(item_id, str) or not item_id or item_id in ids:
            raise StackError("Catalog IDs must be unique non-empty strings.")
        ids.add(item_id)
        repo = item["repo"]
        if not isinstance(repo, str) or not repo.startswith("https://github.com/") or repo in repos:
            raise StackError("Repository URLs must be unique HTTPS GitHub URLs.")
        repos.add(repo)
        if item["source_type"] not in SOURCE_TYPES:
            raise StackError(f"Unknown source_type for {item_id}.")
        if item["evidence"] not in EVIDENCE:
            raise StackError(f"Unknown evidence level for {item_id}.")
        if not str(item["install_reference"]).startswith("https://"):
            raise StackError(f"Install reference must use HTTPS for {item_id}.")

    for lane_id, lane in lanes.items():
        if not isinstance(lane, dict) or not isinstance(lane.get("items"), list):
            raise StackError(f"Invalid lane: {lane_id}")
        if len(lane["items"]) != 5:
            raise StackError(f"Lane {lane_id} must contain exactly five starting items.")
        if len(set(lane["items"])) != 5:
            raise StackError(f"Lane {lane_id} contains duplicate items.")
        missing = [item_id for item_id in lane["items"] if item_id not in ids]
        if missing:
            raise StackError(f"Lane {lane_id} references missing items: {missing}")


def item_index(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in data["items"]}


def compact(item: dict[str, Any]) -> str:
    return (
        f'{item["id"]}: {item["name"]} | {item["role"]} | '
        f'{item["source_type"]} | {item["evidence"]}'
    )


def print_item(item: dict[str, Any]) -> None:
    print(item["name"])
    print("=" * len(item["name"]))
    print(f'ID: {item["id"]}')
    print(f'Role: {item["role"]}')
    print(f'Layer: {item["layer"]}')
    print(f'Source: {item["source_type"]}')
    print(f'Evidence: {item["evidence"]}')
    print(f'Repository: {item["repo"]}')
    print(f'Use when: {item["use_when"]}')
    print(f'Avoid when: {item["avoid_when"]}')
    print(f'First result: {item["first_result"]}')
    print(f'Permissions: {item["permission_note"]}')
    print(f'Cost: {item["cost_note"]}')
    print(f'Install/docs: {item["install_reference"]}')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    listing = sub.add_parser("list", help="List catalog items.")
    listing.add_argument("--role", help="Case-insensitive substring filter on role.")
    listing.add_argument("--source-type", choices=sorted(SOURCE_TYPES))
    listing.add_argument("--evidence", choices=sorted(EVIDENCE))
    listing.add_argument("--json", action="store_true", dest="as_json")

    show = sub.add_parser("show", help="Show one item by ID.")
    show.add_argument("id")

    recommend = sub.add_parser("recommend", help="Print one five-item starting lane.")
    recommend.add_argument("--lane", choices=["coding_core", "creator_core"], required=True)
    recommend.add_argument("--json", action="store_true", dest="as_json")

    sub.add_parser("check", help="Validate the catalog.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        data = load_catalog()
        items = item_index(data)

        if args.command == "check":
            print(f'PASS: {len(data["items"])} items, {len(data["lanes"])} lanes; checked {data["checked_at"]}.')
            return 0

        if args.command == "show":
            item = items.get(args.id)
            if not item:
                raise StackError("Unknown item ID. Run 'list' first.")
            print_item(item)
            return 0

        if args.command == "recommend":
            lane = data["lanes"][args.lane]
            selected = [items[item_id] for item_id in lane["items"]]
            if args.as_json:
                print(json.dumps({"lane": args.lane, "title": lane["title"], "items": selected}, indent=2))
            else:
                print(lane["title"])
                print(lane["purpose"])
                for index, item in enumerate(selected, 1):
                    print(f'{index}. {compact(item)}')
            return 0

        selected = data["items"]
        if args.role:
            needle = args.role.casefold()
            selected = [item for item in selected if needle in item["role"].casefold()]
        if args.source_type:
            selected = [item for item in selected if item["source_type"] == args.source_type]
        if args.evidence:
            selected = [item for item in selected if item["evidence"] == args.evidence]
        if args.as_json:
            print(json.dumps(selected, indent=2))
        else:
            for item in selected:
                print(compact(item))
        return 0
    except StackError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
