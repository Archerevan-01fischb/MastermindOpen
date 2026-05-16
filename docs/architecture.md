# Mastermind Architecture

A bird's-eye view of how the pieces fit. Each piece has its own doc — links below.

## The picture

```
                         ┌─────────────────────────────────┐
                         │   You + your phone + your PC    │
                         └──────────────┬──────────────────┘
                                        │
   inbound: DMs, voice, terminal        │     outbound: pings, dashboards
                                        ▼
                  ┌─────────────────────────────────────────┐
                  │            MASTERMIND (this)            │
                  │   one Claude Code instance, all your    │
                  │   projects, persistent memory           │
                  └─┬─────────┬──────────┬────────┬────────┘
                    │         │          │        │
            ┌───────┘         │          │        └─────────┐
            ▼                 ▼          ▼                  ▼
       ┌─────────┐    ┌──────────────┐  ┌─────────────┐   ┌──────────────┐
       │ Memory  │    │ Integrations │  │ Boot/Shutdown│   │  Projects     │
       │ (tiered)│    │  (MCP servers)│  │  chain       │   │  (each its    │
       │         │    │              │  │              │   │   own dir +    │
       │  ⭐ index│    │  Telegram    │  │  WOL boot   │   │   memory)     │
       │  session│    │  Gmail       │  │  DM shutdown│   │              │
       │  todo   │    │  Calendar    │  │  HA fallback│   │  Project A    │
       │  rules  │    │  Drive       │  │              │   │  Project B    │
       │  vignett│    │  HA          │  │              │   │  ...          │
       │  scripts│    │  QB / DocuSign│ │              │   │              │
       └─────────┘    └──────────────┘  └─────────────┘   └──────────────┘
```

## The four big ideas

### 1. Persistent, tiered memory

Five tiers from "working" (this conversation) to "archive" (raw old logs). Demotion rules run on triggers — pre-shutdown, end-of-session, on contradiction. The active context stays small (MEMORY.md < 200 lines, session_log.md < 120 lines, todo.md the master list).

See: [memory-protocol.md](memory-protocol.md), [snapshot-pattern.md](snapshot-pattern.md).

### 2. Orchestrator over many projects

CLAUDE.md is a router. The mastermind sits above projects and routes requests to the right context. Each project has its own CLAUDE.md and memory dir at `~/.claude/projects/<hash>/memory/`. The mastermind reads them on demand.

See: [orchestrator-pattern.md](orchestrator-pattern.md), [per-project-memory.md](per-project-memory.md).

### 3. Inbound + outbound channels for reach

Telegram in (DMs from your phone control the mastermind), Telegram out (boot pings, push notifications when long tasks finish), Home Assistant in (dashboard buttons fire scripts), Home Assistant out (TTS broadcasts).

See: `../integrations/telegram.md`, `../integrations/home-assistant.md`, [shutdown-pattern.md](shutdown-pattern.md).

### 4. Self-improvement loop

A daily scheduled task polls for new Claude Code releases, queues findings to `pending_self_improvement.md`. Mastermind reads the file at session start and surfaces non-empty content. You discuss with mastermind; entries clear after action.

Same pattern works for system health (NAS, VPS, router) — one PS1 + one pending file + the startup-hook surface.

See: [self-improvement-loop.md](self-improvement-loop.md), [automation-categories.md](automation-categories.md).

## The runtime — what happens when you sit down

```
  You launch Claude Code (via auto-boot chain or manually)
    │
    ▼
  Mastermind wakes up
    │
    ├── reads MEMORY.md (always loaded, < 200 lines)
    ├── reads session_log.md (most recent active work)
    ├── reads todo.md (active items)
    ├── reads any pending_*.md (auto-generated alerts)
    ├── identifies the most-recent active project
    ├── reads that project's memory file
    ├── verifies in-flight state (pings the service, checks the file)
    │
    ▼
  Opens with substantive resume:
   "Picking up — X. Status: Y. Next step: Z."

  (You drive from there.)
```

If it's your first time after `python init.py`, you get the **Onboarding Wake** instead — see [onboarding-flow.md](onboarding-flow.md).

## What this is NOT

- **Not a multi-agent orchestrator.** One Claude. Multiple projects, but one Claude instance at a time.
- **Not a daemon.** Mastermind only runs while Claude Code is running. It doesn't poll, doesn't have a background process. The scheduled tasks (`check_updates.ps1`, weekly health) are OS-level Task Scheduler entries, not Claude.
- **Not magic.** It's a CLAUDE.md + a memory dir + ~30 markdown files + a few small Python/PS1 scripts. The orchestration value is in the patterns, not the code.

## Read order if you're new

1. [why-mastermind.md](why-mastermind.md) — the pitch in long form
2. [orchestrator-pattern.md](orchestrator-pattern.md) — how the routing works
3. [memory-protocol.md](memory-protocol.md) — the tiered memory model
4. [onboarding-flow.md](onboarding-flow.md) — what your first session feels like
5. ... then specific tiers as you wire each integration
