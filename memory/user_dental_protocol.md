---
name: dental-protocol
description: Daily / monthly / quarterly dental routine. Mastermind tracks adherence + reminds for replacement intervals.
metadata:
  type: user
---

# Dental Protocol

## Daily routine

- **Morning:** {AM_ROUTINE} (e.g. "Dr. Plotka mini-brush, then 30s of xylitol rinse")
- **Evening:** {PM_ROUTINE} (e.g. "Floss → brush → fluoride rinse → 5min nightguard insert")
- **After meals:** {POST_MEAL_ROUTINE}

## Replacement intervals

- **Toothbrush replacement:** every {BRUSH_INTERVAL} (e.g. "3 months — set calendar reminder")
- **Floss type:** {FLOSS_TYPE}
- **Rinse type:** {RINSE_TYPE} (e.g. "Closys preDIN morning; ACT Anticavity evening")
- **Nightguard:** {GUARD_TYPE} (e.g. "custom upper guard from Dr. {DENTIST_NAME}, replace every 2 years")

## Practitioner protocol

- **Dentist:** {DENTIST_NAME}, {DENTIST_PRACTICE_NAME}
- **Hygiene visits:** {HYGIENE_CADENCE} (e.g. "every 4 months")
- **Source/protocol followed:** {PROTOCOL_SOURCE} (e.g. "the multi-rinse xylitol-heavy protocol from {DENTIST_AUTHOR}'s book")

## Conditions to track

- {CONDITION_1} (e.g. "TMJ — see [[medical_night_guard]]")
- {CONDITION_2} (e.g. "gum recession on lower-left molar — monitor each cleaning")

## Reminders mastermind owns

- **Brush replacement reminder:** add a calendar event every {BRUSH_INTERVAL} for "{REMINDER_TEXT}"
- **Hygiene appointment reminder:** check {N_DAYS} days before each scheduled visit
- **Guard replacement reminder:** {GUARD_REPLACEMENT_DATE}
