# Trust & Discovery Matrix

Last reviewed: **2026-10-11**

This document explains the external trust/discovery systems that currently matter to the public projects, what they actually measure, what can be improved through engineering, and what must be earned through real adoption.

The objective is **not** to game scores.

The objective is to make the software easier to inspect, safer to install, clearer to use and more credible to external reviewers.

---

## 1. Current snapshot

| Surface | Current observed state | What is strong | What remains |
| --- | --- | --- | --- |
| **M8ven — Toolkit** | 89/100, B, stale snapshot from 2026-10-03 | Verified Publisher, Sandbox Verified, Live Monitored, no concerning exfiltration finding | listing still sees old commit / old tool count; reputation/adoption caps grade |
| **M8ven — AI Workbench MCP** | 74/100, C, old snapshot | clean static findings | listing unclaimed, Live Monitoring not connected, old 2-tool snapshot |
| **OpenSSF — Toolkit** | 6.3/10 snapshot on 2026-10-11 | CI 10, SAST 10, pinned dependencies 10, token permissions 10, security policy 10, vulnerabilities 10 | Snapshot showed Signed-Releases 0; GitHub OIDC + Sigstore bundles were added afterward and need a fresh external rescan; Branch Protection 4; Code Review/Contributors/Maintained remain maturity-limited; Packaging not detected |
| **OpenSSF — AI Workbench MCP** | 6.7/10 | Packaging 10, Signed-Releases 8, CI/SAST/token permissions/vulnerabilities 10 | security policy content scored 3; branch/review/maturity limits; one pinning finding |
| **OpenSSF — Safety Auditor** | 6.4/10 | CI/SAST/token/dependency-update/vulnerabilities strong | security policy scored 3; no package/release; maturity/review limits |
| **OpenSSF — Creator Signal Lab** | 6.5/10 | CI/SAST/pinning/token/vulnerabilities strong | security policy scored 3; no package/release; maturity/review limits |
| **Official MCP Registry** | AI Workbench MCP active | namespace/package ownership verified; standardized discovery | registry presence is not a security certificate or host-compatibility guarantee |
| **Glama — AI Workbench MCP** | independently inspected, 3 tools, TDQS A ~4/5 | narrow tool surface, good naming/disambiguation, read-only/idempotent behavior | listing claim pending; usage guidance can be sharper; external responsiveness signal weak |
| **skills.sh** | install telemetry is the relevant signal | standardized install/discovery | real external installs must be earned; do not self-install/farm counts |

External systems can lag behind main. Always compare the commit/version named by the external service with the current repository state.

---

# 2. M8ven

## What it rewards

Observed M8ven findings across public listings show strong emphasis on:

- publisher identity / ownership;
- code or sandbox verification;
- Live Monitoring;
- absence of credential exfiltration / surprising sensitive access;
- license and README;
- complete MCP tool annotations;
- every tool referenced by tests;
- accurate destructive/read-only behavior;
- adoption/reputation.

## Common reasons for weak scores

- missing one or more of the four tool hints;
- tool handlers not referenced by name in tests;
- no test files;
- no license;
- destructive behavior without `destructiveHint:true`;
- secrets flowing to logs;
- shell execution;
- stale/unclaimed listing;
- low reputation/adoption.

## Toolkit posture

Current code already requires all four explicit boolean hints:

- `readOnlyHint`;
- `destructiveHint`;
- `idempotentHint`;
- `openWorldHint`.

Current release-readiness also checks name-level test coverage.

The public M8ven Toolkit page is stale and still reports an older commit/tool count. Do not modify correct code merely to satisfy a stale snapshot.

## AI Workbench MCP posture

Current standalone code exposes three tools and current public docs/Glama see all three. M8ven still shows an older two-tool unclaimed snapshot.

Remaining non-code action:

- claim the listing;
- connect Live Monitoring/GitHub App;
- ask/rely on re-scan of current main.

This requires the external account/UI and should not be faked in repository metadata.

---

# 3. OpenSSF Scorecard

OpenSSF Scorecard is a supply-chain security health signal.

High-value checks for these repositories include:

- **Pinned-Dependencies**
- **Token-Permissions**
- **CI-Tests**
- **SAST**
- **Dependency-Update-Tool**
- **Security-Policy**
- **Branch-Protection**
- **Signed-Releases**
- **Vulnerabilities**
- **Packaging**
- **Binary-Artifacts**

## What we should fix

### Pinned dependencies

GitHub Actions should use immutable full commit SHAs where supported.

Keep Dependabot enabled so pinned dependencies are not frozen forever.

### Token permissions

Top-level workflow permissions should be read-only/minimal.

Write permissions should exist only on the job that needs them.

### CI / SAST

Keep tests and CodeQL on relevant PR/main paths.

A green local run is not a replacement for CI.

### Security policy

A strong SECURITY.md should include:

- what counts as a vulnerability;
- a private reporting URL/email;
- what information to include;
- coordinated disclosure expectations;
- a response/acknowledgement target;
- no request to publish secrets/exploit details publicly.

### Signed releases

Release artifacts should carry cryptographic signing/provenance.

The flagship uses GitHub OIDC + Sigstore to produce public `.sigstore.json` bundles for user-facing ZIP/checksum assets. The original downloadable files remain unchanged; signatures are additive evidence.

A signature proves artifact identity/integrity for the signed bytes and signing workflow identity. It does not prove the software is vulnerability-free.

**Applied 2026-10-11:** workflow run `38173909007` successfully signed all five user-facing v0.3 assets and uploaded public `.sigstore.json` bundles. This is an applied remediation; OpenSSF should only be reported as improved after its external API rescans the signed release.

### Branch protection / Code Review

