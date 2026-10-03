# AI Workbench MCP

**A tiny, dependency-free, read-only MCP server for reusable prompt templates and assistant blueprints.**

<!-- mcp-name: io.github.alptugharun/ai-workbench-mcp -->

It exists for one job: let an MCP-capable host discover a small local AI Workbench catalog without giving the server network, shell, account or filesystem-write access.

> **Status:** alpha package candidate. The source package is CI-tested. Do not treat it as a published PyPI or official MCP Registry package until the exact public artifact is linked here.

## What you get

| Tool | Input | Result | Side effects |
| --- | --- | --- | --- |
| `list_prompts` | none | available prompts + assistant blueprints | none |
| `render_prompt` | prompt ID + string variables | rendered instruction text | none |
| `get_assistant` | assistant ID + target | portable host-specific instruction blueprint | none |

Supported assistant output targets are currently `chatgpt`, `claude`, `gemini`, `grok`, and `skill`.

The server **does not call a model**. It returns local text from the bundled catalog.

## Try it from this repository

Requirements:

- Python 3.10+
- a checkout of this repository

Install the local package:

```bash
python -m pip install --no-deps ./packages/ai-workbench-mcp
```

Run the same installed-package smoke check used by CI:

```bash
python packages/ai-workbench-mcp/examples/smoke_client.py
```

A successful check prints:

```text
MCP SMOKE PASS
- server: alptugharun-ai-workbench-mcp
- version: 0.1.0a1
- tools: get_assistant, list_prompts, render_prompt
- side-effects: read-only contract verified
```

That proves the installed console command can initialize and expose the expected local tool contract. It is **not** proof that every MCP host is compatible.

## Connect it to a local MCP host

The host should launch:

```text
alptugharun-ai-workbench-mcp
```

A generic stdio launcher shape is:

```json
{
  "command": "alptugharun-ai-workbench-mcp",
  "args": []
}
```

Exact configuration fields and file locations vary by host. Follow the current documentation for the host you are actually using instead of copying another product's config path.

After connection, verify the host discovers all three tools before relying on it.

## Security model

Every public tool declares:

```text
readOnlyHint: true
destructiveHint: false
idempotentHint: true
openWorldHint: false
```

The runtime imports only Python standard-library modules needed for JSON-RPC, local package resources and input handling.

The MCP tools do not:

- access the network;
- execute shell commands;
- read arbitrary user files;
- write files;
- read environment credentials;
- modify accounts;
- publish content;
- call OpenAI, Anthropic, Google, xAI or another model provider.

Input validation rejects unknown tool names, undeclared top-level arguments, invalid initialization order, non-object arguments and oversized input lines.

Annotations describe expected behavior; the tests and implementation are the actual enforcement evidence.

## How it is tested

The repository CI builds a wheel, installs that wheel, launches the installed console script and runs the public smoke client on:

- Ubuntu 24.04
- Ubuntu 26.04
- Windows Server 2025

The test suite also checks:

- bundled catalog parity;
- exact package/version metadata;
- all three tool names;
- explicit MCP annotations;
- prompt rendering;
- assistant target handling;
- stdio initialization;
- invalid tool/input paths;
- absence of network/process imports in the packaged server.

Run the package tests locally:

```bash
python -m unittest discover -s tests -p "test_mcp_distribution_package.py" -v
python -m unittest discover -s tests -p "test_mcp_smoke_client.py" -v
```

## What can fail?

**`alptugharun-ai-workbench-mcp` is not found**

Make sure the same Python environment used for installation owns the active scripts directory:

```bash
python -m pip show alptugharun-ai-workbench-mcp
```

Then reopen the terminal if your platform added a scripts directory to PATH during installation.

**The host starts the process but shows no tools**

Verify the installed package independently first:

```bash
python packages/ai-workbench-mcp/examples/smoke_client.py
```

If that passes, record the host name/version and its MCP configuration. That is host-specific evidence rather than a package failure.

**A prompt render reports missing or extra variables**

Call `list_prompts` first and supply exactly the template variables required by that prompt. Variable mismatches fail instead of silently filling unknown values.

**You expected the MCP to contact an AI model**

It will not. This server is intentionally local and read-only. Use the returned instruction in the model/host you chose.

## Exact-version install after PyPI publication

The first package candidate is `0.1.0a1`.

Only after that exact version is actually published and verified will this become a valid public install command:

```bash
uvx --from alptugharun-ai-workbench-mcp==0.1.0a1 alptugharun-ai-workbench-mcp
```

Until then, use the repository-local install above.

## Official MCP Registry gate

A `server.json` is intentionally **not** added just to look registry-ready.

The publication sequence is:

1. publish the exact signed package to PyPI;
2. clean-install that exact public version;
3. repeat initialize → `tools/list` → named tool calls;
4. generate metadata using the current MCP publisher/schema;
5. run `mcp-publisher validate server.json`;
6. publish only after validation succeeds;
7. test the registry-installed package in a real MCP host.

See [REGISTRY-PUBLISHING.md](REGISTRY-PUBLISHING.md).

## Independent verification wanted

Maintainer CI is useful, but another user running the package in a real host is stronger evidence.

If you can test it, use:

→ [Independent runtime verification wanted — AI Workbench MCP on a real host](https://github.com/alptugharun/ai-social-media-toolkit/issues/110)

A useful report includes the host/version, OS/Python version, exact setup, discovered tools, one successful call, one invalid-input result and the first point of friction.

## License

This standalone package is MIT licensed. See [LICENSE](LICENSE).
