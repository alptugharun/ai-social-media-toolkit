# AI Social Media Toolkit

[![Validate Agent Skills](https://github.com/alptugharun/ai-social-media-toolkit/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/alptugharun/ai-social-media-toolkit/actions/workflows/validate-skills.yml)
[![GitHub stars](https://img.shields.io/github/stars/alptugharun/ai-social-media-toolkit?style=flat-square)](https://github.com/alptugharun/ai-social-media-toolkit/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/alptugharun/ai-social-media-toolkit?style=flat-square)](https://github.com/alptugharun/ai-social-media-toolkit/forks)
[![GitHub release](https://img.shields.io/github/v/release/alptugharun/ai-social-media-toolkit?include_prereleases&style=flat-square&label=alpha)](https://github.com/alptugharun/ai-social-media-toolkit/releases)
![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Creator%20Ops-blue?style=flat-square)
![Skills license](https://img.shields.io/badge/skills-MIT-green?style=flat-square)
![Tools license](https://img.shields.io/badge/tools-MIT-green?style=flat-square)

**Open-source creator operations for AI-assisted social media.**

Turn a signal into **research → strategy → platform-native content → review → measurement → winner expansion** using portable Agent Skills, runnable tools and approval-gated automation.

Built for **creators, social-media strategists, agencies and AI-agent users** who want repeatable workflows instead of isolated prompt lists.

Created and maintained by **Alptuğ Harun** · [alptugharun.com](https://alptugharun.com)

### Start in 60 seconds

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

Or inspect before installing:

```bash
npx skills add alptugharun/ai-social-media-toolkit --list
npx skills use alptugharun/ai-social-media-toolkit --skill signal-to-content
```

Works with portable Agent Skills workflows across **Claude Code, OpenAI Codex, Gemini CLI, Grok, Cursor and compatible runtimes**.

→ [Installation & compatibility](docs/INSTALLATION.md) · [Quick Start](START-HERE.md) · [Free Creator Materials](downloads/README.md)

**New here? → [How to Use Everything: complete field manual](docs/HOW-TO-USE-EVERYTHING.md)**

→ [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [Security](SECURITY.md)

Growth milestone: **[First 10 real users](docs/FIRST-10-USERS.md)** — usage and friction before vanity metrics.

## Two-minute proof

**Want proof before installation? Run the dependency-free demo.**

```bash
git clone https://github.com/alptugharun/ai-social-media-toolkit.git
cd ai-social-media-toolkit
python tools/two_minute_demo.py
```

It uses synthetic example data to show two real decisions: **which content opportunity to prioritize** and **which post broke the supplied performance baseline**.

→ [See exactly what the demo does](examples/TWO-MINUTE-DEMO.md) · [Preview the expected output](examples/TWO-MINUTE-DEMO-OUTPUT.md)

→ [v0.1.0-alpha.1 release notes](releases/v0.1.0-alpha.1.md)

### What ships today

| Layer | Current public surface |
| --- | --- |
| Agent workflows | **17 Agent Skills** for creator ops, Reels, Pinterest, repurposing, influencer fit, brand voice, research and local intelligence |
| Runnable tooling | **10 Python tools** for scoring, radars, installation, market scanning, traction and self-healing support |
| Automation | **8 GitHub Actions workflows** for validation, research radars, health monitoring, traction review and bounded self-healing |
| Starter materials | Prompt system, AI assistant blueprints, automation starters, Pinterest, Reels, Canva + AI and Creator OS starter map |
| Evidence layer | Explicit source rules, human-review gates and no fabricated trend/search/revenue claims |

### Choose your path

| I want to… | Start here |
| --- | --- |
| Build an end-to-end creator workflow | [Creator Ops](skills/creator-ops/SKILL.md) |
| Turn a signal into a content test | [Signal to Content](skills/signal-to-content/SKILL.md) |
| Build Reels faster | [Reels Director](skills/reels-director/SKILL.md) or [Reels Starter Kit](downloads/REELS-PRODUCTION-STARTER-KIT.md) |
| Grow through Pinterest visual search | [Pinterest Growth Engine](skills/pinterest-growth-engine/SKILL.md) or [Pinterest Starter Kit](downloads/PINTEREST-GROWTH-STARTER-KIT.md) |
| Remove generic AI writing texture | [Brand Voice Humanizer](skills/brand-voice-humanizer/SKILL.md) |
| Analyze what actually outperformed | [Social Outlier Analyzer](tools/outlier_score.py) |
| Start without a terminal | [Creator Materials Hub](downloads/README.md) |

### Why this repository exists

A lot of AI marketing content stops at “generate more.”

This project focuses on the harder part: **making creator work inspectable, repeatable and measurable**.

The repository is deliberately proof-first:

- real examples over feature-count inflation
- one-command installation where possible
- measurable outputs over vague “AI magic”
- human approval before external publishing
- official/permitted data sources over scraping shortcuts
- improvement of existing workflows before adding another shiny skill

If this is useful, ⭐ **star the repository** so you can find future releases and workflow improvements again.


---

## Toolkit

This repository includes practical resources covering the following areas.

### AI Content Workflows

Workflows for combining AI tools with research, ideation, writing, visual production and publishing.

Examples:

- ChatGPT-assisted research
- Content ideation systems
- AI-supported editorial workflows
- Multi-platform content repurposing
- Human + AI review processes

### Social Media Strategy

Frameworks for planning and managing content across social platforms.

Topics include:

- Content pillars
- Audience positioning
- Hook development
- Content calendars
- Platform adaptation
- Organic visibility
- Performance analysis

### Canva + AI

Practical workflows combining Canva with generative AI tools.

Including:

- Social media design systems
- Reels cover workflows
- Instagram content systems
- Brand consistency
- AI-assisted visual ideation
- Template production

### Pinterest & Visual Search

Systems designed around Pinterest discovery and visual search.

Topics include:

- Pinterest trend research
- Keyword strategy
- Pin architecture
- Visual search optimization
- Evergreen content
- Seasonal trend planning
- Pinterest-to-website traffic systems

### Prompt Frameworks

Reusable prompt structures for:

- Content research
- Social media strategy
- Visual generation
- Marketing
- Brand positioning
- Editorial planning
- Workflow automation

The objective is not to collect random prompts, but to build **reusable prompt systems**.

### Content Automation

Experiments and practical systems for reducing repetitive content work.

Areas include:

- Research automation
- Content pipelines
- Approval workflows
- Publishing preparation
- AI agent workflows
- Multi-tool automation

---

## Free Creator Materials

Prefer a ready-to-use resource before installing the full Agent Skills system?

The new [Creator Materials Hub](downloads/README.md) provides practical, non-developer starter assets:

- [Creator Prompt Starter Kit](downloads/CREATOR-PROMPT-STARTER-KIT.md) — a connected 10-step prompt workflow from audience/evidence to QA and winner expansion
- [AI Assistant Blueprint Starter Pack](downloads/AI-ASSISTANT-BLUEPRINTS.md) — five portable creator-operations assistant blueprints for Gemini Gems or comparable custom assistants
- [Creator Automation Starter Pack](downloads/CREATOR-AUTOMATION-STARTER-PACK.md) — three approval-gated automation blueprints for research, repurposing and weekly performance review
- [Pinterest Growth Starter Kit](downloads/PINTEREST-GROWTH-STARTER-KIT.md) — evidence-to-keyword-to-7-Pin cluster workflow
- [Reels Production Starter Kit](downloads/REELS-PRODUCTION-STARTER-KIT.md) — 30–35 second production workflow with timing and QA
- [Canva + AI Content Starter Kit](downloads/CANVA-AI-CONTENT-STARTER-KIT.md) — master visual, adaptation and export system
- [AI Creator OS Starter Map](downloads/AI-CREATOR-OS-STARTER.md) — connects research, production, review and measurement into one operating loop

The product rule is simple:

**Free proves the workflow. A future premium companion must remove meaningful setup or operational friction — not merely contain more prompts.**

---

## Agent Skills — Creator Ops Alpha

The toolkit now includes portable AI-agent skills for creator and social-media workflows.

### Install

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

Designed for Agent Skills-compatible environments including Claude Code, Cursor, Codex, Gemini CLI and similar runtimes.

| Skill | What it does |
| --- | --- |
| [Creator Ops](skills/creator-ops/SKILL.md) | Routes end-to-end creator workflows |
| [Viral Content Radar](skills/viral-content-radar/SKILL.md) | Finds trends, outliers and repeatable content mechanics |
| [Reels Director](skills/reels-director/SKILL.md) | Turns ideas into short-form video production plans |
| [Pinterest Growth Engine](skills/pinterest-growth-engine/SKILL.md) | Builds visual-search, keyword and traffic systems |
| [Pinterest Opportunity Radar](skills/pinterest-opportunity-radar/SKILL.md) | Finds evidence-backed Pinterest trends, seasonality and visual-search opportunities |
| [Content Repurposer](skills/content-repurposer/SKILL.md) | Rebuilds one source into platform-native assets |
| [Influencer Fit Auditor](skills/influencer-fit-auditor/SKILL.md) | Evaluates creator partnerships and campaign fit |
| [Brand Voice Humanizer](skills/brand-voice-humanizer/SKILL.md) | Removes generic AI texture while preserving facts and voice |
| [Signal to Content](skills/signal-to-content/SKILL.md) | Converts evidence-backed trends and outliers into original content tests |
| [Comment Intelligence](skills/comment-intelligence/SKILL.md) | Mines comments for recurring questions, objections, audience language and testable content opportunities |
| [Agent Skill Safety Auditor](skills/agent-skill-safety-auditor/SKILL.md) | Audits third-party skills before installation or reuse |
| [GitHub Opportunity Radar](skills/github-opportunity-radar/SKILL.md) | Researches GitHub demand signals, fast-rising repositories and Agent Skill gaps |
| [Maps Opportunity Radar](skills/maps-opportunity-radar/SKILL.md) | Finds under-served Google Maps, Places, local-business and geospatial AI workflows |
| [Maps Policy Guard](skills/maps-policy-guard/SKILL.md) | Reviews Maps workflows for scraping, storage, caching, attribution and authorization risks |
| [Local Business Intelligence](skills/local-business-intelligence/SKILL.md) | Turns permitted location and owned Business Profile signals into market, creator and content decisions |
| [Commercial Opportunity Radar](skills/commercial-opportunity-radar/SKILL.md) | Finds product, service, report and monetization opportunities from evidence-backed demand signals |
| [Monetization Architect](skills/monetization-architect/SKILL.md) | Turns validated open-source value into a staged commercial model |

Research-oriented skills follow an explicit [Evidence Policy](references/EVIDENCE-POLICY.md).

For consistent outputs, start with the [Creator Context Template](references/CREATOR-CONTEXT-TEMPLATE.md).

**Status:** Alpha. Skill structure, manifests and the cross-agent installer are automatically validated with GitHub Actions. Runtime-specific behavior should still be tested before production use.

[Browse all Agent Skills](skills/README.md)

### Automated GitHub Opportunity Radar

A scheduled GitHub Actions workflow scans current GitHub demand proxies and refreshes a single `growth-radar` issue with:

- current Trending signals
- recent star-velocity proxies
- repository-search supply estimates
- fast-rising relevant repositories
- under-served Agent Skill candidates
- packaging and monetization-readiness checks

The radar runs daily and deliberately requires human approval before any new skill is published.

Research method: [GitHub Growth & Discovery Playbook](references/GITHUB-GROWTH-PLAYBOOK.md)

### Automated Maps & Local Intelligence Radar

A second scheduled GitHub Actions workflow runs after the general GitHub radar and refreshes a single `maps-radar` issue with:

- Google Maps / Places / Business Profile opportunity signals
- current open-source competitor snapshots
- ChatGPT / Claude / Agent Skill demand proxies
- local-business and creator-location workflow gaps
- compliance-feasibility checks
- product candidates such as Local Business Intelligence and MapWrapped

The Maps radar runs daily at **08:35 Türkiye time** and keeps human approval before any new skill or product is published.

Research method: [Maps + AI Opportunity Playbook](references/MAPS-AI-OPPORTUNITY-PLAYBOOK.md)

Project continuity: [Project State](docs/PROJECT-STATE.md)

### Automated Commercial Opportunity Radar

A third scheduled GitHub Actions workflow runs after the general and Maps radars and refreshes a single `commercial-radar` issue with:

- commercially promising GitHub / open-source signals
- buyer clarity and recurring-use analysis
- reference repositories and adoption patterns
- service, hosted SaaS, paid-report, Sponsors and Marketplace paths
- current repository monetization-readiness checks
- candidate products such as Local Business Intelligence Cloud, Creator Ops Workspace and B2B Signal-to-Offer briefs

The commercial radar runs daily at **08:50 Türkiye time**. It automates research and prioritization, not billing, pricing changes, contracts or mass outreach.

Research method: [Open-Source Monetization & Commercial Opportunity Playbook](references/OPEN-SOURCE-MONETIZATION-PLAYBOOK.md)

### Automated Pinterest Visibility Radar

A fourth scheduled GitHub Actions workflow runs at **09:05 Türkiye time** and refreshes a single `pinterest-radar` issue with:

- official Pinterest Trends API data when accessible
- regional growing-keyword evidence
- Pinterest automation / MCP / scheduling ecosystem changes
- seasonal and visual-search opportunities
- content-cluster and destination-fit guidance
- API-readiness status without inventing trend numbers

Research method: [Pinterest Automation & Visibility Playbook](references/PINTEREST-AUTOMATION-PLAYBOOK.md)

### Automation Health Watch

A separate health workflow monitors the four radars and opens an `automation-health` issue only when a monitored workflow is missing or fails. Healthy runs do not create noise.

### Traction & Focus Watch

A weekly GitHub Actions workflow checks whether repository growth is producing **external proof**, not only internal activity.

It tracks public signals such as stars, forks, releases, external issue participation and external contributors, then recommends one operating state:

- **BUILD PROOF**
- **VALIDATE WEDGE**
- **SCALE WHAT WORKS**

The purpose is to prevent unnecessary scope expansion. Commit count and skill count are treated as shipping activity, not product-market fit.

Research method: [Focus & Traction Playbook](references/FOCUS-TRACTION-PLAYBOOK.md)

### Working Tools

The repository includes dependency-free utilities that turn creator research into auditable scores instead of opaque AI judgments:

- [Signal to Content Opportunity Scorer](tools/signal2content_score.py) — ranks trend and content opportunities with a transparent heuristic. Example: [signal2content-opportunities.csv](examples/signal2content-opportunities.csv)
- [Social Outlier Analyzer](tools/outlier_score.py) — compares post performance against the creator's own median baseline using views and engagement signals. Example: [social-outlier-posts.csv](examples/social-outlier-posts.csv)
- [Places Aggregate Market Scanner](tools/places_market_scan.py) — queries the official Places Aggregate API for live category-count / Place-ID insights without building a scraped Maps database.
- [Maps Opportunity Radar Analyzer](tools/maps_opportunity_radar.py) — scores Maps / local-intelligence repository demand, direct supply, strategic fit and compliance feasibility.
- [Commercial Opportunity Radar Analyzer](tools/commercial_opportunity_radar.py) — scores buyer clarity, recurring-use potential, proof, distribution and monetization paths without treating stars as revenue.
- [Pinterest Visibility Radar Analyzer](tools/pinterest_growth_radar.py) — combines official Pinterest Trends data when accessible with Pinterest automation ecosystem signals and never fabricates trend numbers.
- [Traction & Focus Analyzer](tools/traction_focus_report.py) — separates internal shipping from external adoption and keeps expansion tied to proof.

---

## Tools

Some of the tools used across these workflows include:

**AI**

ChatGPT • Claude • Gemini • Grok • DeepSeek • NotebookLM

**Creative**

Canva • Adobe Photoshop • Adobe Illustrator • CapCut • DaVinci Resolve

**Automation & Development**

Cursor • Codex • Zapier

---

## Projects

Some workflows published here may originate from real-world work developed for:

### ADYA Creative

AI-powered creative agency focused on:

Social Media • Influencer Marketing • Creative Design • Digital Marketing • AI Content • Brand Strategy

### Yeşil Dijital Akademi

A digital education and communication initiative combining:

Environment • Sustainability • Technology • Artificial Intelligence • Education

---

## Included Resources

Version 1 includes:

- [x] [AI Content Workflow](AI-CONTENT-WORKFLOW.md)
- [x] [Social Media Content System](SOCIAL-MEDIA-CONTENT-SYSTEM.md)
- [x] [Canva + AI Workflow](CANVA-AI-WORKFLOW.md)
- [x] [Pinterest Research Framework](PINTEREST-RESEARCH-FRAMEWORK.md)
- [x] [Prompt Engineering Framework](PROMPT-ENGINEERING-FRAMEWORK.md)
- [x] [Reels Production Workflow](REELS-PRODUCTION-WORKFLOW.md)
- [x] [Content Automation Architecture](CONTENT-AUTOMATION-ARCHITECTURE.md)
- [x] [AI Tool Comparison Resources](AI-TOOL-COMPARISON-RESOURCES.md)
- [x] [Digital Visibility Checklist](DIGITAL-VISIBILITY-CHECKLIST.md)

---

## Start Here

New to the toolkit?

Begin with the [Start Here Quick-Start Guide](START-HERE.md).

It shows how to move from objective to framework, template, human review, publishing and measurement.

---

## Practical Templates

Use these resources directly in your own workflow:

- [Content Brief Template](templates/CONTENT-BRIEF-TEMPLATE.md)
- [Reels Production Template](templates/REELS-PRODUCTION-TEMPLATE.md)
- [Pinterest Research Sheet](templates/PINTEREST-RESEARCH-SHEET.csv)
- [Reusable Prompt Template](templates/PROMPT-TEMPLATE.md)
- [AI Tool Comparison Matrix](templates/AI-TOOL-COMPARISON-MATRIX.csv)
- [Digital Visibility Audit Checklist](downloads/DIGITAL-VISIBILITY-AUDIT-CHECKLIST.md)

### Case Study

- [Building the AI Social Media Toolkit](case-studies/AI-SOCIAL-MEDIA-TOOLKIT-CASE-STUDY.md)

---

## Philosophy

AI should not replace creative thinking.

It should reduce repetitive work, accelerate research and give creators more time to focus on strategy, storytelling and original ideas.

The most valuable AI workflow is not the one that generates the most content.

It is the one that creates the **best system**.

---

## Author

**Alptuğ Harun**

Social Media Specialist • Digital Content Creator • Creative Strategist

Antalya, Türkiye

🌐 [Website](https://alptugharun.com)  
💼 [LinkedIn](https://www.linkedin.com/in/alptugharun/)  
🎨 [Behance](https://www.behance.net/alptugharun/)

---
## License

Licensing is intentionally split by artifact type so the installable/reusable parts remain open-source:

- [`skills/`](skills/) — **MIT License** ([skills/LICENSE](skills/LICENSE)). Skills may be used, modified, distributed and included in commercial workflows under the MIT terms.
- [`tools/`](tools/) — **MIT License** ([tools/LICENSE](tools/LICENSE)). Runnable utilities may be used, modified, distributed and included in commercial workflows under the MIT terms.
- Other original documentation, frameworks, templates and repository material — **Creative Commons Attribution-NonCommercial 4.0 International** under the root [LICENSE.md](LICENSE.md).

Preserve the applicable copyright and license notices when redistributing MIT-licensed material. See the license files for the controlling terms.

---
_Last updated: September 2026_