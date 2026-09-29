# AI Lab — prompts, assistants, skills, bots and automation

**Use AI for more than content creation. Start with a real task and leave with something you can inspect.**

ChatGPT/OpenAI, Claude/Anthropic, Grok/xAI and Gemini are all covered here. The lab includes research, writing, learning, support, debugging, prompt evaluation and automation design. Canva, Pinterest and Reels remain useful application areas, not the boundary of the library.

## Start with the result you need

| I want to… | Open this | What is ready |
|---|---|---|
| Use a better prompt immediately | [12 filled prompt cards](downloads/AI-LAB-PROMPT-CARDS.md) | Original instructions, synthetic examples and acceptance checks |
| Browse without a terminal | [Offline catalog guide](downloads/AI-WORKBENCH-GUIDE.md) | Build or download the single-file HTML catalog |
| Configure a GPT, Project, Gem or Grok instruction | [Assistant Setup Lab](downloads/ASSISTANT-SETUP-LAB.md) | Four exportable instruction packages and platform-specific boundaries |
| Start an OpenAI, Grok, Claude or Gemini API conversation | [API and terminal-chat guide](downloads/AI-WORKBENCH-GUIDE.md) | Preview-first code with four adapters and bounded multi-turn chat |
| Connect a read-only MCP tool | [Local catalog server](tools/prompt_mcp_server.py) | Three tools, stdio handshake and protocol tests |
| Export a portable Agent Skill | [AI Workbench commands](tools/ai_workbench.py) | Frontmatter, instructions, starters and acceptance checks |
| Use existing creator workflows | [Creator Materials](downloads/README.md) | The existing Pinterest, Reels and Canva resources are retained |

## Try it without an API key

```bash
python tools/ai_workbench.py list
python tools/ai_workbench.py render evidence-brief --example
python tools/ai_workbench.py export evidence-desk --target skill
python tools/ai_workbench.py build-ui
```

Open `downloads/ai-workbench.html` after building it. These commands do not connect an account or call a provider.

## What is tested—and what is not

Local tests cover all filled prompt examples, assistant export structure, four provider request/response adapters with mock responses, explicit live opt-in, size/turn limits, sanitized failures and the read-only MCP conversation over stdio.

Real provider entitlements, output quality, host discovery and deployment require separate live tests. No live provider call was required to build this lab. No custom GPT, ChatGPT plugin, social bot, public MCP endpoint or scheduled service is claimed to be deployed.

The code and the original prompt catalog live under the existing `tools/` MIT license. Documentation retains the repository's existing license. No third-party repository code or distinctive branding was copied into this implementation.

[Full usage guide](downloads/AI-WORKBENCH-GUIDE.md) · [Assistant setup](downloads/ASSISTANT-SETUP-LAB.md) · [Source catalog](tools/ai_workbench_catalog.json) · [Tests](tests/test_ai_workbench.py)
