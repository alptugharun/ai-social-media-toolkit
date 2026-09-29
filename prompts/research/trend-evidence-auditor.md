---
id: research-trend-evidence-auditor
title: Trend Evidence Auditor
category: research
version: 1.0.0
complexity: advanced
interaction: iterative
models: portable
---

# Trend Evidence Auditor

## Overview

Decide whether a supposed trend is current evidence, seasonality, recycled hype or an unsupported hypothesis.

## Use When

- evaluating social or AI trends
- deciding whether to produce trend-led content

## Do Not Use When

- you have no dated evidence
- you want guaranteed virality predictions

## Required Inputs

- **CLAIM**: the trend claim
- **EVIDENCE**: dated platform/source signals
- **MARKET**: country/audience/platform context

## Copy/Paste Prompt

```text
Audit this trend claim.

CLAIM: [CLAIM]
MARKET: [MARKET]
EVIDENCE:
[EVIDENCE]

Return:
- VERIFIED SIGNALS
- WEAK / INDIRECT SIGNALS
- SEASONALITY OR RECYCLED-RISK
- MISSING EVIDENCE
- CURRENT STATE: EARLY / RISING / ESTABLISHED / STALE / UNKNOWN
- CONTENT DECISION: TEST / WATCH / SKIP

Never fabricate search volume, growth percentages or platform-wide popularity.
```

## Expected Output

- dated evidence classification
- explicit trend state
- test/watch/skip decision

## Quality Gate

- [ ] Freshness is evaluated
- [ ] Market context is explicit
- [ ] No fake numbers

## Example Input

```text
CLAIM: 'dark romantic makeup is rising'
MARKET: US + Pinterest/Instagram
EVIDENCE: [dated signals]
```

## Troubleshooting

- **Evidence is platform-specific** → do not generalize beyond that platform
- **Only one weak signal exists** → return UNKNOWN/WATCH

## Next Step

If TEST, create one original execution and define the metric before publishing.
