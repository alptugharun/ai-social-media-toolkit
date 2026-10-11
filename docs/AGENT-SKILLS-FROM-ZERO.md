# Every Agent Skill — Start From Zero

This guide explains **every installable Agent Skill in this repository** for someone who has never used the skill before.

Do not install all skills just because they exist.

Use this order:

1. define the job;
2. choose the smallest relevant skill;
3. inspect its `SKILL.md`;
4. install only that skill when possible;
5. use synthetic/public-safe input first;
6. check the expected result and limitations;
7. add another skill only when the workflow actually needs it.

## Install basics

List all skills:

```bash
npx skills add alptugharun/ai-social-media-toolkit --list
```

Install one:

```bash
npx skills add alptugharun/ai-social-media-toolkit --skill SKILL-NAME
```

Install all only when you intentionally want the whole pack:

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

A successful install is **not** proof that every host/runtime behaves identically. Confirm the loaded skill path in your agent and run one small test.

---

## creator-context-builder

**What it is:** the shared-context foundation for personalized creator/brand work.

**Why it exists:** repeated briefing creates inconsistency. This skill builds one reusable source of truth while separating facts from preferences and guesses.

**Use it when:** several downstream skills need the same identity, audience, proof, voice, platform and approval context.

**First request:**  
> Build my shared creator context from these current facts and approved writing samples. Separate VERIFIED facts, PREFERENCE choices, OBSERVED patterns and HYPOTHESIS items. Flag stale metrics and do not store secrets.

**Expected result:** a reusable creator-context file, stale/recheck list, open questions and up to three recommended next skills.

**Limit:** it must not infer sensitive traits, store credentials or silently turn old metrics into current facts.

---

## creator-ops

**What it is:** the routing/orchestration skill.

**Why it exists:** one giant generic prompt should not pretend to be research, strategy, production and measurement at once.

**Use it when:** you know the outcome but are unsure which specialized skill(s) should handle the workflow.

**First request:**  
> My objective is [goal], platform is [platform], evidence is [input]. Route this through the minimum relevant skills and stop before public publishing.

**Expected result:** objective → evidence → route → usable artifact → review → measurement.

**Limit:** orchestration does not prove any external account/API is connected.

---

## viral-content-radar

**What it is:** an evidence-first trend/outlier deconstruction workflow.

**Why it exists:** one popular post is not automatically a trend, and copying surface details is not strategy.

**Use it when:** you have recent posts, trend signals, outliers or references and want the reusable mechanics behind them.

**First request:**  
> Analyze these examples. Separate verified evidence from weak signals, identify reusable mechanics, and propose original tests without copying source-specific expression.

**Expected result:** evidence table, pattern/mechanic analysis, confidence labels and original experiments.

**Limit:** it must not call one isolated post a confirmed trend or promise virality.

---

## reels-director

**What it is:** a production-ready short-form vertical-video planner.

**Why it exists:** a caption is not a Reel production plan.

**Use it when:** you need a 9:16 Reel/Short/TikTok concept with timing, voiceover, shots and QA.

**First request:**  
> Turn this evidence/topic into a 30–35 second vertical video. Give me a 0–2 second hook, timed voiceover, shot list, on-screen text, edit direction and review gate.

**Expected result:** timed hook/script/shot flow plus visual/edit instructions and final QA.

**Limit:** it does not guarantee reach and should not invent facts or assets.

---

## pinterest-growth-engine

**What it is:** a search-led Pinterest planning workflow.

**Why it exists:** Pinterest growth needs query intent, board fit, creative variation and destinations—not random Pin volume.

**Use it when:** you already have keyword/trend/account evidence and want a coherent Pin cluster.

**First request:**  
> Build a 7-Pin cluster around this validated search intent. Give every Pin a distinct role, visual direction, board match, destination and KPI.

**Expected result:** non-duplicate Pin concepts mapped to search intent and destinations.

**Limit:** it must not invent search volume or turn one visual into seven near-duplicates.

---

## pinterest-opportunity-radar

**What it is:** the evidence-gathering/selection layer before Pinterest production.

**Why it exists:** seasonal, visual-search and query opportunities change; planning should start from current evidence.

**Use it when:** you need to decide **what** Pinterest opportunity is worth pursuing before building a cluster.

**First request:**  
> Evaluate these Pinterest signals. Separate verified trend/search evidence from hypotheses, score the strongest opportunities, and explain what would invalidate each one.

**Expected result:** evidence-ranked opportunity shortlist with freshness, fit, saturation/uncertainty and next validation.

**Limit:** it does not have permission to fabricate Pinterest search volume or claim discovery placement.

