# How to Use Everything — The AI Social Media Toolkit Field Manual

> **Open the repo. Pick one job. Get one useful result. Then expand.**

This manual is for people who do **not** want to reverse-engineer a repository before they can use it.

It explains what each public part of the AI Social Media Toolkit is for, what you need before starting, exactly how to use it, what a useful result should look like, and where to go next.

The toolkit has four public layers:

1. **Starter Materials** — use immediately, no terminal required.
2. **Agent Skills** — install into a compatible AI agent for reusable workflows.
3. **Python Tools** — run transparent scoring and research utilities.
4. **GitHub Automations** — maintain research, validation, health and recovery.

---

# Pick Your First Result in 60 Seconds

| If your problem is… | Start here | You should finish with… |
| --- | --- | --- |
| “I have a topic but no strong content angle.” | Creator Prompt Starter Kit | evidence-backed angle + hook + draft |
| “My AI copy sounds generic.” | Brand Voice Humanizer | natural rewrite without changing facts |
| “I need a 30–35 sec Reel.” | Reels Production Starter Kit / Reels Director | timed script + shot plan + QA |
| “I want Pinterest traffic.” | Pinterest Growth Starter Kit / Pinterest Growth Engine | 7-Pin cluster + destinations + KPI |
| “I have one good source and need five platform versions.” | Content Repurposer | native versions for each platform |
| “Which post actually outperformed?” | Social Outlier Analyzer | ranked posts vs your own baseline |
| “Which idea should I produce first?” | Signal-to-Content Scorer | transparent opportunity ranking |
| “I want AI assistants for repeatable creator jobs.” | AI Assistant Blueprints | configured narrow-purpose assistants |
| “I want to automate repetitive creator work.” | Creator Automation Starter Pack | approval-gated automation blueprint |
| “I want the full operating model.” | AI Creator OS Starter Map | connected research → content → measurement loop |

---

# Part I — Starter Materials

These resources live in `downloads/`. You can open them in GitHub, copy them into your notes, or adapt them into your own workspace.

## 1. Creator Prompt Starter Kit

### Headline

**Stop collecting prompts. Start running a repeatable content system.**

### Best for

- creators who use ChatGPT, Claude, Gemini or similar assistants
- social-media managers
- people who keep rewriting the same instructions from scratch
- anyone who wants evidence → angle → hook → content → QA to stay connected

### Before you start

Prepare:

- one topic
- one audience
- one objective
- any real evidence you already have: comments, analytics, source links, FAQs, client questions

### Step by step

1. Open `downloads/CREATOR-PROMPT-STARTER-KIT.md`.
2. Start with **Audience Problem Mapper** if the audience problem is still fuzzy.
3. Paste only real evidence into the evidence field. If you have none, say that explicitly.
4. Run **Evidence-to-Angle Generator** and choose one angle, not all five.
5. Use **Hook Stress Test** to sharpen only that selected angle.
6. Choose the production prompt that matches the asset: Reels, Pinterest, multi-platform, visual direction, etc.
7. Run **Brand Voice Humanizer** after the factual draft exists.
8. Run **Content QA Gate** immediately before publishing.
9. After the post has real data, use **Winner Expansion** with real metrics.

### Example

Input:

```text
Audience: freelance social-media managers
Topic: AI-generated Reels
Objective: saves + authority
Evidence:
- three client questions asking how to make AI visuals look less artificial
- last two behind-the-scenes posts received more saves than generic AI news
```

Useful outcome:

- one specific audience tension
- 3–5 defensible angles
- one selected hook
- one platform-native draft
- one visual direction
- one QA result

### Common mistake

Do not run every prompt and publish every output. The system is a funnel: each step should narrow the decision.

### Next

Use **Reels Production Starter Kit** or **Pinterest Growth Starter Kit** depending on the format.

---

## 2. AI Assistant Blueprint Starter Pack

### Headline

