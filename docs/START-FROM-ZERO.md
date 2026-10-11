# Start From Zero — What Everything Is, Why It Exists, and How to Use It

This guide is for someone who opens the profile and thinks:

> “This looks useful, but I do not know what an Agent Skill, MCP server, prompt blueprint, local tool, release asset or proof ladder is. What should I actually click first?”

You do **not** need to understand the whole repository.

The rule is:

**pick one job → use the smallest layer that solves it → get one reproducible result → only then add complexity.**

---

## 1. The 60-second map

| Thing | Plain-language meaning | Use it when… | Do not use it when… |
| --- | --- | --- | --- |
| **Prompt** | A reusable instruction | one AI task needs structure and QA | you need a tool/account action |
| **Assistant Blueprint** | A reusable AI role/configuration | the same job repeats across sessions/providers | one prompt is enough |
| **Agent Skill** | An installable procedure an AI agent can load | a repeatable workflow should be available inside an agent | you have not inspected the skill or runtime |
| **MCP Server** | A local/remote program that exposes tools to an AI host | the AI needs callable tools with explicit schemas/permissions | a text instruction can solve the job |
| **Automation** | A job that runs later/repeatedly/conditionally | the manual workflow is already understood and repeatable | the underlying workflow is still unclear |
| **Creator Tool** | A normal app focused on one creator job | a UI is faster than talking to an agent | the app does not match the job |
| **Trust Tool** | A tool that makes permissions/risk/evidence visible | before installing/connecting powerful AI extensions | as a substitute for runtime security monitoring |

### One important distinction

**Prompt ≠ Assistant ≠ Agent Skill ≠ MCP ≠ Automation.**

They can work together, but they solve different layers of the problem.

A repository with 50 features is not automatically more useful. Start with the smallest one that solves the job.

---

# 2. What is on Alptuğ Harun's GitHub profile?

## AI Social Media Toolkit — the main hub

### What is it?

The umbrella project. It connects:

- structured prompts;
- assistant blueprints;
- Agent Skills;
- creator workflows;
- local scoring tools;
- MCP examples;
- automation patterns;
- live Creator Frame Studio;
- security/trust tooling;
- release/download evidence.

### Why would I use it?

Use the Toolkit when you do **not yet know which AI layer you need**, or when you want one place to test the public system.

### Absolute beginner path

1. Open the repository.
2. Do **not** read every file.
3. If you do not want a terminal, open Creator Frame Studio first.
4. If you are comfortable with a terminal, clone/download the repo.
5. Run:

```bash
python tools/first_run_check.py
```

Windows alternative:

```powershell
py -3 -X utf8 tools/first_run_check.py
```

### Expected result

The last lines should include:

```text
FIRST-RUN CHECK: PASS
No API key, network call, account login or third-party Python package was required.
```

### If it fails

Do not add API keys to fix an offline test.

Record:

- operating system;
- Python version;
- exact command;
- first error;
- PASS / FAIL / BLOCKED.

Then use `START-HERE.md`, `SUPPORT.md` or Real User Lab issue #178.

### What a PASS does **not** prove

It does not prove:

- every MCP host works;
- every provider integration is live;
- real users adopted the project;
- the project will make money;
- a creator workflow will go viral.

It proves the documented local first-run path behaved as expected.

---

# 3. Creator Context Builder — build the shared briefing once

## What problem does it solve?

Without a shared context, every workflow starts like this:

> Who are you?  
> What is your audience?  
> What tone do you want?  
> What should I avoid?  
> Which metric is current?

That creates repeated briefing and brand drift.

Creator Context Builder creates one reusable context file.

## What makes it different?

It separates:

- **VERIFIED** — facts explicitly supplied or source-backed;
- **PREFERENCE** — user-approved choices;
- **OBSERVED** — patterns found in approved samples;
- **HYPOTHESIS** — useful interpretations that still need confirmation.

Time-sensitive metrics should also include a source and date/window.

## Install only this skill

```bash
npx skills add alptugharun/ai-social-media-toolkit --skill creator-context-builder
```

