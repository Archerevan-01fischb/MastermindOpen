---
name: personal-weightlifting
description: Weightlifting program — schedule, current phase, sheet locations, progression log. Read this before discussing lifts or generating new sheets.
metadata:
  type: personal
---

# Weightlifting

## Program identity

- **Program name:** {PROGRAM_NAME} (e.g. "Push-Pull-Legs A/B, 6-day rotating")
- **Source:** {PROGRAM_SOURCE} (e.g. "Renaissance Periodization Male Hypertrophy")
- **Current phase:** {CURRENT_PHASE} (e.g. "Phase 3 — 8-12 rep range")
- **Phase start date:** {PHASE_START}
- **Phase end date:** {PHASE_END}
- **Body-comp posture this phase:** {BODY_COMP_POSTURE} (e.g. "Maintenance, no cut during Phase 3")

## Schedule

- **Days:** {LIFT_DAYS} (e.g. "Mon Push A, Tue Pull A, Wed Legs A, Thu Push B, Fri Pull B, Sat Legs B")
- **Time of day:** {LIFT_TIME}
- **Location:** {GYM_NAME}

## Sheet locations

Live lift sheets are at:

- `{SHEET_ROOT}/{PHASE}/push-a.html`
- `{SHEET_ROOT}/{PHASE}/pull-a.html`
- `{SHEET_ROOT}/{PHASE}/legs-a.html`
- `{SHEET_ROOT}/{PHASE}/push-b.html`
- `{SHEET_ROOT}/{PHASE}/pull-b.html`
- `{SHEET_ROOT}/{PHASE}/legs-b.html`
- `{SHEET_ROOT}/progression-log.json` (canonical weight log per exercise)

## Per-cycle conventions

- **Weight progression rule:** {PROGRESSION_RULE} (e.g. "if all sets hit top of rep range with clean form → +5 lb next cycle for compounds, +2.5 for isolations")
- **Rep recording:** {REP_RECORDING_POLICY} (e.g. "weights only, no reps — sheet pre-prints the rep range")
- **Cycle length:** {CYCLE_LENGTH} (e.g. "1 cycle = full A/B rotation completed = ~9 days")

## Sheet generation conventions

- **Print limit:** {PRINT_LIMIT} (e.g. "2 pages per sheet — tighten exercise descriptions to fit")
- **Reference card included:** {REFERENCE_CARD} (e.g. "yes, last cycle's weights + exercise form notes printed on page 2")

## Progression log structure

`progression-log.json` shape:
```json
{
  "{exercise_name}": [
    {"date": "YYYY-MM-DD", "weight": "XX lb", "notes": "optional"}
  ]
}
```

## Macros for this phase

- **Protein target:** {PROTEIN_G_PER_DAY} g/day (see [[user_dietary_restrictions]])
- **Calorie posture:** {CALORIE_POSTURE}
- **Body weight tracking:** {WEIGHT_TRACKING_FREQUENCY}

## Active follow-ups

- {FOLLOW_UP_1} (e.g. "RDL cycle 3 decision — bump 20 → 22.5 if all sets clean")
- {FOLLOW_UP_2}
