---
name: memory-hygiene-protocol
description: "⭐ How to keep mastermind memory lean and unpolluted. Tiered by recency (like human memory). Hygiene runs automatically on triggers."
metadata:
  node_type: memory
  type: feedback
---

# Memory Hygiene Protocol

## Why this exists

Mastermind memory accumulates faster than it shrinks. The textbook failure mode the research literature calls **context pollution** (or the "Day 30 problem") happens when memory keeps adding facts but never demotes stale ones. A `session_log.md` that grows to 1,500 lines spanning a month, with last month's dead deadlines still pinned at the top of "Where We Left Off," is the canonical example. Memory fails not because anything was forgotten but because **nothing was demoted**.

This file is the protocol so that doesn't happen.

## The five tiers (hour/day/week/month/year framing)

| Tier | Frame | What lives here | Always loaded? | Where on disk |
|---|---|---|---|---|
| **Working** | "last hour" — what I'm doing right now | Active task state, mid-session decisions | Yes (in conversation context) | conversation only |
| **Short-term** | "today / yesterday" | Today's session log + pickup notes for tomorrow | Yes (auto-read on session start) | `session_log.md` |
| **Medium-term** | "this week" | Live todo list + active project state | Yes (auto-read on session start) | `todo.md`, `MEMORY.md` index, ⭐-flagged memory files |
| **Long-term** | "this month / quarter" | Stable preferences, project decisions, references | On demand (loaded when topic comes up) | non-⭐ memory files |
| **Archive** | "this year+" | Raw old session logs, superseded decisions, historical snapshots | Cold — only loaded if explicitly asked | `session_archive/`, `archived/superseded` section of MEMORY.md |

**Why this maps to expert consensus** (research circa 2026): the field has converged on 3-4 tier splits — working / episodic / semantic / archive. Letta/MemGPT call it core/recall/archival; Mem0 calls it user/session/agent scope; Generative Agents adds reflection-driven promotion between tiers. The tier structure isn't the hard part — **the demotion rules are**.

## Promotion and demotion rules

