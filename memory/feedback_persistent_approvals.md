---
name: Proactively persist session-scoped approvals
description: When the user approves a non-Bash permission prompt, offer to save it to settings.json since that UI option is session-only for non-Bash tools.
type: feedback
---
When the user approves a permission prompt for a non-Bash tool (WebFetch, MCP tools, Edit, Write, etc.), proactively offer to add it to `~/.claude/settings.json` so they don't have to re-approve next session. Claude Code's "Yes, don't ask again" is permanent for Bash but session-only for everything else — that's the gap.

Trigger: the user approves an ask-prompt for a tool/domain/MCP method they're likely to hit again (news sites, sports sites, recurring MCP calls, repeated file-edit paths). Don't do this for clearly one-off approvals.

If the user says "make that permanent" or "never ask me about X again," do it without further clarification — edit the `permissions.allow` array in `~/.claude/settings.json`. Use domain-scoped WebFetch rules (`WebFetch(domain:example.com)`) and tool-method MCP rules (`mcp__server__*`).

**Why:** The re-prompt-every-session friction is annoying enough that most users will eventually start hitting "Yes, don't ask again" without understanding it expires at session end. Owning the persistence step removes that footgun.

**How to apply:** After the user approves a prompt or when they say "allow X permanently," jump straight to editing settings.json. Brief confirmation is fine — don't ask which file, don't ask permission to edit, don't enumerate options. Just do it and tell them what you added.