**Build five useful AI teammates — not one assistant pretending to do everything.**

### Best for

People who use custom assistants such as Gemini Gems or comparable instruction-based assistants.

### Before you start

Prepare:

- your approved brand voice examples
- audience definition
- platform priorities
- claims you must never make
- preferred output format

Never add passwords, access tokens or private client data to a shared/public assistant.

### Step by step

1. Open `downloads/AI-ASSISTANT-BLUEPRINTS.md`.
2. Pick **one** blueprint for one repeated job.
3. Create a new custom assistant in your chosen platform.
4. Paste the blueprint's **Instruction** into the system/instruction field.
5. Add your own brand/audience context as knowledge only if the platform supports it safely.
6. Save the provided starter requests.
7. Test the assistant with one real task you already know well.
8. Check whether it follows the narrow job rather than wandering into unrelated work.
9. Tighten instructions if it repeatedly overreaches.

### Example

Use **Reels Director**.

First request:

```text
Turn this verified topic into a 32-second Turkish Reel for beginner creators.
Keep the first three seconds problem-first.
Here are the only facts you may use: [paste evidence].
```

Useful outcome:

- spoken script
- shot structure
- B-roll needs
- edit notes
- CTA

### Common mistake

Do not merge all five blueprints into one mega-assistant. Narrow assistants are easier to test and trust.

### Next

Pair the assistant with **Creator Automation Starter Pack** only after its manual output is consistently useful.

---

## 3. Creator Automation Starter Pack

### Headline

**Automate the boring handoffs. Keep judgment and publishing under control.**

### Best for

Creators or agencies already repeating the same research, repurposing or reporting steps.

### Before you start

You need:

- a workflow you can already complete manually
- verified connector/account access
- a clear source of truth
- a clear human approval step
- a failure/rollback plan

### Step by step

1. Open `downloads/CREATOR-AUTOMATION-STARTER-PACK.md`.
2. Choose **one** of the three blueprints.
3. Recreate the blocks in n8n, Zapier, Make or your orchestration system.
4. Connect only the accounts needed for that flow.
5. Test with sample/non-sensitive data first.
6. Add deduplication before any content creation or external write.
7. Add the human approval gate.
8. Run the workflow manually several times.
9. Only then schedule it.
10. Monitor the first scheduled runs and save failure evidence.

### Example flow

```text
RSS / source URL
→ extract title/date/source
→ evidence check
→ content brief
→ save draft
→ human approval
→ stop
```

The starter version deliberately does **not** auto-publish.

### Common mistake

Automating a bad manual workflow only makes bad output arrive faster.

### Next

When a flow is stable and repeatedly valuable, evaluate whether it belongs in a future **Creator Automation Vault**.

---

## 4. Pinterest Growth Starter Kit

### Headline

**Turn one search opportunity into a 7-Pin system — not seven random designs.**

### Best for

- Pinterest creators
- visual niches
- bloggers
- ecommerce/editorial discovery
- people who need Pin → destination consistency

### Before you start

Prepare:

- keyword or trend evidence
- one destination page per meaningful intent
- a visual concept
- the KPI you care about: saves, outbound clicks, etc.

### Step by step

1. Open `downloads/PINTEREST-GROWTH-STARTER-KIT.md`.
2. Separate evidence into broad, problem, inspiration, seasonal and commercial intent.
3. Build the seven Pin roles.
4. Fill the table **before** designing.
5. Assign a destination to every Pin.
6. Reject any Pin whose promise and destination do not match.
7. Create a consistent visual system.
8. Publish only after checking crops, titles/descriptions and destination.
9. Measure with real Pinterest analytics.
10. Expand winners by changing one variable at a time.

### Example

Topic: autumn nail art.

A good cluster does **not** create seven nearly identical autumn nail images.

It might separate:

- inspiration
- beginner tutorial
- short-nail variation
- comparison
- seasonal color palette
- search-led design
- high-save visual reference

