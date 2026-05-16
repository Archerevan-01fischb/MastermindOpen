# Self-Improvement Loop

How mastermind notices Claude Code releases (and other watch-items) and surfaces them at session start.

## The pattern

```
Scheduled task                  Pending file              Startup hook
(daily / weekly)                (memory dir)              (session start)

check_updates.ps1   ────────►   pending_self_improvement.md ────────►  Active Resume
(7am every day)                  (auto-populated)                       hook #3 reads it

                                 ↑
                                 │ (cleared after
                                 │  user discusses)
                                 ↓

                                 (empty until next finding)
```

Four moving parts:

1. **The scheduled task** — daily or weekly OS-level Task Scheduler entry. Polls for new info.
2. **The pending file** — `<memory_dir>/pending_<topic>.md`. Auto-populated by the task.
3. **The startup hook** — Active Resume hook #3 reads any `pending_*.md` and surfaces non-empty content at session start.
4. **The discussion + clear** — user and mastermind discuss, take action if needed, clear the entry.

## Why this works

- **No background noise during sessions.** The polling happens out-of-process; mastermind only sees the result when you next open it.
- **Surfaced at the right moment.** "Picking up — also, Claude Code v2.1.110 dropped yesterday with these changes: ..."
- **Easy to ignore.** If you don't care about a finding, say "skip" and the entry clears.
- **Composable.** Add more pending files for other watch-items: NAS health, VPS uptime, TLS certs, package updates.

## Worked examples

### Example 1 — Claude Code release check (lives in this fork)

`startup-chain/check_updates.ps1` runs daily at 7am via Task Scheduler. It:
1. Fetches https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md.
2. Parses the latest version heading.
3. Compares to a small state file (`<state_file>` — tracks the last-seen version).
4. If new: appends the release section to `<memory_dir>/pending_self_improvement.md` with today's date.
5. Updates the state file.

Mastermind reads the file at session start. Non-empty → surfaces the highlight.

You discuss → entries clear.

### Example 2 — Weekly system health check (template lives in this fork)

`startup-chain/weekly_system_health.ps1.template` is a skeleton. Adapt per system (NAS, VPS, router, certs). Schedule it Monday 7am. It:
1. Runs system-specific checks (SSH into NAS, check disk %; curl VPS /health; etc.).
2. If any alert: appends to `<memory_dir>/pending_<system>_alerts.md`.
3. Optionally: pushes severe alerts straight to Telegram (so you don't have to wait for the next session start).

Mastermind reads each `pending_*.md` at session start. Surfaces non-empty content.

### Example 3 — TLS expiry check

Same pattern. One PS1 per system you care about. Each PS1 writes alerts to its own `pending_*.md`.

```powershell
# Pseudocode for the check
$cert = Get-RemoteCertExpiry "yourdomain.com" 443
$daysLeft = ($cert.NotAfter - (Get-Date)).Days
if ($daysLeft -lt 30) {
    Add-Content $PendingFile "TLS for yourdomain.com expires in $daysLeft days"
}
```

### Example 4 — Package update advisor

Daily check for `npm outdated`, `cargo outdated`, `pip list --outdated` across your active projects. Queue findings; mastermind decides whether they're worth surfacing at the next session.

## Designing your own watch-items

For each thing you want mastermind to passively monitor:

1. **What's the smallest "is something different?" check?** (Disk %, last commit timestamp, version string, expiry date.)
2. **What's the cadence?** Daily for fast-changing things, weekly for slow.
3. **What's the alert threshold?** Don't ping for noise.
4. **Where does the alert go?** Pending file for next session, push for time-sensitive.

Each watch-item is one PS1 + one Task Scheduler entry + one pending file. Repeat for each domain.

## Anti-pattern: mastermind polls in-session

Don't have mastermind poll an external service during a session. That blows token budget and forces mastermind to manage state. Use the scheduled task → pending file pattern instead — let the OS schedule the polling, let the pending file carry state across sessions.

## Read also

- `startup-chain/check_updates.ps1` — concrete daily example
- `startup-chain/weekly_system_health.ps1.template` — adaptable skeleton
- `memory/pending_alerts_template.md` — generic pending file pattern
- [automation-categories.md](automation-categories.md) — why scheduled tasks need per-job approval (Category 3)
