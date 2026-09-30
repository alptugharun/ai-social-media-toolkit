# 10 Quick Wins — Useful AI Results in Under 10 Minutes

> **No giant setup. Pick one job, get one useful result, then decide whether to go deeper.**

This page is for first-time visitors who do not want to understand the whole repository before getting value.

## 1. Turn messy sources into a traceable brief

**Use:** [Source Synthesis](prompts/research/source-synthesis.md)

**Best for:** articles, release notes, reports, research notes.

**Do this:**
1. open the prompt;
2. replace QUESTION / AUDIENCE / SOURCES;
3. paste into ChatGPT, Claude, Gemini or Grok;
4. check the quality gate.

**You should get:** supported facts, disagreements, uncertainty and next verification steps.

---

## 2. Check whether a “trend” is actually current

**Use:** [Trend Evidence Auditor](prompts/research/trend-evidence-auditor.md)

**Best for:** social trends, AI trends, creator opportunities.

**You should get:** verified signals, weak signals, stale/seasonal risk and TEST / WATCH / SKIP.

**Important:** do not invent platform-wide growth percentages.

---

## 3. Build a reusable AI assistant

**Use:** [Narrow AI Assistant Builder](prompts/assistants/assistant-builder.md)

Then export the result into:

- [Portable Assistant Blueprint](assistants/PORTABLE-ASSISTANT-BLUEPRINT.md)
- [Claude Project](assistants/CLAUDE-PROJECT-BLUEPRINT.md)
- [Gemini Gem](assistants/GEMINI-GEM-BLUEPRINT.md)
- [Grok/xAI](assistants/GROK-ASSISTANT-BLUEPRINT.md)
- [ChatGPT / Plugin migration-aware path](assistants/CHATGPT-GPT-PLUGIN-MIGRATION.md)

**You should get:** instructions, starter requests, output contract, failure rules and acceptance tests.

---

## 4. Run an AI assistant locally without an API key

```bash
python tools/multi_provider_assistant.py \
  --provider mock \
  --prompt "Turn these notes into a concise action brief"
```

**You should get:** a local mock response path proving the CLI works.

Want a real provider later? Use your own key + model and read [Bot Starters](bots/README.md).

---

## 5. Inspect an API request before sending it

```bash
python tools/multi_provider_assistant.py \
  --provider openai \
  --model YOUR_MODEL \
  --prompt "Summarize this" \
  --dry-run
```

The same pattern works for `anthropic`, `xai` and `gemini`.

**You should get:** endpoint + redacted headers + payload.

**Why this matters:** you can inspect what would be sent before a paid/live request.

---

## 6. Design an automation without losing human control

**Use:** [Approval-Gated Automation Designer](prompts/automation/approval-gated-workflow.md)

**You should get:**
- trigger;
- state/checkpoint;
- deduplication key;
- approval gate;
- write step;
- read-back verification;
- retry policy;
- rollback/stop condition.

Then compare it with [Automation Recipes](automation-recipes/README.md).

---

## 7. Build a 30–35 second Reel package

**Use:** [Reels Director](prompts/creator/reels-director.md)

**You should get:**
- first-3-second hook;
- timed spoken script;
- shot/B-roll plan;
- AI visual brief;
- CapCut notes;
- cover title;
- CTA;
- QA.

---

## 8. Turn one Pinterest opportunity into seven distinct Pins

**Use:** [Pinterest 7-Pin Cluster Builder](prompts/creator/pinterest-cluster.md)

**You should get seven roles:**
Hero · Educational · Checklist · Comparison · Seasonal · Search-led · Visual-discovery.

Each should have a different intent and destination logic.

---

## 9. Remove generic AI writing texture

**Use:** [Brand Voice Humanizer](prompts/brand/voice-humanizer.md)

**Best for:** LinkedIn, captions, articles, scripts and brand copy.

**You should get:** revised copy + change note + factual claims that still need verification.

---

## 10. Audit an AI output before publishing

**Use:** [AI Output Quality Auditor](prompts/evaluation/output-quality-auditor.md)

It returns **PASS / REVISE / BLOCK** for:
- factual support;
- objective fit;
- clarity;
- originality;
- platform fit;
- unsupported claims;
- rights/privacy risk;
- AI artifacts;
- CTA/destination fit;
- measurement readiness.

---

# Want a guided path?

Choose one:

- [Prompt → Assistant → Skill → API → MCP → Automation](learning/README.md)
- [Complete AI Ecosystem Hub](AI-ECOSYSTEM-HUB.md)
- [Creator Materials](downloads/README.md)
- [How to Use Everything](docs/HOW-TO-USE-EVERYTHING.md)

If one of these saved you time, star the repository so you can find future workflows and releases again.
