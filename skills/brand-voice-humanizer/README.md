# Brand Voice Humanizer + Rewrite Fact Guard

[Türkçe](README_TR.md) · [Skill instructions](SKILL.md)

**Your rewrite sounds better. Did the price or deadline change?**

This existing skill has two parts: writing guidance an agent can follow, and an optional small Python program that compares two drafts locally. The program is a **lexical review aid**, not an AI detector or factual-accuracy certificate.

## Which part do I need?

Use the skill to improve the draft's voice. Use Audit mode to get concrete comments without a rewrite. Use Rewrite Fact Guard when you have both the original and edited text and want to flag changed number tokens, URLs or exact phrases you selected.

The helper does not rewrite, call an AI model, publish, connect to a social account or create an assistant. You do not need an API key or paid model to run it. Running the instruction skill inside an AI host is a separate operation and may involve that host's normal costs and data policies.

## Start without a terminal

1. Open [SKILL.md](SKILL.md) and use its process in your authorized AI environment.
2. Supply a draft and name the mode: Audit, Light, Editorial, Spoken or Brand-Locked.
3. Mark names, prices, deadlines and qualifiers that must remain unchanged.
4. Ask for the edited draft and material changes, or only findings in Audit mode.
5. Read both versions before publishing. No content is automatically posted.

First request: “Light edit this caption. Keep my Turkish phrasing and humor. Do not change the price, deadline or the phrase ‘garanti değildir’. Tell me what changed.”

A voice improvement is subjective; compare against your own approved examples. The helper below verifies only a narrower mechanical property.

## Run the local helper from zero

Download or clone the repository and open a terminal **inside the repository folder**. Confirm Python 3.10 or newer with `python --version`. No `pip install` is needed. On Windows, `py -3` can replace `python` when configured.

Try the synthetic before/after files (these prices and deadlines are not commercial offers):

```bash
python skills/brand-voice-humanizer/scripts/fact_guard.py --before skills/brand-voice-humanizer/examples/before.txt --after skills/brand-voice-humanizer/examples/after-good.txt --lock "garanti değildir"
```

Expected: `NO_TRACKED_CHANGE`, zero changed items, exit code **0**, and a limitation message. This means only that tracked tokens and the selected phrase were retained.

Now deliberately try the changed-price example:

```bash
python skills/brand-voice-humanizer/scripts/fact_guard.py --before skills/brand-voice-humanizer/examples/before.txt --after skills/brand-voice-humanizer/examples/after-review.txt --lock "garanti değildir" --format json --show-values
```

Expected: `REVIEW_REQUIRED`, **7 findings**, exit code **1**. Removed and added tokens are separate findings: two price entries, two duration entries, two URLs, and the missing protected phrase. This command displays values only because the bundled example is synthetic.

On PowerShell, check the result immediately with `$LASTEXITCODE`. Exit **2** is an input/configuration problem; **1** means review is required. In an agent workflow, do not respond to exit 1 by repeatedly running the command or automatically approving the rewrite.

## Use your own drafts

Save the original and edited drafts as separate UTF-8 `.txt` files. Replace the two paths in the command. Add repeated `--lock` options for exact names, quotes, disclaimers or other important phrases that already occur in the original. A misspelled or absent lock stops with an error instead of silently passing.

The defaults omit literal values from findings. Do not use `--show-values` with private drafts that might be captured in CI logs. Never put credentials in drafts or `--lock` arguments; shell histories can record arguments. Source documents stay unchanged. Any shell redirection you add yourself, such as `> report.json`, is a separate file write by your shell.

## What it checks, and what it misses

| Check | Boundary |
|---|---|
| Number-like tokens | Detects examples such as prices, ISO dates, simple versions and percentages. It is not a universal numeric parser. |
| Common units | A small explicit set, including TL/USD/EUR, kg/mg, gün and common time units. Written-out numbers and many inflected units are not understood. |
| URLs | Compares literal URLs after removing common trailing punctuation; does not fetch a link or verify its destination. |
| Protected phrases | Exact, case-sensitive occurrence counts after Unicode NFC normalization. It does not understand synonyms or entailment. |

`1,500` and `1.500` are deliberately not assumed equivalent. A human can clear a harmless formatting change. Conversely, “A: 25, B: 50” rewritten as “A: 50, B: 25” retains the token bag and can escape detection. Lock complete statements when their association matters, and still review the meaning.

Unchanged numbers do not prove true numbers. “May help” becoming “will help” is not detected unless the relevant text is protected. No AI-authorship probability, trust grade, legal assessment or publication guarantee is produced.

## Troubleshooting and privacy

- **INPUT_ERROR / missing lock:** copy the exact phrase from the original; do not weaken a real requirement just to get a zero exit code.
- **UTF-8 error:** save the text as UTF-8. A UTF-8 BOM is accepted.
- **Too large:** each input is capped at 256 KiB; compare coherent sections, keeping associations intact.
- **Missing file:** check the working folder and relative path. Directories and symlinks are not accepted.
- **No numbers or locks:** there may be nothing meaningful for the mechanical check to track. Read the full drafts.

The program uses the Python standard library, reads only the two specified regular text files, and has no network or model dependency. This does not make the surrounding operating system, agent host or document storage a sandbox.

## Verify or report a problem

From the repository root:

```bash
python -m unittest discover -s tests -p test_rewrite_fact_guard.py -v
```

These are synthetic lexical, validation and CLI regression tests, including intentionally documented blind spots. They are not an evaluation of an AI model's editing quality.

Report a public-safe reproduction through [repository issues](https://github.com/alptugharun/ai-social-media-toolkit/issues/new/choose). Do not attach private customer drafts or secrets. Report sensitive security concerns privately through the repository security policy.
