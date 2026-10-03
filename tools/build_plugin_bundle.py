#!/usr/bin/env python3
"""Build a narrow, deterministic skills-only Agent Plugin archive."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")

# Repository-level resources referenced by one portable skill.
EXTRA_FILES = (
    Path("learning/AI-BUILDER-PATH.md"),
    Path("integrations/README.md"),
    Path("prompts/assistants/plugin-mcp-architect.md"),
)

SKIP_NAMES = {"__pycache__", ".DS_Store"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest(root: Path) -> dict:
    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    required = {"$schema", "name", "version", "description"}
    missing = sorted(required - manifest.keys())
    if missing:
        raise ValueError("plugin.json missing required release fields: " + ", ".join(missing))
    if manifest["$schema"] != SCHEMA:
        raise ValueError(f"unexpected plugin schema: {manifest['$schema']!r}")
    if not NAME_RE.fullmatch(manifest["name"]):
        raise ValueError("plugin name must be stable kebab-case")
    if not SEMVER_RE.fullmatch(manifest["version"]):
        raise ValueError("plugin version must be semantic version text")
    if not str(manifest["description"]).strip():
        raise ValueError("plugin description must not be empty")
    return manifest


def discover_skill_dirs(root: Path) -> list[Path]:
    skills_root = root / "skills"
    skills = sorted(
        child
        for child in skills_root.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    )
    if not skills:
        raise ValueError("no installable skills found")
    return skills


def iter_tree_files(base: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_NAMES for part in path.parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        files.append(path)
    return files


def bundle_files(root: Path) -> list[Path]:
    files = [root / "plugin.json"]
    for skill_dir in discover_skill_dirs(root):
        files.extend(iter_tree_files(skill_dir))
    for relative in EXTRA_FILES:
        path = root / relative
        if not path.is_file():
            raise ValueError(f"required plugin resource missing: {relative.as_posix()}")
        files.append(path)

    unique = sorted(set(files), key=lambda p: p.relative_to(root).as_posix())
    return unique


def write_zip(root: Path, output: Path, files: list[Path]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(f"{output} already exists; remove it or choose another output")

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in files:
            relative = source.relative_to(root).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, source.read_bytes())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the skills-only Agent Plugin ZIP.")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--repo-root", type=Path, default=None, help=argparse.SUPPRESS)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = (args.repo_root or repo_root()).resolve()

    try:
        manifest = load_manifest(root)
        files = bundle_files(root)
        output = (
            args.output.expanduser().resolve()
            if args.output is not None
            else root / "dist" / f"{manifest['name']}-plugin-{manifest['version']}.zip"
        )
        write_zip(root, output, files)
    except (OSError, ValueError, json.JSONDecodeError, FileExistsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    skill_count = len(discover_skill_dirs(root))
    print(f"PLUGIN BUNDLE PASS: {output}")
    print(f"Version: {manifest['version']}")
    print(f"Skills: {skill_count}")
    print(f"Files: {len(files)}")
    print("MCP: none (skills-only package)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
