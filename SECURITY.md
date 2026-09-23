# Security Policy

AI agent skills are executable trust boundaries. Treat installation, updates, scripts, MCP integrations, and external tools with the same care as software dependencies.

## Supported surface

Security reports are relevant when they affect this repository's:

- Agent Skills and their supporting files
- installers or validation utilities
- plugin / extension manifests
- GitHub Actions workflows
- examples that execute code or access external services
- documented installation paths

## Before installing

1. Review the exact repository and ref you intend to use.
2. Inspect `SKILL.md`, scripts, package manifests, lifecycle hooks, and external URLs.
3. Prefer a reviewed tag, release, or immutable commit for sensitive workflows.
4. Grant only the filesystem, network, credential, shell, and tool permissions the skill actually needs.
5. Never place secrets in prompts, committed files, examples, or logs.
6. Test executable third-party skills in an isolated or disposable environment before granting access to important repositories or accounts.

Popularity, stars, forks, badges, marketplace presence, or inclusion in a curated list are not security guarantees.

## Supply-chain rule

A displayed commit hash is not enough by itself. After fetching or installing code that is expected to be pinned, verify that the resolved object is the exact reviewed commit before executing scripts or granting privileged access. Do not silently follow a moving branch when an immutable revision is expected.

For third-party Agent Skills, use the repository's `agent-skill-safety-auditor` skill as a review checklist before installation or redistribution.

## High-risk findings

Stop installation or execution when there is evidence of:

- credential, token, cookie, SSH-key, browser-data, or environment-variable exfiltration
- hidden or obfuscated executable payloads
- unexplained remote downloads or pipes to a shell
- destructive writes outside the documented scope
- persistence outside the documented install location
- privilege escalation unrelated to the advertised task
- install instructions that resolve to an unexpected repository or domain
- unexpected package registries, lifecycle hooks, or binary-only payloads

Do not label a dependency or project malicious without evidence. Record the exact file, command, URL, ref, and observed behavior behind the finding.

## Reporting a vulnerability

Do not publish secrets, exploit payloads, or sensitive user data in a public issue.

If GitHub's private vulnerability reporting is available for this repository, use **Security → Report a vulnerability**. Otherwise, open a minimal public issue that states only that you found a security concern and asks the maintainer for a private contact path. Do not include exploit details in that public issue.

A useful report includes:

- affected file or component
- exact commit, tag, or release
- reproducible impact
- minimum steps needed to confirm the issue
- suggested mitigation, when known

## Maintainer response

Security fixes should favor the smallest reversible change, add a regression check when practical, and avoid weakening existing validation to make a test pass.

When a compromised or unsafe release is confirmed, documentation should clearly identify the affected revision and a known-safe replacement.

## Security is part of usability

The goal is not to make Agent Skills inert. The goal is to make useful automation inspectable, least-privileged, reproducible, and explicit about side effects.
