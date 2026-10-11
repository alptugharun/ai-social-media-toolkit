#!/usr/bin/env python3
"""Read-only MCP stdio example for the original AI Workbench catalog.

Implements initialize, initialized, ping, tools/list and tools/call. No web,
provider calls, writes, shell execution or account access. Local protocol tests
are not proof of compatibility with every MCP host. MIT, Alptuğ Harun, 2026.
"""
from __future__ import annotations

import json
import sys
from typing import Any

from ai_workbench import WorkbenchError, assistant_markdown, load_catalog, lookup, render_prompt

VERSIONS = ("2025-06-18", "2025-03-26")
LINE_LIMIT = 128000
TOOLS = [
    {"name": "list_prompts", "description": "Use this first to discover valid prompt and assistant IDs in the original local catalog before calling render_prompt or get_assistant. Returns catalog metadata only; no network or provider call.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
     "annotations": {"title": "List Prompt Catalog", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}},
    {"name": "render_prompt", "description": "Use after list_prompts when you want one prompt template filled with the supplied string variables. Returns plain text only; use get_assistant instead for a reusable assistant blueprint. No AI model or provider is called.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string"},
                     "variables": {"type": "object", "additionalProperties": {"type": "string"}}},
                     "required": ["id", "variables"], "additionalProperties": False},
     "annotations": {"title": "Render Prompt Template", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}},
    {"name": "get_assistant", "description": "Use after list_prompts when you want one reusable assistant instruction blueprint. Use render_prompt instead for a single filled prompt. Returns local text only; no installation, publishing, provider call, or account change.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}},
                     "required": ["id"], "additionalProperties": False},
     "annotations": {"title": "Get Assistant Blueprint", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}},
]


def failure(rpc_id, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": rpc_id, "error": {"code": code, "message": message}}


class CatalogServer:
    def __init__(self, catalog: dict):
        self.catalog = catalog
        self.initialized = False
        self.ready = False

    def call_tool(self, name: str, arguments: Any) -> str:
        if not isinstance(arguments, dict):
            raise WorkbenchError("Tool arguments must be an object.")
        if name == "list_prompts" and not arguments:
            entries = {group: [{"id": x["id"], "title": x["title"], "purpose": x["purpose"]}
                               for x in self.catalog[group]] for group in ("prompts", "assistants")}
            return json.dumps(entries, ensure_ascii=False)
        if name == "render_prompt" and set(arguments) == {"id", "variables"} and isinstance(arguments["id"], str):
            return render_prompt(lookup(self.catalog, "prompts", arguments["id"]), arguments["variables"])
        if name == "get_assistant" and set(arguments) == {"id"} and isinstance(arguments["id"], str):
            return assistant_markdown(lookup(self.catalog, "assistants", arguments["id"]), "grok")
        raise WorkbenchError("Unknown tool or invalid arguments.")

    def handle(self, message: Any) -> dict | None:
        if not isinstance(message, dict):
            return failure(None, -32600, "Expected a JSON-RPC object; batches are not supported.")
        rpc_id = message.get("id")
        if message.get("jsonrpc") != "2.0" or not isinstance(message.get("method"), str):
            return failure(None, -32600, "Invalid JSON-RPC request.")
        if "id" in message and (type(rpc_id) not in (str, int)):
            return failure(None, -32600, "Request ID must be a string or integer.")
        method = message["method"]
        if "id" not in message:
            if method == "notifications/initialized" and self.initialized:
                self.ready = True
            return None  # no response to notifications, including cancellation
        params = message.get("params", {})
        if not isinstance(params, dict):
            return failure(rpc_id, -32602, "params must be an object.")
        if method == "initialize":
            if self.initialized:
                return failure(rpc_id, -32600, "Already initialized.")
            if not isinstance(params.get("protocolVersion"), str):
                return failure(rpc_id, -32602, "protocolVersion is required.")
            requested = params["protocolVersion"]
            version = requested if requested in VERSIONS else VERSIONS[0]
            self.initialized = True
            result = {"protocolVersion": version, "capabilities": {"tools": {"listChanged": False}},
                      "serverInfo": {"name": "alptugharun-ai-workbench", "version": "0.1.0"},
                      "instructions": "Read-only local catalog. Call list_prompts first to discover valid IDs. Use render_prompt for one filled prompt and get_assistant for a reusable assistant blueprint. No network/provider call, file write, or account modification."}
        elif method == "ping":
            result = {}
        elif not self.ready:
            return failure(rpc_id, -32600, "Complete initialization before using catalog tools.")
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            if not isinstance(params.get("name"), str):
                return failure(rpc_id, -32602, "Tool name is required.")
            try:
                text = self.call_tool(params["name"], params.get("arguments", {}))
                result = {"content": [{"type": "text", "text": text}], "isError": False}
            except WorkbenchError as exc:
                result = {"content": [{"type": "text", "text": str(exc)}], "isError": True}
        else:
            return failure(rpc_id, -32601, "Method not supported by this read-only example.")
        return {"jsonrpc": "2.0", "id": rpc_id, "result": result}


def serve(input_stream, output_stream, catalog: dict) -> int:
    server = CatalogServer(catalog)
    while True:
        line = input_stream.readline(LINE_LIMIT + 1)
        if not line:
            return 0
        if len(line) > LINE_LIMIT:
            print(json.dumps(failure(None, -32600, "Request line exceeds limit; closing transport.")), file=output_stream, flush=True)
            return 2
        if not line.strip():
            continue
        try:
            response = server.handle(json.loads(line))
        except json.JSONDecodeError:
            response = failure(None, -32700, "Invalid JSON.")
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), file=output_stream, flush=True)


if __name__ == "__main__":
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        raise SystemExit(serve(sys.stdin, sys.stdout, load_catalog()))
    except (WorkbenchError, OSError, UnicodeError):
        print("Cannot load the local catalog; no tools started.", file=sys.stderr)
        raise SystemExit(2)
    except KeyboardInterrupt:
        raise SystemExit(130)
