# Two-Minute Demo — See the Toolkit Make Two Decisions

> **No API key. No external package. No publishing.**

This synthetic demo ranks content opportunities and identifies posts above the supplied dataset's median. “Two-minute” describes the short walkthrough, not a measured guarantee: Python/Git installation and downloading the repository are not included.

## Run it

Prerequisites: Python 3.11 (the CI baseline); Git for the clone option. A downloaded ZIP also works after extraction. In a terminal:

```bash
git clone https://github.com/alptugharun/ai-social-media-toolkit.git
cd ai-social-media-toolkit
python tools/two_minute_demo.py
```

Use `python3` if your installation uses that command. The Markdown report prints in the terminal and does not call a provider API.

## What happens under the hood?

| Input | Tool | Result |
| --- | --- | --- |
| [signal2content-opportunities.csv](signal2content-opportunities.csv) | [signal2content_score.py](../tools/signal2content_score.py) | Ranked opportunities |
| [social-outlier-posts.csv](social-outlier-posts.csv) | [outlier_score.py](../tools/outlier_score.py) | Ranked performance outliers |

The current sample chooses **Pinterest seasonal visual series** at **83.05** and ranks **reel-004** first at **6.73**, with **3.94×** the sample median views. Inspect the [expected numeric snapshot](TWO-MINUTE-DEMO-OUTPUT.md) before running anything.

## Try your own data

The report now prints the exact sample, required header, private-copy command, validation command and direct input-contract link **after each proof**.

Use [CSV inputs](../docs/CSV-INPUTS.md) for the authoritative requirements:

- [Content opportunities](../docs/CSV-INPUTS.md#content-opportunities): six supplied 0–100 ratings and an opportunity name.
- [Social posts](../docs/CSV-INPUTS.md#social-posts): platform, post identifier and five observed metrics.

Keep your copy outside the repository. Do not replace or commit the public fixtures with private analytics. These tools do not automatically convert native platform exports or infer missing values.

Check first, then rank:

```bash
python tools/signal2content_score.py "../opportunities.csv" --validate-only
python tools/signal2content_score.py "../opportunities.csv" --top 3
python tools/outlier_score.py "../posts.csv" --validate-only
python tools/outlier_score.py "../posts.csv" --top 3
```

Create those copies using the report's commands before running this block. Input errors identify the file, offending field/record when applicable, and the contract to consult; no ranked output is printed on failure.

## What this demo does not prove

Sample results do not predict virality, revenue or platform algorithms. They are not Alptuğ Harun's real analytics. Local tool execution also does not prove that a skill was discovered or executed by Codex, Claude or another host.

## Next

[Reels from an outlier: complete example](workflows/reels-from-outlier.md) · [CSV troubleshooting](../docs/CSV-INPUTS.md#troubleshooting) · [Complete field manual](../docs/HOW-TO-USE-EVERYTHING.md) · [Contribute through a fork](../CONTRIBUTING.md#submit-through-a-fork)
