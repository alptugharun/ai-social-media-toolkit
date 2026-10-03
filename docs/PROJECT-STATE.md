# Project State — AI Social Media Toolkit

Last updated: **2026-10-03**

This file is the continuity anchor for future ChatGPT / Claude / Codex / Cursor sessions working on this repository.

**Read this file and AGENTS.md before making project-wide changes.**

## Repository

- Owner: **Alptuğ Harun**
- Repository: `alptugharun/ai-social-media-toolkit`
- Website: `https://alptugharun.com`
- Positioning: Social Media Specialist • Digital Content Creator • Creative Strategist
- Related projects: ADYA Creative, Yeşil Dijital Akademi

## Current trust & distribution checkpoint — 2026-10-03

- M8ven publisher ownership is verified and GitHub Live Monitoring is connected.
- M8ven's latest visible public grade is **B / 89** at commit `0e62484`; current `main` is newer, so treat the displayed M8ven finding as a stale external snapshot until its page names the newer commit.
- PR #112 added direct name-level calls for every packaged MCP tool and strengthened the release-readiness gate. PR #135 later added adjacent package-local tests for `list_prompts`, `render_prompt` and `get_assistant` and made that coverage part of CI/release readiness. PR #136 added the AI Builder learning path plus `plugin-mcp-architect`; PR #137 moved the embedded build backend to patched `setuptools==84.0.0` with a regression guard.
- **[alptugharun/ai-workbench-mcp](https://github.com/alptugharun/ai-workbench-mcp)** is now the canonical standalone MCP distribution repository. The toolkit copy remains an integration/test surface during cutover.
- The standalone MCP repo has Linux/Windows CI, CodeQL, OpenSSF Scorecard, Dependabot, Repository Rules, private vulnerability reporting and a protected `pypi` GitHub environment. Version `0.1.0a1` is published to PyPI through Trusted Publishing with signed release evidence.
- The official MCP Registry entry `io.github.alptugharun/ai-workbench-mcp` is published and reports `active`. A maintainer-run Cursor 3.20.21 session invoked all three public tools successfully; independent external host verification remains a separate open adoption goal.
- This toolkit now uses active GitHub Repository Rules on `main` (PR flow, required validation/CodeQL checks, linear history, no force-push/delete bypass), plus Dependabot security updates and private vulnerability reporting.
- OpenSSF Scorecard last observed **7.0** on `af97b51` before the Repository Rules migration; the next external run must confirm that branch protection is now readable.

## Current owner direction

**Useful public work -> relevant visibility and real adoption -> qualified website traffic -> revenue.**

The owner delegates routine planning, research, content preparation and low-risk reversible maintenance within available access and existing approval requirements. The priority is first to grow accurate identity, recognition, genuine followers, meaningful engagement, GitHub stars and real use. Website advertising/sponsorship, client acquisition and GitHub-related income are later conversion goals, not reasons to inflate metrics or prematurely build paid infrastructure.

Use the visibility-first operating section of `AGENTS.md`. Do not add another skill, dashboard or scheduled task simply to document this direction. Finish existing user-facing proof and distribution assets.

### Cross-project priorities

| Surface | Current priority | Completion evidence |
| --- | --- | --- |
| GitHub | Reliable existing tools, a usable quick start, concrete input/output demo and release-readiness review | Reproducible example, exact tested commit, real user feedback when available |
| Behance / LinkedIn | Finish the toolkit case study and concise proof-led presentation | Actual saved assets and, separately, confirmed public project/post |
| Pinterest | Original niche-relevant visual/search clusters with relevant destinations | Verified account/board mapping, authentic analytics and confirmed publication when authorized |
| ADYA / Google Business Profile | Consistent identity, service information and genuine case studies | Current field read, permitted change and read-back, not merely Maps research |
| alptugharun.com | Main content/portfolio/traffic hub, coordinated with the separate website project | Confirmed current project state before code, SEO or deployment changes |
| Yeşil Dijital Akademi | Environmental education and technology content with correct joint authorship | Source-backed content and approved brand/author identity |

Keep MiyaPaw's visual/lifestyle audiences distinct from the AI/agency audience. Do not redirect unrelated Pin topics to a generic agency page. Alptuğ Harun, ADYA Creative and Yeşil Dijital Akademi require related but distinct positioning. Ahu Nur Şahin Harun is a co-founder of Yeşil Dijital Akademi; do not erase her role or infer article authorship from subject matter.

### Integration checkpoint, observed 2026-09-28

This is a dated observation, not a permanent claim. Recheck before any dependent action.

- Metricool's brand lookup was reachable but reported no connected social networks. Social analytics and publishing must not be reported as operational until an actual connected account and successful read are verified.
- Windsor.ai onboarding was shown in the conversation, but directory discovery did not confirm an installed/usable connection. Search Console, GA4 and Business Profile data access remains unverified from this session. Do not create duplicate analytics properties or replace the website stack to work around an access gap.
- The installed GitHub repository search returned the profile repository and toolkit, not the website code repository. Do not infer website deployment access from toolkit access.
- Behance project preparation is in progress. A project ID or an editor screenshot alone does not prove that all fields were saved or that the project was published. Keep the ten independent case-study visual sections as the existing backlog, not a collage.
- The existing six-hour Alptuğ Authority Radar task was updated to coordinate visibility-first work. Task configuration is not evidence that a later execution succeeded. Do not rely on an unverified separate hourly task or silently reactivate paused tasks.

Do not store credentials, private account identifiers, client data or private analytics in this public document. Use precise states: **DRAFT**, **APPLIED**, **VERIFIED**, **BLOCKED**.


## Growth surface update — 2026-09-29

Current benchmark research shows that high-adoption Agent Skill / AI-marketing repositories tend to reduce first-use friction with a clear value proposition, a fast install path, task-oriented routing, visible proof, contribution paths and release discipline.

Applied direction:

- keep the profile product-led rather than decoration-heavy
- keep the main repository's one-command install above the fold
- route non-developers to the Creator Materials Hub
- make real tools and workflows easy to inspect
- collect bug reports separately from real-workflow feedback
- maintain a public changelog and release policy
- use `references/GROWTH-PRODUCTIZATION-GATES.md` before turning public traction into a paid companion product

Commercial automation may research, score and prepare. It must not autonomously activate billing, change live pricing or remove useful free functionality.



## Documentation & onboarding standard — 2026-09-29

Every public starter kit, downloadable resource, tool, workflow or major skill must now include human-facing usage guidance, not only implementation files or installation commands.

Required user journey:

**result → audience → prerequisites → exact steps → copyable example → expected output → common mistake → troubleshooting → next step**

The complete reference is `docs/HOW-TO-USE-EVERYTHING.md`. New public assets should extend that manual and follow `references/USER-FACING-ASSET-DOC-TEMPLATE.md`. Current onboarding patterns are tracked in `references/ONBOARDING-BENCHMARKS.md`.

Public titles should be outcome-led and memorable without clickbait, fabricated urgency or unsupported claims. Apply Brand Voice Humanizer principles to outward-facing copy.


## Current Architecture

The repository has four layers:

1. **Frameworks** — social-media, AI content, Pinterest, Reels, prompt, automation and digital-visibility methodology.
2. **Practical assets** — templates, CSV sheets, case study and checklists.
3. **Agent Skills** — portable workflows for creator, marketing, research and local-intelligence work.
4. **Automation / validation** — GitHub Actions, tests, installers and opportunity-radar tooling.


## Creator Materials Layer — 2026-09-29

**State: VERIFIED on `main`.**

A user-facing materials hub is being added under `downloads/` to improve onboarding and external proof without increasing Agent Skill count.

Initial public assets:

- Creator Prompt Starter Kit
- AI Assistant Blueprint Starter Pack
- Creator Automation Starter Pack
- Pinterest Growth Starter Kit
- Reels Production Starter Kit
- Canva + AI Content Starter Kit
- AI Creator OS Starter Map

Product rule:

**Free materials must be independently useful. Premium companion products should be validated as time-saving systems, implementation packs or support layers rather than paywalled prompt quantity.**

Candidate commercial lanes remain hypotheses until external use or buyer evidence exists: Creator Prompt OS, Pinterest Growth OS, Reels Production OS, Canva + AI Content Factory, Creator Automation Vault and AI Creator OS.


## Agent Skills

The repository currently contains **18 Agent Skills**:

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
18. `plugin-mcp-architect`

## Daily Automations

The times below describe configured schedules, not guaranteed execution or delivery times. Verify run history and output freshness separately.

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
- enforce the Pinterest Sandbox validation gate before authenticated automation is treated as production-ready

### 09:20 Türkiye — Automation Health Watch

Workflow:

`.github/workflows/automation-health.yml`

Purpose:

- monitor the four radar workflows plus Traction & Focus Watch
- open/update one `automation-health` issue only when a radar is missing or failed
- close the health issue automatically after recovery

### Event-driven — Self-Healing Automation Guardian

Workflow:

`.github/workflows/self-heal.yml`

Purpose:

- react to completed runs from the four radar workflows, Traction & Focus Watch, Agent Skill validation and Automation Health Watch
- diagnose failed workflow logs with `tools/self_heal.py`
- classify failure fingerprints and keep incident evidence in GitHub Issues
- perform only bounded retries for failures classified as retryable or safe to probe
- learn from successful reruns by marking recovered/transient incidents
- escalate persistent failures instead of silently weakening tests or validation
- optionally delegate persistent repair to the review-gated Self-Healer coding agent when repository/account support is available
- keep repair changes behind pull-request review and CI rather than auto-merging them

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
- require the Pinterest Sandbox validation gate before authenticated automation is promoted toward production use
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

## Focus & Traction Strategy

A new operating rule now sits above expansion:

**Breadth creates possibilities. Traction decides where depth belongs.**

Primary wedge:

**Open-source creator operations for AI-assisted social media and digital visibility.**

Pinterest, Maps/local intelligence, Reels, influencer workflows and commercial research are supporting lanes inside that creator-operations system. They do not automatically become separate products.

Before adding a new skill, automation or product lane:

1. check whether an existing workflow already covers most of the job
2. prefer extending or merging before adding breadth
3. require a measurable external proof plan
4. name the buyer or user
5. keep the idea in research mode when adoption evidence is weak

Commercial sequence:

**GitHub proof / open core → implementation service → productized recurring service → paid intelligence/reporting → hosted workspace/SaaS**

GitHub is treated primarily as proof, distribution, inspectable open core and trust infrastructure, not as the assumed primary revenue source.

Traction evidence priority:

- repeated real-world use
- paid buyer validation
- external installs / reuse
- external contributors / issues
- stars / forks / watchers
- referral traffic / qualitative feedback
- internal activity last

Reference:

`references/FOCUS-TRACTION-PLAYBOOK.md`

### Weekly — Traction & Focus Watch

Workflow:

`.github/workflows/traction-focus-watch.yml`

Schedule:

**Monday 09:40 Türkiye time**

Purpose:

- separate internal activity from external adoption
- track public proof signals
- keep scope expansion under control
- recommend BUILD PROOF, VALIDATE WEDGE or SCALE WHAT WORKS
- refresh one `traction-focus` issue
- prevent skill count from becoming the goal

## Strategic Decision Layer

All major opportunity decisions now use:

`references/STRATEGIC-DECISION-FRAMEWORK.md`

Required questions include:

- Why this?
- Why now?
- Why us?
- Why would anyone care?
- Why would anyone pay?
- What evidence is external?
- What can be proven in seven days?
- What existing workflow overlaps?
- What evidence would make us stop?

Focus rule:

- AI is the default strategic lens because it strengthens the current positioning.
- AI does not automatically win.
- If a non-AI or adjacent opportunity has materially stronger demand, monetization or distribution evidence, it may rank equally or higher.
- Never add AI as decoration.

Major decisions resolve to one of:

- BUILD PROOF
- VALIDATE BUYER
- DEEPEN EXISTING
- WATCH

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

> Read `docs/PROJECT-STATE.md` and `AGENTS.md` in `alptugharun/ai-social-media-toolkit` and continue from the latest repository state.

Then inspect current `main`, open Issues, recent Actions and recent PRs before making changes. Check actual account access separately from installation status. Do not treat earlier conversation claims as live verification.

## Source of Truth

The live GitHub repository is the operational source of truth for this toolkit. It does not establish access to unrelated accounts or the separate website deployment.

This file should be updated when the architecture, automation schedule, core skill inventory or strategic priorities materially change.
