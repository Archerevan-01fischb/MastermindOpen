---
name: first-principles-planning
description: For any plan that proposes to reproduce or fork an existing system, start with a functional definition (what it DOES, not what files it contains) and map every line to plan coverage. Reactive amendment-by-amendment planning misses meta-functions.
metadata:
  type: feedback
---

# First-principles planning for reproduce / fork / template tasks

Rule: For any plan that proposes to "reproduce" or "fork" something the mastermind already does, **start by writing a one-page functional definition**: WHAT does the thing being reproduced actually DO? Not what files it contains — what it functionally provides to the user. Map every line of that definition to coverage in the plan. If any line doesn't map, the plan has a gap.

**Why:** The failure mode is reactive amendment-by-amendment planning. The user keeps saying "have you added X core function?" and the assistant keeps saying "good catch, adding." Each amendment is correct but the meta-pattern is wrong: treating the system as "what's in the memory dir" instead of asking "what is it functionally." Several core functions get missed and only surface because the user catches the omissions one by one. A first-principles functional-definition pass surfaces them all at once.

**How to apply:**
- For "reproduce / fork / template / share-with-others" planning tasks: STEP 1 is a functional definition, not a file inventory. Numbered list, ~10–15 items, each describing a thing the system DOES for the user.
- STEP 2 is mapping each function to plan coverage (files, scripts, docs). Gaps = items to add.
- STEP 3 is the file / repo / tier breakdown — but it falls out of the functional definition, not the other way around.
- Sanity check at the end: ask "would a new user who follows the plan get a system that does function #X?" for each function. If not, gap.
- This applies to ANY "I want to reproduce my setup for someone else" task — not just a mastermind fork.

**Related:** [[feedback_vignette_blindspot]] (sibling meta-rule on evaluating template-worthiness), [[feedback_optimism_drift]] (related — defaults to planning and shows artifacts).
