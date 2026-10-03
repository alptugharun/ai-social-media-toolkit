# AI Workbench MCP publication status

This directory is the monorepo source copy of the read-only AI Workbench MCP server.

The focused public distribution boundary is the standalone repository:

https://github.com/alptugharun/ai-workbench-mcp

## Verified state — 2026-10-03

- MCP server name: `io.github.alptugharun/ai-workbench-mcp`
- PyPI package: `alptugharun-ai-workbench-mcp`
- published version: `0.1.0a1`
- transport: stdio
- PyPI publication: GitHub OIDC Trusted Publishing
- release signing: keyless Sigstore
- official MCP Registry: published, status `active`
- package clean-install/protocol verification: completed
- maintainer-run real-host verification: completed in Cursor 3.20.21 for all three public tools
- independent external host verification: still wanted

## Public install

```bash
python -m pip install "alptugharun-ai-workbench-mcp==0.1.0a1"
```

Then configure a stdio-capable MCP host to launch:

```text
alptugharun-ai-workbench-mcp
```

Host configuration fields and locations vary. Use the current documentation for the host being tested.

## Monorepo validation

From the toolkit repository root:

```bash
python -m unittest discover -s tests -p "test_mcp_distribution_package.py" -v
python -m unittest discover -s tests -p "test_mcp_smoke_client.py" -v
python -m unittest discover -s packages/ai-workbench-mcp/tests -v
python tools/release_readiness.py
```

The package source is also built and smoke-tested in the CI matrix.

## Evidence boundaries

Keep these claims separate:

1. **source tests** — repository code passed local/CI checks;
2. **published package** — exact PyPI version exists;
3. **registry state** — official MCP Registry accepted the metadata/ownership;
4. **host verification** — a named host/version actually invoked the tools;
5. **independent adoption** — another user reproduced the result.

One level does not automatically prove the next.

## Real-host evidence

The current maintainer-run Cursor verification covered:

- `list_prompts`
- `render_prompt`
- `get_assistant`

The detailed record lives in the standalone repository:

https://github.com/alptugharun/ai-workbench-mcp/blob/main/HOST-VERIFICATION.md

This is real host evidence, but it is not an independent third-party endorsement or a claim of universal compatibility.

## Security model

The public tools remain read-only and declare explicit MCP behavior hints.

The runtime does not intentionally provide:

- arbitrary filesystem access;
- shell execution;
- provider/model calls;
- account modification;
- content publishing.

Registry publication does not weaken that boundary.

## Future releases

For a new version:

1. update the package/version deliberately;
2. run the full tests and wheel smoke checks;
3. publish through the trusted release path;
4. clean-install the exact public version;
5. validate/update Registry metadata;
6. record host verification separately;
7. never describe a local build as a published release.

The standalone repository is the source of truth for public package/Registry release state.
