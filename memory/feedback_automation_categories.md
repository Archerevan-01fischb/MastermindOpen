---
name: Automation Categories (Startup / Event / Scheduled)
description: Three-category framework for deciding when automation is allowed without per-call approval.
type: feedback
---
# Automation Categories — When to Run Things Without Asking

## Category 1 — Startup automation → YES (Active Resume)

**What it means:** Things that run at session start to bring the mastermind back online primed for in-flight work.

**Rule:** Run the approved startup hooks listed below every session. The goal is a substantive resume — *"Picking up — X. Status: Y. Next step: Z."* — not a generic greeting and not a silent idle.

**Why:** Without active resume, the user has to remind the mastermind what we were working on every single session. With persistent memory and a wake-up signal in place, the right behavior is for Claude to actively reload context, verify state, and be ready to push the work forward the moment the user engages.

**Approved startup hooks (run every session start):**
1. **Passive context loading** — read `MEMORY.md`, `session_log.md`, `todo.md`.
2. **Most-recent active project memory** — identify what we were last on from session_log, read that project's memory file in full.
3. **Surface pending alerts** — check any `pending_*.md` files (see [[pending_alerts_template]]); surface non-empty content.
4. **Active state verification** — ping the relevant system (HA, VPS, etc.), check the relevant file, run the relevant status command. **Targeted to the in-flight work, NOT a full dashboard sweep.**
5. **Substantive resume opening** — *"Picking up — [topic]. Status: [...]. Next step: [...]."* — never a generic greeting.
6. **Boot ping** (if startup-chain installed) — fires from `StartMastermind.bat` (and AHK launcher) on PC boot, so the user knows the boot chain completed.

**Hard limit:** whole-project dashboards (multi-system sweeps across all projects) do NOT run on startup — only when asked. Hook #4 is *targeted* state verification, not exhaustive.

**Adding new hooks:** propose to the user, get per-action sign-off, append to the list with a one-line note.

## Category 2 — Event-driven automation → YES

**What it means:** Things that run in direct response to a specific in-session event — where the "trigger" is a clear work-related action, not a clock or a startup hook.

**Rule:** Run these without per-call approval. They're implicit in the work the user is already doing.

**Examples:**
- **Memory snapshot after a write** → `snapshot_memory.py` runs after any batch of writes to the memory dir (see [[feedback_memory_snapshot]])
- **Re-running tests** after editing code if a test suite is active in the project
- **TTS broadcast** via Home Assistant when the user says "announce X on the kitchen speaker"
- **Recomputing a dashboard HTML** after fetching fresh data the user asked for

**Why this is fine:** The event that triggers the automation is itself an explicit request or action the user started. The automation is part of doing that thing correctly, not a new thing.

**Limits:**
- The trigger must be narrow and clear — don't turn every Bash command into a trigger for other commands.
- If the event-driven action has side effects on shared state (sending messages, touching external services) it still needs the normal judgment check from the "Executing actions with care" section of the system prompt.

## Category 3 — Scheduled / cron-like automation → NO by default

**What it means:** Things that run on a clock — "every hour check X", "at 4 AM run Y", "once a day rebuild Z".

**Rule:** Don't set these up without the user's explicit, per-job approval. If the user says "yes set that cron up", fine. Otherwise no.

**Why:** Scheduled jobs run in the background forever and the user needs to know they exist, what they do, and where they log, so they can disable them if needed. Silently-created cron jobs are a nightmare to audit later.

**Exception:** The system prompt's `ScheduleWakeup` tool for dynamic-pacing loops is fine when the user has invoked `/loop` — that's not a hidden cron, it's a tool they asked for.

## Quick decision rule when considering "should I run this automatically?"

1. **Is this a session-start action that primes me for in-flight work?** → YES, run it (Category 1, run the approved-hooks list).
2. **Did the user just ask me to do Thing A, and running Thing B automatically is part of doing Thing A correctly?** → YES (Category 2).
3. **Am I thinking of setting up a timer / cron / recurring job?** → Ask first (Category 3).
4. **Is this a startup action NOT on the approved-hooks list — like an unrelated dashboard?** → No, don't run it on startup; only when asked.

## Related memories
- [[feedback_memory_snapshot]] — concrete Category 2 example (auto-snapshot after memory writes)
- [[feedback_global]] — general behavior rules
- `CLAUDE.md` (mastermind root) Core Behavior section references this framework
