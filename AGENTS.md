# AGENTS.md

## Purpose

This repository is a practical, evidence-aware toolkit for AI-assisted social media strategy, creator workflows, content production, Pinterest research, Reels, digital visibility, influencer fit, and reusable Agent Skills.

Treat this file as the shared operating guide for coding and AI agents working in the repository. Keep tool-specific configuration thin; prefer portable instructions and assets that can be used across Codex, Claude Code, Gemini CLI, Cursor, and other compatible agent environments.

## Working principles

- Preserve the working baseline. Do not refactor or replace functioning systems unless the task explicitly requires it.
- Prefer small, reversible changes over broad rewrites.
- Keep the toolkit creator- and marketer-facing. New assets should solve a concrete social-media, creator-economy, content, research, automation, or digital-visibility problem.
- Do not add files merely to make the repository look larger.
- Before adding a new Agent Skill, automation, or product lane, read `references/FOCUS-TRACTION-PLAYBOOK.md` and apply the Expansion Gate.
- Prefer extending or merging existing workflows when they already cover most of the requested job.
- Treat commit count and skill count as internal activity, not external adoption.
- When adoption is weak, prioritize onboarding, examples, demos, distribution and real-user proof over additional breadth.
- For major opportunity decisions, read `references/STRATEGIC-DECISION-FRAMEWORK.md` and challenge the idea with why-this / why-now / why-us / payer / proof / overlap / stop-condition questions before implementation.
- Prefer AI-native opportunities when evidence is comparable, but allow stronger adjacent demand or monetization evidence to outrank AI branding. Never add AI as decoration.
- Never invent platform metrics, trend evidence, benchmark results, downloads, stars, performance claims, or case-study outcomes.
- Distinguish observed evidence from hypotheses and recommendations.
- Do not copy another project's distinctive wording, branding, proprietary assets, or unlicensed code.
- When third-party material is materially reused under a compatible license, preserve required notices and attribution in `THIRD-PARTY-NOTICES.md`.

## Visibility-first operating priority — 2026-09-28

The owner's priority order is:

1. Accurate public identity and useful, professional presentation.
2. Relevant visibility, genuine followers, saves, meaningful comments, stars, external reuse and qualified website traffic.
3. Revenue through website advertising/sponsorship, client work and validated GitHub-related services or products.

Keep commercial readiness in view, but do not replace audience building with premature paid infrastructure. AI-assisted creator operations is the core positioning. Popularity, buyer demand and verified revenue are different measurements.

Routine work is delegated within actual account access and existing approval gates. Do not claim that a broad delegation grants new OAuth scopes, platform permissions, paid budgets or unrestricted publication rights.

### Execution, not planning noise

- Prefer completing one useful demo, example, case study or distribution asset over adding another skill, workflow or planning document.
- Before each change, identify its audience, evidence, affected scope, success check and rollback path.
- Read the current file SHA, object state and relevant open work before writing. Do not overwrite concurrent edits or duplicate another agent's task.
- Keep Alptuğ Harun, ADYA Creative, Yeşil Dijital Akademi and MiyaPaw audiences distinct. Never infer an author from the topic alone or imply an institutional endorsement.
- Keep `alptugharun.com` as the intended long-term content/portfolio/revenue hub. Verify destination relevance and availability before directing traffic there.
- Do not change the website's deployment, DNS, schema, canonical/hreflang, sitemap, Search Console/Bing/indexing or cross-link architecture without resolving the separate website project's current state first.
- Never purchase engagement, generate fake reviews or use automated comments, unsolicited bulk messages or duplicate content to simulate adoption.

### Operational evidence

- Distinguish installed app, authorized account, mapped destination, successful read, saved draft, scheduled publication and confirmed live publication.
- A workflow definition or enabled task is configuration, not evidence of a successful execution.
- A successful health-monitor job does not prove every monitored system is healthy. Inspect its findings, skipped jobs, payload quality, timestamps and remaining incidents.
- A fixed question template or hand-assigned score is not independent AI reasoning or buyer research. Label those limitations.
- Do not report continuous model operation, universal self-repair or zero-error guarantees.

### Controlled recovery

Use: current-state read -> scoped preparation -> tests and factual review -> allowed application -> read-back verification -> evidence record.

- Retry transient failures only within bounded limits and only when safe to repeat.
- After an ambiguous write response, read back the destination before retrying to avoid duplicates.
- On missing credentials, account mapping, plan restrictions, billing requirements or security denials, stop the affected operation. Do not bypass the restriction, alter permissions or repeatedly reactivate a paused task.
- Repair the cause when permitted, then rerun targeted and relevant full tests. Never weaken tests to make the status green.
- Keep useful independent work moving while recording the minimum external blocker once.
- Keep private account identifiers, credentials and sensitive client data out of public project records.

Use precise completion states: **DRAFT**, **APPLIED**, **VERIFIED**, or **BLOCKED**. A change is not verified until the relevant read-back/test evidence exists.

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
- For Google Maps, Places, Street View or Business Profile work, read `references/MAPS-AI-OPPORTUNITY-PLAYBOOK.md` and route policy-sensitive designs through `maps-policy-guard`.
- Do not build Google Maps workflows around consumer-UI scraping, prohibited bulk export, hidden long-term caching, or a permanent database of restricted Maps content.
- Prefer official APIs, aggregate insights, place IDs where permitted, user-owned Business Profile data, user exports, or independently licensed/open datasets.
- For Pinterest trend or growth work, read `references/PINTEREST-AUTOMATION-PLAYBOOK.md`; prefer official Pinterest Trends/API evidence and never label a hypothesis as a live trend.
- Do not scrape Pinterest consumer surfaces as the primary evidence source or commit Pinterest access tokens.
- For monetization work, read `references/OPEN-SOURCE-MONETIZATION-PLAYBOOK.md` and route commercial prioritization through `commercial-opportunity-radar` before proposing pricing or paid product scope.
- Treat revenue, willingness-to-pay, conversion, sponsor interest, customer counts and pricing as hypotheses until supported by real evidence.
- Do not automate mass unsolicited outreach, financial commitments, sponsorship acceptance, billing changes or public revenue claims.

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
