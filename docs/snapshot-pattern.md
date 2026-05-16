# Snapshot Pattern

Why mastermind snapshots its own memory defensively.

## The why (in one sentence)

System-level backups (EaseUS, Time Machine, restic, whatever) catch the memory dir on their cadence, in their proprietary format. Mastermind's per-session plain-file snapshots are point-in-time copies at named timestamps — readable / diffable / restorable with any text editor, regardless of which backup software you run.

## When snapshots fire

Three triggers, all event-driven:

1. **PreCompact hook** — fires when Claude Code is about to compact your conversation context. The snapshot is a defensive checkpoint in case the compaction loses something.
2. **SessionEnd hook (`clear` matcher)** — fires when you type `/clear`. Defensive — `/clear` clears in-conversation memory but not files, but if you'd added context in conversation that should have been a memory and wasn't yet, the snapshot is a recovery path.
3. **SessionEnd hook (`exit` matcher)** — fires when the Claude Code process exits cleanly. The "last known good" snapshot for this session.

Plus manual calls:
4. **Pre-shutdown** — Claude calls it as step 4 of the shutdown checklist.
5. **Post-onboarding** — `init.py` calls it after the Onboarding Wake finishes.
6. **Per-batch in conversation** — when Claude writes one or more memory files, it calls the script once at the end of the batch (per `feedback_memory_snapshot.md`).

## What gets snapshotted

- The entire memory directory (recursive)
- The user's `~/.claude/settings.json`
- The user's `~/.claude.json` (where MCP servers live)
- The mastermind's CLAUDE.md

Each snapshot is a fresh directory at `<SNAPSHOT_ROOT>/YYYY-MM-DD_HHMMSS/`. Snapshots are **never pruned** — disk is cheap, knowing what changed when is invaluable.

## Where snapshots go

Set `SNAPSHOT_ROOT` at the top of `memory/scripts/snapshot_memory.py`. Recommended: a SEPARATE drive from your primary disk (different physical disk or external SSD) so a primary-drive failure doesn't take the snapshots with it.

Defaults during setup:
- Windows: `F:\Mastermind Snapshots\` (external drive) or `~/mastermind-snapshots/`
- macOS / Linux: `~/mastermind-snapshots/` (move to an external mount when you have one)

## The log

Each snapshot appends a one-line summary to `<SNAPSHOT_ROOT>/snapshot_log.txt`:

```
[2026-05-16 12:49:03] snapshot ok | reason=post-plan-approval | 2026-05-16_124901 | memory_files=382 (5,773,875 B) | extras=3 (64,691 B) | total=5,838,566 B
```

If something goes wrong (drive missing, permission error), the log captures the failure and the script exits 1.

## Restoring from a snapshot

The snapshots are plain directories. To restore a memory file:

```bash
cp "<SNAPSHOT_ROOT>/<TIMESTAMP>/memory/<file>" "<MEMORY_DIR>/<file>"
```

To restore the whole memory dir:

```bash
rm -rf <MEMORY_DIR>
cp -r "<SNAPSHOT_ROOT>/<TIMESTAMP>/memory" <MEMORY_DIR>
```

For settings.json restore: copy from `<SNAPSHOT_ROOT>/<TIMESTAMP>/config/settings.json`.

## Why not just use git?

You can — and mastermind's memory dir is often kept in a private git repo too. But:

- **Git is opt-in friction.** You have to commit. People forget mid-session.
- **Snapshots are zero-friction.** The hook fires automatically; no human in the loop.
- **The two compose.** Use git for long-term history + diffs of intentional changes. Use snapshots for catastrophic-recovery checkpoints at every significant event.

## Configuring the snapshot script

After `python init.py`, three constants at the top of `memory/scripts/snapshot_memory.py` should already be filled. If you need to change them later:

```python
MEMORY_DIR    = Path(r"...")   # your memory dir
EXTRA_FILES   = [...]          # additional critical files
SNAPSHOT_ROOT = Path(r"...")   # where snapshots go
```

## Read also

- `memory/feedback_memory_snapshot.md` — when to call the script
- `memory/scripts/snapshot_memory.py` — the script itself
- `settings/settings.json.template` — the hook configuration
