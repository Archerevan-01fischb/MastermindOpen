---
name: Don't assert "never worked" from a current error
description: When a URL/service errors today, don't conclude it never worked — investigate history first, especially if the user remembers it working.
type: feedback
---

When something is broken today (Cloudflare 530, 404, dead DNS, missing file), do NOT tell the user "this was never set up" or "this was aspirational" unless you have positive evidence it never existed. A current error usually means something *broke*, not that it was never built.

**Why:** A Cloudflare 530 means "origin unreachable," not "no such hostname." The DNS still resolved to Cloudflare's proxied IPs, which should read as "this hostname IS configured, the backend is what's broken." Asserting "never worked" when the user remembers it serving traffic erodes trust and wastes time on the wrong diagnostic path.

**How to apply:**
- Cloudflare 530 / 522 / 521 → origin connectivity problem; the public hostname exists.
- Cloudflare 1016 / NXDOMAIN → no DNS, *then* you can say it doesn't exist.
- A 404 from a real server → file/route missing, but the host is up.
- Before saying "X was never deployed," check git history, log files, whatever shows past state.
- If the user remembers something working, they're almost certainly right — believe them and figure out what broke.
