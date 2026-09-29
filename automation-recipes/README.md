# Automation Recipes

These are **workflow blueprints**, not evidence that a specific account is connected or publishing.

## Research → Brief

```text
source signal
→ date/source capture
→ evidence extraction
→ opportunity score
→ brief
→ human review
```

## Source → Multi-Platform Pack

```text
approved source
→ core message
→ platform routing
→ native drafts
→ QA
→ approval
```

Do not auto-cross-post identical copy.

## Weekly Performance Review

```text
analytics export
→ own baseline
→ outlier detection
→ qualitative review
→ next experiments
```

## Release Watch

```text
official release source
→ change detection
→ relevance filter
→ concise summary
→ content opportunity
→ notify only if material
```

## Approval-Gated Publisher

```text
final asset
→ metadata validation
→ destination/rights check
→ explicit approval
→ schedule/publish
→ read-back
→ evidence log
```

Never treat "queued" as "published verified".

## Failure Guardian

```text
failed run
→ collect logs
→ classify
→ transient? bounded retry
→ persistent? incident
→ root-cause fix
→ tests
→ review
```

Never weaken tests to make recovery look successful.
