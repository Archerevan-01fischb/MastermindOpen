# Integrations

Mastermind controls the user's life surface through MCP (Model Context Protocol) integrations. Each integration is opt-in — pick the ones that match how you actually work, skip the rest.

## What is MCP?

MCP is the protocol Claude Code (and Claude Desktop) uses to talk to external services. An MCP server exposes tools (functions Claude can call) and resources (data Claude can read). When you enable an integration here, you're configuring an MCP server endpoint and giving Claude Code permission to call its tools.

## Available integrations

| Integration | What mastermind can do with it | Setup difficulty |
|---|---|---|
| [Telegram](telegram.md) | Inbound DMs (control from your phone), outbound boot/shutdown pings, push notifications | Easy |
| [Gmail](gmail.md) | Read / draft / send / label / search email across multiple accounts | Medium (OAuth) |
| [Google Calendar](google-calendar.md) | Create / update / find events; color-code by event type per `user_calendar_color_schema.md` | Easy (Cloud connector) |
| [Google Drive](google-drive.md) | List / read / search files | Easy (Cloud connector) |
| [Home Assistant](home-assistant.md) | Smart home control, remote PC boot/shutdown via HA, TTS broadcasts | Medium (token + tunnel) |
| [DocuSign](docusign.md) (optional) | Send envelopes for signature, list agreements, track workflows | Hard (sandbox + JWT) |
| [QuickBooks](quickbooks.md) (optional) | Read accounts, create bills/invoices/expenses, generate reports | Hard (Production OAuth) |

## How to enable an integration

1. Read the per-integration guide.
2. Get the credentials it needs (vendor-side OAuth, API token, bot token, etc.).
3. Run `claude mcp add -s user` to register the server — see `mcp-config-examples/` for skeleton configs.
4. Verify with `claude mcp list` showing ✓ Connected.
5. **Then restart Claude Code and verify** with `ToolSearch` that the tools actually appear.

**Important:** `claude mcp list` showing ✓ Connected does NOT mean tools will load. The only proof is `ToolSearch` returning live tool definitions after a fresh restart. See [[feedback_mcp_config_location]] in memory for the why.

## What mastermind does with these (the orchestration value)

Once a few integrations are wired, mastermind starts doing the cross-cutting work that makes a "mastermind" earn the name:

- Reads incoming Gmail, identifies which project an email belongs to, drafts a response
- Sees a Calendar invite, color-codes it per your schema, blocks travel time if you said you commute
- Notices an Assist alert from HA ("dishwasher done"), broadcasts TTS confirmation
- DMs you on Telegram when a long-running task completes while you're AFK
- Files a QuickBooks Journal Entry from a forwarded receipt
- Tracks DocuSign envelope status without you opening DocuSign

Each integration alone is fine. Composed together is where the value compounds.

## Config file locations (gotcha)

User-level MCP servers go in `~/.claude.json`, NOT `~/.claude/mcp.json` — that latter file is ignored by Claude Code despite a tempting name. Always use `claude mcp add -s user` to avoid the wrong-file trap.

See `mcp-config-examples/claude.json.example` for the shape of `~/.claude.json` and `mcp-config-examples/.mcp.json.example` for a per-project `.mcp.json`.

## Smoke tests

Each integration guide ends with a "smoke test" — a one-liner you can run from Claude Code to prove the integration works. Run these BEFORE building anything that depends on the integration. The number of times an integration looks healthy but isn't is high.
