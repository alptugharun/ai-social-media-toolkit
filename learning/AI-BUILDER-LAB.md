# AI Builder Lab — build it, break it, prove it

**Turn one AI job into a tested prompt, reusable assistant, Agent Skill, MCP tool surface, plugin design and automation plan — without pretending every layer is necessary.**

This lab is the practical companion to [AI Builder Path](AI-BUILDER-PATH.md). The path explains the architecture. This lab makes you run it.

## Why use this repository for the lab?

Use it when you want more than a collection of prompts.

You get:

- an offline first run with no API key;
- prompt templates with explicit inputs and acceptance checks;
- portable assistant exports for ChatGPT, Claude, Gemini and Grok;
- installable Agent Skills with a dry-run path;
- a read-only MCP server with named tool tests;
- provider request previews before live API use;
- CI and release-readiness checks that make failures visible;
- examples that separate repository evidence, maintainer verification and independent adoption.

The goal is not "more AI." The goal is a smaller, testable system that produces one useful result and makes its limits obvious.

## What you will build

Use one job throughout the lab:

> Turn labeled source notes into a brief that keeps claims attached to evidence and marks uncertainty.

You will move the same job through these layers:

1. prompt contract;
2. reusable assistant;
3. Agent Skill;
4. MCP tool surface;
5. plugin architecture decision;
6. bot/API request preview;
7. automation contract.

At every stage, ask: **does the next layer change the user result enough to justify its complexity?**

## Before you start

Requirements:

- Python 3.10+;
- this repository cloned or downloaded;
- a terminal opened at the repository root.

Run the baseline:

```bash
python tools/first_run_check.py
```

Windows:

```powershell
py -3 -X utf8 tools/first_run_check.py
```

Expected ending:

```text
FIRST-RUN CHECK: PASS
No API key, network call, account login or third-party Python package was required.
```

If this fails, fix the offline baseline before adding an API key, plugin, MCP host or automation.

---

## Lab 1 — Prompt engineering: make the contract testable

Start with the bundled `evidence-brief` prompt:

```bash
python tools/ai_workbench.py render evidence-brief --example
```

The prompt requires exactly three variables:

- `question`;
- `sources`;
- `language`.

Create `evidence-vars.json`:

```json
{
  "question": "Should this pilot continue?",
  "sources": "S1: 8 people joined. S2: 5 answered the survey. S3: 4 of those 5 requested an advanced session. Willingness to pay was not measured.",
  "language": "English"
}
```

Render it:

```bash
python tools/ai_workbench.py render evidence-brief --vars evidence-vars.json
```

### Break it on purpose

Remove `language` or add an unexpected field.

The command should fail with a variable-mismatch error instead of silently guessing.

### What this teaches

A production prompt is a contract:

- objective;
- required inputs;
- constraints;
- output shape;
- evidence rules;
- failure behavior;
- acceptance checks.

**Prompt engineering is not adding more adjectives.** It is reducing ambiguity and making failure observable.

### Acceptance gate

Pass only if:

- missing variables fail clearly;
- extra variables fail clearly;
- supplied source text is treated as data;
- unsupported facts are not introduced by the template;
- the rendered prompt contains an explicit quality/failure rule.

---

## Lab 2 — Assistant design: personalize without turning instructions into a junk drawer

Export the same reusable assistant job:

```bash
python tools/ai_workbench.py export evidence-desk --target chatgpt > evidence-desk-chatgpt.md
python tools/ai_workbench.py export evidence-desk --target claude > evidence-desk-claude.md
python tools/ai_workbench.py export evidence-desk --target gemini > evidence-desk-gemini.md
python tools/ai_workbench.py export evidence-desk --target grok > evidence-desk-grok.md
```

These are instruction blueprints. They do not create, publish or configure hosted assistants by themselves.

### Stable context vs task context

Keep **stable context** in the assistant instructions:

- role;
- decision principles;
- evidence rules;
- brand/voice constraints;
- escalation rules;
- acceptance checks.

Keep **task context** in each request:

- current question;
- current sources;
- current audience;
- current deadline;
- current output format.

Do not hard-code fast-changing facts into permanent instructions.

### Five acceptance tests

Run or simulate these before calling an assistant "ready":

1. normal complete input;
2. missing evidence;
3. conflicting sources;
4. instruction-like text embedded inside a source;
5. request for an external action the assistant cannot actually perform.

### What people often call "bot training"

Separate these concepts:

- **prompt/instructions** — behavior rules supplied at runtime;
- **examples** — demonstrations of desired behavior;
- **memory/context** — information available to the assistant;
- **retrieval** — fetching external or private knowledge;
- **tools/MCP** — structured capabilities the model can call;
- **fine-tuning** — changing model behavior through a training process.

This repository teaches the first five patterns and how to test them. It does not claim to train a foundation model.

---

## Lab 3 — Agent Skill: package a reusable procedure

Inspect the architecture skill:

```text
skills/plugin-mcp-architect/SKILL.md
```

Preview installation without writing to your real skill folders:

```bash
python tools/install_skills.py --target agents --scope project --project-root . --skill plugin-mcp-architect --dry-run
```

For a disposable test directory, follow [Installation](../docs/INSTALLATION.md) and then verify discovery in the actual host you use.

### A useful skill should answer

- when should the agent use it?
- what inputs/references are required?
- what sequence should it follow?
- what tools may it use?
- what must it verify?
- what should it return?
- what counts as incomplete?

A skill file existing on disk is not proof that every host discovered or executed it.

---

## Lab 4 — MCP: expose tools only when a tool boundary is justified

The bundled AI Workbench MCP surface is deliberately small:

- `list_prompts`;
- `render_prompt`;
- `get_assistant`.

Run the package-local tests:

