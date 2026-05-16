---
name: travel-profile
description: Travel preferences — cabin class, hotel loyalty, insurance, routing preferences. Drives flight + hotel suggestions.
metadata:
  type: user
---

# Travel Profile

## Air travel

- **Domestic preferred class:** {DOMESTIC_CLASS} (e.g. "Main Cabin Extra+", "First if available")
- **International preferred class:** {INTERNATIONAL_CLASS} (e.g. "Business class always", "Premium Economy on flights <8 hr")
- **Preferred airlines (alliance):** {AIRLINE_GROUP} (e.g. "OneWorld via AA")
- **Status / frequent-flyer:** {FF_PROGRAMS} (e.g. "AA Platinum, Delta SkyMiles")
- **Seat preference:** {SEAT_PREFERENCE} (window / aisle / front / back / exit row)
- **Stopover style:** {STOPOVER_PREFERENCE} (e.g. "Turkish Airlines free stopover in Istanbul preferred")

## Hotels

- **Chain loyalty:** {HOTEL_CHAIN} (e.g. "Marriott Bonvoy", "Hyatt", "IHG")
- **Status tier:** {HOTEL_STATUS}
- **Room preferences:** {ROOM_PREFS} (e.g. "high floor", "king bed", "away from elevator")
- **Brands to avoid:** {AVOID_BRANDS}

## Ground

- **Rental car:** {RENTAL_PREF} (e.g. "Hertz Gold, mid-size SUV")
- **Rideshare vs taxi:** {RIDE_PREF}
- **Public transit comfort:** {TRANSIT_COMFORT}

## Insurance

- **Annual travel insurance:** {INSURANCE_PROVIDER} (e.g. "Allianz Prime annual policy")
- **Trip cancellation policy:** {TRIP_CANCEL}
- **Medical-evacuation coverage:** {EVAC_COVERAGE}

## Trip cadence

- **Approximate trips per year:** {TRIPS_PER_YEAR}
- **Typical trip duration:** {TYPICAL_DURATION}
- **Typical companions:** {TRAVEL_COMPANIONS} (solo / partner / family)
- **Reasons:** {TRIP_REASONS} (work / vacation / family)

## Hard avoids

- {AVOID_1}
- {AVOID_2}

## Booking workflow

(How you actually book — relevant if mastermind helps with this.)

- {BOOKING_TOOL_OF_CHOICE} (e.g. "Google Flights search → book direct on airline site")
- {PAYMENT_METHOD_FOR_TRAVEL} (e.g. "Chase Sapphire Reserve")
- {LOYALTY_NUMBER_STORAGE} (e.g. "saved in 1Password 'Travel Loyalty' folder")
