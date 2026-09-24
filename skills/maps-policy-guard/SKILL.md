---
name: maps-policy-guard
description: Reviews Google Maps, Places, Street View and Business Profile workflow designs for scraping, storage, caching, attribution, ownership and data-use risks. Use before implementing or publishing a map-data automation, lead workflow, local-intelligence tool or Maps-based Agent Skill.
license: MIT
metadata:
  version: 0.1.0
  author: Alptuğ Harun
---

# Maps Policy Guard

Review a Maps-related architecture before it becomes a product or automation.

This is a technical/product compliance checklist, not legal advice.

## Required Reference

Read:

- `references/EVIDENCE-POLICY.md`
- `references/MAPS-AI-OPPORTUNITY-PLAYBOOK.md`

Use fresh official Google documentation for time-sensitive policy claims.

## Inputs

Ask for or infer:

- data source
- API / endpoint
- user owns the data?
- retrieval frequency
- storage duration
- fields stored
- export format
- map renderer
- external enrichment source
- write actions
- outreach behavior
- target geography
- whether EEA-specific terms may apply

## Checks

### 1. Retrieval Method

Classify:

- official API
- user export
- first-party business data
- open / licensed third-party data
- browser scraping
- undocumented endpoint

Browser scraping of Google Maps consumer surfaces should trigger redesign.

### 2. Persistence

Identify whether the design stores:

- place IDs
- coordinates
- business names
- addresses
- reviews
- photos
- Street View imagery
- search results
- aggregate counts

Do not assume every field may be stored indefinitely.

Prefer ephemeral retrieval when rights are unclear or restricted.

### 3. Bulk Export / Lead Database

Check whether the design effectively creates a reusable database from Google Maps content.

If yes, return **REDESIGN** unless the data source and terms clearly permit it.

Use official aggregate insights, place IDs, first-party records or separately licensed datasets instead.

### 4. Attribution / Display

Check:

- required Google attribution
- display rules
- whether content is being shown on a non-Google map
- whether mixed-source presentation is allowed for the intended API

### 5. Street View

Check:

- prefetching
- indexing
- caching
- dataset creation
- computer-vision extraction
- retention

Street View analysis requires especially careful current-policy verification.

### 6. Business Profile

For managed Business Profile data verify:

- user/business authorization
- verified/managed location
- OAuth / approved API access when required
- write action permissions
- human approval for replies / edits when appropriate

### 7. Reviews

Do not:

- generate fake reviews
- incentivize prohibited review behavior
- label a review fake without evidence
- mass-post replies without an approval/control layer

### 8. Sensitive Inference

Return **REDESIGN** for concepts that infer sensitive or high-impact traits from location imagery or neighborhood proxies, including socioeconomic class or criminal propensity.

### 9. EEA / Regional Terms

If the deployment or billing scope may invoke region-specific terms, require a fresh check of the relevant service terms before launch.

## Output

# Maps Policy Guard

## Verdict
Choose one:

- **PASS** — architecture appears compatible with the checked constraints
- **REVIEW** — implementation can proceed only after specified policy/docs checks
- **REDESIGN** — core data flow should be changed

## Data Flow
| Stage | Source | Data | Stored? | Risk |
| --- | --- | --- | --- | --- |

## Findings
For each finding:

- observed design
- relevant current policy/source
- risk
- safer alternative

## Safer Architecture

Prefer when appropriate:

- official Places / Routes APIs
- Places Aggregate API for density questions
- place IDs as durable references when allowed
- user-owned Business Profile data
- user-provided exports
- open / independently licensed persistent datasets
- human approval before external write actions

## Release Gate
- [ ] Sources are current
- [ ] API terms checked
- [ ] storage rules checked
- [ ] attribution checked
- [ ] ownership / auth checked
- [ ] region-specific rules checked
- [ ] no prohibited scraping
- [ ] no hidden mass outreach

## Core Principle

**If the product only works by quietly turning Google Maps into a private database, redesign the product.**
