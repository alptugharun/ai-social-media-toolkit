# Runtime verification report

Copy this template into an issue comment or a Markdown file in your fork. Do not submit it with placeholder values or interpret this unfilled template as verification.

**This unfilled template is not evidence of a successful runtime test.**

## Environment

- Result: NOT TESTED / BLOCKED / FAIL / PASS
- Runtime and surface (CLI, IDE, desktop, web):
- Runtime version and how it was obtained:
- Date (YYYY-MM-DD):
- OS and version:
- Repository commit (`git rev-parse HEAD`):
- Skill name and relative source path:
- Prerequisites available / missing (no account identifiers):

## Installation and discovery

- Exact install command or UI steps:
- Relative destination (replace home-directory usernames with `<HOME>`):
- Exact discovery command/UI action:
- Observed discovery result:
- Sanitized evidence that the host selected/read this skill, not merely a same-named file:

## Execution

- Exact request:
- Synthetic fixture path or complete safe input:
- Expected behavior:
- Observed output (safe excerpt is enough):
- Acceptance checks passed / failed / not reached:
- Reproduction steps from a clean project:

## Interpretation

- Local file/installer checks:
- Host discovery:
- Host invocation:
- Output check:
- Limitations and first blocked/failed step:
- Reusable correction or documentation suggestion:

A PASS requires discovery, invocation and the specified output checks in a real runtime. A useful BLOCKED report is welcome but does not finish end-to-end verification. Never attach tokens, session files, full private logs, private project paths or billing details.
