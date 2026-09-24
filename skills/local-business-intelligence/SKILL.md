---
name: local-business-intelligence
description: Turns permitted Google Maps, Places, Places Aggregate and user-owned Business Profile signals into market, content, creator-location, sponsorship and agency insights. Use for local-business research, local content gaps, venue scouting, market-density questions, GBP performance analysis or human-reviewed local partnership discovery.
license: MIT
metadata:
  version: 0.1.0
  author: Alptuğ Harun
---

# Local Business Intelligence

Convert location intelligence into useful creator, agency and business decisions.

This skill is a workflow layer, not a scraping engine.

## Required References

Read:

- `references/EVIDENCE-POLICY.md`
- `references/MAPS-AI-OPPORTUNITY-PLAYBOOK.md`

For a new architecture or questionable data flow, use `maps-policy-guard` first.

## Modes

### Market Density / Expansion

Use aggregate or permitted live data to answer:

- How dense is this category in the target area?
- How does one area compare with another?
- Where does a service appear under-represented?
- Which hypotheses should be investigated further?

Prefer Places Aggregate API for density/count questions.

Do not present place density as guaranteed revenue or investment return.

### Live Place Discovery

Use live place search for a narrow, user-requested task.

Examples:

- find suitable cafes for a creator shoot
- compare nearby venues
- shortlist businesses that match a campaign
- plan a route across selected places

Return only what is necessary for the task.

Do not construct a permanent bulk lead database from Google Maps content.

### Owned Business Profile Performance

When the user has authorized access to managed locations, analyze:

- Maps / Search impressions
- website clicks
- calls
- direction requests
- supported search-keyword impressions
- review themes
- response gaps
- period-over-period changes

Separate observed metrics from interpretation.

### Review Intelligence

For authorized / user-provided reviews:

- recurring praise
- recurring friction
- unanswered questions
- service confusion
- local language
- content ideas
- response-draft suggestions

Keep replies as drafts unless the user explicitly authorizes a supported write action.

### Creator Location Scout

Inputs:

- city / area
- creator niche
- visual concept
- time window
- practical constraints

Output:

- short venue list
- why each place fits
- opening / access considerations when available
- route logic
- Reels / Shorts concept
- shot list
- collaboration angle
- fallback option

### Local Sponsor-Fit Shortlist

Inputs:

- creator audience
- niche
- campaign idea
- geography
- brand exclusions

Output:

- small human-review shortlist
- fit rationale
- public evidence
- possible collaboration concept
- research gaps

Do not auto-send mass outreach.

### Local Content Gap Engine

Combine first-party / authorized signals such as:

- GBP search-query data
- GBP performance metrics
- review themes
- business FAQs
- permitted local category context

Create:

- high-intent content gaps
- FAQ themes
- Reels concepts
- carousel concepts
- local landing-page briefs
- Pinterest / visual-search angles where relevant
- KPI plan

## Evidence Labels

Every important claim should be labeled implicitly or explicitly as:

- **Observed**
- **Inferred**
- **Recommended**

## Output

# Local Business Intelligence Brief

## Objective
- Business / creator:
- Geography:
- Mode:
- Time window:

## Evidence
| Signal | Source | Date | Observation | Confidence |
| --- | --- | --- | --- | --- |

## Findings
Prioritize actionable findings.

## Recommended Tests
| Test | Why | Effort | KPI |
| --- | --- | ---: | --- |

## Content / Campaign Opportunities
Only when relevant.

## Data & Policy Check
- source:
- persistence:
- authorization:
- human approval required:
- policy status:

## Next Decision
Choose the smallest useful next action.

## Core Principle

**Use local data to make a better decision, not to manufacture a larger database.**
