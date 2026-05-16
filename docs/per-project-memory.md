# Per-Project Memory

How orchestrator memory and per-project memory stay separate.

## The split

| Lives at | Used for | Loaded when |
|---|---|---|
| Mastermind memory dir (`~/.claude/projects/<hash-of-RustroverProjects>/memory/`) | User preferences, cross-cutting work, project registry, voice rules, snapshots | Every Claude Code session run from the parent dir |
| Per-project memory dirs (`~/.claude/projects/<hash-of-ProjectA>/memory/`) | Project-specific commands, credentials, dashboards, known issues, deploy steps | Only when Claude Code is run from inside ProjectA (or when mastermind explicitly reads it) |

The dirs are flat siblings of each other. Claude Code's hash function is deterministic: `<hash-of-X>` is just a fixed function of the absolute path `X`.

## Why split?

- **Always-loaded context stays small.** Mastermind doesn't carry WarNews's deploy commands or MW's debug guidelines on every session start. Those load on demand.
- **Concerns separate cleanly.** "Bruce prefers terse responses" belongs in mastermind. "WarNews VPS uptime command is `ssh root@... uptime`" belongs in WarNews's memory.
- **You can spawn child Claudes** with their own identity and memory dir (see [child-mastermind-pattern](projects/child-mastermind-pattern.md)) — that pattern only works if memory is per-project.

## What lives in mastermind memory

- `MEMORY.md` (index)
- `session_log.md`, `todo.md`
- `user_*.md`, `personal_*.md`, `medical_*.md`, `home_*.md`
- `feedback_*.md` (all the behavior rules)
- `pending_*.md` (auto-generated alerts)
- Reference files: credentials master list, toolchain inventory
- Vignettes (strategy game, aquaculture, woodworking, smart home)

## What lives in per-project memory

- `project_<name>.md` for the project itself (its own descriptor)
- Project-specific feedback (e.g. "for this project, always run X before Y")
- Project-specific credentials (if scoped to one project)
- Dashboard scripts for this project (kept in `scripts/` subdir + referenced from the memory file)

## The Project Registry table (mastermind side)

Mastermind's CLAUDE.md has a Project Registry table with one row per project:

```markdown
| Project | Path | Description | Has Dashboard |
|---------|------|-------------|---------------|
| ProjectA | `ProjectA/` | Web service that does X | Yes |
| ProjectB | `ProjectB/` | Game project | No |
```

When you say "let's look at ProjectA's deploy," mastermind reads:
1. The Project Registry row for ProjectA (to find the path).
2. `ProjectA/CLAUDE.md` (project-specific instructions).
3. `~/.claude/projects/<hash-of-ProjectA>/memory/project_a.md` (project memory).

Then acts in that lane.

## Adding a new project

`python init.py bootstrap` walks you through:
1. Project name + type
2. Where it lives
3. (Optional) spawn dedicated child Claude

The script:
1. Creates the project directory.
2. Drafts the project's `CLAUDE.md` from the per-type template.
3. Initializes `~/.claude/projects/<hash-of-new-project>/memory/MEMORY.md` and `project_<name>.md`.
4. Appends a row to mastermind's Project Registry.
5. If child Claude requested: sets up the child's identity (a name, isolated memory dir, etc.).

See [bootstrapping-a-new-project.md](projects/bootstrapping-a-new-project.md) for the walk-through.

## Manually adding a project (no script)

If you prefer to wire it by hand:

1. Create the project dir.
2. Write a project CLAUDE.md.
3. From inside the project dir, run `claude` once to make Claude Code create the per-project memory dir at `~/.claude/projects/<hash>/`.
4. In that memory dir, write `MEMORY.md` + `project_<name>.md`.
5. Edit mastermind's CLAUDE.md to add the project to the registry.

## Finding the hash for a path

Quickest way: open Claude Code in the project, run `claude debug paths` (subject to harness availability — verify with `/help`). Or: hash is reflected in the dir name under `~/.claude/projects/`, just look at what got created after step 3.

## Snapshot scope

`snapshot_memory.py` snapshots the **mastermind** memory dir, NOT per-project dirs. Per-project memory should be kept in its own git repo (or at minimum, snapshotted by your system-level backup). The plain-file snapshot pattern is intended for the always-loaded surface — not the on-demand-loaded per-project surface.

## Read also

- [orchestrator-pattern.md](orchestrator-pattern.md) — how routing works
- [projects/bootstrapping-a-new-project.md](projects/bootstrapping-a-new-project.md) — the walk-through
- [projects/child-mastermind-pattern.md](projects/child-mastermind-pattern.md) — Frostsmith model
