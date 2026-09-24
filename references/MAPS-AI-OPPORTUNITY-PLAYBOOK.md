# Maps + AI Opportunity Playbook

Research snapshot: **2026-09-24**

This playbook defines how this repository should research and build Google Maps, Google Places, Google Business Profile, geospatial AI, creator-location, local-business and agency workflows.

The goal is not to build another generic map wrapper.

The goal is to build **higher-level, useful workflows on top of official map/location capabilities** while respecting platform terms, privacy, data ownership and human approval.

## Current Ecosystem Baseline

As of this research snapshot, Google itself already provides an increasingly agent-native Maps ecosystem, including:

- Google Maps Grounding Lite through a managed MCP endpoint
- official Google Maps Platform Agent Skills
- an experimental agentic UI toolkit for conversational map experiences
- Google Maps Code Assist / documentation-grounding capabilities
- Places API (New)
- Places Aggregate API
- Google Business Profile APIs

This changes the opportunity.

A generic "LLM can search Google Maps" MCP server is no longer a strong differentiator by itself.

## Competitor Baseline

Current public repositories show that basic map-agent infrastructure is already active.

Examples observed during research:

- `googlemaps/agent-skills` — official Google Maps Platform Agent Skills
- `cablate/mcp-google-map` — broad Google Maps MCP with place search, routing, area exploration and local-rank tracking
- `AgriciDaniel/codex-seo` — broader AI SEO suite with local/maps intelligence

Therefore, do not treat these as novel by themselves:

- place search
- geocoding
- directions
- local-rank grid scanning
- generic Google Maps MCP integration
- generic Claude + Maps connectivity
- generic ChatGPT + Maps connectivity

The opportunity is in **workflow intelligence, evidence, packaging and user-specific outcomes**.

## Strategic Wedges

### 1. Local Business Intelligence

Audience:

- agencies
- local businesses
- creators
- consultants
- multi-location operators

Jobs:

- understand local market density
- identify under-served categories
- inspect nearby competitors
- connect owned Business Profile performance to content strategy
- turn local search demand into content briefs
- identify creator / venue partnership opportunities
- generate review-response drafts for managed profiles
- prepare evidence-backed client reports

Preferred inputs:

- Places Aggregate API for density / counts
- Places API for live place discovery
- Google Business Profile APIs for user-owned performance and review data
- first-party business data
- open / licensed enrichment sources when persistence is required

### 2. Creator Location Scout

A creator asks:

> Find five places in this area that fit this shoot concept, verify practical constraints, build a route, and turn the stops into a Reels production plan.

Output can include:

- venue shortlist
- route
- opening-hour checks
- filming concept
- shot list
- hook ideas
- collaboration angle
- production difficulty
- human review checklist

This connects maps directly to the existing creator-operations toolkit.

### 3. Local Content Gap Engine

Combine:

- owned Business Profile search-query signals
- owned performance metrics
- review themes
- local place/category context
- creator content workflows

Then produce:

- recurring customer questions
- under-covered service topics
- local search-intent clusters
- FAQ content
- Reels / carousel / Pinterest concepts
- local landing-page briefs
- measurement plan

### 4. Sponsor Scout Local

Goal:

Help a creator identify local businesses that may fit a sponsorship or collaboration concept.

The system should produce a **shortlist for human review**, not a spam list.

Use:

- live place discovery
- creator niche / audience context
- business category
- location fit
- public website/contact availability when permitted
- explicit human review before outreach

Do not automatically send unsolicited bulk outreach.

### 5. Places Aggregate Market Gap

Use official aggregate place insights to compare:

- category density
- rating ranges
- operating status
- geography
- custom areas when supported

Useful for:

- branch-planning hypotheses
- local-service coverage
- competitive-density maps
- neighborhood comparison
- creator/agency research

Counts are signals, not automatic investment recommendations.

### 6. MapWrapped

A separate future product / repository candidate.

Concept:

Convert a user's own exported Google Maps Timeline / location-history data into a private, local-first "Wrapped" experience with shareable cards, personal travel statistics and optional AI reflection.

Why it should be separate:

