# AI Social Media Toolkit

**Practical AI tools, prompts, assistants and automation — with creator workflows included.**

Built by **Alptuğ Harun** for people using ChatGPT, Claude, Grok, Gemini and agent-based tools in real work. Start with research, writing, learning, support or automation. Use the creator resources when the job calls for Canva, Pinterest, Reels or social-media strategy.

[AI Lab](AI-LAB.md) · [Prompt cards](downloads/AI-LAB-PROMPT-CARDS.md) · [Assistant setup](downloads/ASSISTANT-SETUP-LAB.md) · [Usage guide](downloads/AI-WORKBENCH-GUIDE.md)

[![Validate Agent Skills](https://github.com/alptugharun/ai-social-media-toolkit/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/alptugharun/ai-social-media-toolkit/actions/workflows/validate-skills.yml)

## Start with one useful result

No API key or third-party Python package is required for the local commands:

```bash
python tools/ai_workbench.py list
python tools/ai_workbench.py render evidence-brief --example
python tools/ai_workbench.py build-ui
```

Run these from the downloaded repository folder, then open `downloads/ai-workbench.html` in a browser. The catalog lets you select a task, edit example inputs and copy or download the resulting instruction. It does not send data or call a model.

Prefer to read first? Open the [filled prompt examples](downloads/AI-LAB-PROMPT-CARDS.md). Need the complete setup? Use the [AI Workbench guide](downloads/AI-WORKBENCH-GUIDE.md), including Windows commands and troubleshooting.

## What you can use

| Area | Included | Start here |
|---|---|---|
| **Prompts and context** | 12 original task prompts, filled examples and acceptance checks | [Prompt cards](downloads/AI-LAB-PROMPT-CARDS.md) |
| **GPTs and assistants** | Four instruction packages for research, writing, learning and workflow design | [Assistant Setup Lab](downloads/ASSISTANT-SETUP-LAB.md) |
| **Agent Skills** | Existing installable skills plus a portable assistant-to-skill export | [Skills](skills/README.md) |
| **API bots** | OpenAI, xAI, Anthropic and Gemini request adapters; preview-first, bounded terminal chat | [Bot and API guide](downloads/AI-WORKBENCH-GUIDE.md) |
| **MCP and integrations** | A small read-only local catalog server with three tools | [MCP source](tools/prompt_mcp_server.py) |
| **Creative work** | Canva + AI, Pinterest, Reels, brand voice and repurposing resources | [Creator materials](downloads/README.md) |
| **Measurement and operations** | Content scoring, outlier analysis, research radars and bounded failure diagnosis | [Existing toolkit manual](docs/HOW-TO-USE-EVERYTHING.md) |

A prompt is an instruction. An assistant package organizes behavior. A skill is reusable instruction material in a supported host. An MCP server exposes tools. An API bot runs code against a provider. None of these automatically grants account access, installs a plugin or publishes content.

## Build an assistant without starting from a blank page

```bash
python tools/ai_workbench.py export evidence-desk --target chatgpt
python tools/ai_workbench.py export plain-language-editor --target claude
python tools/ai_workbench.py export learning-partner --target gemini
python tools/ai_workbench.py export workflow-designer --target grok
python tools/ai_workbench.py export evidence-desk --target skill
```

These commands produce instruction packages, not hosted assistants. The [setup guide](downloads/ASSISTANT-SETUP-LAB.md) explains current account restrictions, where each kind of instruction belongs and how to test normal, missing-data and conflicting-input cases.

## Inspect an API request before running a bot

```bash
python tools/ai_workbench.py render evidence-brief --example > request.txt
python tools/ai_workbench.py ask --provider xai --model demo-model --input request.txt
```

The second command is a **local preview**. `demo-model` is not a claimed live model. Live requests require an enabled model, your own provider API access and the explicit `--live` option; charges may apply. The code does not use browser cookies or consumer-chat sessions.

[API keys, live opt-in and terminal chat](downloads/AI-WORKBENCH-GUIDE.md) · [Provider contract tests](tests/test_ai_workbench.py)

## Existing creator tools are still here

The original skills and workflows have not been deleted or renamed.

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

Use the [installation guide](docs/INSTALLATION.md) and [runtime verification matrix](docs/RUNTIME-VERIFICATION.md). Documented paths and local tests are not the same as independent verification in every agent host.

For a local scoring example:

```bash
python tools/two_minute_demo.py
```

[Two-minute demo](examples/TWO-MINUTE-DEMO.md) · [Expected synthetic output](examples/TWO-MINUTE-DEMO-OUTPUT.md) · [Creator quick start](START-HERE.md)

## Status and limitations

The first alpha release predates AI Workbench. Use the current branch containing this addition rather than assuming the earlier release includes it.

The workbench tests cover prompt rendering, assistant exports, mock provider contracts, input limits and a read-only MCP protocol subset. Live-provider calls, account entitlement, generated-answer quality, host installation and deployment are separate checks. No published GPT, ChatGPT plugin, social bot or 24-hour service is claimed to exist because these files were added.

Examples are synthetic unless a source says otherwise. No promise of virality, income, GitHub Trending placement or error-free operation is made.

## Help improve a real workflow

Run one task and report the first point where you got confused or blocked. Reproducible bug reports, clearer examples and real runtime checks are more useful than another empty feature list.

[Support](SUPPORT.md) · [Contributing](CONTRIBUTING.md) · [Roadmap](ROADMAP.md) · [Adoption evidence](ADOPTION.md) · [Security](SECURITY.md) · [Releases](https://github.com/alptugharun/ai-social-media-toolkit/releases)

## License

- [`tools/`](tools/LICENSE), including the new workbench code, UI template and original prompt catalog: **MIT**.
- [`skills/`](skills/LICENSE): **MIT**.
- Other original documentation, frameworks and templates retain the existing **CC BY-NC 4.0** terms in [LICENSE.md](LICENSE.md), unless a file states otherwise.

Preserve applicable attribution and license notices. Referenced platforms and trademarks belong to their respective owners.

---

**Alptuğ Harun** · Social Media Specialist · Digital Content Creator · Practical AI Workflows  
[Website](https://alptugharun.com) · [LinkedIn](https://www.linkedin.com/in/alptugharun/)

<details>
<summary>Türkçe</summary>

Bu kütüphane yalnızca Canva, Pinterest veya Reels için değil. ChatGPT/GPT'ler, Claude, Grok, Gemini; promptlar, asistan paketleri, Agent Skills, MCP araçları, API botları ve otomasyonlar birlikte ele alınıyor.

Bir kart seçerek başlayabilir, talimatı örnek verinle doldurabilir, asistan paketi çıkarabilir veya test edilebilir yerel kodu çalıştırabilirsin. Kurulum, canlı model testi ve yayın ayrı adımlardır. Her ürünün kullanım yolu ve sınırları ilgili rehberde yer alır.

</details>
