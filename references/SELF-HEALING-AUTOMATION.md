# Self-Healing Automation Architecture

The repository uses a bounded, review-gated self-healing loop for its scheduled radars and validation workflow.

## Recovery loop

1. Every radar performs a local preflight compile/test before calling external APIs.
2. Self-Healing Automation Guardian observes completed workflow runs.
3. A failed run is reduced to a normalized failure fingerprint.
4. Known transient failures such as GitHub API 403/rate-limit responses, HTTP 429/5xx failures, and network timeouts receive bounded retries with backoff.
5. An unknown failure may receive one probe retry. The outcome becomes feedback:
   - success after retry -> fingerprint is recorded as transient;
   - repeated failure -> fingerprint is recorded as persistent.
6. Persistent failures are recorded as GitHub issues with evidence.
7. When GitHub Copilot coding agent is available, a persistent incident is assigned to the repository Self-Healer custom agent.
8. The coding agent must repair the root cause in a pull request, preserve validation, add regression coverage for deterministic defects, and never merge its own repair.
9. A later successful workflow run closes matching open incidents as recovered.

## Safety boundaries

The privileged workflow_run guardian executes only code from the trusted default branch. It never executes self-healing code from an untrusted pull-request head.

The guardian does not print or rotate secrets, does not disable tests, does not weaken policy guards, and does not auto-merge repairs.

Retries are capped by .github/self-heal-policy.json. Persistent failures escalate instead of looping forever.

## Learning model

This system does not claim to retrain an AI model. It learns operationally by preserving failure fingerprints and their outcomes in GitHub issue state:

- transient signatures can be retried automatically in future;
- persistent signatures are escalated to code repair;
- recovered incidents remain as an audit trail;
- deterministic repairs must arrive through a tested pull request.

This gives the automation memory and adaptation without allowing uncontrolled self-modification.
