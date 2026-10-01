# Start Here — prove the toolkit works before you configure anything

**Do not read the whole repository first. Get one reproducible result, then choose the layer you actually need.**

The toolkit covers prompts, reusable assistants, Agent Skills, API request previews, MCP examples, automation and creator workflows. You do not need all of them.

Created by **Alptuğ Harun**.

## Your first 2 minutes: one command, no API key

### Requirements

- Python **3.10+**
- this repository downloaded or cloned
- a terminal opened in the repository root

No provider account, API key, package install or social-media login is required for this check.

macOS / Linux:

```bash
python tools/first_run_check.py
```

Windows:

```powershell
py -3 -X utf8 tools/first_run_check.py
```

### What this checks

The script reproduces the first things a new user is likely to try:

1. loads the prompt/assistant catalog;
2. renders a filled evidence prompt;
3. previews an xAI/Grok API request **without making a network call**;
4. dry-runs one Agent Skill installation without changing your real skill folders;
5. exports the same assistant job for ChatGPT, Claude, Gemini and Grok;
6. runs the existing two-minute creator proof.

A successful run ends with:

```text
FIRST-RUN CHECK: PASS
No API key, network call, account login or third-party Python package was required.
```

If you do not get that result, stop there and use [Troubleshooting](downloads/AI-WORKBENCH-GUIDE.md#troubleshooting) or [Support](SUPPORT.md). Do not add API keys to debug an offline failure.

## Choose one lane — not the whole toolkit

| I want to… | Start here | What you should get |
| --- | --- | --- |
| **Try a useful AI workflow now** | [10 Quick Wins](QUICK-WINS.md) | one copyable workflow with a quality check |
| **Build a reusable ChatGPT / Claude / Gemini / Grok assistant** | [AI Workbench guide](downloads/AI-WORKBENCH-GUIDE.md) | provider-specific instruction package from one portable job |
| **Install Agent Skills** | [Installation](docs/INSTALLATION.md) | a dry-run plan first, then an explicit install path |
| **Connect local read-only tools with MCP** | [MCP guide](integrations/MCP-PLUGIN-GUIDE.md) | a local stdio configuration and three bounded tools |
| **Analyze creator/social signals** | [Two-Minute Demo](examples/TWO-MINUTE-DEMO.md) | synthetic scoring output you can compare with the documented result |
| **Use my own CSV/export** | [CSV input contract](docs/CSV-INPUTS.md) | exact required columns plus validation before scoring |
| **Understand everything A–Z** | [Complete field manual](docs/HOW-TO-USE-EVERYTHING.md) | the full map of tools, skills, automations and limitations |

## Before using real data or a paid API

Keep the first run synthetic. Then:

1. read the exact input contract for the tool you chose;
2. preview the request or use `--dry-run` when available;
3. confirm the expected output;
4. set provider credentials only in the documented environment variable;
5. use `--live` only when you intentionally want a network request;
6. review the result before any downstream action.

**Downloading this repository does not grant account access, publish content, install a hosted assistant or create a background bot.**

## 15-Minute Quick Start

## 15-Minute Quick Start

### 1. Define the objective

Choose one primary goal:

- Reach
- Education
- Authority
- Traffic
- Lead generation
- Brand positioning
- Community growth

### 2. Choose the relevant framework

- AI content production → [AI Content Workflow](AI-CONTENT-WORKFLOW.md)
- Social media planning → [Social Media Content System](SOCIAL-MEDIA-CONTENT-SYSTEM.md)
- Canva + generative AI → [Canva + AI Workflow](CANVA-AI-WORKFLOW.md)
- Pinterest discovery → [Pinterest Research Framework](PINTEREST-RESEARCH-FRAMEWORK.md)
- Prompt systems → [Prompt Engineering Framework](PROMPT-ENGINEERING-FRAMEWORK.md)
- Reels production → [Reels Production Workflow](REELS-PRODUCTION-WORKFLOW.md)
- Automation → [Content Automation Architecture](CONTENT-AUTOMATION-ARCHITECTURE.md)
- AI tool selection → [AI Tool Comparison Resources](AI-TOOL-COMPARISON-RESOURCES.md)
- Search and digital authority → [Digital Visibility Checklist](DIGITAL-VISIBILITY-CHECKLIST.md)

### 3. Choose a practical starter

If you want a non-developer starting point, open the [Creator Materials Hub](downloads/README.md):

- [Creator Prompt Starter Kit](downloads/CREATOR-PROMPT-STARTER-KIT.md)
- [AI Assistant Blueprint Starter Pack](downloads/AI-ASSISTANT-BLUEPRINTS.md)
- [Creator Automation Starter Pack](downloads/CREATOR-AUTOMATION-STARTER-PACK.md)
- [Pinterest Growth Starter Kit](downloads/PINTEREST-GROWTH-STARTER-KIT.md)
- [Reels Production Starter Kit](downloads/REELS-PRODUCTION-STARTER-KIT.md)
- [Canva + AI Content Starter Kit](downloads/CANVA-AI-CONTENT-STARTER-KIT.md)
- [AI Creator OS Starter Map](downloads/AI-CREATOR-OS-STARTER.md)

Or copy a task-specific template:

- [Content Brief Template](templates/CONTENT-BRIEF-TEMPLATE.md)
- [Reels Production Template](templates/REELS-PRODUCTION-TEMPLATE.md)
- [Pinterest Research Sheet](templates/PINTEREST-RESEARCH-SHEET.csv)
- [Prompt Template](templates/PROMPT-TEMPLATE.md)
- [AI Tool Comparison Matrix](templates/AI-TOOL-COMPARISON-MATRIX.csv)
- [Digital Visibility Audit Checklist](downloads/DIGITAL-VISIBILITY-AUDIT-CHECKLIST.md)

### 4. Fill only the fields required for the task

Do not over-document simple work.

Use enough structure to remove ambiguity.

### 5. Apply human review

Check:

- Accuracy
- Brand fit
- Platform fit
- Visual quality
- Copyright concerns
- AI artifacts
- CTA
- Final objective

### 6. Publish and measure

Match measurement to the original objective.

Examples:

**Reach** → Reach + Views

**Education** → Watch Time + Saves

**Traffic** → Outbound Clicks

**Conversion** → Leads + Sales

---

## Recommended Paths

### Reels

Content Brief → Reels Production Template → Human Review → Publish → Measure

### Pinterest

Pinterest Research Sheet → Keyword Cluster → Pin Concept → Design → Destination URL → Measure

### AI-Assisted Social Content

Content Brief → Prompt Template → AI Draft → Canva / Edit → Human Review → Publish

### Automation

Manual Workflow → Content Automation Architecture → Approval Layer → Automation → Monitoring

---

## Real Example

See:

[AI Social Media Toolkit Case Study](case-studies/AI-SOCIAL-MEDIA-TOOLKIT-CASE-STUDY.md)

It documents how this repository itself was structured as a public expertise and workflow library.

---

## Core Principle

Start with the task, not the tool.

Use AI to accelerate execution.

Keep strategy, quality control and final responsibility human-led.

---

Part of the  
[AI Social Media Toolkit](https://github.com/alptugharun/ai-social-media-toolkit)
