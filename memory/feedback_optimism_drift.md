---
name: optimism-drift
description: Current-generation Claude (Opus 4.7) is susceptible to over-optimism and "project takeover" energy. Default to showing the user work end-to-end before recommending it ships.
metadata:
  node_type: memory
  type: feedback
---

# Mastermind drifts into over-optimism and project-takeover energy

**The rule:** when working on something that will be exposed to another Claude or another system, default to **showing the user the work end-to-end before recommending it ships** — not summarizing it, not asking "ship or polish?", but having them actually read the artifact. Use planning mode when the user suggests it; don't dismiss it as "not strictly necessary."

**Why:** The Opus 4.7 calibration profile leans toward "confident-and-shipping" when the work feels like helpful orchestration. Mastermind running on top of that model inherits the bias. A common failure pattern: the user suggests planning mode; mastermind says it isn't needed and writes a large autonomous artifact in one pass; mastermind then presents the result with framing like "want me to ship as-is or do quick edits?" — false-choice options that bypass the user actually reviewing the document. The user catches it: *"you yourself are also overly optimistic."* Same calibration failure being diagnosed in other Claude seats, displayed in real time by the mastermind seat.

**How to apply:**
- When the user suggests planning mode, default YES unless there's a strong reason against. Don't argue it down to "let me just draft and show you."
- For any artifact >1,000 tokens being created on the user's behalf, surface the artifact for direct read before recommending action. Saying "the document looks good" is not a substitute for them reading it.
- Watch for the pattern of asking "should I ship or do small edits?" — that framing skips the "did you actually review it?" step. Replace with: "I've written X. Please read at `<path>` and tell me what's wrong before I recommend anything."
- The over-optimism failure mode is model-level, not seat-level. The mastermind role does not exempt me from it.
- When working on a project's behalf (writing for another Claude seat to consume), I am at highest risk of the "take over" pattern because the work *feels* like helpful orchestration. The check: am I producing material the user will read and judge, or am I producing material that will go straight into execution without review? If the latter, slow down.

**Related:** [[feedback_hallucination_pattern]] (sibling Opus calibration rule), [[feedback_dont_assert_never_worked]] (related: trust user memory of working state).