### Promotion (rare, deliberate)
- A fact promotes from short-term → long-term when it's been referenced twice in different sessions AND won't change in the next month. (Single-use facts don't deserve a memory file.)
- A long-term memory promotes to ⭐ in MEMORY.md when getting it wrong would cause real harm (medical, financial, safety, identity).
- Promotion is always deliberate — say "I'm going to save X as a memory because Y" before doing it.

### Demotion (frequent, automatic)
- **Session log entries older than 3 days → `session_archive/session_log_YYYY-MM.md`** at next session start. Today's session and yesterday's stay in `session_log.md`. Older move to a month-bucketed file.
- **Todo items marked `[x]` more than 2 weeks ago → delete entirely.** They're recoverable from `git log` of the memory dir if ever needed.
- **Dated action items (deadlines, "by Apr 17") → move to "Archived/Expired" section the day after the date passes.** Do NOT leave expired deadlines in "Where We Left Off." This is the rule that prevents the "Day 30 problem" — a dead promo deadline rotting in active context for a month.
- **Superseded decisions → delete.** Git diff of the memory dir is the audit trail. Only keep a superseded note if the *transition* itself is what's interesting (a strategy reversal worth remembering as a lesson), in which case rewrite the memory to be about the lesson, not the dead fact.

### Delete is the default. Forgetting is a feature, not a bug.

One of the genuine superpowers computers have over humans is the ability to forget cleanly. Humans can't expunge a dead deadline, an old grudge, or a stale strategy — it haunts them. A machine can. Don't import enterprise "audit-everything" thinking into a personal mastermind.

**Default: delete.** Git history of the memory directory is the audit trail. If the dead fact is ever needed back, `git log` finds it. The active memory should never carry corpses.

**Supersede-don't-delete only applies in these narrow cases:**
- The old fact is still being actively referenced in conversations or todos for the next ~2 weeks (e.g. "the bank was X, now it's Y" — keep both briefly so cross-references make sense).
- The supersession itself is interesting (a strategy reversal, a rolled-back decision, a "we tried this and it failed" lesson). In that case, the lesson is what gets kept — not the dead fact.

**Everything else: delete it.** Including:
- Expired deadlines
- Closed support cases, finished appointments, completed errands
- "Where We Left Off" items from past sessions that are now done or moot
- Wrong guesses made earlier in a session once the right answer is in

Git's `log --diff-filter=D` on the memory dir gives the recovery path if the deletion turns out wrong.

## Trigger conditions — when hygiene runs

Hygiene is **event-driven**, not scheduled. Triggers:

1. **⭐ Pre-shutdown (Claude-mediated shutdown — the primary trigger).** When a shutdown trigger fires (Telegram DM, terminal message, HA dashboard button per [[feedback_shutdown_via_claude]]), the pre-shutdown checklist gates the actual `shutdown /s /t 5`. Hygiene IS part of that gate. Order: (a) run the 2-minute sweep below, (b) snapshot memory, (c) write session_log "shutdown at HH:MM, hygiene clean", (d) ack on the channel the shutdown came in on, (e) only then call `shutdown /s /t 5`.
2. **End of every session** — if `session_log.md` exceeds ~120 lines OR contains entries older than 3 days, run the "session log cycle":
   - Move entries >3 days old to `session_archive/session_log_YYYY-MM.md`
   - Collapse today's multiple entries into one consolidated entry
   - Verify "Where We Left Off" has no dated items past their date
3. **Every memory write** — before saving a new memory, check if an existing one covers the topic. If yes, update in place. Don't write duplicates.
4. **Auto Dream** — Claude Code's built-in consolidation fires on its own (24h + >5 sessions). Let it handle broad cross-session consolidation; the pre-shutdown sweep handles the targeted dated-item cleanup.
5. **On contradiction** — if a memory contradicts current state, delete or rewrite it immediately. Tell the user. Don't silently work around it.
6. **On user flagging bloat** — drop everything and clean.

## Specific items with TTLs (write these explicitly)

When a memory has a natural expiry date, write it into the frontmatter:

```yaml
---
name: foo
expires_at: 2026-04-17   # promo deadline, appointment, etc.
on_expire: archive       # or "delete" for raw logs
---
```

Then the end-of-session hygiene check should grep `expires_at` against today's date and act.

**Categories that should always have explicit expiries:**
- Promotional deadlines
- Appointment dates
- "Follow up by X" reminders
- Trial / cycle-end markers
- Pending replies waiting on someone else

## What NOT to put in memory at all

- Code patterns / file paths / architecture — derivable from project state.
- Git history / who-changed-what — `git log` is authoritative.
- Debugging fix recipes — the fix is in the code; the commit message has context.
- Ephemeral task state — that's what `todo.md` is for, not memory files.
- Activity logs / "summary of what we did this month" — that's what `session_archive/` is for.
- **Long diagnostic transcripts** — keep ONE consolidated entry per work session, not one per investigation step.

## How to keep the always-loaded surface small

The mastermind auto-loads `MEMORY.md` (index), `session_log.md`, `todo.md`, and any ⭐-flagged items referenced in MEMORY.md. That's the **working set**. Rules:

- MEMORY.md stays under 200 lines (it's truncated past 200 anyway).
- Use one-line entries in MEMORY.md with `[[link]]` to the real file. Don't write content into MEMORY.md.
- ⭐ flag is for "load-this-or-you'll-cause-harm" memories only. Everything else is on-demand.
- If MEMORY.md is approaching 200 lines, **prune the index**, don't shrink fonts. The right move is usually consolidating multiple sub-files into one topic file.

## The 2-minute end-of-session sweep

Before snapshot and shutdown, run this checklist mentally (or as a real script later):

1. Is `session_log.md` > 120 lines? → Archive old entries.
2. Are there dated items in "Where We Left Off" whose date has passed? → Move them to "Archived/Expired."
3. Did I write any new memory this session? → Verify no duplicates, verify it's in MEMORY.md, verify ⭐ only if critical.
4. Did anything I learn this session contradict an existing memory? → Mark `superseded_at`, don't silently work around it.
5. Are there `[x]` items in `todo.md` older than 2 weeks? → Delete them.

Five questions. Should take 2 minutes.

## Related
- [[feedback_memory_snapshot]] — when to call `snapshot_memory.py`
- [[feedback_automation_categories]] — event-driven OK, scheduled needs approval
- [[feedback_global]] — general working style
