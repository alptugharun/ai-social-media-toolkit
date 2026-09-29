from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "validate_prompt_library.py"

spec = importlib.util.spec_from_file_location("validate_prompt_library", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class PromptLibraryTests(unittest.TestCase):
    def test_library_has_multiple_prompts(self):
        files = module.prompt_files(ROOT / "prompts")
        self.assertGreaterEqual(len(files), 8)

    def test_all_prompts_pass_contract(self):
        for path in module.prompt_files(ROOT / "prompts"):
            errors = module.validate_prompt(path)
            self.assertEqual(errors, [], f"{path}: {errors}")


if __name__ == "__main__":
    unittest.main()
