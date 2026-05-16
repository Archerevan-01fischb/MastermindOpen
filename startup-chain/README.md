# Startup Chain (Windows)

Auto-launch your mastermind on login. Sends a Telegram boot ping when the PC powers on, then another after Claude Code is verified running.

## What this gives you

After installation, every PC boot:

1. **t=0:** Windows logs you in → `StartMastermind.bat` runs.
2. **t=30s:** Boot ping #1 fires to Telegram: `[boot] PC powered on at HH:MM`.
3. **t=30s:** RustRover (or your chosen IDE) launches with your project.
4. **t=30s+:** `ClaudeCodeLauncher` Scheduled Task fires → runs the AHK launcher.
5. **AHK launcher** waits for the IDE window, opens its terminal, types `claude --channels plugin:telegram@claude-plugins-official` + Enter.
6. **After Claude verifies running:** Boot ping #2: `[boot] Claude up and listening`.
7. **If Claude verification fails:** Boot ping warns: `[boot] WARNING: claude.exe NOT detected after launch. Use HA SSH shutdown if needed.`

Combined effect: 2 minutes after pressing the power button (or sending a WOL packet from your phone), your mastermind is alive and pinging you on Telegram. From AFK, you know it's up before you sit down.

## Prerequisites

- Windows 10/11.
- AutoHotkey v2 installed.
- Your IDE of choice (the template uses RustRover; adapt for VS Code, PyCharm, IntelliJ, plain `wt.exe`).
- Telegram integration set up (see `../integrations/telegram.md`) — boot pings need the bot token + chat_id.
- PC Matic users: read the gotcha section below.

## Install

1. Copy `StartMastermind.bat.template` to `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\StartMastermind.bat`, edit placeholders.
2. Copy `start_mastermind_in_ide.ahk.template` to a stable location (e.g. `<project_root>/start_mastermind_in_ide.ahk`), edit placeholders.
3. Run `register_mastermind_task.ps1` (elevated) to register the Scheduled Task that fires the AHK launcher.
4. Test by **logging out and back in** (cheaper than a full reboot, exercises the same chain).
5. Verify both boot pings arrive in Telegram. If only the first arrives, your AHK chain failed — check the log file at `<project_root>/claude_startup.log`.

## PC Matic / antivirus gotcha (important)

If you're on PC Matic Super Shield, the original "bat → start → powershell -File" chain gets AMSI-killed silently. The signed-binary AHK approach in the templates is what gets around this.

**Why** (the actual analysis):
- PC Matic detects `start /min "" powershell.exe -File <script>` as a process-spawn pattern matching keylogger / RAT signatures.
- AutoHotkey v2 is a signed binary — its keyboard/window calls run through a different code path that PC Matic doesn't block.

**If you're not on PC Matic,** the simpler PowerShell approach works fine (template not included; ask Claude to draft one if needed).

## Per-script docs

- **`StartMastermind.bat.template`** — the entry point. Runs at login. Logs to `<project_root>/claude_startup.log`. Sends boot ping #1. Launches IDE. Triggers the Scheduled Task.
- **`start_mastermind_in_ide.ahk.template`** — the IDE driver. Waits for the IDE window, opens its terminal, types the Claude launch command. Verifies claude.exe is running, sends boot ping #2.
- **`register_mastermind_task.ps1`** — idempotent script that registers the `ClaudeCodeLauncher` Scheduled Task. Run once per machine (re-run is safe).
- **`check_updates.ps1`** — separate daily-7am Task Scheduler entry. Polls for new Claude Code releases, queues findings to `<memory_dir>/pending_self_improvement.md`. Mastermind surfaces them at next session start. See `../docs/self-improvement-loop.md` for the full pattern.
- **`weekly_system_health.ps1.template`** — weekly Monday-7am Task Scheduler entry (template). Adapt per server (NAS, VPS, router) — queues alerts to a `pending_*.md` for surfacing.

## Logs

`<project_root>/claude_startup.log` collects every step's timestamp. If anything in the chain breaks, this is where to look.

## Uninstalling

1. Delete the .bat from the Startup folder.
2. `schtasks /delete /tn ClaudeCodeLauncher /f`.
3. Delete the AHK file.

That's it. Nothing else is persistent.

## On macOS / Linux

This chain is Windows-specific. The same conceptual setup on other OSes:

- **macOS:** LaunchAgent plist (`~/Library/LaunchAgents/`), AppleScript to open Terminal + type the command.
- **Linux:** systemd user unit, plus a tmux/screen wrapper that runs `claude` inside a persistent session.

Both are doable; templates for them aren't in v0.1.
