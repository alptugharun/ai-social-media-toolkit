# ChatGPT GPT → Plugin Migration-Aware Guide

Checked against OpenAI Help Center on **2026-09-30**.

## Current product reality

OpenAI's current Help Center states:
- personal ChatGPT accounts, including Free, Go, Plus and Pro, cannot create or publish new GPTs;
- existing GPTs can remain usable/editable when account permissions allow;
- managed Business, Enterprise and Edu workspaces can create/publish GPTs when workspace settings allow;
- OpenAI is moving reusable workflows toward **Plugins**, which combine reusable instructions with connected apps.

Official references:
- https://help.openai.com/en/articles/8554407-create-a-custom-gpt
- https://help.openai.com/en/articles/8554397-creating-and-editing-gpts

## What to publish in this repository

Do not publish "install this new personal GPT" instructions as if every user can create one.

Instead publish a **portable assistant package** containing:

1. Name
2. Description
3. Instructions
4. Conversation starters
5. Knowledge/context checklist
6. Required connected apps/tools
7. Output contract
8. Acceptance tests
9. Migration notes for Plugin use

## Example package

### Name
Creator Research Editor

### Description
Turns supplied sources into a traceable content brief without inventing trend or performance claims.

### Instructions
Use the [Portable Assistant Blueprint](PORTABLE-ASSISTANT-BLUEPRINT.md).

### Conversation starters
- "Turn these three sources into one creator brief."
- "Show me what is evidence vs hypothesis."
- "Audit this draft for unsupported claims."

## Plugin migration checklist

When Plugin creation is available in the target account/workspace:
- move reusable instructions into the Plugin workflow;
- connect only the apps actually needed;
- review app permissions;
- test with non-sensitive sample data;
- verify tool results separately from model text;
- confirm external writes before treating them as completed.

## Acceptance

PASS when a user can reproduce the workflow without relying on undocumented account capabilities.
