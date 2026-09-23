# Tools

Small, inspectable utilities that support the AI Social Media Toolkit.

## Signal to Content Opportunity Scorer

Input:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
```

Run:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv
```

Return only the top two:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --top 2
```

The scorer is deliberately simple and dependency-free.

It is a prioritization heuristic, not a virality prediction model.
