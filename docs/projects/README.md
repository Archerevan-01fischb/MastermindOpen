# Project Bootstrapping

Mastermind doesn't just remember projects — it bootstraps them. New projects start from a per-type template (`templates/project-types/<type>/CLAUDE.md.template`), get an initialized memory directory, and a row in mastermind's Project Registry.

For big projects, mastermind can spawn a dedicated **child Claude** with its own identity and isolated memory dir (the "Frostsmith pattern"). The parent mastermind orchestrates; the child does deep work in its own lane.

## Read in this order

1. [bootstrapping-a-new-project.md](bootstrapping-a-new-project.md) — end-to-end walk-through using `python init.py bootstrap`
2. [child-mastermind-pattern.md](child-mastermind-pattern.md) — when and how to spawn a child Claude
3. [spec-driven-pattern.md](spec-driven-pattern.md) — using GitHub Spec Kit (`.specify/`) for content / RE / rewrite projects
4. [web-service-pattern.md](web-service-pattern.md) — the canonical shape for aggregator-style web services
5. [business-pattern.md](business-pattern.md) — the canonical shape for a small business / LLC
6. [game-pattern.md](game-pattern.md) — the canonical shape for a multi-platform game

## The pitch

"Use mastermind to bootstrap new projects, not just remember existing ones."

A new project should feel like a one-minute interactive prompt, not a half-hour of scaffolding decisions. The templates plus the bootstrap script make that real.

## Per-type templates

`templates/project-types/<type>/CLAUDE.md.template` exists for:

- **general** — bare-bones, when nothing else fits.
- **web-service** — feed-ingest + processing + storage + web layer (aggregator pattern).
- **business** — LLC operational surfaces (website + email + accounting + e-sign + ads + analytics).
- **game** — engine + asset pipeline + multi-platform release pipeline.
- **document-library** — source-to-output content pipeline, often spec-driven.

Pick the closest. You'll customize the placeholders on first edit anyway.
