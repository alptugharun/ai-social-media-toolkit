# AI Creator Stack — Curated Open-Source Reference Map

> A focused map of projects worth learning from if you work with prompts, assistants, agents, skills, MCP, automation and creator workflows.

This is **not** a leaderboard and it is not an endorsement of every implementation detail.

The purpose is simple:

**learn the useful pattern → understand why it works → build an original version for your own job.**

Need a smaller, evidence-labeled starting team instead of a broad reference map? Use the **[Verified AI Team Stack](AI-TEAM-STACK.md)** and its dependency-free CLI.

## Prompt engineering & prompt libraries

| Project | What to learn | Best use |
| --- | --- | --- |
| [DAIR.AI Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) | learning architecture, techniques, applications, references | structured prompt learning |
| [f / awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) | low-friction prompt discovery, community-friendly contribution model | inspiration for reusable prompt categories |
| [aj-geddes / useful-ai-prompts](https://github.com/aj-geddes/useful-ai-prompts) | standardized prompt contracts and quality gates | production-style prompt libraries |
| [convertscout / awesome-ai-prompts](https://github.com/convertscout/awesome-ai-prompts) | category navigation and platform-specific prompt discovery | browse-first collections |

### What we do differently here

Our [Prompt Library](../prompts/README.md) requires:
- use case;
- non-use case;
- inputs;
- copyable prompt;
- expected output;
- quality gate;
- example;
- troubleshooting;
- next step.

---

## Agent Skills & reusable capabilities

| Project | What to learn | Best use |
| --- | --- | --- |
| [Anthropic Skills](https://github.com/anthropics/skills) | self-contained skill folders, instructions, examples, portability | learning Agent Skills structure |
| [VoltAgent Awesome Agent Skills](https://github.com/VoltAgent/awesome-agent-skills) | breadth of real-world skill categories | discovering skill jobs worth studying |

### What we do differently here

We keep skill count secondary to:
- real job-to-be-done;
- clear output;
- evidence rules;
- installation guidance;
- runtime verification;
- external use.

Start: [Agent Skills](../skills/README.md)

---

## Agents, orchestration & workflows

| Project | What to learn | Best use |
| --- | --- | --- |
| [LangChain](https://github.com/langchain-ai/langchain) | components and application wiring | LLM application patterns |
| [LangGraph](https://github.com/langchain-ai/langgraph) | stateful graph-based agent workflows | durable multi-step agent flows |
| [Microsoft AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners) | progressive learning and practical lessons | learning agent fundamentals |

### What we do differently here

We prefer the lightest useful layer:
- prompt before agent;
- assistant before orchestration;
- skill before custom infrastructure;
- automation only after the manual flow works.

Read: [Integrations Hub](../integrations/README.md)

---

## Beginner-friendly AI learning

| Project | What to learn | Best use |
| --- | --- | --- |
| [Microsoft Generative AI for Beginners](https://github.com/microsoft/generative-ai-for-beginners) | lesson sequencing, exercises, approachable progression | structured self-learning |
| [DAIR.AI](https://github.com/dair-ai) | research-to-learning translation | prompt / agents learning ecosystem |

### Our path

[Learning Paths](../learning/README.md):

**Prompt → Assistant → Agent Skill → API → MCP → Automation**

Every stage should produce one useful artifact.

---

## Provider-specific building blocks

| Ecosystem | Useful reference |
| --- | --- |
| OpenAI | [OpenAI Cookbook](https://github.com/openai/openai-cookbook) |
| Anthropic | [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) |
| Google Gemini | [Google Gemini Cookbook](https://github.com/google-gemini/cookbook) |
| xAI / Grok | [xAI developer docs](https://docs.x.ai/) |

Use these for current provider behavior. Do not infer current API behavior from old blog posts or examples.

---

## MCP & integrations

Useful things to study:
- official or provider-maintained MCP examples;
- permission boundaries;
- read-only first implementations;
- deterministic tool contracts;
- clear error handling.

Our rule:

**MCP is a protocol choice, not a badge of sophistication.**

Read: [MCP & Plugin Guide](../integrations/MCP-PLUGIN-GUIDE.md)

---

## Creator / marketing application layer

Our niche is not “AI coding tools only.”

We focus on:
- creator research;
- social content;
- brand voice;
- Pinterest;
- Reels;
- Canva + AI;
- influencer workflows;
- digital visibility;
- measurement;
- approval-gated publishing.

Start:
- [Creator Materials](../downloads/README.md)
- [Reels Director](../prompts/creator/reels-director.md)
- [Pinterest Cluster Builder](../prompts/creator/pinterest-cluster.md)

---

## How to use this map

Do **not** clone every idea.

For each reference project, ask:

1. What user job is obvious in 10 seconds?
2. How fast can a visitor get the first result?
3. Is the example real, runnable or merely descriptive?
4. How does the project explain failure?
5. How does it invite contributions?
6. What makes people return?
7. Which part fits our AI + creator-ops positioning?
8. What should we intentionally *not* copy?

Then build an original implementation with our own scope, wording, examples, tests and evidence.
