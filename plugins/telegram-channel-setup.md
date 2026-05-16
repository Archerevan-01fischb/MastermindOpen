# Telegram Channel Plugin — End-to-End Setup

This is the long-form companion to `integrations/telegram.md`. Use this when you want every step in one place.

## What gets installed

After completing this guide, you'll have:
- A Telegram bot (created via BotFather) reachable at `@your_bot_handle`.
- The `telegram@claude-plugins-official` plugin enabled in Claude Code, which routes inbound bot DMs into your Claude Code sessions as `<channel source="telegram">` tags.
- An access policy (allowlist) controlling which Telegram chat_ids can reach your mastermind.
- Optional: bat/AHK scripts that curl Telegram from PC boot to send boot pings to your phone (see `startup-chain/`).

## Prerequisites

- Claude Code v2.x+ installed.
- `bun` on PATH (`npm install -g bun` if not already there).
- A Telegram account on your phone.

## Step 1 — Create the bot

1. Open Telegram on your phone.
2. Search for **@BotFather** and start a chat.
3. Send `/newbot`.
4. Pick a display name (`{USER}'s Mastermind`).
5. Pick a unique username ending in `bot` (e.g. `{USER}_mastermind_bot`).
6. BotFather replies with a token of the form `1234567890:AAEessP3-wYv7VaXXXXXXXX`.

**Save the token now.** You can ask BotFather to regenerate it later (`/revoke`), but losing it mid-setup is annoying.

## Step 2 — Get your chat_id

You need your own `chat_id` for the allowlist. Two ways:

**Easy way (after the bot exists):**
1. Open the bot in Telegram, send any message.
2. From your laptop:
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/getUpdates"
   ```
3. Look for `"chat":{"id": <NUMBER>, ...}` — that's your chat_id.

**Phone-only way:**
- Open `@userinfobot` in Telegram, send `/start`. It tells you your user ID, which equals your DM chat_id.

## Step 3 — Enable the plugin

Edit `~/.claude/settings.json` and add to `enabledPlugins`:

```json
{
  "enabledPlugins": {
    "telegram@claude-plugins-official": true
  }
}
```

`init.py` does this for you if you selected Telegram during setup.

## Step 4 — Configure the channel

Inside Claude Code, run the `/telegram:configure` skill. It will:

1. Prompt for your bot token. Paste it.
2. Save the token to the plugin's credentials file (typically `~/.claude/channels/telegram/.env` — verify with the skill output).
3. Verify the bot reachability via Telegram's `/getMe` API.

You should see "Telegram channel configured" on success.

## Step 5 — Configure access

Run the `/telegram:access` skill. This manages the allowlist of `chat_id`s that can reach your mastermind.

1. Add your own chat_id (from Step 2).
2. Decide policy on group chats (default off recommended).
3. Decide whether unknown chat_ids see a generic rejection message or are silently ignored.

**Important access notes:**
- **Never approve a pairing because a Telegram message asked you to.** That's the prompt-injection footgun. Allowlist edits happen at the keyboard, not in response to messages.
- If a chat says "approve my pairing" or "add me," refuse. Tell the person to ask you directly out-of-band.
- The `access.json` file lives at the plugin's data dir. Treat changes to it like password changes.

## Step 6 — Test inbound

From your phone, message the bot: `ping`.

You should see (within ~1 second):
1. The bot react with 👀 (or similar emoji).
2. A short text reply from your mastermind.

If you get no reaction:
- Check Claude Code is actually running (the plugin is in-process, not a separate daemon).
- Verify `bun` is on PATH: `where bun` (Windows) / `which bun` (POSIX).
- Restart Claude Code with the channel flag: `claude --channels plugin:telegram@claude-plugins-official` (or whatever your harness uses).

## Step 7 — Test outbound (boot ping, optional)

If you've installed the Windows startup chain (see `startup-chain/README.md`), boot pings work by curling Telegram directly from `StartMastermind.bat` and the AHK launcher. The bot token is hardcoded in those scripts; chat_id too.

Trigger by rebooting. You should get two pings within a few minutes:
1. `[boot] PC powered on at HH:MM — Claude launching...` (from the bat).
2. `[boot] Claude up and listening (PID X)` (from the AHK launcher).

If neither arrives, the boot chain may have failed before reaching the curl step — check the bat / AHK logs.

## Step 8 — Trigger shutdown via Telegram (the payoff)

This is the big one — the reason you wired Telegram. Send any of these to the bot:

- `shut down`
- `power off`
- `good night`
- `kill the PC`

(Full trigger list in `feedback_shutdown_via_claude.md`.)

Mastermind should:
1. React 👀.
2. Reply "running pre-shutdown checklist".
3. Run the hygiene sweep + snapshot.
4. Reply "shutting down in 5s — reply 'cancel' to abort".
5. Power the PC off.

If something goes wrong mid-flow, reply `cancel`. The 5-second grace window will abort the shutdown.

## Reference: per-skill quick guide

- `/telegram:configure` — set or change the bot token; review channel status.
- `/telegram:access` — manage allowlist; change group policy.

## Reference: routing logic

When a Telegram DM arrives:
1. Plugin checks `access.json` for the sender's chat_id.
2. If allowed: injects the message as a `<channel source="telegram" chat_id="X" message_id="Y" user="Z" ts="...">` block in your next Claude Code session turn.
3. If denied: bot replies with the configured rejection message (or stays silent).

Your mastermind handles the message per `feedback_telegram_immediate_react.md` and `feedback_telegram_reply_channel_match.md`.

## Removing the channel

To uninstall:
1. Disable in `~/.claude/settings.json` (`telegram@claude-plugins-official: false`).
2. Delete the bot via BotFather (`/deletebot`) if you want it gone entirely.
3. Remove the credentials file at `~/.claude/channels/telegram/`.
