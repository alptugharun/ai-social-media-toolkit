---
name: pinterest-opportunity-radar
description: Researches Pinterest Trends, seasonality, visual-search opportunities, Pinterest automation tools and destination-fit gaps to identify evidence-backed Pin clusters and growth opportunities. Use when the user asks what to publish on Pinterest, what is rising, what Pinterest automation to build, or how to turn Pinterest discovery into website traffic.
license: MIT
metadata:
  version: 0.1.0
  author: Alptuğ Harun
---

# Pinterest Opportunity Radar

Find evidence-backed Pinterest opportunities before content production.

## Required References

Read:

- `references/EVIDENCE-POLICY.md`
- `references/PINTEREST-AUTOMATION-PLAYBOOK.md`
- `PINTEREST-RESEARCH-FRAMEWORK.md`

Use `pinterest-growth-engine` after the opportunity has been selected.

## Evidence hierarchy

Prefer:

1. Pinterest Trends API
2. Pinterest Business / Trends evidence
3. authorized account analytics
4. current official Pinterest documentation
5. open-source ecosystem evidence
6. user-provided exports
7. clearly labeled hypotheses

Never convert a hypothesis into a "trend".

## Research questions

1. Which keywords are actually rising now?
2. Which opportunities are seasonal versus evergreen?
3. Which visual patterns can support multiple original Pins?
4. Which topics match a real destination page?
5. Which content clusters are likely to produce saves versus outbound clicks?
6. Which Pinterest automation features already have mature open-source implementations?
7. What should be built or published next?

## API-aware mode

If Pinterest Trends API access is available, collect region, keyword, WoW growth, MoM growth, YoY growth and time-series shape.

If access is unavailable, continue non-authenticated research, mark live trend evidence unavailable, and do not fabricate numbers.

## Opportunity score

When live trend data exists:

- 25% trend growth
- 20% seasonal timing
- 20% search / intent fit
- 15% visual potential
- 10% destination fit
- 10% repeatability

When live trend data does not exist, return an **incomplete score** and name the missing evidence.

## Output

# Pinterest Opportunity Radar

## Evidence Window
- Date:
- Regions:
- Pinterest API status:
- Confidence:

## Rising Keywords
| Keyword | Region | WoW | MoM | YoY | Pattern | Confidence |
| --- | --- | ---: | ---: | ---: | --- | --- |

## Seasonal Opportunities
| Topic | Planning window | Intent | Destination | Evidence |
| --- | --- | --- | --- | --- |

## Tool / Competitor Changes
| Project | Signal | Capability | Gap |
| --- | --- | --- | --- |

## Content Cluster Candidates
| Cluster | Intent | Visual potential | Destination fit | Evidence | Priority |
| --- | --- | ---: | ---: | --- | ---: |

## Best Cluster to Build
- Cluster:
- Search intent:
- Why now:
- Destination:
- Hero Pin:
- Educational Pin:
- Checklist Pin:
- Comparison Pin:
- Seasonal variant:
- KPI:

## Automation Recommendation

Separate automatic research, automatic draft generation, human-reviewed publishing and measurement.

## Guardrails
- [ ] No invented trend data
- [ ] No copied Pin
- [ ] Destination matches Pin promise
- [ ] API / access-tier requirements are explicit
- [ ] No secret committed to repository
- [ ] Human approval before live publishing unless explicitly configured otherwise

## Core Principle

**Pinterest growth starts with discovery intent, not posting volume.**