Or read the skill directly:

`skills/creator-context-builder/SKILL.md`

## First request to try

> Build my reusable creator context from these current facts and three approved writing samples. Label verified facts, preferences, observed patterns and hypotheses separately. Do not store secrets. Flag stale metrics.

## Expected output

A file such as:

`.agents/creator-context.md`

with:

- identity;
- positioning;
- evidence ledger;
- audience;
- platforms;
- content system;
- voice;
- approved sample signals;
- visual rules;
- workflow preferences;
- approval/risk boundaries;
- current objectives;
- stale/recheck list;
- open questions.

## What it must never do

- infer sensitive traits from writing;
- store passwords/API keys/session cookies;
- silently treat an old metric as current;
- replace an explicit preference with an AI guess.

A filled synthetic example is in `examples/CREATOR-CONTEXT-EXAMPLE.md`.

---

# 4. Creator Ops — “I know the goal, but I do not know which tool to use”

Creator Ops is the routing layer.

Use it when you say:

- “Turn this research into a Reel.”
- “I need a Pinterest growth workflow.”
- “I have comments; what should I learn from them?”
- “I want to monetize this workflow but I do not want to jump straight to SaaS.”

## First request

> My objective is [OBJECTIVE]. My platform is [PLATFORM]. Here is my evidence [EVIDENCE]. Route this through the minimum number of skills and stop before public publishing.

## Expected result

You should see:

1. objective;
2. evidence/input;
3. chosen route;
4. ready-to-use artifact;
5. review gate;
6. measurement/next test.

If the result immediately writes content without understanding the job, the routing failed.

---

# 5. Creator Frame Studio — easiest no-code first product

## What is it?

A browser-local social-image framing tool.

It helps you check one visual across:

- Instagram 4:5;
- Reels/Story 9:16;
- Pinterest 2:3;
- YouTube 16:9;
- other defined framing profiles.

It also supports editable text and deterministic preflight checks.

## Why use it?

A visual that looks good at 4:5 can break at 9:16.

The tool lets you see that **before** publishing.

## Fastest test

1. Open the live demo:
   https://alptugharun.github.io/ai-social-media-toolkit/
2. Add a non-sensitive test image.
3. Change format.
4. Add one text layer.
5. Read the preflight/status card.
6. Export and inspect the file.

## Privacy boundary

The app is designed to operate browser-local and its CSP blocks network connections.

Still use a throwaway/non-sensitive test image for first evaluation.

## What it is not

- not an AI image generator;
- not Canva;
- not a social publisher;
- not a promise that platform safe areas will never change;
- not an automatic “quality score”.

---

# 6. AI Workbench MCP — what MCP means in this project

## What is MCP?

Model Context Protocol lets an AI host discover structured tools/resources from an MCP server.

Think of it as:

**AI host ↔ explicit tool contract ↔ local/remote server**

The server decides what tools exist. The host/model chooses when to call them.

## What does AI Workbench MCP do?

It deliberately exposes only three read-only tools:

- `list_prompts` — discover valid prompt/assistant IDs;
- `render_prompt` — fill one prompt template;
- `get_assistant` — return one assistant blueprint for a target host.

It does **not**:

- access the internet;
- execute a shell;
- write files;
- sign into accounts;
- call OpenAI/Anthropic/Google/xAI;
- publish content.

## Zero-to-first-result

Install the exact published alpha:

```bash
python -m pip install "alptugharun-ai-workbench-mcp==0.1.0a2"
```

Check the package before editing any MCP host config:

```bash
alptugharun-ai-workbench-mcp --doctor
```

Then configure the host using the repository's host-specific guide.

For the maintainer-tested path, use the Cursor guide.

## Verification ladder

Do not jump from “installed” to “works everywhere.”

Verify in order:

**installed → doctor pass → protocol handshake → host discovery → tool invocation → expected output**

That ladder is part of the trust model.

---

# 7. Agent Skill Safety Auditor — inspect before install

