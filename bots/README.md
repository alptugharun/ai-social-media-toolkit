# API Bot & Assistant Starters

**Developer starters for provider APIs. Not claims of autonomous always-on bots.**

## Included starter

`tools/multi_provider_assistant.py`

Adapter shapes:
- OpenAI Responses API
- Anthropic Messages API
- xAI Responses-compatible API
- Gemini Generate Content API
- local `mock` provider for offline testing

## Quick start without an API key

```bash
python tools/multi_provider_assistant.py \
  --provider mock \
  --prompt "Turn this idea into a short brief"
```

## Real provider usage

Use your own provider key and an explicit model name.

```bash
OPENAI_API_KEY=... python tools/multi_provider_assistant.py \
  --provider openai --model YOUR_MODEL \
  --prompt "Summarize this brief"

XAI_API_KEY=... python tools/multi_provider_assistant.py \
  --provider xai --model YOUR_MODEL \
  --prompt "Audit this trend claim"

ANTHROPIC_API_KEY=... python tools/multi_provider_assistant.py \
  --provider anthropic --model YOUR_MODEL \
  --prompt "Rewrite this naturally"

GEMINI_API_KEY=... python tools/multi_provider_assistant.py \
  --provider gemini --model YOUR_MODEL \
  --prompt "Build a content outline"
```

## Evidence status

- request builders/parsers: **offline tested**
- mock provider: **offline tested**
- live provider calls: **not provider-verified** unless a dated verification note is added

## Acceptance

A provider path is only "verified" when:
1. the request reaches the real provider;
2. the response parses correctly;
3. model/account details are recorded;
4. no secret is committed.

## Safety

Provider access, billing, rate limits, model availability and retention policies are external account concerns.
