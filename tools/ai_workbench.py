#!/usr/bin/env python3
"""Original AI Workbench: prompts, assistant exports and opt-in API chat.

Python 3.10+, standard library only. Local commands never call a provider.
The API adapters are contract-tested offline; no live provider claim is made.
Copyright (c) 2026 Alptuğ Harun. MIT; see tools/LICENSE in the parent project.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

CATALOG_PATH = Path(__file__).with_name("ai_workbench_catalog.json")
PROVIDERS = {
    "openai": ("https://api.openai.com/v1/responses", "OPENAI_API_KEY"),
    "xai": ("https://api.x.ai/v1/responses", "XAI_API_KEY"),
    "anthropic": ("https://api.anthropic.com/v1/messages", "ANTHROPIC_API_KEY"),
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/models/", "GEMINI_API_KEY"),
}
MAX_INPUT = 32000  # characters, NOT a token or currency limit
MAX_RESPONSE_BYTES = 2_000_000
MAX_MESSAGES = 13  # six previous user/assistant pairs + current user
MODEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,150}$")
PLACEHOLDER_RE = re.compile(r"\{\{([a-z_]+)\}\}")


class WorkbenchError(ValueError):
    """A user-actionable failure safe to display without request credentials."""


def read_json(path: Path, limit: int = 1_000_000) -> Any:
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise WorkbenchError("JSON input exceeds the size limit.")
    try:
        return json.loads(raw.decode("utf-8-sig"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise WorkbenchError("Expected a valid UTF-8 JSON file.") from exc


def load_catalog(path: Path = CATALOG_PATH) -> dict:
    data = read_json(path)
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise WorkbenchError("Unsupported catalog schema.")
    for group in ("prompts", "assistants"):
        entries = data.get(group)
        if not isinstance(entries, list) or not entries:
            raise WorkbenchError(f"Catalog requires a non-empty {group} list.")
        seen = set()
        for entry in entries:
            if not isinstance(entry, dict):
                raise WorkbenchError("Catalog entries must be objects.")
            slug = entry.get("id", "")
            if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in seen:
                raise WorkbenchError("Catalog has an invalid or duplicate ID.")
            seen.add(slug)
            for field in ("title", "purpose", "instructions"):
                if not isinstance(entry.get(field), str) or not entry[field].strip():
                    raise WorkbenchError(f"Catalog entry requires {field}.")
            if group == "prompts":
                example = entry.get("example")
                if not isinstance(example, dict):
                    raise WorkbenchError("Each prompt needs a filled example.")
                render_prompt(entry, example)
    return data


def lookup(catalog: dict, group: str, slug: str) -> dict:
    for entry in catalog[group]:
        if entry["id"] == slug:
            return entry
    raise WorkbenchError(f"Unknown {group} ID. Run the list command first.")


def render_prompt(entry: dict, values: dict) -> str:
    if not isinstance(values, dict):
        raise WorkbenchError("Prompt variables must be a JSON object.")
    required = set(PLACEHOLDER_RE.findall(entry["instructions"]))
    if set(values) != required:
        missing, extra = required - set(values), set(values) - required
        raise WorkbenchError(f"Variable mismatch; missing={sorted(missing)}, extra={sorted(extra)}")
    if any(not isinstance(v, str) or not v.strip() for v in values.values()):
        raise WorkbenchError("Every variable must be a non-empty string.")
    # One substitution pass: user text is data, never a format string or code.
    rendered = PLACEHOLDER_RE.sub(lambda match: values[match.group(1)], entry["instructions"])
    if len(rendered) > MAX_INPUT:
        raise WorkbenchError("Rendered prompt exceeds 32000 characters.")
    return rendered


def assistant_markdown(entry: dict, target: str) -> str:
    notes = {
        "chatgpt": "Instruction blueprint only. Use an eligible existing GPT/editor or permitted workspace. This file does not create or publish a GPT or ChatGPT plugin.",
        "claude": "Project-instruction blueprint. Claude Projects and Claude Code skills are different products; importing this text does not install a tool.",
        "gemini": "Gem instruction blueprint. Create/configure the Gem in an eligible account and test it there. No account modification occurs here.",
        "grok": "Portable Grok instruction blueprint. Use as session instructions or with the xAI API starter; no consumer-app bot or X account is deployed.",
        "skill": "Portable Agent Skill source. Inspect it before placing it in a host's supported skill directory. Host discovery has not been verified by this exporter.",
    }
    if target not in notes:
        raise WorkbenchError("Unknown export target.")
    prefix = ""
    if target == "skill":
        prefix = f'---\nname: {entry["id"]}\ndescription: {json.dumps(entry["purpose"], ensure_ascii=False)}\nlicense: MIT\n---\n\n'
    starters = "\n".join(f"- {item}" for item in entry["starters"])
    checks = "\n".join(f"- {item}" for item in entry["acceptance"])
    return (f'{prefix}# {entry["title"]}\n\n{entry["purpose"]}\n\n'
            f'## Status\n\n{notes[target]}\n\n## Instructions\n\n{entry["instructions"]}\n\n'
            f'## Conversation starters\n\n{starters}\n\n## Acceptance checks\n\n{checks}\n')


def validate_messages(messages: list[dict]) -> None:
    if not isinstance(messages, list) or not messages or len(messages) > MAX_MESSAGES:
        raise WorkbenchError("Expected 1-13 conversation messages.")
    total = 0
    for index, message in enumerate(messages):
        if not isinstance(message, dict) or set(message) != {"role", "content"}:
            raise WorkbenchError("Each message requires only role and content.")
        expected = "user" if index % 2 == 0 else "assistant"
        text = message["content"]
        if message["role"] != expected or not isinstance(text, str) or not text.strip():
            raise WorkbenchError("Use alternating, non-empty user/assistant messages starting with user.")
        total += len(text)
    if messages[-1]["role"] != "user" or total > MAX_INPUT:
        raise WorkbenchError("Conversation must end with user and fit the 32000-character budget.")


def build_request(provider: str, model: str, system: str, messages: list[dict], max_tokens: int) -> tuple[str, dict]:
    if provider not in PROVIDERS or not isinstance(model, str) or not MODEL_RE.fullmatch(model):
        raise WorkbenchError("Choose a known provider and a valid explicit model ID.")
    if not isinstance(system, str) or len(system) > 12000:
        raise WorkbenchError("System instructions must fit 12000 characters.")
    if type(max_tokens) is not int or not 64 <= max_tokens <= 4096:
        raise WorkbenchError("max-output-tokens must be between 64 and 4096.")
    validate_messages(messages)
    url = PROVIDERS[provider][0]
    if provider in ("openai", "xai"):
        payload = {"model": model, "input": [{"role": "system", "content": system}, *messages],
                   "max_output_tokens": max_tokens, "store": False}
    elif provider == "anthropic":
        payload = {"model": model, "system": system, "messages": messages, "max_tokens": max_tokens}
    else:
        url += model + ":generateContent"
        payload = {"systemInstruction": {"parts": [{"text": system}]},
                   "contents": [{"role": "model" if msg["role"] == "assistant" else "user",
                                 "parts": [{"text": msg["content"]}]} for msg in messages],
                   "generationConfig": {"maxOutputTokens": max_tokens}}
    return url, payload


def extract_text(provider: str, data: Any) -> str:
    if not isinstance(data, dict) or data.get("error"):
        raise WorkbenchError("Provider returned an error object; no response accepted.")
    if provider in ("openai", "xai"):
        if data.get("status") not in (None, "completed"):
            raise WorkbenchError("Provider response is incomplete or not completed; no automatic retry.")
        parts = [part.get("text", "") for item in data.get("output", []) if item.get("type") == "message"
                 for part in item.get("content", []) if part.get("type") == "output_text"]
    elif provider == "anthropic":
        if data.get("stop_reason") not in (None, "end_turn", "stop_sequence"):
            raise WorkbenchError("Claude response is incomplete, refused or requests unsupported tools.")
        parts = [part.get("text", "") for part in data.get("content", []) if part.get("type") == "text"]
    elif provider == "gemini":
        candidates = data.get("candidates", [])
        if not candidates or candidates[0].get("finishReason") not in (None, "STOP"):
            raise WorkbenchError("Gemini response is blocked, incomplete or empty.")
        parts = [part.get("text", "") for part in candidates[0].get("content", {}).get("parts", [])
                 if not part.get("thought")]
    else:
        raise WorkbenchError("Unknown response provider.")
    text = "\n".join(part for part in parts if isinstance(part, str) and part.strip()).strip()
    if not text:
        raise WorkbenchError("Provider returned no supported text. Refusals are not automatically retried.")
    return text


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise WorkbenchError("Provider redirect refused; credentials were not forwarded.")


def ask(provider: str, model: str, system: str, messages: list[dict], max_tokens: int = 1024,
        *, live: bool = False, opener=None) -> dict:
    url, payload = build_request(provider, model, system, messages, max_tokens)
    if not live:
        return {"mode": "preview", "network_called": False, "url": url,
                "required_env": PROVIDERS[provider][1], "payload": payload}
    key = os.environ.get(PROVIDERS[provider][1], "").strip()
    if not key or any(char.isspace() for char in key) or len(key) > 1000:
        raise WorkbenchError("Set the selected provider's API key in your local environment. Do not paste it into an issue or chat.")
    headers = {"Content-Type": "application/json", "User-Agent": "alptugharun-ai-workbench/0.1"}
    if provider == "anthropic":
        headers.update({"x-api-key": key, "anthropic-version": "2023-06-01"})
    elif provider == "gemini":
        headers["x-goog-api-key"] = key
    else:
        headers["Authorization"] = "Bearer " + key
    request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        transport = opener or urllib.request.build_opener(NoRedirect())
        with transport.open(request, timeout=30) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise WorkbenchError("Provider response exceeds the local size limit.")
        data = json.loads(raw.decode("utf-8"))
        text = extract_text(provider, data)
    except urllib.error.HTTPError as exc:
        # Never print response bodies: they may contain credentials or user input.
        raise WorkbenchError(f"Provider HTTP {exc.code}. Check access, model, quota and provider status; no automatic retry.") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise WorkbenchError("Network request failed or timed out. Billing outcome may be unknown; no automatic retry.") from None
    except (UnicodeError, json.JSONDecodeError, KeyError, TypeError, AttributeError):
        raise WorkbenchError("Unexpected provider response format; no automatic retry.") from None
    return {"mode": "live", "provider": provider, "model": model, "text": text}


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", newline="")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List original prompts and assistants; offline.")
    sub.add_parser("mcp-config", help="Print a local stdio config with resolved paths; does not register a host.")
    ui = sub.add_parser("build-ui", help="Create the offline browser catalog without installing a service.")
    ui.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "downloads" / "ai-workbench.html")
    render = sub.add_parser("render", help="Fill a prompt without calling an AI provider.")
    render.add_argument("id")
    render.add_argument("--vars", type=Path)
    render.add_argument("--example", action="store_true")
    export = sub.add_parser("export", help="Print assistant instructions; does not install anything.")
    export.add_argument("id")
    export.add_argument("--target", choices=["chatgpt", "claude", "gemini", "grok", "skill"], required=True)
    for command in ("ask", "chat"):
        api = sub.add_parser(command, help="Preview an API request, or opt in with --live.")
        api.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
        api.add_argument("--model", required=True, help="Use a model enabled in your own provider account.")
        api.add_argument("--assistant", default="evidence-desk")
        api.add_argument("--live", action="store_true", help="Send text to the chosen provider; may incur charges.")
        api.add_argument("--max-output-tokens", type=int, default=1024)
        if command == "ask":
            api.add_argument("--input", type=Path, required=True, help="UTF-8 text file, max 32000 characters.")
        else:
            api.add_argument("--max-turns", type=int, default=3, help="1-6 provider calls per session.")
    args = parser.parse_args(argv)
    try:
        catalog = load_catalog()
        if args.command == "build-ui":
            template = Path(__file__).with_name("ai_workbench_ui.html").read_text(encoding="utf-8")
            if template.count("__CATALOG__") != 1:
                raise WorkbenchError("UI template must contain one catalog insertion point.")
            page = template.replace("__CATALOG__", json.dumps(catalog, ensure_ascii=False).replace("<", "\\u003c"))
            with args.output.open("x", encoding="utf-8") as output:
                output.write(page)
            print("Created offline catalog. No model call, hosting or tracking was configured.")
        elif args.command == "mcp-config":
            print(json.dumps({"mcpServers": {"ai-workbench": {"command": sys.executable, "args": [str(Path(__file__).with_name("prompt_mcp_server.py").resolve())]}}}, indent=2))
        elif args.command == "list":
            for group in ("prompts", "assistants"):
                print(group.upper())
                for entry in catalog[group]:
                    print(f'  {entry["id"]}: {entry["title"]}')
        elif args.command == "render":
            if bool(args.vars) == args.example:
                raise WorkbenchError("Choose exactly one of --vars FILE or --example.")
            entry = lookup(catalog, "prompts", args.id)
            print(render_prompt(entry, entry["example"] if args.example else read_json(args.vars)))
        elif args.command == "export":
            print(assistant_markdown(lookup(catalog, "assistants", args.id), args.target))
        else:
            system = lookup(catalog, "assistants", args.assistant)["instructions"]
            if args.command == "ask":
                with args.input.open(encoding="utf-8-sig") as stream:
                    text = stream.read(MAX_INPUT + 1)
                result = ask(args.provider, args.model, system, [{"role": "user", "content": text}], args.max_output_tokens, live=args.live)
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                if not 1 <= args.max_turns <= 6:
                    raise WorkbenchError("max-turns must be between 1 and 6.")
                build_request(args.provider, args.model, system, [{"role": "user", "content": "check"}], args.max_output_tokens)
                print("LIVE: text goes to the selected provider; charges may apply." if args.live else "PREVIEW ONLY: no provider calls, no generated AI answers.")
                print("Type /exit to stop. History exists only in this process; no tools are executed.")
                history = []
                for _ in range(args.max_turns):
                    try:
                        text = input("you> ").strip()
                    except EOFError:
                        break
                    if text == "/exit":
                        break
                    if not text:
                        break
                    history.append({"role": "user", "content": text})
                    result = ask(args.provider, args.model, system, history, args.max_output_tokens, live=args.live)
                    print(result["text"] if args.live else json.dumps(result, ensure_ascii=False, indent=2))
                    if not args.live:
                        break  # do not fabricate a model reply to continue the history
                    history.append({"role": "assistant", "content": result["text"]})
        return 0
    except FileExistsError:
        print("error: Output already exists; choose another --output path.", file=sys.stderr)
        return 2
    except (WorkbenchError, OSError, UnicodeError) as exc:
        message = str(exc) if isinstance(exc, WorkbenchError) else "Cannot read or create the requested local UTF-8 file; check the path and permissions."
        print("error: " + message, file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Stopped; no automatic retry.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
