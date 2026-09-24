# Pinterest Automation & Visibility Playbook

Research snapshot: **2026-09-24**

This playbook defines how the repository should automate Pinterest research, trend discovery, content planning, analytics and publishing preparation without inventing trend data or depending on consumer-UI scraping.

## Official Pinterest capability baseline

Pinterest's current developer platform supports API v5, reading Pins and boards, creating image/video Pins, organic analytics, top Pin analytics, audience insights, Trends & Insights, Sandbox testing, and production access through Pinterest's app/access-tier process.

The current Trends API can return today's top trending keywords for a requested region and trend type, including week-over-week, month-over-month and year-over-year growth plus a normalized one-year weekly time series.

Current documented limits include up to 50 results for supported filter combinations, current-date trend retrieval rather than arbitrary historical snapshots, and access that may depend on Pinterest app approval.

## Automation model

### Mode A — no Pinterest credential

The daily radar can still inspect:

- Pinterest API / MCP / scheduling / analytics repositories
- open-source feature competition
- seasonal planning rules
- keyword and content hypotheses
- destination strategy

It must not invent Pinterest trend numbers.

### Mode B — Pinterest API connected

When a valid `PINTEREST_ACCESS_TOKEN` is available, the radar can additionally attempt:

- current growing-keyword retrieval
- regional trend comparisons
- growth-rate ranking
- yearly trend-shape interpretation

Secrets must never be committed to the repository.

## Strategic wedge

Generic bulk-pinning and scheduler tools already exist.

The stronger workflow is:

**Trend / intent signal → keyword cluster → visual pattern → Pin concept → destination match → publish → measure → expand winners**

## Opportunity scoring

When live trend data exists:

- 25% live trend growth
- 20% seasonal timing
- 20% search / intent fit
- 15% visual potential
- 10% destination fit
- 10% repeatability

If live trend data is unavailable, do not silently redistribute the missing 25%. Mark the score incomplete.

## Content cluster contract

For a selected opportunity generate:

1. Hero Pin
2. Educational Pin
3. Checklist Pin
4. Comparison Pin
5. Seasonal variant
6. Search-led variant
7. Visual-discovery variant

Each item needs a title, keyword intent, visual direction, destination, CTA, KPI and evidence source.

## Publishing automation

Pinterest API v5 supports creating Pins for authenticated users.

Automatic publishing should only be enabled after app access, scopes, board IDs, destination URLs, media review and approval rules are explicitly configured.

The research radar must not silently publish content.

## Safety / platform rules

Do not:

- scrape the consumer Pinterest UI as the core data source
- fake trend numbers
- copy individual Pins
- mass-repost other creators' content
- publish hundreds of low-quality variants
- use irrelevant destination links
- commit access tokens
- bypass API access tiers

## Recommended visibility architecture

**09:05 Türkiye — Pinterest Visibility Radar**

Outputs:

- one live `pinterest-radar` issue
- current evidence status
- live trend candidates when accessible
- seasonal opportunities
- tool / competitor changes
- content-cluster candidates
- destination strategy
- API-readiness status

Future authenticated layer:

**Pinterest Analytics Intelligence**

→ account performance → top Pins → winner expansion → content decay → destination optimization

Future publishing layer:

**Approved Pin Queue**

→ reviewed asset → verified board → verified destination → API create Pin → log Pin ID → measure outcome

## Official references

- https://developers.pinterest.com/docs/analytics-and-reports/analytics-overview/
- https://developers.pinterest.com/docs/analytics-and-reports/organic-reporting/
- https://developers.pinterest.com/docs/analytics-and-reports/trends/
- https://developers.pinterest.com/docs/work-with-organic-content-and-users/create-boards-and-pins/
- https://developers.pinterest.com/docs/key-concepts/access-tiers/
- https://developers.pinterest.com/docs/developer-tools/sandbox/
- https://help.pinterest.com/business/article/pinterest-trends
- https://help.pinterest.com/business/article/pinterest-analytics

## Core principle

**Automate evidence and iteration first. Automate publishing only after the evidence loop works.**
