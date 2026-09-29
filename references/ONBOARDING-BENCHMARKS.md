# Onboarding & Documentation Benchmarks

Research snapshot: **2026-09-29**

This note records public patterns observed in high-adoption Agent Skill / workflow repositories. It is a product-reference document, not a ranking of project quality.

## Public reference set

| Repository | Snapshot stars | Useful onboarding pattern |
| --- | ---: | --- |
| [obra/superpowers](https://github.com/obra/superpowers) | 292,754 | install paths by runtime, Basic Workflow, troubleshooting, community and update path |
| [anthropics/skills](https://github.com/anthropics/skills) | 178,962 | explains what a skill is, gives platform-specific use instructions, shows a basic skill example |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 51,894 | “how skills work together,” multiple install routes, task-oriented catalog, help/issues path |
| [ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills) | 3,592 | workflow positioning, concrete input/output conventions, production-oriented examples |
| [kostja94/marketing-skills](https://github.com/kostja94/marketing-skills) | 1,000 | quick start, usage guide, learning paths and task-specific playbooks |
| [OpenClaudia/openclaudia-skills](https://github.com/OpenClaudia/openclaudia-skills) | 702 | concise category positioning and multi-agent compatibility |

Counts are a dated snapshot and can change.

## Patterns worth adapting

### 1. Explain the job before the implementation

A visitor should understand the result before learning the file structure.

### 2. Give a first successful action

Examples:

- one install command
- one first request
- one sample input
- one visible expected output

### 3. Separate “install” from “use”

Installation success is not user success.

A good guide continues through:

**install → first request → input → output → QA → next step**

### 4. Show how pieces connect

A large catalog is easier to understand when users see dependency/order maps.

### 5. Document failure behavior

Useful repositories explain:

- what can go wrong
- how to diagnose it
- what not to retry blindly
- where to ask for help

### 6. Use examples without turning examples into claims

Examples should be clearly synthetic unless they are sourced real results.

### 7. Provide multiple skill levels

Technical users may want CLI/API details. Non-technical users need a no-terminal path.

## What this toolkit should do differently

The strongest differentiated lane remains **creator operations for social media**, especially:

- Pinterest / visual search
- Reels / short-form
- Canva + AI
- content repurposing
- creator research and measurement
- approval-gated automation

The goal is not to imitate large skill catalogs.

The goal is to make a smaller system unusually easy to understand, use, verify and improve.

## Documentation standard

Every new user-facing resource should answer:

1. **What result does this create?**
2. **Who is it for?**
3. **What do I need before starting?**
4. **Exactly how do I use it?**
5. **What should the output look like?**
6. **What is the most common mistake?**
7. **What do I do next?**
8. **What changes if something fails?**

Reference implementation: [How to Use Everything](../docs/HOW-TO-USE-EVERYTHING.md).
