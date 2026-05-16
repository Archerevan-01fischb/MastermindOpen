---
name: personal-financial-profile
description: ⭐ Retirement/financial planning template. Highest-value vignette — mastermind helps run Monte Carlo, SWR, Social Security claim scenarios.
metadata:
  type: personal
---

# Financial Profile

## Household identity

- **Primary:** {PRIMARY_NAME}, age {PRIMARY_AGE}, born {PRIMARY_DOB_YEAR}
- **Partner (if applicable):** {PARTNER_NAME}, age {PARTNER_AGE}, born {PARTNER_DOB_YEAR}
- **State of residence:** {STATE} (drives state tax + Medicaid + 529 rules)
- **Dependents:** {DEPENDENTS}

## Income — current

- **Primary salary:** {PRIMARY_SALARY}/yr (after-tax: {PRIMARY_AFTER_TAX})
- **Partner salary:** {PARTNER_SALARY}/yr
- **Side income:** {SIDE_INCOME_SOURCES_AND_AMOUNTS}
- **Bonus / RSU:** {BONUS_RSU} (vesting cadence)

## Liquid assets

- **Schwab brokerage:** ${SCHWAB_BALANCE} (advisor: {ADVISOR_NAME}, fee {ADVISOR_FEE})
- **Cash / HYSA:** ${CASH_BALANCE} at {BANK_NAME}, APY {APY}%
- **401(k) / 403(b):** ${RETIREMENT_PRIMARY} ({TRADITIONAL_OR_ROTH}, employer match {MATCH}%)
- **IRA:** ${IRA_BALANCE} ({TYPE})
- **Brokerage 2 / other:** {OTHER_INVEST_ACCOUNTS}

## Real estate

- **Primary home:** ${HOME_VALUE} value, ${MORTGAGE_BALANCE} mortgage at {MORTGAGE_RATE}%, ${MONTHLY_PI} PI/month
- **Rental property:** {RENTAL_DETAILS}

## Liabilities

- **Mortgage:** ${MORTGAGE_BALANCE}
- **Auto loans:** {AUTO_LOANS}
- **Credit cards:** {CARDS_AND_BALANCES}
- **Other:** {OTHER_LIABILITIES}

## Expected windfall / lumpy income

- {WINDFALL_1} (e.g. "DNA payout YYYY-MM, est. ${AMOUNT}")
- {WINDFALL_2}

## Net worth snapshot

| Category | Value |
|---|---|
| Liquid invest | ${LIQUID} |
| Retirement | ${RETIREMENT} |
| Real estate equity | ${RE_EQUITY} |
| Other | ${OTHER} |
| **Total** | **${NET_WORTH}** |

Last updated: {SNAPSHOT_DATE}

## Retirement planning

- **Target retirement age:** {RETIRE_AGE_PRIMARY} (primary), {RETIRE_AGE_PARTNER} (partner)
- **SWR assumed:** {SWR_PCT}% (typically 3.5-4%)
- **Target annual spend in retirement:** ${TARGET_RETIREMENT_SPEND}/yr
- **Social Security claim ages:** {SS_CLAIM_AGES} (e.g. "primary at 70, partner at 67")
- **Monte Carlo last run:** {MONTE_CARLO_DATE} → {MONTE_CARLO_RESULT} (e.g. "94% success at $200K/yr spend")

## Tax posture

- **Filing status:** {FILING_STATUS}
- **Estimated bracket:** {TAX_BRACKET}
- **Accountant:** {ACCOUNTANT_NAME} at {ACCOUNTANT_FIRM}
- **Quarterly estimated tax:** {QUARTERLY_EST} (if applicable)

## Insurance

- **Term life:** {TERM_LIFE_AMOUNT}, {TERM_END_DATE}
- **Disability:** {DISABILITY_DETAILS}
- **Umbrella:** {UMBRELLA_AMOUNT}
- **LTC:** {LTC_STATUS}

## How mastermind helps here

- Run Monte Carlo / SWR simulations on demand (Python notebook or local model)
- Track quarterly estimated tax filings + reminders
- Surface tax-loss-harvesting candidates at year end
- Run "what if I retire at 60 vs 65 vs 67" scenarios
- Watch for IRMAA cliffs when discussing Roth conversions

**Decision-making rule:** mastermind is the spreadsheet engine, not the advisor. {ADVISOR_NAME} is the human advisor. Don't make moves based on mastermind's projection without running it past the advisor.
