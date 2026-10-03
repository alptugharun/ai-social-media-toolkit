# Trust, Discovery & External Review

This repository treats third-party ratings, registries and directory listings as **external evidence**, not something that can be manufactured inside the repo.

## What is already machine-checkable

Run:

```bash
python tools/release_readiness.py
python -m unittest discover -s tests -v
```

The readiness audit checks repository evidence that can be proven offline:

- public security, contribution, support, license, roadmap and adoption files exist;
- every local MCP tool has a non-empty description and object input schema;
- every MCP tool explicitly declares `readOnlyHint`, `destructiveHint`, `idempotentHint` and `openWorldHint` as booleans;
- every MCP tool name is referenced by tests;
- core JSON manifests parse successfully;
- third-party GitHub Actions are pinned to immutable 40-character commit SHAs.

It deliberately does **not** claim stars, users, registry acceptance, M8ven grade, OpenSSF score, live monitoring or provider compatibility.

## M8ven

M8ven grades combine code findings, verification depth and reputation/adoption. Their public listings state that new projects can remain capped at **C / Emerging** until adoption is earned, even when no concerning code findings remain.

### Current repository state — observed 2026-10-03

- publisher ownership is verified;
- GitHub Live Monitoring is connected;
- Sandbox Verified is present;
- the public grade moved from the earlier **C / 74** snapshot to **B / 89** after current-code verification;
- the remaining visible quality suggestion at that snapshot was tool-name test coverage;
- PR #112 added direct name-level tests for every packaged MCP tool and strengthened the release-readiness gate; its cross-platform validation and CodeQL checks passed before merge.

For the repository's local and packaged MCP surfaces:

- all public tools declare the four trust hints explicitly;
- tests lock those hints to explicit booleans;
- the package is read-only and dependency-free at runtime;
- no network, shell, account, filesystem-write or provider call is exposed by the MCP tools.

Treat any future M8ven grade as dated external evidence. Live Monitoring can re-score after pushes, and reputation/adoption remains outside the repository's direct control.

### Publisher review rule

Review every new finding against the exact commit M8ven says it scanned. Dispute only stale or incorrect findings with file-level evidence. Do not ask for a grade increase unsupported by the scanner or by adoption evidence.

## OpenAI / ChatGPT plugin review readiness

Current OpenAI plugin guidance expects tool descriptions to match behavior and requires explicit `readOnlyHint`, `destructiveHint` and `openWorldHint`; `idempotentHint` is also useful where truthful.

The local server is intentionally a protocol example, not a hosted remote plugin. A future public ChatGPT plugin submission needs a remotely reachable Streamable HTTP MCP endpoint, deployment, privacy/data-handling review and host-level testing. Do not call the local stdio example a published ChatGPT plugin.

Official references:

- https://developers.openai.com/plugins/plan/tools
- https://developers.openai.com/plugins/build/mcp-server
- https://developers.openai.com/plugins/deploy/app-review

## Official MCP Registry

The official MCP Registry uses `server.json` metadata and verifies publish/package ownership. This repository does **not** add a cosmetic `server.json` before the MCP server has a real distributable package or remote URL.

The standalone product boundary now exists at `packages/ai-workbench-mcp`. The remaining publication gate is:

1. publish the exact prerelease version to PyPI through the existing Trusted Publishing workflow;
2. verify a clean exact-version install and MCP handshake from the published artifact;
3. generate a valid `server.json` using the current registry schema;
4. validate with `mcp-publisher`;
5. authenticate the `io.github.alptugharun` namespace;
6. publish to the official registry;
7. verify the registry install in a real MCP host and record the dated result.

Official references:

- https://github.com/modelcontextprotocol/registry
- https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/generic-server-json.md

## Glama, Smithery and other directories

Treat each directory as a distribution surface, not a quality shortcut.

Before submitting anywhere:

- use the same canonical repository and version;
- keep the description truthful and non-comparative;
- point installation instructions to a versioned artifact or reproducible command;
- avoid claiming compatibility that has not been tested in that host;
- verify the directory is showing the latest release, not a stale branch snapshot;
- keep one evidence ledger for external runtime tests.

A listing is useful only if a visitor can install, run and understand the result.

## OpenSSF Scorecard

The repository includes an OpenSSF Scorecard workflow and CodeQL. Scorecard results can still be held back by repository/account settings that code changes alone cannot fix, such as branch protection, security settings or maintainer practices. The current repository ruleset API returned no configured rulesets during the 2026-10-03 audit, so default-branch protection remains an explicit account-level hardening task.

Never weaken CI just to raise a score. Prefer:

- immutable Action SHAs;
- least-privilege workflow permissions;
- dependency update automation;
- code scanning;
- review before merging externally supplied code;
- protected release/publish credentials;
- reproducible tests and versioned releases.

## Adoption is the remaining hard problem

External systems can distinguish a clean repo from an adopted repo. Stars alone are weak evidence.

Higher-quality adoption evidence includes:

- an independent user running the two-minute demo;
- a real host verifying one Agent Skill end-to-end;
- an external bug report with a reproduction;
- a third-party pull request that improves a real workflow;
- a registry install followed by successful MCP tool calls;
- a public case study that states exactly what was tested.

Record only evidence that actually happened in `ADOPTION.md`.

## Release rule

Do not publish a new feature merely because it sounds novel.

For any new assistant, skill, MCP tool, bot or automation:

1. define one user job;
2. inspect direct alternatives;
3. build the smallest useful version;
4. add invalid-input and failure-path tests;
5. run the readiness audit and full test suite;
6. document setup, limits and troubleshooting;
7. test in the intended host;
8. publish only after the relevant checks pass;
9. collect real feedback;
10. improve the proven bottleneck before adding another lane.
