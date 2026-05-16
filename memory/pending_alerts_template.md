---
name: Pending Alerts (Template)
description: Generic pending-alerts pattern. Auto-populated by a scheduled task; surface non-empty content at session start; clear entries after discussion.
type: project
---
# Pending Alerts — {SOURCE}

Auto-populated by `{SCHEDULED_TASK_NAME}` on `{SCHEDULE}` (e.g. daily at 7am, or weekly Mon 7am).

When this file has alert entries below, surface the highlights to {USER} at session start. After discussion or action, clear the entries (leave the frontmatter + this paragraph).

## How to use this template

Copy this file to a domain-specific name and adapt the source:
- `pending_self_improvement.md` — checks Claude Code releases / changelog
- `pending_system_health.md` — checks NAS / VPS / router health
- `pending_certificate_expiry.md` — checks TLS certs that are within N days of expiry
- `pending_security_advisories.md` — checks for CVE feeds matching your stack

Each instance is one pending file. The startup-hook surface (Active Resume protocol, see [[feedback_automation_categories]]) reads all `pending_*.md` files and surfaces non-empty content.

---

_(empty — alerts will appear below this line when generated)_
