#!/usr/bin/env python3
"""Small multi-provider AI assistant starter.

Evidence status:
- request builders and parsers: offline tested
- mock provider: offline tested
- real provider calls: require user-owned credentials and separate verification

This is a single-turn assistant starter, not an autonomous always-running bot.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RequestSpec:
    url: str
    headers: dict[str, str]
    payload: dict[str, Any]


def required_model(provider: str, explicit: str | None) -> str:
    env_name = {
        "openai": "OPENAI_MODEL",
        "anthropic": "ANTHROPIC_MODEL",
        "xai": "XAI_MODEL",
        "gemini": "GEMINI_MODEL",
    }[provider]
    model = explicit or os.environ.get(env_name)
    if not model:
        raise ValueError(f"Model required. Pass --model or set {env_name}.")
    return model


def build_request(provider: str, model: str, prompt: str, system: str = "") -> RequestSpec:
    if provider == "openai":
        payload: dict[str, Any] = {"model": model, "input": prompt}
        if system:
            payload["instructions"] = system
        return RequestSpec(
            "https://api.openai.com/v1/responses",
            {
                "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', '')}",
                "Content-Type": "application/json",
            },
            payload,
        )

    if provider == "anthropic":
        payload = {
            "model": model,
            "max_tokens": 1200,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system
        return RequestSpec(
            "https://api.anthropic.com/v1/messages",
            {
                "x-api-key": os.environ.get("ANTHROPIC_API_KEY", ""),
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            payload,
        )

    if provider == "xai":
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return RequestSpec(
            "https://api.x.ai/v1/chat/completions",
            {
                "Authorization": f"Bearer {os.environ.get('XAI_API_KEY', '')}",
                "Content-Type": "application/json",
            },
            {"model": model, "messages": messages},
        )

    if provider == "gemini":
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        return RequestSpec(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            {
                "x-goog-api-key": os.environ.get("GEMINI_API_KEY", ""),
                "Content-Type": "application/json",
            },
            payload,
        )

    raise ValueError(f"Unsupported provider: {provider}")


def api_key_present(provider: str) -> bool:
    env_name = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "xai": "XAI_API_KEY",
        "gemini": "GEMINI_API_KEY",
    }[provider]
    return bool(os.environ.get(env_name))


def extract_text(provider: str, data: dict[str, Any]) -> str:
    if provider == "openai":
        if isinstance(data.get("output_text"), str):
            return data["output_text"]
        parts: list[str] = []
        for item in data.get("output", []):
            for content in item.get("content", []):
                text = content.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts).strip()

    if provider == "anthropic":
        return "\n".join(
            part.get("text", "")
            for part in data.get("content", [])
            if isinstance(part, dict) and isinstance(part.get("text"), str)
        ).strip()

    if provider == "xai":
        choices = data.get("choices") or []
        if not choices:
            return ""
        return str((choices[0].get("message") or {}).get("content", "")).strip()

    if provider == "gemini":
        candidates = data.get("candidates") or []
        if not candidates:
            return ""
        parts = (candidates[0].get("content") or {}).get("parts") or []
        return "\n".join(
            part.get("text", "")
            for part in parts
            if isinstance(part, dict) and isinstance(part.get("text"), str)
        ).strip()

    raise ValueError(f"Unsupported provider: {provider}")


def call_provider(spec: RequestSpec, timeout: int = 45) -> dict[str, Any]:
    request = urllib.request.Request(
        spec.url,
        data=json.dumps(spec.payload).encode("utf-8"),
        method="POST",
        headers=spec.headers,
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def redacted_headers(headers: dict[str, str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in headers.items():
        if key.lower() in {"authorization", "x-api-key", "x-goog-api-key"}:
            result[key] = "<redacted>"
        else:
            result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Single-turn multi-provider AI assistant starter.")
    parser.add_argument("--provider", choices=["mock", "openai", "anthropic", "xai", "gemini"], required=True)
    parser.add_argument("--model")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--system", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.provider == "mock":
        print(f"[mock] {args.prompt}")
        return 0

    try:
        model = required_model(args.provider, args.model)
        spec = build_request(args.provider, model, args.prompt, args.system)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(json.dumps({
            "provider": args.provider,
            "url": spec.url,
            "headers": redacted_headers(spec.headers),
            "payload": spec.payload,
        }, ensure_ascii=False, indent=2))
        return 0

    if not api_key_present(args.provider):
        print(f"error: API key for {args.provider} is not set", file=sys.stderr)
        return 2

    try:
        data = call_provider(spec)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"provider error {exc.code}: {detail}", file=sys.stderr)
        return 3
    except Exception as exc:
        print(f"request failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 4

    output = extract_text(args.provider, data)
    if not output:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 5

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
