# HA Area + Assist Aliases for PC Power

After wiring the scripts (see `README.md`), polish the UX so voice control works smoothly.

## 1. Create a "PC Power" area

Settings → Devices & Services → Areas → "+ Add Area" → name it `PC Power`.

Pick an icon — `mdi:desktop-classic` is the typical choice.

## 2. Assign the scripts to the area

Each script (`script.pc_boot`, `script.pc_shutdown_force`, `script.pc_reboot_force`) needs to be tagged with the area:

Settings → Devices & Services → Helpers → find each script → Configure → set Area to `PC Power`.

## 3. Add Assist aliases (the voice phrases)

For each script, add multiple aliases so voice Assist understands various phrasings:

### `script.pc_boot`
- "boot the PC"
- "wake the PC"
- "wake the desk"
- "turn on the PC"
- "turn on the desk"
- "power on the PC"

### `script.pc_shutdown_force`
- "force shutdown the PC"
- "kill the PC"
- "force off the PC"
- "force power off the PC"
- "force off the desk"

### `script.pc_reboot_force`
- "force reboot the PC"
- "force restart the PC"
- "cycle the PC"
- "power cycle the PC"

## 4. Mind the trigger overlap with shutdown-via-Claude

Notice the **force** prefix. The Claude-mediated DM shutdown triggers (`shut down`, `good night`, `power off`) intentionally do NOT include the word "force" — that's the routing signal. So:

- "Shut down" → Claude (hygiene + snapshot first)
- "Force shutdown" → HA (no hygiene, immediate)

This keeps the user-language differentiation clear: **force = bypass Claude**.

## 5. Test

With Claude alive AND running:
- "Hey {assistant}, shut down" → should go to Claude (no HA action), hygiene sweep runs.

With Claude dead:
- "Hey {assistant}, force shutdown the PC" → HA dashboard fires `script.pc_shutdown_force`, PC powers off.

Both should work. If Claude doesn't pick up the "shut down" phrase, see `memory/feedback_shutdown_via_claude.md` trigger list.
