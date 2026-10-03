# Integrations Hub

**Choose the lightest integration that actually solves the job.**

| Pattern | Use it for | It is not |
| --- | --- | --- |
| Prompt | reusable instructions | tool access |
| Assistant / Gem / Project | reusable context + instructions | automatic external permissions |
| Agent Skill | portable task procedure | account authorization |
| Plugin / connected app | reusable instructions plus connected tools/data | automatically public |
| MCP | a protocol for exposing tools/context | a permission bypass |
| API assistant starter | code that calls a provider API | an always-running autonomous bot |
| Automation | trigger + state + actions + verification | proof that a future run succeeded |

## Resources

- [MCP & Plugin Guide](MCP-PLUGIN-GUIDE.md)
- [AI Workbench MCP](../packages/ai-workbench-mcp/README.md) — focused read-only MCP product; version `0.1.0a1` is published on PyPI and the official MCP Registry, with package/registry/host evidence tracked separately.
- [Assistant Blueprints](../assistants/README.md)
- [Agent Skills](../skills/README.md)
- [Bot Starters](../bots/README.md)
- [AI Builder Path](../learning/AI-BUILDER-PATH.md) — decide when a job needs a prompt, assistant, Agent Skill, MCP, plugin or automation.
- [Automation Recipes](../automation-recipes/README.md)

## Integration checklist

Before connecting a live account:

1. Define the job.
2. Use the minimum permissions.
3. Test read-only/sample data first.
4. Add approval before risky writes.
5. Make writes idempotent where possible.
6. Read back external state.
7. Store only non-sensitive evidence.
8. Document failure and rollback behavior.
