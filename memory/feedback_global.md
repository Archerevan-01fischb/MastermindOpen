---
name: Global feedback rules
description: Feedback and behavioral rules that apply across ALL projects — save before restart, research limits, no trailing summaries, etc.
type: feedback
---

**Save before restart:** NEVER suggest restarting anything without first saving all progress to memory. Work has been lost to crashes before.
**Why:** Past incidents where in-flight work was lost during restarts.
**How to apply:** Before any restart/reboot suggestion, write all current state to memory files first.

**Research scope:** Keep web research to 2-3 targeted fetches. NEVER launch massive agent crawls with dozens of parallel web searches.
**Why:** Runaway research sessions burn token budgets and bury the user in noise.
**How to apply:** When researching, pick 2-3 best sources and fetch those. If insufficient, ask before expanding.

**No trailing summaries:** Don't summarize what you just did at the end of every response. The user can read the diff/output.
**Why:** Trailing recaps add token cost and read as filler.
**How to apply:** After completing work, state the outcome briefly (1 line) or just show the result. No recap paragraphs.

**Don't repeat done work:** Check memory files FIRST before suggesting any action. If it's marked DONE, don't bring it up again.
**Why:** Re-suggesting completed work erodes trust in your memory.
**How to apply:** Read relevant memory before making suggestions or creating checklists.

**Channel-availability hints don't need rediscovery.** If a channel (Telegram, Push, MCP) was confirmed available, don't keep telling the user to "restart with --channels X" or "enable Y" — those flags/configs are part of how they always start. Surface that fact only if there's positive evidence it's actually missing this session.
**Why:** Re-prompting "you need to restart with the channels flag" across many sessions when the channel is fine is high friction.
**How to apply:** Trust the previous-session memory. If telegram is on, use it. Don't mention the flag unless it's actually broken.
