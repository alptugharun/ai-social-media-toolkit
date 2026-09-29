# Grok / xAI Assistant Blueprint

Use this guide for a reusable Grok instruction package or a developer-side xAI assistant workflow.

## What this is

A blueprint for one repeated job, such as:
- trend evidence review;
- research synthesis;
- creator brief generation;
- output QA.

## What this is not

A one-shot API request is not an autonomous always-running bot.

## Instruction package

Start from [PORTABLE-ASSISTANT-BLUEPRINT.md](PORTABLE-ASSISTANT-BLUEPRINT.md).

Define:
1. one job;
2. required inputs;
3. output contract;
4. evidence rules;
5. stop conditions;
6. acceptance tests.

## API path

For developer use, xAI documents a REST inference API and recommends current integrations use the appropriate modern endpoint for the task.

Official reference:
https://docs.x.ai/developers/rest-api-reference/inference

See [Bot Starters](../bots/README.md) for the provider-neutral starter architecture.

## Verification

Mark a workflow **provider verified** only after a real xAI call is tested with the user's own account, model access and billing state.

Do not commit credentials to the repository.
