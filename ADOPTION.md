# Adoption & Evidence Ledger

This page records **publicly defensible adoption evidence** for the AI Social Media Toolkit.

It deliberately starts sparse.

## Current public evidence

| Signal | Current evidence | What it means |
| --- | --- | --- |
| Public alpha release | `v0.2.0-alpha.1` published | the project has a current versioned public prerelease baseline |
| Runnable proof | two-minute demo is CI-gated | visitors can verify runnable tooling |
| External runtime verification | **not yet recorded** | documented compatibility still needs independent host evidence |
| External workflow examples | **not yet recorded** | first contributor examples are still open |
| External forks/contributions | record only when independently visible | do not infer use from internal activity |
| Paid buyer signal | **not yet recorded** | premium productization remains gated |

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
