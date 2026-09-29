from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import ai_workbench as workbench


class FakeResponse:
    def __init__(self, data):
        self.raw = data if isinstance(data, bytes) else json.dumps(data).encode()
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self, size):
        return self.raw[:size]


class FakeOpener:
    def __init__(self, data=None, error=None):
        self.data, self.error, self.calls = data, error, []
    def open(self, request, timeout):
        self.calls.append((request, timeout))
        if self.error:
            raise self.error
        return FakeResponse(self.data)


def output(provider):
    if provider in ("openai", "xai"):
        return {"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": "Verified fixture"}]}]}
    if provider == "anthropic":
        return {"stop_reason": "end_turn", "content": [{"type": "text", "text": "Verified fixture"}]}
    return {"candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": "Verified fixture"}]}}]}


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = workbench.load_catalog()
    def test_twelve_original_prompt_cards(self):
        self.assertEqual(len(self.catalog["prompts"]), 12)
    def test_four_assistant_blueprints(self):
        self.assertEqual(len(self.catalog["assistants"]), 4)
    def test_every_example_renders(self):
        for entry in self.catalog["prompts"]:
            with self.subTest(entry=entry["id"]):
                text = workbench.render_prompt(entry, entry["example"])
                self.assertNotRegex(text, workbench.PLACEHOLDER_RE)
                self.assertTrue(entry["acceptance"])
    def test_missing_field_rejected(self):
        with self.assertRaises(workbench.WorkbenchError):
            workbench.render_prompt(self.catalog["prompts"][0], {})
    def test_extra_field_rejected(self):
        entry = self.catalog["prompts"][0]
        with self.assertRaises(workbench.WorkbenchError):
            workbench.render_prompt(entry, dict(entry["example"], secret="not-needed"))
    def test_source_text_not_reinterpreted(self):
        entry = {"instructions": "Source: {{source}}"}
        self.assertEqual(workbench.render_prompt(entry, {"source": "{{other}} ${HOME} {1+1}"}), "Source: {{other}} ${HOME} {1+1}")
    def test_non_string_variable_rejected(self):
        with self.assertRaises(workbench.WorkbenchError):
            workbench.render_prompt({"instructions": "{{x}}"}, {"x": []})
    def test_empty_variable_rejected(self):
        with self.assertRaises(workbench.WorkbenchError):
            workbench.render_prompt({"instructions": "{{x}}"}, {"x": " "})
    def test_large_prompt_rejected(self):
        with self.assertRaises(workbench.WorkbenchError):
            workbench.render_prompt({"instructions": "{{x}}"}, {"x": "a" * 32001})
    def test_five_export_targets(self):
        for target in ("chatgpt", "claude", "gemini", "grok", "skill"):
            for entry in self.catalog["assistants"]:
                text = workbench.assistant_markdown(entry, target)
                self.assertIn("Acceptance checks", text)
                if target == "skill":
                    self.assertTrue(text.startswith("---\n"))
                    self.assertIn("license: MIT", text)
    def test_unknown_assistant_rejected(self):
        with self.assertRaises(workbench.WorkbenchError):
            workbench.lookup(self.catalog, "assistants", "missing")
    def test_catalog_duplicate_rejected(self):
        altered = json.loads(json.dumps(self.catalog))
        altered["prompts"].append(altered["prompts"][0])
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "catalog.json"
            file.write_text(json.dumps(altered))
            with self.assertRaises(workbench.WorkbenchError):
                workbench.load_catalog(file)


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.messages = [{"role": "user", "content": "Hello"}]
    def test_preview_never_calls_transport(self):
        fake = FakeOpener(error=AssertionError("Network forbidden"))
        for provider in workbench.PROVIDERS:
            result = workbench.ask(provider, "test-model", "system", self.messages, opener=fake)
            self.assertFalse(result["network_called"])
        self.assertEqual(fake.calls, [])
    def test_responses_store_disabled(self):
        for provider in ("openai", "xai"):
            _, data = workbench.build_request(provider, "test-model", "policy", self.messages, 1024)
            self.assertIs(data["store"], False)
            self.assertEqual(data["input"][0]["role"], "system")
    def test_anthropic_system_separate(self):
        _, data = workbench.build_request("anthropic", "test-model", "policy", self.messages, 1024)
        self.assertEqual(data["system"], "policy")
        self.assertEqual(data["messages"], self.messages)
    def test_gemini_role_mapping(self):
        history = self.messages + [{"role": "assistant", "content": "Hi"}, {"role": "user", "content": "More"}]
        url, data = workbench.build_request("gemini", "test-model", "policy", history, 1024)
        self.assertTrue(url.endswith("test-model:generateContent"))
        self.assertEqual(data["contents"][1]["role"], "model")
    def test_explicit_model_validation(self):
        for model in ("", "../secret", "x?key=y", "https://untrusted", "x\nheader"):
            with self.subTest(model=model), self.assertRaises(workbench.WorkbenchError):
                workbench.build_request("gemini", model, "policy", self.messages, 1024)
    def test_invalid_provider(self):
        with self.assertRaises(workbench.WorkbenchError):
            workbench.ask("unknown", "test", "policy", self.messages)
    def test_output_budget_bound(self):
        for number in (0, 63, 4097, True):
            with self.assertRaises(workbench.WorkbenchError):
                workbench.build_request("xai", "test", "policy", self.messages, number)
    def test_message_history_validation(self):
        invalid = [[], [{"role": "assistant", "content": "x"}], [{"role": "user", "content": ""}],
                   [{"role": "user", "content": "x", "secret": "y"}], [{"role": "user", "content": "x" * 32001}]]
        for messages in invalid:
            with self.assertRaises(workbench.WorkbenchError):
                workbench.validate_messages(messages)
    def test_live_missing_key_fails_before_network(self):
        fake = FakeOpener()
        with patch.dict(os.environ, {}, clear=True), self.assertRaises(workbench.WorkbenchError):
            workbench.ask("openai", "test", "policy", self.messages, live=True, opener=fake)
        self.assertEqual(fake.calls, [])
    def test_all_adapters_with_mocked_provider(self):
        for provider, (_, env) in workbench.PROVIDERS.items():
            fake = FakeOpener(output(provider))
            with self.subTest(provider=provider), patch.dict(os.environ, {env: "fake-local-test-key"}, clear=True):
                result = workbench.ask(provider, "test-model", "policy", self.messages, live=True, opener=fake)
                self.assertEqual(result["text"], "Verified fixture")
                request, timeout = fake.calls[0]
                self.assertEqual(timeout, 30)
                self.assertEqual(len(fake.calls), 1)
                self.assertNotIn("fake-local-test-key", request.full_url)
                self.assertNotIn("fake-local-test-key", request.data.decode())
    def test_http_error_sanitized_no_retry(self):
        fake = FakeOpener(error=urllib.error.HTTPError("https://api.x.ai/v1/responses", 429, "SECRET_VALUE", {}, None))
        with patch.dict(os.environ, {"XAI_API_KEY": "fake"}):
            with self.assertRaises(workbench.WorkbenchError) as exc:
                workbench.ask("xai", "test", "policy", self.messages, live=True, opener=fake)
        self.assertIn("429", str(exc.exception))
        self.assertNotIn("SECRET_VALUE", str(exc.exception))
        self.assertEqual(len(fake.calls), 1)
    def test_network_failure_no_retry(self):
        fake = FakeOpener(error=urllib.error.URLError("private text"))
        with patch.dict(os.environ, {"XAI_API_KEY": "fake"}), self.assertRaises(workbench.WorkbenchError):
            workbench.ask("xai", "test", "policy", self.messages, live=True, opener=fake)
        self.assertEqual(len(fake.calls), 1)
    def test_redirect_blocked(self):
        with self.assertRaises(workbench.WorkbenchError):
            workbench.NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.example/")
    def test_response_size_bounded(self):
        fake = FakeOpener(b"x" * (workbench.MAX_RESPONSE_BYTES + 1))
        with patch.dict(os.environ, {"XAI_API_KEY": "fake"}), self.assertRaises(workbench.WorkbenchError):
            workbench.ask("xai", "test", "policy", self.messages, live=True, opener=fake)
    def test_invalid_json_response_fails(self):
        fake = FakeOpener(b"not-json")
        with patch.dict(os.environ, {"XAI_API_KEY": "fake"}), self.assertRaises(workbench.WorkbenchError):
            workbench.ask("xai", "test", "policy", self.messages, live=True, opener=fake)
    def test_incomplete_responses_rejected(self):
        for provider, fixture in (("xai", {"status": "incomplete"}), ("anthropic", {"stop_reason": "max_tokens"}),
                                  ("gemini", {"candidates": [{"finishReason": "SAFETY"}]})):
            with self.assertRaises(workbench.WorkbenchError):
                workbench.extract_text(provider, fixture)
    def test_reasoning_not_returned_as_answer(self):
        fixture = {"candidates": [{"finishReason": "STOP", "content": {"parts": [{"thought": True, "text": "private"}, {"text": "answer"}]}}]}
        self.assertEqual(workbench.extract_text("gemini", fixture), "answer")
    def test_cli_renders_outside_repository(self):
        result = subprocess.run([sys.executable, str(ROOT / 'tools/ai_workbench.py'), 'render', 'evidence-brief', '--example'], cwd=ROOT.parent, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('S1', result.stdout)
    def test_chat_keeps_actual_multiturn_history(self):
        with patch('builtins.input', side_effect=['Hello', 'Follow up']), patch.object(workbench, 'ask', side_effect=[{'text': 'Answer'}, {'text': 'Second'}]) as mocked:
            with contextlib.redirect_stdout(io.StringIO()):
                code = workbench.main(['chat', '--provider', 'xai', '--model', 'test', '--live', '--max-turns', '2'])
        self.assertEqual(code, 0)
        self.assertEqual(mocked.call_count, 2)
        self.assertEqual(mocked.call_args.args[3][1], {'role': 'assistant', 'content': 'Answer'})

    def test_build_ui_embeds_catalog_and_blocks_connections(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "catalog.html"
            with contextlib.redirect_stdout(io.StringIO()):
                code = workbench.main(["build-ui", "--output", str(target)])
            page = target.read_text(encoding="utf-8")
            self.assertEqual(code, 0)
            self.assertIn("connect-src 'none'", page)
            self.assertNotIn("__CATALOG__", page)
            self.assertIn("evidence-brief", page)
    def test_build_ui_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "catalog.html"
            target.write_text("keep me")
            with contextlib.redirect_stderr(io.StringIO()):
                code = workbench.main(["build-ui", "--output", str(target)])
            self.assertEqual(code, 2)
            self.assertEqual(target.read_text(), "keep me")
    def test_build_ui_escapes_script_terminators(self):
        altered = json.loads(json.dumps(workbench.load_catalog()))
        altered["title"] = "</script><script>bad()</script>"
        with tempfile.TemporaryDirectory() as tmp, patch.object(workbench, "load_catalog", return_value=altered):
            target = Path(tmp) / "catalog.html"
            with contextlib.redirect_stdout(io.StringIO()):
                code = workbench.main(["build-ui", "--output", str(target)])
            self.assertEqual(code, 0)
            self.assertNotIn("</script><script>bad()", target.read_text(encoding="utf-8"))
    def test_mcp_config_uses_existing_absolute_paths(self):
        result = io.StringIO()
        with contextlib.redirect_stdout(result):
            code = workbench.main(["mcp-config"])
        self.assertEqual(code, 0)
        server = json.loads(result.getvalue())["mcpServers"]["ai-workbench"]
        self.assertTrue(Path(server["command"]).is_absolute())
        self.assertTrue(Path(server["args"][0]).is_file())
    def test_chat_preview_stops_without_fake_model_reply(self):
        with patch("builtins.input", return_value="Hello") as user_input:
            with contextlib.redirect_stdout(io.StringIO()) as result:
                code = workbench.main(["chat", "--provider", "xai", "--model", "demo-model"])
        self.assertEqual(code, 0)
        self.assertEqual(user_input.call_count, 1)
        self.assertIn('"network_called": false', result.getvalue())


if __name__ == '__main__':
    unittest.main()
