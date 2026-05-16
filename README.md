# Mastermind for Claude Code

**Clone, run `python init.py`, get a Claude Code that remembers you, sits above every project you work on, reaches you on your phone, and shuts your PC down for you when you say good night.**

> _by DrEvil_

A persistent AI partner for Claude Code that:

- **Remembers you** across sessions (tiered memory with explicit demotion rules — no "Day 30" context pollution).
- **Sits above all your projects** as a router, with each project's context loaded on demand.
- **Reaches you anywhere** via Telegram, push notifications, and Home Assistant.
- **Boots and shuts down your PC** through Claude (hygiene + snapshot first, then `shutdown /s /t 5`).
- **Self-improves** — a daily scheduled task surfaces new Claude Code releases for you to discuss.
- **Snapshots itself defensively** — PreCompact + SessionEnd hooks dump plain-file copies of the memory dir to a separate drive.
- **Has a voice** — ~7 voice/behavior rules calibrated from real failure modes (Opus over-optimism, hallucination on tool names, diagnose-before-suggesting discipline).
- **Bootstraps new projects** with one command — drafts CLAUDE.md from per-type templates, initializes per-project memory dirs, updates the Project Registry.

## Quick start

```bash
git clone https://github.com/{YOUR_HANDLE}/MastermindOpen.git
cd MastermindOpen
python init.py
```

Answer 4 questions (name, memory dir, snapshot target, integrations). Then open Claude Code in your project root and say:

> *"Mastermind waking up for the first time."*

5 minutes of conversational setup later, you have a Claude Code that knows who you are and what you're working on.

## Start a new project

After install, bootstrap projects via:

```bash
python init.py bootstrap
```

Walks you through naming, picking a template type (general / web-service / business / game / document-library), and (optionally) spawning a dedicated child Claude with its own identity.

## What's in the box

```
MastermindOpen/
├── init.py                    Cross-platform installer
├── CLAUDE.md                  Generic mastermind orchestrator scaffold
├── memory/                    ~30 template memory files (Tier 0 + 1 + 1b + 2)
│   ├── MEMORY.md              Index (always loaded, < 200 lines)
│   ├── session_log.md         Short-term memory shell
│   ├── todo.md                Persistent todo shell
│   ├── user_*.md              User profile templates
│   ├── personal_*.md          Hobby vignettes (golf, weightlifting, strategy_game, etc.)
│   ├── medical_*.md           Health metrics templates
│   ├── home_*.md              Home / hardware / network templates
│   ├── feedback_*.md          Voice + behavior rules (verbatim from upstream)
│   ├── pending_alerts_template.md
│   └── scripts/
│       ├── snapshot_memory.py
│       ├── scan_perms.ps1
│       └── render_dashboard.py.template
├── settings/                  Claude Code settings + statusline templates
├── integrations/              MCP setup guides (8 integrations)
├── plugins/                   Plugin docs (Telegram channel setup)
├── startup-chain/             Windows boot chain templates (.bat + .ahk + .ps1)
├── shutdown-chain/            HA SSH-fallback templates (yaml + ps1 + dashboard)
├── templates/                 Per-type CLAUDE.md templates for new projects
└── docs/                      Long-form architecture / pattern / FAQ docs
    └── projects/              Project-bootstrapping patterns
```

## Read order if you're new

1. [docs/why-mastermind.md](docs/why-mastermind.md) — the pitch in long form
2. [docs/architecture.md](docs/architecture.md) — how the pieces fit
3. [docs/onboarding-flow.md](docs/onboarding-flow.md) — what your first session feels like
4. [docs/memory-protocol.md](docs/memory-protocol.md) — the tiered memory model + demotion rules
5. [docs/orchestrator-pattern.md](docs/orchestrator-pattern.md) — multi-project routing
6. [integrations/README.md](integrations/README.md) — wire up the integrations you want

## Status

**v0.1 released — 2026-05-16.** Working but unpolished. The author runs a divergent live version daily — this fork is a snapshot in time, not a live mirror.

PRs welcome but feature PRs unlikely to land. The repo is a template, not a maintained framework. Take what you want, leave the rest.

## License

MIT — see `LICENSE`. Copyright DrEvil 2026.

## Contact

DrEvil is the mysterious creator of mastermind. Reach out via GitHub Issues — that's the only door.

## FAQ

See [docs/faq.md](docs/faq.md).
