# Why Mastermind

The long-form pitch — what problem this solves and who it's for.

## The problem

Claude Code is excellent at the task in front of it. It's terrible at:

- **Remembering you across sessions.** Every session, you re-explain your preferences, your tech stack, why you made the architectural choice you made three weeks ago.
- **Switching between projects without losing context.** You're in Project A; you ask about Project B; Claude has no memory of Project B's conventions.
- **Doing anything when you're not at the keyboard.** Claude is a desktop tool. Your phone has no relationship with it.
- **Picking up where you left off.** When you sit down, Claude doesn't know what you were doing yesterday.
- **Improving itself.** Claude Code ships updates regularly; you'd never know unless you happened to check.

Each of these is a paper cut. They compound. After a month of paper cuts, "Claude Code as my collaborator" has cost you N hours of re-explanation, lost context, and missed updates.

## What mastermind does about it

### Persistent memory, not just context window

A tiered memory directory at `~/.claude/projects/<hash>/memory/` that mastermind reads at session start. Five tiers (working / short / medium / long / archive) with explicit demotion rules. The "Day 30 problem" — context pollution from never demoting stale memories — is engineered against, not hoped-against.

Result: Day 90 looks like Day 1, not Day 90.

### One Claude over many projects

A CLAUDE.md at the parent directory of your projects acts as a router. Each project has its own CLAUDE.md and per-project memory dir. When you name a project, mastermind reads its context on demand. Project A's deploy commands live in Project A's memory, not in the always-loaded surface.

Result: You can work on five projects in one session without Claude losing the thread.

### Inbound + outbound channels

Telegram in: DM the bot from your phone to ask questions, trigger shutdowns, get status. Telegram out: boot pings on PC power-on; push notifications when long-running tasks finish; substantive replies when you're AFK.

Home Assistant in: dashboard buttons fire mastermind scripts; voice Assist phrases trigger HA actions. Home Assistant out: TTS broadcasts to media players.

Result: mastermind reaches you wherever you are, you reach mastermind from anywhere.

### Boot and shutdown discipline

Every PC boot fires a Telegram ping confirming Claude is alive. Every PC shutdown goes through Claude — DM the trigger, Claude runs hygiene + snapshot + then issues the actual shutdown. No orphaned in-flight work. No stale dated items rotting in next-week's "Where we left off."

(When Claude is dead, the HA SSH fallback exists — see `shutdown-chain/README.md`.)

Result: every shutdown is a clean cut, every boot is a confirmed restart.

### Self-improvement

A daily scheduled task polls for new Claude Code releases. New releases get queued to a pending file. Mastermind surfaces non-empty pending content at session start. Same pattern for system health (NAS, VPS, router), cert expiry, package updates.

Result: you learn about Claude Code updates within a day of release, not months later. Your NAS surfaces problems before they cascade.

### Defensive snapshots

Hooks fire on PreCompact + SessionEnd + per-batch writes. Each snapshot is a plain-file copy of the memory dir + critical config files at a timestamped directory on a separate drive. Snapshots are never pruned.

Result: when you fat-finger a memory edit (or when Claude does), recovery is `cp` from a directory tree.

### Voice + behavior

The memory dir ships with ~7 "voice/behavior" rules learned the hard way from real failure modes — Claude's Opus 4.7 over-optimism, hallucination patterns on tool names, "diagnose before suggesting" discipline, "verify before asserting never worked" discipline. They shape mastermind's defaults; you edit them to taste.

Result: mastermind feels like it knows you after ~5-10 hours of work together, instead of having to retrain it every session.

### Child masterminds for big projects

For large projects that earn their own dedicated Claude (e.g. a multi-month rewrite), spawn a "child Claude" with its own identity and memory dir. The parent mastermind delegates project-specific work to it. The "Frostsmith pattern" — pun-name optional, structure required.

Result: a giant project gets its own Claude with its own voice and memory, without polluting the orchestrator.

### Project bootstrapping

`python init.py bootstrap` creates a new project: directory, CLAUDE.md from a per-type template, memory dir, Project Registry entry. Optionally spawns a child Claude. The "father function" — mastermind doesn't just remember projects, it creates them.

Result: starting a new project is a one-minute interactive prompt, not a half-hour of scaffolding decisions.

## Who this is for

- **Solo developers** who run multiple projects and lose context switching between them.
- **People who work AFK** and want their Claude reachable from a phone.
- **People who care about Claude Code as a long-term tool** rather than a session-by-session helper.
- **People with strong opinions** about how they want Claude to behave, who want those opinions encoded so they don't have to re-explain.

## Who this is NOT for

- **People who want a UI.** This is a memory directory + a CLAUDE.md + a few markdown files. Configuration is text editing.
- **People who want zero setup.** First-time onboarding is 5 minutes. Wiring all the integrations is another 30-60 minutes.
- **People with strict corporate policies on cloud integrations.** Most integrations call vendor APIs (Google, Telegram, Intuit, DocuSign). If your security posture forbids those, only the local-only pieces apply.

## The promise

Clone the repo. Run `python init.py`. Open Claude Code, say "Mastermind waking up for the first time." 5 minutes later, you have a Claude Code that remembers you.

By the end of week one, mastermind knows your projects, your preferences, your hardware, and at least one personal-life vignette in depth. It can shut down your PC when you say good night, fire up your PC from your phone, surface new Claude Code releases, and snapshot itself defensively.

By the end of month one, the live mastermind has accreted a few dozen feedback rules calibrated to you specifically, and feels like a teammate.

That's the promise.
