# AI Assistant Blueprints

**Reusable assistant designs for ChatGPT/OpenAI, Claude, Gemini and Grok — with platform differences kept explicit.**

## Start here

| Platform | Resource | Status |
| --- | --- | --- |
| ChatGPT / OpenAI | [GPT → Plugin migration-aware guide](CHATGPT-GPT-PLUGIN-MIGRATION.md) | product behavior checked 2026-09-30 |
| Claude | [Claude Project Blueprint](CLAUDE-PROJECT-BLUEPRINT.md) | project setup pattern |
| Gemini | [Gemini Gem Blueprint](GEMINI-GEM-BLUEPRINT.md) | Gem setup pattern |
| Grok / xAI | [Grok Assistant Blueprint](GROK-ASSISTANT-BLUEPRINT.md) | reusable instruction + API pattern |
| Portable | [Portable Assistant Blueprint](PORTABLE-ASSISTANT-BLUEPRINT.md) | provider-neutral |

## Rule

A reusable assistant should own **one repeated job** and expose:
- purpose;
- inputs;
- instructions;
- knowledge/context;
- starter requests;
- output contract;
- failure rules;
- acceptance tests.

Do not claim that a blueprint is deployed simply because the Markdown exists.
