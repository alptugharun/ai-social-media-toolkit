# AI Ecosystem Hub

**One place for prompts, assistants, Agent Skills, plugins/MCP, bot starters, automation recipes and practical AI learning.**

This hub expands the toolkit beyond social media without pretending that every platform integration is already live.

## Explore by job

| I want to… | Start here |
| --- | --- |
| copy a reusable prompt | [Prompt Library](prompts/README.md) |
| build a reusable AI assistant | [Assistant Blueprints](assistants/README.md) |
| install Agent Skills | [Agent Skills](skills/README.md) |
| understand plugins / MCP / connected apps | [Integrations Hub](integrations/README.md) |
| learn to build prompts → skills → MCP → plugins | [AI Builder Path](learning/AI-BUILDER-PATH.md) |
| prototype an API-based assistant or bot | [Bot Starters](bots/README.md) |
| automate a repeatable workflow | [Automation Recipes](automation-recipes/README.md) |
| learn from beginner to working system | [Learning Paths](learning/README.md) |
| see creator-focused examples | [Creator Materials](downloads/README.md) |

## Pick a provider in 60 seconds

The same useful job should not require relearning the whole system every time you switch models.

| Provider | Reusable assistant path | API / bot path | Portable layer |
| --- | --- | --- | --- |
| **ChatGPT / OpenAI** | [ChatGPT migration-aware assistant path](assistants/CHATGPT-GPT-PLUGIN-MIGRATION.md) | [Bot Starters](bots/README.md) | prompts → assistant contract → Agent Skill / MCP when needed |
| **Claude / Anthropic** | [Claude Project blueprint](assistants/CLAUDE-PROJECT-BLUEPRINT.md) | [Bot Starters](bots/README.md) | prompts → Project instructions → Agent Skill / MCP when needed |
| **Gemini** | [Gemini Gem blueprint](assistants/GEMINI-GEM-BLUEPRINT.md) | [Bot Starters](bots/README.md) | prompts → Gem instructions → portable workflow / MCP when needed |
| **Grok / xAI** | [Grok assistant blueprint](assistants/GROK-ASSISTANT-BLUEPRINT.md) | [Bot Starters](bots/README.md) | prompts → reusable instructions → portable workflow / API when needed |

### Try the same job across four providers

Use one assistant definition and export provider-specific instruction packages:

```bash
python tools/ai_workbench.py export evidence-desk --target chatgpt
python tools/ai_workbench.py export evidence-desk --target claude
python tools/ai_workbench.py export evidence-desk --target gemini
python tools/ai_workbench.py export evidence-desk --target grok
```

These are instruction packages, not claims that a hosted assistant was created. Compare the outputs, note provider-specific limitations, and keep the underlying job contract portable.

## Platform lanes

- **OpenAI / ChatGPT** — prompts, Responses API starter patterns, existing GPT workflows and migration-aware Plugin guidance.
- **Claude / Anthropic** — project instructions, knowledge context, Agent Skills and plugin-compatible workflows.
- **Gemini** — Gems, reusable instructions, knowledge-backed workflows and API patterns.
- **Grok / xAI** — reusable instructions plus xAI API starter patterns.
- **Portable** — provider-neutral prompt contracts, Agent Skills, MCP patterns and approval-gated automations.

## Quality rule

A resource is not complete because the file exists.

Every public asset should answer:

1. What result does it create?
2. Who should use it?
3. What is required before starting?
4. What are the exact steps?
5. What can I copy and try?
6. What should a useful output contain?
7. What can go wrong?
8. How do I verify the result?
9. What should I do next?

## Evidence labels

- **Blueprint** — instructions/design, not live-provider verified.
- **Offline tested** — local logic/tests passed without calling a paid provider.
- **Provider verified** — a real provider/runtime call was tested and the evidence is documented.
- **Production ready** — requires stronger operational evidence than one successful call.

Do not silently promote one evidence level into another.
