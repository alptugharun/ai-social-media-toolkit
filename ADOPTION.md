# Adoption & Evidence Ledger

This page records **publicly defensible adoption evidence** for the AI Social Media Toolkit.

It deliberately starts sparse.

## Current public evidence

| Signal | Current evidence | What it means |
| --- | --- | --- |
| Public alpha release | `v0.3.0-alpha.1` published with 5 public release assets | versioned prerelease + measurable per-asset download surface |
| Runnable proof | two-minute demo is CI-gated | visitors can verify runnable tooling |
| External runtime verification | **not yet recorded** | documented compatibility still needs independent host evidence |
| External workflow examples | **not yet recorded** | first contributor examples are still open |
| External forks/contributions | record only when independently visible | do not infer use from internal activity |
| Paid buyer signal | **not yet recorded** | premium productization remains gated |

## Release-asset baseline — captured 2026-10-11

`v0.3.0-alpha.1` is the first Toolkit release with separate downloadable assets and integrity hashes.

| Asset | Public count at first read | Interpretation |
| --- | ---: | --- |
| `agent-skills-v0.3.0-alpha.1.zip` | **0** | full 19-skill bundle |
| `creator-context-builder-v0.3.0-alpha.1.zip` | **0** | focused foundation-skill bundle |
| `creator-frame-studio-v0.3.0-alpha.1.zip` | **0** | offline static Creator Frame Studio bundle |
| `ai-social-media-toolkit-plugin-0.6.0.zip` | **0** | deterministic skills-only Agent Plugin bundle |
| `SHA256SUMS.txt` | **0** | integrity manifest |

These were the public GitHub API counts **before maintainer verification downloads**. Immediately after that baseline, the maintainer downloaded `creator-context-builder-v0.3.0-alpha.1.zip` and `SHA256SUMS.txt` once to verify the public asset path and SHA256 integrity. Their later counters may therefore include at least one maintainer-generated download.

A release-asset download is a stronger signal of intentional artifact retrieval than raw clone telemetry, but it is still **not a unique-user, successful-install, repeat-use or customer count**.

The downloaded Creator Context Builder ZIP matched the hash published in `SHA256SUMS.txt`.

### Known internal counter movement after Sigstore signing

Workflow run `38173909007` signed the user-facing v0.3 assets with GitHub OIDC + Sigstore. To sign the exact published bytes, the workflow first downloaded each ZIP/checksum from the release. Those retrievals increment GitHub's public `download_count`.

Immediately after signing, the public counters were:

| Asset | Counter | Known internal explanation |
| --- | ---: | --- |
| `agent-skills-v0.3.0-alpha.1.zip` | **1** | Sigstore workflow retrieval |
| `ai-social-media-toolkit-plugin-0.6.0.zip` | **1** | Sigstore workflow retrieval |
| `creator-context-builder-v0.3.0-alpha.1.zip` | **2** | one maintainer integrity check + Sigstore workflow retrieval |
| `creator-frame-studio-v0.3.0-alpha.1.zip` | **1** | Sigstore workflow retrieval |
| `SHA256SUMS.txt` | **2** | one maintainer integrity check + Sigstore workflow retrieval |
| each `.sigstore.json` bundle | **0** | no retrieval at capture |

Treat these values as the **known internal baseline**. Future increases may indicate external retrieval, but even then a download counter is not a unique-user, successful-install, repeat-use or customer count.

The signing workflow completed successfully and the release exposed five additive `.sigstore.json` bundles without replacing the original downloadable files.

## GitHub traffic baseline — captured 2026-10-09

GitHub's repository traffic API reported the following for the **14-day window 2026-09-25 through 2026-10-08**:

| Signal | Value | Interpretation |
| --- | ---: | --- |
| Repository views | **90** | page-view events |
| Unique visitors | **50** | GitHub's deduplicated visitor estimate for this repo/window |
| Clone events | **5,039** | clone operations, including repeats and automation |
| Unique cloners | **907** | deduplicated clone sources; **not equivalent to 907 people** |
| Stars | **1** | lightweight public interest signal |
| Forks | **0** | no public reuse fork recorded at capture time |
| Subscribers/watchers | **0** | no repository subscriber recorded at capture time |

The clone-to-view ratio is unusually high, so clone telemetry is treated as **automation-sensitive infrastructure data**, not user adoption. CI runners, bots, repeated environments and machine identities may contribute. Do not market 5,039 clone events or 907 unique cloners as users/installations.

Useful page-path evidence in the same window:

- repository overview: **40 views / 28 unique**;
- `START-HERE.md`: **2 views / 2 unique**.

This creates a measurable onboarding question: **can more overview visitors reach a real first-run or live-demo action?** The current growth experiments are the one-click Creator Frame Studio demo and [Real User Lab #178](https://github.com/alptugharun/ai-social-media-toolkit/issues/178). Success should be measured by reproducible external reports, repeat use, useful issues/PRs and qualified implementation inquiries—not clone volume alone.

Observed referrers included GitHub plus small samples from Instagram, Threads, Bluesky, Google, LinkedIn, M8ven and Reddit. These are discovery signals only; no conversion is inferred.

## Reported onboarding feedback — reviewed 2026-10-01

`soyeladice-svg` reported a concrete own-data handoff problem in [#30](https://github.com/alptugharun/ai-social-media-toolkit/issues/30): the demo did not print the required CSV columns or direct input-contract links. This is public feedback, not proof of a complete runtime test, recurring use or traffic attribution. The comment states that only public demo/source and synthetic data were used; it supplies no full command/environment transcript.

The same account explicitly withdrew the uncompleted claims for [runtime verification #38](https://github.com/alptugharun/ai-social-media-toolkit/issues/38) and [workflow example #40](https://github.com/alptugharun/ai-social-media-toolkit/issues/40). Do not count those claims as completed contributions. The cause of the contributor's branch/PR restriction is not established by the comments.

Maintainer-created fixes, examples and passing local tests remain **internal project work**, not new external adoption. No visitor count, install count or conversion rate is inferred here.

## What counts as adoption evidence?

Examples:

- an external user reports a reproducible install/use result;
- an independent fork adapts a workflow;
- an external pull request improves a real workflow;
- the same person returns to use another release/workflow;
- a public case study demonstrates a real task;
- a buyer asks for implementation or a deeper managed version.

## What does not count?

- maintainer commits;
- automated issues created by our own workflows;
- impressions without a use event;
- a star treated as proof of successful installation;
- synthetic demo data;
- internal tests presented as external adoption.

## Adding an entry

When real evidence appears, record:

1. date;
2. public evidence link when available;
3. workflow/runtime used;
4. result reached;
5. friction discovered;
6. whether the user returned or contributed.

Never publish private user/client information without permission.

## Why keep this public?

The project should become more credible as evidence grows—not by rewriting marketing copy to sound bigger than it is.
