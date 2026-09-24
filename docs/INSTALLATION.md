# Installation

The **AI Social Media Toolkit** uses portable `SKILL.md` packages so the same creator workflows can be reused across multiple AI-agent environments.

## Fastest route

For environments supported by the open Skills CLI:

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

Browse before installing:

```bash
npx skills add alptugharun/ai-social-media-toolkit --list
```

Install an individual skill:

```bash
npx skills add alptugharun/ai-social-media-toolkit --skill viral-content-radar
```

## Runtime paths

The repository also ships a dependency-free installer for direct placement into native skill directories.

```bash
python tools/install_skills.py --target agents --scope user
```

Supported targets:

| Target | User scope | Project scope |
| --- | --- | --- |
| Portable Agent Skills | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` |
| OpenAI Codex | `~/.codex/skills/` | `.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| Grok | `~/.grok/skills/` | `.grok/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |

Use `--skill <name>` to install only selected skills.

Use `--dry-run` to inspect planned changes.

Use `--force` only when you intentionally want to replace an existing installed skill.

## GitHub Copilot

GitHub Copilot supports project skills in `.github/skills/`, `.claude/skills/` or `.agents/skills/`, and personal skills in `~/.copilot/skills/` or `~/.agents/skills/`.

With GitHub CLI 2.90.0 or later, preview a skill before installing it:

```bash
gh skill preview alptugharun/ai-social-media-toolkit signal-to-content
gh skill install alptugharun/ai-social-media-toolkit signal-to-content
```

Or use the repository installer:

```bash
python tools/install_skills.py --target copilot --scope user
```

`gh skill` is currently a GitHub public-preview feature, so verify its current CLI behavior before scripting it into production automation.

## Gemini CLI native install

The repository includes a root `gemini-extension.json`, so Gemini CLI can install the toolkit as a first-class extension and automatically discover the bundled `skills/` directory:

```bash
gemini extensions install https://github.com/alptugharun/ai-social-media-toolkit
```

Gemini CLI copies extensions into its extension directory. Pull future toolkit updates with:

```bash
gemini extensions update ai-social-media-toolkit
```

If you prefer skill-only installation rather than the extension package, Gemini CLI also supports installing skills directly from Git repositories:

```bash
gemini skills install https://github.com/alptugharun/ai-social-media-toolkit.git --consent
```

Gemini CLI also recognizes the portable `.agents/skills/` alias.

## OpenAI Codex

Codex supports user skills under `$CODEX_HOME/skills/` (normally `~/.codex/skills/`) and project-local skill discovery including `.codex/skills/` and `.agents/skills/`.

Examples:

```bash
python tools/install_skills.py --target codex --scope user
python tools/install_skills.py --target codex --scope project --project-root /path/to/project
```

## Claude Code

Claude Code uses skill directories containing `SKILL.md` and supports plugin packages with a `.claude-plugin/plugin.json` manifest.

For direct skill installation:

```bash
python tools/install_skills.py --target claude --scope user
```

The repository also includes a Claude Code plugin manifest so the repository can be loaded or packaged as a plugin-compatible skill collection.

## Grok

Grok discovers skills from `.grok/skills/` and also supports compatibility discovery for `.agents/skills/`, Claude skill directories and Cursor skill directories.

For native Grok placement:

```bash
python tools/install_skills.py --target grok --scope user
```

## Security

Agent Skills are instructions with potential access to tools, files, shell commands, APIs, and credentials.

Before installing third-party skills, inspect them.

This repository includes:

[Agent Skill Safety Auditor](../skills/agent-skill-safety-auditor/SKILL.md)

Never treat popularity alone as a security guarantee.

## Verification

After installation, use the runtime's own skill listing / inspection command when available.

For this repository itself, GitHub Actions validates the skill package structure and runs installer tests on relevant changes.
