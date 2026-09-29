# Two-Minute Demo — Expected Output Snapshot

> This snapshot is generated from the repository's **synthetic example data**. It is included so visitors can inspect the proof before running anything.

## Content opportunity ranking

| Rank | Opportunity | Score |
| ---: | --- | ---: |
| 1 | Pinterest seasonal visual series | **83.05** |
| 2 | AI before-after workflow | **79.00** |
| 3 | Creator teardown carousel | **74.10** |

**Decision:** review `Pinterest seasonal visual series` first. The score is a transparent prioritization heuristic, not a virality prediction.

## Social outlier ranking

| Rank | Platform | Post | Outlier score | Views vs median | Engagement vs median |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | instagram | reel-004 | **6.73** | 3.94× | 8.91× |
| 2 | instagram | reel-002 | **1.11** | 1.10× | 1.11× |
| 3 | instagram | reel-005 | **1.00** | 1.00× | 1.00× |

**Decision:** inspect `reel-004` first. It reached **3.94×** the supplied dataset's median views.

## Why this matters

The useful result is not “AI generated content.” The useful result is a narrower decision:

- what deserves production attention;
- what deserves qualitative performance analysis;
- what should be tested next.

## Verify it yourself

```bash
python tools/two_minute_demo.py
```

If the scoring logic or example data changes intentionally, update this snapshot in the same pull request and explain why.
