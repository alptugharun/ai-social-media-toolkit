# Gemini Gem Blueprint

Checked against Google Gemini Apps Help on **2026-09-30**.

Google's current help states that custom Gems can be created/edited in the Gemini web app, used on web/mobile, and can include instructions plus optional knowledge files.

Official references:
- https://support.google.com/gemini/answer/15146780
- https://support.google.com/gemini/answer/15235603
- https://support.google.com/gemini/answer/15236321

## Build one

1. Open Gemini on the web.
2. Open Gems and choose **New Gem**.
3. Give the Gem a narrow job-based name.
4. Paste the portable instructions.
5. Add only relevant knowledge files if needed.
6. Preview with the acceptance tests.
7. Save only after the preview matches the output contract.

## Example

**Name:** Pinterest Search Planner

**Instructions:** use the [Portable Assistant Blueprint](PORTABLE-ASSISTANT-BLUEPRINT.md) with the Pinterest 7-Pin workflow.

**First request:**

```text
Build a 7-Pin cluster from these verified keywords.
Label any unsupported trend claim as a hypothesis.
```

## Verification

Preview is not the same as saved configuration. Confirm the Gem is saved and visible before calling setup complete.
