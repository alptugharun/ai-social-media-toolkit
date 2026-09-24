---
name: pinterest-growth-engine
description: Builds evidence-aware Pinterest keyword maps, seasonal opportunity clusters, board architecture, pin concepts, visual-series plans, and website traffic paths. Use for Pinterest research, visual search, trend planning, pin systems, and Pinterest-to-site growth.
license: MIT
metadata:
  version: 0.1.0
  author: Alptuğ Harun
---

# Pinterest Growth Engine

Treat Pinterest as a visual discovery and search system, not only a social feed.

## Evidence

Use live search, Pinterest data, trend tools, or user-provided exports when available.

Never invent search volume or trend status.

If only autocomplete / related terms are available, label them correctly.

When live Pinterest Trends API evidence is required, route discovery through `pinterest-opportunity-radar` first.

Do not scrape the consumer Pinterest UI as the primary evidence source.

## Workflow

1. Define niche, audience, market, season, and destination.
2. Collect seed keywords.
3. Expand into:
   - supporting keywords
   - long-tail keywords
   - seasonal keywords
   - commercial / product intent
   - informational intent
   - aesthetic / visual language
4. Cluster keywords by intent.
5. Identify visual patterns.
6. Build content clusters.
7. Map Pins to destination pages.
8. Define measurement.
9. If account analytics are available, compare current winners against the planned cluster before expanding production.

## Opportunity Map

For each opportunity capture:

| Cluster | Intent | Seasonality | Evidence | Visual pattern | Destination | Priority |
| --- | --- | --- | --- | --- | --- | --- |

## Pin System

For each cluster create:

- Hero Pin
- Educational Pin
- Checklist Pin
- Comparison Pin
- Seasonal variation
- Search-led variation
- Visual discovery variation

## Visual-Series Rule

Maintain enough continuity to build recognition.

Possible constants:

- subject
- composition
- camera
- typography system
- layout logic
- brand mark

Possible variables:

- season
- color direction
- style
- environment
- historical period
- product
- theme

## Traffic Path

Every Pin should have a reason to exist:

**Search / discovery intent → Pin promise → Destination match**

Avoid sending users to irrelevant pages simply to generate clicks.

## Output

Return:

- Keyword map
- Content clusters
- Board / section plan when useful
- 10–30 prioritized Pin concepts
- Visual direction
- Destination mapping
- Seasonal calendar
- Measurement plan

## Measurement

Track when available:

- impressions
- saves
- outbound clicks
- CTR
- top Pins
- top boards
- search-led landing-page sessions
- conversions


## Automation Mode

For recurring Pinterest operations:

1. Let `pinterest-opportunity-radar` collect current evidence.
2. Select only supported opportunities.
3. Build the seven-variant Pin cluster.
4. Map each Pin to a relevant destination.
5. Keep publishing human-reviewed until API access, board mapping and destination checks are explicitly configured.
6. After publishing, use organic analytics to identify winners and expand only the strongest clusters.

## API Evidence

Pinterest API v5 can support organic reporting and Pin creation for approved/authenticated apps. The Trends API can return current growing keywords with WoW, MoM and YoY growth when access is available.

Never expose or commit a Pinterest access token.
