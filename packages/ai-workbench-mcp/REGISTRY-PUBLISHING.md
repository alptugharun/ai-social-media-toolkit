# Official MCP Registry Publishing Gate

This directory is the standalone distribution boundary for the repository's read-only AI Workbench MCP server.

The official MCP Registry is preview infrastructure, so re-check its schema and publisher CLI immediately before publication.

## Planned identity

- MCP server name: `io.github.alptugharun/ai-workbench-mcp`
- PyPI package: `alptugharun-ai-workbench-mcp`
- Package transport: `stdio`
- Runtime hint: `uvx`
- First package candidate: `0.1.0a1`
- GitHub release tag for that candidate: `ai-workbench-mcp-v0.1.0a1`
- PyPI workflow: `.github/workflows/publish-ai-workbench-mcp-pypi.yml`

The package README contains the PyPI ownership marker expected by the MCP Registry publication flow:

```text
mcp-name: io.github.alptugharun/ai-workbench-mcp
```

## Do not create server.json yet

A registry file that points to an unpublished package would be operationally false. Create `server.json` only after the exact PyPI version exists and a clean exact-version install succeeds.

## Pre-publish checks

From the repository root:

```bash
python -m unittest discover -s tests -v
python -m pip wheel --no-deps packages/ai-workbench-mcp --wheel-dir .mcp-dist
python -m pip install --no-deps --force-reinstall .mcp-dist/*.whl
```

Then verify the installed console script with an MCP handshake and all three tool contracts.

## PyPI Trusted Publisher setup

The repository uses PyPI Trusted Publishing through GitHub OIDC. No long-lived PyPI API token belongs in GitHub secrets.

For the first publication, configure a **pending GitHub Trusted Publisher** on PyPI using these exact values:

- PyPI project name: `alptugharun-ai-workbench-mcp`
- GitHub owner: `alptugharun`
- GitHub repository: `ai-social-media-toolkit`
- Workflow filename: `publish-ai-workbench-mcp-pypi.yml`
- GitHub environment: `pypi`

A pending publisher does not reserve the project name until it is actually used. Do not announce the package as available before the first publish succeeds.

On GitHub, configure the `pypi` environment with deployment protection appropriate for a release credential boundary. The publish job is the only job granted `id-token: write`.

## First PyPI publication

1. Make sure all tests on the exact release commit are green.
2. Confirm the package version in `pyproject.toml` is `0.1.0a1`.
3. Confirm the PyPI pending publisher and GitHub `pypi` environment match the values above.
4. Publish a GitHub release tagged exactly `ai-workbench-mcp-v0.1.0a1`.
5. The publish workflow verifies the tag/version match, reruns package tests, builds one wheel, inspects its metadata and bundled catalog, then exchanges GitHub OIDC for a short-lived PyPI publishing credential.
6. Confirm the PyPI project page exists and shows version `0.1.0a1`.
7. Confirm the public package metadata/README contains the `mcp-name` marker.
8. Perform the clean exact-version install below before any MCP Registry metadata is created.

## Exact-version verification

After PyPI publication:

```bash
uvx --from alptugharun-ai-workbench-mcp==0.1.0a1 alptugharun-ai-workbench-mcp
```

A real host verification should cover:

1. `initialize`;
2. `notifications/initialized`;
3. `tools/list`;
4. successful `list_prompts`;
5. successful `render_prompt`;
6. successful `get_assistant`;
7. invalid/extra arguments returning bounded errors;
8. no unexpected network, shell, write, or account behavior.

Record the host/version and result in the runtime verification matrix. Package publication by itself is not a host-compatibility claim.

## Future server.json shape

After PyPI publication and clean exact-version verification, generate metadata with the **current** `mcp-publisher init` rather than copying an old schema. The intended fields are:

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

Registry acceptance proves metadata and ownership requirements. It does not prove correctness in every MCP host. Keep real host verification and adoption evidence separate from package/registry publication.
