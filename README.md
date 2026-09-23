# AI Social Media Toolkit

[![Validate Agent Skills](https://github.com/alptugharun/ai-social-media-toolkit/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/alptugharun/ai-social-media-toolkit/actions/workflows/validate-skills.yml)
[![GitHub stars](https://img.shields.io/github/stars/alptugharun/ai-social-media-toolkit?style=flat-square)](https://github.com/alptugharun/ai-social-media-toolkit/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/alptugharun/ai-social-media-toolkit?style=flat-square)](https://github.com/alptugharun/ai-social-media-toolkit/forks)
![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Creator%20Ops-blue?style=flat-square)
![Skills license](https://img.shields.io/badge/skills-MIT-green?style=flat-square)

**An installable creator-operations toolkit for turning research signals into platform-native social content systems.**

Built for creators, strategists and AI agents working across social-media research, Reels, Pinterest, influencer marketing, content repurposing, brand voice and digital visibility.

Created and maintained by **Alptuğ Harun**.

🌐 [alptugharun.com](https://alptugharun.com)

### Install the Agent Skills

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

Discover first, install only what you need, or run a skill without permanently installing it:

```bash
# List the skills in this repository
npx skills add alptugharun/ai-social-media-toolkit --list

# Install one workflow only
npx skills add alptugharun/ai-social-media-toolkit --skill viral-content-radar

# Target a specific supported agent
npx skills add alptugharun/ai-social-media-toolkit --skill comment-intelligence -a codex

# Try a skill without installing it
npx skills use alptugharun/ai-social-media-toolkit --skill signal-to-content
```

Works as portable `SKILL.md` packages with installation paths and manifests for **Claude Code, OpenAI Codex, Gemini CLI, Grok, Cursor and Agent Skills-compatible runtimes**.

→ [Installation & compatibility guide](docs/INSTALLATION.md)

---

## About This Repository

Artificial intelligence is changing how social media content is researched, created, optimized and distributed.

This repository documents practical systems I use and develop across:

- Social Media Strategy
- AI-Assisted Content Creation
- Digital Marketing
- Content Automation
- Pinterest & Visual Search
- Canva Workflows
- Prompt Design
- Creative AI Tools
- Brand Strategy
- Digital Visibility

The focus is not simply generating more content.

The goal is to build **repeatable, efficient and measurable content systems**.

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
| [Content Repurposer](skills/content-repurposer/SKILL.md) | Rebuilds one source into platform-native assets |
| [Influencer Fit Auditor](skills/influencer-fit-auditor/SKILL.md) | Evaluates creator partnerships and campaign fit |
| [Brand Voice Humanizer](skills/brand-voice-humanizer/SKILL.md) | Removes generic AI texture while preserving facts and voice |
| [Signal to Content](skills/signal-to-content/SKILL.md) | Converts evidence-backed trends and outliers into original content tests |
| [Comment Intelligence](skills/comment-intelligence/SKILL.md) | Mines comments for recurring questions, objections, audience language and testable content opportunities |
| [Agent Skill Safety Auditor](skills/agent-skill-safety-auditor/SKILL.md) | Audits third-party skills before installation or reuse |
| [GitHub Opportunity Radar](skills/github-opportunity-radar/SKILL.md) | Researches GitHub demand signals, fast-rising repositories and Agent Skill gaps |

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

### Working Tools

The repository includes dependency-free utilities that turn creator research into auditable scores instead of opaque AI judgments:

- [Signal to Content Opportunity Scorer](tools/signal2content_score.py) — ranks trend and content opportunities with a transparent heuristic. Example: [signal2content-opportunities.csv](examples/signal2content-opportunities.csv)
- [Social Outlier Analyzer](tools/outlier_score.py) — compares post performance against the creator's own median baseline using views and engagement signals. Example: [social-outlier-posts.csv](examples/social-outlier-posts.csv)

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

This repository is licensed under the  
[Creative Commons Attribution-NonCommercial 4.0 International License](LICENSE.md).

You may share and adapt the original material with appropriate attribution to **Alptuğ Harun**.

Commercial use requires separate permission.

---
_Last updated: September 2026_