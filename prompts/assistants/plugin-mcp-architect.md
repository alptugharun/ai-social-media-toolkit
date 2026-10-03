---
id: assistants-plugin-mcp-architect
title: Plugin & MCP Architect
category: assistants
version: 1.0.0
complexity: advanced
interaction: iterative
models: portable
---

# Plugin & MCP Architect

## Overview

Turn one repeated AI job into the smallest justified architecture: prompt, reusable assistant, Agent Skill, MCP server, plugin, or automation.

## Use When

- deciding whether a ChatGPT/Codex plugin actually needs MCP
- designing a reusable skill + tool package
- turning a manual AI workflow into an installable product
- auditing an idea before writing integration code

## Do Not Use When

- a normal prompt already solves the job
- the workflow has not been proven manually
- you want to add tools only to make the project look more advanced

## Required Inputs

- **USER**: who has the problem
- **JOB**: what they need to finish
- **INPUTS**: data/context they provide
- **RESULT**: observable successful output
- **SYSTEMS**: external apps/data/services, if any
- **WRITE_ACTIONS**: any external changes the system may make
- **HOSTS**: intended environments, if known
- **CONSTRAINTS**: privacy, cost, runtime, dependency or policy limits

## Copy/Paste Prompt

```text
Act as a plugin and MCP systems architect.

USER: [USER]
JOB: [JOB]
INPUTS: [INPUTS]
RESULT: [RESULT]
SYSTEMS: [SYSTEMS]
WRITE_ACTIONS: [WRITE_ACTIONS]
HOSTS: [HOSTS]
CONSTRAINTS: [CONSTRAINTS]

Design the smallest reliable architecture.

Return:

1. Layer decision
   - prompt only
   - reusable assistant
   - Agent Skill
   - MCP server
   - plugin
   - automation
   Explain why each heavier layer is or is not justified.

2. Product contract
   - target user
   - one-sentence promise
   - first useful result
   - required inputs
   - boundaries
   - known limitations

3. Skill contract, if needed
   - trigger/use cases
   - procedure
   - referenced resources
   - output contract
   - completion checks

4. MCP contract, if needed
   - public tool names
   - when each tool is used
   - strict input fields
   - output shape
   - read/write behavior
   - permission/approval requirements
   - bounded errors
   - idempotency/retry/read-back rules

5. Plugin package, if needed
   - included skills
   - included MCP configuration
   - installation assumptions
   - permissions/data handled
   - uninstall/recovery notes

6. Test plan
   - static/schema
   - unit
   - protocol/integration
   - clean install
   - host-level invocation
   - invalid/adversarial input
   - regression cases

7. First-run documentation
   - headline
   - what it does
   - why use it
   - 2-minute quick start
   - expected output
   - troubleshooting
   - limitations

Do not invent host capabilities, account permissions, live connections, package publication, registry acceptance or completed tests.
Flag every assumption that requires current official documentation or a real runtime check.
Prefer read-only architecture until a write action is truly required.
```

## Expected Output

- architecture decision with justification
- bounded product/skill/MCP contracts
- test matrix
- first-run documentation outline
- explicit assumptions and verification steps

## Quality Gate

- [ ] The user/job/result are concrete
- [ ] The lightest viable layer is chosen
- [ ] MCP is not added without a tool/data need
- [ ] Write actions have approval and verification rules
- [ ] Tool contracts are testable
- [ ] Host/account claims are not invented
- [ ] Test plan includes negative and host-level checks
- [ ] First-use value is visible before architecture detail

## Example Input

```text
USER: content researcher
JOB: reuse evidence-backed research prompts inside multiple AI hosts
INPUTS: question and labeled source notes
RESULT: rendered prompt or assistant blueprint
SYSTEMS: none
WRITE_ACTIONS: none
HOSTS: Cursor and other stdio-capable MCP clients
CONSTRAINTS: read-only, no network calls, Python 3.10+
```

## Troubleshooting

- **Architecture is too large** → remove every layer that does not change the user result
- **Tool list keeps growing** → merge tools around user jobs, not internal implementation steps
- **Write workflow is risky** → add approval, idempotency and read-back before implementation
- **Docs sound impressive but vague** → put one runnable first-use example before feature lists
- **“Works everywhere” claim appears** → replace it with named host/version evidence

## Next Step

Turn the accepted architecture into a narrow implementation, run the full test ladder, and record package/registry/host evidence separately.
