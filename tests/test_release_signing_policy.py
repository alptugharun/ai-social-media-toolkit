from pathlib import Path
import os
import subprocess
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "sign-release-assets.yml"


class ReleaseSigningPolicyTests(unittest.TestCase):
    def setUp(self):
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_signing_workflow_uses_oidc_and_narrow_write_permission(self):
        self.assertIn("id-token: write", self.text)
        self.assertIn("contents: write", self.text)
        self.assertIn("permissions:\n  contents: read", self.text)

    def test_sigstore_action_is_immutable_and_release_assets_are_preserved(self):
        self.assertIn(
            "sigstore/gh-action-sigstore-python@790bc6befb9d733738f18d8f895854b453640ec9",
            self.text,
        )
        self.assertIn("--pattern '*.zip'", self.text)
        self.assertIn("--pattern 'SHA256SUMS.txt'", self.text)
        self.assertIn("*.sigstore.json", self.text)
        self.assertNotIn("--clobber", self.text)
        self.assertIn('existing_assets="$(gh release view "$TAG"', self.text)
        self.assertIn("existing_count", self.text)

    def test_workflow_supports_current_and_future_releases(self):
        self.assertIn("release:\n    types: [published]", self.text)
        self.assertIn("workflow_dispatch:", self.text)
        self.assertIn("github.event.release.tag_name", self.text)


    def run_upload_step(self, existing, bundles=("a.zip.sigstore.json", "SHA256SUMS.txt.sigstore.json")):
        snippet = self.text.split("      - name: Upload Sigstore bundles to the same release\n", 1)[1]
        snippet = snippet.split("      - name: Verify public signature assets exist\n", 1)[0]
        self.assertIn("        run: |\n", snippet)
        script = textwrap.dedent(snippet.split("        run: |\n", 1)[1])
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            (base / "dist/signing").mkdir(parents=True)
            for name in bundles:
                (base / "dist/signing" / name).write_text("signed", encoding="utf-8")
            (base / "mockbin").mkdir()
            gh = base / "mockbin/gh"
            gh.write_text(
                '#!/usr/bin/env bash\nset -euo pipefail\n'
                'if [[ "$1 $2" == "release view" ]]; then\n'
                '  cat "$GH_TEST_EXISTING"\n'
                'elif [[ "$1 $2" == "release upload" ]]; then\n'
                '  printf "%s\n" "$*" >> "$GH_TEST_UPLOADS"\n'
                'else\n  exit 64\nfi\n', encoding="utf-8",
            )
            gh.chmod(0o755)
            (base / "existing.txt").write_text("\n".join(existing), encoding="utf-8")
            env = {**os.environ,
                   "PATH": str(base / "mockbin") + os.pathsep + os.environ["PATH"],
                   "GH_TEST_EXISTING": str(base / "existing.txt"),
                   "GH_TEST_UPLOADS": str(base / "uploads.txt"),
                   "TAG": "v0.3.0-alpha.1", "GITHUB_REPOSITORY": "alptugharun/ai-social-media-toolkit"}
            result = subprocess.run(["bash", "-c", script], cwd=base, env=env,
                                    capture_output=True, text=True, timeout=10)
            uploads = (base / "uploads.txt")
            log = uploads.read_text(encoding="utf-8") if uploads.exists() else ""
            return result, log

    @unittest.skipIf(os.name == "nt", "release upload snippet is Bash-only and runs on Ubuntu in GitHub Actions")
    def test_initial_signing_uploads_once_without_replace(self):
        result, log = self.run_upload_step([])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(log.splitlines()), 1)
        self.assertNotIn("--clobber", log)

    @unittest.skipIf(os.name == "nt", "release upload snippet is Bash-only and runs on Ubuntu in GitHub Actions")
    def test_rerun_preserves_all_existing_bundles(self):
        result, log = self.run_upload_step(["a.zip.sigstore.json", "SHA256SUMS.txt.sigstore.json"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("keeping published provenance unchanged", result.stdout)
        self.assertEqual(log, "")

    @unittest.skipIf(os.name == "nt", "release upload snippet is Bash-only and runs on Ubuntu in GitHub Actions")
    def test_partial_signatures_fail_closed_without_upload(self):
        result, log = self.run_upload_step(["a.zip.sigstore.json"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("refusing a partial re-sign", result.stdout)
        self.assertEqual(log, "")

    @unittest.skipIf(os.name == "nt", "release upload snippet is Bash-only and runs on Ubuntu in GitHub Actions")
    def test_no_generated_bundles_fails_closed(self):
        result, log = self.run_upload_step([], bundles=())
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(log, "")



if __name__ == "__main__":
    unittest.main()
