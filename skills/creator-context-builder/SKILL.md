---
name: creator-context-builder
description: Builds or updates a privacy-aware shared creator context from user-provided facts, preferences, goals, platform rules and approved writing samples. Use before personalized creator workflows or whenever repeated briefing, stale facts or inconsistent brand voice are causing friction.
license: MIT
metadata:
  version: 0.1.0
  author: Alptuğ Harun
---

# Creator Context Builder

Create one reusable source of truth for creator and brand work.

The goal is not to collect every possible fact.

The goal is to capture only the context that materially improves downstream work while keeping facts, preferences, observations and hypotheses separate.

## When to Use

Use this skill when:

- the user keeps repeating the same creator / brand brief;
- several skills need the same audience, positioning or voice context;
- brand voice is inconsistent because no approved source exists;
- old metrics or profile facts may have gone stale;
- a creator wants a portable context file before using Reels, Pinterest, repurposing or creator-ops workflows.

Do not force this setup for a one-off research task that does not need personal or brand context.

## Context Labels

Every meaningful item should be classed as one of:

- **VERIFIED** — explicitly supplied or supported by a named source, ideally with a date;
- **PREFERENCE** — a user-approved choice, style rule or operating constraint;
- **OBSERVED** — a pattern found in approved writing/content samples;
- **HYPOTHESIS** — a useful interpretation that still needs confirmation.

Never silently upgrade OBSERVED or HYPOTHESIS items into VERIFIED facts.

## Privacy Boundary

Do not request or store:

- passwords, API keys, session cookies or recovery codes;
- private client credentials or unpublished confidential documents unless the task explicitly requires a safe local handling workflow;
- unnecessary sensitive personal information;
- secrets that another skill can access through a proper connector or environment variable instead.

If a supplied sample contains private data, summarize only the style or workflow signal needed for context and omit the private detail.

## Build Process

### 1. Reuse Before Asking

Look for existing context in this order:

1. `.agents/creator-context.md`
2. `.claude/creator-context.md`
3. another user-approved project context file
4. `references/CREATOR-CONTEXT-TEMPLATE.md`

If a completed file exists, read it first and ask only about missing or stale fields.

### 2. Ask the Minimum Useful Questions

Prefer a compact batch covering:

- identity / role;
- current positioning;
- primary audience and their main problem;
- strongest proof or credibility signals;
- primary platforms and preferred formats;
- content pillars;
- tone and language rules;
- phrases / styles to avoid;
- approval boundaries;
- current business or growth objective.

Do not interrogate the user with every template field.

### 3. Learn From Approved Samples

When the user supplies writing, captions, scripts or posts:

- identify vocabulary, sentence rhythm, paragraph length, humor, emoji behavior and CTA style;
- separate style observations from factual claims;
- use multiple samples before calling a pattern stable when possible;
- do not infer sensitive traits or private facts from writing style.

### 4. Record Evidence Freshness

For time-sensitive proof or metrics, record:

- value;
- source;
- date / reporting window;
- what the metric actually measures.

Example:

`VERIFIED — GitHub repository unique visitors: 54 — GitHub Traffic API — 2026-10-11 current 14-day window.`

Do not convert impressions, clones or reach into users, customers or revenue.

### 5. Write the Shared Context

Default output path when file writes are available:

`.agents/creator-context.md`

If that path is unsuitable, return the complete Markdown and let the user choose the location.

Use this structure:

- Identity
- Positioning
- Proof & Evidence Ledger
- Audience
- Platforms
- Content System
- Brand Voice
- Approved Sample Signals
- Visual System
- Workflow Preferences
- Approval / Risk Boundaries
- Current Objectives
- Stale / Recheck List
- Open Questions

### 6. Finish With Routing

After the context is ready, recommend no more than three next skills based on the actual job.

Examples:

- `creator-ops` for routing an end-to-end workflow;
- `reels-director` for short-form production;
- `brand-voice-humanizer` for copy alignment;
- `pinterest-growth-engine` for Pinterest planning;
- `content-repurposer` for platform-native derivatives.

## Update Rules

When updating an existing context:

1. preserve approved facts unless new evidence replaces them;
2. mark stale time-sensitive fields instead of silently deleting them;
3. show material changes before overwriting when the environment supports review;
4. never replace a user's explicit preference with an inferred preference;
5. keep the file concise enough that downstream skills can actually use it.

## Output Standard

Return:

- context status: NEW / UPDATED / NEEDS_CONFIRMATION;
- saved path or copyable Markdown;
- stale or unresolved items;
- the evidence labels used;
- up to three recommended next skills.

## Quality Gate

Before finishing, check:

- Is every metric dated or clearly non-current?
- Are facts separated from preferences and hypotheses?
- Did we avoid storing secrets or unnecessary private data?
- Could another skill use this file without asking the same questions again?
- Are unsupported claims absent?
- Is the context concise enough to remain useful?
