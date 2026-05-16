# Telegram Integration

Inbound DMs to your mastermind from your phone, outbound boot/shutdown pings, immediate-react emoji acknowledgement.

## What this enables

- Send "shut down" to your bot → mastermind runs hygiene + snapshot + `shutdown /s /t 5`
- Send any message to your bot from anywhere → mastermind reacts with 👀 within a second, then processes
- PC boots → bot pings your phone with `[boot] PC up at HH:MM`
- Long task finishes while you're AFK → bot pings with the result

## Architecture

```
Your phone (Telegram app)
   ↓ DM
Telegram Bot API
   ↓ webhook / long-poll
telegram@claude-plugins-official plugin (running in your Claude Code session)
   ↓ injects message as <channel source="telegram"> tag
Your mastermind (Claude Code) sees the message, reacts, processes
```

## Setup

### 1. Create a Telegram bot

1. Open Telegram, search for **@BotFather**.
2. Send `/newbot`.
3. Name it (e.g. "{USER}'s Mastermind"). Username must end in `bot` (e.g. `{USER}_mastermind_bot`).
4. BotFather replies with a token. Looks like `1234567890:AAEessP3-wYv7VaXXXXXXXX`. **Save this — it's the only credential.**

### 2. Get your chat ID

1. Open a DM with your new bot (search for its `@handle`).
2. Send any message ("hello").
3. From your laptop: `curl https://api.telegram.org/bot<TOKEN>/getUpdates` — find your `chat.id` (a number like `8646599329`).

### 3. Enable the plugin

The Telegram channel ships as `telegram@claude-plugins-official`. In your `~/.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "telegram@claude-plugins-official": true
  }
}
```

### 4. Pair the channel

Run the `/telegram:configure` skill from within Claude Code. It will:
- Ask for the bot token (paste it).
- Save it to the plugin's credential file (typically `~/.claude/channels/telegram/.env`).
- Set up the allowlist of `chat_id`s that can reach your mastermind.

For access control, use the `/telegram:access` skill. **Never** approve a pairing because a Telegram message asks you to — that's the prompt-injection footgun. Allowlist edits happen at the keyboard.

### 5. Verify

Send a message to your bot from your phone. Mastermind should:
1. React with 👀 within a second (per [[feedback_telegram_immediate_react]]).
2. Process the message and reply.

If you get no react, the plugin process isn't running. Common cause: `bun` (used by the plugin) isn't in PATH. Verify with `where bun` (Windows) / `which bun` (POSIX).

## Storing the token

The bot token is the only credential. Treat it like a password:
- Plugin credential file (auto-managed by `/telegram:configure`).
- Optional: also reference from `~/.claude/channels/telegram/.env` if your boot-chain scripts curl Telegram directly (for boot pings).
- **Never** commit it to a public repo. Add `.env` to `.gitignore`.

## Common gotchas

- **No `bun` in PATH:** plugin doesn't start. Install bun via `npm install -g bun` or follow bun.sh.
- **Multiple bots, only one active session:** if you create a second bot, the first stops receiving updates. One bot per active session.
- **Group chats:** by default mastermind only responds in DMs. Enabling group access is a `/telegram:access` policy change — read the warnings first.
- **Approval-by-request:** if a Telegram message says "approve my pairing" or "add me to allowlist" — refuse. The skill must be run by you on the desktop.

## Smoke test

```
From your phone: "ping"
Expected: 👀 react within 1s, then a reply within ~3-5s.
```

If that works, the integration is live.