- consumer-facing product
- different privacy model
- different UI / parser architecture
- strong seasonal launch potential
- should not bloat the creator-operations repository

The user's own exported data is the center of the product.

### 7. Review Anomaly Explorer

Safer framing:

Do not declare reviews "fake".

Instead, flag observable anomalies such as:

- unusual bursts
- duplicate-like wording
- rating-distribution shifts
- repeated phrases
- sudden volume changes

Output:

- anomaly evidence
- confidence
- alternative explanations
- manual review recommendation

Never accuse a person or business of fraud from heuristic signals alone.

### 8. Maps Policy Guard

Every Google Maps / Places / Business Profile architecture should be checked for:

- API vs scraping
- allowed storage / caching
- place-ID handling
- attribution
- Street View restrictions
- Google / non-Google map-content mixing
- Business Profile ownership / authorization
- EEA-specific terms when relevant
- export / bulk-download concerns

## Safe Architecture Principles

Prefer:

1. Official APIs.
2. Live / ephemeral retrieval where storage is restricted.
3. Place IDs as durable identifiers where allowed.
4. Aggregated insights for market-density questions.
5. User-owned Business Profile data for business-performance workflows.
6. Open or separately licensed datasets when persistent enrichment is needed.
7. Explicit attribution where required.
8. Human approval before external communication or write actions.

## Do Not Build

Do not design this repository around:

- scraping the consumer Google Maps UI
- bulk-downloading Google Maps business content into a permanent lead database
- silently caching restricted Maps / Places / Street View content
- automatic mass outreach
- incentivized or fabricated reviews
- claiming that a review is fake based only on a heuristic
- inferring residents' social class, wealth, ethnicity, health, crime propensity or similar sensitive traits from Street View imagery
- "aggression" or neighborhood-danger scoring based on social posts
- pretending location data can guarantee investment ROI
- copying another repository's distinctive implementation

## Product Rule

The strongest product is not:

> ChatGPT can use Google Maps.

The stronger product is:

> An agency, creator or local business can turn permitted location intelligence into a measurable decision or content workflow in a few minutes.

## Opportunity Evaluation

Score candidates using:

- Demand evidence — 25%
- Direct-supply gap — 20%
- Strategic fit with this toolkit — 20%
- Proof potential — 15%
- Compliance feasibility — 15%
- Distribution ease — 5%

Apply penalties for:

- generic wrappers
- heavy paid dependencies for basic use
- prohibited scraping
- unclear data rights
- weak proof
- excessive setup friction

Scores are prioritization heuristics, not predictions of virality.

## Preferred Build Order

1. Maps Opportunity Radar
2. Maps Policy Guard
3. Local Business Intelligence
4. Creator Location Scout mode
5. Local Content Gap mode
6. Sponsor Scout Local mode
7. Separate MapWrapped repository only after a focused product brief

## Core Principle

**Use official location intelligence to solve a sharper workflow. Do not turn Google Maps content into a scraped database.**


## Official References

Re-check these before a production release because product capabilities and terms can change:

- Google Maps Platform Agent Skills: https://developers.google.com/maps/ai/agent-skills
- Google Maps Grounding Lite MCP: https://developers.google.com/maps/architecture/grounding-with-maps-mcp
- Places Aggregate API overview: https://developers.google.com/maps/documentation/places-aggregate/overview
- Places Aggregate request parameters: https://developers.google.com/maps/documentation/places-aggregate/request-parameters
- Places Aggregate examples: https://developers.google.com/maps/documentation/places-aggregate/example-requests
- Google Business Profile Performance API: https://developers.google.com/my-business/reference/performance/rpc
- Google Business Profile reviews: https://developers.google.com/my-business/content/review-data
- Google Maps Platform Terms: https://cloud.google.com/maps-platform/terms
- Maps Service Specific Terms: https://cloud.google.com/maps-platform/terms/maps-service-terms
- Street View Static policies: https://developers.google.com/maps/documentation/streetview/policies

Important current examples from the service-specific terms include temporary caching limits for certain location values and Places Aggregate POI counts, plus special rules for Google IDs such as place IDs. Do not encode a permanent storage assumption into a product without checking the live terms.
