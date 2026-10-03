# GitHub Showcase Benchmark — 2026-10-03

This note records the public GitHub patterns reviewed while improving Alptuğ Harun's profile and repository presentation.

It is a dated benchmark, not a permanent ranking. Star counts and repository state change over time.

## Profiles and repositories reviewed

### komutan234

Profile pattern:

- full English / Turkish switch;
- centered social buttons;
- large technology badge wall;
- GitHub stats cards;
- strong visual density.

Observed repository signal:

- `Proxy-List-Free`: 14 stars;
- `data-beans`: 6 stars;
- `ai-agent-marketplace`: 3 stars.

Lesson: a polished profile can improve scanning, but visual density alone does not create repository adoption.

### keon

Profile pattern:

- no dedicated profile README was found.

Observed repository signal:

- `algorithms`: 25,559 stars;
- `awesome-nlp`: 19,051 stars.

Repository pattern:

- one clear job;
- concise value proposition;
- immediate installation;
- copyable examples;
- tests;
- package distribution;
- clear project structure;
- contribution path.

Lesson: focused utility can massively outperform profile decoration.

### themiralay

Profile pattern:

- no dedicated profile README was found.

Observed repository signal:

- `Proxy-List-World`: 185 stars.

Repository pattern:

- extremely narrow job;
- live/updating output;
- usage instructions above the fold;
- current counts and source table;
- little conceptual overhead.

Lesson: a four-file utility can beat a large portfolio when the result is immediately useful.

### mustafacagri

Profile pattern:

- visually rich;
- social buttons;
- clear technical identity;
- personal voice;
- GitHub stats cards;
- long stack list.

Observed repository signal:

- `mevn-boilerplate`: 246 stars;
- `vue3-chatgpt-ai`: 121 stars;
- `ai-quality-gate`: 31 stars.

Engineering pattern in `ai-quality-gate`:

- dedicated MCP product boundary;
- published-package install path;
- CI and release workflows;
- many unit/integration tests;
- configuration contracts;
- failure handling;
- explicit setup and troubleshooting.

Lesson: the useful pattern to copy is not the emoji density; it is the product boundary + test depth + install clarity.

### omarsar / DAIR.AI

Profile pattern:

- very short personal README;
- research identity and contact routes;
- no decorative stack wall.

Observed repository signal:

- `omarsar/nlp_overview`: 1,324 stars;
- `dair-ai/Prompt-Engineering-Guide`: 78,799 stars.

Prompt Engineering Guide pattern:

- durable educational job;
- web version;
- large table of contents;
- multilingual pages;
- notebooks and lectures;
- contribution path;
- citation information;
- public updates;
- multiple useful entry points.

Lesson: authority compounds when one resource becomes the canonical place people return to.

### Anthropic

Organization pattern:

- no profile README dependency;
- separate repositories for distinct user jobs.

Observed repository signal:

- `anthropics/skills`: 179,469 stars;
- `anthropics/claude-code`: 149,026 stars;
- `anthropics/claude-cookbooks`: 53,158 stars;
- `anthropics/claude-quickstarts`: 17,789 stars.

Repository pattern:

- one-sentence job statement;
- first useful action immediately visible;
- demos / quickstarts;
- separate repositories instead of one universal mega-repo;
- disclaimers and data/usage boundaries where relevant;
- issue/support routes.

Lesson: a portfolio becomes strong when every repository has its own reason to exist.

## Agent Skills topic benchmark

The `agent-skills` topic currently contains several high-adoption repositories.

Examples from the snapshot:

- `anthropics/skills`: 179,469 stars;
- `addyosmani/agent-skills`: 100,649 stars;
- `blader/humanizer`: 53,674 stars.

Patterns worth keeping:

1. **One-line outcome before architecture.**
2. **One-command installation.**
3. **Examples before theory.**
4. **Named workflows / commands users can remember.**
5. **Host-specific setup hidden under collapsible details when long.**
6. **Evaluation fixtures and acceptance criteria.**
7. **Known limitations stated directly.**
8. **Adoption evidence kept separate from internal tests.**

## What we should copy as a pattern

Not wording. Not branding. Not screenshots.

Use these structural ideas:

- bilingual entry where it helps the actual audience;
- a strong first sentence;
- one clear job per standalone repository;
- installation / first result above the fold;
- visible example input and output;
- test commands users can reproduce;
- current support / runtime boundaries;
- screenshots or demos only when they prove a real result;
- contribution path;
- changelog / releases for software;
- citation / source trail for knowledge repositories;
- real external adoption recorded separately from maintainer activity.

## What we should not copy

- another person's exact README wording;
- exaggerated "best / ultimate / revolutionary" claims without proof;
- giant technology badge walls for tools not actually used;
- empty repositories created only to make the profile look busy;
- fake stars, fake users, fake testimonials or fake compatibility;
- a universal mega-repo after a component has earned a clear standalone job.

## Portfolio direction for Alptuğ Harun

The current main toolkit remains the integration / proof hub.

The best standalone candidates are:

1. **AI Workbench MCP**
   - existing package boundary;
   - read-only local MCP;
   - published PyPI package, official MCP Registry entry, cross-platform tests and maintainer-run real-host evidence already exist.

2. **Agent Skill Safety Auditor**
   - narrow trust job;
   - relevant to the fast-growing Agent Skills ecosystem;
   - should ship with deterministic checks, examples and a risk-report contract.

3. **Human-first Content QA**
   - bilingual TR/EN positioning is a useful differentiator;
   - should be framed as a writing-quality / voice tool, not an AI-detector promise.

4. **Creator Research Radar**
   - reusable evidence-first opportunity research;
   - should combine only proven radar logic and avoid platform-scraping claims.

Do not create these as empty shells. Split one out only when:

- its README can explain one job in one sentence;
- first useful result is under a few minutes;
- tests pass independently;
- dependencies and permissions are explicit;
- it has its own issue / support path;
- the main toolkit can link to the standalone repository without duplicate ownership confusion.

## Profile standard

The profile should feel human before it feels decorated.

Preferred order:

1. who Alptuğ is;
2. what he actually builds;
3. strongest proof project;
4. quick way to try it;
5. current standalone work;
6. evidence philosophy;
7. creator/brand context;
8. stats / visual extras last.

The test for every section is simple:

> Does this help a new visitor understand, try, trust, or contribute?

If not, remove it.
