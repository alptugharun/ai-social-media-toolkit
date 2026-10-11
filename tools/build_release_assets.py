#!/usr/bin/env python3
"""Build deterministic public release assets for the toolkit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

SAFE_VERSION = re.compile(r"^v?[0-9A-Za-z][0-9A-Za-z._-]*$")
FIXED_DT = (2026, 1, 1, 0, 0, 0)
SKIP_NAMES = {"__pycache__", ".DS_Store"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def iter_files(base: Path, *, exclude_parts: set[str] | None = None) -> list[Path]:
    exclude_parts = exclude_parts or set()
    files: list[Path] = []
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_NAMES or part in exclude_parts for part in path.parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        files.append(path)
    return files


def write_zip(output: Path, entries: list[tuple[Path, str]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(f"{output} already exists")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, arcname in sorted(entries, key=lambda item: item[1]):
            info = zipfile.ZipInfo(arcname.replace("\\", "/"), date_time=FIXED_DT)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, source.read_bytes())


def skill_dirs(root: Path) -> list[Path]:
    return sorted(
        p for p in (root / "skills").iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file()
    )


def build_skills_bundle(root: Path, output: Path) -> None:
    entries: list[tuple[Path, str]] = []
    for skill in skill_dirs(root):
        for source in iter_files(skill):
            entries.append((source, source.relative_to(root).as_posix()))
    extras = [
        root / "skills" / "README.md",
        root / "references" / "CREATOR-CONTEXT-TEMPLATE.md",
        root / "references" / "EVIDENCE-POLICY.md",
        root / "docs" / "INSTALLATION.md",
    ]
    for source in extras:
        if not source.is_file():
            raise FileNotFoundError(source)
        entries.append((source, source.relative_to(root).as_posix()))
    write_zip(output, entries)


def build_context_bundle(root: Path, output: Path) -> None:
    skill = root / "skills" / "creator-context-builder"
    entries = [
        (source, source.relative_to(root / "skills").as_posix())
        for source in iter_files(skill)
    ]
    write_zip(output, entries)


def build_frame_studio_bundle(root: Path, output: Path) -> None:
    app = root / "tools" / "creator-frame-studio"
    entries = [
        (source, source.relative_to(root / "tools").as_posix())
        for source in iter_files(app, exclude_parts={"tests"})
    ]
    write_zip(output, entries)


def build_plugin_bundle(root: Path, output: Path) -> None:
    cmd = [
        sys.executable,
        str(root / "tools" / "build_plugin_bundle.py"),
        "--output",
        str(output),
        "--repo-root",
        str(root),
    ]
    result = subprocess.run(cmd, cwd=root, text=True, capture_output=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "plugin bundle failed")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_release_assets(root: Path, out_dir: Path, version: str) -> list[Path]:
    if not SAFE_VERSION.fullmatch(version):
        raise ValueError("release version contains unsupported characters")

    out_dir.mkdir(parents=True, exist_ok=True)
    if any(out_dir.iterdir()):
        raise FileExistsError(f"{out_dir} must be empty")

    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    plugin_version = manifest["version"]

    assets = [
        out_dir / f"agent-skills-{version}.zip",
        out_dir / f"creator-context-builder-{version}.zip",
        out_dir / f"creator-frame-studio-{version}.zip",
        out_dir / f"ai-social-media-toolkit-plugin-{plugin_version}.zip",
    ]

    build_skills_bundle(root, assets[0])
    build_context_bundle(root, assets[1])
    build_frame_studio_bundle(root, assets[2])
    build_plugin_bundle(root, assets[3])

    checksums = out_dir / "SHA256SUMS.txt"
    checksums.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in sorted(assets, key=lambda p: p.name)),
        encoding="utf-8",
    )
    return assets + [checksums]


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Build deterministic GitHub release assets.")
    p.add_argument("--version", required=True)
    p.add_argument("--output-dir", type=Path, default=None)
    p.add_argument("--repo-root", type=Path, default=None, help=argparse.SUPPRESS)
    return p


def main() -> int:
    args = parser().parse_args()
    root = (args.repo_root or repo_root()).resolve()
    out = (args.output_dir or (root / "dist" / "release-assets")).resolve()
    try:
        assets = build_release_assets(root, out, args.version)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"RELEASE ASSET BUILD FAIL: {exc}", file=sys.stderr)
        return 2

    print("RELEASE ASSET BUILD PASS")
    print(f"Version: {args.version}")
    print(f"Skills: {len(skill_dirs(root))}")
    for path in assets:
        print(f"- {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