This is where score chasing can become harmful.

OpenSSF's branch score is tiered and code review naturally expects multiple reviewers.

For a single-maintainer repository:

- keep force-push/deletion blocked;
- require status checks where practical;
- use PRs for substantial changes;
- do **not** create fake reviewers/accounts to manufacture review evidence.

A real second maintainer/reviewer can improve this later.

### Maintained

Very new repositories can receive a zero because they are too young to establish maintenance history.

There is nothing honest to “fix” immediately. Keep maintaining them.

### Contributors

Real external contributors improve this.

Do not manufacture contributor diversity.

### Fuzzing

Scorecard's detectable fuzzing support does not cover every language/workflow equally. Add fuzz/property testing only when it materially improves the actual parser/protocol risk surface, not for points.

### Packaging

The standalone MCP has a real PyPI package and therefore scores well.

Not every documentation/tool hub should be forced into a language package solely to satisfy the check.

---

# 4. Official MCP Registry

The official Registry is a metadata/discovery layer.

It validates things such as:

- namespace authentication;
- package ownership;
- allowed public package registries;
- server metadata/schema requirements.

For PyPI packages, the ownership marker must match the MCP server name.

The Registry hosts metadata, not the package itself.

## What registry presence proves

It provides evidence that:

- a standardized server identity exists;
- the publisher has satisfied registry ownership/auth requirements;
- installation metadata can be discovered.

## What it does not prove

It does not prove:

- no vulnerability exists;
- every MCP host is compatible;
- the server's runtime behavior is always safe;
- the project has real adoption.

Keep Registry, code/security audit and host verification separate.

---

# 5. Glama

Glama gives an independent view of the MCP server.

For AI Workbench MCP it currently sees:

- 3 tools;
- read-only/idempotent annotations;
- a narrow local server;
- TDQS A around 4/5.

Useful TDQS-style questions include:

- Is the tool name unambiguous?
- Does the description state the specific action/resource?
- Does it explain when to use this tool versus sibling tools?
- Are parameter relationships clear?
- Are side effects/auth/network behavior clear?
- Is the description concise enough for an agent to choose correctly?

## Current improvement target

Tool descriptions should explicitly route:

- use `list_prompts` first for valid IDs;
- use `render_prompt` for one filled prompt;
- use `get_assistant` for a host-formatted assistant blueprint.

A good tool description helps the model choose the right tool before execution.

---

# 6. skills.sh

skills.sh ranks Agent Skills partly from anonymous install telemetry produced by the skills CLI.

This makes a simple install command important:

```bash
npx skills add owner/repo --list
npx skills add owner/repo --skill specific-skill
```

It also means:

**do not self-install repeatedly to inflate telemetry.**

Real external install interest is the signal we want.

---

# 7. What users repeatedly care about

Across MCP/Agent Skill community discussions and security guidance, recurring concerns include:

1. **What exactly will this execute?**
2. **Does it use network access?**
3. **Can it read credentials/environment/files?**
4. **Does it mutate anything?**
5. **Can I inspect it before install?**
6. **Can remote behavior change later?**
7. **How do I know which tool to call?**
8. **How do I reproduce the maintainer's “works” claim?**
9. **What is a real measured result versus a heuristic?**
10. **How do I uninstall/update it?**

This is why the portfolio emphasizes:

- read-only MCP boundaries where possible;
- Agent Skill static inspection;
- MCP configuration review;
- explicit tool hints;
- local no-key first runs;
- doctor commands;
- failure-first troubleshooting;
- versioned downloads/checksums/signatures;
- evidence/adoption ledgers.

---

# 8. Static trust is not runtime trust

A recurring security concern in MCP discussions is behavior drift:

A static manifest/source review can look clean at install time, while a remote service may behave differently later.

Therefore:

- Safety Auditor = pre-install static evidence;
- Permission Inspector = pre-connect configuration evidence;
- tool hints = declared behavior;
- CodeQL/Scorecard/M8ven = code/supply-chain signals;
- Live Monitoring/runtime network controls = runtime evidence.

Do not collapse those into “safe.”

---

# 9. Why choose this portfolio?

The differentiator should not be “more files.”

The public promise is:

**smallest useful layer + inspectable permissions + reproducible first result + explicit limits.**

A visitor should be able to answer:

- What is it?
- Why would I use it?
- What do I run first?
- What should happen?
- What can it access?
- How do I verify it?
- What does the proof not establish?
- Where do I report failure?

If any public surface cannot answer those, documentation is incomplete.

---

# 10. Trust improvement policy

## Always do

- pin build/release dependencies;
- least-privilege tokens;
- CI + CodeQL;
- security policy and private reporting;
- explicit tool permission hints;
- name-level tests for public tools;
- versioned reproducible releases;
- checksums/signatures where users download artifacts;
- clear install/update/uninstall/troubleshooting;
- synthetic examples before private/real data;
- real adoption evidence separated from maintainer activity.

## Never do for a score

- fake reviewers;
- alternate-account contributors;
- self-star/star exchange;
- fake installs/downloads;
- meaningless releases/packages;
- weaken tests;
- add broad permissions only to satisfy an integration;
- call a static scan a certification;
- claim stale external ratings as current.

---

# 11. Review cadence

The GitHub Growth Guardian should periodically re-check:

- M8ven commit/tool count/grade/findings;
- OpenSSF Scorecard per-check scores;
- Official MCP Registry status/version;
- Glama tool/schema snapshot and TDQS issues;
- skills.sh listing/install evidence when available;
- GitHub release asset downloads;
- vulnerabilities/security alerts;
- Real User Lab and external contributor activity.

Only notify on a meaningful change or actionable blocker.

