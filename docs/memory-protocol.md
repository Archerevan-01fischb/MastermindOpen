# Memory Protocol — in depth

The "Day 30 problem": context pollution from never demoting stale memories. This doc explains how mastermind avoids it.

## The five tiers

| Tier | Frame | Where | Always loaded? |
|---|---|---|---|
| Working | last hour | in-conversation context | yes |
| Short-term | today / yesterday | `session_log.md` | yes |
| Medium-term | this week | `todo.md`, `MEMORY.md` index, ⭐-flagged memories | yes |
| Long-term | this month/quarter | other memory files | on demand |
| Archive | this year+ | `session_archive/`, removed lines (recoverable via git) | cold |

Why five and not three? Research has converged on 3-4 (Letta/MemGPT: core/recall/archival; Mem0: user/session/agent; Generative Agents: working/episodic/reflection). The five-tier split here splits "short-term" and "medium-term" because they have different demotion cadences (3 days vs 2 weeks) and different read frequencies (every session vs on-demand).

## Promotion rules (rare, deliberate)

- A fact promotes from short → long when it's referenced twice in different sessions AND won't change in the next month.
- A long-term memory becomes ⭐ in MEMORY.md when getting it wrong causes real harm (medical, financial, safety, identity).
- Promotion is explicit: say "I'm going to save X as a memory because Y" before doing it.

## Demotion rules (frequent, automatic)

- `session_log.md` entries older than 3 days → `session_archive/session_log_YYYY-MM.md`.
- `todo.md` items marked `[x]` more than 2 weeks ago → **delete** (git log is the audit trail).
- Dated action items → move to "Archived/Expired" the day after the date passes. **This is the rule that catches the Day 30 problem.**
- Superseded decisions → delete, unless the supersession itself is interesting (a strategy reversal worth remembering as a lesson).

## Forgetting is a feature

The default for stale state is **delete**. Don't import enterprise "audit-everything" thinking into a personal mastermind. Git history of the memory directory is the audit trail — if you're ever wrong about deleting, `git log --diff-filter=D` recovers it.

## Triggers — when hygiene runs

Hygiene is event-driven, not scheduled.

1. **Pre-shutdown** — primary trigger. Hygiene sweep runs as part of the shutdown checklist.
2. **End-of-session** — if `session_log.md` > 120 lines or has entries > 3 days, cycle.
3. **Every memory write** — check for duplicates before writing.
4. **Auto Dream** — Claude Code's built-in (24h + >5 sessions).
5. **On contradiction** — delete or rewrite immediately. Tell the user. Don't silently work around.
6. **When the user flags bloat** — drop everything and clean.

## TTL via frontmatter

Mark dated memories with explicit expiry:

```yaml
---
name: foo
expires_at: 2026-04-17
on_expire: archive  # or delete
---
```

The end-of-session hygiene check should grep `expires_at` against today's date.

## The 2-minute end-of-session sweep

Before snapshot + shutdown:
1. session_log.md > 120 lines? Archive.
2. Dated items in "Where We Left Off" past date? Delete.
3. New memories this session? Verify no dupes, in MEMORY.md.
4. Contradictions noticed? Mark superseded.
5. `[x]` todos > 2 weeks? Delete.

## Read also

- `memory/feedback_memory_hygiene.md` — the canonical rules (verbatim in the memory dir)
- `memory/feedback_memory_snapshot.md` — when to call `snapshot_memory.py`
- [snapshot-pattern.md](snapshot-pattern.md) — what the snapshots are for
