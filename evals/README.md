# Agent Skill Evaluation Contracts

This directory contains **static evaluation contracts**, not model-score claims.

Each contract names:

- one public Agent Skill;
- one representative user request;
- output elements that should be present;
- failure patterns that should not appear;
- a short note explaining the behavior being tested.

The contracts are useful for three jobs:

1. keeping every skill attached to a concrete user outcome;
2. giving future host/runtime tests a repeatable acceptance target;
3. preventing the repository from treating "the file exists" as proof that the skill works.

## What these files do not prove

A JSON contract does **not** prove that Claude, Codex, Gemini, Cursor, Copilot, Grok or another host executed the skill correctly.

Runtime evidence still belongs in [Runtime Verification](../docs/RUNTIME-VERIFICATION.md).

## Validation

Run:

```bash
python -m unittest tests.test_skill_evaluation_contracts -v
```

The test requires every current `skills/*/SKILL.md` directory to have exactly one contract and checks that each fixture contains explicit positive and negative acceptance criteria.

When a new skill is added, CI should fail until its evaluation contract is added too.
