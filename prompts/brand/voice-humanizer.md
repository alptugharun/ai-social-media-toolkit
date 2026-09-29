---
id: brand-voice-humanizer
title: Brand Voice Humanizer
category: brand
version: 1.0.0
complexity: intermediate
interaction: single-shot
models: portable
---

# Brand Voice Humanizer

## Overview

Remove generic AI texture while preserving factual meaning, brand voice and platform fit.

## Use When

- AI-assisted drafts sound generic
- copy needs to match approved examples

## Do Not Use When

- the draft contains unverified claims that need research first
- you want to disguise authorship or evade detection systems

## Required Inputs

- **DRAFT**: text to edit
- **VOICE_EXAMPLES**: approved writing samples/rules
- **PLATFORM**: where it will be used

## Copy/Paste Prompt

```text
Edit this draft for natural brand voice.

PLATFORM: [PLATFORM]
APPROVED VOICE: [VOICE_EXAMPLES]
DRAFT:
[DRAFT]

Preserve names, dates, numbers and factual meaning.
Remove generic AI phrasing, repeated transitions, inflated adjectives, filler and robotic symmetry.
Do not add claims.
Return:
1. revised copy
2. a short change note
3. any factual sentence that still needs verification.
```

## Expected Output

- natural revised copy
- preserved facts
- verification flags

## Quality Gate

- [ ] No new factual claims
- [ ] Voice matches examples
- [ ] Rhythm feels platform-native

## Example Input

```text
PLATFORM: LinkedIn
VOICE: short, concrete, knowledgeable, no hype
DRAFT: [text]
```

## Troubleshooting

- **Rewrite changes facts** → lock factual payload before editing
- **Still sounds generic** → provide stronger approved examples

## Next Step

Run the Output Quality Auditor before publishing.
