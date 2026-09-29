---
id: evaluation-output-quality-auditor
title: AI Output Quality Auditor
category: evaluation
version: 1.0.0
complexity: advanced
interaction: single-shot
models: portable
---

# AI Output Quality Auditor

## Overview

Review an AI-generated deliverable and return PASS, REVISE or BLOCK by criterion.

## Use When

- pre-publication review
- testing assistant/prompt quality

## Do Not Use When

- you need domain facts that were never supplied
- you expect the auditor to replace legal/medical/security review

## Required Inputs

- **OUTPUT**: deliverable to audit
- **OBJECTIVE**: what it must achieve
- **EVIDENCE**: facts/sources it may rely on
- **CONSTRAINTS**: format, rights, platform rules

## Copy/Paste Prompt

```text
Audit this AI output.

OBJECTIVE: [OBJECTIVE]
EVIDENCE: [EVIDENCE]
CONSTRAINTS: [CONSTRAINTS]
OUTPUT:
[OUTPUT]

Score each criterion PASS / REVISE / BLOCK:
- factual support
- objective fit
- clarity
- originality
- platform/format fit
- unsupported claims
- rights/privacy risk
- AI artifacts
- CTA/destination fit
- measurement readiness

For every REVISE/BLOCK, give one concrete fix. Do not rewrite the entire output unless asked.
```

## Expected Output

- criterion table
- specific fixes
- overall disposition

## Quality Gate

- [ ] Can actually block publication
- [ ] Evidence gaps are explicit
- [ ] No empty praise

## Example Input

```text
OBJECTIVE: publish a 30-second Reel
EVIDENCE: [source notes]
CONSTRAINTS: no unsupported numbers
OUTPUT: [draft]
```

## Troubleshooting

- **Everything passes too easily** → require evidence references per factual criterion
- **Audit becomes a rewrite** → keep fixes scoped

## Next Step

Apply only the required fixes, then rerun the audit.
