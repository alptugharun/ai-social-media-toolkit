# Agent Plugin ZIP: your first safe result

[Türkçe](PLUGIN-QUICKSTART_TR.md) | [Brand Voice Humanizer instructions](skills/brand-voice-humanizer/SKILL.md)

## What this is
This extracted ZIP is a **skills-only** agent plugin. It contains reusable instructions for creator work, not a hosted AI service, social-media login, or publishing bot. Use it when your agent host can load Agent Skills. If you need one standalone prompt or a working MCP server, this ZIP is not the right starting point.

## Prerequisites and cost
You need an agent host that supports the relevant plugin or skill format. Loading differs by host: follow its official import/skill instructions and confirm that it recognizes `skills/brand-voice-humanizer/SKILL.md`. Inspecting the ZIP needs no key, paid API, or account access. Using a host may require its own account or incur its usual costs. Do not grant write, network, publishing or credential permissions to run this example.

## Exact first action
Extract the ZIP. Read [the skill instructions](skills/brand-voice-humanizer/SKILL.md), then import the package into a compatible agent host or load that skill as the host documents. Keep external account integrations disabled. Use **Audit** mode so the agent comments on the draft without editing or publishing it.

### Safe synthetic first request

```text
Use Brand Voice Humanizer in Audit mode. This is fictional practice copy:
"The imaginary workshop starts on 10 March 2027 at 18:00. A ticket costs 120 TL."
Suggest clearer, more natural wording. Do not rewrite the copy, change
the numbers or date, publish anything, or claim the event is real.
Report observations and any factual-risk warnings.
```

## Expected result and verification
Expect observations about voice and clarity and, where needed, warnings about factual changes. Compare the response with the original sentence. Confirm that **10 March 2027**, **18:00**, and **120 TL** remain intact and that no external action was taken. Host activation and model output must be verified in your actual host; static packaging tests do not establish either.

## Limitations and troubleshooting
The instructions do not verify the event or offer factual correctness. The optional local Rewrite Fact Guard checks selected tokens and protected phrases, **not semantic accuracy**, and needs a suitable Python environment for its separate script. See [the detailed helper guide](skills/brand-voice-humanizer/README.md). If the host cannot find the skill, confirm the extracted `skills/` layout and host import rules. If it cannot activate Audit mode, inspect the skill instructions manually; do not report a successful plugin installation. If the output changes a protected fact, mark the test **FAIL** and review before reuse.

## Privacy, permissions and help
No automatic publishing, account access, remote data collection or elevated permissions are part of this example. Use fabricated input first. Never share credentials or confidential customer material with a host you have not approved. Report a public-safe reproduction in the [repository issue tracker](https://github.com/alptugharun/ai-social-media-toolkit/issues); use the repository security policy for sensitive vulnerabilities. Include host/version, expected result, observed result and whether the test was PASS, FAIL or BLOCKED.
