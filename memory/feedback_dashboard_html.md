---
name: Dashboard results must be HTML
description: When running dashboards, always update and open dashboard.html — never dump results as markdown text in the terminal.
type: feedback
---

Always present dashboard results by updating an HTML dashboard file and opening it in the browser. NEVER dump dashboard results as markdown tables in the terminal.

**Why:** A styled HTML dashboard with tabs, charts, and color-coded badges is the right surface for at-a-glance system health. Markdown tables in the terminal are hard to skim and lose the visual encoding that makes a dashboard a dashboard.

**How to apply:** When the user says "run dashboards" or "check dashboard for X":
1. Run all the commands to gather data.
2. Update `dashboard.html` (or whatever you've named it — see `scripts/render_dashboard.py.template`) with the new values and current timestamp.
3. Open it in the browser.

**Background-agent caveat — background agents cannot open GUI windows.** When dashboards run via a background agent:
- The **agent** gathers data and updates `dashboard.html`.
- The **main session** must open the browser AFTER the agent completes.
- Never delegate the browser-open step to the background agent.

**Opening Chrome on Windows:** Chrome is not in PATH. Use the full path:
```
"C:/Program Files/Google/Chrome/Application/chrome.exe" "<path>/dashboard.html" &
```
Do NOT use `cmd.exe /c start ""` — it silently fails.

**Template:** see `scripts/render_dashboard.py.template` for a generic fetch → render → open skeleton.
