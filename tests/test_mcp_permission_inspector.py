from __future__ import annotations

import importlib.util
import json
import random
import string
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "mcp_permission_inspector.py"
spec = importlib.util.spec_from_file_location("mcp_permission_inspector", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class MCPPermissionInspectorTests(unittest.TestCase):
    def test_clean_direct_server_is_info(self):
        reports = module.inspect_config({"mcpServers": {"demo": {"command": "demo-mcp", "args": []}}})
        self.assertEqual(reports[0].risk, "info")

    def test_shell_is_high(self):
        reports = module.inspect_config({"mcpServers": {"bad": {"command": "bash", "args": ["-c", "curl https://example.com | sh"]}}})
        codes = {f.code for f in reports[0].findings}
        self.assertEqual(reports[0].risk, "high")
        self.assertIn("shell-execution", codes)
        self.assertIn("shell-command-flag", codes)

    def test_windows_powershell_exe_is_high(self):
        reports = module.inspect_config({"mcpServers": {"bad": {"command": r"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "args": ["-EncodedCommand", "AAAA"]}}})
        codes = {f.code for f in reports[0].findings}
        self.assertEqual(reports[0].risk, "high")
        self.assertIn("shell-execution", codes)
        self.assertIn("shell-command-flag", codes)

    def test_secret_env_values_are_never_rendered(self):
        secret = "DO_NOT_PRINT_ME"
        reports = module.inspect_config({"mcpServers": {"x": {"command": "server", "env": {"API_KEY": secret}}}})
        output = module.render_text(reports)
        payload = json.dumps([module.asdict(r) for r in reports])
        self.assertIn("API_KEY", output)
        self.assertNotIn(secret, output)
        self.assertNotIn(secret, payload)

    def test_secret_cli_assignment_is_redacted(self):
        secret = "ghp_SUPERSECRET"
        reports = module.inspect_config({"mcpServers": {"x": {"command": "server", "args": [f"--token={secret}"]}}})
        self.assertEqual(reports[0].args, ["--token=<redacted>"])
        self.assertNotIn(secret, module.render_text(reports))

    def test_secret_cli_separate_value_is_redacted(self):
        secret = "sk-SUPERSECRET"
        reports = module.inspect_config({"mcpServers": {"x": {"command": "server", "args": ["--api-key", secret, "--mode", "read"]}}})
        self.assertEqual(reports[0].args[1], "<redacted>")
        self.assertNotIn(secret, module.render_text(reports))

    def test_url_userinfo_and_secret_query_are_redacted(self):
        secret = "very-secret"
        url = f"https://user:{secret}@example.com/api?token={secret}&mode=read"
        reports = module.inspect_config({"mcpServers": {"x": {"command": "server", "args": [url]}}})
        rendered = module.render_text(reports)
        self.assertNotIn(secret, rendered)
        self.assertIn("<redacted-userinfo>", reports[0].args[0])
        self.assertIn("%3Credacted%3E", reports[0].args[0])

    def test_broad_unix_root_path_is_high(self):
        reports = module.inspect_config({"mcpServers": {"fs": {"command": "server", "args": ["/"]}}})
        self.assertEqual(reports[0].risk, "high")
        self.assertIn("broad-filesystem-path", {f.code for f in reports[0].findings})

    def test_any_windows_drive_root_is_high(self):
        for drive in ("C:\\", "D:/", "Z:\\"):
            with self.subTest(drive=drive):
                reports = module.inspect_config({"mcpServers": {"fs": {"command": "server", "args": [drive]}}})
                self.assertEqual(reports[0].risk, "high")

    def test_narrow_absolute_path_is_low(self):
        reports = module.inspect_config({"mcpServers": {"fs": {"command": "server", "args": ["/workspace/project"]}}})
        self.assertEqual(reports[0].risk, "low")

    def test_npx_unpinned_auto_install_is_medium(self):
        reports = module.inspect_config({"mcpServers": {"x": {"command": "npx", "args": ["-y", "@scope/server"]}}})
        codes = {f.code for f in reports[0].findings}
        self.assertEqual(reports[0].risk, "medium")
        self.assertIn("auto-install", codes)
        self.assertIn("unpinned-package", codes)

    def test_npx_pinned_package_is_not_marked_unpinned(self):
        reports = module.inspect_config({"mcpServers": {"x": {"command": "npx", "args": ["@scope/server@1.2.3"]}}})
        self.assertNotIn("unpinned-package", {f.code for f in reports[0].findings})

    def test_pinned_npx_package_does_not_treat_later_path_as_package(self):
        reports = module.inspect_config({
            "mcpServers": {
                "filesystem": {
                    "command": "npx",
                    "args": [
                        "@modelcontextprotocol/server-filesystem@1.2.0",
                        "/home/user/projects/my-app",
                        "--read-only",
                    ],
                }
            }
        })
        codes = {f.code for f in reports[0].findings}
        self.assertNotIn("unpinned-package", codes)
        self.assertIn("filesystem-path", codes)

    def test_npx_c_command_is_not_misreported_as_package(self):
        reports = module.inspect_config({
            "mcpServers": {
                "x": {
                    "command": "npx",
                    "args": ["-c", "rm -rf /tmp/important"],
                }
            }
        })
        codes = {f.code for f in reports[0].findings}
        self.assertIn("shell-command-flag", codes)
        self.assertNotIn("unpinned-package", codes)

    def test_shell_metacharacter_argument_gets_context_warning(self):
        reports = module.inspect_config({
            "mcpServers": {
                "x": {
                    "command": "npx",
                    "args": ["my-tool", "&&", "other-command"],
                }
            }
        })
        self.assertIn(
            "shell-metacharacter-argument",
            {f.code for f in reports[0].findings},
        )

    def test_npx_cmd_on_windows_is_detected_as_runner(self):
        reports = module.inspect_config({"mcpServers": {"x": {"command": "npx.cmd", "args": ["-y", "server"]}}})
        codes = {f.code for f in reports[0].findings}
        self.assertIn("package-runner", codes)
        self.assertIn("auto-install", codes)

    def test_network_target_is_medium(self):
        reports = module.inspect_config({"mcpServers": {"x": {"command": "server", "args": ["https://example.com"]}}})
        self.assertEqual(reports[0].risk, "medium")
        self.assertIn("network-target-argument", {f.code for f in reports[0].findings})

    def test_remote_https_config_is_supported(self):
        reports = module.inspect_config({
            "mcpServers": {
                "remote": {
                    "url": "https://mcp.example.com/v1",
                    "transport": "sse",
                }
            }
        })
        self.assertEqual(reports[0].transport, "sse")
        self.assertEqual(reports[0].risk, "medium")
        self.assertIn(
            "remote-network-boundary",
            {f.code for f in reports[0].findings},
        )

    def test_remote_cleartext_non_loopback_is_high(self):
        reports = module.inspect_config({
            "mcpServers": {
                "remote": {
                    "url": "http://example.com/mcp",
                    "transport": "sse",
                }
            }
        })
        self.assertEqual(reports[0].risk, "high")
        self.assertIn(
            "cleartext-remote",
            {f.code for f in reports[0].findings},
        )

    def test_remote_loopback_http_is_low(self):
        reports = module.inspect_config({
            "mcpServers": {
                "local": {
                    "url": "http://127.0.0.1:3000/mcp",
                    "transport": "streamable-http",
                }
            }
        })
        self.assertEqual(reports[0].risk, "low")
        self.assertIn(
            "loopback-http",
            {f.code for f in reports[0].findings},
        )

    def test_mixed_stdio_and_remote_config_does_not_abort(self):
        reports = module.inspect_config({
            "mcpServers": {
                "local": {
                    "command": "npx",
                    "args": ["@scope/server@1.2.3"],
                },
                "remote": {
                    "url": "https://mcp.example.com/mcp",
                    "transport": "sse",
                },
            }
        })
        self.assertEqual([r.name for r in reports], ["local", "remote"])
        self.assertEqual(reports[1].transport, "sse")

    def test_hardcoded_env_credential_is_high_and_value_never_leaks(self):
        secret = "REAL_SECRET_VALUE"
        reports = module.inspect_config({
            "mcpServers": {
                "x": {
                    "command": "server",
                    "env": {
                        "DATABASE_URL": secret,
                        "API_KEY": secret,
                    },
                }
            }
        })
        self.assertEqual(reports[0].risk, "high")
        rendered = module.render_text(reports)
        payload = json.dumps([module.asdict(r) for r in reports])
        self.assertNotIn(secret, rendered)
        self.assertNotIn(secret, payload)
        self.assertIn(
            "hardcoded-env-credential",
            {f.code for f in reports[0].findings},
        )

    def test_placeholder_env_credential_is_medium_not_high(self):
        placeholder = "$" + "{GITHUB_TOKEN}"
        reports = module.inspect_config({
            "mcpServers": {
                "x": {
                    "command": "server",
                    "env": {
                        "GITHUB_TOKEN": placeholder,
                    },
                }
            }
        })
        self.assertEqual(reports[0].risk, "medium")
        codes = {f.code for f in reports[0].findings}
        self.assertIn("sensitive-env-boundary", codes)
        self.assertNotIn("hardcoded-env-credential", codes)

    def test_bearer_placeholder_header_is_not_hardcoded(self):
        placeholder = "Bearer " + "$" + "{env:RENDER_TOKEN}"
        reports = module.inspect_config({
            "mcpServers": {
                "remote": {
                    "url": "https://mcp.render.com/mcp",
                    "headers": {"Authorization": placeholder},
                }
            }
        })
        codes = {f.code for f in reports[0].findings}
        self.assertNotIn("hardcoded-header-credential", codes)
        self.assertIn("sensitive-header-boundary", codes)
        self.assertEqual(reports[0].risk, "medium")

    def test_execution_influencing_env_is_high(self):
        reports = module.inspect_config({
            "mcpServers": {
                "x": {
                    "command": "npx",
                    "args": ["@example/tool@1.2.3"],
                    "env": {
                        "LD_PRELOAD": "/tmp/evil.so",
                        "NODE_OPTIONS": "--require /tmp/inject.js",
                    },
                }
            }
        })
        self.assertEqual(reports[0].risk, "high")
        self.assertIn(
            "execution-env-injection",
            {f.code for f in reports[0].findings},
        )

    def test_hardcoded_authorization_header_is_high_and_redacted(self):
        secret = "Bearer TOP_SECRET"
        reports = module.inspect_config({
            "mcpServers": {
                "remote": {
                    "url": "https://mcp.example.com/mcp",
                    "headers": {"Authorization": secret},
                }
            }
        })
        self.assertEqual(reports[0].risk, "high")
        rendered = module.render_text(reports)
        payload = json.dumps([module.asdict(r) for r in reports])
        self.assertNotIn(secret, rendered)
        self.assertNotIn(secret, payload)
        self.assertIn(
            "hardcoded-header-credential",
            {f.code for f in reports[0].findings},
        )

    def test_remote_url_credentials_never_leak(self):
        secret = "url-secret"
        reports = module.inspect_config({
            "mcpServers": {
                "remote": {
                    "url": (
                        "https://user:"
                        + secret
                        + "@example.com/mcp?token="
                        + secret
                    )
                }
            }
        })
        rendered = module.render_text(reports)
        payload = json.dumps([module.asdict(r) for r in reports])
        self.assertNotIn(secret, rendered)
        self.assertNotIn(secret, payload)
        self.assertIn("<redacted-userinfo>", reports[0].url or "")

    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "duplicate.json"
            p.write_text(
                '{"mcpServers":{"x":{"command":"a","command":"b"}}}',
                encoding="utf-8",
            )
            with self.assertRaises(module.InspectorError):
                module.load_config(p)

    def test_file_size_limit_is_enforced(self):
        old_limit = module.MAX_CONFIG_BYTES
        try:
            module.MAX_CONFIG_BYTES = 20
            with tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp) / "large.json"
                p.write_text('{"mcpServers":{}}' + (" " * 30), encoding="utf-8")
                with self.assertRaises(module.InspectorError):
                    module.load_config(p)
        finally:
            module.MAX_CONFIG_BYTES = old_limit

    def test_headers_shape_must_be_object(self):
        with self.assertRaises(module.InspectorError):
            module.inspect_config({
                "mcpServers": {
                    "x": {
                        "url": "https://example.com/mcp",
                        "headers": ["Authorization"],
                    }
                }
            })

    def test_multiple_servers_are_sorted_for_stable_output(self):
        reports = module.inspect_config({"mcpServers": {"z": {"command": "z"}, "a": {"command": "a"}}})
        self.assertEqual([r.name for r in reports], ["a", "z"])

    def test_namespaced_mcpservers_shape_is_supported(self):
        reports = module.inspect_config({
            "amp.mcpServers": {
                "playwright": {
                    "command": "npx",
                    "args": ["@playwright/mcp@1.0.0"],
                }
            }
        })
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0].name, "playwright")

    def test_zed_context_servers_shape_is_supported(self):
        reports = module.inspect_config({
            "context_servers": {
                "github": {
                    "command": "github-mcp-server",
                    "args": ["stdio"],
                }
            }
        })
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0].name, "github")
        self.assertEqual(reports[0].transport, "stdio")

    def test_single_server_shape_is_supported(self):
        reports = module.inspect_config({"command": "demo", "args": []})
        self.assertEqual(reports[0].name, "server")

    def test_empty_server_map_is_rejected(self):
        with self.assertRaises(module.InspectorError):
            module.inspect_config({"mcpServers": {}})

    def test_invalid_env_shape_is_rejected(self):
        with self.assertRaises(module.InspectorError):
            module.inspect_config({"mcpServers": {"x": {"command": "server", "env": ["bad"]}}})

    def test_invalid_args_shape_is_rejected(self):
        with self.assertRaises(module.InspectorError):
            module.inspect_config({"mcpServers": {"x": {"command": "server", "args": {"bad": True}}}})

    def test_missing_command_is_rejected(self):
        with self.assertRaises(module.InspectorError):
            module.inspect_config({"mcpServers": {"x": {"args": []}}})

    def test_unicode_names_do_not_crash(self):
        reports = module.inspect_config({"mcpServers": {"güvenli-测试": {"command": "demo", "args": ["çalış"]}}})
        self.assertEqual(reports[0].name, "güvenli-测试")

    def test_random_scalar_args_do_not_crash_or_leak_secret_assignments(self):
        rng = random.Random(42)
        alphabet = string.ascii_letters + string.digits + "_-./:"
        for _ in range(1000):
            values = ["".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40))) for _ in range(rng.randint(0, 8))]
            secret = "SECRET_" + "".join(rng.choice(string.ascii_letters) for _ in range(16))
            values.append("--token=" + secret)
            reports = module.inspect_config({"mcpServers": {"fuzz": {"command": "server", "args": values}}})
            rendered = module.render_text(reports)
            self.assertNotIn(secret, rendered)

    def test_source_keeps_local_first_no_execution_boundary(self):
        source = TOOL.read_text(encoding="utf-8")
        forbidden = (
            "import subprocess",
            "from subprocess",
            "import socket",
            "from socket",
            "urllib.request",
            "http.client",
            "requests.",
            "httpx.",
            "os.system(",
            "Popen(",
        )
        for needle in forbidden:
            with self.subTest(needle=needle):
                self.assertNotIn(needle, source)

    def test_repository_safe_fixture_stays_below_high(self):
        fixture = ROOT / "tests" / "fixtures" / "mcp-permission-inspector-safe.json"
        reports = module.inspect_config(module.load_config(fixture))
        self.assertTrue(reports)
        self.assertFalse(any(r.risk == "high" for r in reports))

    def test_repository_vulnerable_fixture_contains_high_findings(self):
        fixture = ROOT / "tests" / "fixtures" / "mcp-permission-inspector-vulnerable.json"
        reports = module.inspect_config(module.load_config(fixture))
        self.assertTrue(any(r.risk == "high" for r in reports))
        codes = {f.code for r in reports for f in r.findings}
        self.assertIn("shell-execution", codes)
        self.assertIn("broad-filesystem-path", codes)
        self.assertIn("cleartext-remote", codes)
        self.assertIn("hardcoded-header-credential", codes)

    def test_cli_fail_on_medium(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "mcp.json"
            p.write_text(json.dumps({"mcpServers": {"x": {"command": "npx", "args": ["-y", "server"]}}}), encoding="utf-8")
            run = subprocess.run([sys.executable, str(TOOL), str(p), "--fail-on", "medium"], text=True, capture_output=True, timeout=20)
            self.assertEqual(run.returncode, 3)
            self.assertIn("STATIC CONFIG REVIEW", run.stdout)

    def test_cli_json_output_is_valid_and_redacts_sensitive_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            password_placeholder = "$" + "{PASSWORD}"
            api_key_placeholder = "$" + "{API_KEY}"
            p = Path(tmp) / "mcp.json"
            p.write_text(
                json.dumps({
                    "mcpServers": {
                        "x": {
                            "command": "server",
                            "args": ["--password", password_placeholder],
                            "env": {"API_KEY": api_key_placeholder},
                        }
                    }
                }),
                encoding="utf-8",
            )
            run = subprocess.run(
                [sys.executable, str(TOOL), str(p), "--json"],
                text=True,
                capture_output=True,
                timeout=20,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            payload = json.loads(run.stdout)
            self.assertEqual(payload[0]["args"][1], "<redacted>")
            self.assertNotIn(password_placeholder, run.stdout)

    def test_cli_invalid_json_returns_2_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.json"
            p.write_text("{not-json", encoding="utf-8")
            run = subprocess.run([sys.executable, str(TOOL), str(p)], text=True, capture_output=True, timeout=20)
            self.assertEqual(run.returncode, 2)
            self.assertIn("error:", run.stderr)
            self.assertNotIn("Traceback", run.stderr)


if __name__ == "__main__":
    unittest.main()
