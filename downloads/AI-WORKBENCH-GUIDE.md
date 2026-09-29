# AI Workbench — from a useful prompt to a working assistant

**A local toolkit for prompts, assistant instructions, API chat and read-only MCP. Not a promise that a bot has already been deployed.**

Author: Alptuğ Harun. Implementation: Python 3.10+ and its standard library. No package installation is required for these new tools. The workbench is an addition to the existing social-media toolkit; it also covers research, writing, learning, support, coding diagnosis and general automation.

## What you receive

| Component | What it actually does | What it does not do |
|---|---|---|
| 12 original prompt cards | Fill a tested input structure and prepare an instruction | Guarantee answer quality or fetch live evidence |
| 4 assistant blueprints | Export instructions for ChatGPT, Claude, Gemini, Grok or a portable skill | Create an account, publish a GPT or install a plugin |
| Offline browser catalog | Search cards, edit inputs, copy or download a prompt | Send data, call a model or host a website |
| Four API adapters | Preview or explicitly send text to OpenAI, xAI, Anthropic or Gemini | Use the consumer chat subscription as API credit |
| Multi-turn terminal chat | Keep up to six turns in memory during the process | Run indefinitely, store long-term memory or post to social networks |
| Read-only MCP example | Expose three local catalog tools over stdio | Browse, execute shell commands, change files or grant permissions |

## 1. Open it without a terminal

In the downloadable workbench bundle, open `downloads/ai-workbench.html` in your browser. Select **Promptlar**, choose a task, edit the filled example fields and press **Talimatı hazırla**. The lower panel is the exact instruction to copy into your chosen AI assistant. Then evaluate the AI answer using the checks below the panel.

Use **Asistanlar** for reusable assistant instructions. This tab does not install a GPT or connect an account. Input stays in the page until you close or refresh it; nothing is saved automatically.

On GitHub, an HTML file is shown as source, not as a running app. Download the bundle, or generate the standalone page from source:

```bash
python tools/ai_workbench.py build-ui
```

This creates `downloads/ai-workbench.html`. It refuses to overwrite an existing file. To produce another copy, use `--output downloads/ai-workbench-new.html`. Keep the page next to the Markdown guides for its relative documentation links.

**Success check:** editing a field changes the copied instruction; no sign-in or API key is requested. Automatic clipboard access may be restricted for local files. The page then selects the result so you can use Ctrl+C or Command+C.

## 2. Get the source and check Python

Download the current repository as ZIP using **Code → Download ZIP** and extract it. Open a terminal inside the extracted `ai-social-media-toolkit` directory. Alternatively, clone the repository if you already have Git:

```bash
git clone https://github.com/alptugharun/ai-social-media-toolkit.git
cd ai-social-media-toolkit
python --version
python tools/ai_workbench.py list
```

On Windows, use `py -3` instead of `python` if that is your installed launcher. If neither is recognized, install Python using its official installer, reopen the terminal and repeat the version check. Do not run random installation scripts from comments or issue replies.

**Success check:** the list contains 12 prompt IDs and four assistant IDs. Running from another directory is supported when you provide the complete path to `ai_workbench.py`.

## 3. Produce a ready-to-use prompt

Start with bundled synthetic input, not private client data:

```bash
python tools/ai_workbench.py render evidence-brief --example
python tools/ai_workbench.py render evidence-brief --vars examples/ai-workbench/research-input.json
```

The JSON file has three keys: `question`, `sources` and `language`. Replace their values with your real question, labelled source notes and preferred output language. Keep all keys. Missing keys, extra keys, empty values and oversized input are rejected.

To save the filled instruction on macOS/Linux:

```bash
python tools/ai_workbench.py render evidence-brief --example > request.txt
```

On Windows PowerShell:

```powershell
py -3 -X utf8 tools/ai_workbench.py render evidence-brief --example | Out-File -Encoding utf8 request.txt
```

