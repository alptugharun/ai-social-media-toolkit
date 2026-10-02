# AI Workbench MCP

A small, dependency-free, **read-only** stdio MCP server that exposes Alptuğ Harun's bundled AI Workbench prompt and assistant catalog.

<!-- mcp-name: io.github.alptugharun/ai-workbench-mcp -->

## Scope

This package exposes three local tools:

- `list_prompts` — list bundled prompt templates and assistant blueprints;
- `render_prompt` — render a local prompt template using supplied strings;
- `get_assistant` — return a local assistant blueprint for ChatGPT, Claude, Gemini, Grok, or portable Agent Skill format.

The MCP tools do **not** access the network, run a model, execute shell commands, modify files, access accounts, or publish content.

## Local install from this repository

From the repository root:

```bash
python -m pip install --no-deps ./packages/ai-workbench-mcp
alptugharun-ai-workbench-mcp
```

The process speaks MCP over stdio, so normally an MCP host launches it rather than a human typing into it.

## Exact-version install after PyPI publication

The package is not claimed as published until the exact version is visible on PyPI and a clean-machine install test passes.

After publication, the intended immutable invocation is:

```bash
uvx --from alptugharun-ai-workbench-mcp==0.1.0a1 alptugharun-ai-workbench-mcp
```

Do not copy that into production host configuration until the package actually exists at that version.

## Security model

Every public tool declares:

- `readOnlyHint: true`
- `destructiveHint: false`
- `idempotentHint: true`
- `openWorldHint: false`

These annotations describe behavior; they do not replace input validation. The server rejects undeclared top-level arguments, unknown tool names, invalid initialization order, non-object arguments, and over-sized input lines.

## Registry publication gate

The official MCP Registry metadata is added as `server.json` only after:

1. this package is published to the official PyPI registry;
2. the README ownership marker above is present in the published package page;
3. the exact version installs with `uvx`;
4. initialize → tools/list → each tools/call path passes from a clean environment;
5. `mcp-publisher validate` accepts the final metadata.

See `REGISTRY-PUBLISHING.md` in this package directory.
