# Runtime Verification Matrix

**A valid skill file, a successful installer and a real host execution are three different checks.** None of the instructions or templates below is itself host-verification evidence.

## Current evidence

| Runtime / target | What the repository can test locally | Independent host result |
| --- | --- | --- |
| Portable `.agents/skills/` | File discovery and installer placement | NOT TESTED until a dated report is accepted |
| Claude Code | Installer placement in `.claude/skills/` | NOT TESTED |
| OpenAI Codex | Portable `.agents/skills/` placement; legacy `codex` target still places files in `.codex/skills/` | NOT TESTED |
| Cursor | Installer placement in `.cursor/skills/` | NOT TESTED |
| Gemini CLI | Manifest structure and installer placement | NOT TESTED |
| GitHub Copilot | Installer placement in `.github/skills/` / `.copilot/skills/` | NOT TESTED |
| Grok target | Installer placement in `.grok/skills/`; actual host capability needs separate evidence | NOT TESTED |
| AI Workbench MCP (stdio) | Package build/install, initialize handshake, `tools/list`, named tool calls and bounded failure paths | NOT TESTED in an independent MCP host |

Installer targets describe filesystem behavior, not a guarantee that every product or plan supports them. The contributor's withdrawal in [#38](https://github.com/alptugharun/ai-social-media-toolkit/issues/38) is not a FAIL and is not a PASS.

## Result meanings

- **PASS:** the stated test ran in the named runtime/version; discovery, invocation and output acceptance all passed.
- **FAIL:** the test ran but an acceptance check failed. Record the first failure.
- **BLOCKED:** missing access, environment or another dependency prevented completion. State the blocked step.
- **NOT TESTED:** no execution evidence is available.

Keep local file checks, installer tests, host discovery, host invocation and output quality separate in every report. Do not label a blocked or untested host as supported.

## Prerequisites

Choose **one** runtime you can already access. You need its installed client or supported UI, valid account/model access where required, Git, and Python 3.11 for the repository's installer/scoring commands. Runtime usage may have separate plan or usage costs. You do not need write access to this repository, and there is no need to purchase a plan merely to claim an issue.

Missing a prerequisite? Submit a BLOCKED report or choose a documentation-only contribution instead. Do not bypass an organization policy or relax sandbox permissions.

## Codex: one reproducible test

Official behavior checked against [OpenAI's skills documentation](https://developers.openai.com/codex/skills) on 2026-10-01: repository-local discovery uses `.agents/skills/`; explicit skill selection in Codex uses `$skill-name`. This describes documented behavior, not our own host test. Use the portable installer target below rather than assuming the legacy `.codex/skills/` target works in your version.

### 1. Capture the baseline

In your local checkout:

```bash
git rev-parse HEAD
python --version
python tools/install_skills.py --target agents --scope project --skill signal-to-content --dry-run
```

Record your Codex version from the client/version screen or its version command. Check [`skills/signal-to-content/SKILL.md`](../skills/signal-to-content/SKILL.md) before installing.

### 2. Install only the skill under test

```bash
python tools/install_skills.py --target agents --scope project --skill signal-to-content
```

Expected local file: `.agents/skills/signal-to-content/SKILL.md`. This proves only placement. If it already exists, inspect it; do not use `--force` merely to get past the message. Keep generated local skill copies out of your contribution commit.

### 3. Verify discovery in the real host

Start Codex in this checkout. Use its skills selector (`/skills` or the `$` selector where supported) and record whether **signal-to-content** appears. Record the actual UI/command and result for your client version. Restart the client if newly installed files are not picked up. If discovery is unavailable or unsuccessful, stop and record BLOCKED or FAIL as appropriate; do not manually paste the skill body and call that discovery.

### 4. Invoke the installed skill

Paste this **inside Codex**, not into PowerShell/bash:

```text
Use $signal-to-content with examples/signal2content-opportunities.csv.
All rows are synthetic editorial ratings, not measured platform trends.
Use the supplied scores and the skill's documented heuristic to rank the opportunities.
Do not browse or invent sources, demand, reach or revenue.
Return a Signal to Content Brief: Research Input, Opportunity Table,
Source-Specific Elements Not to Copy, one Original Content Test,
a proposed Content Ladder, and Review Gate.
Mark production, publication and performance measurement as not executed.
Do not publish, connect accounts, change permissions or access credentials.
```

The expected top synthetic opportunity is **Pinterest seasonal visual series**, score **83.05**. A local comparison command is:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --top 1
```

That local command is only a deterministic comparison; it does not substitute for the Codex result.

### 5. Check the result

A PASS needs evidence that the real host discovered and invoked the skill, the requested sections are present, the top score agrees within 0.01, synthetic evidence is labelled, and no publication/performance claim is invented. Save a sanitized excerpt and the exact request. An assistant merely saying “I used the skill” is insufficient by itself; include available selector/tool/file-read evidence.

## AI Workbench MCP: independent host verification

The standalone package lives at [`packages/ai-workbench-mcp`](../packages/ai-workbench-mcp/README.md). Maintainer CI verifies the local package boundary, but that is not independent host evidence.

From a clean checkout:

```bash
python -m pip install --no-deps ./packages/ai-workbench-mcp
```

Configure a current stdio-capable MCP host to launch:

```text
alptugharun-ai-workbench-mcp
```

A useful report records the host/version, OS/Python version, discovery of `list_prompts`, `render_prompt` and `get_assistant`, one successful call, one invalid-input result and the first confusing or blocked step. Submit MCP-specific evidence on [#110](https://github.com/alptugharun/ai-social-media-toolkit/issues/110).

## Other runtimes

Use the same evidence requirements and [report template](RUNTIME-VERIFICATION-TEMPLATE.md), but follow the chosen host's current official installation and invocation instructions. Do not reuse Codex slash commands or `$` syntax in another host without checking. Start with [Installation](INSTALLATION.md); record any version-specific mismatch rather than claiming universal compatibility.

## Submit your evidence

For Agent Skill host evidence, post the filled [report template](RUNTIME-VERIFICATION-TEMPLATE.md) on [#38](https://github.com/alptugharun/ai-social-media-toolkit/issues/38). For the standalone MCP package, use [#110](https://github.com/alptugharun/ai-social-media-toolkit/issues/110). Use the [fork → PR guide](../CONTRIBUTING.md#submit-through-a-fork) for documentation or code corrections. A BLOCKED/FAIL report is useful feedback but does not complete a successful end-to-end verification task.

Only promote a host to verified after a maintainer can reproduce the submitted, dated runtime/version-specific evidence. Local CI success alone never changes this matrix to PASS.
