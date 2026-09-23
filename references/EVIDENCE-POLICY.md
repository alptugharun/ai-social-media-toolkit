# Evidence Policy

Research-oriented skills in this repository should separate **evidence**, **inference**, and **recommendation**.

## Rules

1. Never call something a trend from a single example unless the user explicitly asks for examples only.
2. Preserve source URLs when research is based on public web content.
3. Record dates for time-sensitive evidence.
4. Preserve raw metrics before calculating any derived score.
5. Use medians for creator/account baselines when outliers could distort averages.
6. Do not merge incomparable platform metrics into one baseline.
7. If sample size is small, lower confidence.
8. Do not invent quotes, comments, views, saves, shares, demographics, or conversion results.
9. If the agent cannot access the required source, say what is missing and continue only with supported evidence.
10. Distinguish:
   - **Observed:** directly supported by source data.
   - **Inferred:** reasonable interpretation of observed evidence.
   - **Recommended:** proposed action or experiment.

## Confidence Labels

**High**  
Repeated evidence across multiple relevant sources or a sufficiently large, consistent dataset.

**Medium**  
Useful directional evidence, but limited by sample size, platform coverage, or recency.

**Low**  
Sparse evidence, indirect signals, or incomplete access.

## Research Output Minimum

For each important trend, outlier, or competitor claim include when available:

- Source
- URL
- Date
- Platform
- Metric / signal
- Why it matters
- Confidence

## Heuristic Scores

Any score created by the toolkit is a decision aid, not a scientific truth.

If a skill uses a custom score, it must explain the components and avoid pretending the weighting is universally validated.
