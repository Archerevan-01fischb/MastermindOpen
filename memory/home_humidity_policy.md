---
name: home-humidity-policy
description: Home humidity setpoints — steady-state, transitional, seasonal adjustments. Drives humidifier/dehumidifier control.
metadata:
  type: home
---

# Home Humidity Policy

## Setpoints

- **Steady state (mild outdoor temps):** {STEADY_MIN}-{STEADY_MAX}% RH
- **Cold snap recovery (post-deep-cold):** {COLD_MIN}-{COLD_MAX}% RH (window-condensation tolerated briefly)
- **Hot/humid outdoor:** {HOT_MIN}-{HOT_MAX}% RH (dehumidify mode)
- **Winter steady:** {WINTER_MIN}-{WINTER_MAX}% RH

## Equipment

- **Humidifier:** {HUMIDIFIER_MODEL} (e.g. "Aprilaire 720A whole-house")
- **Dehumidifier:** {DEHU_MODEL}
- **Thermostat:** {THERMOSTAT_MODEL}
- **Humidity sensors:** {SENSOR_LOCATIONS}

## Why these setpoints

- {RATIONALE_1} (e.g. "below 30% → static shocks, dry mucous membranes, wood movement on instruments/furniture")
- {RATIONALE_2} (e.g. "above 50% → window condensation in winter")
- {RATIONALE_3} (e.g. "trade-off chosen with installer {INSTALLER_NAME}")

## Triggers to act

- **If <{STEADY_MIN}%:** raise humidifier setpoint OR check water supply line
- **If >{STEADY_MAX}%:** lower humidifier OR check bypass damper
- **Persistent condensation on windows:** drop {N}% pts temporarily

## Service notes

- **HVAC contractor:** {HVAC_CONTRACTOR} ({HVAC_PHONE})
- **Humidifier service cadence:** {HUMIDIFIER_SERVICE} (filter change interval)
- **Last service:** {LAST_SERVICE_DATE}
