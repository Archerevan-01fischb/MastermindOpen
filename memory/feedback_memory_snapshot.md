---
name: Auto-Snapshot Memory After Writes
description: After any write/edit to the mastermind memory directory, call snapshot_memory.py so the change is captured as a plain-file snapshot in your chosen backup target.
type: feedback
---
# Auto-Snapshot Mastermind Memory

**Rule:** After any batch of writes/edits to files under your mastermind memory directory (or to `settings.json`, `.claude.json`, or the mastermind `CLAUDE.md`), run the snapshot script. One call per logical batch is fine — no need to snapshot after every single write mid-batch.

```bash
python "{MEMORY_DIR}/scripts/snapshot_memory.py" "<short-reason>"
```

Replace `<short-reason>` with a 1-3 word tag for what changed (e.g. `session-end`, `new-credentials`, `project-update`, `feedback-added`). The reason is logged and helps future debugging.

**Why:** Plain-file backup layer separate from any system-level backup (e.g. EaseUS, Time Machine). System-level backups catch everything eventually but on their own schedule; these per-session point-in-time snapshots are readable plain files you can diff/restore with any text editor. Snapshots are **never pruned** — disk is cheap, knowing what changed when is invaluable.

**How to apply:**
1. When you finish writing one or more memory files, **run the snapshot command once** before moving on.
2. Don't skip it on the theory that your system backup will catch it. System backups run on their own cadence; these snapshots are plain readable files at a known timestamp.
3. If the script errors (missing drive, etc.), flag it to the user immediately — don't silently continue.
4. On session end (after the final memory save), call it one more time with reason `session-end`.

**Script:** `{MEMORY_DIR}/scripts/snapshot_memory.py` — plain stdlib, no external deps.
**Destination:** Set `SNAPSHOT_ROOT` at the top of the script. Default placeholder: `~/mastermind-snapshots/`. Override to a separate drive for resilience against the primary drive failing.
**Log:** `<SNAPSHOT_ROOT>/snapshot_log.txt` — append-only.
