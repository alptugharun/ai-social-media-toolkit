# Changelog

All notable public changes to the **AI Social Media Toolkit** are recorded here.

The project is currently in **alpha**. Until the first tagged release is published, this file tracks release-ready milestones without pretending that an unreleased commit is a versioned release.

## Unreleased

### Added

- Portable skills-only Agent Plugin release gate with a deterministic ZIP builder, 18-skill package validation, submission-preparation test cases and a public Plugin Guide.
- Standalone `ai-workbench-mcp` package boundary with dependency-free stdio server, bundled catalog and exact tool contracts.
- CI wheel build/install/handshake verification on Ubuntu 24.04, Ubuntu 26.04 and Windows 2025.
- Tokenless PyPI Trusted Publishing workflow with keyless Sigstore signing for MCP release artifacts.
- Public release-readiness audit covering MCP annotations, schemas, tool-name test coverage, JSON manifests, immutable Action refs and workflow permission posture.
- Offline Markdown navigation validation for broken relative links and duplicate consecutive headings.
- M8ven Verified/Live integration and OpenSSF Scorecard visibility.

### Improved

- Every local and packaged MCP tool declares explicit `readOnlyHint`, `destructiveHint`, `idempotentHint` and `openWorldHint`.
- Packaged MCP tests reference each public tool by name, closing the visible M8ven tool-test-coverage gap.
- GitHub Actions write permissions were reduced from workflow-level grants to narrow job-level permissions where writes are required.
- README, profile, `llms.txt`, project-state and runtime-verification paths now reflect the current AI Workbench / Agent Skills / MCP scope.
- Self-healing now treats deterministic readiness/docs quality-gate failures as non-retryable regressions instead of wasting a probe retry.

### Fixed

- Updated the embedded MCP package build backend from vulnerable `setuptools==80.9.0` to `setuptools==84.0.0` and added a regression guard requiring the patched 83.0.0+ line for CVE-2026-59890.
- Removed a duplicated `15-Minute Quick Start` heading and aligned the MCP quick-start path with the standalone package.

## [v0.2.0-alpha.1] - 2026-09-30

### Added

- AI Workbench with prompt rendering, assistant exports, provider adapters, local browser catalog and read-only MCP tooling.
- Structured Prompt Library with eight starter prompts and an automated prompt contract validator.
- Portable assistant blueprints for ChatGPT/OpenAI, Claude, Gemini and Grok/xAI workflows.
- Integrations Hub with MCP / Plugin decision guidance and integration contracts.
- Multi-provider assistant starter for OpenAI, Anthropic, xAI and Gemini, including mock mode and credential-redacted dry runs.
- Learning Paths from prompt fundamentals through automation.
- Automation Recipes for research, publishing, monitoring and failure recovery.
- 10 Quick Wins for low-friction first use.
- Curated AI Creator Stack reference map.
- v0.2.0 distribution pack for legitimate community and social sharing.

### Improved

- README routing now reflects the wider AI ecosystem rather than only social-media workflows.
- CI validates prompt-library contracts and the wider AI ecosystem directories.
- First-use paths now prioritize immediate useful outcomes and transparent evidence levels.

## [v0.1.0-alpha.1] - 2026-09-29

### Added

- 17 portable creator-operations Agent Skills.
- 10 runnable Python tools for installation, scoring, research radars, market scanning, traction analysis and self-healing support.
- 8 GitHub Actions workflows for validation, opportunity research, health monitoring, traction review and bounded self-healing.
- Creator Materials Hub with starter resources for prompts, AI assistants, automation, Pinterest, Reels, Canva + AI and the AI Creator OS map.
- Evidence, security, Maps policy and monetization guardrails.
- Bug-report and real-workflow-feedback issue templates.
- Two-minute proof demo that runs the content-opportunity and social-outlier tools on synthetic example data.

### Improved

- Product-led profile and repository onboarding.
- One-command install and quick-start routing.
- Validation coverage for downloads, documentation and primary README surfaces.
- Growth strategy shifted from feature-count expansion toward external proof, repeat use and contribution.

## Release policy

A tagged release should include:

1. a tested commit;
2. a reproducible quick start;
3. release notes that describe real shipped behavior;
4. no fabricated adoption claims;
5. known limitations when relevant.

Do not backfill fake semantic-version history for earlier internal commits.
