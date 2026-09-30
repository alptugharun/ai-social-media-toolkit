from __future__ import annotations

import csv
import importlib.util
import io
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_tool(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SIGNAL = load_tool("signal2content_score")
OUTLIER = load_tool("outlier_score")
DEMO = load_tool("two_minute_demo")
TOOLS = (SIGNAL, OUTLIER)


class CreatorCsvTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "input.csv"

    def make_csv(self, module, rows=None, header=None, encoding="utf-8"):
        if rows is None:
            rows = [["Example", "80", "80", "80", "80", "80", "20"]] if module is SIGNAL else [
                ["instagram", "001", "100", "10", "2", "3", "4"]]
        with self.path.open("w", encoding=encoding, newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(header if header is not None else module.INPUT_COLUMNS)
            writer.writerows(rows)
        return self.path

    def cli(self, module, *args, path=None):
        return subprocess.run(
            [sys.executable, str(ROOT / "tools" / (module.__name__ + ".py")), str(path or self.path), *args],
            cwd=ROOT, text=True, encoding="utf-8", capture_output=True, timeout=15,
        )

    def assert_bad(self, module, expected):
        for flags in ((), ("--validate-only",)):
            result = self.cli(module, *flags)
            self.assertEqual(result.returncode, 2, result)
            self.assertEqual(result.stdout, "")
            self.assertIn(expected, result.stderr)
            self.assertIn(str(self.path), result.stderr)
            self.assertIn(module.INPUT_EXAMPLE, result.stderr)
            self.assertIn(module.INPUT_CONTRACT, result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_known_signal_scores_unchanged(self):
        result = self.cli(SIGNAL, "--top", "3", path=ROOT / SIGNAL.INPUT_EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(csv.reader(io.StringIO(result.stdout))), [
            ["rank", "name", "score"], ["1", "Pinterest seasonal visual series", "83.05"],
            ["2", "AI before-after workflow", "79.00"], ["3", "Creator teardown carousel", "74.10"]])

    def test_known_outlier_scores_unchanged(self):
        result = self.cli(OUTLIER, "--top", "3", path=ROOT / OUTLIER.INPUT_EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(csv.reader(io.StringIO(result.stdout))), [
            ["rank", "platform", "post_id", "outlier_score", "view_multiple", "engagement_multiple"],
            ["1", "instagram", "reel-004", "6.73", "3.94", "8.91"],
            ["2", "instagram", "reel-002", "1.11", "1.1", "1.11"],
            ["3", "instagram", "reel-005", "1.0", "1.0", "1.0"]])

    def test_validate_only_does_not_change_input(self):
        for module in TOOLS:
            self.make_csv(module)
            before = self.path.read_bytes()
            result = self.cli(module, "--validate-only")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("1 data rows", result.stdout)
            self.assertNotIn("rank,", result.stdout)
            self.assertEqual(self.path.read_bytes(), before)

    def test_bom_turkish_crlf_and_quoted_text(self):
        text = 'İçerik, "özet"\nikinci satır'
        for module in TOOLS:
            row = [text, 80, 80, 80, 80, 80, 20] if module is SIGNAL else [text, "001", 100, 10, 2, 3, 4]
            self.make_csv(module, [row], encoding="utf-8-sig")
            self.assertTrue(self.path.read_bytes().startswith(b"\xef\xbb\xbf"))
            self.assertIn(b"\r\n", self.path.read_bytes())
            records = module.load_rows(self.path)
            self.assertEqual(records[0][module.INPUT_COLUMNS[0]], text)
            result = self.cli(module)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = list(csv.DictReader(io.StringIO(result.stdout)))
            self.assertEqual(output[0][module.INPUT_COLUMNS[0]], text)

    def test_identifier_leading_zeroes_are_preserved(self):
        self.make_csv(OUTLIER)
        self.assertEqual(OUTLIER.load_rows(self.path)[0]["post_id"], "001")
        self.assertIn(",001,", self.cli(OUTLIER).stdout)

    def test_reordered_columns_and_named_extras(self):
        for module in TOOLS:
            self.make_csv(module)
            original = module.load_rows(self.path)[0]
            header = list(reversed(module.INPUT_COLUMNS)) + ["date_note"]
            self.make_csv(module, [[original[key] for key in reversed(module.INPUT_COLUMNS)] + ["not parsed as a date"]], header)
            self.assertEqual(module.load_rows(self.path)[0][module.INPUT_COLUMNS[0]], original[module.INPUT_COLUMNS[0]])
            self.assertEqual(self.cli(module).returncode, 0)

    def test_missing_columns(self):
        for module in TOOLS:
            self.path.write_text("name\nExample\n")
            self.assert_bad(module, "Missing columns")

    def test_duplicate_headers(self):
        for module in TOOLS:
            self.make_csv(module, [], list(module.INPUT_COLUMNS) + [module.INPUT_COLUMNS[0]])
            self.assert_bad(module, "duplicate column")

    def test_empty_header_name(self):
        for module in TOOLS:
            self.make_csv(module, [], list(module.INPUT_COLUMNS) + [""])
            self.assert_bad(module, "must not be empty")

    def test_empty_file(self):
        for module in TOOLS:
            self.path.write_text("")
            self.assert_bad(module, "no header")

    def test_header_only(self):
        for module in TOOLS:
            self.make_csv(module, [])
            self.assert_bad(module, "no data rows")

    def test_short_and_extra_width_records(self):
        for module in TOOLS:
            for values in (["x", "1"], ["x"] * 8):
                self.make_csv(module, [values])
                self.assert_bad(module, "data record 1: row width")

    def test_blank_identifiers(self):
        self.make_csv(SIGNAL, [[" ", 1, 1, 1, 1, 1, 1]])
        self.assert_bad(SIGNAL, "name must not be blank")
        for platform, post in [(" ", "001"), ("instagram", " ")]:
            self.make_csv(OUTLIER, [[platform, post, 1, 1, 1, 1, 1]])
            self.assert_bad(OUTLIER, "must not be blank")

    def test_invalid_numbers_fail_instead_of_becoming_zero(self):
        for module in TOOLS:
            for bad in ("N/A", "", "12K", "1,000", "82%", "82,5", "nan", "inf", "-inf", "-1"):
                with self.subTest(tool=module.__name__, value=bad):
                    row = ["Example", bad, 80, 80, 80, 80, 20] if module is SIGNAL else ["instagram", "001", bad, 10, 2, 3, 4]
                    self.make_csv(module, [row])
                    self.assert_bad(module, "evidence_strength" if module is SIGNAL else "views")

    def test_opportunity_out_of_range(self):
        self.make_csv(SIGNAL, [["Example", 101, 80, 80, 80, 80, 20]])
        self.assert_bad(SIGNAL, "between 0 and 100")

    def test_zero_is_valid_but_not_missing(self):
        self.make_csv(OUTLIER, [["instagram", "001", 0, 0, 0, 0, 0]])
        result = self.cli(OUTLIER)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(",0.0,0.0,0.0", result.stdout)

    def test_decimal_and_finite_scientific_notation(self):
        self.make_csv(SIGNAL, [["Example", "8e1", "80.5", 80, 80, 80, 20]])
        self.assertEqual(self.cli(SIGNAL).returncode, 0)
        self.make_csv(OUTLIER, [["instagram", "001", "1e2", "10.5", 2, 3, 4]])
        self.assertEqual(self.cli(OUTLIER).returncode, 0)

    def test_wrong_separator_rejected(self):
        for module in TOOLS:
            for delimiter in (";", "\t"):
                self.path.write_text(delimiter.join(module.INPUT_COLUMNS) + "\n")
                self.assert_bad(module, "comma-delimited CSV")

    def test_unclosed_quote_rejected(self):
        for module in TOOLS:
            self.path.write_text(",".join(module.INPUT_COLUMNS) + '\n"unterminated')
            self.assert_bad(module, "unexpected end of data")

    def test_missing_file_error_has_next_step(self):
        self.assertFalse(self.path.exists())
        for module in TOOLS:
            self.assert_bad(module, "error:")

    def test_extreme_values_do_not_print_infinity(self):
        self.make_csv(OUTLIER, [["instagram", "001", "1e308", 1, 1, 1, 1], ["instagram", "002", "1e308", 1, 1, 1, 1]])
        result = self.cli(OUTLIER)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_doc_headers_match_real_parser(self):
        contract = (ROOT / "docs/CSV-INPUTS.md").read_text(encoding="utf-8")
        for module in TOOLS:
            self.assertIn(",".join(module.INPUT_COLUMNS), contract)
            self.assertIn(module.INPUT_EXAMPLE, contract)
            anchor = module.INPUT_CONTRACT.split("#")[1]
            self.assertIn("## " + anchor.replace("-", " ").capitalize(), contract)

    def test_demo_has_contract_commands_after_each_proof(self):
        report = DEMO.render()
        for module in TOOLS:
            self.assertIn(module.INPUT_EXAMPLE, report)
            self.assertIn(module.INPUT_CONTRACT, report)
            self.assertIn(",".join(module.INPUT_COLUMNS), report)
            self.assertIn("--validate-only", report)
        self.assertLess(report.index(SIGNAL.INPUT_CONTRACT), report.index("## Proof 2"))
        self.assertLess(report.index(OUTLIER.INPUT_CONTRACT), report.index("## What this proves"))

    def test_demo_copy_and_validate_commands_execute_without_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            checkout = Path(tmp) / "checkout"
            (checkout / "examples").mkdir(parents=True)
            for module, filename in ((SIGNAL, "opportunities.csv"), (OUTLIER, "posts.csv")):
                shutil.copyfile(ROOT / module.INPUT_EXAMPLE, checkout / module.INPUT_EXAMPLE)
                lines = DEMO.own_data_steps(module.INPUT_EXAMPLE, module.INPUT_CONTRACT,
                                            ",".join(module.INPUT_COLUMNS), module.__name__ + ".py", filename)
                command = next(line for line in lines if line.startswith("python -c"))
                args = shlex.split(command); args[0] = sys.executable
                first = subprocess.run(args, cwd=checkout, capture_output=True, timeout=15)
                self.assertEqual(first.returncode, 0, first.stderr)
                target = Path(tmp) / filename
                self.assertEqual(target.read_bytes(), (ROOT / module.INPUT_EXAMPLE).read_bytes())
                self.assertEqual(self.cli(module, "--validate-only", path=target).returncode, 0)
                self.assertEqual(self.cli(module, "--top", "3", path=target).returncode, 0)
                second = subprocess.run(args, cwd=checkout, capture_output=True, timeout=15)
                self.assertNotEqual(second.returncode, 0)
                self.assertEqual(target.read_bytes(), (ROOT / module.INPUT_EXAMPLE).read_bytes())

    def test_workflow_output_is_actual_analyzer_output(self):
        doc = (ROOT / "examples/workflows/reels-from-outlier.md").read_text(encoding="utf-8")
        block = re.search(r"```csv\n(.*?)\n```", doc, re.S).group(1)
        result = self.cli(OUTLIER, "--top", "3", path=ROOT / OUTLIER.INPUT_EXAMPLE)
        self.assertEqual(result.stdout.strip(), block)
        self.assertIn("HOLD", doc)
        self.assertIn("synthetic", doc)

    def test_minimum_examples_in_contract_are_valid(self):
        doc = (ROOT / "docs/CSV-INPUTS.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```csv\n(.*?)\n```", doc, re.S)
        for module in TOOLS:
            example = next(block for block in blocks if block.startswith(",".join(module.INPUT_COLUMNS)) and "\n" in block)
            self.path.write_text(example + "\n", encoding="utf-8")
            self.assertEqual(self.cli(module).returncode, 0)

    def test_runtime_template_does_not_claim_execution(self):
        text = (ROOT / "docs/RUNTIME-VERIFICATION-TEMPLATE.md").read_text(encoding="utf-8")
        for status in ("PASS", "FAIL", "BLOCKED", "NOT TESTED"):
            self.assertIn(status, text)
        self.assertIn("not evidence", text.lower())


if __name__ == "__main__":
    unittest.main()
