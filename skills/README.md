# Agent Skills

Installable creator and social-media skills for AI agents.

## Human Usage Guide

Not sure what to ask after installation? Open **[How to Use Everything](../docs/HOW-TO-USE-EVERYTHING.md)** for every skill's use case, first request to try, expected result and next step.

## Start with a foundation, not a prompt dump

For personalized creator work, the smallest useful stack is:

1. `creator-context-builder` — build one shared, privacy-aware source of truth;
2. `creator-ops` — route the job to the minimum relevant workflow;
3. `brand-voice-humanizer` — keep final copy aligned without changing facts.

Research-only tasks can skip creator context when personal or brand alignment is irrelevant.

## How the skills work together

```text
creator-context-builder
        │
        ▼
    creator-ops
        │
        ├── CREATE → reels-director · content-repurposer · brand-voice-humanizer
        ├── DISCOVER → viral-content-radar · pinterest-opportunity-radar · github-opportunity-radar
        ├── UNDERSTAND → comment-intelligence · influencer-fit-auditor · local-business-intelligence
        ├── GROW → pinterest-growth-engine · signal-to-content
        ├── PROTECT → agent-skill-safety-auditor · maps-policy-guard · plugin-mcp-architect
        └── COMMERCIALIZE → commercial-opportunity-radar · monetization-architect
```

You do **not** need the whole stack. Install the smallest skill that matches the job.

## Foundation & routing

| Skill | Job |
| --- | --- |
| `creator-context-builder` | Builds a shared creator/brand context with provenance, freshness and privacy boundaries |
| `creator-ops` | Routes an end-to-end creator job to the minimum relevant workflow |
| `brand-voice-humanizer` | Restores natural brand voice while preserving facts and intent |

## Create & repurpose

| Skill | Job |
| --- | --- |
| `reels-director` | Produces short-form vertical video plans |
| `content-repurposer` | Turns one source into platform-native assets |
| `signal-to-content` | Converts evidence into original, measurable content tests |

## Research & audience intelligence

| Skill | Job |
| --- | --- |
| `viral-content-radar` | Finds and deconstructs trends and outliers without treating one hit as a confirmed trend |
| `pinterest-opportunity-radar` | Finds evidence-backed Pinterest trends, seasonality and visual-search opportunities |
| `github-opportunity-radar` | Finds GitHub demand proxies, skill gaps and repository-growth opportunities |
| `maps-opportunity-radar` | Finds Maps, local-intelligence and geospatial Agent Skill opportunities |
| `comment-intelligence` | Mines comments for questions, objections, pain points and content opportunities |
| `influencer-fit-auditor` | Evaluates creator / influencer partnerships with explicit evidence limits |
| `local-business-intelligence` | Turns permitted local and owned business signals into market/content workflows |

## Growth & distribution planning

| Skill | Job |
| --- | --- |
| `pinterest-growth-engine` | Builds Pinterest discovery and traffic systems from validated evidence |

## Trust, policy & architecture

| Skill | Job |
| --- | --- |
| `agent-skill-safety-auditor` | Audits third-party skills before installation or reuse |
| `maps-policy-guard` | Reviews Maps workflows for scraping, storage, attribution and authorization risks |
| `plugin-mcp-architect` | Designs and teaches testable prompt, Agent Skill, MCP and plugin architectures |

## Commercial validation

| Skill | Job |
| --- | --- |
| `commercial-opportunity-radar` | Finds evidence-backed product, service and monetization opportunities |
| `monetization-architect` | Turns validated open-source value into a staged commercial model |


## Compatibility

These skills use portable Markdown instructions and are designed for agent environments that support skill-style instruction files.

Typical compatible environments may include:

- GitHub Copilot
- Claude Code
- Cursor
- Codex
- Gemini CLI
- Grok-compatible skill workflows via the repository installer
- Other Agent Skills-compatible runtimes

## Installation

### GitHub CLI (`gh skill`)

GitHub CLI v2.90.0+ can discover and install Agent Skills across supported hosts. The `gh skill` feature is currently in public preview, so its interface may change.

Browse the repository interactively:

```bash
gh skill install alptugharun/ai-social-media-toolkit
```

Preview a specific skill before installing it:

```bash
gh skill preview alptugharun/ai-social-media-toolkit signal-to-content
```

Install a specific skill for a specific host when needed:

```bash
gh skill install alptugharun/ai-social-media-toolkit signal-to-content --agent claude-code --scope user
gh skill install alptugharun/ai-social-media-toolkit signal-to-content --agent cursor --scope user
gh skill install alptugharun/ai-social-media-toolkit signal-to-content --agent codex --scope user
gh skill install alptugharun/ai-social-media-toolkit signal-to-content --agent gemini --scope user
```

Installed skills receive provenance metadata that `gh skill update` can use for later update checks.

### Universal Skills CLI

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

Browse first:

```bash
npx skills add alptugharun/ai-social-media-toolkit --list
```

Install one skill:

```bash
npx skills add alptugharun/ai-social-media-toolkit --skill signal-to-content
```

### Native / direct placement

The repository includes a dependency-free installer:

```bash
python tools/install_skills.py --target agents --scope user
```

Supported direct targets: `agents`, `claude`, `copilot`, `codex`, `gemini`, `grok`, and `cursor`.

For GitHub Copilot specifically:

```bash
python tools/install_skills.py --target copilot --scope user
```

This installs personal skills to `~/.copilot/skills`. Project-scoped Copilot installs use `.github/skills`.

Gemini CLI can also install directly from Git:

```bash
gemini skills install https://github.com/alptugharun/ai-social-media-toolkit.git --consent
```

See the full [Installation & Compatibility Guide](../docs/INSTALLATION.md).

## Maintainer Validation

GitHub CLI v2.90.0+ can validate a skill repository against the Agent Skills specification without publishing it:

```bash
gh skill publish --dry-run
```

This complements the repository's own validation workflow. Treat the GitHub CLI result as an additional compatibility check rather than a substitute for runtime testing on each agent host.

## Shared Context

For better results, run `creator-context-builder` or copy and complete:

`references/CREATOR-CONTEXT-TEMPLATE.md`

See a filled synthetic example: [`examples/CREATOR-CONTEXT-EXAMPLE.md`](../examples/CREATOR-CONTEXT-EXAMPLE.md).

Install only the foundation skill when that is all you need:

```bash
npx skills add alptugharun/ai-social-media-toolkit --skill creator-context-builder
```

The builder is preferred when the user has approved samples, stale metrics or multiple downstream skills that need the same context.

Research-oriented skills should follow:

`references/EVIDENCE-POLICY.md`

## Status

This skill pack is currently **alpha**.

The Markdown workflows are designed to be inspectable and portable. Runtime-specific behavior can differ, so test critical workflows before production use.
