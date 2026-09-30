# Bring your own CSV — exact inputs for the two demo tools

The two-minute demo uses **synthetic** data. These are toolkit input formats, not a promise that an unchanged Instagram/Pinterest export will work. Map your export deliberately; do not invent missing metrics.

Run commands below from the repository root with Python 3.11 (the CI baseline). Use `python3` instead of `python` if that is how your installation is named. No API key or third-party package is needed.

## Shared format rules

Use a comma-separated `.csv` with a header and at least one data row. Header names are case-sensitive and must match exactly; duplicate headers are rejected. Column order can change. Extra **named** columns are accepted but do not affect scoring. An extra unnamed cell or a truncated row is rejected.

UTF-8 and UTF-8 with BOM are supported, as are LF/CRLF line endings and properly quoted commas, quotes and multiline text. Keep `post_id` as text: `001` is not the same identifier as `1`. The tools do not rewrite identifiers or modify your input files.

Use plain numeric values such as `12000` or `82.5`, not `12K`, `12,000`, `82,5`, `82%`, `NaN` or infinity. Scientific notation accepted by Python's `float` is also accepted when finite and in range. Empty numeric cells are **not** zero. Do not use zero for a metric you could not obtain. Semicolon/tab-delimited files and locale decimal commas are not automatically converted.

Neither tool requires dates. A named date column is ignored, not validated. No file basename or fixed folder is required: pass the file path as the first argument. Keep private exports outside the Git checkout.

## Content opportunities

Tool: [`tools/signal2content_score.py`](../tools/signal2content_score.py)  
Sample: [`examples/signal2content-opportunities.csv`](../examples/signal2content-opportunities.csv)

Required header:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
```

| Field | Required value | Meaning |
| --- | --- | --- |
| `name` | Non-blank text | Your opportunity label |
| `evidence_strength` | Finite number, 0–100 | Your assessment of supporting evidence |
| `audience_fit` | Finite number, 0–100 | Fit with the intended audience |
| `freshness` | Finite number, 0–100 | Timeliness for this use case |
| `repeatability` | Finite number, 0–100 | Potential to repeat the approach |
| `production_ease` | Finite number, 0–100 | Ease of producing the content |
| `saturation` | Finite number, 0–100 | Higher means a larger saturation penalty |

These ratings are supplied by you; the scorer does not discover trends or measure audience demand. Keep the justification for each rating in your own notes.

Minimum valid synthetic example:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
AI before-after workflow,92,90,85,88,80,62
```

The score is `0.30*evidence_strength + 0.25*audience_fit + 0.20*freshness + 0.15*repeatability + 0.10*production_ease - 0.15*saturation`, clamped to 0–100. This row scores **79.00**, not a probability of success.

Copy the bundled sample to the parent folder once (existing files are not overwritten):

```bash
python -c "from pathlib import Path; Path('../opportunities.csv').open('xb').write(Path('examples/signal2content-opportunities.csv').read_bytes())"
```

Open `../opportunities.csv` in a text editor or spreadsheet, keep the header, replace sample rows with your opportunities, and save as comma-separated UTF-8 CSV. Then:

```bash
python tools/signal2content_score.py "../opportunities.csv" --validate-only
python tools/signal2content_score.py "../opportunities.csv" --top 3
```

The first command checks without ranking; the second prints `rank,name,score` to the terminal. Omitting `--top` prints all rows; positive values limit the output. No output file is created by default.

## Social posts

Tool: [`tools/outlier_score.py`](../tools/outlier_score.py)  
Sample: [`examples/social-outlier-posts.csv`](../examples/social-outlier-posts.csv)

Required header:

```csv
platform,post_id,views,likes,comments,shares,saves
```

| Field | Required value | Meaning |
| --- | --- | --- |
| `platform` | Non-blank text | Platform label; no automatic platform grouping |
| `post_id` | Non-blank text | Identifier preserved as text |
| `views` | Finite, non-negative number | Observed views |
| `likes` | Finite, non-negative number | Observed likes |
| `comments` | Finite, non-negative number | Observed comments |
| `shares` | Finite, non-negative number | Observed shares |
| `saves` | Finite, non-negative number | Observed saves |

There are no optional scoring metrics. The parser accepts finite non-negative decimal values; for actual count metrics, supply the recorded counts. **Behavior change:** malformed, missing, blank or negative values previously could silently become zero. They now cause validation failure.

Minimum syntactically valid synthetic example:

```csv
platform,post_id,views,likes,comments,shares,saves
instagram,001,100,10,2,3,4
```

One non-zero row scores 1.0 against itself; it is not a meaningful outlier study. Use comparable posts from the same creator, format and observation window. The tool pools all supplied rows; it does not stratify platforms, dates or accounts and does not deduplicate post IDs.

Copy the bundled five-post sample once, edit only the copy, then validate and rank:

```bash
python -c "from pathlib import Path; Path('../posts.csv').open('xb').write(Path('examples/social-outlier-posts.csv').read_bytes())"
python tools/outlier_score.py "../posts.csv" --validate-only
python tools/outlier_score.py "../posts.csv" --top 3
```

Output columns: `rank,platform,post_id,outlier_score,view_multiple,engagement_multiple`. Default `--top` is 10; zero/negative values retain the existing behavior of printing at most the first row. Prefer a positive number.

Each metric is divided by its dataset median. A zero median uses **1.0** as a numerical fallback; in that case a reported multiple is not a true ratio to a non-zero median. The weighted score caps each metric ratio at 10. The displayed view and engagement multiples are **not** capped. The engagement multiple is the mean of four separate metric ratios, **not** an engagement-rate ratio.

The bundled sample still ranks `reel-004` first: score **6.73**, view multiple **3.94**, engagement multiple **8.91**. This is synthetic evidence of tool behavior, not real account performance.

## Troubleshooting

| Symptom | Check | Correction |
| --- | --- | --- |
| `CSV has no header` or `no data rows` | Empty file or only a header | Add at least one valid record |
| `Missing columns` | Header spelling, case and delimiter | Copy the exact header above; export with commas |
| `duplicate column names` | Repeated header labels | Give every header one unique name |
| `row width differs` | Extra separator, unquoted comma or missing cell | Quote text correctly and match the header width |
| A numeric field fails | Empty/locale-formatted/negative/non-finite value | Supply a known number in range; do not guess missing data |
| `unexpected end of data` | Unclosed quoted field | Close the quote or re-export the CSV |
| Encoding error | UTF-16 or another text encoding | Save as UTF-8 CSV, with or without BOM |
| Copy command reports `FileExistsError` | Private copy already exists | Keep it; use another filename rather than overwrite |
| File not found | Current directory and quoted path | Run from the repository root and verify the supplied path |

Input errors return exit code **2**, print a file/error/example/contract reference to stderr, and print no ranked results. Validation success returns **0**. No network call or data upload occurs.

When reporting a failure, share a tiny synthetic reproducer and the error category, not your private CSV. For a complete production-brief example, use [Reels from an outlier](../examples/workflows/reels-from-outlier.md).
