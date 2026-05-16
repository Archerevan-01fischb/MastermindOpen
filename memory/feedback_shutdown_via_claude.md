---
name: shutdown-via-claude
description: "⭐ When the user signals end-of-day (Telegram, terminal, or HA-dashboard token), mastermind runs the hygiene + save checklist and issues shutdown itself. Every shutdown is Claude-mediated."
metadata:
  node_type: memory
  type: feedback
---

# Shutdown via Claude — always, not just remotely

## The rule
When the user signals end-of-day **on any channel I'm listening to**, I run the pre-shutdown checklist and issue `shutdown /s /t 5` myself. They do not use the Windows Start-menu shutdown. Every shutdown is Claude-mediated.

**Why:** Every shutdown becomes a forced demotion checkpoint + state-save checkpoint. No orphaned in-flight work. No month-old polluters surviving because shutdown bypassed me. Quote from the user when this rule was adopted: *"I will explicitly shut down the computer through you which will allow you to perform all of your saves and hygiene before shutting down the computer every time."*

## Trigger phrases (treat as shutdown intent)
The trigger is a Telegram DM from the user OR a message typed into the local terminal OR an HA-dashboard token. Either way, recognize ANY of these (case-insensitive, as substring or whole message):

**Shutdown:**
- `shut down` / `shutdown`
- `power off` / `power down`
- `turn off the PC` / `turn off PC`
- `good night` / `goodnight` / `g'night` / `night` (alone or with "Claude")
- `I'm done` / `I'm out` / `I'm out for the day` / `done for the day` / `done for the night`
- `wrap up and shut down` / `wrap up`
- `kill the PC` / `kill it` (when context is end-of-day)
- `[HA-SHUTDOWN-REQUEST]` — distinctive token from HA's dashboard button. Unambiguous; never appears in normal chatter.

**Reboot:**
- `reboot` / `restart`
- `reboot the PC` / `restart the PC` / `reboot PC` / `restart PC`
- `cycle the PC` / `power cycle`
- `[HA-REBOOT-REQUEST]`

Things that are NOT triggers (common false positives — do not act on these):
- "shut down the server" / "shutdown service X" / "kill the cron" — qualified shutdown of something other than this PC
- "shutdown sequence work" / "shutdown project" / discussion ABOUT shutdown wiring
- "good night X" said to another person quoted in a message
- "restart the conversation" / "restart Claude" → restart Claude only, NOT a PC reboot (handle separately if user ever asks)

If ambiguous, ask once: "shutting down the PC — confirm?" — don't act without confirmation.

## How to apply (the runbook)
When the trigger fires:

1. **Hygiene sweep** (per [[feedback_memory_hygiene]] §"The 2-minute end-of-session sweep"):
   - session_log >120 lines OR entries >3 days old → archive
   - Dated items in "Where We Left Off" past their date → delete
   - New memories this session → confirm registered in MEMORY.md, no duplicates
   - Contradictions noticed this session → delete/rewrite the stale memory
   - `[x]` items in todo.md older than 2 weeks → delete

2. **Confirm no in-progress critical state**: no mid-deploy, no uncommitted edits to load-bearing files, no background bash agents just spawned.

3. **Append session_log entry**: "shutdown via {Telegram | local | HA-bridge} at HH:MM, hygiene clean, no in-flight work, powering off."

4. **Memory snapshot**:
   ```
   python "{MEMORY_DIR}/scripts/snapshot_memory.py" "pre-shutdown"
   ```

5. **Ack on the same channel** the request arrived on — if Telegram, reply on Telegram; if local terminal, just print. Message: `"hygiene clean, snapshot taken, shutting down in 5s — reply 'cancel' to abort"`.

6. **Issue shutdown with grace window**:
   ```
   shutdown /s /t 5
   ```
   The 5-second window is the cancel beat. If the user sends "cancel" / "wait" / "abort" within the window, run `shutdown /a` to abort.

## Edge cases
- **In-flight critical work** (mid-deploy, mid-build, mid-large-edit): delay shutdown, reply "X is still running — wait, or override?" rather than power-cut.
- **Telegram message arrives but the bot lost connection earlier**: might not be seen. Boot pings are the trust signal — if the user gets the "Claude up" ping at boot, the channel is live.
- **PC is on but Claude is dead** (process crashed, terminal closed): Telegram path is dead. Fallback to the HA SSH shutdown button in the HA Companion dashboard — see `shutdown-chain/README.md`.
- **OS-forced shutdown / power loss / crash**: can't be gated. Auto Dream + end-of-session sweep catch these gaps eventually.
- **`shutdown` typed literally in a shell by the user**: bypasses me. Don't lecture; the "always via Claude" thing is a habit they're building, not enforced.

## Reboot variant
Same recognition + checklist, but issue `shutdown /r /t 5` instead.

## Related
- [[feedback_memory_hygiene]] — the hygiene sweep that runs in step 1
- [[feedback_memory_snapshot]] — snapshot_memory.py usage
- `shutdown-chain/README.md` — HA SSH fallback (for when Claude is dead)
- `startup-chain/README.md` — boot pings + trust signal
