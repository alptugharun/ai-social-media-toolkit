# Validation evidence and limits

Local checks repeated on 29 September 2026. These checks validate this new workbench; they do not certify every existing toolkit component or any external account.

## Reproduce the offline checks

```bash
python -m compileall -q tools tests
python -m unittest discover -s tests -p test_ai_workbench.py -v
python tools/build_workbench_browser.py
python tools/ai_workbench.py request evidence-desk --provider xai --model MODEL_ID --input ai-workbench/sample-input.txt --lang tr
```

Observed locally: 28 workbench unit tests passed. They cover bilingual contracts, unique IDs, six export formats, three provider payloads, text extraction, incomplete/refused responses, missing keys, fixed endpoints, redirect refusal, HTTP error handling, offline preview and browser generation. Network calls in API tests are mocked; test credentials are dummy values.

## Browser checks

A headless Chromium session rendered the generated HTML via `set_content`; file-URL navigation was restricted in the test environment. This is not a claim of testing the user's browser or device.

Observed: eight initial cards; English/Turkish selection; category/search and empty-result behavior; expandable instructions; downloaded SKILL.md matching the CLI; all 8 × 6 × 2 browser exports matching the CLI; no mobile-width horizontal overflow at 390 pixels; dark-mode rendering; no JavaScript page errors; no HTTP requests during the tested interactions.

Eight cards with multiple languages and formats are not 96 independently authored prompts. An acceptance rule on a card is a test recipe, not proof that every AI model will follow it.

## Not verified

No paid live provider request; no new GPT publication; no persistent bot deployment; no messaging channel; no installed MCP server; no account authorization; no social post publication; no independently measured usage or growth. Repository-wide CI is a separate result recorded on the pull request, not implied by this local report.
