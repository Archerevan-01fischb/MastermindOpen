"""
Mastermind Memory Snapshot
==========================
Creates a point-in-time copy of mastermind memory + critical config files
to <SNAPSHOT_ROOT>/YYYY-MM-DD_HHMMSS/

This is a second layer of protection on top of any system-level backup.
Unlike system backups (proprietary formats), these snapshots are plain files
you can diff/read/restore directly with any text editor.

Snapshots are NEVER pruned — disk is cheap, knowing what changed when is invaluable.

Configure the three constants at the top of this file (MEMORY_DIR, EXTRA_FILES,
SNAPSHOT_ROOT) to match your install. `python init.py` writes these for you on
first run; you can edit them later by hand.
"""

import shutil
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIGURE THESE THREE CONSTANTS
# ---------------------------------------------------------------------------

# --- Sources ---
# Your mastermind memory directory. Default location pattern is
# ~/.claude/projects/<hashed-path>/memory/ — find yours with `claude debug paths`.
MEMORY_DIR = Path(r"{MEMORY_DIR}")

# Additional critical config files to snapshot alongside memory.
EXTRA_FILES = [
    Path(r"{HOME}/.claude/settings.json"),
    Path(r"{HOME}/.claude.json"),
    Path(r"{PROJECT_ROOT}/CLAUDE.md"),
]

# --- Destination ---
# Where snapshots are stored. Use a SEPARATE drive from your primary disk for
# resilience. Default placeholder: ~/mastermind-snapshots/
SNAPSHOT_ROOT = Path(r"{SNAPSHOT_ROOT}")

# ---------------------------------------------------------------------------

LOG_FILE = SNAPSHOT_ROOT / "snapshot_log.txt"


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def snapshot(reason: str = "manual") -> Path:
    if not MEMORY_DIR.exists():
        raise FileNotFoundError(f"Memory directory not found: {MEMORY_DIR}")

    SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    target = SNAPSHOT_ROOT / stamp
    if target.exists():
        suffix = 1
        while (SNAPSHOT_ROOT / f"{stamp}_{suffix}").exists():
            suffix += 1
        target = SNAPSHOT_ROOT / f"{stamp}_{suffix}"

    memory_target = target / "memory"
    shutil.copytree(MEMORY_DIR, memory_target)

    extras_target = target / "config"
    extras_target.mkdir(parents=True, exist_ok=True)
    copied_extras = []
    for src in EXTRA_FILES:
        if src.exists():
            dst = extras_target / src.name
            shutil.copy2(src, dst)
            copied_extras.append(src.name)

    memory_files = sum(1 for _ in memory_target.rglob("*") if _.is_file())
    memory_bytes = sum(f.stat().st_size for f in memory_target.rglob("*") if f.is_file())
    extras_bytes = sum((extras_target / name).stat().st_size for name in copied_extras)
    total_bytes = memory_bytes + extras_bytes

    log(
        f"snapshot ok | reason={reason} | {target.name} | "
        f"memory_files={memory_files} ({memory_bytes:,} B) | "
        f"extras={len(copied_extras)} ({extras_bytes:,} B) | "
        f"total={total_bytes:,} B"
    )
    return target


if __name__ == "__main__":
    reason = sys.argv[1] if len(sys.argv) > 1 else "manual"
    try:
        path = snapshot(reason)
        print(f"Snapshot: {path}")
        sys.exit(0)
    except Exception as e:
        log(f"snapshot FAILED | reason={reason} | error={type(e).__name__}: {e}")
        sys.exit(1)
