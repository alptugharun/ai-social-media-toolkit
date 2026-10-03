# Release Gate — v0.1 Alpha

A release is a distribution event, not a version-number decoration.

## Required before tagging

- [ ] Validate Agent Skills is green on the release commit.
- [x] `python tools/two_minute_demo.py` completes successfully in CI.
- [x] README links to the runnable demo.
- [ ] START-HERE gives a non-developer and an Agent Skills path.
- [ ] HOW-TO-USE-EVERYTHING reflects the public surface.
- [x] Known limitations are explicit.
- [ ] CHANGELOG moves shipped items from Unreleased into the release section.
- [x] No fabricated install, user, revenue, trend or performance claims.
- [x] No secrets or private client/account data.
- [x] Release notes explain install, first result, major capabilities and limitations.

## Proposed first tag

`v0.1.0-alpha.1`

Use a prerelease while the toolkit is still validating external installation and repeat use.

## Release-note structure

### What this is

One sentence describing the creator-operations job.

### Try it in two minutes

    git clone https://github.com/alptugharun/ai-social-media-toolkit.git
    cd ai-social-media-toolkit
    python tools/two_minute_demo.py

### Install Agent Skills

    npx skills add alptugharun/ai-social-media-toolkit

### What is included

- 18 Agent Skills
- runnable creator decision tools
- approval-gated GitHub automation
- free creator starter materials
- complete human usage field manual

### Known limitations

- alpha project;
- runtime behavior can differ by Agent Skills host;
- live platform data requires valid official access where documented;
- demo data is synthetic;
- no promise of reach, virality or revenue.

### Feedback request

**Run one workflow and report the first point where you got confused, blocked or wanted a deeper version.**

## After release

Measure external issues, forks/contributions, repeat questions and qualified referral traffic where available. Treat stars as a weak discovery signal.

The next release should respond to evidence, not an arbitrary calendar.
