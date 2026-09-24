from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Diagnosis:
    workflow: str
    run_id: str
    run_attempt: int
    classification: str
    confidence: str
    retryable: bool
    probe_retry_safe: bool
    fingerprint: str
    summary: str
    evidence: list[str]


PATTERNS: tuple[tuple[str, tuple[str, ...], bool, str, str], ...] = (
    (
        "github-api-403",
        (
            r"GitHub API error:?\s*403\b",
            r"\b403 Forbidden\b",
            r"secondary rate limit",
            r"API rate limit exceeded",
            r"rate limit exceeded",
        ),
        True,
        "high",
        "GitHub API erişimi geçici olarak engellendi veya rate-limit uygulandı.",
    ),
    (
        "transient-network-or-http",
        (
            r"\bHTTP\s+(429|500|502|503|504)\b",
            r"\b(429|500|502|503|504)\s+(Too Many Requests|Internal Server Error|Bad Gateway|Service Unavailable|Gateway Timeout)\b",
            r"connection reset",
            r"connection timed out",
            r"read timed out",
            r"temporary failure",
            r"service unavailable",
            r"TLS handshake timeout",
        ),
        True,
        "high",
        "Geçici ağ veya uzak servis hatası tespit edildi.",
    ),
    (
        "auth-or-permission",
        (
            r"\b401 Unauthorized\b",
            r"Bad credentials",
            r"Resource not accessible by integration",
            r"Permission denied",
            r"insufficient permission",
        ),
        False,
        "high",
        "Kimlik doğrulama veya izin problemi tespit edildi.",
    ),
    (
        "test-regression",
        (
            r"AssertionError:",
            r"FAILED \(failures=",
            r"FAILED \(errors=",
            r"tests? failed",
            r"FAIL: test_",
            r"ERROR: test_",
        ),
        False,
        "high",
        "Deterministik test regresyonu tespit edildi.",
    ),
    (
        "python-syntax-or-import",
        (
            r"SyntaxError:",
            r"IndentationError:",
            r"ModuleNotFoundError:",
            r"ImportError:",
        ),
        False,
        "high",
        "Python sözdizimi veya import/dependency problemi tespit edildi.",
    ),
    (
        "git-context",
        (
            r"fatal: not a git repository",
            r"not a git repository \(or any of the parent directories\)",
        ),
        False,
        "high",
        "Workflow içinde gerekli Git repository bağlamı bulunamadı.",
    ),
)

NOISE = (
    "DeprecationWarning:",
    "Post job cleanup.",
    "Complete job",
    "Set up job",
)


def _clean_line(line: str) -> str:
    line = re.sub(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\s*", "", line)
    line = re.sub(r"\x1b\[[0-9;]*m", "", line)
    line = re.sub(r"\b[0-9a-f]{40}\b", "<sha>", line, flags=re.I)
    line = re.sub(r"\b[0-9a-f]{7,12}\b", "<short-sha>", line, flags=re.I)
    line = re.sub(r"\b[0-9a-f]{8}-[0-9a-f-]{27,36}\b", "<uuid>", line, flags=re.I)
    return " ".join(line.strip().split())


def _signal_lines(log_text: str) -> list[str]:
    lines: list[str] = []
    for raw in log_text.splitlines():
        line = _clean_line(raw)
        if not line or any(noise in line for noise in NOISE):
            continue
        if re.search(
            r"error|fail|forbidden|unauthorized|rate limit|timeout|timed out|"
            r"exception|traceback|fatal|assertion|not a git repository|"
            r"permission|bad credentials|module.*not found|syntaxerror|http\s+[45]\d\d",
            line,
            flags=re.I,
        ):
            lines.append(line)
    if not lines:
        lines = [_clean_line(x) for x in log_text.splitlines() if _clean_line(x)][-12:]
    return lines[-24:]


def classify(log_text: str, workflow: str = "", run_id: str = "", run_attempt: int = 1) -> Diagnosis:
    evidence = _signal_lines(log_text)
    searchable = "\n".join(evidence)

    classification = "unknown"
    retryable = False
    confidence = "low"
    summary = "Yeni veya henüz sınıflandırılmamış bir hata imzası tespit edildi."

    for name, patterns, can_retry, level, message in PATTERNS:
        if any(re.search(pattern, searchable, flags=re.I) for pattern in patterns):
            classification = name
            retryable = can_retry
            confidence = level
            summary = message
            break

    normalized = "\n".join(evidence[:16]) or "<no-signal>"
    digest_input = f"{workflow}\n{classification}\n{normalized}".encode("utf-8", errors="replace")
    fingerprint = hashlib.sha256(digest_input).hexdigest()[:12]

    return Diagnosis(
        workflow=workflow,
        run_id=str(run_id),
        run_attempt=int(run_attempt),
        classification=classification,
        confidence=confidence,
        retryable=retryable,
        probe_retry_safe=(classification == "unknown"),
        fingerprint=fingerprint,
        summary=summary,
        evidence=evidence[:12],
    )


def render_markdown(d: Diagnosis) -> str:
    evidence = "\n".join(f"- `{line[:400]}`" for line in d.evidence) or "- Log içinde ayıklanabilir hata satırı bulunamadı."
    return (
        "# Self-Heal Diagnosis\n\n"
        f"- Workflow: **{d.workflow}**\n"
        f"- Run ID: `{d.run_id}`\n"
        f"- Attempt: **{d.run_attempt}**\n"
        f"- Classification: **{d.classification}**\n"
        f"- Confidence: **{d.confidence}**\n"
        f"- Retryable: **{'yes' if d.retryable else 'no'}**\n"
        f"- Fingerprint: `{d.fingerprint}`\n\n"
        f"{d.summary}\n\n"
        "## Evidence\n\n"
        f"{evidence}\n\n"
        "## Guardrail\n\n"
        "The guardian may retry bounded transient failures and may delegate persistent code fixes to a review-gated coding agent. "
        "It must never disable tests, weaken validation, expose secrets, or auto-merge a repair.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify GitHub Actions failures for bounded self-healing.")
    parser.add_argument("--log", required=True)
    parser.add_argument("--workflow", default="")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--run-attempt", type=int, default=1)
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()

    text = Path(args.log).read_text(encoding="utf-8", errors="replace")
    diagnosis = classify(text, args.workflow, args.run_id, args.run_attempt)
    Path(args.json_output).write_text(
        json.dumps(asdict(diagnosis), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    Path(args.markdown_output).write_text(render_markdown(diagnosis), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
