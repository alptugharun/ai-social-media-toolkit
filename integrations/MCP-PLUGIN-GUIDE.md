# MCP & Plugin Guide

## Use MCP when

A compatible AI client needs a structured way to discover and call tools or retrieve context from another system.

Good examples:
- approved document search;
- a business API;
- a deterministic internal utility;
- a scoped database query.

## Do not use MCP when

- a plain prompt solves the job;
- a local script is enough;
- the service already has a safer native connector;
- you cannot define permissions and failure behavior.

## Plugin-style workflow

```text
user request
→ reusable instructions
→ connected tool selection
→ tool result
→ model synthesis
→ approval gate if needed
→ external write
→ read-back verification
```

## Minimum integration contract

Document:
- tool name;
- purpose;
- authentication requirement;
- allowed reads;
- allowed writes;
- sensitive data;
- idempotency;
- expected errors;
- approval requirement;
- read-back method.

## Security rules

Never:
- commit secrets;
- widen permissions just to make a workflow pass;
- retry an unknown write blindly;
- confuse "tool configured" with "action completed";
- treat a model-generated tool call as evidence that the external system changed.

## Next step

Prototype one read-only integration first, then add writes only when verification and rollback are explicit.
