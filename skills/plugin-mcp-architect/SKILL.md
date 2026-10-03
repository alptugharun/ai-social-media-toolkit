---
name: plugin-mcp-architect
description: Designs the smallest justified AI integration for a real user job, choosing between prompts, reusable assistants, Agent Skills, MCP servers, plugins and automation. Use when planning, reviewing or teaching installable AI workflows and their tests.
license: MIT
metadata:
  version: 0.1.0
  author: Alptuğ Harun
---

# Plugin & MCP Architect

Design installable AI capability from the user job outward.

Do not begin by assuming that every idea needs a plugin, MCP server or autonomous agent.

## Read first

- [AI Builder Path](../../learning/AI-BUILDER-PATH.md)
- [Integrations Hub](../../integrations/README.md)
- [Plugin & MCP Architect Prompt](../../prompts/assistants/plugin-mcp-architect.md)

## Trigger

Use this skill when the user asks to:

- build or design a ChatGPT/Codex plugin;
- decide whether a workflow needs MCP;
- package instructions as an Agent Skill;
- convert a manual AI process into a reusable assistant or integration;
- teach someone how prompts, skills, MCP and plugins fit together;
- review an AI integration for unnecessary complexity;
- define installation, testing or troubleshooting for an AI product.

Do not use it merely because the user mentions AI.

## Step 1 — write the job contract

Extract or infer only what is safe to infer:

- target user;
- job-to-be-done;
- input;
- observable result;
- systems/data involved;
- external write actions;
- intended host/runtime;
- cost/privacy/dependency constraints.

If a missing fact changes permissions, external effects or architecture, mark it as unresolved instead of inventing it.

## Step 2 — choose the lightest layer

Evaluate in this order:

1. prompt;
2. reusable assistant;
3. Agent Skill;
4. MCP server;
5. plugin;
6. automation.

Stop at the first layer that can reliably produce the required result.

### Prompt

Choose when the job needs instructions and supplied context only.

### Reusable assistant

Choose when the same bounded instructions/context are reused frequently.

### Agent Skill

Choose when an agent should load a reusable procedure or domain workflow.

### MCP server

Choose when the model needs structured access to tools or data.

### Plugin

Choose when skills and/or MCP should be packaged as one reusable product.

### Automation

Choose only after the manual workflow is reliable and a trigger/state loop creates real value.

## Step 3 — design boundaries

For every architecture, state:

- what it can do;
- what it cannot do;
- what data it reads;
- what it writes;
- what requires approval;
- what depends on the host/account;
- what must be verified against current official documentation.

Never treat a package manifest, registry listing or connected-server status as proof that every tool call works.

## Step 4 — design public interfaces

For skills, define:

- trigger;
- procedure;
- references;
- output;
- completion checks.

For MCP tools, define:

- tool name;
- user-facing purpose;
- strict inputs;
- bounded result;
- errors;
- read/write semantics;
- idempotency/retry behavior;
- approval/read-back for writes.

Avoid one tool per internal implementation step.

## Step 5 — build the test ladder

Require the smallest applicable set:

1. static/schema validation;
2. unit tests;
3. integration/protocol test;
4. clean install/build test;
5. host-level tool invocation;
6. invalid/missing/adversarial input;
7. regression for every fixed failure;
8. cross-host verification when portability is claimed.

A skipped test is not a pass.

A local test is not a published-package verification.

A registry status is not a host test.

## Step 6 — write installable documentation

The public first screen should answer:

- What is this?
- Who is it for?
- What useful result can I get quickly?
- Why should I trust it?
- How do I install/run it?

Then include:

- exact requirements;
- step-by-step install;
- first command/request;
- expected output;
- troubleshooting;
- limitations;
- uninstall/recovery path where relevant.

Use a concrete result before feature lists.

## Step 7 — adoption test

Before adding more features, ask:

- can a stranger understand the promise in 10 seconds?
- can they reach first value in a few minutes?
- can they verify it worked?
- are permissions obvious?
- is there a useful example?
- is the failure path documented?
- is there evidence beyond the maintainer's claim?

If not, improve first-use friction before expanding scope.

## Output contract

Return:

### Architecture decision
- chosen layer(s)
- rejected heavier layers and why

### Product contract
- user
- job
- first result
- inputs
- boundaries
- limitations

### Interfaces
- skill and/or MCP contracts

### Installation
- requirements
- exact steps
- first-use example
- expected output

### Test matrix
| Test | Purpose | Status/evidence |
| --- | --- | --- |

### Failure log
List discovered failures, root cause, fix and regression when implementation/testing is part of the task.

### Adoption copy
- one headline
- one-sentence promise
- three evidence-backed reasons to try it

## Review gate

- [ ] no fake capabilities
- [ ] no unnecessary MCP/plugin layer
- [ ] no undocumented write behavior
- [ ] current host/account assumptions identified
- [ ] install path is reproducible
- [ ] public interfaces are testable
- [ ] negative tests exist
- [ ] fixed bugs have regression coverage
- [ ] limitations are visible
- [ ] adoption claims are evidence-backed

## Core principle

**Make the job obvious, the boundary narrow, the first result fast, and the proof easy to reproduce.**
