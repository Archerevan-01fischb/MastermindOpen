---
name: medical-blood-pressure
description: Blood pressure tracking — current state, meds, target. Drives sodium / cardio / med-reminder rules.
metadata:
  type: medical
---

# Blood Pressure

## Current state

- **Resting BP (recent average):** {SYS}/{DIA} mmHg
- **Heart rate (resting avg):** {HR_RESTING} bpm
- **Target BP:** {TARGET_SYS}/{TARGET_DIA} mmHg
- **Last measured:** {LAST_MEASURED_DATE}

## Meds

- **Medication 1:** {MED_1} {MED_1_DOSE} once daily (started {MED_1_START_DATE})
- **Medication 2:** {MED_2_OR_NONE}
- **Adherence:** {ADHERENCE_NOTES} (e.g. "morning with breakfast — set Apple Watch reminder")

## How well it's controlled

- {CONTROL_STATUS} (e.g. "excellent — averaging 118/76 since starting losartan 100mg")

## What mastermind should NOT do

- {DONT_DO_1} (e.g. "don't flag every sodium-heavy meal — BP is controlled, normal salt is fine")
- {DONT_DO_2}

## What mastermind should do

- {DO_1} (e.g. "if I miss meds for a day, log it; if it happens twice in a week, flag it")
- {DO_2} (e.g. "if I report BP readings outside target range, summarize the trend")

## Provider

- **Primary care:** {PCP_NAME}
- **Check-in cadence:** {CADENCE}
