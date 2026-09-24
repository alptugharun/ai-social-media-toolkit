---
name: maps-opportunity-radar
description: Researches Google Maps, Places, Business Profile, geospatial AI, MCP, ChatGPT, Claude and Agent Skill opportunities to identify under-served map workflows. Use when the user asks what Maps-related product, skill, automation or repository to build next.
license: MIT
metadata:
  version: 0.1.0
  author: Alptuğ Harun
---

# Maps Opportunity Radar

Find evidence-backed Maps + AI opportunities without pretending novelty or virality can be guaranteed.

## Required References

Read:

- `references/EVIDENCE-POLICY.md`
- `references/GITHUB-GROWTH-PLAYBOOK.md`
- `references/MAPS-AI-OPPORTUNITY-PLAYBOOK.md`

## Research Scope

Inspect fresh signals across:

- Google Maps Platform
- Places API
- Places Aggregate API
- Google Business Profile APIs
- Google Maps Agent Skills
- Google Maps MCP projects
- ChatGPT + Maps
- Claude + Maps
- Codex + Maps
- Gemini + Maps
- local SEO
- local-rank tracking
- geospatial agents
- creator-location tools
- Timeline / Takeout tooling
- MapLibre / open geospatial tooling

## Core Questions

1. What official capability already exists?
2. What strong open-source project already solves the basic job?
3. Which user still has an unsolved workflow?
4. Can the result be measured or demonstrated?
5. Can it be built without scraping or prohibited data storage?
6. Is it useful to creators, agencies, local businesses or developers?
7. Does it fit this repository, or should it be a separate product?

## Novelty Rule

Never say:

> Nobody has ever built this.

unless comprehensive evidence actually supports that statement.

Prefer:

> Direct competition appears limited for this specific job based on the current search sample.

## Viral / Revenue Rule

Never promise:

- virality
- one million users
- sponsorship
- revenue
- GitHub Trending placement

Instead identify the mechanics that could improve distribution:

- sharp problem
- fast first result
- shareable output
- proof
- portability
- low setup friction
- trust
- timing

## Competitor Teardown

For each strong competitor capture:

- repository
- stars
- forks
- update recency
- one-line promise
- install friction
- tools / workflows
- proof
- licensing
- missing workflow

## Candidate Score

Use a transparent heuristic:

- 25% demand evidence
- 20% direct-supply gap
- 20% strategic fit
- 15% proof potential
- 15% compliance feasibility
- 5% distribution ease

Apply a strong penalty to a generic Google Maps MCP wrapper if an existing official or mature implementation already covers the same job.

## Policy Gate

Before recommending a build, run the concept through `maps-policy-guard`.

Reject or redesign concepts that depend on:

- consumer Maps UI scraping
- prohibited bulk export / permanent storage
- hidden Street View harvesting
- auto-spam outreach
- sensitive-trait inference
- fabricated review activity

## Output

# Maps Opportunity Radar

## Evidence Window
- Date:
- Sources:
- Confidence:

## Official Capability Baseline
| Capability | Official option | Implication |
| --- | --- | --- |

## Open-Source Competitor Snapshot
| Repository | Signal | Strength | Gap |
| --- | --- | --- | --- |

## Demand / Supply Proxies
| Theme | Demand signal | Direct supply | Interpretation |
| --- | --- | ---: | --- |

## Opportunity Candidates
| Candidate | User | Job | Evidence | Compliance | Score |
| --- | --- | --- | --- | --- | ---: |

## Best Prototype
- Name:
- User:
- Problem:
- Why now:
- Input:
- Output:
- Proof contract:
- Install / run path:
- Policy status:

## Separate-Product Candidates
List ideas that should not be forced into this repository.

## Human Review Gate
- [ ] Current official docs checked
- [ ] Strong competitors checked
- [ ] No fake novelty claim
- [ ] No guaranteed virality claim
- [ ] Policy architecture reviewed
- [ ] Human approval required before publishing a new skill or product

## Core Principle

**Find the missing workflow above the map API, not another wrapper around the same endpoints.**
