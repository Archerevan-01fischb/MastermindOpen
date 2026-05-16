---
name: user-profile
description: Core user profile — name, role, working style. Mastermind reads this every session to tailor responses.
metadata:
  type: user
---

# User Profile — {USER}

## Identity

- **Preferred name:** {USER}
- **Pronouns:** {PRONOUNS}
- **Time zone:** {TIMEZONE}
- **Location:** {CITY_REGION}

## Role

- **Day job:** {JOB_TITLE} at {ORGANIZATION}
- **Side projects:** {SIDE_PROJECTS_BRIEF}
- **Domain expertise:** {EXPERTISE_AREAS} (e.g. "10 years Go, new to Rust", "data scientist, light on devops")

## Working style preferences

- **Response length:** {SHORT_OR_THOROUGH} — e.g. "default to short, expand only when I ask"
- **Tone:** {DIRECT_OR_WARM} — e.g. "direct, no preamble"
- **Code comments:** {COMMENT_PREFERENCE} — e.g. "minimal, no obvious narrators"
- **Confirmation threshold:** {CONFIRMATION_PREFERENCE} — e.g. "confirm before destructive ops, otherwise go"
- **Notification preferences:** {PUSH_TELEGRAM_BOTH} — e.g. "push for AFK long-task done, Telegram for conversational"

## Hard constraints

(Things never to do, regardless of context — safety/identity/etiquette boundaries.)

- {CONSTRAINT_1}
- {CONSTRAINT_2}

## Strong soft preferences

(Defaults that should hold unless explicitly overridden in the moment.)

- {PREFERENCE_1}
- {PREFERENCE_2}

## How to ask me questions

- **Default channel:** {DEFAULT_CHANNEL} — e.g. "chat UI when I'm at the desk, Telegram if I'm AFK"
- **AFK signals:** I'll say "running errands" / "AFK" / "back later" — when you see these, switch to Telegram for substantive replies and never call blocking UI tools like `ExitPlanMode` until I'm back.
- **Genuine yes/no questions:** ask once, succinctly. Don't enumerate four options when I asked you for a recommendation.

## What I want from mastermind, specifically

(Why I installed this in the first place — keep this short and concrete.)

- {GOAL_1}
- {GOAL_2}
- {GOAL_3}
