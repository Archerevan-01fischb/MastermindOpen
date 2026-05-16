# Google Drive Integration

List / read / search files in Google Drive. Use the Anthropic-managed Cloud connector (`mcp__claude_ai_Google_Drive__*`).

## What this enables

- Search Drive ("find that contract I uploaded last month")
- Read file contents (Docs, Sheets, PDFs, text)
- Surface file URLs for sharing

## Setup

1. In Claude Code or Claude Desktop, open Settings → Connectors.
2. Find Google Drive, click Connect.
3. Browser → Google consent screen → approve.

## What it does NOT do

Note: at the time of writing, the Anthropic-managed Google Drive connector is **read-mostly** — list, read, search. It does NOT typically support upload / modify / delete from Claude Code. If you need write access, look at the community Google Drive MCP servers or build one against the Drive API directly.

## Authentication tools

Some versions of the connector expose:

- `mcp__claude_ai_Google_Drive__authenticate`
- `mcp__claude_ai_Google_Drive__complete_authentication`

These are for re-auth flows if the connection expires. You probably don't need to call them directly unless something has gone wrong.

## Common gotchas

- **Google Workspace vs personal Gmail:** Workspace OAuth may require an admin to approve the app for the org. If the connect flow loops back to consent without completing, check with your Workspace admin.
- **Sharing scope:** the connector sees files YOU have access to. Files shared with you (but in someone else's Drive) may or may not appear depending on the OAuth scopes granted.
- **PDF text extraction:** for scanned PDFs (image-only, no OCR layer), Claude can read them as images but Drive search won't index them. If a search misses something, the file might be OCR-less.

## Smoke test

```
Ask Claude Code: "List my 5 most recently modified files in Drive."
Expected: 5 file names + last-modified timestamps.
```