Each should have a reason to exist.

### Common mistake

Bulk pinning is not a strategy. Search intent + useful visual + destination fit is.

### Next

Install **Pinterest Growth Engine** if you want the workflow available directly inside your AI agent.

---

## 5. Reels Production Starter Kit

### Headline

**From “I have an idea” to a shoot-ready 30–35 second Reel.**

### Best for

Short-form creators who lose time between idea, script, visuals and edit.

### Before you start

Prepare:

- one topic
- audience
- one desired viewer action
- evidence/facts
- whether the video is talking-head, B-roll, AI visual or mixed

### Step by step

1. Open `downloads/REELS-PRODUCTION-STARTER-KIT.md`.
2. Write the hook first.
3. Use the timing model to limit each section.
4. Read the voiceover aloud.
5. Fill the shot-plan table line by line.
6. Generate/collect visuals only after the shot purpose is clear.
7. Edit to speech rhythm.
8. Prepare caption/CTA/cover separately.
9. Run the five-question QA gate.
10. Export and watch the final file once before publishing.

### Example request

```text
Create a 32-second Reel about why AI product photos look fake.
Audience: beginner creators.
Goal: saves.
Use only these three points: [facts].
Output: timed voiceover + shot plan + visual brief + final QA.
```

### Useful result

You should be able to hand the output to yourself, an editor or a collaborator and start production without asking what comes next.

### Common mistake

Do not use a long article and “cut it down.” Write for speech from the start.

### Next

Use **Reels Director** when you want the AI agent to own the reusable production workflow.

---

## 6. Canva + AI Content Starter Kit

### Headline

**Stop resizing templates. Build one visual system that survives every platform.**

### Best for

Creators who use Canva + AI imagery and need consistent cross-platform production.

### Before you start

Prepare:

- approved content idea
- brand typography/colors
- focal subject
- required outputs
- CTA and destination

### Step by step

1. Open `downloads/CANVA-AI-CONTENT-STARTER-KIT.md`.
2. Write the creative brief first.
3. Build one master visual.
4. Lock hierarchy, spacing and image treatment.
5. Duplicate for each platform.
6. **Recompose** each version; do not only resize.
7. Recheck AI images for artifacts and crop safety.
8. Use the export checklist.
9. Open exported files and inspect them before publishing.

### Example

Master idea: “7 AI image mistakes making your Reels look fake.”

Outputs:

- Instagram 4:5 educational cover
- 9:16 Reel cover
- Pinterest vertical discovery version
- LinkedIn proof-led graphic

Same idea. Different composition and information density.

### Common mistake

Random template selection creates visual inconsistency even when every individual design looks “nice.”

### Next

When the same production system is repeatedly used by a team/client, that is evidence for a deeper **Canva + AI Content Factory** product.

---

## 7. AI Creator OS Starter Map

### Headline

**See the whole machine before you automate one piece of it.**

### Best for

Anyone who wants to understand how all toolkit parts connect.

### Step by step

1. Open `downloads/AI-CREATOR-OS-STARTER.md`.
2. Start with one real content signal.
3. Move through the nine layers in order.
4. Record the artifact produced by each layer.
5. Do not automate a layer until its manual version works.
6. After publishing, feed real performance back into measurement.
7. Expand only winners with actual proof.

### Useful result

You should finish with a traceable chain:

```text
source
→ opportunity
→ brief
→ draft
→ creative
→ QA decision
→ live content
→ real metrics
→ next test
```

### Common mistake

Skipping from “trend” directly to “publish” removes the strategy and QA layers that make the system useful.

---

# Part II — Agent Skills

## Install once

Fastest general route:

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

See available skills before installing:

```bash
npx skills add alptugharun/ai-social-media-toolkit --list
```

Install one:

```bash
npx skills add alptugharun/ai-social-media-toolkit --skill reels-director
```

After installation, speak naturally to your agent. The examples below are good first requests.

