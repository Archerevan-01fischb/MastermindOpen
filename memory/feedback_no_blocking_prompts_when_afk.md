---
name: no-blocking-prompts-when-afk
description: Never call ExitPlanMode, AskUserQuestion, or any UI-approval tool while the user is AFK — these suspend the turn and block inbound Telegram messages until they return.
metadata:
  type: feedback
---

# Don't use blocking UI-approval tools while the user is AFK

Rule: Do NOT call `ExitPlanMode`, `AskUserQuestion`, or any other tool that requires UI approval when the user has signaled they are AFK or running errands. Such tools suspend my conversation turn, which blocks inbound Telegram messages from being delivered until the user returns to the desktop and resolves the prompt.

**Why:** Failure mode: user goes on errands; I call `ExitPlanMode` to present a finished plan; my turn is suspended waiting on their desktop approval. Telegram messages they send queue behind the prompt and don't reach me until they return and dismiss it. Effective Telegram-channel silence during the entire AFK window — exactly the opposite of what the Telegram bridge is for.

**How to apply:**
- When the user signals they're leaving ("running errands", "AFK", "going for X", "back later", "heading out"), set a mental flag that approval-pending tools are forbidden until they confirm they're back at the desktop.
- If a plan is finished while they're away: write the plan file (or save the content to memory / a draft file so it survives a crash) and Telegram-ping with "plan ready, review when back" — DO NOT call `ExitPlanMode`.
- If a clarifying question genuinely needs their input while AFK: send it via Telegram. Don't use `AskUserQuestion`.
- Resume the approval flow only after they confirm presence at the desktop (recent UI activity or explicit "I'm back").
- The same logic applies to any other tool that suspends the turn pending UI interaction.

**Related:** [[feedback_telegram_reply_channel_match]] — companion rule on which channel to reply on once they're back.
