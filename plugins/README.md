# Plugins

Claude Code plugins are bundles that ship MCP servers, slash commands, and skills as a package. The mastermind setup uses a small number of them — listed below.

## Plugins enabled in the default mastermind config

| Plugin | Purpose | Marketplace name |
|---|---|---|
| Telegram channel | Inbound DMs from your phone + outbound bot pings | `telegram@claude-plugins-official` |
| rust-analyzer LSP (optional) | Rust LSP integration for in-Claude-Code linting/jumps | `rust-analyzer-lsp@claude-plugins-official` |

Plugins are enabled via the `enabledPlugins` block in `~/.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "telegram@claude-plugins-official": true
  }
}
```

`init.py` writes the right entries based on which integrations you enabled during setup.

## How to discover other plugins

From within Claude Code, the `/help` skill links to the plugin marketplace. You can also browse https://claude.com/code/plugins (canonical URL subject to change — check the docs).

## Should you enable more?

Default no. Plugins ship as opt-in for a reason: each one adds tools, slash commands, and possibly hooks that change how mastermind behaves. Add one only when you have a concrete use case.

## Per-plugin setup

- **Telegram** — see [telegram-channel-setup.md](telegram-channel-setup.md) for the full end-to-end pairing flow.
- Other plugins typically have a README in the marketplace listing. Follow it.

## Common gotcha

- **`bun` in PATH:** the Telegram channel plugin (and many others) require `bun` to be installed and on PATH. If a plugin silently isn't responding, run `where bun` (Windows) / `which bun` (POSIX) first — if it's not found, install bun.
