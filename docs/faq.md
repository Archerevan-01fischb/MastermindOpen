# FAQ

## Will my data leave my machine?

The memory directory is local. `snapshot_memory.py` writes to a local target you choose. Nothing in this repo's templates sends your data anywhere.

That said: the MCP integrations DO send data to external services:

- **Gmail / Calendar / Drive** integrations send queries to Google's APIs.
- **Telegram channel** sends DMs to Telegram's servers.
- **QuickBooks** sends queries to Intuit's APIs.
- **DocuSign** sends envelopes to DocuSign's servers.
- **Home Assistant** is local-only IF your HA install is local-only.

You choose which integrations to enable. Skip the ones whose vendors you don't want to share with.

Claude Code itself sends your messages to Anthropic's API. That's how it works. See Anthropic's privacy policy.

## Is this maintained?

This repo is **DrEvil's personal config released as a template, not a maintained framework.** Small fixes welcome. Feature PRs unlikely to land — the live mastermind diverges from the public fork by design.

If you want a more polished, supported equivalent, look at the various "AI coding assistant memory" projects that have shipped recently. This one is for people who want to take a working setup and adapt it.

## Why is it called "mastermind"?

Because it's the AI partner that sits above everything — like a chess mastermind playing several boards at once. The name is meant to suggest scope (multi-project orchestrator), not arrogance.

## Why publish anonymously as "DrEvil"?

Pen-name decision. The author wants the repo on its own merits without the real-name brand entanglement. Contact via GitHub Issues only.

## Does it work on macOS / Linux?

The MEMORY system + integrations layer + plugins work on any OS Claude Code supports. The **startup chain** is Windows-specific (bat / AHK / PC Matic workarounds). macOS LaunchAgent and Linux systemd equivalents aren't in v0.1 — they're a v0.2 candidate.

## Do I need all the integrations?

No. Mastermind works fine with zero integrations — just the memory + orchestrator. Add integrations as you find use cases.

## How big does the memory dir get?

Typical steady-state: 20-40 memory files, 5-15 MB total (most of which is the `session_archive/` subdir if you keep old logs). The always-loaded surface (`MEMORY.md` + `session_log.md` + `todo.md` + ⭐-flagged) stays under ~500 lines.

## What if I want to use multiple Claude Code instances at once?

You can — but only one mastermind. If you spawn child Claude instances for specific projects (see `docs/projects/child-mastermind-pattern.md`), each child runs in its own Claude Code window with its own memory dir. The parent mastermind is the orchestrator; children are project-scoped.

## Can I run this on a remote server?

Yes — install Claude Code on the server, set up the memory dir, point at it. Boot/shutdown chains don't apply to a server (they're for personal PCs). Snapshots work the same.

## How do I export my memory dir to share with a teammate?

Two options:

1. **Share specific files.** Pick the files that capture conventions you want to share. Drop them into a team-shared repo.
2. **Use mastermind's planning + sharing pattern.** Plan what to share in a planning-mode session, fork (like this repo did), sanitize, ship.

Don't share your whole memory dir unsanitized — it contains personal preferences and likely credentials.

## What if mastermind starts hallucinating?

See `memory/feedback_hallucination_pattern.md` — Claude Code (Opus 4.7) has a known confidence-hallucination pattern, especially for named external tools. Verify before citing. If mastermind cites a repo or package that doesn't exist, push back: "verify that repo exists before recommending it."

## How do I uninstall?

1. Remove the entries `init.py` added to `~/.claude/settings.json`.
2. Optionally: delete the memory dir (`<MEMORY_DIR>`). Snapshots will still exist on `SNAPSHOT_ROOT`.
3. Remove the startup-chain Scheduled Task + bat / AHK files.
4. Remove the shutdown-chain HA scripts + pubkey from your PC.

Each step is reversible — nothing here writes to the registry or modifies system state outside the locations the install told you about.

## Is this a Claude Code plugin?

No, it's a pattern + a memory template + some scripts. It uses Claude Code plugins (specifically the Telegram channel plugin) but isn't one itself.

## Why do you use Python for the snapshot but PowerShell for the perms scan?

Snapshots are cross-platform; PowerShell is Windows-specific. The perms scan was easier in PowerShell because it parses Claude Code's transcripts which are most accessible via PS on Windows. Both scripts are simple enough to translate to other languages if you prefer.

## Where do I report a bug?

GitHub Issues. The repo's Issues tab is the only contact channel.
