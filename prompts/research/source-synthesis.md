---
id: research-source-synthesis
title: Source Synthesis
category: research
version: 1.0.0
complexity: intermediate
interaction: iterative
models: portable
---

# Source Synthesis

## Overview

Turn several sources into one structured synthesis while keeping facts, disagreements and unknowns separate.

## Use When

- researching a current topic from multiple sources
- preparing a sourced article or brief

## Do Not Use When

- you only have one weak source
- you need a verbatim summary of copyrighted material

## Required Inputs

- **QUESTION**: the decision or question to answer
- **SOURCES**: source excerpts/links/notes with dates
- **AUDIENCE**: who will use the synthesis

## Copy/Paste Prompt

```text
You are an evidence-focused research editor.

QUESTION: [QUESTION]
AUDIENCE: [AUDIENCE]
SOURCES:
[SOURCES]

Build a synthesis, not a stitched summary.
1. List the strongest supported facts.
2. Separate agreement, disagreement and uncertainty.
3. Flag stale or weak evidence.
4. Answer the question only to the level the sources support.
5. End with what should be verified next.

Do not invent citations, statistics, motives or consensus.
```

## Expected Output

- supported facts table
- disagreement/uncertainty section
- concise synthesis
- verification gaps

## Quality Gate

- [ ] Every factual claim traces to supplied evidence
- [ ] Uncertainty is visible
- [ ] No invented citations

## Example Input

```text
QUESTION: What changed in AI assistant workflows this month?
AUDIENCE: creators
SOURCES: [three dated source notes]
```

## Troubleshooting

- **The answer sounds certain** → force a separate uncertainty section
- **Sources conflict** → show both claims and evidence strength

## Next Step

Route the strongest verified signal into a content brief or decision workflow.