**Expected result:** a filled instruction containing the synthetic source labels S1 and S2. This is not an AI-generated answer. Send it to your assistant, then check that interest in a workshop is not presented as proven willingness to pay.

All filled examples are also readable in [AI-LAB-PROMPT-CARDS.md](AI-LAB-PROMPT-CARDS.md).

## 4. Preview an API request before spending anything

```bash
python tools/ai_workbench.py ask --provider xai --model demo-model --input request.txt
```

Without `--live`, this prints JSON with `mode: preview`, `network_called: false`, the selected endpoint, the required environment variable and the request payload. `demo-model` is deliberately a local preview label, not a claimed valid model.

Supported provider names are `openai`, `xai`, `anthropic` and `gemini`. The API implementation follows the official endpoint shapes listed in the source notes below. You must select a model actually enabled in your own provider account for live requests. No automatic provider fallback occurs.

## 5. Make a deliberate live request

Live requests send the supplied text to the selected provider and may incur charges. Set an account/project spending limit at the provider before using them. The local output-token and turn caps are **not** a monetary budget or a guarantee against charges.

| Provider | Local environment variable | Interface used |
|---|---|---|
| OpenAI | `OPENAI_API_KEY` | Responses API |
| xAI / Grok | `XAI_API_KEY` | Responses API |
| Anthropic / Claude | `ANTHROPIC_API_KEY` | Messages API |
| Google Gemini | `GEMINI_API_KEY` | generateContent API |

The program does not read `.env` files automatically. Do not put a key in a command argument, source file, screenshot, public issue or ChatGPT conversation.

Example for entering an xAI key into the current PowerShell session without displaying the key:

```powershell
$secureKey = Read-Host "xAI API key" -AsSecureString
$env:XAI_API_KEY = ([System.Net.NetworkCredential]::new('', $secureKey)).Password
$model = Read-Host "Exact model ID enabled in your xAI account"
py -3 tools/ai_workbench.py ask --provider xai --model $model --input request.txt --live
Remove-Item Env:XAI_API_KEY
Remove-Variable secureKey
```

On Bash:

```bash
read -r -s -p "xAI API key: " XAI_API_KEY
export XAI_API_KEY
printf '\n'
read -r -p "Exact model ID enabled in your account: " MODEL
python tools/ai_workbench.py ask --provider xai --model "$MODEL" --input request.txt --live
unset XAI_API_KEY
```

Use the matching environment-variable and provider name for another adapter. Do not share keys between providers.

**Expected result:** `mode: live` and a text response. A 401/403, invalid model, quota error, refusal, incomplete response or network timeout stops the call. Raw provider error bodies are not printed. The program does not retry automatically; after an ambiguous timeout the billing outcome may be unknown.

OpenAI and xAI requests set `store: false`. That flag is not a blanket promise about abuse monitoring, logging or every provider's retention policy. Review your provider's current data terms before sending sensitive material.

## 6. Run a bounded terminal bot

After setting the matching API key and model:

```bash
python tools/ai_workbench.py chat --provider xai --model YOUR_ENABLED_MODEL_ID --assistant evidence-desk --max-turns 3 --live
```

Replace `YOUR_ENABLED_MODEL_ID` before running. Ask a question at `you>`, then ask a follow-up. The actual assistant answer is included in the next request. Type `/exit` or press Ctrl+C to stop. The process ends after the configured number of calls, with a maximum of six.

Without `--live`, chat previews one request and stops; it does not invent a fake model answer. No conversation file is saved. No Telegram, Discord, X account, hosting service, scheduled task or social publisher is created.

## 7. Export an assistant or skill

```bash
python tools/ai_workbench.py export evidence-desk --target chatgpt
python tools/ai_workbench.py export plain-language-editor --target claude
python tools/ai_workbench.py export learning-partner --target gemini
python tools/ai_workbench.py export workflow-designer --target grok
python tools/ai_workbench.py export evidence-desk --target skill
```

