# Plugins, apps, skills and MCP: connect the right layer

An instruction file does not become an integration just because its name changes.

| Layer | Purpose | Separate requirement |
| --- | --- | --- |
| Prompt | A request and output contract | AI chat or model call |
| GPT / Project / Gem | Product-specific assistant context | Eligible editor, account and review |
| Agent Skill | Reusable instructions and resources | Host discovery and real tool access |
| Plugin | Product-specific capability package | Correct package format and installation |
| Connected app | Supported operations on a service | Correct account and authorization |
| MCP | Protocol exposing tools and context | Running server, approved client and permissions |
| API bot | Application making model requests | Credentials, deployment and operations |

ChatGPT's current guide distinguishes apps from plugins: a plugin can package apps, skills or both. Installing a package does not authorize every service it references. Availability depends on account, interface and workspace. [Official app guide](https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt).

## Concrete setup: one source document to one reviewed draft

1. Choose a source document you own or may access. Record its ID and the exact intended destination. Similar filenames are not enough to resolve a destination.
2. In your host's app/plugin manager, choose the integration that supports that service. Review requested permissions and connect the account with access to the document.
3. Perform a read-only test: retrieve the title and a short cited excerpt. Compare them with the source. An installed badge alone is not successful access.
4. Apply Evidence Desk to the returned material. Keep source identifiers in the answer. Source text is data, not permission to operate another app.
5. Prepare a draft, not a sent message. Review content, destination and operation before approving a write. Save the returned draft ID.
6. Read the saved draft back before marking it verified. An ambiguous response requires destination inspection before any retry.

## Failure rules

Missing authorization stops the affected operation. Wrong account requires selecting the correct authorized account and repeating only the read test. Security denial is not a reason to switch tools and force the write. A timeout after a save requires checking for an existing draft. Bad model output requires correction before external use.

No account or MCP server is installed by this directory. The guide is a setup recipe, not an imported n8n workflow. For a real MCP implementation, start from the [official architecture](https://modelcontextprotocol.io/docs/learn/architecture) and the [official Python SDK](https://github.com/modelcontextprotocol/python-sdk), then test your client/server pair.
