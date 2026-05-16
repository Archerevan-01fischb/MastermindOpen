# Automation Categories

Three-category framework for "should this run without asking the user?"

| Category | What | Approval needed? |
|---|---|---|
| 1. Startup | Active resume hooks at session start | **No** (run the approved list) |
| 2. Event-driven | Direct response to in-session action | **No** (it's part of the action) |
| 3. Scheduled / cron | Background timers, recurring jobs | **Yes** — per-job approval |

## Category 1 — Startup automation (Active Resume)

Approved hooks that run every session start:

1. Read `MEMORY.md`, `session_log.md`, `todo.md`.
2. Identify most-recent active project from session_log; read its memory file in full.
3. Surface non-empty `pending_*.md` files.
4. Verify the state of in-flight work (targeted — ping the relevant system, check the relevant file).
5. Open with substantive resume: *"Picking up — X. Status: Y. Next step: Z."*
6. (If startup chain installed) Boot ping fired from `StartMastermind.bat`.

**Hard limit:** no whole-project dashboard sweeps on startup — those run only when asked. Hook #4 is targeted, not exhaustive.

**Adding new hooks:** propose first, get sign-off, then append.

## Category 2 — Event-driven automation

Runs in direct response to a specific in-session event. The trigger is a work-related action the user just did or asked for, not a clock.

Examples:
- Memory snapshot after a write (the snapshot is part of doing the write correctly)
- Re-running tests after a code edit if a suite is active
- TTS broadcast when the user said "announce X on the kitchen speaker"
- Re-rendering a dashboard after fetching fresh data

**Why this is fine:** the trigger is itself an explicit request. The automation is part of doing the thing correctly, not a new thing.

**Limits:** the trigger must be narrow. Don't turn every Bash command into a trigger for other commands. Side effects on shared state (sending messages, touching external services) still need the normal judgment check.

## Category 3 — Scheduled / cron-like

Don't set these up without explicit per-job approval. Why: scheduled jobs run forever in the background. The user needs to know they exist, what they do, where they log, and how to disable them. Silently-created cron jobs are a nightmare to audit.

**Exception:** `ScheduleWakeup` for `/loop` is fine — it's a tool the user invoked, not a hidden cron.

## Decision rule when in doubt

1. Session-start action priming me for in-flight work? → YES, Category 1.
2. Part of doing something the user just asked for? → YES, Category 2.
3. Setting up a timer / cron / recurring job? → Ask first. Category 3.
4. Startup action NOT on the approved list (random dashboard)? → No — only when asked.

## Read also

- `memory/feedback_automation_categories.md` — canonical rules (verbatim)
- `memory/feedback_memory_snapshot.md` — concrete Category 2 example
- [self-improvement-loop.md](self-improvement-loop.md) — Category 3 + the surfacing pattern
