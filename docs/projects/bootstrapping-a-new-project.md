# Bootstrapping a New Project

End-to-end walk-through.

## The interactive flow

```bash
$ python init.py bootstrap

  What's the project name? [my-cool-thing]: weather-aggregator
  What type? [general / web-service / business / game / document-library]: web-service
  Brief description (1 sentence): RSS-style aggregator for severe-weather alerts in Colorado
  Where should the project live? [~/projects/weather-aggregator]:
  Spawn a dedicated child Claude? [y/N]: n

  > Creating ~/projects/weather-aggregator/...
  > Drafting ~/projects/weather-aggregator/CLAUDE.md from web-service template...
  > Initializing project memory dir at ~/.claude/projects/<hash>/memory/...
  > Writing project_weather_aggregator.md to project memory dir...
  > Adding "weather-aggregator" to mastermind's Project Registry in ~/.claude/CLAUDE.md...

  Done. Open Claude Code in ~/projects/weather-aggregator and say:
    "Project waking up for the first time."
```

## What happens under the hood

1. **Directory created** at the chosen path.
2. **CLAUDE.md drafted** from `templates/project-types/web-service/CLAUDE.md.template`. Placeholders left for you to fill (project name, tech stack details, deploy commands).
3. **Memory dir initialized** at `~/.claude/projects/<hash-of-new-dir>/memory/`.
4. **Project memory file** written: `~/.claude/projects/<hash>/memory/project_weather_aggregator.md` based on `templates/project-bootstrap-memory.md.template`.
5. **Project Registry row appended** to the mastermind's CLAUDE.md table:
   ```markdown
   | weather-aggregator | `~/projects/weather-aggregator/` | RSS-style aggregator for severe-weather alerts in Colorado | No |
   ```
6. (If child requested): the child's identity setup — see [child-mastermind-pattern.md](child-mastermind-pattern.md).

## First session in the new project

Open Claude Code from the project directory. Say:

> "Project waking up for the first time."

The project's CLAUDE.md is loaded, the project's memory dir is loaded. The project-Claude welcomes you and asks about the next concrete step — typically:

- What's the actual tech stack? (Bevy? Axum? Flask?)
- What's the first feature?
- Are there reference implementations to read?

From there you're doing project work.

## When does mastermind get involved vs the project-Claude?

- **Mastermind** = run Claude Code from the parent dir (e.g. `~/projects/`). Sees all projects, routes between them.
- **Project-Claude** = run Claude Code from a specific project dir. Sees only that project's context.

Both are the same Claude Code binary; the difference is which CLAUDE.md is loaded.

For cross-cutting work ("update all my projects' deploy scripts to use the new approach"), mastermind. For project-specific deep work, project-Claude.

## Tearing down a project

To remove a project from mastermind's scope:

1. Edit mastermind's CLAUDE.md, remove the row from the Project Registry.
2. Decide what to do with the project directory:
   - **Archive:** rename it out of the projects parent dir (e.g. `~/projects-archive/old-project/`).
   - **Delete:** `rm -rf` (the memory dir at `~/.claude/projects/<hash>/` stays — clean it up separately if you want).
3. (Optional) Archive the project's memory dir to your `session_archive` or just leave it — disk is cheap.

Don't manually delete `~/.claude/projects/<hash>/` for a project you might come back to. Claude Code will re-create it empty next time you `cd` into the dir.

## Adapting a template after bootstrap

The bootstrap drafts CLAUDE.md and the project memory file from templates with placeholders left in `{CURLY_BRACES}`. After bootstrap, your first task is filling those in. Mastermind can help — it knows what the placeholders represent because it just wrote them.

Suggested first conversation:

> "Read this project's CLAUDE.md and project memory. Then ask me one question at a time to fill the placeholders. Skip ones I don't have answers for yet."

A 5-10 minute pass and the templates are real.

## What if I want to skip the script?

You can wire a project by hand:

1. Create the project dir.
2. Copy `templates/project-types/<type>/CLAUDE.md.template` to `<project_dir>/CLAUDE.md`. Edit placeholders.
3. From inside the project dir, run `claude` once. Claude Code creates the memory dir at `~/.claude/projects/<hash>/`.
4. In that memory dir, write `MEMORY.md` (use the existing one as a model) and `project_<name>.md` (from `templates/project-bootstrap-memory.md.template`).
5. Edit mastermind's CLAUDE.md to add the project to the Project Registry table.

Same result, more manual.
