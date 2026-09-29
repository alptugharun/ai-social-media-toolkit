# AI Workbench

**Choose a task. Take the instructions with you. Check what comes back.**

A practical AI library by Alptuğ Harun for research, writing, learning, coding, decisions and automation. ChatGPT, Claude, Grok and Gemini are all in scope. Social media remains one application, not the boundary of this library.

## Start here

The downloadable standalone package includes `ai-workbench/index.html`. Open it in a browser, select English or Turkish, find a task, and inspect its instructions and example. Download one setup file or copy the instructions into the AI product you use. This browser does not contact a model, request credentials or track usage.

In a GitHub source checkout, generate the standalone page once from the repository root:

```bash
python tools/build_workbench_browser.py
```

Then open the generated `ai-workbench/index.html`, not `browser-template.html`. GitHub's file viewer displays HTML source; it does not run this application.

[Turkish walkthrough](START-HERE-TR.md) · [Assistant setup](ASSISTANTS.md) · [Plugins, apps and MCP](INTEGRATIONS.md) · [API bot starter](BOT-AND-AUTOMATION.md) · [Validation](VALIDATION.md)

## What is included

| Surface | Included | Not claimed |
| --- | --- | --- |
| Original prompt cards | Eight tasks in English and Turkish; examples and acceptance checks | Thousands of benchmarked prompts |
| Offline browser | Search, categories, language switch, copy and setup-file downloads | Hosted AI chat or deployed website |
| Six export formats | Prompt, ChatGPT GPT blueprint, Claude Project, Grok instructions, Gemini Gem and SKILL.md | Automatic installation or publication |
| API request runner | OpenAI, xAI and Anthropic adapters; offline preview and explicit one-request live mode | Continuous bot, messaging integration or live-provider verification |
| Integration guide | Concrete source-to-reviewed-draft setup and permission checks | Connected accounts or a running MCP server |
| Automation guide | One draft-first workflow with deduplication and recovery design | An imported n8n flow or autonomous publisher |

## Pick a job

| Card | Useful result |
| --- | --- |
| `evidence-desk` | Source-linked answer with gaps and uncertainty |
| `voice-editor` | Natural rewrite without invented facts or experiences |
| `study-companion` | Explanation, example, exercise and answer key |
| `debug-brief` | Reproducible bug report and next safe test |
| `workflow-designer` | Trigger, data flow, approval and failure-handling design |
| `prompt-repair` | A precise output contract and three test types |
| `decision-notebook` | Comparison respecting non-negotiable requirements |
| `knowledge-map` | Source IDs, contradictions and retrieval-test questions |

## Command-line use

Python 3.10 or newer. Standard library only.

```bash
python tools/ai_workbench.py list
python tools/ai_workbench.py export evidence-desk --target gpt --lang tr
python tools/ai_workbench.py export workflow-designer --target skill --lang en
python tools/ai_workbench.py request evidence-desk --provider xai --model MODEL_ID --input ai-workbench/sample-input.txt
python -m unittest discover -s tests -p test_ai_workbench.py -v
```

The last request example is an offline preview. It makes no API call. A real request requires an exact model ID accessible to your API account, a private environment key and `--live`. It may incur provider charges; see the bot guide before using it.

## Maintain the source, not copies

`catalog.json` is the source of truth. Edit English and Turkish together, run tests, and rebuild the browser. Exporting a prompt into a different format does not create a new independently tested product.

Existing toolkit skills, tools, creator materials and releases remain intact. [Reference notes](REFERENCES.md) distinguish supplied references from completed review. [Launch copy](LAUNCH-DRAFTS.md) is prepared material, not a published social post.

## Licensing

Python tools under `tools/` retain the toolkit's MIT license. Original cards, examples, browser and guides follow the root CC BY-NC 4.0 terms. SKILL.md exports from this catalog remain CC BY-NC 4.0; exporting does not change the license. [Details](LICENSE-NOTES.md).
