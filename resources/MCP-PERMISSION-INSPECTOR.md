# MCP Permission Inspector

**A local, dependency-free preflight check for MCP stdio configuration.**

It answers a narrow question before you connect a server:

> **What risky configuration patterns are visible here, and what should I verify next?**

It does **not** launch the MCP server, contact the network, read secret values, or claim runtime safety.

## Why this exists

“Connected” is not the same as “safe” or “verified.”

MCP host configuration can quietly add:

- general-purpose shell execution;
- broad filesystem paths;
- sensitive environment variables;
- remote HTTP(S) targets;
- package runners that auto-install dependencies;
- unpinned packages that make reproduction harder.

This tool makes those boundaries visible before runtime.

## Run it

No install is required:

```bash
python tools/mcp_permission_inspector.py path/to/mcp-config.json
```

Machine-readable output:

```bash
python tools/mcp_permission_inspector.py path/to/mcp-config.json --json
```

Use it as a CI/preflight gate:

```bash
python tools/mcp_permission_inspector.py path/to/mcp-config.json --fail-on high
```

Exit codes:

- `0` — inspection completed and did not cross the configured gate;
- `2` — invalid/unreadable configuration;
- `3` — configured risk threshold was reached.

## Example

Input:

```json
{
  "mcpServers": {
    "example": {
      "command": "npx",
      "args": ["-y", "@vendor/server"],
      "env": {
        "API_KEY": "do-not-commit-real-values"
      }
    }
  }
}
```

The inspector reports the **environment variable name**, never its value, and flags the auto-install/unpinned package pattern.

## What it checks

| Signal | Typical level | Why |
| --- | --- | --- |
| shell launcher / shell evaluation flag | high | broad command-execution surface |
| broad filesystem root | high | excessive local data exposure |
| sensitive env key | medium | credential boundary exists |
| HTTP(S) target | medium | external data/network boundary |
| package runner auto-install | medium | supply-chain/reproducibility friction |
| unpinned package | medium | host may resolve a different build later |
| narrower absolute path | low | filesystem scope should still be reviewed |

## What it deliberately does not claim

Static configuration review cannot prove:

- what an upstream package actually does at runtime;
- whether a server is malicious or safe;
- whether a host grants additional capabilities;
- whether a tool call has side effects;
- whether network destinations are trustworthy;
- whether a package name resolves to the code you intended.

The stronger verification ladder remains:

**inspect config → verify source/version → run local diagnostics → connect host → discover tools → execute bounded call → test failure path → record evidence.**

## Privacy rule

Secret **values are never included in the report**. Only environment-variable names are surfaced so the user can see that a credential boundary exists.

## Acceptance checks

```bash
python -m unittest tests.test_mcp_permission_inspector -v
python tools/mcp_permission_inspector.py --help
```

The test suite covers shell execution, broad paths, secret redaction, package auto-install/unpinned detection and CI threshold behavior.