## Skill-by-skill usage

| Skill | Use it when… | First request to try | Expected result |
| --- | --- | --- | --- |
| **creator-ops** | you want the full creator workflow routed for you | “Route this topic from evidence to a publish-ready Instagram asset, but stop before publishing.” | ordered workflow + correct sub-skill routing |
| **viral-content-radar** | you have trend/outlier evidence to deconstruct | “Analyze these five posts and identify repeatable mechanics without copying them.” | patterns, evidence, original tests |
| **reels-director** | you need a short-form production package | “Turn this evidence into a 32-second Reel with shot plan and QA.” | hook, script, shot plan, visual/edit direction |
| **pinterest-growth-engine** | you need search-led Pinterest planning | “Build a 7-Pin cluster from this keyword evidence and map each Pin to a destination.” | cluster, visual roles, destination plan |
| **pinterest-opportunity-radar** | current Pinterest opportunity evidence matters | “Evaluate these Pinterest signals and separate verified trend evidence from hypotheses.” | evidence-ranked opportunities |
| **content-repurposer** | one strong source must become native assets | “Turn this article into Reel, LinkedIn and Pinterest versions without duplicate copy.” | platform-native derivatives |
| **influencer-fit-auditor** | evaluating a creator-brand match | “Audit this creator for campaign fit using these audience/campaign facts.” | fit, risk, missing evidence, next questions |
| **brand-voice-humanizer** | copy sounds generic/AI-written | “Rewrite this in Brand-Locked mode using these approved examples.” | natural rewrite with facts preserved |
| **signal-to-content** | you need to turn evidence into a testable content idea | “Convert this source into three original content tests and define the metric for each.” | testable angles + measurement |
| **comment-intelligence** | comments contain repeated needs/objections | “Cluster these comments into questions, objections and demand signals.” | audience-language map + content opportunities |
| **agent-skill-safety-auditor** | before installing an unknown third-party skill | “Audit this SKILL.md and scripts before I install them.” | risk findings + stop/pass conditions |
| **github-opportunity-radar** | researching Agent Skill/repo gaps | “Find evidence-backed creator-ops opportunities; penalize overlap with our current skills.” | prioritized gaps + evidence limits |
| **maps-opportunity-radar** | exploring local/maps workflow opportunities | “Evaluate these local intelligence ideas and reject generic Maps wrappers.” | scored opportunities + feasibility |
| **maps-policy-guard** | any Maps/Places/Street View design might cross data-policy lines | “Review this proposed local-business workflow for scraping/storage/attribution risks.” | policy risks + safer architecture |
| **local-business-intelligence** | turning permitted local/owned signals into action | “Use these authorized business signals to identify content and market opportunities.” | local insights + action plan |
| **commercial-opportunity-radar** | comparing possible paid/service lanes | “Compare these three product ideas using buyer clarity, recurring need and proof.” | commercial prioritization, not revenue forecast |
| **monetization-architect** | you already have value and want a staged paid path | “Design the smallest paid test around this proven workflow.” | open-core → service → recurring product ladder |

## Important

The skill name is not magic. Better input produces better work.

When possible include:

- audience
- objective
- platform
- evidence
- constraints
- available assets
- definition of success

---

# Part III — Python Tools

Clone the repository first if you want to run the local Python tools:

```bash
git clone https://github.com/alptugharun/ai-social-media-toolkit.git
cd ai-social-media-toolkit
```

The tools are designed to use Python's standard library unless the individual tool documents an external API.

## 1. Skill Installer

**Job:** place selected Agent Skills into supported runtime folders.

Preview first:

```bash
python tools/install_skills.py --target codex --scope user --skill reels-director --dry-run
```

Install:

```bash
python tools/install_skills.py --target codex --scope user --skill reels-director
```

Use `--force` only when replacing an existing installed copy is intentional.

---

## 2. Social Outlier Analyzer

**Job:** rank your own posts against your own median baseline.