---

## content-repurposer

**What it is:** a source-to-platform transformation workflow.

**Why it exists:** repurposing should adapt the idea to each platform instead of copying the same text everywhere.

**Use it when:** one strong source article/video/research asset should become several platform-native outputs.

**First request:**  
> Repurpose this source into Instagram, LinkedIn and Pinterest versions. Preserve facts, change the structure/hook/CTA for each platform, and show what came from the source versus creative adaptation.

**Expected result:** distinct platform-native derivatives tied to one verified source.

**Limit:** it must not invent facts or mechanically duplicate the same execution.

---

## influencer-fit-auditor

**What it is:** an evidence-led creator/brand fit review.

**Why it exists:** follower count alone is weak evidence for campaign fit.

**Use it when:** evaluating a creator, influencer or partnership using supplied/public-safe campaign and audience evidence.

**First request:**  
> Audit this creator for this campaign using only the supplied evidence. Separate fit, risk, missing evidence and the questions we must answer before committing.

**Expected result:** fit rationale, evidence, risks, uncertainty and next questions.

**Limit:** it must not invent demographics, campaign results or treat follower count as sufficient proof.

---

## brand-voice-humanizer

**What it is:** a rewrite workflow for removing generic AI texture without changing facts.

**Why it exists:** AI-assisted writing often becomes over-polished, repetitive or templated.

**Use it when:** the factual payload is correct but the writing does not sound like the creator/brand.

**First request:**  
> Rewrite this in Brand-Locked mode using my approved context/examples. Preserve every factual claim and remove generic AI texture.

**Expected result:** more natural wording/rhythm while factual meaning stays intact.

**Limit:** it must not add unsupported claims or manufacture personality the user did not approve.

---

## signal-to-content

**What it is:** a bridge from evidence to a bounded content experiment.

**Why it exists:** interesting signals should become testable hypotheses, not instant certainty.

**Use it when:** you have research/audience/trend evidence and need original content tests.

**First request:**  
> Turn this evidence into three original content experiments. For each, show the evidence, hypothesis, execution, KPI and stop/review condition.

**Expected result:** original test angles with measurement logic.

**Limit:** it must not present a hypothesis as measured fact or guarantee virality.

---

## comment-intelligence

**What it is:** a workflow for clustering comments into questions, objections, language and opportunity signals.

**Why it exists:** comments often contain useful qualitative evidence that gets lost in manual scrolling.

**Use it when:** you have a permitted comment sample/export and want recurring themes or content/product questions.

**First request:**  
> Cluster these comments into repeated questions, objections, pains, desired outcomes and useful audience language. Keep sample evidence separate from market-wide conclusions.

**Expected result:** evidence-backed theme map plus content/research opportunities.

**Limit:** a small comment sample is not proof of total market demand.

---

## agent-skill-safety-auditor

**What it is:** the procedural Agent Skill version of pre-install safety review.

**Why it exists:** third-party skills can ask an agent to execute shell/network/filesystem/credential-related behavior.

**Use it when:** inspecting an unfamiliar Agent Skill before installing/reusing it.

**First request:**  
> Review this Agent Skill and referenced scripts before installation. Identify execution, network, credential, filesystem and supply-chain risks with concrete evidence.

**Expected result:** evidence-led risk findings and PASS/REVIEW/BLOCK-style conditions for human judgment.

**Limit:** static review is not runtime monitoring or a security certificate.

For deterministic offline scanning, use the standalone **Agent Skill Safety Auditor** Python CLI.

---

## github-opportunity-radar

**What it is:** a GitHub demand/supply proxy and project-gap research workflow.

**Why it exists:** “few repos exist” is not the same as “users want this.”

**Use it when:** deciding whether a new Agent Skill/repo/tool is worth building.

**First request:**  
> Compare these GitHub opportunity ideas using current repository/search/activity proxies. Label proxies honestly, inspect closest competition, and define a seven-day proof plus stop condition.

**Expected result:** ranked opportunities with competitor overlap, evidence limitations and validation plan.

**Limit:** GitHub result counts are not search volume and the score is not a star forecast.

---

## plugin-mcp-architect

**What it is:** a design/teaching workflow for prompt → assistant → Agent Skill → MCP → plugin architecture.

**Why it exists:** many AI projects choose a more powerful integration layer than the job needs.

**Use it when:** deciding which AI integration layer to build, package or teach.

**First request:**  
> Map this job to the smallest appropriate layer: prompt, assistant, Agent Skill, MCP, plugin or automation. Explain permissions, tests, packaging and why the next-more-powerful layer is unnecessary.

