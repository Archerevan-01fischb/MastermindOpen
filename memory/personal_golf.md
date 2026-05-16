---
name: personal-golf
description: Personal golf tracker — home course, current swing keys, handicap, gear, range/play schedule. Read in order when discussing golf.
metadata:
  type: personal
---

# Golf

## Identity

- **Handicap:** {HANDICAP}
- **Home course:** {HOME_COURSE} ({HOME_COURSE_LOCATION})
- **Secondary regular course:** {SECONDARY_COURSE}
- **Goal:** {SEASON_GOAL} (e.g. "consistent contact, then putting")

## Current swing keys (in order — read top to bottom)

These are the {N_KEYS} keys I'm currently using. Order matters — the first key gates the next. If the first stops working, all of them are off.

1. **Key 1: {SWING_KEY_1}** — {KEY_1_DESCRIPTION}
2. **Key 2: {SWING_KEY_2}** — {KEY_2_DESCRIPTION}
3. **Key 3: {SWING_KEY_3}** — {KEY_3_DESCRIPTION}
4. **Key {N}: {SWING_KEY_N}** — {KEY_N_DESCRIPTION}

## Gear

- **Driver:** {DRIVER}
- **Fairway/hybrid:** {FAIRWAY_HYBRID}
- **Irons:** {IRONS}
- **Wedges:** {WEDGES}
- **Putter:** {PUTTER}
- **Ball:** {BALL} (e.g. "TaylorMade TP5x — track if I change brand, performance drifts")
- **Tees / grips / glove brand:** {ACCESSORIES}

## Distance reference (carry, not total)

| Club | Yards |
|------|-------|
| Driver | {DRIVER_YARDS} |
| 3-wood | {3W_YARDS} |
| 4-iron | {4I_YARDS} |
| 7-iron | {7I_YARDS} |
| PW | {PW_YARDS} |
| SW | {SW_YARDS} |

## Standing warnings / watchlist

(Things to mention if they come up in conversation — see [[personal_golf_watchlist]] companion file if you split it out.)

- {WATCH_1} (e.g. "wrist hinge feels lazy when grip pressure ≥6 — caused last round's pulls")
- {WATCH_2}

## Practice schedule

- **Range:** {RANGE_FREQUENCY}
- **Short game:** {SHORT_GAME_FREQUENCY}
- **Course play:** {COURSE_FREQUENCY}
- **Lesson cadence:** {LESSON_FREQUENCY} with {INSTRUCTOR_NAME} at {INSTRUCTOR_LOCATION}

## Rationale (deep-dive — debug only, don't recite)

When the keys above STOP working, this is the WHY for each so mastermind can help diagnose. Don't read this section unless I ask.

- **Why Key 1 works:** {KEY_1_RATIONALE}
- **Why Key 2 works:** {KEY_2_RATIONALE}
- ...
