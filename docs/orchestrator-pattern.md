# Orchestrator Pattern

How mastermind routes between many projects without losing context.

## The model

```
RustroverProjects/        ← your projects parent dir
├── CLAUDE.md             ← MASTERMIND (this is the orchestrator)
├── ProjectA/
│   ├── CLAUDE.md         ← project-specific instructions
│   └── ...
├── ProjectB/
│   ├── CLAUDE.md
│   └── ...
└── ProjectC/
    ├── CLAUDE.md
    └── ...

~/.claude/projects/
├── <hash-of-RustroverProjects>/memory/  ← MASTERMIND's memory
│   ├── MEMORY.md
│   ├── session_log.md
│   └── ...
├── <hash-of-ProjectA>/memory/           ← ProjectA's memory
├── <hash-of-ProjectB>/memory/
└── <hash-of-ProjectC>/memory/
```

The parent CLAUDE.md is the mastermind. It contains a **Project Registry** table listing the projects and a one-line description of each. When you mention Project A by name (or work in that dir), mastermind reads Project A's CLAUDE.md and memory files to load full context.

## Why this works

- **Mastermind's memory is small.** It tracks user preferences, cross-cutting work, and high-level project state. It doesn't carry per-project technical details — those live in the project's own memory.
- **Project memory is rich.** Per-project: deploy commands, credentials, dashboard scripts, known issues. Loaded only when the project is in scope.
- **One Claude, many lanes.** When you say "let's look at Project A's deploy," mastermind reads Project A's context on demand and acts in that lane. The next message can be a Project B question and mastermind switches.

## The Project Registry table

In mastermind's `CLAUDE.md`, maintain a one-row-per-project table:

```markdown
| Project | Path | Description | Has Dashboard |
|---------|------|-------------|---------------|
| ProjectA | `ProjectA/` | Service that does X | Yes — see project_a.md |
| ProjectB | `ProjectB/` | Game project | No |
```

Update this when projects are added/removed. `python init.py bootstrap` adds rows automatically when creating new projects (see [per-project-memory.md](per-project-memory.md)).

## Hash-path resolution

Claude Code computes a `<hash-of-path>` for each project — that's the directory name under `~/.claude/projects/`. The hash function is deterministic per absolute path. If you `cd` into different projects, Claude Code reads different memory dirs automatically.

Mastermind's CLAUDE.md describes how to derive the per-project memory dir path so you can read it explicitly (instead of relying on Claude Code's auto-load).

## Child mastermind (the "Frostsmith" pattern)

For large projects (e.g. a game project that gets its own multi-month rewrite), spawn a **dedicated child Claude** with its own identity and memory dir. The child knows it's a child — has a name, behaves like its own seat, doesn't try to be the mastermind. The parent mastermind delegates project-specific work to it.

See [child-mastermind-pattern.md](projects/child-mastermind-pattern.md) — but TL;DR:
- Child gets its own memory dir.
- Child's CLAUDE.md gives it a name (e.g. "Frostsmith") and identifies it as a child.
- Mastermind's Project Registry entry references the child.

When you're in the child's project dir, the child Claude wakes up. When you're at the parent, mastermind wakes up. Same Claude Code binary, different identity per project.

## Bootstrapping new projects

Run `python init.py bootstrap` and answer 4 questions:
- Project name?
- Type? (general / web-service / business / game / document-library)
- Path?
- Spawn dedicated child Claude? (y/N)

The script:
1. Creates the project directory.
2. Drafts the project's CLAUDE.md from a per-type template.
3. Initializes the project's memory dir.
4. Adds a row to the Project Registry in mastermind's CLAUDE.md.
5. If you opted for a child: sets up the child's identity + isolated memory dir.

See [bootstrapping-a-new-project.md](projects/bootstrapping-a-new-project.md) for the full walk-through.

## Read also

- [per-project-memory.md](per-project-memory.md) — split between orchestrator and project memory
- [projects/README.md](projects/README.md) — full project-bootstrapping playbook
- [projects/child-mastermind-pattern.md](projects/child-mastermind-pattern.md)
