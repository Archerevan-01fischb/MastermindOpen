---
name: medical-a1c
description: A1C tracking — values over time, target, controlling levers (diet, weight, meds).
metadata:
  type: medical
---

# A1C

## Current state

- **Latest A1C:** {LATEST_A1C}% on {LATEST_DATE}
- **Trend:** {TREND} (e.g. "5.9 → 5.8 over 12 months on diet alone")
- **Target:** {TARGET_A1C}% (e.g. "<5.7 — drop out of prediabetic range")
- **On meds:** {ON_MEDS} (e.g. "no — diet only", "metformin 500mg/day")

## Drivers I'm using

- **Diet:** {DIET_LEVER} (see [[user_dietary_restrictions]])
- **Weight:** {WEIGHT_LEVER} (e.g. "weight stable at {WEIGHT} lb, no cut planned")
- **Exercise:** {EXERCISE_LEVER} (e.g. "PPL 6-day, see [[personal_weightlifting]]")

## History (last 5 readings)

| Date | A1C % | Fasting glucose | Notes |
|---|---|---|---|
| {DATE_1} | {A1C_1} | {FG_1} | {NOTES_1} |
| {DATE_2} | {A1C_2} | {FG_2} | {NOTES_2} |
| ... | | | |

## Provider

- **Primary care:** {PCP_NAME} at {PRACTICE}
- **Endocrinologist:** {ENDO_NAME} (if applicable)
- **Lab order cadence:** {LAB_CADENCE} (e.g. "every 6 months")

## What mastermind does with this

- Surface trend when relevant ("your last A1C was {X}, target {Y}")
- Don't flag every carb suggestion as metabolic risk — that gets noisy
- DO flag if I'm doing something that has caused a spike in past readings
