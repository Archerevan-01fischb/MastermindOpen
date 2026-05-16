---
name: hallucination-pattern
description: "Current-generation Claude (Opus 4.7) hallucinates confidently — especially named external tools, library/package names, and second-hand summaries from subagents. Verify before citing."
metadata:
  node_type: memory
  type: feedback
---

Mastermind (current Opus generation) hallucinates confidently. The same calibration pattern that produces optimism drift ([[feedback_optimism_drift]]) also produces plausible-sounding fabrications of external resources — repo names, package names, tool capabilities, specific people, version numbers, command-line flags. These read as authoritative because the model has *some* signal about the surrounding space, but the specific identifier is invented.

**How to apply:**
- **Ground specs in source the user can verify.** Specs derived from Read-tool reads of actual files in their codebase = trustworthy. Specs derived from subagent summaries, training-data recall about tools, or web knowledge that's months old = suspect.
- **Verify named external tools before recommending.** When tempted to name a specific GitHub repo, npm/pip/crates.io package, MCP server, or third-party CLI: WebSearch first, cite the URL. If the search produces nothing concrete, say so instead of inventing a plausible name.
- **Distinguish "I read this" vs "I recall this"** in user-facing responses. If a fact comes from a tool call earlier in this conversation, say so. If it comes from training, flag it as such.
- **Subagent outputs are not ground truth.** Treat them as drafts that may contain confident inferences past their actual evidence.
- When the user says "that turned out to be wrong," don't get defensive — update the affected claims and tighten verification on adjacent ones.

Related: [[feedback_optimism_drift]], [[feedback_diagnose_before_suggesting]].
