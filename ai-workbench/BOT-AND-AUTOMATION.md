# A bot starter you can inspect before spending credits

`tools/ai_workbench.py` is a single-turn command-line assistant runner for OpenAI, xAI and Anthropic. It does not deploy a web chat, run a Telegram/X bot, store multi-turn memory or keep executing after the process exits.

## 1. Preview without credentials

From the repository root:

```bash
python tools/ai_workbench.py request evidence-desk --provider openai --model MODEL_ID --input ai-workbench/sample-input.txt --lang en
```

`OFFLINE_PREVIEW` and `network_called: false` mean the request was built locally. Read the instructions, input and output limit. Choose `--provider xai` for the xAI shape or `--provider anthropic` for Claude's Messages shape. This is not a generated model answer.

## 2. Make a live call deliberately

API accounts, billing and model access are separate from chat-app subscriptions. Use the exact model ID your selected API account permits; the code intentionally does not guess one.

Set only the corresponding key privately in your environment: `OPENAI_API_KEY`, `XAI_API_KEY` or `ANTHROPIC_API_KEY`. Do not commit keys, put them in prompts or expose them in screenshots. The runner does not load .env files automatically.

PowerShell 7 supports masked, one-session entry:

```powershell
$env:OPENAI_API_KEY = Read-Host 'OpenAI API key' -MaskInput
```

Use your approved credential manager in other environments. Do not weaken an organization's policy to run this example. Add `--live` only after reviewing the request:

```powershell
py -3 tools/ai_workbench.py request evidence-desk --provider openai --model YOUR_ACTUAL_MODEL_ID --input ai-workbench/sample-input.txt --lang tr --max-tokens 512 --live
```

This sends instructions and input to the selected provider and may incur charges. The Responses payload requests `store: false`; that is not a blanket zero-retention guarantee. Provider policies still apply.

## 3. Check the answer, not only HTTP success

A successful call prints text. Apply the card's acceptance check and compare factual claims with the original input. The adapters are offline/mock tested, not live-provider verified. Confirm a harmless sample in your own authorized account before relying on them.

The runner sends no tool definitions, executes no returned code and enables no browsing. An unsupported model/parameter, incomplete answer or tool-only response is an error, not a completed task. There is no automatic retry: a timed-out request might already have been billed.

## 4. Complete draft-first workflow

Prepare a sanitized meeting note. Select Evidence Desk. Preview the request and confirm the material is permitted to leave your device. Make one explicitly approved live request. Save its output as a local draft. Check each claim against the note and apply the acceptance rule. Only then move the reviewed text to its intended destination.

Before scheduling that sequence, add a record keyed by source ID, source revision and task ID. Suggested states: RECEIVED, DRAFTED, REVIEWED, SAVED and FAILED. A repeated trigger checks the existing record before another request. On an ambiguous save, inspect the destination before retrying. On an API timeout, inspect usage rather than blindly repeating a potentially billed request.

That state-machine recipe is documentation, not a deployed scheduler in this package. The existing repository automation remains separate.

## 5. Layers still needed for a persistent bot

Session storage, authentication, rate and cost limits, privacy/deletion handling, monitoring and human handoff must be implemented and tested. A messaging bot additionally needs a supported, authorized channel. Do not relabel this CLI as an autonomous production service.

## Official API references

- [OpenAI text/Responses](https://developers.openai.com/api/docs/guides/text)
- [xAI text/Responses](https://docs.x.ai/developers/model-capabilities/text/generate-text)
- [Anthropic API overview](https://platform.claude.com/docs/en/api/overview)

Checked 29 September 2026. Model availability and schemas may change.
