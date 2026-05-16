# Onboarding Flow

What your first session with mastermind feels like.

## After `python init.py`

The init script has just:
1. Asked you 4 questions (name, memory dir, snapshot target, integrations).
2. Copied templates to the memory dir.
3. Personalized MEMORY.md with your name and renamed `user_{USER}.md` to `user_<your-name>.md`.
4. Created empty `session_log.md` and `todo.md`.
5. Installed `snapshot_memory.py` with your paths filled in.
6. Merged settings into `~/.claude/settings.json` (preserving existing).
7. Written `<memory_dir>/.onboarding_pending` with a JSON blob of selected integrations.

Then printed:

```
Setup complete.

Next steps:
  1. Open Claude Code in your project root.
  2. Say (exactly): "Mastermind waking up for the first time."
  3. Claude will detect the onboarding flag and walk you through
     populating your templates (~5 minutes of natural conversation).

If you skip step 2, mastermind will still notice you're new and offer
to onboard automatically — but the magic phrase is the proper invocation.
```

## When you open Claude Code

Mastermind's wake protocol checks (in this order):

1. **Does `<memory_dir>/.onboarding_pending` exist?** — YES → Onboarding Wake.
2. Does any required template have unfilled `{PLACEHOLDER}` tokens? (fallback check — covers users who deleted the flag but didn't actually finish) — YES → Onboarding Wake.
3. Does `wake_log.md` exist? — NO → First Wake (post-onboarding diagnostics).
4. Else → Active Resume.

So on first open: Onboarding Wake.

## The Onboarding Wake conversation

Mastermind opens with:

> "I see this is your first time with mastermind. Let me help you set up — this takes about 5 minutes."

Then conversationally walks through:

### Required (gates onboarding completion)

1. **User profile.** Mastermind asks about you — name, role, preferences, working style. Fills in `user_<name>.md`.
2. **MEMORY.md header personalization.** Just your name in the heading.

### Optional (mastermind offers, you can skip any)

3. **Personal-life vignettes you care about.** "Want to set up a financial profile now, or skip and come back later?" / "Golf, weightlifting, or something else first?" Whatever you say yes to gets filled in conversationally.
4. **Integration setup for the integrations you enabled in `init.py`.** If you said yes to Telegram, mastermind walks you through bot creation. If you said yes to Gmail, the OAuth flow. Etc.

You can say "skip the rest" at any time to fast-track the end.

## When Onboarding Wake ends

Mastermind:
1. Deletes `<memory_dir>/.onboarding_pending`.
2. Runs `snapshot_memory.py "post-onboarding"`.
3. Appends a `session_log.md` entry: "Onboarding complete. User: X. Integrations: Y. Templates filled: Z. Next session Active-Resume."
4. Tells you:

> "You're set up. From here on, just talk to me normally — I'll remember everything between sessions. Try saying 'good night' when you're done to see the shutdown protocol in action."

## What happens next session

Active Resume. Mastermind reads `session_log.md`, sees the "Onboarding complete" entry, and opens with:

> "Picking up — yesterday we finished onboarding. Status: clean slate. Next step: whatever you'd like to start. Ready when you are."

From there on out, every session begins with Active Resume — pick up the most-recent work, ping the relevant system, open with a substantive resume.

## What if you skip "Mastermind waking up for the first time"?

Mastermind still detects you're new because of the flag file. It opens with:

> "Before we dive into that, I notice your mastermind isn't fully set up yet — quick 5-min walkthrough?"

You can say yes (onboarding starts) or no ("skip — I'll fill it in later" — mastermind respects that, doesn't pester).

## What if you manually delete `.onboarding_pending` without filling templates?

Mastermind's secondary check (regex scan for unfilled `{PLACEHOLDERS}` in required templates) catches this and still offers onboarding. You can't skip onboarding by deleting the flag — the templates have to be filled.

## Read also

- `init.py` — the installer that drops the flag
- [memory-protocol.md](memory-protocol.md) — tier system after onboarding
- [orchestrator-pattern.md](orchestrator-pattern.md) — adding your first real project after onboarding
