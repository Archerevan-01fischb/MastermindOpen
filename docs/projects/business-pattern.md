# Business / LLC Pattern

Canonical shape for a small business with multiple operational surfaces.

## The surfaces

A typical small business / LLC has:

| Surface | What | Vendor (typical) |
|---|---|---|
| Legal entity | LLC / S-Corp / etc. | State of registration + IRS EIN |
| Website | Landing + content | Cloudflare Pages, Vercel, Netlify, WordPress |
| Email | `info@yourdomain` etc. | Google Workspace, Fastmail, Zoho |
| Calendar | Booking / scheduling | Google Calendar (or Calendly for self-serve booking) |
| Accounting | Books, P&L, tax prep | QuickBooks Online (most common) |
| E-signature | Contracts, releases | DocuSign, HelloSign, Adobe Sign |
| Ads | Paid acquisition | Google Ads, Microsoft Ads, Meta Ads |
| Analytics | Web + ad attribution | GA4, Cloudflare Analytics, Plausible |
| Payments | Receivables | Stripe, Square, Google Payments |
| Bank | Operating account | Local bank or Mercury / Novo for online |

Mastermind orchestrates across these via MCP integrations (Gmail, Calendar, QuickBooks, DocuSign).

## Operational cadence

### Daily

- Triage `info@yourdomain` for client emails (Gmail MCP).
- Calendar check for next appointments.
- Quick QuickBooks ledger glance for any new transactions to categorize.

### Weekly

- Process accumulated receipts → Journal Entries in QB (see "owner-paid expenses" below).
- Ads review (only if you're actively running ads; respect the "no changes from <2 weeks data" rule per the Ads playbook).
- Calendar / scheduling housekeeping.

### Monthly

- Run P&L + balance sheet (QB).
- Reconcile bank account against QB.
- Review subscription expenses (cancel anything unused).

### Quarterly

- File quarterly estimated taxes (if self-employed).
- Sales tax filing (if applicable).
- Review pricing.

### Annually

- File income taxes (with accountant if you have one).
- Renew domain + business license + LLC registration.
- Audit insurance policies.

## Owner-paid business expenses (the QB gotcha)

When you pay a business expense from a personal card, the QB entry is **NOT** an "expense" or a "bill." It's a **Journal Entry**:

- Debit: the expense account (e.g. "Subscription Services")
- Credit: Owner Equity / Owner Investments

Easy to get wrong. Easy to forget. Mastermind should know to use a Journal Entry when you say "I paid X from my personal card for the business."

If you forward receipts to QB via email forwarding, the auto-categorization will treat them as Expenses — WRONG. Manual entry as Journal Entry is the right move.

See `memory/feedback_owner_paid_business_expenses.md` if you adopt this pattern (or write one — it's worth the rule).

## Email / calendar conventions

- Business events on the business calendar (`info@yourbusiness.com` calendar). Personal events on personal. Never mix.
- Business calendar uses one accent color schema (per `user_calendar_color_schema.md`); personal uses another.

## Ads — the 2-week rule

Don't make ad-spend changes from less than 2 weeks of data. Statistical noise dominates. Honor PMax learning periods. See `memory/feedback_ads_analysis.md` if you adopt.

## Winding down

Eventually a business closes (success or otherwise). Pre-decommission checklist:

1. Pause new acquisition (turn ads off; remove sign-up flows).
2. Notify active clients (30+ day notice for service businesses).
3. Export records: client list, financials, contracts.
4. Cancel paid subscriptions in this order — keep email + calendar live until last:
   - Ads first (no more spend).
   - Payments (no more receivables).
   - Bookkeeping (after last quarter close).
   - Hosting + website (after last visit).
   - Email + calendar (last — keep reachable for inbound for 60 days).
5. Final tax filings.
6. Dissolve LLC with the state.

Order matters. Don't kill email first — you'll miss the "wait, are you closing?" replies.

## Read also

- `templates/project-types/business/CLAUDE.md.template` — bootstrap template
- `integrations/quickbooks.md` — QB MCP setup
- `integrations/gmail.md` — multi-account Gmail
- `integrations/docusign.md` — DocuSign for contracts
- `integrations/google-calendar.md` — booking + scheduling
