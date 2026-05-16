# Google Calendar Integration

Create / update / find / list events on one or more Google calendars. The cleanest path is the Anthropic-managed Cloud connector (`mcp__claude_ai_Google_Calendar__*`); a community gcal MCP also works.

## What this enables

- Create events with proper `colorId` per your color schema (see [[user_calendar_color_schema]])
- Update / move / delete events
- Find free time across calendars
- Respond to invites (accept / decline / tentative)
- Look up "what's on my calendar today / this week / next month"

## Setup (Cloud connector path — easiest)

1. In Claude Code or Claude Desktop, open Settings → Connectors.
2. Find Google Calendar, click Connect.
3. Browser opens to Google's consent screen.
4. Approve.

That's the entire flow. Tools become available at `mcp__claude_ai_Google_Calendar__*`.

## Setup (community gcal MCP path)

For if you want to self-host or use a community fork:

1. Create OAuth credentials in Google Cloud (same procedure as Gmail — see `gmail.md`).
2. Enable the **Calendar API**.
3. Install the community gcal MCP server (search GitHub for the canonical repo).
4. Register: `claude mcp add -s user gcal <launch-cmd>`.
5. First-run OAuth.

## Tools to know

The Anthropic-managed connector exposes (subject to change — verify with `ToolSearch`):

- `create_event` / `gcal_create_event`
- `update_event` / `gcal_update_event`
- `delete_event` / `gcal_delete_event`
- `list_events` / `gcal_list_events`
- `get_event` / `gcal_get_event`
- `list_calendars` / `gcal_list_calendars`
- `respond_to_event` / `gcal_respond_to_event`
- `suggest_time` / `gcal_find_meeting_times`
- `find_my_free_time` (your own free/busy)

## Calendar selection convention

You probably have multiple calendars (personal Gmail, work Google Workspace, shared family). Tell mastermind which calendar each event type belongs on in `user_calendar_color_schema.md`. Default rule: put events on the user's primary calendar; only use other calendars for events scoped to that calendar's domain.

## Allowlist

To skip per-call approval prompts for routine calendar operations, allowlist the calendar tools in `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__claude_ai_Google_Calendar__*"
    ]
  }
}
```

Adjust the wildcard if you only want some methods auto-approved.

## Common gotchas

- **Time zones:** every event has an implicit time zone. Always pass `timeZone` explicitly when creating events; rely on the calendar's default at your peril.
- **All-day events:** these use `date` (not `dateTime`) in the API. Recurring all-day events are a special case.
- **Recurrence rules (RRULE):** standard iCal RRULE format. Test with simple cases first.
- **Color ID is numeric**, not a name. `9` is Blueberry, not `"blueberry"`. See `user_calendar_color_schema.md`.

## Smoke test

```
Ask Claude Code: "What's on my calendar today?"
Expected: list of today's events, one per line, with times.
```
