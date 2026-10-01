import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FirstRunCheckTests(unittest.TestCase):
    def test_first_run_check(self):
        completed = subprocess.run(
            [sys.executable, "tools/first_run_check.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("FIRST-RUN CHECK: PASS", completed.stdout)
        self.assertIn("API path stays offline by default", completed.stdout)


if __name__ == "__main__":
    unittest.main()
