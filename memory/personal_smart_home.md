---
name: personal-smart-home
description: Smart-home orchestration vignette — device catalog, integration dependency graph, hardware-gap tracking, REST/MQTT recipes. The orchestration layer; individual devices live in home_* template files.
metadata:
  type: personal
---

# Smart Home Orchestration

## Devices table

| Name | Type | Room | IP | MAC | Protocol | Integration | Notes |
|---|---|---|---|---|---|---|---|
| {DEV_1} | {TYPE_1} | {ROOM_1} | {IP_1} | {MAC_1} | {PROTO_1} | {INTEG_1} | {NOTES_1} |
| {DEV_2} | {TYPE_2} | {ROOM_2} | {IP_2} | {MAC_2} | {PROTO_2} | {INTEG_2} | {NOTES_2} |

## Integrations loaded

- **Home Assistant version:** {HA_VERSION} on {HA_HOST} (typically a NAS, RPi, or dedicated mini-PC)
- **Hubs / bridges:**
  - {HUB_1} (e.g. "Z-Wave 800 stick on /dev/ttyACM0")
  - {HUB_2}
- **Cloud-bridged integrations:** {CLOUD_INTEGRATIONS} (e.g. "Google Home, SmartThings")
- **Local-only integrations:** {LOCAL_INTEGRATIONS}

## Integrations pending / blocked

- {PENDING_1} (e.g. "Orbit B-hyve via HACS — Bruce credentials in 1Password")
- {PENDING_2}

## Hardware blockers

(Things that can't be integrated until you buy something.)

- {BLOCKER_1} (e.g. "garage door — needs ratgdo ($27-45), only viable path")
- {BLOCKER_2}

## MCP bridge

- **MCP server endpoint:** {MCP_ENDPOINT} (if running mcp__homeassistant)
- **Token rotation cadence:** {TOKEN_ROTATION}

## REST / MQTT recipe library

(Common automations / actions worth keeping handy as snippets.)

### Turn off everything in a room
```yaml
{TURN_OFF_ROOM_SNIPPET}
```

### TTS broadcast to a media player
```yaml
{TTS_SNIPPET}
```

### Set volume on a media player
```yaml
{VOLUME_SNIPPET}
```

### Trigger a script remotely via SSH (PC boot / shutdown example)
```yaml
{SSH_TRIGGER_SNIPPET}
```

## OAuth account map

| Account | Owner | Used by |
|---|---|---|
| {ACCT_1} | {OWNER_1} | {USED_BY_1} |

## Areas / zones

(Logical groupings in HA so Assist understands "kitchen lights".)

- {AREA_1}: {AREA_DEVICES}
- {AREA_2}: {AREA_DEVICES}

## Voice Assist aliases (cheatsheet)

- {ALIAS_1} → {ENTITY_1}
- {ALIAS_2} → {ENTITY_2}

## Known issues

- {ISSUE_1} (e.g. "front door battery 40% — sensor type unidentified, troubleshoot next time")
