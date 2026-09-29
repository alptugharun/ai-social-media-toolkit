# Two-Minute Demo — See the Toolkit Make Two Decisions

> **No API key. No external package. No publishing. One command.**

This demo answers two practical creator-operations questions with synthetic repository data:

1. **Which content opportunity should I review first?**
2. **Which social post actually outperformed the supplied baseline?**

## Run it

Clone the repository, enter the folder, then run:

    python tools/two_minute_demo.py

Save the Markdown report if you want:

    python tools/two_minute_demo.py > demo-report.md

## What happens under the hood?

    examples/signal2content-opportunities.csv
            ↓
    tools/signal2content_score.py
            ↓
    ranked content opportunities

    examples/social-outlier-posts.csv
            ↓
    tools/outlier_score.py
            ↓
    ranked social-performance outliers

The demo combines both outputs into one proof report.

## Expected output snapshot

Want to see the current synthetic result before running it? Open [TWO-MINUTE-DEMO-OUTPUT.md](TWO-MINUTE-DEMO-OUTPUT.md).

## What should you inspect?

- the input CSVs;
- the scoring code;
- the ranked output;
- the decision notes;
- the limitations.

## This demo does not prove

- future virality;
- future revenue;
- platform algorithm behavior;
- Alptuğ Harun’s real account performance.

The bundled data is synthetic demonstration data.

## Try your own data

Content opportunity columns:

    name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation

Social post columns:

    platform,post_id,views,likes,comments,shares,saves

Then run the underlying tools directly.

## Next

- [Complete field manual](../docs/HOW-TO-USE-EVERYTHING.md)
- [Creator Materials Hub](../downloads/README.md)
- [Agent Skills](../skills/README.md)
- [Tools](../tools/README.md)