**Expected result:** architecture decision, boundaries, implementation path and test/release plan.

**Limit:** an architecture brief does not publish/register/deploy the external integration by itself.

---

## maps-opportunity-radar

**What it is:** opportunity research for Maps/Places/local-intelligence AI workflows.

**Why it exists:** generic place-search wrappers are easy to build but often poorly differentiated.

**Use it when:** exploring a local/geospatial product/workflow and wanting to understand competition, workflow value and validation.

**First request:**  
> Evaluate these Maps/local intelligence ideas. Reject generic wrappers, compare existing solutions, identify a higher-level workflow gap and define a seven-day proof.

**Expected result:** evidence-ranked map/local opportunities plus differentiation and validation.

**Limit:** it must not recommend restricted scraping or present result-count proxies as demand.

---

## maps-policy-guard

**What it is:** a policy/architecture review for Maps/Places/Street View data workflows.

**Why it exists:** storage, caching, scraping, attribution and screenshot use can cross platform-policy boundaries.

**Use it when:** designing a workflow that collects, stores, caches, exports or republishes Maps-related data/media.

**First request:**  
> Review this proposed Maps workflow before implementation. Identify authorization, scraping, storage, retention, attribution and screenshot/media risks, then suggest a safer architecture.

**Expected result:** policy-risk map, BLOCK/REVISE items and safer design choices.

**Limit:** it is not legal advice and should not fabricate platform permissions.

---

## local-business-intelligence

**What it is:** a workflow for turning owned/authorized local-business signals into useful market/content/creator insight.

**Why it exists:** local reviews, FAQs, location data and business signals are useful only when source/permission and inference boundaries are clear.

**Use it when:** you have authorized local/owned signals and want demand/content/positioning ideas.

**First request:**  
> Use these authorized local-business signals. Separate source observation from inference, identify content/market opportunities, and show what additional evidence is needed.

**Expected result:** source-backed local insights and practical actions.

**Limit:** it must not invent private analytics, scrape restricted surfaces or infer sensitive traits.

---

## commercial-opportunity-radar

**What it is:** a validation-first comparison of possible products/services/revenue lanes.

**Why it exists:** technical novelty does not prove buyer demand.

**Use it when:** several things could be monetized and you need to choose what deserves a real buyer test.

**First request:**  
> Compare these three commercial ideas by buyer clarity, pain frequency, proof, recurring need, distribution and implementation cost. Give me the smallest seven-day validation and stop condition.

**Expected result:** prioritized commercial hypotheses and proof plan—not a revenue forecast.

**Limit:** it must not invent buyers, willingness-to-pay, conversion rates or revenue.

---

## monetization-architect

**What it is:** a staged monetization design workflow for value that already has some proof.

**Why it exists:** jumping straight from an open-source idea to SaaS/pricing can waste time before demand is validated.

**Use it when:** a workflow/product has credible use evidence and you need the next paid layer.

**First request:**  
> Design the smallest paid test around this proven workflow. Keep the free artifact useful and stage the path from implementation service to recurring product only if evidence supports it.

**Expected result:** open proof → service → productized/recurring layer → hosted/product path with gates.

**Limit:** it must not set prices, promise income or treat stars/clones as paying demand.

---

# Quick decision map

| If your job is… | Start with… |
| --- | --- |
| Stop repeated briefing | `creator-context-builder` |
| Route an unclear creator workflow | `creator-ops` |
| Deconstruct recent trends/outliers | `viral-content-radar` |
| Produce a short vertical video plan | `reels-director` |
| Build a Pinterest cluster | `pinterest-growth-engine` |
| Find the Pinterest opportunity first | `pinterest-opportunity-radar` |
| Adapt one source across platforms | `content-repurposer` |
| Evaluate creator/brand fit | `influencer-fit-auditor` |
| Remove AI-sounding copy | `brand-voice-humanizer` |
| Turn evidence into tests | `signal-to-content` |
| Learn from comments | `comment-intelligence` |
| Inspect a third-party Agent Skill | `agent-skill-safety-auditor` |
| Find a GitHub project/skill gap | `github-opportunity-radar` |
| Choose prompt vs skill vs MCP/plugin | `plugin-mcp-architect` |
| Research Maps/local product gaps | `maps-opportunity-radar` |
| Review Maps data/policy risk | `maps-policy-guard` |
| Analyze authorized local business signals | `local-business-intelligence` |
| Validate what may be worth selling | `commercial-opportunity-radar` |
| Design the paid path after proof | `monetization-architect` |

## Final rule

**One job, one first skill, one verifiable result.**

Add complexity only when the next layer solves a real problem.
