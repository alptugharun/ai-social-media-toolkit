# AI Learning Paths

**Learn by building one useful artifact at every level.**

Start with the detailed [AI Builder Path](AI-BUILDER-PATH.md) when you want the full prompt → assistant → Agent Skill → MCP → plugin → automation decision and testing workflow.

## 1 — Prompt Fundamentals

Outcome: write prompts with explicit inputs, task, output and QA.

- Read [Prompt Library Standard](../prompts/PROMPT-STANDARD.md).
- Run [Source Synthesis](../prompts/research/source-synthesis.md).
- Compare the answer with the quality gate.
- Change one variable and rerun.

## 2 — Reusable Assistants

Outcome: turn repeated instructions into a narrow assistant.

- Use [Assistant Builder](../prompts/assistants/assistant-builder.md).
- Convert it into the [Portable Assistant Blueprint](../assistants/PORTABLE-ASSISTANT-BLUEPRINT.md).
- Adapt it to Claude Project, Gemini Gem, Grok or an eligible ChatGPT workspace.
- Run five acceptance tests.

## 3 — Agent Skills

Outcome: install and use one portable skill.

- Read [Agent Skills](../skills/README.md).
- Install one skill.
- Run its example request.
- Record runtime/version and first friction point.

## 4 — API Assistants

Outcome: understand provider API calls without pretending a script is autonomous.

- Run the mock provider.
- Inspect one request builder.
- Add your own provider key/model locally.
- Run a real call.
- Record provider verification separately.

## 5 — Integrations & MCP

Outcome: decide whether something should be a prompt, skill, plugin, MCP integration or automation.

- Read [Integrations Hub](../integrations/README.md).
- Write the minimum integration contract.
- Define permissions and failure behavior.
- Prototype read-only first.

## 6 — Automation

Outcome: automate a proven manual process.

- Start from [Approval-Gated Automation Designer](../prompts/automation/approval-gated-workflow.md).
- Use an [Automation Recipe](../automation-recipes/README.md).
- Add deduplication, approval and read-back.
- Schedule only after manual runs are reliable.