Required CSV columns:

```csv
platform,post_id,views,likes,comments,shares,saves
```

Run:

```bash
python tools/outlier_score.py examples/social-outlier-posts.csv --top 5
```

Output includes:

- outlier score
- view multiple
- engagement multiple

Use it to decide what deserves qualitative analysis. Do not treat the score as an algorithm prediction.

---

## 3. Signal-to-Content Opportunity Scorer

**Job:** decide which content opportunity deserves production first.

Required CSV columns:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
```

Each numeric field is 0–100.

Run:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --top 3
```

Use the output as a prioritization aid, then apply human judgment.

---

## 4. GitHub Opportunity Radar

**Job:** create an evidence-aware report on Agent Skill / AI repository opportunity lanes.

Run:

```bash
python tools/github_growth_radar.py --output github-opportunity-radar.md
```

Optional: set `GITHUB_TOKEN` in your environment for authenticated GitHub API access.

Output:

- demand/supply proxies
- fast-rising repositories
- skill-gap candidates
- packaging checks
- evidence limits

It does not provide exact GitHub search volume.

---

## 5. Maps Opportunity Radar

**Job:** research higher-level Maps/local-intelligence product opportunities.

Run:

```bash
python tools/maps_opportunity_radar.py --output maps-opportunity-radar.md
```

Use the result together with **Maps Policy Guard** before building anything that stores or redistributes Maps-derived content.

---

## 6. Pinterest Visibility Radar

**Job:** combine official Pinterest trend data when authenticated access exists with ecosystem signals.

Run:

```bash
python tools/pinterest_growth_radar.py --output pinterest-visibility-radar.md
```

Environment variables:

- `PINTEREST_ACCESS_TOKEN` — required for authenticated live Pinterest Trends data
- `PINTEREST_REGIONS` — optional region list
- `PINTEREST_TRENDS_LIMIT` — optional result limit
- `GITHUB_TOKEN` — optional authenticated GitHub API access

No token means no fabricated live Pinterest trend numbers.

---

## 7. Commercial Opportunity Radar

**Job:** compare monetization/product/service candidates without pretending to forecast revenue.

Run:

```bash
python tools/commercial_opportunity_radar.py --output commercial-opportunity-radar.md
```

Output looks at buyer clarity, repeat need, proof, distribution, feasibility and monetization path.

Use it to decide what to test — not what will definitely make money.

---

## 8. Places Aggregate Market Scanner

**Job:** query Google's official Places Aggregate API for permitted count / place insights.

First test the payload without calling Google:

```bash
python tools/places_market_scan.py \
  --lat 36.8841 \
  --lng 30.7056 \
  --radius 3000 \
  --types cafe \
  --mode count \
  --dry-run
```

For a real API call, set `GOOGLE_MAPS_API_KEY` in your environment.

Do not paste the key into committed files.

---

## 9. Traction & Focus Report

**Job:** separate internal shipping from external adoption proof.

Run:

```bash
python tools/traction_focus_report.py --output traction-focus-report.md
```

It checks weak public signals such as stars/forks/releases plus stronger external participation signals where visible.

The output state is one of:

- BUILD PROOF
- VALIDATE WEDGE
- SCALE WHAT WORKS

---

## 10. Self-Heal Classifier

**Job:** classify a saved GitHub Actions failure log and generate machine-readable + human-readable diagnosis files.

Example:

```bash
python tools/self_heal.py \
  --log failed-job.log \
  --workflow "Validate Agent Skills" \
  --run-id 123456 \
  --run-attempt 1 \
  --json-output diagnosis.json \
  --markdown-output diagnosis.md
```

It can identify patterns such as:

- GitHub API rate limiting
- transient network/HTTP problems
- auth/permission problems
- test regression
- Python syntax/import errors
- missing git context

Unknown failures are not automatically declared safe.

---

# Part IV — GitHub Automations

