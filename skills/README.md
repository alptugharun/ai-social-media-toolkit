# Agent Skills

Installable creator and social-media skills for AI agents.

## Skills

| Skill | Job |
| --- | --- |
| `creator-ops` | Orchestrates end-to-end creator workflows |
| `viral-content-radar` | Finds and deconstructs trends and outliers |
| `reels-director` | Produces short-form vertical video plans |
| `pinterest-growth-engine` | Builds Pinterest discovery and traffic systems |
| `content-repurposer` | Turns one source into platform-native assets |
| `influencer-fit-auditor` | Evaluates creator / influencer partnerships |
| `brand-voice-humanizer` | Restores natural brand voice |
| `signal-to-content` | Converts trend evidence into original platform-native tests |
| `comment-intelligence` | Mines comments for questions, objections, pain points, demand signals, and content opportunities |
| `agent-skill-safety-auditor` | Audits third-party skills before installation or reuse |
| `github-opportunity-radar` | Finds GitHub demand signals, skill gaps and repository-growth opportunities |

## Compatibility

These skills use portable Markdown instructions and are designed for agent environments that support skill-style instruction files.

Typical compatible environments may include:

- GitHub Copilot
- Claude Code
- Cursor
- Codex
- Gemini CLI
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

For better results, copy and complete:

`references/CREATOR-CONTEXT-TEMPLATE.md`

Research-oriented skills should follow:

`references/EVIDENCE-POLICY.md`

## Status

This skill pack is currently **alpha**.

The Markdown workflows are designed to be inspectable and portable. Runtime-specific behavior can differ, so test critical workflows before production use.
