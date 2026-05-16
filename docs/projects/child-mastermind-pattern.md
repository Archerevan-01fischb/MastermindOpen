# Child Mastermind Pattern ("Frostsmith")

When and how to spawn a dedicated Claude for a project, with its own identity and isolated memory.

## The idea

For most projects, mastermind handles project-specific work directly. Mastermind reads the project's CLAUDE.md + memory dir, does the work, returns to the parent context.

For a small subset of projects — big ones, long-running ones, ones with deeply project-specific conventions and voice — it makes more sense to give the project its own Claude. The "child" has a name, knows it's a child, and behaves like its own seat. The parent mastermind orchestrates; the child does deep work.

The archetype is "Frostsmith" — a dedicated Claude for a multi-year game engine rewrite. The name signals identity (you're not just "Claude," you're Frostsmith working on this game). The isolated memory dir lets the child accumulate project-deep context without polluting the parent.

## When to spawn a child

✅ Yes:
- Multi-month or multi-year project at active development.
- Project has its own voice / writing style.
- Project has its own deep memory worth keeping separate (architectural decisions, asset conventions, debugging lore).
- You'd want to dedicate one terminal window to it exclusively.

❌ No:
- Short-lived project.
- Project that's just "let me write a script."
- Project you can complete in a session or two.
- You're already at terminal-window overload.

Roughly: if you would name a teammate to work on this full-time, the project earns a child.

## What "child" actually means

It's still one Claude Code binary. Two differences from the parent:

1. **Distinct CLAUDE.md identity:** the child's CLAUDE.md says e.g. "You are Frostsmith. You work exclusively on {the game project}. The parent mastermind tracks your progress at a high level, but you own the technical work."
2. **Distinct memory dir:** the child's memory dir lives at the project's hash path. None of the parent's user-preference / cross-cutting memory is loaded.

The child is "less generalist, more specialist." It loses the user-preference layer the parent has built up; that's the trade-off.

## How `init.py bootstrap` handles it

If you answer `y` to "Spawn a dedicated child Claude?":

1. Ask for the child's name (e.g. "Frostsmith").
2. Ask for the child's memory dir (defaults to the project's hash path; rarely overridden).
3. Write the child's CLAUDE.md with the name baked in.
4. Initialize the child's memory dir with a child-specific MEMORY.md.
5. Add the child to the parent's Project Registry with a "(child Claude: Frostsmith)" note.

## Parent ↔ child interaction

Parent mastermind's role:
- Knows the child exists. Knows their name.
- Tracks the project at a high level (status, deadlines, blockers).
- Routes user requests to the child when the work is project-specific.

Child's role:
- Owns project-specific technical work.
- Has its own session_log, todo, project memory.
- Can defer cross-cutting questions to the parent.

How the user interacts:
- Most sessions: open Claude Code in the project dir → child wakes up.
- Cross-cutting work: open Claude Code in the parent dir → parent mastermind wakes up, can read child's memory to summarize progress.

## Naming the child

Naming matters because the name appears in:
- The child's CLAUDE.md opening line ("You are Frostsmith...")
- The parent's registry table
- The child's session_log entries
- The child's Telegram boot pings (if wired)

Good names:
- Memorable, short, evocative.
- NOT "Claude" or generic LLM names.
- NOT collisions with real-people names you also work with.

Examples: "Frostsmith" (a game remaster), "Helios" (a solar tracker), "Cooper" (a logistics tool).

## When the child should defer to the parent

Children should explicitly say "this isn't my lane — ask the parent mastermind" when:

- The question is about user preferences they don't have memory of.
- The question is about another project.
- The question is about cross-cutting infrastructure (Telegram channel, shutdown chain, snapshot config).

A polite "ask the parent" is better than the child making up an answer.

## Child-specific feedback memories

Children accumulate their own feedback memories over time, scoped to that project. The "voice rules" the parent has can be inherited as starting defaults — copy the file from parent memory to child memory at bootstrap, then let them diverge.

The parent doesn't read the child's feedback memories (they live in a different dir). Each is its own seat.

## Removing a child

If the project ends or you decide the child wasn't worth the overhead:

1. Archive the child's memory dir (rename it under a `_archived/` subdir, don't delete).
2. Either: convert the project back to direct-mastermind mode (the parent reads project memory directly), or fully delete the project per [bootstrapping-a-new-project.md](bootstrapping-a-new-project.md)'s teardown section.

## Read also

- `templates/project-types/game/CLAUDE.md.template` — typical content for a project that warrants a child.
- [orchestrator-pattern.md](../orchestrator-pattern.md) — how parent ↔ child routing fits in.
- [per-project-memory.md](../per-project-memory.md) — the memory split.
