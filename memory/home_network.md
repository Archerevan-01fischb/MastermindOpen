---
name: home-network
description: Home network topology — ISP, router, switches, AP layout, wired/wireless segmentation.
metadata:
  type: home
---

# Home Network

## ISP

- **Provider:** {ISP}
- **Plan:** {ISP_PLAN} ({DOWN}/{UP})
- **Modem:** {MODEM_MODEL} (owned / rented)
- **Public IP type:** {PUBLIC_IP_TYPE} (static / dynamic)

## Topology (wired core)

```
ISP modem
   │
   └── {ROUTER_MODEL} (router/firewall)
         │
         ├── {SWITCH_1} ({SPEED}, port count) — {LOCATION_1}
         │     ├── {DEVICE_1}
         │     ├── {DEVICE_2}
         │     └── ...
         │
         └── {SWITCH_2} — {LOCATION_2}
               └── ...
```

## Wireless

- **AP system:** {AP_SYSTEM} (e.g. "UniFi 3x U6-LR")
- **SSID 1 (primary):** {SSID_1} — {BAND} — {LOCATION}
- **SSID 2 (IoT):** {SSID_2} — segmented to {IOT_VLAN}
- **Guest network:** {GUEST_DETAILS}

## VLANs / segmentation

- **VLAN 1:** {VLAN_1_PURPOSE}
- **VLAN 2:** {VLAN_2_PURPOSE}
- **Firewall rules of note:** {FW_RULES}

## Static reservations

| Hostname | IP | MAC | Purpose |
|---|---|---|---|
| {HOST_1} | {IP_1} | {MAC_1} | {PURPOSE_1} |

## Known issues / drama

- {ISSUE_1}
- {ISSUE_2}

## Service / vendor info

- **Network installer:** {INSTALLER}
- **ISP support:** {ISP_SUPPORT_PHONE_OR_PORTAL}
