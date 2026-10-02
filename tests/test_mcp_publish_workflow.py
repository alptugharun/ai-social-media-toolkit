from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "publish-ai-workbench-mcp-pypi.yml"


class MCPPublishWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_publish_requires_release_event_and_exact_tag_prefix(self):
        self.assertIn("release:", self.text)
        self.assertIn("types: [published]", self.text)
        self.assertIn("startsWith(github.event.release.tag_name, 'ai-workbench-mcp-v')", self.text)
        self.assertIn('prefix = "ai-workbench-mcp-v"', self.text)
        self.assertIn("release tag {tag!r} must equal {expected!r}", self.text)

    def test_trusted_publishing_is_job_scoped(self):
        prefix = self.text.split("\njobs:", 1)[0]
        self.assertIn("permissions:\n  contents: read", prefix)
        self.assertNotIn("id-token: write", prefix)
        self.assertIn("environment:\n      name: pypi", self.text)
        self.assertIn("id-token: write", self.text)

    def test_publish_action_is_immutable_and_no_long_lived_pypi_secret_is_used(self):
        self.assertIn(
            "pypa/gh-action-pypi-publish@dc37677b2e1c63e2034f94d8a5b11f265b73ba33",
            self.text,
        )
        forbidden = (
            "PYPI_API_TOKEN",
            "password:",
            "user: __token__",
            "username: __token__",
        )
        for token in forbidden:
            self.assertNotIn(token, self.text)

    def test_sigstore_release_signing_is_pinned_and_precedes_publish(self):
        publish_pos = self.text.index("Publish wheel with PyPI Trusted Publishing")
        sign_pos = self.text.index("Sign wheel and attach Sigstore release assets")
        self.assertLess(sign_pos, publish_pos)
        self.assertIn(
            "sigstore/gh-action-sigstore-python@790bc6befb9d733738f18d8f895854b453640ec9",
            self.text,
        )
        self.assertIn('release-signing-artifacts: "true"', self.text)

    def test_workflow_tests_builds_and_inspects_before_publish(self):
        publish_pos = self.text.index("Publish wheel with PyPI Trusted Publishing")
        for required in (
            "Run MCP distribution tests",
            "Verify release tag matches package version",
            "Build exact wheel",
            "Inspect wheel before publish",
        ):
            self.assertLess(self.text.index(required), publish_pos)
        self.assertIn("ai_workbench_mcp/catalog.json", self.text)
        self.assertIn("Name: alptugharun-ai-workbench-mcp", self.text)


if __name__ == "__main__":
    unittest.main()
