# Shutdown Chain (Home Assistant SSH fallback)

**Optional.** The primary shutdown path is "DM Claude → Claude runs hygiene + snapshot → Claude issues shutdown" (defined in `memory/feedback_shutdown_via_claude.md`). The HA SSH fallback exists for one specific failure mode: **the PC is on but Claude is dead**. In that case, your DM path is gone too. This is the backup.

## When to use HA fallback

| Situation | Use which path? |
|---|---|
| Normal end-of-day | DM Claude (Telegram or local terminal) |
| Tomorrow's "good night" | DM Claude |
| Claude crashed, you need to power off | **HA SSH fallback** |
| Claude is unresponsive, terminal closed | **HA SSH fallback** |
| You want a forced reboot bypassing hygiene | HA SSH fallback (reboot variant) |

## Architecture

```
Phone (Home Assistant Companion app)
   ↓ tap "PC Shutdown FORCE" tile
HA dashboard runs script.pc_shutdown_force
   ↓
shell_command.pc_shutdown_force
   ↓
ssh <admin>@<pc-ip> "shutdown /s /t 0"
   ↓
PC powers off (no hygiene, no snapshot — that's the trade-off)
```

The SSH key path bypasses the Telegram channel entirely. You're trading off the hygiene sweep for the certainty that you can power-off when Claude is dead.

## Setup

### 1. Generate an SSH keypair inside HA

In your HA container/VM (over SSH or HA Terminal & SSH add-on):

```bash
mkdir -p /config/.ssh
ssh-keygen -t ed25519 -f /config/.ssh/id_ed25519 -N "" -C "ha-pc-shutdown"
cat /config/.ssh/id_ed25519.pub
```

Copy the public key — you'll install it on your PC next.

### 2. Install the public key on your PC

Use the `install_ha_pubkey.ps1.template` (in this directory) — run elevated. It:
- Installs the pubkey to `C:\ProgramData\ssh\administrators_authorized_keys`.
- Sets ACL to SYSTEM + Administrators only (Windows requires this for admin key auth).
- Ensures OpenSSH Server (sshd) is enabled and running.

### 3. Wire HA scripts and shell_commands

- Copy `ha-shell-commands.yaml.example` content into your `configuration.yaml` under `shell_command:`.
- Copy `ha-scripts.yaml.example` content into your `scripts.yaml`.

Then restart HA. You should see in the service registry:
- `script.pc_shutdown_force`
- `script.pc_reboot_force`
- (optional) `script.pc_boot` for WOL

### 4. Verify SSH from HA → PC

From the HA terminal:
```bash
ssh -i /config/.ssh/id_ed25519 -o StrictHostKeyChecking=no <admin>@<pc-ip> "whoami"
```
Should print your Windows admin username. If it fails, check the ACL on `administrators_authorized_keys` — Windows is strict about SYSTEM/Admin-only permissions on that file.

### 5. Build the dashboard

Copy `ha-pc-power-dashboard.json.example` into the Lovelace dashboard editor (Raw config edit). It defines three tile cards:

- **Green** — PC Boot (WOL, no confirmation needed)
- **Yellow** — PC Reboot FORCE (with confirmation dialog)
- **Red** — PC Shutdown FORCE (with confirmation dialog)

The confirmation dialogs are critical — you don't want to mash the wrong button mid-meeting.

### 6. Add the "PC Power" area + Assist aliases

See `area-and-aliases-setup.md` for the step-by-step. The TL;DR:
- Create an HA area named "PC Power".
- Move the three scripts into it.
- Add Assist aliases ("power off the PC", "kill the PC", "shut down the desk", etc.) so you can voice-control it from a speaker.

## Safety notes

- **The force shutdown is force.** No hygiene sweep, no save, no snapshot. Don't tap it unless you actually need it.
- **Anyone with access to your HA dashboard can power off your PC.** Treat HA access like a password. Don't expose HA publicly without strong auth (preferably Tailscale + LE cert; see `integrations/home-assistant.md`).
- **The SSH key is your perimeter.** If the HA container is compromised, the attacker can power-cycle your PC. Use HA-side firewall rules to limit exposure of the HA container itself.

## Removing the fallback

If you decide you don't need it:
1. Remove the scripts from `scripts.yaml`.
2. Remove the `shell_command:` entries from `configuration.yaml`.
3. Restart HA.
4. On the PC: delete `C:\ProgramData\ssh\administrators_authorized_keys` (only if no other admin keys are stored there).
