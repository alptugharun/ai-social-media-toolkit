# MCP Permission Inspector

**A local, dependency-free preflight check for MCP client configuration.**

It answers one narrow question before you connect a server:

> **What risky configuration patterns are visible here, and what should I verify next?**

It does **not** launch configured servers, contact their endpoints, execute shell commands, inspect package contents, or claim runtime safety.

## v1 scope

Supported in v1:

- JSON MCP client config;
- stdio servers with `command` / `args`;
- remote HTTP/SSE-style entries with `url`;
- mixed configs containing both local and remote servers;
- `env` and `headers` credential-boundary review;
- text and JSON output;
- CI threshold exits.

Intentionally **not** in v1:

- JSONC or YAML parsing;
- automatic discovery of every client's config location;
- package download/SAST/dependency scanning;
- live MCP handshake or tool execution;
- config drift/rug-pull monitoring;
- SARIF;
- "safe" / "unsafe" verdicts.

Those are larger products. This tool stays a **first-connect config preflight** until real usage proves a broader need.

## Why this exists

“Connected” is not the same as “safe” or “verified.”

MCP configuration can silently introduce:

- general-purpose shell execution;
- broad filesystem paths;
- hardcoded credentials;
- authorization headers;
- cleartext remote endpoints;
- package runners that auto-install dependencies;
- unpinned package versions;
- a local launcher that bridges to a network target.

The inspector makes those boundaries visible **before runtime**.

## Run it

No install is required:

```bash
python tools/mcp_permission_inspector.py path/to/mcp-config.json
```

Machine-readable output:

```bash
python tools/mcp_permission_inspector.py path/to/mcp-config.json --json
```

CI/preflight gate:

```bash
python tools/mcp_permission_inspector.py path/to/mcp-config.json --fail-on high
```

Exit codes:

- `0` — inspection completed and did not cross the configured gate;
- `2` — invalid/unreadable/ambiguous configuration;
- `3` — configured risk threshold was reached.

## Examples

### Local stdio

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-filesystem@1.2.0",
        "/workspace/project",
        "--read-only"
      ]
    }
  }
}
```

### Remote

```json
{
  "mcpServers": {
    "remote": {
      "url": "https://mcp.example.com/mcp",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "${MCP_AUTH_HEADER}"
      }
    }
  }
}
```

The inspector reports credential **key names**, not values.

A literal credential value is treated more severely than a placeholder such as `${GITHUB_TOKEN}`. Header templates such as `Bearer ${env:TOKEN}` are treated as credential boundaries, not as hardcoded secrets.

## What it checks

| Signal | Typical level | Why |
| --- | --- | --- |
| shell launcher / shell evaluation flag | high | broad command-execution surface |
| broad filesystem root | high | excessive local data exposure |
| literal credential in env/header | high | secret is embedded in config |
| execution-influencing env (`LD_PRELOAD`, `NODE_OPTIONS`, etc.) | high | process/module loading can change before server startup |
| cleartext remote HTTP outside loopback | high | transport confidentiality risk |
| sensitive env/header placeholder | medium | credential boundary exists |
| remote HTTPS endpoint | medium | external trust/data boundary |
| package runner auto-install | medium | supply-chain/reproducibility friction |
| unpinned package | medium | host may resolve a different build later |
| narrower absolute path | low | filesystem scope should still be reviewed |
| loopback HTTP | low | local transport still deserves review |

## Privacy contract

The report must never echo secret values from:

- environment variables;
- HTTP headers;
- `--token=value` / `--api-key value`-style arguments;
- URL userinfo;
- credential-like URL query parameters;
- JSON output;
- finding messages or error text produced from inspected values.

If a regression causes a secret to reappear in any output channel, the build should fail.

## Parsing contract

v1 accepts **strict UTF-8 JSON only**.

It rejects:

- malformed JSON;
- duplicate JSON keys;
- non-object top-level values;
- oversized configs above the documented limit;
- invalid server/env/header/args shapes.

JSONC and YAML are deferred rather than parsed inconsistently.

## What it deliberately does not claim

Static configuration review cannot prove:

- what an upstream package actually does at runtime;
- whether a server is malicious or safe;
- whether a host grants extra capabilities;
- whether a tool call has side effects;
- whether a remote endpoint is trustworthy;
- whether a package name resolves to the code you intended;
- whether a configuration stays unchanged after approval.

The stronger verification ladder remains:

**inspect config → verify source/version → run local diagnostics → connect host → discover tools → execute bounded call → test failure path → record evidence.**

## Heavy-test evidence

The inspector has regression coverage for bugs found during development, including:

- dynamic-import/dataclass test loading;
- Unix root-path normalization;
- secret re-leak through secondary finding text;
- remote-only entries that previously aborted mixed configs;
- package/path false positives after pinned `npx` packages.

The dedicated workflow exercises:

- Ubuntu, Windows and macOS;
- Python 3.10–3.13;
- targeted adversarial tests;
- safe/vulnerable config fixtures;
- deterministic fuzzing;
- large-config stress;
- the full repository regression suite.

Run locally:

```bash
python -m unittest tests.test_mcp_permission_inspector -v
python tests/stress_mcp_permission_inspector.py
python -m unittest discover -s tests -p "test_*.py"
```

## Product gate

Do not split this into another standalone repository yet.

First prove that people actually use the preflight:

1. external users scan real configs;
2. at least one real issue/false-positive report improves a rule;
3. repeat usage or CI integration appears;
4. users value the narrow first-connect explanation instead of asking for a full security scanner.

If those signals do not appear, pivot or kill the tool instead of adding features.
