# MCP Preflight — External Configuration Validation

Validation date: **2026-10-09**

Purpose: test the local-only MCP configuration preflight against configuration examples published by unrelated upstream projects, without starting their servers or contacting their endpoints.

## Case 1 — package runner / unpinned package

Upstream documentation:

- project: `mnemox-ai/idea-reality-mcp`
- pinned source: https://github.com/mnemox-ai/idea-reality-mcp/blob/83281b4cf7b66da8e80ad6e2527a154cefdaa480/llms.txt
- documented configuration:

```json
{
  "mcpServers": {
    "idea-reality": {
      "command": "uvx",
      "args": ["idea-reality-mcp"]
    }
  }
}
```

Observed result:

- overall risk: **MEDIUM**
- `package-runner`: LOW
- `unpinned-package`: MEDIUM
- recommendation: pin an exact reviewed version for reproducible host configuration.

Interpretation: this is a reproducibility/supply-chain review signal. It is **not** a maliciousness verdict.

## Case 2 — loopback HTTP

Upstream documentation:

- project: `dannote/figma-use`
- pinned source: https://github.com/dannote/figma-use/blob/7bfa9ba3ea7c56c5c8ca6cd5085c6e56a0735027/MCP.md
- documented configuration:

```json
{
  "mcpServers": {
    "figma-use": {
      "url": "http://localhost:38451/mcp"
    }
  }
}
```

Observed result:

- overall risk: **LOW**
- `loopback-http`: LOW
- recommendation: keep the endpoint loopback-only; use HTTPS if traffic leaves the machine.

Interpretation: the tool distinguishes local HTTP from cleartext remote traffic.

## Windows parser regression found during this validation

The first maintainer run saved the examples with Windows PowerShell's UTF-8 encoding, which included a UTF-8 BOM. The parser rejected the files before inspection.

Fix:

- config reading changed from `utf-8` to `utf-8-sig`;
- normal UTF-8 remains supported;
- a regression test now covers BOM-bearing JSON.

Targeted result after the fix: **52 tests PASS**.

## Evidence boundary

This validation proves that the inspector can parse and explain these two documented configuration shapes in the maintainer's environment. It does **not** prove runtime MCP safety, upstream package behavior, external adoption, or production use.
