# Tools

Small, inspectable utilities that support the AI Social Media Toolkit.

## Choose a task

| Task | First-use guide | What the result means |
| --- | --- | --- |
| Check a rewrite for changed prices, deadlines, URLs or protected phrases | [Rewrite Fact Guard — English](../skills/brand-voice-humanizer/README.md) · [Türkçe](../skills/brand-voice-humanizer/README_TR.md) | A lexical review report, not a truth or AI-authorship certificate |
| Check local setup without a paid model | [Start Here](../START-HERE.md) | A bounded offline first-run check |
| Prioritize content opportunities | [CSV input guide](../docs/CSV-INPUTS.md) | Explainable heuristic scores, not a virality prediction |

For setup, exact commands, inputs, outputs and failure notes for the broader toolkit, open **[How to Use Everything](../docs/HOW-TO-USE-EVERYTHING.md)**. Do not assume every source feature is present in every older release.

## Rewrite Fact Guard: which download includes it?

The helper was added to source after **v0.3.0-alpha.1**. That historical release's ZIPs do not include it. Use the current repository source, or a later release whose notes explicitly include the helper. The [English](../skills/brand-voice-humanizer/README.md) and [Turkish](../skills/brand-voice-humanizer/README_TR.md) guides include both a preserved example and a deliberately changed example, expected exit codes and troubleshooting. No account or API key is needed for the Python comparison.

## Signal to Content Opportunity Scorer

Input:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
```

Run from the repository root:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv
```

Return only the top two:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --top 2
```

The scorer is deliberately simple and dependency-free.

It is a prioritization heuristic, not a virality prediction model.
