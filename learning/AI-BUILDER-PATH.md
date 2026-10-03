# AI Builder Path — prompt → assistant → skill → MCP → plugin

Build the **smallest reliable layer that solves the job**, prove it works, then add capability only when the next layer is justified.

This path is for people who want to learn prompt engineering, reusable assistants, Agent Skills, MCP servers, ChatGPT/Codex plugins, bot starters and automation without confusing those layers.

## The layer map

| Layer | Use it when | What it gives you | What it does not give you |
| --- | --- | --- | --- |
| Prompt | one repeatable reasoning/writing job | explicit inputs, output and QA | tool access or persistent permissions |
| Reusable assistant | the same job needs stable instructions/context | repeatable behavior and starter requests | automatic external actions |
| Agent Skill | an agent should load a reusable procedure | portable task expertise | account authorization |
| MCP server | the model needs structured tools/data | callable tools/resources/prompts | permission bypass |
| Plugin | skills and/or MCP should install as one product | packaged capability and discovery | proof that every host behaves identically |
| Automation | a proven workflow needs triggers/state | repeatable execution | proof that a future external action succeeded |

## Rule zero: start from the job

Before choosing technology, write:

- **User:** who has the problem?
- **Job:** what are they trying to finish?
- **Input:** what do they already have?
- **Output:** what observable result should exist?
- **Boundary:** what must the system never claim or do?
- **Proof:** how will you know it worked?

If those six lines are vague, adding more tools will usually make the system harder to debug.

## Stage 1 — engineer the prompt contract

A production prompt is not “a clever sentence.” It is a testable contract.

Use this structure:

1. objective;
2. required inputs;
3. relevant context;
4. constraints;
5. output schema;
6. evidence rules;
7. failure behavior;
8. quality gate.

### Prompt test set

Create at least five cases:

- normal input;
- missing input;
- conflicting input;
- oversized/noisy input;
- adversarial or instruction-in-source input.

Record expected behavior before refining the wording.

### Prompt failure log

For every meaningful failure, record:

- test case;
- observed output;
- expected output;
- root cause;
- exact change;
- regression test.

Do not “fix” a prompt by adding random paragraphs until one example passes.

## Stage 2 — turn repeated work into a reusable assistant

Create an assistant only when the prompt is used repeatedly and the job boundary is stable.

The assistant package should contain:

- name;
- one-sentence promise;
- instructions;
- required context/knowledge;
- connected-tool assumptions;
- starter requests;
- output contract;
- escalation rules;
- acceptance tests.

### Personalization without chaos

Separate stable context from per-task input.

**Stable context** may include brand rules, audience, terminology, formatting and decision principles.

**Task input** should contain the current topic, source material, goal and constraints.

Do not bury constantly changing facts inside permanent instructions.

## Stage 3 — package procedure as an Agent Skill

Use a skill when an agent should load a reusable procedure for a specific job.

A useful skill should answer:

1. when should the agent use this?
2. what files/references are required?
3. what sequence should it follow?
4. what tools may it use?
5. what must it verify before completion?
6. what should it return?

Keep the skill narrow enough to evaluate.

For GitHub Copilot, current official documentation supports project skills in locations such as `.github/skills`, `.claude/skills` or `.agents/skills`. Runtime details can change, so validate against the current host documentation before publishing.

## Stage 4 — add MCP only when a tool boundary is needed

An MCP server is appropriate when the model needs structured access to a capability or data source.

An MCP server can expose:

- tools;
- resources;
- prompts;
- instructions.

### Tool contract checklist

Every public tool should have:

- a precise name;
- a description that says when to use it;
- strict input schema;
- bounded output;
- explicit error behavior;
- permission/safety annotations where supported;
- tests that invoke the public tool name.

Prefer read-only first.

Add writes only when the product job requires them and when approval, idempotency, retry behavior and read-back verification are defined.

### MCP test ladder

1. schema/static validation;
2. unit tests;
3. direct protocol/transport test;
4. packaged clean-install test;
5. host-level invocation;
6. negative/invalid-input tests;
7. cross-host evidence where meaningful.

