---
name: MCP Config File Location
description: User-level MCP servers go in ~/.claude.json (NOT ~/.claude/mcp.json). Wrong file = servers silently don't load.
type: feedback
---

When adding MCP servers at user scope, use `claude mcp add -s user` which writes to `~/.claude.json`. Do NOT manually edit `~/.claude/mcp.json`.

**Why:** Multiple sessions have "discovered" that an MCP config was in the wrong file and "fixed" it. Each time `claude mcp list` shows ✓ Connected afterward, but tools still don't load on restart. The config file location is one factor, but **`claude mcp list` showing ✓ Connected is NOT proof tools will load.** The only valid confirmation is `ToolSearch` returning actual tool definitions after a fresh restart.

**How to apply:**
- Always use `claude mcp add -s user` or `-s project` rather than manually editing config files.
- NEVER treat `claude mcp list` showing ✓ Connected as proof tools will load — it doesn't mean that.
- If MCP tools don't appear in `ToolSearch` after restart, do NOT re-diagnose the config file issue. Move to a different diagnostic path (logs, direct API curl, etc.).
