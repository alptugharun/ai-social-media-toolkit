# From a synthetic Reel outlier to a production brief

**Result:** run the existing analyzer, inspect its output, and build one original Reel treatment without mistaking sample metrics for a success guarantee.

For creators reviewing their own short-form content. Requirements: Python 3.11 and this repository. No API, AI account or external publishing connection is needed. Numerical output below is from the actual analyzer; the script/shot plan is an original editorial example, not output claimed from a live Agent Skills host.

## Input and context

Use [`examples/social-outlier-posts.csv`](../social-outlier-posts.csv). It contains five synthetic Instagram posts. The [social-post CSV contract](../../docs/CSV-INPUTS.md#social-posts) defines the seven columns. Do not insert private analytics into this public fixture.

Additional **synthetic editorial context** for this example: the creator teaches AI-assisted writing. We choose to test a before/after explanation of source-based summaries. The CSV contains no transcript or hook data, so it cannot establish why a post performed differently.

## Run and inspect

From the repository root:

```bash
python tools/outlier_score.py examples/social-outlier-posts.csv --validate-only
python tools/outlier_score.py examples/social-outlier-posts.csv --top 3
```

Validation reports five data rows. Actual ranked output:

```csv
rank,platform,post_id,outlier_score,view_multiple,engagement_multiple
1,instagram,reel-004,6.73,3.94,8.91
2,instagram,reel-002,1.11,1.1,1.11
3,instagram,reel-005,1.0,1.0,1.0
```

The sample median views are 13,200. `reel-004` has 52,000 / 13,200 = 3.94× median views (rounded). Its composite score is **6.73**, not 6.73% and not a probability of going viral. Its **8.91** engagement multiple is not an engagement-rate measure.

**Decision:** inspect `reel-004` first. Metrics alone do not tell us which hook, edit or topic caused the difference. In a real review, inspect your own post before selecting a reusable mechanism.

## Original production treatment

The editorial hypothesis is that showing a weak brief beside an evidence-aware brief may teach the process more clearly. This hypothesis has not been performance-tested.

**Audience:** Turkish-speaking creators using AI for writing.  
**Objective:** help viewers distinguish supported statements from guesses.  
**Format:** one 9:16 Reel, planned for roughly 30–35 seconds. The duration is a production target, not a recorded timing result.  
**CTA:** save the three-question checklist.

### Spoken script

> Yapay zekâya aynı konuyu veriyorsun, ama her seferinde başka bir cevap geliyor. Ben önce komutu değil, verdiğim bilgiyi düzenliyorum. Konuyu yazıyorum, kullanacağı kaynakları ekliyorum ve istediğim çıktıyı söylüyorum. Sonra üç soruyla kontrol ediyorum: Bu bilgi hangi kaynağa dayanıyor? Neresi yorum? Neyi henüz bilmiyoruz? Ekranda önce dağınık notları, sonra bu üç soruyla düzenlenmiş özeti gösteriyorum. Böylece eksikleri görebiliyor, son kararı kendim verebiliyorum. Bir sonraki denemende bu üç soruyu kaydet.

### Shot plan

| Planned time | Picture | Purpose |
| --- | --- | --- |
| 0–4 s | Two visibly different drafts from the same synthetic brief | Introduce the inconsistency |
| 4–12 s | Highlight topic, supplied sources and output format | Show the setup, not a magic prompt |
| 12–23 s | Reveal the three checking questions one at a time | Give the viewer a repeatable check |
| 23–30 s | Synthetic before/after notes; label unsupported points | Show what changed |
| 30–35 s | Saveable three-question end card | One clear CTA |

Use made-up source notes for the demonstration or your own shareable material. Do not put fabricated statistics, private client drafts or real account tokens on screen. Adjust the edit after reading the script aloud.

## QA decision

**PASS — offline analysis and documented production brief:** commands run, numerical output matches the fixture, a single creator lane is used, and editorial assumptions are labelled.

**HOLD — publication:** no finished video, recorded duration, rights check or audience test is claimed. Review these before posting. No live Agent Skills runtime was invoked to produce this example; this does not satisfy #38.

## Common mistake

Calling **6.73** an engagement rate, claiming the “before/after hook caused 52,000 views,” or expecting the next Reel to reproduce the synthetic result. None follows from the CSV. The analyzer chooses what to inspect; an editorial review still chooses what to test.

## Next measurable step

Produce one original Reel, record its actual duration, and evaluate it after a consistent observation window against comparable posts from the same account. Record views and saves; compute saves per 1,000 views only when views are non-zero. Treat the outcome as one observation, not causal proof. No real outcome has been collected here.

## Reproduce or contribute

Run the two commands, compare the CSV block, then adapt the **editorial** section to a different public-safe scenario. Follow [Contributing](../../CONTRIBUTING.md#submit-through-a-fork). This is a maintainer-provided example; independent reproduction or another scoped example is still welcome in [#40](https://github.com/alptugharun/ai-social-media-toolkit/issues/40).