Registry publication is distribution evidence. It is not universal runtime compatibility evidence.

## Stage 5 — build a plugin when capability should install as one product

Current OpenAI plugin documentation describes plugins as packages that can contain reusable skills, MCP configuration, or both.

Choose:

- **skill-only plugin** when instructions/resources are enough;
- **MCP-only plugin** when tools/data are the product;
- **skill + MCP plugin** when the user needs both procedure and capability.

### Plugin product contract

Write these before packaging:

- target user;
- job-to-be-done;
- first useful result;
- included skills;
- included MCP/tools;
- required permissions;
- data handled;
- installation path;
- five acceptance tests;
- uninstall/recovery notes;
- known limitations.

### Why would someone install it?

A plugin earns installation when it gives a faster or safer result than copying instructions manually.

Strong reasons include:

- repeatable time saving;
- fewer setup mistakes;
- portable workflow;
- clear tool access;
- visible tests;
- narrow permissions;
- useful examples;
- trustworthy failure behavior.

Weak reasons include:

- “AI powered” with no concrete result;
- dozens of features with no first-use path;
- unsupported performance claims;
- a giant prompt hidden behind packaging.

## Stage 6 — automate only after manual proof

Do not schedule an unreliable workflow.

Before automation, prove:

- the manual run succeeds repeatedly;
- duplicate execution is handled;
- missing input has a defined outcome;
- external writes have approval/read-back;
- failure is visible;
- retry behavior is bounded.

Automation should remove repeated checking, not hide uncertainty.

## Installation and verification paths

### This repository

Start with the offline proof:

```bash
python tools/first_run_check.py
```

On Windows:

```powershell
py -3 -X utf8 tools/first_run_check.py
```

For Agent Skills, see [Installation & Compatibility](../docs/INSTALLATION.md).

For the read-only MCP product, see [AI Workbench MCP](../packages/ai-workbench-mcp/README.md) and the focused standalone repository linked there.

### OpenAI plugin development

Use the current official Plugin and MCP documentation because workspace/plan capabilities evolve.

A typical development sequence is:

1. define the plugin job;
2. decide skill-only, MCP-only or combined;
3. implement the smallest capability;
4. run local/unit tests;
5. connect in the supported development surface;
6. invoke real tools from the host;
7. inspect returned data;
8. test failure/permission cases;
9. package only after the host test passes.

### GitHub Agent Skills

Keep the procedure in a dedicated skill directory with `SKILL.md` and optional referenced resources/scripts.

Validate the repository and then test the skill inside at least one real host instead of treating file existence as runtime proof.

## Quality gate before public release

- [ ] one clear user/job
- [ ] first useful result documented
- [ ] install steps tested
- [ ] examples use real or clearly synthetic data
- [ ] no fake capabilities
- [ ] permissions are minimal
- [ ] errors are bounded and understandable
- [ ] public tools have tests
- [ ] docs links resolve
- [ ] clean environment test passes
- [ ] real host test is recorded separately
- [ ] limitations are visible
- [ ] uninstall/recovery path exists where relevant

## How to write the public page

The first screen should answer:

1. **What is this?**
2. **Who is it for?**
3. **What can I do in two minutes?**
4. **Why should I trust it?**
5. **How do I install it?**

A useful headline pattern is:

> **[Concrete result] for [specific user] — without [major friction].**

Then show the shortest working example before architecture diagrams.

## Error report template

When something fails, report:

```text
Environment:
Version/commit:
Command or host action:
Expected:
Observed:
First meaningful error:
Reproduction steps:
Affected test:
Fix:
Regression added:
Final verification:
```

This makes debugging teachable and prevents “it did not work” reports from turning into guesswork.

## Official references

- OpenAI Plugins: https://developers.openai.com/plugins
- OpenAI plugin quickstart: https://developers.openai.com/plugins/quickstart
- OpenAI MCP server concept: https://developers.openai.com/plugins/concepts/mcp-server
- OpenAI MCP server/UI quickstart: https://developers.openai.com/plugins/build/app-quickstart
- GitHub Agent Skills: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills

Check the current official documentation before relying on account, plan, publishing or host-specific behavior.
