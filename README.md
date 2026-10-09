<p align="center">
  <a href="./README.md"><img src="https://img.shields.io/badge/English-0D1117?style=for-the-badge&logo=github&logoColor=white" alt="English"></a>
  <a href="./README_TR.md"><img src="https://img.shields.io/badge/Türkçe-E30A17?style=for-the-badge&logo=readme&logoColor=white" alt="Türkçe"></a>
</p>

# AI Social Media Toolkit — AI Workbench, Agent Skills & MCP

**Build practical, testable AI workflows for ChatGPT, Claude, Gemini, Grok and creator operations.**

Built by **Alptuğ Harun**, this repository combines reusable prompts, portable assistant blueprints, installable Agent Skills, a read-only MCP server, API/bot starters, automation patterns and creator workflows. The priority is a fast first result, explicit limits and reproducible verification — not a giant list of untested features.

[Start Here](START-HERE.md) · [Creator Frame Studio](tools/creator-frame-studio/README.md) · [10 Quick Wins](QUICK-WINS.md) · [AI Builder Path](learning/AI-BUILDER-PATH.md) · [Hands-on Builder Lab](learning/AI-BUILDER-LAB.md) · [Practical AI Workflows](https://alptugharun.hashnode.dev) · [AI Ecosystem Hub](AI-ECOSYSTEM-HUB.md) · [Standalone MCP](https://github.com/alptugharun/ai-workbench-mcp) · [Agent Skills](skills/README.md) · [Security](SECURITY.md)

> **New creator tool:** [Creator Frame Studio v0.3](tools/creator-frame-studio/README.md) adds multi-format framing, editable text, Hook / Subtitle / CTA quick styles, editorial guide profiles and a deterministic preflight status card — all browser-local, with no account or API key.
>
> **New trust tool:** [MCP Permission Inspector](resources/MCP-PERMISSION-INSPECTOR.md) reviews MCP client config locally before first connection. It does not launch servers or claim runtime safety.

**Choose the smallest layer that solves the job:** prompt → assistant → Agent Skill → MCP/API → automation. Use the [60-second provider map](AI-ECOSYSTEM-HUB.md#pick-a-provider-in-60-seconds) when switching between ChatGPT, Claude, Gemini and Grok.

[![Validate Agent Skills](https://github.com/alptugharun/ai-social-media-toolkit/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/alptugharun/ai-social-media-toolkit/actions/workflows/validate-skills.yml)
[![M8ven Score](https://m8ven.ai/badge/mcp/alptugharun-ai-social-media-toolkit-adv58l?v=03bebb9d62df5457451770e8ba62ec55)](https://m8ven.ai/mcp/alptugharun-ai-social-media-toolkit-adv58l?s=readme)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/alptugharun/ai-social-media-toolkit/badge)](https://scorecard.dev/viewer/?uri=github.com/alptugharun/ai-social-media-toolkit)

## Prove it works in 2 minutes

No API key, social login or paid model call is required:

```bash
git clone https://github.com/alptugharun/ai-social-media-toolkit.git
cd ai-social-media-toolkit
python tools/first_run_check.py
```

A passing run verifies the local catalog, dry-run provider path, Agent Skill installer flow and creator demo from the checkout. It does **not** claim that every external host/provider works.

**PASS?** Pick one path below. **FAIL?** Keep the first error and use the linked troubleshooting/evidence path instead of guessing.

If the proof saved you setup time, a star helps other builders discover the repository. A reproducible failure report is even more useful than a generic “works for me.”

## Pick one path

| Goal | Fastest entry point |
| --- | --- |
| **Prove the repo works without an API key** | [Start Here](START-HERE.md) |
| **Try a useful AI job in minutes** | [10 Quick Wins](QUICK-WINS.md) |
| **Build the same assistant job across providers** | [AI Ecosystem Hub](AI-ECOSYSTEM-HUB.md) |
| **Learn prompt → assistant → skill → MCP → plugin design** | [AI Builder Path](learning/AI-BUILDER-PATH.md) |
| **Read the architecture guide before building** | [Prompt → Assistant → Agent Skill → MCP → Plugin](https://alptugharun.hashnode.dev/prompt-assistant-agent-skill-mcp-plugin-guide) |
| **Build, break and test every AI layer hands-on** | [AI Builder Lab](learning/AI-BUILDER-LAB.md) |
| **Choose a small evidence-labeled AI team** | [Verified AI Team Stack](resources/AI-TEAM-STACK.md) |
| **Install reusable Agent Skills** | [Agent Skills](skills/README.md) |
| **Build/test the skills-only ChatGPT/Codex plugin** | [Plugin Guide](PLUGIN-GUIDE.md) |
| **Run a local read-only MCP server** | [AI Workbench MCP](https://github.com/alptugharun/ai-workbench-mcp) |
| **Use creator workflows for Canva, Pinterest or Reels** | [Creator Materials](downloads/README.md) |
| **Frame and export creator visuals across social formats** | [Creator Frame Studio](tools/creator-frame-studio/README.md) |
| **Review an MCP config before first connection** | [MCP Permission Inspector](resources/MCP-PERMISSION-INSPECTOR.md) |
| **Inspect security, trust and runtime evidence** | [Trust & Discovery Review](docs/TRUST-DISCOVERY-REVIEW.md) |

Want a curated ecosystem map after the first run? Use the **[AI Creator Stack](resources/AI-CREATOR-STACK.md)**.

## Start with one useful result

No API key or third-party Python package is required for the local commands:

```bash
python tools/ai_workbench.py list
python tools/ai_workbench.py render evidence-brief --example
python tools/ai_workbench.py build-ui
```

Run these from the downloaded repository folder, then open `downloads/ai-workbench.html` in a browser. The catalog lets you select a task, edit example inputs and copy or download the resulting instruction. It does not send data or call a model.

### Try the read-only MCP locally

The MCP package now has a dedicated public home at **[alptugharun/ai-workbench-mcp](https://github.com/alptugharun/ai-workbench-mcp)**. This toolkit keeps a mirrored package surface for integration testing, so the local checkout can still be tested directly:

```bash
python -m pip install --no-deps ./packages/ai-workbench-mcp
```

Point a local stdio-capable MCP host at this command:

```text
alptugharun-ai-workbench-mcp
```

It exposes three tools — `list_prompts`, `render_prompt`, and `get_assistant` — and does not request network, shell, filesystem-write, account, or provider access. The wheel build/install/handshake path is CI-gated on Ubuntu 24.04, Ubuntu 26.04, and Windows 2025.

[Standalone MCP repository](https://github.com/alptugharun/ai-workbench-mcp) · [Bundled integration copy](packages/ai-workbench-mcp/README.md) · [Independent host verification wanted](https://github.com/alptugharun/ai-workbench-mcp/issues/5)

Version `0.1.0a2` is published on PyPI and the official MCP Registry reports `io.github.alptugharun/ai-workbench-mcp` version `0.1.0a2` as active/latest. The `0.1.0a2` release adds local `--doctor` and `--version` diagnostics without widening the read-only tool surface. The recorded maintainer-run Cursor 3.20.21 session successfully invoked all three public tools; that host evidence remains separate from package publication, registry acceptance and independent user verification.

Prefer to read first? Open the [filled prompt examples](downloads/AI-LAB-PROMPT-CARDS.md). Need the complete setup? Use the [AI Workbench guide](downloads/AI-WORKBENCH-GUIDE.md), including Windows commands and troubleshooting.

**Using your own data?** Start with the [exact CSV columns, examples and validation commands](docs/CSV-INPUTS.md), then follow the [Reels analysis-to-brief example](examples/workflows/reels-from-outlier.md).

**Want to contribute?** Follow [fork → branch → tests → PR](CONTRIBUTING.md#submit-through-a-fork). You do not need write access to this repository. Runtime reports have a separate [evidence checklist](docs/RUNTIME-VERIFICATION.md).

## What you can use

| Area | Included | Start here |
|---|---|---|
| **Prompts and context** | AI Workbench prompt cards plus a structured prompt library with inputs, QA, examples and troubleshooting | [Prompt Library](prompts/README.md) |
| **GPTs and assistants** | Portable assistant blueprints plus ChatGPT/Plugin migration, Claude Project, Gemini Gem and Grok setup guides | [Assistant Blueprints](assistants/README.md) |
| **Agent Skills** | Existing installable skills plus a portable assistant-to-skill export | [Skills](skills/README.md) |
| **API bots** | Existing AI Workbench adapters plus a small provider-neutral starter for OpenAI, xAI, Anthropic and Gemini | [Bot Starters](bots/README.md) |
| **MCP and integrations** | Read-only local MCP tooling, integration contracts and Plugin/MCP decision guidance | [Integrations Hub](integrations/README.md) |
| **Creative work** | Canva + AI, Pinterest, Reels, brand voice and repurposing resources | [Creator materials](downloads/README.md) |
| **Automation recipes** | Approval-gated research, publishing, monitoring and recovery patterns | [Automation Recipes](automation-recipes/README.md) |
| **Learning paths** | Prompt → assistant → skill → MCP → plugin → automation progression, including hands-on failure and regression gates | [AI Builder Lab](learning/AI-BUILDER-LAB.md) |
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

[Community](COMMUNITY.md) · [Discussions](https://github.com/alptugharun/ai-social-media-toolkit/discussions) · [Support](SUPPORT.md) · [Contributing](CONTRIBUTING.md) · [Roadmap](ROADMAP.md) · [Adoption evidence](ADOPTION.md) · [Security](SECURITY.md) · [Trust & discovery review](docs/TRUST-DISCOVERY-REVIEW.md) · [Cite this project](CITATION.cff) · [Releases](https://github.com/alptugharun/ai-social-media-toolkit/releases)

## Verify before trusting a badge

Run the offline public-readiness gate before release:

```bash
python tools/release_readiness.py
python -m unittest discover -s tests -v
```

This checks the evidence the repository can prove itself: MCP annotations and schemas, name-level MCP test coverage, public trust/onboarding files, JSON manifests and immutable third-party GitHub Action refs. It does **not** fabricate external adoption, registry acceptance, a trust grade or live-host compatibility. See [Trust & Discovery Review](docs/TRUST-DISCOVERY-REVIEW.md) for M8ven, OpenAI plugin review, the official MCP Registry, directory submission and OpenSSF guidance.

## License

- [`tools/`](tools/LICENSE), including the new workbench code, UI template and original prompt catalog: **MIT**.
- [`skills/`](skills/LICENSE): **MIT**.
- Other original documentation, frameworks and templates retain the existing **CC BY-NC 4.0** terms in [LICENSE.md](LICENSE.md), unless a file states otherwise.

Preserve applicable attribution and license notices. Referenced platforms and trademarks belong to their respective owners.

---

**Alptuğ Harun** · Social Media Specialist · Digital Content Creator · Practical AI Workflows  
[Website](https://alptugharun.com) · [Practical AI Workflows](https://alptugharun.hashnode.dev) · [LinkedIn](https://www.linkedin.com/in/alptugharun/)

<details>
<summary>Türkçe</summary>

Bu kütüphane yalnızca Canva, Pinterest veya Reels için değil. ChatGPT/GPT'ler, Claude, Grok, Gemini; promptlar, asistan paketleri, Agent Skills, MCP araçları, API botları ve otomasyonlar birlikte ele alınıyor.

Bir kart seçerek başlayabilir, talimatı örnek verinle doldurabilir, asistan paketi çıkarabilir veya test edilebilir yerel kodu çalıştırabilirsin. Kurulum, canlı model testi ve yayın ayrı adımlardır. Her ürünün kullanım yolu ve sınırları ilgili rehberde yer alır.

</details>
