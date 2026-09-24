# Project State — AI Social Media Toolkit

Last updated: **2026-09-24**

This file is the continuity anchor for future ChatGPT / Claude / Codex / Cursor sessions working on this repository.

**Read this file before making project-wide changes.**

## Repository

- Owner: **Alptuğ Harun**
- Repository: `alptugharun/ai-social-media-toolkit`
- Website: `https://alptugharun.com`
- Positioning: Social Media Specialist • Digital Content Creator • Creative Strategist
- Related projects: ADYA Creative, Yeşil Dijital Akademi

## Current Architecture

The repository has four layers:

1. **Frameworks** — social-media, AI content, Pinterest, Reels, prompt, automation and digital-visibility methodology.
2. **Practical assets** — templates, CSV sheets, case study and checklists.
3. **Agent Skills** — portable workflows for creator, marketing, research and local-intelligence work.
4. **Automation / validation** — GitHub Actions, tests, installers and opportunity-radar tooling.

## Agent Skills

After the Maps & Local Intelligence release, the repository contains **14 Agent Skills**:

1. `creator-ops`
2. `viral-content-radar`
3. `reels-director`
4. `pinterest-growth-engine`
5. `content-repurposer`
6. `influencer-fit-auditor`
7. `brand-voice-humanizer`
8. `signal-to-content`
9. `comment-intelligence`
10. `agent-skill-safety-auditor`
11. `github-opportunity-radar`
12. `maps-opportunity-radar`
13. `maps-policy-guard`
14. `local-business-intelligence`

## Daily Automations

### 08:20 Türkiye — GitHub Opportunity Radar

Workflow:

`.github/workflows/github-opportunity-radar.yml`

Purpose:

- scan GitHub demand/supply proxies
- inspect fast-rising relevant repositories
- find under-served Agent Skill opportunities
- refresh one `growth-radar` issue
- keep human approval before skill publication

### 08:35 Türkiye — Maps & Local Intelligence Radar

Workflow:

`.github/workflows/maps-opportunity-radar.yml`

Purpose:

- scan Google Maps / Places / local-business / geospatial-AI repository demand
- compare strong reference repositories
- identify higher-level Maps workflow gaps
- penalize generic Maps MCP wrappers
- refresh one `maps-radar` issue
- keep human approval before publication

## Maps Strategy

Current conclusion:

**Do not build another generic Google Maps MCP wrapper as the flagship.**

The official Google ecosystem and existing open-source projects already cover much of the basic place-search, routing, geocoding and local-rank plumbing.

Build higher-level workflow intelligence instead.

Current priorities:

1. **Local Business Intelligence** inside this repository.
2. Creator Location Scout mode.
3. Local Content Gap Engine mode.
4. Sponsor Scout Local mode with human review.
5. Places Aggregate market-density tooling.
6. **MapWrapped** as a future separate consumer-facing repository/product.

## Maps Data Rules

For Google Maps / Places / Street View / Business Profile work:

- prefer official APIs
- use Places Aggregate for permitted market-density questions
- use user-owned / authorized Business Profile data for performance workflows
- do not scrape consumer Google Maps
- do not create a permanent bulk lead database from restricted Google Maps content
- check storage / caching / attribution rules before shipping
- use place IDs as durable references only where permitted
- use open / separately licensed data when persistent enrichment is needed
- keep human approval before outreach, replies or other external write actions
- do not infer sensitive socioeconomic / criminality / similar traits from Street View or neighborhood proxies

Reference:

`references/MAPS-AI-OPPORTUNITY-PLAYBOOK.md`

Policy skill:

`skills/maps-policy-guard/SKILL.md`

## Quality Rules

- Never invent metrics, downloads, stars, search volume or case-study outcomes.
- Separate observed evidence, inference and recommendation.
- Do not guarantee virality, one million users, sponsors or revenue.
- New skills need a narrow job-to-be-done, useful output and measurable proof contract.
- Prefer small, reversible changes.
- Use a branch + PR for substantial architecture changes.
- Run CI and tests before merging.
- If CI fails, inspect the logs and fix the change before merging.
- Do not auto-publish a large number of low-quality skills.

## Current Strategic Loop

**Research → score opportunity → policy check → human approval → prototype → test → package → publish → measure → learn**

## Website Coordination Rule

GitHub and `alptugharun.com` are intended to reinforce each other, but do not change:

- schema
- Search Console
- Bing
- DNS
- sitemap
- indexing
- migration / go-live settings

without first checking the current state of the separate website project.

## New-Conversation Recovery

If a future conversation has lost context, start with:

> Read `docs/PROJECT-STATE.md` in `alptugharun/ai-social-media-toolkit` and continue from the latest repository state.

Then inspect current `main`, open Issues, recent Actions and recent PRs before making changes.

## Source of Truth

The live GitHub repository is the operational source of truth.

This file should be updated when the architecture, automation schedule, core skill inventory or strategic priorities materially change.
