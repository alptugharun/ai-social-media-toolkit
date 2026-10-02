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

For this repository's local MCP server:

- all three tools now declare the four trust hints explicitly;
- the hints are locked by tests;
- the server is read-only and local;
- no network, shell, account, file-write or provider call is exposed by those MCP tools.

### Publisher action

After claiming the listing, review each finding against the current commit and submit corrections where the scanner is still showing an older snapshot. A publisher claim is an identity/account step and must be performed by the repository owner.

Do not ask for a grade increase that the evidence does not support. Ask for **re-evaluation of the current commit** and identify the exact fixed findings.

Suggested note:

> The current main branch explicitly declares readOnlyHint, destructiveHint, idempotentHint and openWorldHint for every MCP tool, and tests enforce all four fields as booleans. Please re-evaluate the latest commit and update any findings that still reflect an older snapshot. If the remaining grade cap is adoption/reputation-based, please leave that distinction visible rather than treating it as an unresolved code defect.

## OpenAI / ChatGPT plugin review readiness

Current OpenAI plugin guidance expects tool descriptions to match behavior and requires explicit `readOnlyHint`, `destructiveHint` and `openWorldHint`; `idempotentHint` is also useful where truthful.

The local server is intentionally a protocol example, not a hosted remote plugin. A future public ChatGPT plugin submission needs a remotely reachable Streamable HTTP MCP endpoint, deployment, privacy/data-handling review and host-level testing. Do not call the local stdio example a published ChatGPT plugin.

Official references:

- https://developers.openai.com/plugins/plan/tools
- https://developers.openai.com/plugins/build/mcp-server
- https://developers.openai.com/plugins/deploy/app-review

## Official MCP Registry

The official MCP Registry uses `server.json` metadata and verifies publish/package ownership. This repository does **not** add a cosmetic `server.json` before the MCP server has a real distributable package or remote URL.

The publication gate is:

1. choose the MCP product boundary;
2. package it as a versioned artifact (for example PyPI/npm) **or** deploy a supported remote endpoint;
3. add a valid `server.json` using the current schema;
4. validate with `mcp-publisher`;
5. authenticate the namespace;
6. publish;
7. verify the exact published version can be installed and called from a real MCP host.

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

The repository includes an OpenSSF Scorecard workflow and CodeQL. Scorecard results can still be held back by repository/account settings that code changes alone cannot fix, such as branch protection, security settings or maintainer practices.

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
