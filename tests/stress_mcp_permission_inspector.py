from __future__ import annotations

import importlib.util
import json
import random
import string
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "mcp_permission_inspector.py"
spec = importlib.util.spec_from_file_location("mcp_permission_inspector_stress", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def main() -> int:
    rng = random.Random(20261005)
    alphabet = string.ascii_letters + string.digits + "_-./:@?=&"
    commands = [
        "server",
        "npx",
        "npx.cmd",
        "uvx",
        "pipx",
        "bash",
        "bash.exe",
        "sh",
        "cmd.exe",
        "powershell.exe",
        "pwsh.exe",
    ]

    counts = {"info": 0, "low": 0, "medium": 0, "high": 0}
    start = time.perf_counter()

    for i in range(20_000):
        command = rng.choice(commands)
        args = [
            "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 60)))
            for _ in range(rng.randint(0, 10))
        ]
        secret = f"SENTINEL_SECRET_{i:05d}"
        mode = i % 8

        if mode == 0:
            args += ["--token=" + secret]
        elif mode == 1:
            args += ["--api-key", secret]
        elif mode == 2:
            args += [
                "https://user:"
                + secret
                + "@example.com/api?token="
                + secret
                + "&mode=read"
            ]
        elif mode == 3:
            args += ["/"]
        elif mode == 4:
            args += ["D:\\"]
        elif mode == 5:
            args += ["@scope/server"]
        elif mode == 6:
            args += ["@scope/server@1.2.3", "/workspace/project"]
        else:
            args += ["https://example.com/service"]

        env = {"API_KEY": secret} if i % 7 == 0 else {}
        headers = {"Authorization": secret} if i % 11 == 0 else {}
        raw = {"command": command, "args": args, "env": env, "headers": headers}

        reports = module.inspect_config({"mcpServers": {"fuzz": raw}})
        rendered = module.render_text(reports)
        payload = json.dumps([module.asdict(r) for r in reports], ensure_ascii=False)
        if secret in rendered or secret in payload:
            raise AssertionError(f"secret leak at fuzz case {i}")

        second = module.render_text(
            module.inspect_config({"mcpServers": {"fuzz": raw}})
        )
        if rendered != second:
            raise AssertionError(f"non-deterministic output at fuzz case {i}")

        counts[reports[0].risk] += 1

    servers = {
        f"srv-{2500 - i:04d}": {
            "command": "server",
            "args": [f"/workspace/project-{i}", "--mode", "read"],
        }
        for i in range(2500)
    }
    large_start = time.perf_counter()
    reports = module.inspect_config({"mcpServers": servers})
    large_seconds = time.perf_counter() - large_start

    if len(reports) != 2500:
        raise AssertionError("large config lost servers")
    if [r.name for r in reports] != sorted(r.name for r in reports):
        raise AssertionError("large config output is not deterministic")
    if large_seconds >= 10:
        raise AssertionError(f"large config too slow: {large_seconds:.3f}s")

    print(
        json.dumps(
            {
                "fuzz_cases": 20_000,
                "secret_leaks": 0,
                "risk_counts": counts,
                "large_servers": 2500,
                "large_seconds": round(large_seconds, 3),
                "total_seconds": round(time.perf_counter() - start, 3),
                "status": "PASS",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
