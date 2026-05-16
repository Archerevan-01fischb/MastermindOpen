---
name: telegram-reply-channel-match
description: For substantive replies to Telegram messages, match the reply channel to the user's current presence — Telegram if AFK, chat UI if at desktop. Immediate-react emoji still fires regardless.
metadata:
  type: feedback
---

# Match the reply channel to user presence

Rule: When responding to a Telegram message, check whether the user is currently at the desktop before defaulting to a Telegram reply. If they've been actively clicking prompts or typing in the Claude Code UI within the last few seconds, reply in the chat UI, not on Telegram.

**Why:** The immediate-react rule ([[feedback_telegram_immediate_react]]) covers the "got it" signal. But mechanically defaulting substantive replies to Telegram when the user is sitting at the keyboard produces unwanted phone notifications. The fix is presence-aware reply routing.

**How to apply:**
- The immediate-react rule (👀 / 👍 emoji on inbound Telegram) **stays in force regardless of presence** — that's just a "got it" signal and costs nothing.
- For substantive replies, match the reply channel to current presence:
  - At the desktop (recently dismissed a UI prompt, recently typed in chat, conversation is in active back-and-forth) → reply in the chat UI.
  - AFK (no recent UI activity, last signal was "going out", Telegram is the only active surface) → reply on Telegram.
  - Ambiguous → ask once: "reply here or on Telegram?"
- Do **not** double-reply on BOTH channels — that's noise.
- A Telegram message arriving doesn't automatically mean the user is AFK. They may be at their desk and just using Telegram for a one-off ping.

**Related:** [[feedback_telegram_immediate_react]] (the react-emoji rule that this layers on top of), [[feedback_no_blocking_prompts_when_afk]] (sibling AFK-handling rule).
