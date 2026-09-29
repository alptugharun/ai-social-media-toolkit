# Claude Project Blueprint

Checked against Anthropic Help Center on **2026-09-30**.

Claude Projects are available on paid Claude plans and provide self-contained workspaces with project knowledge and project instructions.

Official references:
- https://support.anthropic.com/en/articles/9519177-how-can-i-create-and-manage-projects
- https://support.anthropic.com/en/articles/9517075-what-are-projects

## Build one

1. Create a Project in Claude.
2. Name it after one job, e.g. **Creator Research Desk**.
3. Add only reusable knowledge needed for that job.
4. Put the portable assistant instructions into Project Instructions.
5. Start a chat inside the Project and run the acceptance tests.

## Recommended knowledge

- brand voice examples;
- content pillars;
- approved facts;
- output templates;
- evidence policy.

## Do not add

- API keys;
- passwords;
- private client exports not needed for the job;
- unrelated files "just in case".

## Example first request

```text
Use the project instructions.
Turn these source notes into:
1. supported facts,
2. uncertainty,
3. three content angles,
4. one recommended test.
```

## Verification

A project is **host verified** only after the instructions and knowledge are tested in a real Claude Project/version and the result is documented.
