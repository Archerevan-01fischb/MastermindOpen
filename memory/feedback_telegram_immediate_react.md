---
name: Telegram immediate react
description: On every incoming Telegram message, react with an emoji immediately as the first action before any thinking/work.
type: feedback
---
On every incoming Telegram message, the FIRST tool call must be `mcp__plugin_telegram_telegram__react` with an acknowledgment emoji (👀 for normal, 🤔 for a question I'm about to research, 👍 for simple confirmations). Do this BEFORE any other tool call, BEFORE reading files, BEFORE thinking-heavy work.

**Why:** Long silent gaps on Telegram while I think/work leave the user with no signal their message landed. A react fires instantly and gives visible confirmation.

**How to apply:**
- Triggers on any message with `<channel source="telegram" ...>` tag
- React first, then proceed with the actual work
- For tasks expected to take more than a few seconds, also follow the react with a quick `reply` ("on it" / "checking now") so the user has a message to track — then edit that or send a final new reply when done (new replies push-notify, edits don't)
- Does NOT apply to non-Telegram sessions (regular CLI, web, etc.)

**Companion rule:** [[feedback_telegram_reply_channel_match]] — for substantive replies, match the channel to user presence (chat-UI if at desktop, Telegram if AFK).
