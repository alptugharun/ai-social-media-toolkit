# AI Workbench & Social Media Toolkit

**Practical prompts, assistants, skills and automation — with a clear path from download to first result.**

Resources by **Alptuğ Harun** for working with ChatGPT, Claude, Grok, Gemini and AI tools. The project began with social-media workflows; it now also includes a general AI workbench for research, writing, learning, coding and automation. The repository address stays unchanged.

[AI Workbench](ai-workbench/README.md) · [Türkçe başlangıç](ai-workbench/START-HERE-TR.md) · [Creator materials](downloads/README.md) · [Complete toolkit guide](docs/HOW-TO-USE-EVERYTHING.md)

## Choose what you need

| Your task | Start here | What you get |
| --- | --- | --- |
| Find a useful prompt | [AI Workbench](ai-workbench/README.md) | Eight original bilingual tasks, examples and acceptance checks |
| Configure an AI assistant | [Assistant setup](ai-workbench/ASSISTANTS.md) | GPT, Claude Project, Grok, Gemini Gem and portable skill routes |
| Understand plugins, apps and MCP | [Integration guide](ai-workbench/INTEGRATIONS.md) | Clear distinctions and a source-to-reviewed-draft setup recipe |
| Build an API-based assistant | [Bot starter](ai-workbench/BOT-AND-AUTOMATION.md) | OpenAI/xAI/Anthropic request preview and opt-in single-request execution |
| Use an existing Agent Skill | [Skill catalog](skills/README.md) | The established creator/research/automation skill collection |
| Create content with AI | [Creator materials](downloads/README.md) | Reels, Pinterest, Canva, voice and repurposing workflows |
| Inspect a runnable result | [Two-minute demo](examples/TWO-MINUTE-DEMO.md) | Content prioritization and outlier analysis using synthetic data |

## Try the general AI workbench

The generated browser runs locally without an API key. In a source checkout:

```bash
python tools/build_workbench_browser.py
```

Open `ai-workbench/index.html` in your browser. Search a task, read its example and acceptance check, then copy the instructions or download a setup file. GitHub's HTML viewer displays source rather than running the page.

Prefer the terminal?

```bash
python tools/ai_workbench.py list
python tools/ai_workbench.py export evidence-desk --target gpt --lang tr
python tools/ai_workbench.py request evidence-desk --provider xai --model MODEL_ID --input ai-workbench/sample-input.txt
```

The request command above is an **offline preview**, not a model call. Python 3.10+ is required. Live API access, billing and account eligibility are separate; [read the setup and limits](ai-workbench/BOT-AND-AUTOMATION.md) before adding `--live`.

## Existing toolkit

The existing tools and resources remain available. No repository, release or working skill is removed by the workbench addition.

| Collection | Resources |
| --- | --- |
| Content and creative work | [AI content](AI-CONTENT-WORKFLOW.md), [social-media system](SOCIAL-MEDIA-CONTENT-SYSTEM.md), [Canva + AI](CANVA-AI-WORKFLOW.md), [Reels](REELS-PRODUCTION-WORKFLOW.md), [Pinterest](PINTEREST-RESEARCH-FRAMEWORK.md) |
| Prompting and automation | [Prompt framework](PROMPT-ENGINEERING-FRAMEWORK.md), [automation architecture](CONTENT-AUTOMATION-ARCHITECTURE.md), [AI tool comparisons](AI-TOOL-COMPARISON-RESOURCES.md) |
| Discovery and measurement | [Digital visibility](DIGITAL-VISIBILITY-CHECKLIST.md), [runnable tools](tools/README.md), [expected demo output](examples/TWO-MINUTE-DEMO-OUTPUT.md) |
| Installation and use | [Install guide](docs/INSTALLATION.md), [runtime verification](docs/RUNTIME-VERIFICATION.md), [complete usage manual](docs/HOW-TO-USE-EVERYTHING.md) |

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

That command installs from the existing Agent Skills collection. It does not publish a ChatGPT GPT, connect an account or deploy a bot. New Workbench instruction exports are a separate catalog; their availability and licensing are documented in the [Workbench guide](ai-workbench/README.md).

## What is verified?

[Repository validation](https://github.com/alptugharun/ai-social-media-toolkit/actions/workflows/validate-skills.yml) and [Workbench local checks](ai-workbench/VALIDATION.md) describe different evidence. Offline tests do not establish live-provider behavior, model answer quality or independent adoption. Prompt examples and demo metrics are labelled as illustrative or synthetic.

The toolkit includes scheduled research and health/recovery workflows. A workflow file or green monitor is not a guarantee of uninterrupted operation or universal self-repair. Check actual run findings before relying on an automation.

## Feedback and contribution

Try one task and report the first step that confused or blocked you. Reproducible examples and small fixes are welcome.

[Support](SUPPORT.md) · [Contributing](CONTRIBUTING.md) · [Roadmap](ROADMAP.md) · [Adoption evidence](ADOPTION.md) · [Releases](https://github.com/alptugharun/ai-social-media-toolkit/releases) · [Changelog](CHANGELOG.md) · [Security](SECURITY.md)

## About the author

Alptuğ Harun is an Antalya-based social media specialist, digital content creator and creative strategist. Founder of **ADYA Creative** and co-founder of **Yeşil Dijital Akademi** with **Ahu Nur Şahin Harun**.

[Website](https://alptugharun.com) · [LinkedIn](https://www.linkedin.com/in/alptugharun/) · [Instagram](https://www.instagram.com/alptug.harun/) · [Behance](https://www.behance.net/alptugharun/)

## License

Existing [`skills/`](skills/LICENSE) and [`tools/`](tools/LICENSE) are MIT-licensed. Other original documentation, templates, Workbench cards and browser material follow the root [CC BY-NC 4.0 terms](LICENSE.md). Workbench SKILL.md exports keep the catalog's CC BY-NC license. Preserve applicable notices; export format does not change licensing.