## Why does this exist?

An Agent Skill can contain instructions/scripts that:

- execute shell commands;
- make network requests;
- read environment variables;
- touch SSH/browser credential paths;
- run install lifecycle hooks;
- perform destructive filesystem operations.

A skill can be useful and still deserve inspection.

## What the auditor does

It runs an offline static scan and returns evidence for manual review.

It does **not** upload the target to an AI model.

## Beginner setup

```bash
git clone https://github.com/alptugharun/agent-skill-safety-auditor.git
cd agent-skill-safety-auditor
python -m pip install -e .
```

Audit a skill folder:

```bash
skill-audit path/to/skill
```

Machine-readable output:

```bash
skill-audit path/to/skill --format json
```

CI gate:

```bash
skill-audit path/to/skill --fail-on high
```

## Read the result correctly

- **LOW** — no configured heuristic finding was detected;
- **MODERATE** — inspect network/process/env/dependency behavior;
- **HIGH** — powerful behavior deserves manual review;
- **BLOCK** — reserved for stronger concrete evidence.

**LOW does not mean “certified safe.”**

Static inspection cannot detect a remote service changing behavior after installation. Runtime allowlists, egress controls and monitoring remain separate defenses.

---

# 8. MCP Permission Inspector — inspect the connection boundary

Safety Auditor examines Agent Skill files.

MCP Permission Inspector examines an MCP client configuration before first connection.

Use it when:

- adding a new MCP server config;
- reviewing command/arguments/environment boundaries;
- checking what the first connection would launch.

Do **not** treat it as runtime monitoring.

A common MCP security concern is exactly this distinction:

**install-time review helps; runtime behavior can still drift later.**

That is why this project does not call static review a security certificate.

---

# 9. Creator Signal Lab — transparent scoring instead of “AI says this will go viral”

## Tool A: opportunity scorer

Question:

> Which content opportunity deserves attention first?

Input:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
```

Run the synthetic example:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --top 3
```

## Tool B: outlier scorer

Question:

> Which post behaved unusually well against my own baseline?

Input:

```csv
platform,post_id,views,likes,comments,shares,saves
```

Run:

```bash
python tools/outlier_score.py examples/social-outlier-posts.csv --top 3
```

## Why this is useful

The formulas are visible.

You can disagree with the weights and change them.

The tool does not pretend an opaque score is a prediction.

## What it is not

- not scraping;
- not a live social API;
- not an algorithm reverse-engineer;
- not a virality probability;
- not a sales/revenue predictor.

---

# 10. Prompt Library — when a prompt is enough

Use a structured prompt before building something more complicated.

A good prompt entry in this repository includes:

- job/use case;
- required inputs;
- output shape;
- quality gate;
- example;
- troubleshooting;
- next step.

Start with:

`prompts/README.md`

or:

`QUICK-WINS.md`

If a single reusable instruction solves the job, you do **not** need an MCP server.

---

# 11. Assistant Blueprints — when the same role repeats

An assistant blueprint is more persistent than a one-off prompt.

Use it when the same job repeats and needs:

- role;
- boundaries;
- output structure;
- quality rules;
- provider adaptation.

The toolkit can export the same underlying job for several provider formats.

Important:

**exporting an assistant blueprint does not create/publish an assistant account.**

It returns the configuration text/artifact.

---

# 12. Agent Skills — when a procedure should be installable

For all 19 skills one by one, use **[Every Agent Skill — Start From Zero](AGENT-SKILLS-FROM-ZERO.md)**.

Agent Skills are reusable workflow instructions designed for compatible agent runtimes.

## List available skills

```bash
npx skills add alptugharun/ai-social-media-toolkit --list
```

## Install one skill

```bash
npx skills add alptugharun/ai-social-media-toolkit --skill reels-director
```

## Install all skills

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

Do not install all 19 merely because you can.

Pick the job first.

Before installing an unknown third-party skill, inspect it.

---

# 13. Automation Recipes and GitHub Automations — only after the manual workflow makes sense

Automation is useful when a job repeats.

