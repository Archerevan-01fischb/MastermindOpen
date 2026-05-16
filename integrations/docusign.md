# DocuSign Integration (optional)

Send envelopes for signature, list agreements, track workflows. Useful if you run a business / LLC that needs signature workflows.

## What this enables

- Create + send envelopes (single recipient or multi-step routing)
- List envelopes (sent / received / draft)
- Get envelope status (sent / delivered / signed / declined)
- List + run workflows (templated multi-recipient flows)
- Send reminders to pending signers

## Setup

### 1. DocuSign developer account

1. Sign up at https://developers.docusign.com/.
2. Create an integration key (your "client ID").
3. Choose JWT Grant or Auth Code Grant for the integration.

### 2. JWT path (recommended for unattended use)

DocuSign JWT auth is server-to-server with a key file. Procedure:
1. In the DocuSign Admin → Apps & Keys → your integration → Service Integration → generate an RSA keypair.
2. Save the private key file (PEM format) somewhere safe.
3. The MCP server needs: integration key, user GUID (impersonated user), and the private key file path.

### 3. Sandbox first

Always wire to the DocuSign **sandbox** (demo) environment first:
- Base URL: `https://demo.docusign.net/`
- Authentication: `https://account-d.docusign.com/`

Test the full flow (create + send + sign) in sandbox before flipping to production.

### 4. Production

When you flip to production, you need to **promote** the integration key to production via the DocuSign Admin UI. Each integration has its own promotion flow.

### 5. Register the MCP server

```bash
claude mcp add -s user docusign <launch-cmd>
```

## Tools to know

The Anthropic-managed DocuSign connector exposes (subject to change — verify with `ToolSearch`):

- `createEnvelope` / `getEnvelope` / `getEnvelopes` / `updateEnvelope` / `updateEnvelopeRecipients`
- `listRecipients` / `sendReminder`
- `getAgreementDetails` / `getAllAgreements`
- `getTemplates`
- `triggerWorkflow` / `pauseNewWorkflowInstances` / `resumeWorkflow` / `cancelWorkflowInstance`
- `getWorkflowInstance` / `getWorkflowInstancesList` / `getWorkflowsList`
- `getWorkflowTriggerRequirements`
- `getUser` / `getUsers` / `getUserInfo` / `getAccount`

## Common gotchas

- **Sandbox vs production**: easy to mix up. The endpoints, auth servers, and integration-key promotions are all separate. Confirm which environment you're in before sending anything to a real signer.
- **Templates vs envelopes**: a template defines fields + routing; an envelope is an instance of a template sent to specific recipients. Don't conflate them.
- **JWT impersonation grants**: the user GUID you impersonate must consent to the impersonation on first run. There's a one-time consent URL the DocuSign Admin must visit.
- **PII in envelopes**: agreements contain real names, addresses, signatures. Never paste an envelope ID into a public log or screenshot without redaction.

## Smoke test

```
Ask Claude Code: "List my most recent 5 DocuSign envelopes."
Expected: 5 envelope IDs + statuses + recipient names.
(Run against sandbox, not prod, for your first test.)
```
