---
id: assistants-narrow-assistant-builder
title: Narrow AI Assistant Builder
category: assistants
version: 1.0.0
complexity: intermediate
interaction: iterative
models: portable
---

# Narrow AI Assistant Builder

## Overview

Design a reusable assistant for one repeated job, with clear boundaries and test cases.

## Use When

- building a Claude Project, Gemini Gem, managed-workspace GPT or reusable system prompt
- turning repeated instructions into a stable assistant

## Do Not Use When

- you want one assistant to do every business function
- the workflow is not understood manually yet

## Required Inputs

- **JOB**: one repeated job
- **INPUTS**: what the user will provide
- **OUTPUT**: what success looks like
- **BOUNDARIES**: what it must not claim or do

## Copy/Paste Prompt

```text
Design a narrow reusable AI assistant.

JOB: [JOB]
INPUTS: [INPUTS]
OUTPUT: [OUTPUT]
BOUNDARIES: [BOUNDARIES]

Produce:
1. Name
2. One-sentence description
3. System/project instructions
4. Required context/knowledge
5. 5 realistic starter requests
6. Output contract
7. Failure / escalation rules
8. 5 acceptance tests

Keep the assistant narrow enough to evaluate. Do not pretend it has tools, memory, accounts or live data that are not actually connected.
```

## Expected Output

- assistant instructions
- starter prompts
- acceptance tests
- failure rules

## Quality Gate

- [ ] One clear job
- [ ] No fake capabilities
- [ ] Test cases are observable

## Example Input

```text
JOB: turn evidence into 30-second Reels packages
INPUTS: topic, audience, sources
OUTPUT: timed script + shot plan + QA
```

## Troubleshooting

- **Assistant wanders** → narrow the job and add stop conditions
- **Outputs vary too much** → tighten the output contract

## Next Step

Adapt the blueprint using the platform guide in assistants/ and test with three real tasks.
