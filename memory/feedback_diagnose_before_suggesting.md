---
name: Diagnose before suggesting user actions
description: NEVER tell the user to "try X" (DM a bot, restart with a flag, etc.) without first verifying the underlying system is actually running. Check processes, check PATH, check logs BEFORE suggesting user-facing actions.
type: feedback
---

When something isn't working, verify the backend is alive before asking the user to do anything.

**Why:** A common failure mode: the user is told to "DM the bot" across many sessions, and every time the bot doesn't respond because the plugin process wasn't even running. Each session re-diagnoses from scratch instead of checking memory for prior findings.

**How to apply:**
1. Before telling the user to interact with any service, verify the process is running.
2. Check memory files for prior diagnosis of known issues — don't start from zero.
3. If a feature has never worked, the problem is infrastructure, not user action.
4. Session logs and todo items must describe the ROOT CAUSE, not just the next user step.
