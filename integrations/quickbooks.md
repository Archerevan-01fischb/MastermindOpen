# QuickBooks Integration (optional)

Read account data, create bills / invoices / expenses, generate P&L and balance sheet reports. Useful if you run a business.

## What this enables

- Read company info, accounts, customers, vendors, transactions
- Create + edit bills, invoices, expenses, sales receipts, deposits, journal entries, vendor credits
- Run reports: P&L, balance sheet, trial balance, account-period summary, account-transaction listings
- Query QBO data with their SQL-like query language

## Setup

### 1. QuickBooks Online developer account

1. Sign up at https://developer.intuit.com/.
2. Create an app for QuickBooks Online (not Desktop — those are different).
3. Get your **Client ID** and **Client Secret**.

### 2. Production vs Dev OAuth

**This is the most common gotcha** with QB MCP setup:

- **Sandbox / Development** OAuth credentials look like they should work. They sometimes don't. Some MCP servers fail OAuth with dev creds even though the OAuth dance completes.
- **Production** OAuth credentials are required for actual production company connections. The OAuth dance works reliably.

**If your QB MCP server isn't loading tools after setup,** the most likely cause (verified across multiple sessions, see [[feedback_mcp_config_location]]) is that you're using dev OAuth creds when you need production. Switch to production creds and rerun the auth flow.

### 3. OAuth dance

QuickBooks uses standard OAuth 2.0 + a `realmId` (your company ID):
1. Approve the integration in the QuickBooks Online consent screen.
2. Get back an authorization code.
3. Exchange for access + refresh tokens, save them.

The refresh token expires after 100 days of inactivity — keep using the integration to avoid re-auth.

### 4. Connect to a company

QBO is multi-tenant. You'll be asked which company to connect during the OAuth flow. Each company has its own `realmId`. The MCP server stores company + tokens together.

### 5. Register the MCP server

```bash
claude mcp add -s user quickbooks <launch-cmd>
```

Then run the included `qbo_authenticate` tool (or whatever your server calls it) on first use.

## Tools to know

(Subject to change — verify with `ToolSearch`.)

**Reading:**
- `list_accounts`, `get_company_info`, `get_balance_sheet`, `get_profit_loss`, `get_trial_balance`
- `account_period_summary`, `query_account_transactions`
- `get_bill` / `get_customer` / `get_vendor_credit` / `get_invoice` / `get_journal_entry` etc.
- `query` — run a QBO SQL-like query string

**Writing:**
- `create_bill` / `edit_bill`
- `create_invoice` / `edit_invoice`
- `create_expense` / `edit_expense`
- `create_journal_entry` / `edit_journal_entry`
- `create_sales_receipt` / `edit_sales_receipt`
- `create_deposit` / `edit_deposit`
- `create_vendor_credit` / `edit_vendor_credit`
- `create_customer` / `edit_customer`
- `delete_entity`

**Auth:**
- `qbo_authenticate` — kicks off the OAuth dance

## Common gotchas

- **Dev creds when you need prod creds:** see the warning under setup. If `claude mcp list` shows ✓ but `ToolSearch` returns nothing after restart, this is almost always the cause.
- **`claude mcp list` is misleading:** showing ✓ Connected doesn't mean tools load. Only `ToolSearch` post-restart is authoritative.
- **realmId scope:** tokens are per-company. If you have multiple companies in QBO, each one needs its own connection.
- **Owner-paid business expenses:** when paying a business expense from a personal card, the correct QB entry is a **Journal Entry** (debit the expense account, credit Owner Equity / Owner Investments). NOT an expense or a bill. Mastermind should know this; if not, see `feedback_owner_paid_business_expenses.md` in your live memory.

## Smoke test

```
Ask Claude Code: "What's my QuickBooks company info?"
Expected: company name, accountant name (if set), fiscal year start.
```
