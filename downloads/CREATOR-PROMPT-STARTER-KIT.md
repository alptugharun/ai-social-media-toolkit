# Stop Prompt-Hopping — Build a Repeatable Content System

Turn scattered AI requests into one connected workflow: evidence → angle → hook → content → QA → winner expansion.

**Need the full walkthrough?** See [How to Use Everything](../docs/HOW-TO-USE-EVERYTHING.md) for setup, example inputs, expected outputs and troubleshooting.

A compact, reusable prompt system for turning a content objective into researched, platform-native execution.

This is not a “100 random prompts” list. Use the prompts as a connected sequence.

## How to use

Recommended path:

**Objective → Audience → Evidence → Angle → Hook → Script/Copy → Visual Direction → Platform Adaptation → QA → Winner Expansion**

Replace bracketed fields with real inputs. If evidence is missing, the model should say so rather than inventing it.

---

## 1. Audience Problem Mapper

**Use when:** the topic is known, but the audience problem is still vague.

**Inputs**

- Audience: [AUDIENCE]
- Topic: [TOPIC]
- Offer or objective: [OBJECTIVE]
- Known evidence: [COMMENTS / SEARCHES / CLIENT QUESTIONS / ANALYTICS]

**Prompt**

> Act as a social-content strategist. Map the most likely audience problems around [TOPIC] for [AUDIENCE], but distinguish evidence from hypothesis. Use [KNOWN EVIDENCE] as the primary source. Return: 1) recurring problem, 2) audience language, 3) desired outcome, 4) objection, 5) content opportunity, 6) evidence strength. Do not invent search volume, trend status or user quotes.

**Quality check**

A useful output should contain language that can become a hook or content angle, not only broad demographic observations.

---

## 2. Evidence-to-Angle Generator

**Use when:** you have a signal and need original content angles.

**Prompt**

> Using this evidence: [EVIDENCE], generate 5 original content angles for [PLATFORM]. For each angle include: audience tension, promise, proof source, execution format and why it is different from simply copying the source. Reject any angle that depends on a fact not supported by the evidence.

**Quality check**

Every angle should trace back to a source or be clearly labeled as a hypothesis.

---

## 3. Hook Stress Test

**Use when:** a topic is useful but the opening is weak.

**Prompt**

> Write 12 hook options for this idea: [IDEA]. Split them into curiosity, specificity, contrarian, problem-first and result-first styles. Avoid fake urgency, unsupported numbers, “you won’t believe” clichés and guaranteed outcomes. Then rank the hooks by clarity, specificity and platform fit for [PLATFORM]. Explain the top 3 in one sentence each.

**Quality check**

The strongest hook should still be true if the viewer only sees the first sentence.

---

## 4. 30–35 Second Reels Script

**Use when:** creating short-form voiceover content.

**Prompt**

> Turn [TOPIC] into a 30–35 second Reels voiceover for [AUDIENCE]. Structure it as: 0–3 sec hook, 3–10 sec context, 10–25 sec value, 25–32 sec payoff, final CTA. Use natural spoken Turkish, short sentences and no filler. Keep factual claims inside [EVIDENCE]. Output voiceover only, followed by a separate timing table.

**Quality check**

Read it aloud. If it sounds like an article rather than speech, shorten it.

---

## 5. Platform-Native Repurposer

**Use when:** one source needs to become multiple assets.

**Prompt**

> Repurpose [SOURCE] into native versions for Instagram Reels, Instagram carousel, Pinterest, LinkedIn and a blog teaser. Preserve the core fact but change the format, opening, CTA and information density for each platform. Do not cross-post identical copy. For every version state the primary platform objective.

**Quality check**

Each version should feel designed for its platform rather than resized from one master post.

---

## 6. Pinterest Search Intent Builder

**Use when:** building Pinterest content clusters.

**Prompt**

> For [TOPIC], build a Pinterest search-intent cluster using only the keyword evidence I provide: [KEYWORD EVIDENCE]. Group into broad intent, problem intent, inspiration intent, seasonal intent and commercial intent. Then propose 7 Pin concepts: hero, educational, checklist, comparison, seasonal, search-led and visual-discovery. If live Pinterest evidence is unavailable, label the cluster as a hypothesis.

**Quality check**

Every Pin concept should have a distinct search intent and destination purpose.

---

## 7. Visual Direction Builder

**Use when:** a content concept needs an image-production brief.

**Prompt**

> Convert this content concept into a visual production brief: [CONCEPT]. Return subject, setting, composition, camera distance, lighting, texture/material details, styling, negative constraints and aspect ratio. Keep the scene coherent and avoid adding decorative objects that do not support the concept. If the asset is for social media, optimize for [FORMAT].

**Quality check**

A designer or image model should be able to execute the brief without asking what the focal point is.

---

## 8. Brand Voice Humanizer

**Use when:** AI copy sounds generic.

**Prompt**

> Rewrite [DRAFT] in this brand voice: [VOICE EXAMPLES / RULES]. Preserve factual meaning. Remove generic AI phrasing, unnecessary headings, repetitive transitions and inflated claims. Keep any useful specificity. Return the revised copy and a short note listing the biggest tonal changes.

**Quality check**

The rewrite should sound like the brand, not simply “more casual.”

---

## 9. Content QA Gate

**Use when:** content is nearly ready to publish.

**Prompt**

> Audit this draft before publication: [DRAFT]. Check factual support, platform fit, clarity, originality, misleading claims, CTA fit, repetition, copyright risk, AI artifacts and accessibility. Return PASS, REVISE or BLOCK for each criterion. Do not rewrite unless a criterion fails.

**Quality check**

The audit should be capable of stopping publication, not only praising the draft.

---

## 10. Winner Expansion

**Use when:** a post has proven performance.

**Inputs**

- Winning post: [POST]
- Measured result: [REAL METRICS]
- Baseline: [BASELINE]
- Audience responses: [COMMENTS / SAVES / CLICKS / WATCH TIME]

**Prompt**

> Analyze why this content may have outperformed the creator’s baseline using only [REAL METRICS], [BASELINE] and [AUDIENCE RESPONSES]. Separate evidence from interpretation. Generate 6 follow-up tests that preserve the winning mechanism without duplicating the original post. For each test state what variable changes and what metric should be watched.

**Quality check**

Expansion should test the mechanism, not merely repost the same idea.

---

## Recommended workflow

1. Audience Problem Mapper
2. Evidence-to-Angle Generator
3. Hook Stress Test
4. Reels Script or platform-native copy
5. Visual Direction Builder
6. Brand Voice Humanizer
7. Content QA Gate
8. Publish
9. Measure
10. Winner Expansion

## Core rule

**A prompt is useful when it improves a repeatable decision or workflow. Prompt count is not product quality.**
