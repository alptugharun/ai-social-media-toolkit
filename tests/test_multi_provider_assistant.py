from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "multi_provider_assistant.py"

spec = importlib.util.spec_from_file_location("multi_provider_assistant", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class MultiProviderAssistantTests(unittest.TestCase):
    def test_openai_request(self):
        spec = module.build_request("openai", "example-model", "hello", "be concise")
        self.assertTrue(spec.url.endswith("/v1/responses"))
        self.assertEqual(spec.payload["model"], "example-model")
        self.assertEqual(spec.payload["instructions"], "be concise")

    def test_anthropic_extract(self):
        data = {"content": [{"type": "text", "text": "hello"}]}
        self.assertEqual(module.extract_text("anthropic", data), "hello")

    def test_xai_extract(self):
        data = {"choices": [{"message": {"content": "hello"}}]}
        self.assertEqual(module.extract_text("xai", data), "hello")

    def test_gemini_extract(self):
        data = {"candidates": [{"content": {"parts": [{"text": "hello"}]}}]}
        self.assertEqual(module.extract_text("gemini", data), "hello")

    def test_redacts_credentials(self):
        headers = {"Authorization": "Bearer secret", "Content-Type": "application/json"}
        redacted = module.redacted_headers(headers)
        self.assertEqual(redacted["Authorization"], "<redacted>")
        self.assertEqual(redacted["Content-Type"], "application/json")


if __name__ == "__main__":
    unittest.main()