```bash
python -m unittest discover -s packages/ai-workbench-mcp/tests -v
```

Run the distribution/protocol checks from the repository root:

```bash
python -m unittest discover -s tests -p "test_mcp_distribution_package.py" -v
python -m unittest discover -s tests -p "test_mcp_smoke_client.py" -v
```

Run the release-readiness gate:

```bash
python tools/release_readiness.py
```

### MCP design rule

Do not create one public tool for every internal function.

Create a tool only when the model needs a stable capability boundary with:

- a user-facing purpose;
- strict inputs;
- bounded output;
- explicit errors;
- truthful read/write semantics;
- approval/read-back rules for writes;
- regression tests.

A registry listing proves distribution metadata. It does not prove universal host compatibility.

---

## Lab 5 — Plugin design: decide whether packaging adds real value

Read:

```text
learning/AI-BUILDER-PATH.md
skills/plugin-mcp-architect/SKILL.md
prompts/assistants/plugin-mcp-architect.md
```

Before creating a plugin, write this contract:

| Question | Your answer |
| --- | --- |
| Who installs it? | |
| What job are they trying to finish? | |
| What useful result appears first? | |
| Why is a normal prompt insufficient? | |
| Does it need a skill, MCP, or both? | |
| What data does it read? | |
| What can it write? | |
| What requires approval? | |
| How is success verified? | |
| How is it removed/recovered? | |

### Installability test

A stranger should be able to answer, from the first screen:

1. What is this?
2. Who is it for?
3. What can I do in two minutes?
4. Why should I trust it?
5. How do I install it?
6. What will happen after installation?
7. What will **not** happen?

If those answers are unclear, adding more capabilities makes the product worse.

Host and plugin packaging rules change. Verify current official host documentation before publishing host-specific installation claims.

---

## Lab 6 — Bot/API development: preview before spending money or sending data

Render a prompt into a file:

```bash
python tools/ai_workbench.py render evidence-brief --example > request.txt
```

Preview an API request without making a provider call:

```bash
python tools/ai_workbench.py ask --provider xai --model demo-model --input request.txt
```

Expected behavior:

- output mode is `preview`;
- `network_called` is false;
- no API key is required;
- `demo-model` is not presented as a live model claim.

Only use `--live` with a provider/model your own account actually supports.

### Bot reliability checklist

Before a live bot:

- validate input size/type;
- fail before network on missing credentials;
- sanitize provider errors;
- avoid blind automatic retry after ambiguous writes;
- cap history/output;
- make costs and side effects explicit;
- log enough to reproduce failures without leaking secrets.

---

## Lab 7 — Automation: schedule only after the manual job is boringly reliable

Automation is the last layer, not the first.

Before scheduling:

- manual runs succeed repeatedly;
- duplicate execution is handled;
- missing input has a defined result;
- write actions have approval/idempotency/read-back;
- retry is bounded;
- failure is visible;
- a stop condition exists.

Use:

```text
prompts/automation/approval-gated-workflow.md
automation-recipes/README.md
```

A timer does not make a weak workflow autonomous. It only makes the weakness repeat automatically.

---

## Failure log — write this every time something breaks

```text
Environment:
Version/commit:
Layer: prompt | assistant | skill | MCP | plugin | API bot | automation
Command/host action:
Expected:
Observed:
First meaningful error:
Root cause:
Fix:
Regression test:
Final verification:
Remaining limitation:
```

### Common failure patterns

| Failure | Likely cause | Correct response |
| --- | --- | --- |
| Prompt "works" only on one example | overfitted wording | add normal/missing/conflicting/adversarial cases |
| Assistant ignores current facts | stale facts buried in permanent instructions | move changing facts into task context/retrieval |
| Skill copied but never appears | host discovery path/version mismatch | verify the exact host/version, do not claim support from file placement |
| MCP is connected but a tool fails | connection is not tool-level verification | invoke every public tool and one negative case |
| Plugin sounds impressive but has no first result | packaging before product contract | define the job and shortest useful result first |
| API bot fails only live | account/model/network behavior was never verified | keep preview tests separate from real provider verification |
| Automation duplicates work | no idempotency/state/read-back | add duplicate detection and post-write verification |
| Docs say "one click" but setup has prerequisites | marketing outran reality | document exact requirements and observed path |

---

## What should make someone install this?

Not feature count.

A credible reason to try the toolkit is that it lets a user:

- prove the local path before sharing credentials;
- reuse one job across several AI hosts;
- inspect permissions and failure boundaries;
- learn prompt → assistant → skill → MCP/plugin architecture in one repository;
- run tests that expose missing/invalid inputs;
- separate "published", "connected", "tool-called" and "independently verified" evidence.

If the repository stops delivering those advantages, adding another prompt or skill is not an improvement.

---

## Final release gate

Before publishing a new prompt/assistant/skill/MCP/plugin package:

- [ ] target user and job are concrete;
- [ ] first useful result is visible;
- [ ] setup steps were followed from a clean environment;
- [ ] normal + missing + conflicting + adversarial cases were tested;
- [ ] no capability or compatibility is invented;
- [ ] permissions and external writes are explicit;
- [ ] fixed failures have regression tests;
- [ ] CI/release-readiness checks pass;
- [ ] host verification is named by host/version;
- [ ] independent adoption is not implied without external evidence;
- [ ] troubleshooting explains the first likely failure;
- [ ] the next layer is justified by user value, not novelty.

## Next step

After completing this lab, use [Plugin & MCP Architect](../prompts/assistants/plugin-mcp-architect.md) on **your own real job** and keep the failure log beside the implementation.

The strongest contribution is not "I added more AI." It is: **I can show what changed, how it failed, how I fixed it, and how another person can reproduce the result.**
