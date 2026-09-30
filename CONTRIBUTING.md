# Contributing

Thanks for helping improve the **AI Social Media Toolkit**.

The project focuses on practical creator, social-media, AI, automation and digital-visibility workflows.

## Start with a real open task

You do **not** need to write a new Agent Skill to contribute.

Choose a task whose prerequisites you already meet:

- [Verify one Agent Skills runtime end-to-end](https://github.com/alptugharun/ai-social-media-toolkit/issues/38)
- [Add one end-to-end creator workflow example](https://github.com/alptugharun/ai-social-media-toolkit/issues/40)

**#40 can be a Markdown-only contribution. #38 needs access to an actual agent host** and is not a no-account beginner task. A local Python test is not host verification. Use the [runtime test and evidence template](docs/RUNTIME-VERIFICATION.md).

For #40, add one original, public-safe file under `examples/workflows/`, for example `your-workflow.md`. Include the input, exact steps, expected output, QA decision, common mistake and measurable next step. The [maintainer-provided Reels example](examples/workflows/reels-from-outlier.md) demonstrates the format; it does not replace an independent reproduction.

A short issue comment is helpful for coordinating work, not a permanent reservation. For a small, in-scope fix you may submit a focused PR without waiting for assignment. Check existing comments and PRs first. Discuss larger changes before starting. If you stop, say what is incomplete and release the task.

## Submit through a fork

**You do not need write access to `alptugharun/ai-social-media-toolkit`.** Make changes in your own fork, then propose them to this repository's `main` branch. A missing write path in an AI tool does not establish that upstream contributions are disabled.

### Browser-only documentation route

1. Sign in to GitHub, open this repository and select **Fork**. Create the fork in your own account.
2. In **your fork**, create a branch named `docs/creator-example` using the branch selector.
3. Edit a specific document, or use **Add file → Create new file** for `examples/workflows/your-workflow.md`.
4. Preview the Markdown and check every referenced file. Commit to your branch, not upstream.
5. Choose **Contribute → Open pull request**, or **compare across forks** if needed.
6. Check **base repository** is `alptugharun/ai-social-media-toolkit`, **base** is `main`, **head repository** is your fork and **compare** is `docs/creator-example`.
7. Describe the change, reference the issue and state which checks you ran. If local tests were unavailable, say so; do not claim a pass. Submit as draft while evidence is incomplete.

### Local Git route

First create your fork in GitHub. Replace `YOUR-USERNAME` below with your own GitHub login:

```bash
git clone https://github.com/YOUR-USERNAME/ai-social-media-toolkit.git
cd ai-social-media-toolkit
git switch -c docs/creator-example
```

Make your focused change. Run the checks below. Inspect what will be committed:

```bash
git status --short
git diff
```

For the example task, stage only the file you actually created (replace the sample filename):

```bash
git add examples/workflows/your-workflow.md
git diff --cached
git commit -m "docs: add a reproducible creator workflow example"
git push -u origin docs/creator-example
```

`origin` must point to **your fork**. Open GitHub's offered PR URL and check the base/head settings above. Do not use `git add .` when private exports, local credentials or generated skill copies might be present. Never paste a token into an issue or command example.

### When the route is blocked

Report **which step** is blocked: fork creation, local editing, push to your fork, or opening the PR. Include a short sanitized error and whether you used GitHub's website, Git or an agent connector. Do not post private filesystem paths or account secrets.

You may share a small public-safe proposed diff or Markdown example in the issue for review when a PR is unavailable. Label it **proposal, not applied**. Do not request administrator access or widen token permissions merely to bypass an environment restriction. A maintainer review or CI approval may still be needed for a first-time contributor's PR; do not work around that gate.

## Good Contributions

Useful contributions include:

- real runtime compatibility evidence
- stronger evidence or verification logic
- filled end-to-end creator examples
- tested automation recipes
- better templates
- accessibility improvements
- documentation fixes
- reproducible bug reports
- focused improvements to an existing Agent Skill

A **new Agent Skill is usually not the first choice**. Show that an existing workflow cannot solve the job cleanly before increasing the skill count.

## Skill Requirements

A new skill should:

1. Solve one clear job.
2. Include a `SKILL.md`.
3. Start with YAML frontmatter.
4. Include `name`, `description`, and `license`.
5. Produce an actionable output.
6. Separate evidence from inference when research is involved.
7. Avoid fabricated metrics or unsupported claims.
8. Avoid copying another project's unique wording or branding.
9. Preserve required third-party notices when code is reused under an open-source license.
10. Be understandable without proprietary internal context.

## Research Skills

Use [references/EVIDENCE-POLICY.md](references/EVIDENCE-POLICY.md).

Research outputs should preserve source URLs when possible and label confidence honestly.

## Before opening a pull request

With Python 3.11 (the CI baseline), run these from the repository root when your change touches code, skills, examples or workflows:

```bash
python -m compileall -q tools tests
python -m unittest discover -s tests -v
python tools/two_minute_demo.py
```

For documentation-only changes, verify every changed relative link and make sure the instructions still match the current repository.

For CSV changes, also check the examples before ranking:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --validate-only
python tools/outlier_score.py examples/social-outlier-posts.csv --validate-only
```

The [CSV input contract](docs/CSV-INPUTS.md) is the user-facing reference. Runtime reports use [this template](docs/RUNTIME-VERIFICATION-TEMPLATE.md); an unrun or blocked check is not PASS.

The pull-request template asks for evidence, documentation impact and safety/scope checks. Keep `#38` open until real host evidence meets its acceptance criteria; onboarding docs alone do not complete it. Avoid `Closes #...` until the linked issue's full scope is actually complete.

## Pull Requests

Keep pull requests focused.

Explain:

- what changed
- why it is useful
- how it was tested
- any external dependencies
- any third-party code or license obligations

## Licensing

Licensing is determined by the directory you contribute to:

- `skills/` — **MIT License** under [skills/LICENSE](skills/LICENSE).
- `tools/` — **MIT License** under [tools/LICENSE](tools/LICENSE).
- Other original documentation, frameworks, templates and repository material — **Creative Commons Attribution-NonCommercial 4.0 International** under the root [LICENSE.md](LICENSE.md), unless a file states otherwise.

By contributing to a directory, you agree that your contribution may be distributed under the license applicable to that directory. Preserve required copyright, attribution and license notices for any permitted third-party material you include.