You normally do **not** run these every day by hand. They live in `.github/workflows/` and execute from GitHub Actions.

## 1. Validate Agent Skills

**Purpose:** protect the baseline.

Checks include:

- skill frontmatter
- JSON manifests
- Python compilation
- unit tests
- installer smoke tests
- creator scoring smoke tests

Use the Actions tab to inspect failures before merging.

## 2. GitHub Opportunity Radar

**Purpose:** refresh the repository's GitHub opportunity research.

Configured daily.

Read its latest `growth-radar` issue rather than rerunning manually unless debugging.

## 3. Maps & Local Intelligence Radar

**Purpose:** track Maps/local-intelligence opportunities and gaps.

Read the latest `maps-radar` issue.

## 4. Commercial Opportunity Radar

**Purpose:** compare commercial lanes without auto-pricing or auto-selling.

Read the latest `commercial-radar` issue.

## 5. Pinterest Visibility Radar

**Purpose:** track official Pinterest trend data when access exists and ecosystem signals otherwise.

Read the latest `pinterest-radar` issue.

If the report says authentication is unavailable, do not reinterpret that as “no trend exists.”

## 6. Automation Health Watch

**Purpose:** detect monitored workflow failure/missing states without creating noise when healthy.

If it opens an issue, inspect the actual affected workflow.

## 7. Self-Healing Automation Guardian

**Purpose:** classify failure evidence, retry only bounded transient cases and escalate persistent failures.

It must never:

- disable tests
- reveal secrets
- auto-merge a repair
- convert unknown failures into blind retry loops

## 8. Traction & Focus Watch

**Purpose:** stop internal activity from being mistaken for traction.

Use its state to decide whether to:

- improve proof
- validate one wedge
- scale a proven workflow

---

# Part V — Three Complete Journeys

## Journey A — Make a Reel

1. Creator Prompt Starter Kit → choose angle.
2. Reels Production Starter Kit → build the production package.
3. Brand Voice Humanizer → clean the script.
4. Content QA Gate → final review.
5. Publish manually.
6. Export real metrics later.
7. Social Outlier Analyzer → compare performance.
8. Winner Expansion → create the next test.

## Journey B — Build Pinterest Traffic

1. Pinterest Opportunity Radar → evidence/hypothesis separation.
2. Pinterest Growth Starter Kit → 7-Pin cluster.
3. Canva + AI Starter → create the visual system.
4. Destination-match check.
5. Publish.
6. Measure saves/outbound clicks.
7. Expand the winner, not every Pin.

## Journey C — Turn a Workflow Into a Paid Offer

1. Use the workflow manually.
2. Collect external use/feedback.
3. Traction & Focus Watch → confirm evidence state.
4. Commercial Opportunity Radar → compare monetization paths.
5. Monetization Architect → design smallest paid test.
6. Use Growth & Productization Gates.
7. Only productize after real buyer/repeat-use evidence.

---

# Troubleshooting

## “I installed a skill but my agent does not use it.”

Check:

1. Did you install to the correct runtime target?
2. Did you choose user vs project scope correctly?
3. Does that runtime discover `SKILL.md` from the chosen path?
4. Can you see the skill in the runtime's own listing/inspection UI?
5. Restart the agent/session if the host requires it.

See `docs/INSTALLATION.md`.

## “The AI output is generic.”

Provide:

- one real audience
- one real objective
- evidence
- constraints
- approved voice examples

Then run **Brand Voice Humanizer** after factual drafting.

## “The radar has huge numbers. Are those search volumes?”

No. Repository result counts are explicitly treated as **supply/competition proxies**, not market search volume.

## “Can I connect everything and auto-publish?”

Technically some systems can. This toolkit intentionally keeps external publishing behind human review until access, mapping, quality and failure behavior are proven.

---

# The One Rule to Remember

**Do not add automation before you have a useful manual workflow. Do not add a paid layer before you have proof that someone values the deeper outcome.**
