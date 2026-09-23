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

## Compatibility

These skills use portable Markdown instructions and are designed for agent environments that support skill-style instruction files.

Typical compatible environments may include:

- Claude Code
- Cursor
- Codex
- Gemini CLI
- Other Agent Skills-compatible runtimes

## Installation

Where supported by the open Skills CLI:

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

List or install individual skills according to your runtime's supported Skills workflow.

Manual installation also works: copy the desired skill folder into the skills directory recognized by your agent.

## Shared Context

For better results, copy and complete:

`references/CREATOR-CONTEXT-TEMPLATE.md`

Research-oriented skills should follow:

`references/EVIDENCE-POLICY.md`

## Status

This skill pack is currently **alpha**.

The Markdown workflows are designed to be inspectable and portable. Runtime-specific behavior can differ, so test critical workflows before production use.
