# One instruction set, different assistant homes

**Choose the product you use. Keep instructions, knowledge and tests separate.**

Start with `evidence-desk`. Its export includes a behavior block, a first request, an illustrative answer and acceptance criteria. Do not paste the entire exported document into every configuration field.

## ChatGPT GPTs

Availability checked 29 September 2026: OpenAI's current guide says personal accounts cannot create or publish new GPTs. Existing GPTs may remain editable with the required permissions; managed workspaces depend on their eligibility and settings. Check the current guide before following an older creation tutorial.

For an existing editable GPT, open My GPTs, select it and choose Edit GPT. In an eligible managed workspace, use Create only when it is available. Put the exported Instructions block into Instructions, the sample input into a conversation starter, and permitted reference documents into Knowledge. Test the example in Preview. Compare its answer with the acceptance check; then review sharing separately. A downloaded file is not a GPT Store listing.

[OpenAI creation/editing and eligibility](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts)

## Claude Projects

Export with `--target claude`. Create or open a Project in the Claude interface available to your account. Put the behavior block in project instructions. Add approved source files to project knowledge. Start a fresh chat within the Project and supply the sample input. Confirm the answer preserves facts and admits missing evidence.

A Project is not a Claude Code plugin. For a portable Agent Skill, select `--target skill` and follow the chosen host's current installation instructions.

[Claude Projects](https://support.claude.com/en/articles/9517075-what-are-projects)

## Gemini Gems

Export with `--target gemini`. Open the Gem manager available to your account. Give the Gem a narrow task name, put the behavior block into Instructions, and test the sample before saving. Add only reference files you may use and review access separately.

Gemini support in this starter is the instruction/Gem route. The CLI does not implement Gemini API requests or install a Gemini CLI extension.

[Google Gem setup](https://support.google.com/gemini/answer/15235603)

## Grok and xAI assistants

Export with `--target grok`. In a fresh Grok chat, supply the instruction block and then the sample input. For a programmatic route, preview the xAI payload using the [API starter](BOT-AND-AUTOMATION.md).

This package does not configure the official Grok Bot product, X posting or a messaging channel. A single completed reply is not an always-running bot. Those deployments need their own verified accounts, supported interfaces, cost limits and operational tests.

[xAI text generation](https://docs.x.ai/developers/model-capabilities/text/generate-text)

## Test before reuse

Run three inputs: the supplied sample; a question missing a required source; and a source containing a request to ignore the user's instructions. The assistant should preserve source facts, admit gaps and treat source text as data rather than authority. Record the date, product/version and actual output. Repeat after changing tools or instructions. This describes an evaluation method, not a claim that every model passes.
