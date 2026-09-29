---
id: automation-approval-gated-workflow
title: Approval-Gated Automation Designer
category: automation
version: 1.0.0
complexity: advanced
interaction: iterative
models: portable
---

# Approval-Gated Automation Designer

## Overview

Turn a manual repeatable process into an automation design that keeps risky writes behind approval.

## Use When

- designing Zapier/Make/n8n/GitHub Actions workflows
- automating research, drafts or reporting

## Do Not Use When

- the manual process is still unreliable
- the flow requires bypassing permissions or platform policy

## Required Inputs

- **MANUAL_FLOW**: current manual steps
- **SYSTEMS**: apps/APIs involved
- **RISKY_WRITES**: publishing, billing, deletion or external writes
- **SUCCESS**: observable completion evidence

## Copy/Paste Prompt

```text
Convert this manual process into an approval-gated automation.

MANUAL FLOW: [MANUAL_FLOW]
SYSTEMS: [SYSTEMS]
RISKY WRITES: [RISKY_WRITES]
SUCCESS: [SUCCESS]

Return:
- trigger
- state/checkpoint
- each processing step
- deduplication/idempotency key
- approval gate
- write step
- read-back verification
- retry policy
- rollback/stop condition
- audit log fields

Never hide a required human/platform approval. Never treat a queued write as a verified publish.
```

## Expected Output

- workflow map
- approval and rollback design
- failure behavior
- verification step

## Quality Gate

- [ ] Idempotency exists
- [ ] Writes are verified
- [ ] Unknown failures do not blind-retry

## Example Input

```text
MANUAL FLOW: source URL → brief → caption → schedule
SYSTEMS: RSS, AI, scheduler
RISKY WRITES: external scheduling
SUCCESS: scheduled item can be read back
```

## Troubleshooting

- **Duplicates appear** → define a stable dedup key
- **Write status is ambiguous** → read back before retry

## Next Step

Implement first with sample data and manual triggering before adding a schedule.
