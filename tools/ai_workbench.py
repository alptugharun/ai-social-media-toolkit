#!/usr/bin/env python3
"""Portable prompt/assistant workbench. Offline by default; live calls are opt-in.

Python 3.10+. Standard library only. No shell execution, browsing, or scheduling.
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

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "ai-workbench" / "catalog.json"
PROVIDERS = {
    "openai": ("https://api.openai.com/v1/responses", "OPENAI_API_KEY"),
    "xai": ("https://api.x.ai/v1/responses", "XAI_API_KEY"),
    "anthropic": ("https://api.anthropic.com/v1/messages", "ANTHROPIC_API_KEY"),
}
TARGETS = ("prompt", "gpt", "claude", "grok", "gemini", "skill")
MAX_INPUT_BYTES = 100_000
MAX_RESPONSE_BYTES = 2_000_000


def load_catalog(path: Path = CATALOG) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cards = data.get("cards")
    if data.get("schema_version") != 1 or not isinstance(cards, list) or not cards:
        raise ValueError("Expected a version-1 catalog with nonempty cards.")
    seen: set[str] = set()
    for card in cards:
        key = card.get("id", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", key) or key in seen:
            raise ValueError("Catalog IDs must be unique lowercase slugs.")
        seen.add(key)
        for field in ("title", "instructions", "sample_input", "expected_output", "acceptance"):
            value = card.get(field)
            if not isinstance(value, dict) or any(not isinstance(value.get(lang), str) or not value[lang].strip() for lang in ("en", "tr")):
                raise ValueError(f"{key}: missing bilingual {field}.")
    return cards


def find_card(cards: list[dict[str, Any]], key: str) -> dict[str, Any]:
    for card in cards:
        if card["id"] == key:
            return card
    raise ValueError("Unknown card ID. Run the list command first.")


def export_card(card: dict[str, Any], target: str, lang: str) -> str:
    if target not in TARGETS or lang not in ("en", "tr"):
        raise ValueError("Unsupported export target or language.")
    title = card["title"][lang]
    rules = card["instructions"][lang]
    prefix = ""
    if target == "skill":
        prefix = (f"---\nname: {card['id']}\n"
                  f"description: {json.dumps(title + '. Use when explicitly requested for this task.', ensure_ascii=False)}\n"
                  "license: CC-BY-NC-4.0\n---\n\n")
    modes = {
        "prompt": "Use the instructions below in a new chat, then supply your input.",
        "gpt": "Configuration blueprint, not an installed or published GPT. Check account eligibility before using the GPT editor.",
        "claude": "Project-instructions blueprint. Add source files separately as project knowledge; this is not a Claude Code plugin.",
        "grok": "Portable instruction block for a Grok chat or an xAI API assistant. This file does not create a running bot.",
        "gemini": "Gem-instructions blueprint. Paste into your Gem instructions; this is not an API credential or an installed Gemini CLI extension.",
        "skill": "Portable SKILL.md export. Review before installing; host discovery and permissions must be tested separately.",
    }
    return (prefix + f"# {title}\n\n{modes[target]}\n\n"
            f"## Instructions\n\n{rules}\n\n"
            f"## Example input / conversation starter\n\n{card['sample_input'][lang]}\n\n"
            f"## Illustrative output (not a measured model result)\n\n{card['expected_output'][lang]}\n\n"
            f"## Acceptance check\n\n{card['acceptance'][lang]}\n")


def build_payload(provider: str, model: str, instructions: str, text: str, max_tokens: int) -> dict[str, Any]:
    if provider not in PROVIDERS:
        raise ValueError("Provider must be openai, xai, or anthropic.")
    if not model.strip() or len(model) > 160:
        raise ValueError("Supply an exact model ID available to your API account.")
    if not text.strip() or len(text.encode("utf-8")) > MAX_INPUT_BYTES:
        raise ValueError("Input must contain 1 to 100000 UTF-8 bytes.")
    if not 64 <= max_tokens <= 8192:
        raise ValueError("max-tokens must be between 64 and 8192.")
    if provider == "anthropic":
        return {"model": model, "max_tokens": max_tokens, "system": instructions,
                "messages": [{"role": "user", "content": text}]}
    if provider == "xai":
        return {"model": model, "store": False, "max_output_tokens": max_tokens,
                "input": [{"role": "system", "content": instructions}, {"role": "user", "content": text}]}
    return {"model": model, "store": False, "max_output_tokens": max_tokens,
            "instructions": instructions, "input": text}


def extract_text(provider: str, result: dict[str, Any]) -> str:
    if not isinstance(result, dict) or result.get("error"):
        raise ValueError("Provider returned an error or unsupported response.")
    if provider == "anthropic":
        if result.get("stop_reason") not in (None, "end_turn", "stop_sequence"):
            raise ValueError("Response is truncated or requires an unsupported tool action.")
        blocks = result.get("content", [])
    else:
        if result.get("status") not in (None, "completed"):
            raise ValueError("Response did not complete; review before retrying.")
        blocks = [block for item in result.get("output", []) if isinstance(item, dict) and item.get("type") == "message"
                  for block in item.get("content", [])]
    texts = [block["text"] for block in blocks if isinstance(block, dict)
             and block.get("type") in ("text", "output_text") and isinstance(block.get("text"), str)]
    if not texts:
        raise ValueError("No text answer returned; output may be refused, incomplete, or tool-only.")
    return "\n".join(texts)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Redirect refused: credentials must stay on the selected provider endpoint.")


def call_provider(provider: str, payload: dict[str, Any], timeout: int) -> str:
    if provider not in PROVIDERS or not 1 <= timeout <= 300:
        raise ValueError("Invalid provider or timeout (1-300 seconds).")
    endpoint, key_name = PROVIDERS[provider]
    key = os.environ.get(key_name, "").strip()
    if not key or any(ch in key for ch in "\r\n"):
        raise ValueError(f"Set {key_name} privately in your environment. Never paste it into the repository.")
    headers = {"Content-Type": "application/json"}
    if provider == "anthropic":
        headers.update({"x-api-key": key, "anthropic-version": "2023-06-01"})
    else:
        headers["Authorization"] = "Bearer " + key
    req = urllib.request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    # No automatic retries: a timeout may still represent a billed request.
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ValueError("Response exceeded the configured safety limit.")
        return extract_text(provider, json.loads(raw.decode("utf-8")))
    except urllib.error.HTTPError as exc:
        raise ValueError(f"Provider HTTP {exc.code}. Check model access, credentials, limits and billing; no automatic retry.") from None
    except (urllib.error.URLError, TimeoutError):
        raise ValueError("Network request failed or timed out. Provider execution may have occurred; inspect usage before retrying.") from None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List bundled original prompt cards.")
    exp = sub.add_parser("export", help="Print one portable instruction blueprint; does not install it.")
    exp.add_argument("id")
    exp.add_argument("--target", choices=TARGETS, default="prompt")
    exp.add_argument("--lang", choices=("en", "tr"), default="en")
    run = sub.add_parser("request", help="Preview a provider payload. Use --live to send one billable API request.")
    run.add_argument("id")
    run.add_argument("--provider", choices=tuple(PROVIDERS), required=True)
    run.add_argument("--model", required=True)
    run.add_argument("--input", type=Path, required=True)
    run.add_argument("--lang", choices=("en", "tr"), default="en")
    run.add_argument("--max-tokens", type=int, default=1024)
    run.add_argument("--timeout", type=int, default=90)
    run.add_argument("--live", action="store_true")
    args = parser.parse_args(argv)
    try:
        cards = load_catalog()
        if args.command == "list":
            print("\n".join(c["id"] + " — " + c["title"]["en"] for c in cards))
            return 0
        card = find_card(cards, args.id)
        if args.command == "export":
            print(export_card(card, args.target, args.lang))
            return 0
        if args.input.stat().st_size > MAX_INPUT_BYTES:
            raise ValueError("Input file is too large; maximum 100000 bytes.")
        text = args.input.read_text(encoding="utf-8-sig")
        payload = build_payload(args.provider, args.model, card["instructions"][args.lang], text, args.max_tokens)
        if args.live:
            print(call_provider(args.provider, payload, args.timeout))
        else:
            print(json.dumps({"mode": "OFFLINE_PREVIEW", "network_called": False,
                              "endpoint": PROVIDERS[args.provider][0], "payload": payload}, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("error: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
