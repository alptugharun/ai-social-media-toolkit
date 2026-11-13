# Self-Heal Guardian: first safe result

[Türkçe](SELF-HEAL-FROM-ZERO_TR.md) · [Source](../tools/self_heal.py) · [Workflow](../.github/workflows/self-heal.yml)

## What and for whom

This local helper classifies failed GitHub Actions logs and produces a machine-readable diagnosis plus a Markdown incident summary. It helps maintainers decide whether **bounded** retry is safe. It is not an automatic repair, a GitHub API quota reset, a vulnerability scanner or proof that a failure will disappear. Not intended for non-maintainers to deploy on another account without reviewing workflow permissions.

**Requirements / cost:** Python 3.11+ and a repository checkout containing the helper and example. No API key, network request, paid API or GitHub write permission is needed for this example. Outputs are written only to the two paths you name.

## First action: synthetic HTTP 429

From the repository root:

```bash
python tools/self_heal.py --log examples/self-heal-429.log --workflow "GitHub Opportunity Radar" --run-id demo-429 --json-output self-heal-demo.json --markdown-output self-heal-demo.md
```

Open `self-heal-demo.json`. Expected values: `classification: "http-rate-limit"`, `retryable: false`, `probe_retry_safe: false`, and a 12-character fingerprint. `self-heal-demo.md` should describe the incident and limitations. Verify independently with:

```bash
python -m unittest tests.test_self_heal -v
```

Tests use synthetic errors, including GitHub-specific and generic HTTP 429, 403 and 503. Passing does not establish actual GitHub rate-limit recovery or real runner behavior. The historical release ZIPs are not guaranteed to contain this newer policy.

## Troubleshooting and data safety

If Python is missing, install a supported local Python interpreter; if a file cannot be found, run the command from the repository root; if an output path is unwritable, select a writable local path. `HTTP 429` means *pause and investigate*; this classifier never schedules a retry based on a reset number. A standalone 503 can remain eligible for existing bounded retry policy. A generic 403 remains non-retryable because authorization and throttling cannot safely be distinguished.

Only use synthetic or deliberately redacted logs in public issues. Real logs may contain tokens, private URLs or personal data: do not paste them publicly. The classifier extracts limited diagnostic lines, **not a comprehensive secret scrubber**. It cannot enforce GitHub rules or independently attest the runner environment. For sensitive findings follow [private reporting](../SECURITY.md); for reproducible non-sensitive errors use [GitHub issues](https://github.com/alptugharun/ai-social-media-toolkit/issues) and attach the synthetic reproduction. Delete `self-heal-demo.json` and `self-heal-demo.md` when finished.
