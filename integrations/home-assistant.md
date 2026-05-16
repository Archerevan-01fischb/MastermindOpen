# Home Assistant Integration

Smart home control + remote PC boot/shutdown via Home Assistant. Critical for the shutdown-chain HA fallback path (see `shutdown-chain/README.md`).

## What this enables

- Control lights / switches / scenes
- Trigger HA scripts (the main payload of this integration)
- TTS broadcasts to media players ("hey Kitchen Display, dinner's ready")
- Read live context (which devices are on, sensor readings)
- Pause / play media, set volume

Plus: when paired with the shutdown-chain (see Tier 6), HA becomes the dead-Claude fallback path for shutting down the PC.

## Setup

### 1. Have a Home Assistant install

If you don't already have HA running, this integration won't help. The typical setup is HA Container or HA OS on a small server (Raspberry Pi, NUC, NAS Docker host). HA setup is its own rabbit hole — skip to integrations.md if you want to defer this.

### 2. Long-lived access token

In HA:
1. Click your profile (bottom-left) → Long-Lived Access Tokens.
2. Create token, name it "mastermind".
3. Copy the token — you won't see it again.

### 3. Network access to HA

The MCP server needs to reach HA over HTTP. Two paths:

**Path A: same LAN (simplest).**
- HA URL: `http://<ha-host-ip>:8123/` (e.g. `http://192.0.2.55:8123/` — substitute your actual LAN IP)
- Works for desktop sessions on home Wi-Fi.

**Path B: off-LAN via Tailscale / Cloudflare Tunnel / similar.**
- Set up Tailscale on both HA and your dev machine (free for personal use).
- Tailscale's MagicDNS gives HA a fixed `*.tailnet.ts.net` hostname.
- Configure `tailscale serve` for HTTPS termination, OR use the LE cert Tailscale issues plus `http.trusted_proxies` in HA's `configuration.yaml`.

### 4. MCP server

The Anthropic-managed HA connector exposes tools at `mcp__homeassistant__*`. Setup:
- Settings → Connectors → Home Assistant → Connect.
- Paste the long-lived token + HA URL.

For a self-hosted MCP setup, see the community `hass-mcp` server on GitHub.

### 5. Trusted proxies (if using a reverse proxy)

If HA sits behind anything (Tailscale Serve, nginx, Caddy), you must allow that proxy in HA's `configuration.yaml`:

```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 127.0.0.1     # tailscale serve binds to localhost
    - 10.x.x.x      # add your proxy IPs
```

Restart HA after editing.

## Tools to know

(Subject to change — verify with `ToolSearch`.)

- `mcp__homeassistant__HassTurnOn` / `HassTurnOff` — turn entities on/off
- `mcp__homeassistant__HassLightSet` — brightness / color
- `mcp__homeassistant__HassBroadcast` — TTS to a media player
- `mcp__homeassistant__HassMediaPause` / `HassMediaUnpause` / `HassMediaNext`
- `mcp__homeassistant__HassSetVolume` / `HassSetVolumeRelative`
- `mcp__homeassistant__GetLiveContext` — pull current state of all entities
- `mcp__homeassistant__GetDateTime`
- `mcp__homeassistant__todo_get_items`
- Custom scripts you've defined in HA: `mcp__homeassistant__<script_name>` (e.g. `mcp__homeassistant__pc_boot`)

## Companion app (mobile)

For dashboards + the HA-fallback shutdown buttons to work on your phone:

1. Install Home Assistant Companion from Play Store / App Store.
2. **Connection settings:**
   - Home Assistant URL: tailnet URL or LAN URL.
   - **Internal connection URL:** set to your tailnet URL too if you want it to work from cellular without a "home network detected" hiccup.
3. After config changes, **force-stop the app** before retesting — it caches connection state aggressively.

## Common gotchas

- **`claude mcp list` ✓ Connected but tools don't load:** restart Claude Code, verify with `ToolSearch`. The "Connected" status doesn't mean tools loaded.
- **Companion app "home network detected" but on cellular:** the app misclassifies VPN as home network. Set BOTH internal and external URLs to the tailnet IP and force-stop after changes.
- **HA-side firewall (QuFirewall on QNAP, etc.):** if HA is behind a firewall that doesn't see your VPN interface (Tailscale on QNAP App Center is 2+ years old and `tailscale0` is invisible to QuFirewall's UI), you need to either disable that firewall or hand-edit its JSON config to add a `tailscale0` allow rule.

## Smoke test

```
Ask Claude Code: "What's the current state of <some-entity-id>?"
Expected: current state, last-updated timestamp, attributes.
```
