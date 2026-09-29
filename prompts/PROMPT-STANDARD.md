# Prompt Library Standard

Every prompt in `prompts/` uses a consistent human-readable contract.

## Required frontmatter

- `id`
- `title`
- `category`
- `version`
- `complexity`
- `interaction`
- `models`

## Required sections

1. Overview
2. Use When
3. Do Not Use When
4. Required Inputs
5. Copy/Paste Prompt
6. Expected Output
7. Quality Gate
8. Example Input
9. Troubleshooting
10. Next Step

## Design principles

- prompts should solve one clear job;
- inputs and deliverables must be explicit;
- unsupported facts must be flagged rather than invented;
- examples must be synthetic unless sourced;
- platform-specific claims need current official documentation;
- prompt quantity is not quality.
