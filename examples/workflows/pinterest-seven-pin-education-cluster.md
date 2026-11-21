# From a synthetic Pinterest opportunity to seven useful Pins

**Job:** help a creator educator turn one candidate topic into a coherent seven-Pin teaching series, with a matching public guide as the destination. This is a **planning example**, not evidence of Pinterest trends, user demand, published Pins or traffic.

**Audience:** creators learning to plan Pinterest visual-search content. **Deliverable:** a seven-row production brief, not automatically generated artwork or published content. **Requirements:** Python 3.11, this repository, and a text editor. No Pinterest account, AI model, API token or publishing permission is needed.

## Input: a reproducible *synthetic* prioritization

Use the repository's [`examples/signal2content-opportunities.csv`](../signal2content-opportunities.csv). Its four rows contain **illustrative human-assigned ratings**, not observed trend volume or creator performance. The [content-opportunity CSV contract](../../docs/CSV-INPUTS.md#content-opportunities) specifies each field and its 0–100 range.

From the repository root, run:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --validate-only
python tools/signal2content_score.py examples/signal2content-opportunities.csv --top 3
```

**Observed with the repository's scorer and bundled fixture (offline):**

```text
VALID examples/signal2content-opportunities.csv: 4 data rows
```

```csv
rank,name,score
1,Pinterest seasonal visual series,83.05
2,AI before-after workflow,79.00
3,Creator teardown carousel,74.10
```

The `83.05` score is a **relative planning heuristic based on the supplied ratings**, not a search-volume estimate, click probability, or forecast. It only tells us which row to inspect first *within this sample*. Before actual seasonal production, a human must check current audience and Pinterest evidence using the [`pinterest-growth-engine` skill](../../skills/pinterest-growth-engine/SKILL.md) or the [Pinterest starter kit](../../downloads/PINTEREST-GROWTH-STARTER-KIT.md); that external research is **not performed here**.

## Editorial scenario and destination gate

**Hypothetical choice:** interpret the top row as an educational series on *planning seasonal Pinterest visuals*, rather than claiming a particular seasonal aesthetic is trending. This is an editorial decision, **not a tool-generated conclusion**. The destination is the real, public [Pinterest Growth Starter Kit](../../downloads/PINTEREST-GROWTH-STARTER-KIT.md), which covers evidence, intent, seven roles, visual consistency, destination matching and measurement.

All search phrases below are **candidate queries to validate**, not Pinterest keyword results. Each Pin must deliver the stated lesson *in the Pin itself*, with the linked guide offering the full workflow. Do not use the series to promote unrelated products or link to a generic sales page.

**Destination URL for all seven concepts:** `https://github.com/alptugharun/ai-social-media-toolkit/blob/main/downloads/PINTEREST-GROWTH-STARTER-KIT.md` (a documented guide; not a tracked landing-page campaign).

| Pin role | Proposed query / intent (unverified) | Pin promise and distinct original visual | CTA | Primary KPI |
| --- | --- | --- | --- | --- |
| Hero | "Pinterest content series plan" / overview | Explain the seven distinct Pin jobs in a seven-panel editorial map; one panel per role | Read the seven-role walkthrough | Outbound clicks |
| Educational | "Pinterest keyword clusters" / learn | Show the difference between broad, problem, inspiration, seasonal and commercial intent with original example labels | See the intent-mapping steps | Saves |
| Checklist | "Pinterest Pin planning checklist" / implement | Six-item checklist: query, promise, focal point, destination, CTA, KPI | Use the full planning guide | Saves |
| Comparison | "Pinterest Pin ideas vs strategy" / decide | Side-by-side: seven near-identical photos versus seven differentiated jobs, **without** claiming either performs better | Compare the seven roles | Outbound clicks |
| Seasonal | "seasonal Pinterest content planning" / timing | A calendar-style *planning* board: evidence check, preparation, publication review; no invented trend dates | Review the seasonality step | Saves |
| Search-led | "how to plan a Pinterest Pin cluster" / how-to | Simple flowchart: evidence → intent → Pin role → matched guide → measurement | Follow the workflow | Outbound clicks |
| Visual discovery | "Pinterest visual content framework" / explore | A distinct original storyboard combining the same seven jobs with a consistent composition system | Explore the complete starter kit | Saves |

**Production specification (editorial proposal):** seven original vertical **2:3** visuals, a repeatable type hierarchy, consistent margins and a single recognizable visual language. Avoid reusing an identical image with seven captions. Write concise, useful text or diagrams *inside* a Pin if the educational promise needs it; do not sacrifice comprehension to enforce text-free art. Use original/cleared assets and check visual legibility before export. No artwork was generated or uploaded by this example.

## QA gate

- **PASS — local, offline prioritization:** the fixture validates and the ranked top three above match the scorer's output.
- **PASS — editorial destination fit:** every Pin teaches a section actually covered by the linked starter kit. The links reference repository files verified to exist at preparation time.
- **HOLD — live distribution:** no Pinterest search evidence, target audience validation, landing-page analytics, rendered images, permission grant or published Pins were tested. Verify each candidate query, destination response, accessibility and image rights before scheduling; do not infer a platform trend from the `83.05` score.

## Common mistake and correction

**Mistake:** describe `83.05` as "83% likelihood of going viral," mass-produce seven cosmetic variants, then send them to an unrelated homepage. **Correction:** treat the number as an internal prioritization score, assign a different teaching job to each Pin, and match the destination to the actual promise. The [starter kit's destination-match rule](../../downloads/PINTEREST-GROWTH-STARTER-KIT.md#5-destination-match-gate) explains the boundary.

## One measurable next step

After a real human review and a permitted publication workflow, publish a *small*, deliberately spaced subset first. At one consistent observation window, record each Pin's **impressions, saves and outbound clicks**, using Pinterest's reported figures. For Pins with nonzero impressions, calculate saves per 1,000 impressions; record the same metric for the remaining Pins before expanding a winner. No result, conversion, causal effect or revenue is asserted here.

For a new contribution based on **independent** execution, follow [Contributing](../../CONTRIBUTING.md#submit-through-a-fork) and [issue #40](https://github.com/alptugharun/ai-social-media-toolkit/issues/40). This maintainer-supplied example does **not** count as independent runtime verification, and does not close that request.
