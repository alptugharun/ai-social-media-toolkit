# API Bot & Assistant Starters

**Single-turn developer starters for provider APIs. These are not autonomous, always-on bots.**

## Purpose

Use this lane to understand and test a small provider request without pulling in a framework. The starter builds one request, optionally prints a redacted dry run, sends a single live call only when you supply credentials, parses the text response and exits.

Included starter: `tools/multi_provider_assistant.py`.

## Prerequisites

- Python 3.11 is the CI-tested version.
- No third-party Python package is required.
- The `mock` provider and `--dry-run` mode do not require an API key.
- A live call requires your own provider account, API key, enabled model and any applicable billing/usage entitlement.
- Never commit keys to the repository.

## Start offline first

Run a deterministic local check:

```bash
python tools/multi_provider_assistant.py \
  --provider mock \
  --prompt "Turn this idea into a short brief"
```

Expected output:

```text
[mock] Turn this idea into a short brief
```

Inspect a provider request without sending it:

```bash
python tools/multi_provider_assistant.py \
  --provider xai \
  --model example-model \
  --prompt "Audit this trend claim" \
  --dry-run
```

Expected result: JSON showing the provider, endpoint, redacted headers and request payload. A dry run proves local request construction only; it does **not** prove that the model name exists or that the live provider accepts the request.

## Provider interface status

Official provider documentation was re-checked on **2026-09-30** before this guidance was updated.

| Provider | Starter currently uses | Evidence label | Current note |
| --- | --- | --- | --- |
| OpenAI | Responses API | offline tested | Request builder targets `/v1/responses`. Live behavior is not claimed until separately verified. |
| Anthropic | Messages API | offline tested | Request builder targets `/v1/messages`. |
| xAI | Chat Completions API | offline tested, legacy interface | xAI now documents the Responses API as its preferred interface and labels Chat Completions as legacy. The current starter has **not** yet been migrated or live-verified, so do not describe it as a Responses API starter. |
| Gemini | `generateContent` | offline tested | Google still documents `generateContent` as a standard content-generation endpoint; its API reference also recommends Interactions for more agentic/stateful workflows. This starter remains intentionally single-turn. |

Official references:

- OpenAI Responses API: https://platform.openai.com/docs/api-reference/responses
- Anthropic Messages API: https://docs.anthropic.com/en/api/messages
- xAI text generation / Responses API: https://docs.x.ai/developers/model-capabilities/text/generate-text
- xAI Chat Completions legacy note: https://docs.x.ai/developers/model-capabilities/legacy/chat-completions
- Gemini generateContent reference: https://ai.google.dev/api/generate-content

## Live provider examples

Use an explicit model name that is enabled for your own account. These examples describe the current starter; they are not a claim that every model/provider path has been live-verified.

```bash
OPENAI_API_KEY=... python tools/multi_provider_assistant.py \
  --provider openai --model YOUR_MODEL \
  --prompt "Summarize this brief"

ANTHROPIC_API_KEY=... python tools/multi_provider_assistant.py \
  --provider anthropic --model YOUR_MODEL \
  --prompt "Rewrite this naturally"

XAI_API_KEY=... python tools/multi_provider_assistant.py \
  --provider xai --model YOUR_MODEL \
  --prompt "Audit this trend claim"

GEMINI_API_KEY=... python tools/multi_provider_assistant.py \
  --provider gemini --model YOUR_MODEL \
  --prompt "Build a content outline"
```

## Expected output

A successful live call prints the extracted assistant text to standard output and exits with code `0`.

The starter does not keep a long-running process, maintain an autonomous task loop, publish content, schedule jobs or act on external accounts.

## Acceptance criteria

Treat a provider path as **provider verified** only when all of the following are true:

1. the request reaches the real provider;
2. the provider accepts the selected model for the test account;
3. the response parser extracts the expected text;
4. the provider, model, date and test case are recorded;
5. no secret, private payload or billable credential is committed;
6. any provider-specific storage, retention or billing behavior relevant to the test is documented.

Until then, keep the label **offline tested**.

## Failure handling

The starter uses explicit exit codes so failures are not mistaken for successful output:

- `2` — local configuration problem, such as missing model or API key;
- `3` — provider returned an HTTP error;
- `4` — request failed before a usable provider response was received;
- `5` — a response arrived but no supported text field could be extracted.

If a live provider fails, first repeat the command with `--dry-run`, confirm the endpoint/model against current official docs, then inspect the provider error. Do not weaken tests or silently switch APIs just to make a request appear successful.

## Next step

1. Prove the local path with `mock`.
2. Inspect one provider with `--dry-run`.
3. Read that provider's current official API documentation.
4. Run one narrow live test only if you have the required account access.
5. Record provider verification separately from offline test coverage.
6. Move to an automation or MCP integration only after the single-turn behavior is reliable and the job actually needs tools, state or repeated execution.

See also: [Integrations Hub](../integrations/README.md) · [Learning Paths](../learning/README.md) · [AI Ecosystem Hub](../AI-ECOSYSTEM-HUB.md)
