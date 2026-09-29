# Runtime Verification Matrix

The toolkit uses portable `SKILL.md` packages and includes installer paths for several Agent Skills hosts.

**Documented compatibility is not the same as independently verified runtime behavior.** This matrix separates what the repository tests itself from what still needs real host verification.

## Status meanings

- **CI verified** — repository-owned installer/path behavior is covered by automated tests.
- **Host verified** — a real host/version has been tested end-to-end and evidence is recorded.
- **Needs external verification** — documentation/path exists, but we still want an independent real-host report.

| Runtime | Install path / method | Repository CI | Independent host verification | Evidence / next action |
| --- | --- | --- | --- | --- |
| Portable Agent Skills | `.agents/skills/` | CI verified | Needs external verification | Run one skill in a compatible host and report discovery behavior |
| Claude Code | `~/.claude/skills/` / project scope | installer path tested | Needs external verification | Issue #38 |
| OpenAI Codex | `~/.codex/skills/` / project scope | installer path tested | Needs external verification | Issue #38 |
| Cursor | `~/.cursor/skills/` / project scope | installer path tested | Needs external verification | Issue #38 |
| Gemini CLI | extension / skill install / `.gemini/skills/` | manifests + installer tested | Needs external verification | Issue #38 |
| GitHub Copilot | `~/.copilot/skills/` / `.github/skills/` | installer path tested | Needs external verification | Issue #38 |
| Grok | `~/.grok/skills/` | installer path tested | Needs external verification | Issue #38 |

## How to verify one runtime

1. Record runtime name and version.
2. Record OS.
3. Follow `docs/INSTALLATION.md` without undocumented steps.
4. Install one skill first.
5. Confirm the host discovers it.
6. Run one request from `docs/HOW-TO-USE-EVERYTHING.md`.
7. Report success/failure and the first friction point.

Do not post credentials, tokens, private project paths or client data.

## Promotion rule

A runtime moves to **Host verified** only when the evidence is reproducible and tied to a real runtime/version. Marketing copy should not imply stronger compatibility than this matrix supports.
