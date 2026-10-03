#!/usr/bin/env python3
"""Deterministic repository readiness checks for public AI/MCP distribution.

This tool is intentionally offline: it verifies repository evidence that can be
proven from the checkout and refuses to turn external reputation signals into
fabricated pass/fail claims.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP_SERVER = ROOT / "tools" / "prompt_mcp_server.py"
MCP_TESTS = ROOT / "tests" / "test_prompt_mcp_server.py"
PACKAGED_MCP_SERVER = ROOT / "packages" / "ai-workbench-mcp" / "src" / "ai_workbench_mcp" / "server.py"
PACKAGED_MCP_TESTS = ROOT / "tests" / "test_mcp_distribution_package.py"
PACKAGED_MCP_ADJACENT_TESTS = ROOT / "packages" / "ai-workbench-mcp" / "tests" / "test_public_tools.py"
PLUGIN_MANIFEST = ROOT / "plugin.json"
PLUGIN_GUIDE = ROOT / "PLUGIN-GUIDE.md"
PLUGIN_CASES = ROOT / "evals" / "plugin-submission-cases.json"
SKILLS_ROOT = ROOT / "skills"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PLUGIN_MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
REQUIRED_PUBLIC_FILES = (
    "README.md",
    "LICENSE.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SUPPORT.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "ADOPTION.md",
)
REQUIRED_HINTS = {
    "readOnlyHint",
    "destructiveHint",
    "idempotentHint",
    "openWorldHint",
}
ACTION_REF = re.compile(r"^\s*uses:\s*[^#\s]+@([^\s#]+)")


class ReadinessError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ReadinessError(message)


def load_tools_literal_from(path: Path) -> list[dict]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "TOOLS" for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            if not isinstance(value, list):
                fail("TOOLS must be a literal list.")
            return value
    fail(f"Could not find literal TOOLS declaration in {path.relative_to(ROOT)}.")


def load_tools_literal() -> list[dict]:
    return load_tools_literal_from(MCP_SERVER)


def check_public_files() -> list[str]:
    missing = [path for path in REQUIRED_PUBLIC_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("Missing public trust/onboarding files: " + ", ".join(missing))
    return [f"public-files:{len(REQUIRED_PUBLIC_FILES)}"]


def check_mcp_tools() -> list[str]:
    tools = load_tools_literal()
    if not tools:
        fail("MCP server exposes no tools.")

    names: list[str] = []
    for tool in tools:
        name = tool.get("name")
        if not isinstance(name, str) or not name:
            fail("Every MCP tool needs a non-empty string name.")
        names.append(name)

        description = tool.get("description")
        if not isinstance(description, str) or len(description.strip()) < 12:
            fail(f"{name}: description is missing or too vague.")

        schema = tool.get("inputSchema")
        if not isinstance(schema, dict) or schema.get("type") != "object":
            fail(f"{name}: inputSchema must be an object schema.")
        if schema.get("additionalProperties") is not False:
            fail(f"{name}: inputSchema must reject undeclared top-level properties.")

        annotations = tool.get("annotations")
        if not isinstance(annotations, dict):
            fail(f"{name}: annotations are missing.")
        missing = REQUIRED_HINTS - set(annotations)
        if missing:
            fail(f"{name}: missing annotations: {', '.join(sorted(missing))}.")
        for hint in REQUIRED_HINTS:
            if type(annotations[hint]) is not bool:
                fail(f"{name}: {hint} must be an explicit boolean.")

    if len(names) != len(set(names)):
        fail("MCP tool names must be unique.")

    test_text = MCP_TESTS.read_text(encoding="utf-8")
    missing_tests = [name for name in names if name not in test_text]
    if missing_tests:
        fail("MCP tools without name-level test coverage: " + ", ".join(missing_tests))

    packaged_tools = load_tools_literal_from(PACKAGED_MCP_SERVER)
    packaged_names = [tool.get("name") for tool in packaged_tools]
    if any(not isinstance(name, str) or not name for name in packaged_names):
        fail("Every packaged MCP tool needs a non-empty string name.")
    if len(packaged_names) != len(set(packaged_names)):
        fail("Packaged MCP tool names must be unique.")

    packaged_test_text = PACKAGED_MCP_TESTS.read_text(encoding="utf-8")
    missing_packaged_tests = [name for name in packaged_names if name not in packaged_test_text]
    if missing_packaged_tests:
        fail(
            "Packaged MCP tools without name-level test coverage: "
            + ", ".join(missing_packaged_tests)
        )

    adjacent_test_text = PACKAGED_MCP_ADJACENT_TESTS.read_text(encoding="utf-8")
    missing_adjacent_tests = [name for name in packaged_names if name not in adjacent_test_text]
    if missing_adjacent_tests:
        fail(
            "Packaged MCP tools without adjacent name-level tests: "
            + ", ".join(missing_adjacent_tests)
        )

    return [
        f"mcp-tools:{len(tools)}",
        f"packaged-mcp-tools:{len(packaged_tools)}",
        "mcp-hints:complete",
        "mcp-name-test-coverage:complete",
        "packaged-mcp-name-test-coverage:complete",
        "packaged-mcp-adjacent-name-test-coverage:complete",
    ]


def check_json_files() -> list[str]:
    checked = 0
    for path in (
        ROOT / "plugin.json",
        ROOT / "gemini-extension.json",
        ROOT / ".claude-plugin" / "plugin.json",
        ROOT / ".github" / "self-heal-policy.json",
    ):
        with path.open(encoding="utf-8") as handle:
            json.load(handle)
        checked += 1
    return [f"json-manifests:{checked}"]


def check_plugin_package() -> list[str]:
    manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        fail("plugin.json must use the Agent Plugins 1.0.0 portable schema.")

    name = manifest.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail("plugin.json name must be stable kebab-case.")

    version = manifest.get("version")
    if not isinstance(version, str) or not re.fullmatch(
        r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version
    ):
        fail("plugin.json version must be explicit semantic version text.")

    description = manifest.get("description")
    if not isinstance(description, str) or len(description.strip()) < 40:
        fail("plugin.json description is missing or too vague.")

    skills = sorted(
        path.parent.name
        for path in SKILLS_ROOT.glob("*/SKILL.md")
        if path.is_file()
    )
    if len(skills) != 18:
        fail(f"Expected 18 portable plugin skills, found {len(skills)}.")

    for skill_name in skills:
        text = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
        prefix = text.replace("\r\n", "\n").split("---", 2)
        if len(prefix) < 3:
            fail(f"{skill_name}: SKILL.md is missing YAML frontmatter.")
        frontmatter = prefix[1]
        name_match = re.search(r"(?m)^name:\s*(.+?)\s*$", frontmatter)
        desc_match = re.search(r"(?m)^description:\s*(.+?)\s*$", frontmatter)
        if not name_match or name_match.group(1).strip().strip("\"'") != skill_name:
            fail(f"{skill_name}: frontmatter name must match the directory.")
        if not desc_match or len(desc_match.group(1).strip().strip("\"'")) < 30:
            fail(f"{skill_name}: frontmatter description is missing or too vague.")

    if not PLUGIN_GUIDE.is_file():
        fail("PLUGIN-GUIDE.md is missing.")

    cases = json.loads(PLUGIN_CASES.read_text(encoding="utf-8"))
    positives = cases.get("positive_cases")
    negatives = cases.get("negative_cases")
    if not isinstance(positives, list) or len(positives) != 5:
        fail("Plugin submission preparation requires exactly 5 positive cases.")
    if not isinstance(negatives, list) or len(negatives) != 3:
        fail("Plugin submission preparation requires exactly 3 negative cases.")

    mcp_path = ROOT / "mcp.json"
    if mcp_path.exists():
        mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
        if mcp.get("$schema") != PLUGIN_MCP_SCHEMA:
            fail("Portable plugin mcp.json must use the Agent Plugins MCP schema.")
        servers = mcp.get("mcpServers")
        if not isinstance(servers, dict) or not servers:
            fail("Portable plugin mcp.json must declare at least one MCP server.")
        for server_name, server in servers.items():
            if not isinstance(server, dict):
                fail(f"{server_name}: MCP server declaration must be an object.")
            if server.get("type") != "streamable-http":
                fail(f"{server_name}: public plugin MCP transport must be streamable-http.")
            url = server.get("url")
            if not isinstance(url, str) or not url.startswith("https://"):
                fail(f"{server_name}: public plugin MCP URL must use HTTPS.")
        mcp_status = f"plugin-mcp:{len(servers)}"
    else:
        mcp_status = "plugin-mcp:none-skills-only"

    return [
        f"plugin-version:{version}",
        f"plugin-skills:{len(skills)}",
        "plugin-submission-cases:5+3",
        mcp_status,
    ]


def check_citation_metadata() -> list[str]:
    path = ROOT / "CITATION.cff"
    text = path.read_text(encoding="utf-8")
    required_literals = (
        "cff-version: 1.2.0",
        "title: \"AI Social Media Toolkit\"",
        "type: software",
        "given-names: \"Alptuğ\"",
        "family-names: \"Harun\"",
        "repository-code: \"https://github.com/alptugharun/ai-social-media-toolkit\"",
    )
    missing = [item for item in required_literals if item not in text]
    if missing:
        fail("CITATION.cff is missing required metadata: " + ", ".join(missing))
    return ["citation-metadata:complete"]

def check_actions_pinned() -> list[str]:
    workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    if not workflows:
        fail("No GitHub Actions workflows found.")

    unpinned: list[str] = []
    uses_count = 0
    for workflow in workflows:
        for line_no, line in enumerate(workflow.read_text(encoding="utf-8").splitlines(), 1):
            match = ACTION_REF.match(line)
            if not match:
                continue
            uses_count += 1
            ref = match.group(1)
            if ref.startswith("./") or re.fullmatch(r"[0-9a-f]{40}", ref):
                continue
            unpinned.append(f"{workflow.relative_to(ROOT)}:{line_no} -> {ref}")

    if unpinned:
        fail("Third-party Actions must use immutable 40-char commit SHAs:\n" + "\n".join(unpinned))
    return [f"actions-immutable-refs:{uses_count}"]


def check_workflow_top_level_permissions() -> list[str]:
    workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    if not workflows:
        fail("No GitHub Actions workflows found.")

    unsafe: list[str] = []
    missing: list[str] = []
    for workflow in workflows:
        text = workflow.read_text(encoding="utf-8")
        prefix = text.split("\njobs:", 1)[0]
        match = re.search(r"(?ms)^permissions:\s*(.*?)(?=^\S|\Z)", prefix)
        if not match:
            missing.append(str(workflow.relative_to(ROOT)))
            continue
        block = match.group(0)
        if re.search(r"(?m)^permissions:\s*write-all\s*$", block) or re.search(
            r"(?m)^\s{2}[A-Za-z0-9_-]+:\s*write\s*(?:#.*)?$", block
        ):
            unsafe.append(str(workflow.relative_to(ROOT)))

    if missing:
        fail("Workflows must declare top-level permissions: " + ", ".join(missing))
    if unsafe:
        fail(
            "Top-level workflow permissions must remain read-only; move required writes to the narrowest job: "
            + ", ".join(unsafe)
        )
    return [f"workflow-top-level-readonly:{len(workflows)}"]


def run() -> list[str]:
    checks: list[str] = []
    checks.extend(check_public_files())
    checks.extend(check_mcp_tools())
    checks.extend(check_json_files())
    checks.extend(check_plugin_package())
    checks.extend(check_citation_metadata())
    checks.extend(check_actions_pinned())
    checks.extend(check_workflow_top_level_permissions())
    return checks


def main() -> int:
    try:
        checks = run()
    except (ReadinessError, OSError, SyntaxError, ValueError, json.JSONDecodeError) as exc:
        print(f"READINESS FAIL: {exc}", file=sys.stderr)
        return 1

    print("READINESS PASS")
    for item in checks:
        print(f"- {item}")
    print("- external-reputation:not-asserted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
