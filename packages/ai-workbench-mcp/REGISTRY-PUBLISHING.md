# Official MCP Registry Publishing Gate

This directory is being prepared as the standalone distribution boundary for the repository's read-only AI Workbench MCP server.

The official MCP Registry is currently preview infrastructure. Re-check the official documentation immediately before publishing.

## Planned identity

- MCP server name: `io.github.alptugharun/ai-workbench-mcp`
- PyPI package: `alptugharun-ai-workbench-mcp`
- Package transport: `stdio`
- Runtime hint: `uvx`
- First package candidate: `0.1.0a1`

The package README contains the required PyPI ownership marker:

```text
mcp-name: io.github.alptugharun/ai-workbench-mcp
```

## Do not create server.json yet

A registry file that points to an unpublished package would be syntactically impressive but operationally false. Create `server.json` only after the exact PyPI version exists and a clean install succeeds.

## Pre-publish checks

From the repository root:

```bash
python -m unittest discover -s tests -v
python -m pip wheel --no-deps packages/ai-workbench-mcp --wheel-dir .mcp-dist
python -m pip install --no-deps --force-reinstall .mcp-dist/*.whl
```

Then verify the installed console script with an MCP handshake and all three tool contracts.

## PyPI publication

Publishing credentials and package ownership are account actions. Do not commit tokens.

Recommended release flow:

1. build wheel and sdist from the tagged commit;
2. inspect the archives and run the installed smoke test;
3. publish the exact prerelease to PyPI;
4. confirm the public package page contains the `mcp-name` marker;
5. run the exact-version `uvx` command from a clean environment;
6. only then create the registry metadata.

## Future server.json shape

After PyPI publication, generate metadata with the current `mcp-publisher init` rather than blindly copying an old schema. The intended fields are:

- current official `$schema`;
- `name: io.github.alptugharun/ai-workbench-mcp`;
- repository URL and GitHub source;
- exact server/package version;
- one PyPI package entry using the official PyPI registry;
- `runtimeHint: uvx`;
- `transport.type: stdio`.

Then run:

```bash
mcp-publisher validate server.json
```

Resolve every validation error before authentication or publication.

## Publication is not compatibility proof

Registry acceptance proves metadata/ownership requirements, not correctness in every MCP host. Record real host verification separately in the repository runtime verification matrix and adoption ledger.
