# AGENTS.md

## Purpose

This repository is a practical, evidence-aware toolkit for AI-assisted social media strategy, creator workflows, content production, Pinterest research, Reels, digital visibility, influencer fit, and reusable Agent Skills.

Treat this file as the shared operating guide for coding and AI agents working in the repository. Keep tool-specific configuration thin; prefer portable instructions and assets that can be used across Codex, Claude Code, Gemini CLI, Cursor, and other compatible agent environments.

## Working principles

- Preserve the working baseline. Do not refactor or replace functioning systems unless the task explicitly requires it.
- Prefer small, reversible changes over broad rewrites.
- Keep the toolkit creator- and marketer-facing. New assets should solve a concrete social-media, creator-economy, content, research, automation, or digital-visibility problem.
- Do not add files merely to make the repository look larger.
- Never invent platform metrics, trend evidence, benchmark results, downloads, stars, performance claims, or case-study outcomes.
- Distinguish observed evidence from hypotheses and recommendations.
- Do not copy another project's distinctive wording, branding, proprietary assets, or unlicensed code.
- When third-party material is materially reused under a compatible license, preserve required notices and attribution in `THIRD-PARTY-NOTICES.md`.

## Repository map

- `skills/` — reusable Agent Skills. Each skill lives in its own directory and requires a valid `SKILL.md`.
- `tools/` — runnable utilities and validators.
- `examples/` — small example inputs or outputs that make workflows easier to test and understand.
- `references/` — shared policies, creator context, and supporting reference material.
- `downloads/` — standalone reusable resources for non-developer users.
- `case-studies/` — documented applications and evidence-aware case studies.
- `.github/workflows/` — repository validation and CI.
- Root Markdown files — major human-facing workflow guides and documentation.

## Agent Skill requirements

For every new or edited `skills/<skill-name>/SKILL.md`:

1. Keep the skill self-contained and narrowly useful.
2. Include YAML frontmatter with at least `name` and `description`.
3. Make the description explicit about both capability and trigger conditions so an agent can select the skill correctly.
4. Put procedural instructions in the Markdown body rather than bloating frontmatter.
5. Prefer deterministic steps, acceptance criteria, and output contracts over vague persona prompts.
6. Keep examples generic unless a real source is cited or the example is clearly labeled synthetic.
7. Do not add credentials, secrets, private data, or instructions that bypass platform safeguards.

## Evidence and research

Before adding claims about current platform behavior, AI products, APIs, trends, or growth:

- Prefer primary documentation, official repositories, release notes, and first-party platform sources.
- Record dates when freshness matters.
- Use `references/EVIDENCE-POLICY.md` as the repository-wide standard.
- Avoid presenting forecasts as facts.
- If evidence is weak or contradictory, say so instead of forcing a conclusion.

## Validation

Before completing a change:

1. Inspect the affected files and nearby conventions.
2. Run the repository's relevant validator or tests when runnable in the environment.
3. For skill changes, ensure required frontmatter and directory structure remain valid.
4. Check links, paths, examples, and command snippets touched by the change.
5. If CI fails because of the change, fix or revert it rather than leaving the default branch knowingly broken.

## Change boundaries

Use a branch and pull request for substantial architecture changes. Small documentation, example, skill, validator, or utility improvements may be committed directly when they are low-risk and validated.

Do not, without explicit authorization:

- change the repository's root licensing strategy
- delete important content or history
- change repository visibility or account permissions
- alter domains or DNS
- deploy external production systems
- add paid dependencies or services
- publish fabricated growth or adoption claims

## Definition of done

A change is complete when it is useful to a real user, consistent with the repository's scope, legally safe to distribute, understandable without hidden context, and validated to the extent the environment permits.
