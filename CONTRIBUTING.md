# Contributing

Thanks for helping improve the **AI Social Media Toolkit**.

The project focuses on practical creator, social-media, AI, automation and digital-visibility workflows.

## Start with a real open task

You do **not** need to write a new Agent Skill to contribute.

Good first contributions currently include:

- [Verify one Agent Skills runtime end-to-end](https://github.com/alptugharun/ai-social-media-toolkit/issues/38)
- [Add one end-to-end creator workflow example](https://github.com/alptugharun/ai-social-media-toolkit/issues/40)

Both are intentionally small enough to complete without understanding the whole repository.

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

Run the repository baseline when your change touches code, skills, examples or workflows:

```bash
python -m compileall -q tools tests
python -m unittest discover -s tests -v
python tools/two_minute_demo.py > /tmp/two-minute-demo.md
```

For documentation-only changes, verify every changed relative link and make sure the instructions still match the current repository.

The pull-request template will ask for evidence, user-facing documentation impact and safety/scope checks.

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
