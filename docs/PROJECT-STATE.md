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

After the Pinterest visibility release, the repository contains **17 Agent Skills**:

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
15. `commercial-opportunity-radar`
16. `monetization-architect`
17. `pinterest-opportunity-radar`

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

### 08:50 Türkiye — Commercial Opportunity Radar

Workflow:

`.github/workflows/commercial-opportunity-radar.yml`

Purpose:

- scan commercially relevant GitHub / open-source demand proxies
- compare agentic-workflow, AI-marketing, creator-tool, local-business and B2B-intelligence lanes
- score buyer clarity, recurring need, proof, distribution, feasibility and monetization paths
- inspect current repository monetization readiness
- refresh one `commercial-radar` issue
- keep billing, pricing, contracts, sponsorship acceptance and outreach behind human approval

### 09:05 Türkiye — Pinterest Visibility Radar

Workflow:

`.github/workflows/pinterest-visibility-radar.yml`

Purpose:

- attempt current official Pinterest Trends API retrieval when accessible
- compare regional growing-keyword evidence
- monitor Pinterest API, MCP, scheduling and analytics repositories
- identify seasonal / visual-search opportunities
- refresh one `pinterest-radar` issue
- never fabricate trend numbers when API evidence is unavailable

### 09:20 Türkiye — Automation Health Watch

Workflow:

`.github/workflows/automation-health.yml`

Purpose:

- monitor the four radar workflows
- open/update one `automation-health` issue only when a radar is missing or failed
- close the health issue automatically after recovery

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

## Commercial Strategy

The pasted B2B-radar idea was retained in a safer and more useful form: **signal collection → evidence → insight → reusable report → offer → recurring delivery**.

The project does **not** use the weaker pattern of scraping restricted platforms and mass-emailing scraped contacts.

Primary commercial candidates currently tracked:

1. Local Business Intelligence Cloud
2. Creator Ops Workspace
3. B2B Signal-to-Offer recurring briefs
4. Maps / Local Content Gap reports
5. implementation-as-a-service
6. Agentic Workflow Packs
7. MapWrapped premium companion products
8. GitHub Sponsors / Marketplace only after adoption evidence

Reference:

`references/OPEN-SOURCE-MONETIZATION-PLAYBOOK.md`

Commercial skills:

`skills/commercial-opportunity-radar/SKILL.md`

`skills/monetization-architect/SKILL.md`

## Pinterest Visibility Strategy

Pinterest now has a dedicated automation lane.

Strategy:

**evidence → keyword cluster → visual system → destination match → publish → measure → expand winners**

Current rules:

- use official Pinterest Trends/API evidence when accessible
- do not fabricate search volume or trend status
- do not scrape Pinterest consumer UI as the core evidence source
- use `pinterest-opportunity-radar` before `pinterest-growth-engine` when current trend evidence matters
- keep publishing human-reviewed until access, board mapping and destination checks are intentionally configured
- future authenticated layer: Pinterest analytics → top Pins → winner expansion → destination optimization

Reference:

`references/PINTEREST-AUTOMATION-PLAYBOOK.md`

Pinterest skills:

`skills/pinterest-opportunity-radar/SKILL.md`

`skills/pinterest-growth-engine/SKILL.md`

GitHub Agentic Workflows are monitored as an optional future AI execution layer. They are currently public preview and should not be enabled until a supported engine credential / repository secret and permissions are intentionally configured.

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
- Do not treat stars as revenue or assume sponsor interest without evidence.
- Do not automate mass unsolicited outreach or restricted-platform scraping.
- Monetization sequence: prove useful value → identify buyer → test a small offer → automate delivery only after demand exists.

## Current Strategic Loop

**Research → score opportunity → policy/commercial check → human approval → prototype → test → package → publish → measure adoption → validate buyer → monetize carefully → learn**

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
