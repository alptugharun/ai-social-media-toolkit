#!/usr/bin/env python3
"""Install AI Social Media Toolkit skills into common Agent Skills locations.

No third-party dependencies are required.

Examples:
    python tools/install_skills.py --target agents --scope user
    python tools/install_skills.py --target gemini --scope project
    python tools/install_skills.py --target codex --scope user --skill viral-content-radar
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

TARGETS = {
    "agents": (Path(".agents") / "skills", Path.home() / ".agents" / "skills"),
    "claude": (Path(".claude") / "skills", Path.home() / ".claude" / "skills"),
    "copilot": (Path(".github") / "skills", Path.home() / ".copilot" / "skills"),
    "codex": (Path(".codex") / "skills", Path.home() / ".codex" / "skills"),
    "gemini": (Path(".gemini") / "skills", Path.home() / ".gemini" / "skills"),
    "grok": (Path(".grok") / "skills", Path.home() / ".grok" / "skills"),
    "cursor": (Path(".cursor") / "skills", Path.home() / ".cursor" / "skills"),
}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def discover_skills(repo_root: Path) -> dict[str, Path]:
    skills_root = repo_root / "skills"
    if not skills_root.is_dir():
        raise ValueError(f"Skills directory not found: {skills_root}")

    skills: dict[str, Path] = {}
    for child in sorted(skills_root.iterdir()):
        if child.is_dir() and (child / "SKILL.md").is_file():
            skills[child.name] = child
    if not skills:
        raise ValueError(f"No installable skills found in {skills_root}")
    return skills


def destination_root(
    target: str,
    scope: str,
    project_root: Path,
    override: Path | None,
) -> Path:
    if override is not None:
        return override.expanduser().resolve()

    project_path, user_path = TARGETS[target]
    if scope == "user":
        return user_path.expanduser()
    return (project_root / project_path).resolve()


def install_skill(source: Path, destination: Path, force: bool, dry_run: bool) -> str:
    if destination.exists():
        if not force:
            raise FileExistsError(
                f"{destination} already exists. Use --force only if replacement is intentional."
            )
        action = "replace"
    else:
        action = "install"

    if dry_run:
        return action

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    return action


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install AI Social Media Toolkit Agent Skills."
    )
    parser.add_argument(
        "--target",
        choices=sorted(TARGETS),
        default="agents",
        help="Agent runtime or portable Agent Skills target.",
    )
    parser.add_argument(
        "--scope",
        choices=("user", "project"),
        default="user",
        help="Install globally for the current user or into one project.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root used with --scope project. Defaults to the current directory.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Install one named skill. Repeat the flag to install multiple skills.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing destination skill directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files.",
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=None,
        help="Override the destination skills root. Useful for testing or custom runtimes.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help=argparse.SUPPRESS,
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    repo_root = (
        args.repo_root.expanduser().resolve()
        if args.repo_root is not None
        else repository_root()
    )
    project_root = args.project_root.expanduser().resolve()

    try:
        available = discover_skills(repo_root)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    selected_names = args.skill or list(available)
    unknown = [name for name in selected_names if name not in available]
    if unknown:
        print(
            "error: unknown skill(s): " + ", ".join(unknown)
            + "\navailable: " + ", ".join(available),
            file=sys.stderr,
        )
        return 2

    dest_root = destination_root(
        args.target,
        args.scope,
        project_root,
        args.destination,
    )

    print(f"Target: {args.target}")
    print(f"Scope: {args.scope}")
    print(f"Destination: {dest_root}")
    print(f"Mode: {'dry-run' if args.dry_run else 'write'}")

    try:
        for name in selected_names:
            destination = dest_root / name
            action = install_skill(
                source=available[name],
                destination=destination,
                force=args.force,
                dry_run=args.dry_run,
            )
            print(f"{action}: {name} -> {destination}")
    except (FileExistsError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
