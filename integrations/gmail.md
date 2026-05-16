# Gmail Integration (multi-account)

Read / draft / send / label / search Gmail across one or more Google accounts. Uses the open-source `gmail-multi` MCP server (search GitHub for the canonical repo — community-maintained).

## What this enables

- Search inboxes across multiple accounts in one query
- Draft and send mail (with explicit confirmation by default — set per-account policy)
- Apply / strip labels
- Read threads (the user can ask "what did I last say to X about Y?")
- Build label-based workflows (e.g. label="Receipts/Business" → file as QB expense)

## Setup

### 1. Google Cloud project + OAuth credentials

For each Gmail account you want to wire:

1. Go to https://console.cloud.google.com — create a new project (or reuse one).
2. Enable the **Gmail API** for that project.
3. **APIs & Services → Credentials → Create Credentials → OAuth client ID** → choose **Desktop** application type.
4. Download the JSON. You'll get something like `client_secret_<id>.json`.

### 2. Install gmail-multi

Check the gmail-multi MCP server's GitHub README for the canonical install. The shape is typically:

```bash
git clone <gmail-multi-repo-url>
cd gmail-multi
npm install     # or bun / pnpm depending on the project
```

### 3. First-run OAuth (per account)

Run the gmail-multi auth flow once per account. The server opens a browser to Google's consent screen; you log in to that specific Gmail account, approve scopes, and the resulting refresh token is saved to a per-account credentials file.

Per-account token files typically land at `~/.gmail-multi/<account>.json` (check the gmail-multi docs — naming varies by version).

### 4. Register the MCP server

```bash
claude mcp add -s user gmail-multi <command-to-launch-the-server>
```

Or hand-edit `~/.claude.json` per the example in `mcp-config-examples/claude.json.example`. **Don't** edit `~/.claude/mcp.json` — that's the wrong file (see [[feedback_mcp_config_location]]).

### 5. Verify

```bash
claude mcp list
# Should show ✓ Connected for gmail-multi
```

Then restart Claude Code and verify:
```
ToolSearch query: "select:mcp__gmail-multi__list_emails"
```

If the tool schema loads, it's live.

## Common gotchas

- **OAuth scope expansion:** if you later want to draft + send (not just read), you may need to re-run the OAuth flow with broader scopes. The refresh token doesn't grant scopes you didn't authorize.
- **Multiple accounts:** gmail-multi typically takes an `account` parameter on each call. Make sure mastermind knows which account corresponds to which domain (track this in your `user_{USER}.md` or in a dedicated `reference_gmail_accounts.md`).
- **Token refresh failures:** if the refresh token expires, the integration goes silent (no error, just no responses). Run the auth flow again.
- **Rate limits:** Gmail has per-user, per-method quotas. Don't loop over every message in a 10K-message inbox — paginate.

## Smoke test

```
Ask Claude Code: "What's my most recent email in {ACCOUNT}?"
Expected: subject line + sender + snippet, returned in ~2-5s.
```

## Privacy

The OAuth tokens grant gmail-multi (and therefore Claude) read/write access to the entire inbox. Treat the credential files like password manager exports. Add them to `.gitignore`. Rotate the OAuth client secret periodically.
