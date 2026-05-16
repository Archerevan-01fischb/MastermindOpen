# Web Service / Aggregator Pattern

The canonical shape for an aggregator-style web service.

## Shape

```
Upstream feeds ──┐
                 ├──► Ingest ──► Processing ──► Storage ──► Web layer ──► Delivery
                 │   (poll)     (AI grade /     (DB)        (HTML +       (email
                 │              dedupe /        SQLite       REST +        digest,
                 │              summarize)      typically)   RSS)          RSS)
Other sources ──┘
```

Each layer is replaceable; the boundaries between them are the API contract.

## Tech-stack patterns that work

### "Rust + Axum + SQLite + Caddy" (lean, single-binary)
- Build: `cargo build --release`
- Deploy: scp binary + restart systemd unit
- Database: SQLite (single file, no separate DB process)
- Reverse proxy: Caddy with auto-Let's-Encrypt
- Cron: systemd timers

### "Python + FastAPI + Postgres + nginx" (mainstream)
- Build: `pip install -r requirements.txt`
- Deploy: scp + systemctl, or container
- Database: managed Postgres or self-hosted
- Reverse proxy: nginx with certbot
- Cron: systemd timers or crontab

### "Cloudflare Pages + Workers + D1" (serverless)
- Build: `npm run build`
- Deploy: `wrangler pages deploy`
- Database: D1 (SQLite at the edge)
- TLS: managed by Cloudflare
- Cron: Cloudflare Cron Triggers

Pick based on cost sensitivity, control needs, and how much VPS-fiddling you want to do.

## Critical considerations

### Cost (LLM tokens add up fast)

If your processing layer calls an LLM (grading articles, summarizing, dedupe), token costs can dwarf hosting costs. Track this from day one:

- Log every API call with token count + cost.
- Dashboard the daily/weekly cost.
- Optimize: prompt caching, batch APIs, smaller model for grading + bigger for summarizing.
- Hard rule: only call the expensive model once per high-value cycle (e.g. once per digest, not once per item).

### Subscribers / list management

If you have a newsletter / digest:

- DB schema includes a `subscribers` table with `confirmed` (boolean) for double-opt-in.
- Unsubscribe link in every email. Make it 1-click, not "fill out a form to unsubscribe."
- Backup the subscribers table to NAS before any deploy that touches the schema.

### Health monitoring

Dashboard should track:
- Service status (`systemctl is-active foo`)
- Disk free %
- Memory + load
- DB sizes (rows in critical tables)
- Recent error count (filtered for known-noise)
- Daily cost summary

See `memory/scripts/render_dashboard.py.template` for the rendering pattern.

### Wind-down / decommission

When you decide to wind down: have a checklist.
1. Backup the DB to NAS.
2. Forward active threads from project email to personal.
3. Cancel paid integrations (mail provider, hosting, ads).
4. Set a "going offline DATE" notice on the site for 30 days.
5. Final scrape of any data worth keeping (analytics, subscriber export).
6. Delete the VPS / hosting account.

Don't skip steps 1-5. The "I'll get to that later" trap kills more useful data than crashes do.

## Conventions

- **`./scripts/deploy.sh` is the only deploy path.** With flags for `--binary`, `--static`, `--config`. `--config` always deliberate (never accidentally redeploy config).
- **Cron jobs in `cron.d/`**, NOT in user crontabs. Centralize.
- **Secrets in `.env` files**, NOT committed. Reference from systemd unit files.
- **Logs go to journald**, not files. `journalctl -u foo` is the canonical "tail logs."

## Read also

- `templates/project-types/web-service/CLAUDE.md.template` — the bootstrap template for this pattern
- `memory/scripts/render_dashboard.py.template` — dashboard rendering skeleton
- `startup-chain/weekly_system_health.ps1.template` — health-check pattern for VPS
