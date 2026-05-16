# Shutdown Pattern

Why every shutdown goes through Claude, and the fallback when Claude is dead.

## The principle

Every PC shutdown is a forced demotion checkpoint. The hygiene sweep, memory snapshot, and "where we left off" capture happen as part of the shutdown — not as a hopeful "remember to save" reminder. Quote from the user who codified this:

> "I will explicitly shut down the computer through you which will allow you to perform all of your saves and hygiene before shutting down the computer every time."

Result: no orphaned in-flight work. No month-old polluters surviving because shutdown bypassed me.

## The primary path (DM Claude)

```
You type / DM "good night"  (Telegram, terminal, HA-dashboard token)
   ↓
Mastermind recognizes shutdown intent
   ↓
Hygiene sweep (the 5 questions from feedback_memory_hygiene.md)
   ↓
Confirm no in-flight critical work (mid-deploy, mid-build, etc.)
   ↓
Append session_log: "shutdown via {channel} at HH:MM, hygiene clean"
   ↓
python snapshot_memory.py "pre-shutdown"
   ↓
Reply on same channel: "hygiene clean, snapshot taken, shutting down in 5s — reply 'cancel' to abort"
   ↓
shutdown /s /t 5
   ↓
(5s grace window — if user replies "cancel" / "wait", run shutdown /a)
   ↓
PC powers off
```

See `memory/feedback_shutdown_via_claude.md` for the canonical trigger list and runbook.

## Trigger phrases

Recognized as shutdown intent:
- `shut down` / `shutdown`
- `power off` / `power down`
- `turn off the PC`
- `good night` / `goodnight` / `g'night`
- `I'm done` / `I'm out`
- `wrap up`
- `[HA-SHUTDOWN-REQUEST]` (distinctive token from HA dashboard)

NOT shutdown intent:
- "shut down the server" / "kill the cron" (qualified shutdown of something else)
- "good night X" said to another person
- Discussion ABOUT shutdown wiring

If ambiguous, ask once before acting.

## Reboot variant

Same recognition + checklist, but `shutdown /r /t 5`. Triggers: `reboot`, `restart`, `cycle the PC`, `[HA-REBOOT-REQUEST]`.

## The fallback path (HA SSH)

**When to use:** PC is on but Claude is dead. The DM path is gone too. You need to power off without going through Claude.

```
Phone (HA Companion app) → tap "PC Shutdown FORCE" tile
   ↓
HA dashboard runs script.pc_shutdown_force
   ↓
shell_command.pc_shutdown_force
   ↓
ssh <admin>@<pc-ip> "shutdown /s /t 0"
   ↓
PC powers off (NO hygiene — that's the trade-off)
```

The "FORCE" prefix is intentional. It's a verbal signal that this path bypasses the hygiene sweep. Voice Assist aliases use "force shutdown" / "kill the PC" — distinct from the Claude-routed "shut down" / "good night."

See `shutdown-chain/README.md` for the full setup.

## What gets sacrificed in the fallback

- No hygiene sweep before power-off (no last-minute session_log archive, no expired-date cleanup).
- No memory snapshot timestamped to this shutdown.
- The "Where We Left Off" block in session_log.md reflects the LAST normal shutdown, not this one.

Trade-off accepted: better to be able to power off when Claude is dead than to have no off-button.

## Edge cases

- **In-flight critical work** (mid-deploy, mid-build): Claude should refuse and reply "X is still running — wait, or override?" rather than power-cut.
- **Telegram bot offline:** Claude doesn't see the DM. Boot pings (see startup chain) are the trust signal that the channel is live.
- **OS-forced shutdown / power loss / crash:** can't be gated. Auto Dream + end-of-session sweep catch these gaps eventually.
- **`shutdown` typed literally in a shell by the user:** bypasses Claude. Don't lecture — the "always via Claude" habit is preferred, not enforced.

## Read also

- `memory/feedback_shutdown_via_claude.md` — canonical trigger list + runbook
- `shutdown-chain/README.md` — HA fallback setup
- `memory/feedback_memory_hygiene.md` — the 2-minute end-of-session sweep