Examples:

- research → brief;
- release monitoring;
- recurring quality checks;
- traction/adoption watch;
- bounded failure diagnosis.

A safe automation should answer:

1. What triggers it?
2. What data can it read?
3. What can it write?
4. What is the output?
5. How do we verify the write?
6. What causes it to stop?
7. Who approves public/irreversible actions?

Configured schedule ≠ successful execution.

Always inspect run history and the output.

---

# 14. Releases and ZIP downloads

The Toolkit publishes versioned prereleases.

The v0.3 release includes separate assets so intentional downloads can be measured more cleanly than raw clone telemetry.

Available examples include:

- all Agent Skills bundle;
- Creator Context Builder ZIP;
- Creator Frame Studio offline ZIP;
- skills-only plugin bundle;
- SHA256 checksums.

A release download is a stronger intentional-action signal than a clone event, but it is still **not automatically a unique user or successful installation**.

---

# 15. Trust ladder — how to read badges and scores

A badge is a signal, not a certificate.

## M8ven

Useful for MCP trust inspection such as:

- publisher verification;
- code/sandbox verification;
- live monitoring;
- tool annotations;
- tool test coverage;
- suspicious access/exfiltration findings;
- reputation/adoption.

A new project can remain grade-capped because reputation/adoption is weak even when code findings are clean.

## OpenSSF Scorecard

Useful supply-chain checks include:

- pinned dependencies;
- token permissions;
- CI tests;
- CodeQL/SAST;
- dependency updates;
- security policy;
- branch protection;
- signed releases;
- known vulnerabilities;
- packaging.

Some score dimensions naturally remain low for a brand-new, single-maintainer project. Do not create fake reviewers or contributors to game them.

## Official MCP Registry

The registry verifies publication metadata/namespace/package ownership. It is a discovery/identity layer, not a complete security audit.

## Glama

Glama can independently inspect an MCP server, show tools/schemas and score tool-description quality. Treat it as another external view, not absolute truth.

## skills.sh

skills.sh ranks skills partly from anonymous install telemetry from its CLI. Install counts are more useful when they come from real external users, not maintainer self-install farming.

---

# 16. “Which one should I use?” decision tree

### I just want to try something useful without coding
→ Creator Frame Studio  
→ Creator Materials / Quick Wins

### I repeat the same creator briefing every time
→ Creator Context Builder

### I know my goal but do not know which workflow fits
→ Creator Ops

### My AI writing sounds generic
→ Brand Voice Humanizer

### I need a Reel production brief
→ Reels Director

### I want local prompt/assistant tools inside an MCP host
→ AI Workbench MCP

### I am about to install someone else's Agent Skill
→ Agent Skill Safety Auditor

### I am adding an MCP config and want to inspect it first
→ MCP Permission Inspector

### I have CSV metrics and want transparent prioritization
→ Creator Signal Lab

### A single task only needs a reusable instruction
→ Prompt Library

### The same role/job repeats across providers
→ Assistant Blueprint

### A workflow should be installable inside an agent
→ Agent Skill

### A proven workflow should run repeatedly
→ Automation

---

# 17. Before you trust any result

Ask:

- What exact evidence produced this?
- Is the data current?
- Is the result synthetic or real?
- Is the tool local or networked?
- Does it write anything?
- Does it need credentials?
- Is a score a heuristic or measured outcome?
- Was it tested in this exact runtime?
- Is the claim code evidence, host evidence, or independent-user evidence?

The project intentionally keeps those layers separate.

---

# 18. Where to ask for help

For the main Toolkit:

- `START-HERE.md`
- `SUPPORT.md`
- `SECURITY.md`
- Real User Lab #178
- Community Idea Box #169
- GitHub Discussions

For a security vulnerability, do not publish exploit details or secrets in a normal issue. Use private vulnerability reporting when available.

---

## Final beginner rule

You do not need the entire AI stack.

**Use the smallest layer that gives you a verifiable useful result.**

Then add the next layer only when the job actually requires it.