Use the exported instruction in a host that actually supports it. A `skill` export contains frontmatter plus instructions, starters and acceptance checks. Save it as `SKILL.md` inside an `evidence-desk` folder in the chosen host's documented skill location. The export command itself does not install anything.

The full setup and test procedure is in [ASSISTANT-SETUP-LAB.md](ASSISTANT-SETUP-LAB.md).

## 8. Connect the read-only MCP example

```bash
python tools/ai_workbench.py mcp-config
```

This prints a local `mcpServers` configuration with your current Python executable and the actual absolute path to `prompt_mcp_server.py`. Use it only in a client that supports that configuration shape and stdio servers. Other clients may require translating the fields through their own setup UI.

Expected tools: `list_prompts`, `render_prompt`, `get_assistant`. `render_prompt` prepares text; it does not call a model. The server does not implement remote HTTP, OAuth, sampling, resources, arbitrary file reading or shell execution. It implements a small, pinned MCP subset with local protocol tests, not a universal host-certification claim.

## Troubleshooting

| Symptom | First check |
|---|---|
| `No such file` | You are in the repository folder, or have supplied the absolute script path. |
| Invalid JSON / encoding | Save variable files as UTF-8; use double quotes and no trailing commas. |
| Variable mismatch | Compare your keys with the filled example for that exact prompt ID. |
| No API answer | Preview is the default; it prepares a request without spending. |
| Missing key | Set the selected provider's environment variable in the same terminal. |
| HTTP 400 | Check model ID, selected provider and current supported request fields. |
| HTTP 401/403 | Check provider account access; do not retry to bypass a restriction. |
| HTTP 429 | Check quota and provider status; the tool does not loop or auto-switch providers. |
| Incomplete output | Review input scope and output budget; any new request is a deliberate, possibly billable call. |
| MCP tools do not appear | Check stdio support, actual Python path, catalog location and initialization logs. |

## Tests and limits

```bash
python -m unittest discover -s tests -p "test_ai_workbench.py" -v
python -m unittest discover -s tests -p "test_prompt_mcp_server.py" -v
```

Provider tests use mock responses. They check request construction, parsing, opt-in, input limits and failure handling. They do not verify a real subscription, model entitlement, generated answer quality, zero-cost operation or every MCP host. Live-provider and host tests remain separate.

## Türkçe kullanım özeti

**Kod istemeyen kullanıcı:** HTML kataloğunu aç → bir kart seç → örnek girdiyi değiştir → talimatı kopyala → kullandığın yapay zekâya ver → kabul ölçütleriyle yanıtı değerlendir.

**GPT / asistan isteyen kullanıcı:** `export` ile rolü çıkar → hesabının gerçekten desteklediği editörde kur → normal, eksik bilgi ve çelişkili girdi testlerini çalıştır → ancak sonra paylaşım ayarlarını değerlendir. Dosya indirmek bir GPT'yi yayımlamaz.

**Bot isteyen kullanıcı:** önce `ask` önizlemesini gör → kendi bilgisayarında ayrı API erişimini yapılandır → ücretli çağrıyı bilerek `--live` ile başlat → sınırlı `chat` oturumunda dene. Bu bir başlangıç kodudur; 24 saat çalışan hizmet değildir.

**Eklenti / MCP isteyen kullanıcı:** üç yerel, salt-okunur aracı destekleyen MCP istemcisine bağla. Bağlantı yeni yetki, web erişimi veya sosyal medya yayın hakkı yaratmaz.

## Official implementation references

Checked 29 September 2026; these document API contracts, not successful live tests of this code.

- [OpenAI text generation](https://developers.openai.com/api/docs/guides/text)
- [xAI Responses API](https://docs.x.ai/developers/rest-api-reference/inference/responses)
- [Anthropic Messages API](https://platform.claude.com/docs/en/api/go/messages/create)
- [Gemini generateContent](https://ai.google.dev/api/generate-content)
- [MCP stdio transport](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
- [MCP initialization](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle)
- [MCP tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
