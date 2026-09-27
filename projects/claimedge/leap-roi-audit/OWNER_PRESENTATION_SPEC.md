# Owner Presentation Specification

## Goal

Present a credible before/after case for operational value, financial protection, claim completeness, and Bobby's contribution.

Do not present modeled savings as cash realized.

## Executive page

Show six top-line metrics:

1. Claims/jobs audited
2. Missing or incomplete fields found
3. Verified fields recovered
4. Hours of manual work avoided
5. Verified financial impact
6. Modeled/estimated opportunity, shown separately

## Core scorecard

### Data completeness
- required fields audited
- missing fields found
- fields recovered
- unresolved fields
- conflict rate
- verification rate
- source-linked field rate

Formula:
`verification_rate = verified_or_source_confirmed_fields / audited_required_fields`

### Time savings
Track per event, not by guesswork after the fact.

`minutes_saved = max(manual_baseline_minutes - actual_minutes, 0)`

Show:
- total hours saved
- average minutes saved per job
- search/retrieval time saved
- data-entry time saved
- follow-up time saved
- rework avoided
- automation coverage

Manual baselines must be evidence-backed when possible:
- timed sample
- historical task duration
- staff estimate identified as ESTIMATED
- repeated observation median

### Financial impact

Keep three buckets:

#### VERIFIED REALIZED
Money demonstrably received, invoiced, recovered, or cost actually avoided.

#### VERIFIED IDENTIFIED
Documented value found or protected but not yet realized.

#### MODELED OPPORTUNITY
Scenario-based value with assumptions clearly displayed.

Do not combine the three in a single unlabeled total.

### Claim completeness / scope recovery

Track:
- carrier baseline RCV
- carrier baseline ACV
- baseline depreciation
- baseline deductible
- baseline net claim
- current documented RCV
- current documented ACV
- current net claim
- approved supplements
- pending supplements
- upgrade/code amounts
- scope items added
- unsupported/duplicate items rejected by QA

`documented_claim_delta = current_documented_rcv - baseline_rcv`

This delta is not automatically profit and not automatically Bobby-attributed value.

### Profitability

When actual company cost/revenue data are available, calculate:

`incremental_gross_profit = incremental_revenue - incremental_direct_cost`

`labor_savings_value = verified_hours_saved * approved_loaded_hourly_cost`

`process_roi = (verified_financial_benefit - process_cost) / process_cost`

Never invent loaded labor rate, close rate, gross margin, commission rate, or overhead. Store assumptions with date/source.

## Bobby contribution

Owner-facing attribution should show:

- data gaps personally identified
- verified facts recovered
- claims audited
- evidence packages created
- estimate/scope corrections found
- supplement support value
- time saved for staff
- rework prevented
- workflows/automations created
- processes standardized
- unresolved risks surfaced before they became expensive

Use an attribution note on every financial event:
- DIRECT
- SHARED
- ENABLED
- NOT-ATTRIBUTED

## Recommended charts

1. Before vs after data completeness
2. Missing fields by section
3. Hours saved by workflow category
4. Verified financial impact by impact type
5. Claim-value baseline vs current documented value
6. Monthly cumulative verified value
7. Bobby-attributed vs shared vs non-attributed impact
8. Rework/errors prevented
9. Open missing-data risk
10. Workflow cycle-time trend

## Owner narrative

The presentation should answer:

- What was missing before?
- What did the new process find?
- How quickly can the same work now be completed?
- What errors or omissions does the process prevent?
- What documented dollars were recovered/protected/accelerated?
- What remains only estimated?
- Which improvements are reusable across every claim?
- What work is Bobby uniquely performing?
- What would it cost the company to recreate this process without him?

The final answer to the last question must be a model with assumptions, not a made-up salary number.
