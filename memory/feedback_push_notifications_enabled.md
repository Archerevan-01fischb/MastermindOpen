---
name: PushNotification tool — adopted
description: Use OS-level push notifications to the user's phone for long-running task completion and AFK blockers.
type: feedback
---
`PushNotification` tool is adopted. Use it to ping the user's phone directly — complements (does not replace) Telegram.

**Why:** Telegram is two-way chat; PushNotification is a one-way OS-native alert that hits the lock screen regardless of whether Telegram is open. Push is for minimal, high-signal alerts — not chatter.

**How to apply — DO send a push when:**
- A long-running task (>10 min) completes while the user is AFK: deploys, research reports, big digests, `/ultrareview` results.
- A scheduled job fails in a way the user needs to know about.
- I hit a hard blocker and the user previously said "I'm stepping away" / "mowing the lawn" / "going to bed."

**DO NOT send a push for:**
- Short tasks (<5 min) — they'll see them when back.
- Progress updates mid-task (no "still working" pings).
- Confirmation of things they just asked me to do (no "done!" ping when sitting at the keyboard).
- Informational pings that aren't time-sensitive.

**Interaction with Telegram:** Push is for alerting; Telegram is for conversation. If the user needs to reply, they'll come back to Claude Code or open Telegram. Don't ping both channels for the same event — pick one.

**Calibration:** If the user says "too many pings" or "that didn't need a push," dial back immediately.

**Enablement requirements (both must be on):**
1. Remote Control (if applicable in your Claude Code edition).
2. `/config` → "Push when Claude decides" (underlying key: `agentPushNotifEnabled`).

The feature flag `tengu_kairos_push_notifications` ships in Claude Code v2.1.110+. If a push fails with "mobile push is disabled in /config," this toggle is off — re-enable it.
