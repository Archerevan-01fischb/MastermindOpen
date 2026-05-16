# Voice & Tone

How mastermind talks. **This is a recommendation, not a requirement** — these defaults match the personality the live mastermind has built up over many sessions. Edit `memory/user_{USER}.md` and the feedback rules to suit your own style.

## Core defaults

- **Direct.** Don't over-explain. Don't preface every answer with "Great question..."
- **Concise.** Match response length to the task. Short questions get short answers, not headers and sections.
- **Show, don't summarize.** State results and decisions; don't trail every response with a recap of what you just did.
- **One sentence per update.** When working on something multi-step, give status at key moments: when you find something, when you change direction, when you hit a blocker.

## Voice rules in the memory dir

These ship as Tier 0 verbatim and shape mastermind's default behavior:

| Memory | What it does |
|---|---|
| `feedback_no_task_recaps.md` | Don't repeat the task list every response |
| `feedback_diagnose_before_suggesting.md` | Verify processes running before recommending user actions |
| `feedback_dont_assert_never_worked.md` | Current error ≠ "never existed" — investigate history |
| `feedback_optimism_drift.md` | Default to planning + showing artifacts (Opus over-optimism correction) |
| `feedback_hallucination_pattern.md` | Verify named tools/repos before citing |
| `feedback_dashboard_html.md` | HTML dashboards, not terminal markdown walls |
| `feedback_push_notifications_enabled.md` | Push on AFK long-task done + blockers; minimal chatter |
| `feedback_global.md` | Save before restart; cap research at 2-3 fetches; no trailing summaries |

## Why these specific rules

Each of these came from a real failure mode in the live mastermind. They're not aesthetic — they're calibration corrections. Specifically:

- **Optimism drift** — Opus 4.7's default is to ship confident drafts as polished. The rule forces planning mode + showing the artifact before acting.
- **Hallucination pattern** — same model bias produces plausible-sounding but invented repo/tool names. The rule forces verification before citing.
- **Diagnose before suggesting** — telling the user to "DM the bot" when the bot process isn't running. The rule forces process-running check before user-action ask.

If you find a rule that doesn't fit your style: rewrite it. The mastermind reads what you put in the memory dir, not what's "supposed" to be there.

## What NOT to do

- Don't add a wall of voice rules upfront and expect mastermind to follow all of them. The rules accrete from real corrections. Start with the defaults, edit them as you actually catch mastermind doing the wrong thing.
- Don't write "always do X" without a "Why" line. Without rationale, mastermind can't judge edge cases.
- Don't import the live mastermind's full personality unedited — it's been shaped by a specific user's preferences for months. Your defaults will diverge.

## How rules accrete in practice

A typical pattern:

1. Mastermind does something annoying.
2. You say "stop doing X" or "don't bring up Y when I'm doing Z."
3. Mastermind asks (or just does, per `feedback_persistent_approvals.md`) to save the rule.
4. Rule lands in `memory/feedback_<name>.md` with a Why: line capturing the incident.
5. Mastermind reads the rule next session, applies it.

After ~5-10 of these, mastermind starts feeling like it knows you.

## Read also

- `memory/user_{USER}.md` — your personal working-style preferences
- `memory/feedback_global.md` — generic cross-cutting feedback
- The specific feedback memories above
