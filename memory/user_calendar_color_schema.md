---
name: user-calendar-color-schema
description: Calendar color-coding rules. Mastermind applies these automatically when creating events.
metadata:
  type: user
---

# Calendar Color Schema

## The principle

Recurring event types should always use the SAME Google Calendar color (`colorId` in the API). At a glance, the calendar should communicate domain — work / health / family / hobby — without reading the title.

## Google Calendar colorId values

(The Google Calendar API uses numeric colorIds, not names. Reference:)

| colorId | Color name | Hex |
|---------|------------|-----|
| 1 | Lavender | #7986CB |
| 2 | Sage | #33B679 |
| 3 | Grape | #8E24AA |
| 4 | Flamingo | #E67C73 |
| 5 | Banana | #F6BF26 |
| 6 | Tangerine | #F4511E |
| 7 | Peacock | #039BE5 |
| 8 | Graphite | #616161 |
| 9 | Blueberry | #3F51B5 |
| 10 | Basil | #0B8043 |
| 11 | Tomato | #D50000 |

## My event-type → color mapping

| Event type | colorId | Rationale |
|---|---|---|
| {EVENT_TYPE_1} | {COLOR_1} | {RATIONALE_1} (e.g. "Avs games → Blueberry (9) — team color match") |
| {EVENT_TYPE_2} | {COLOR_2} | {RATIONALE_2} (e.g. "Lifting sessions → Sage (2) — green for growth") |
| {EVENT_TYPE_3} | {COLOR_3} | {RATIONALE_3} (e.g. "Doctor/medical → Tomato (11) — high attention") |
| {EVENT_TYPE_4} | {COLOR_4} | {RATIONALE_4} (e.g. "Travel → Tangerine (6)") |
| {EVENT_TYPE_5} | {COLOR_5} | |
| {EVENT_TYPE_6} | {COLOR_6} | |

## Default

If an event doesn't match any rule above: use {DEFAULT_COLOR_ID} ({DEFAULT_COLOR_NAME}).

## How mastermind applies this

When creating an event via `mcp__claude_ai_Google_Calendar__create_event`:
1. Match the event title/keyword against the rules above.
2. Set `colorId` accordingly.
3. If ambiguous, use default.
4. Never use a colorId NOT listed above — keeps the schema consistent.

## Which calendar to use

(Separate from color — which calendar account / sub-calendar.)

- **Personal:** {PERSONAL_CAL_EMAIL_OR_NAME}
- **Work / business:** {WORK_CAL_EMAIL_OR_NAME}
- **Family / shared:** {SHARED_CAL_EMAIL_OR_NAME}

Default rule: most personal events on {DEFAULT_CAL}; only put events on {WORK_CAL} if they're related to {WORK_DOMAIN}.
