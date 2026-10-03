# AI Social Media Toolkit Plugin — build, test and release guide

The repository root is a **portable Agent Plugins package** with a valid Agent Plugins 1.0.0 `plugin.json` and a `skills/` directory.

Current package version: **0.6.0**

Current shape: **skills-only plugin**

It intentionally does **not** bundle the local AI Workbench MCP server.

## Why install this plugin?

Install it when you want one reusable AI workflow package instead of manually copying prompts between chats.

The plugin packages 18 focused Agent Skills for jobs such as:

- turning research into platform-specific content;
- directing short-form Reels;
- Pinterest opportunity and growth workflows;
- repurposing one source across channels;
- brand voice and content-quality review;
- influencer-fit analysis;
- local-business and Maps-aware intelligence;
- commercial opportunity research;
- evidence-aware GitHub research;
- designing prompts, Agent Skills, MCP servers and plugins.

The value is not “18 prompts.” The value is a set of **triggered procedures with boundaries, output contracts and tests**.

## Who should not install it?

Do not install this plugin if you only need one simple one-off prompt.

Do not use it as proof that:

- content will go viral;
- a platform trend exists without evidence;
- a connected account was modified;
- Google Maps consumer data may be scraped without restriction;
- every Agent Skills host behaves identically.

## Why skills-only first?

OpenAI's current plugin architecture supports:

- skills-only plugins;
- remote MCP-only plugins;
- plugins that combine skills and remote MCP.

The MCP server in this repository is currently a local stdio product. Public MCP-backed OpenAI plugins require a stable public HTTPS MCP endpoint. Shipping the local stdio server as if it were a public ChatGPT MCP plugin would create a false capability claim.

So version 0.6.0 keeps the OpenAI plugin package **skills-only**.

The standalone local MCP remains separately installable and testable:

https://github.com/alptugharun/ai-workbench-mcp

## Package layout

```text
ai-social-media-toolkit/
├── plugin.json
├── skills/
│   ├── creator-ops/
│   ├── reels-director/
│   ├── pinterest-growth-engine/
│   ├── ...
│   └── plugin-mcp-architect/
├── learning/AI-BUILDER-PATH.md
├── integrations/README.md
└── prompts/assistants/plugin-mcp-architect.md
```

Portable Agent Plugins discover `skills/` from the plugin root automatically. The root portable manifest does not need a Codex-only `skills` path field.

## Build the distributable ZIP

From the repository root:

```bash
python tools/build_plugin_bundle.py
```

Expected result:

```text
PLUGIN BUNDLE PASS
Version: 0.6.0
Skills: 18
MCP: none (skills-only package)
```

The output is written under `dist/`.

To choose another output location:

```bash
python tools/build_plugin_bundle.py --output ./ai-social-media-toolkit-plugin.zip
```

The builder intentionally includes only:

- `plugin.json`;
- installable skill directories;
- the three repository-level resources currently referenced by `plugin-mcp-architect`.

It does not package Git metadata, CI workflows, local caches or unrelated repository files.

## Validate before upload

Run:

```bash
python -m unittest tests.test_plugin_package -v
python tools/validate_prompt_library.py
python tools/validate_docs.py
python tools/release_readiness.py
python -m unittest discover -s tests -v
```

A plugin ZIP is not considered ready merely because it can be created.

## First useful requests

Use concrete jobs rather than “show me what you can do.”

### Starter 1 — Creator workflow

```text
Turn these source notes into a platform-specific Instagram + Pinterest content plan.
Keep factual claims grounded and show the quality checks.
```

### Starter 2 — Short-form production

```text
Create a 30-second Reel plan for this topic with hook, timing, shot logic,
voiceover structure and a final QA gate.
```

### Starter 3 — AI architecture

```text
I repeat this AI workflow every week. Decide whether it should remain a prompt,
become an Agent Skill, need MCP tools, or become a plugin. Give me the smallest
reliable architecture and the tests required before release.
```

## Submission test matrix

The machine-readable preparation cases live in:

`evals/plugin-submission-cases.json`

They include **5 positive** and **3 negative** cases.

Positive coverage:

1. content repurposing;
2. Reel production;
3. Pinterest opportunity research;
4. local-business visibility;
5. prompt/skill/MCP/plugin architecture.

Negative coverage:

1. unsupported virality/revenue guarantees;
2. restricted Google Maps scraping;
3. fake external publication/account-action claims.

These are static acceptance cases. They are **not** proof that an OpenAI review or live ChatGPT plugin test has passed.

## Current release gate

Before calling this plugin package ready:

- [x] Portable Agent Plugins schema URI in root `plugin.json`
- [x] Stable kebab-case plugin name
- [x] Explicit semantic version
- [x] 18 discoverable `skills/*/SKILL.md` packages
- [x] One evaluation contract per skill
- [x] Skills-only boundary documented
- [x] No root `mcp.json` pretending the local stdio server is public HTTPS
- [x] 5 positive submission-preparation cases
- [x] 3 negative submission-preparation cases
- [x] Deterministic ZIP builder
- [ ] Private ChatGPT/Codex plugin upload tested
- [ ] Live activation behavior tested in a plugin host
- [ ] Public listing metadata/assets finalized
- [ ] Verified publisher identity / submission permissions confirmed
- [ ] Public submission reviewed and approved

Do not convert unchecked items into claims.

## Listing copy draft

This copy is a **draft for review**, not a published directory listing.

**Display name**

AI Social Media Toolkit

**Short description**

Creator workflows with AI

**Long description**

AI Social Media Toolkit packages reusable Agent Skills for creators, strategists and small teams. Use focused workflows for research, Reels, Pinterest, repurposing, brand voice, influencer fit, local visibility, commercial opportunity analysis and plugin/MCP architecture. The plugin favors evidence, explicit limits and human review over invented trend data, guaranteed virality or unverified external actions.

**Suggested category**

Productivity

The final category should be selected from the current submission portal rather than assumed from this document.

## What is still required for public OpenAI submission?

OpenAI currently requires the submission flow to include publisher identity, listing information, realistic starter prompts and test cases. Skills-only plugins can omit remote MCP configuration.

Before a public submission:

1. confirm Apps Management / plugin submission access in the intended OpenAI organization;
2. confirm the publishing identity;
3. prepare production logo/icon assets;
4. review the plugin ZIP in a private/local plugin test;
5. run live positive and negative activation tests;
6. record failures and fixes;
7. upload the final skill bundle;
8. submit only after the listing and release notes match the tested package.

If a future version adds MCP, deploy a stable public HTTPS Streamable HTTP endpoint first and complete the extra MCP review, domain, privacy and tool-metadata requirements.

## Failure report

Use this when a plugin test fails:

```text
Plugin version:
Host / version:
Skill expected:
User prompt:
Expected activation:
Observed activation:
Expected result:
Observed result:
First meaningful error:
Root cause:
Fix:
Regression test:
Final retest:
```

Every meaningful fixed failure should gain a regression case.

## Important distinction

**Package created** ≠ **plugin installed** ≠ **live host tested** ≠ **submitted** ≠ **approved** ≠ **publicly published**.

Keep these states separate in documentation and release notes.
