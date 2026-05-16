# Mastermind — Memory Index for {USER}

## How Memory Works (READ THIS FIRST)

Three tiers — check all three every session start:

1. **Short-term → [session_log.md](session_log.md)** — Last session: what happened, decisions, where we left off. Read FIRST. Update through session. Archive old logs to `session_archive/`.
2. **Intermediate → [todo.md](todo.md)** — Master todo list. Survives shutdowns. Check every session.
3. **Long-term** — Everything below. Stable reference.

Archive: `session_archive/` (old logs) + bottom of this file (superseded memories).

---

## Session State (check first)
- [session_log.md](session_log.md) — Current/last session: what happened, decisions, open threads
- [todo.md](todo.md) — Persistent master todo list across all projects
- [pending_alerts_template.md](pending_alerts_template.md) — Pattern for queued auto-generated alerts (rename per source: e.g. `pending_self_improvement.md`)

## User Profile
- [user_{USER}.md](user_{USER}.md) — Role, preferences, working style (applies to all projects)
- [user_author_persona.md](user_author_persona.md) — If publishing OSS or content under a pen-name, register it here once
- [user_travel_profile.md](user_travel_profile.md) — Travel preferences (cabin class, hotel loyalty, etc.)
- [user_calendar_color_schema.md](user_calendar_color_schema.md) — How to color-code recurring event types in your calendar
- [user_dietary_restrictions.md](user_dietary_restrictions.md) — Diet rules / no-eat list / preferences
- [user_dental_protocol.md](user_dental_protocol.md) — Example health-routine template

## Medical (templates — fill or delete)
- [medical_chronic_condition_template.md](medical_chronic_condition_template.md) — Generic chronic condition tracking template
- [medical_a1c.md](medical_a1c.md) — Common metric tracking template
- [medical_blood_pressure.md](medical_blood_pressure.md) — Common metric tracking template
- [medical_night_guard.md](medical_night_guard.md) — Health-appliance template (TMJ guard etc.)

## Personal — example vignettes
- [personal_golf.md](personal_golf.md) — Hobby tracker exemplar
- [personal_weightlifting.md](personal_weightlifting.md) — Fitness program template
- [personal_financial_profile.md](personal_financial_profile.md) — Retirement / financial planning template
- [personal_investing.md](personal_investing.md) — Investment management template
- [personal_strategy_game.md](personal_strategy_game.md) — Strategy game companion vignette (Civ-style, sim racing, etc.)
- [personal_aquaculture.md](personal_aquaculture.md) — Small-tank / pond management vignette
- [personal_woodworking_project.md](personal_woodworking_project.md) — Furniture reverse-engineering / build vignette
- [personal_smart_home.md](personal_smart_home.md) — Smart home ecosystem inventory vignette

## Home (physical)
- [home_humidity_policy.md](home_humidity_policy.md) — HVAC management template
- [home_av_inventory.md](home_av_inventory.md) — A/V system documentation template
- [home_network.md](home_network.md) — Home network topology template
- [home_pc_hardware.md](home_pc_hardware.md) — System specs template
- [home_smart_shades.md](home_smart_shades.md) — Smart home integration template

## Behavior Rules — Working Style (verbatim from upstream)
- [feedback_memory_hygiene.md](feedback_memory_hygiene.md) — ⭐ Tiered memory; demotion rules; the "Day 30 problem"
- [feedback_automation_categories.md](feedback_automation_categories.md) — ⭐ Startup=YES (active resume), event-driven=YES, scheduled=NO-by-default
- [feedback_memory_snapshot.md](feedback_memory_snapshot.md) — When to call `snapshot_memory.py`
- [feedback_persistent_approvals.md](feedback_persistent_approvals.md) — On non-Bash approve: save to settings.json
- [feedback_global.md](feedback_global.md) — Global feedback rules across all projects
- [feedback_shutdown_via_claude.md](feedback_shutdown_via_claude.md) — Shutdown trigger phrases + checklist
- [feedback_no_blocking_prompts_when_afk.md](feedback_no_blocking_prompts_when_afk.md) — Don't suspend turn waiting for UI approval when user is AFK
- [feedback_first_principles_planning.md](feedback_first_principles_planning.md) — For reproduce/fork plans, start with functional definition not file inventory
- [feedback_no_task_recaps.md](feedback_no_task_recaps.md) — Don't repeat task lists in responses
- [feedback_diagnose_before_suggesting.md](feedback_diagnose_before_suggesting.md) — Verify processes running before recommending user actions
- [feedback_dont_assert_never_worked.md](feedback_dont_assert_never_worked.md) — Current error ≠ "never existed"
- [feedback_optimism_drift.md](feedback_optimism_drift.md) — Opus over-optimism; default to planning + show artifacts
- [feedback_hallucination_pattern.md](feedback_hallucination_pattern.md) — Hallucinated tool/repo names; verify before citing

## Behavior Rules — Tools & Workflow
- [feedback_dashboard_html.md](feedback_dashboard_html.md) — Present dashboards via HTML, not terminal markdown
- [feedback_push_notifications_enabled.md](feedback_push_notifications_enabled.md) — Push on AFK long-task done + blockers; minimal chatter
- [feedback_telegram_immediate_react.md](feedback_telegram_immediate_react.md) — First tool call on incoming Telegram = emoji react
- [feedback_telegram_reply_channel_match.md](feedback_telegram_reply_channel_match.md) — Substantive replies: chat-UI if at desktop, Telegram if AFK
- [feedback_mcp_config_location.md](feedback_mcp_config_location.md) — User-level MCP in ~/.claude.json, NOT ~/.claude/mcp.json

## Reference
- _Drop your own reference memories here — credentials, toolchain inventory, etc._

## Archived / Superseded
- _Memories pruned over time end up referenced here, or get removed entirely (git log of memory dir is the audit trail)._

---

*This index is auto-loaded on every session start. Keep it under 200 lines — entries past 200 are truncated. One-line entries with [[links]] only; never write content directly into this file.*
