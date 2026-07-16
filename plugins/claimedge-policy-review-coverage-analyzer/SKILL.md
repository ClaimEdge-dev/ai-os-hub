---
name: claimedge-policy-review-coverage-analyzer
description: >
  Insurance policy coverage analysis and review system for ClaimEdge LLC. Analyzes
  homeowners, commercial property, and dwelling policies to identify coverage limits,
  exclusions, endorsements, and gaps. Triggers on any request involving: policy review,
  coverage analysis, insurance policy reading, coverage verification, declarations page
  analysis, endorsement review, coverage gap identification, policy interpretation, or
  Illinois insurance law (215 ILCS 5/155, 5/154.6). Use when a new claim requires policy
  review after intake/fee agreement, when coverage disputes arise, when preparing
  supplement demands that require policy citations, or when the user uploads a policy
  document for analysis. Integrates with claim intake (Pillar 1) and feeds into
  inspection planning (Pillar 3) and supplement support (Pillar 6).
---

# ClaimEdge Policy & Coverage Review Analyzer

## Purpose

Analyze insurance policies to extract every coverage element that affects claim outcomes.
Produces a structured Coverage Analysis Report used throughout the claim lifecycle.

## When This Skill Activates

- New client signs fee agreement → policy review is next step in Golden Path
- User uploads a policy document (PDF, image, or text)
- Coverage dispute with carrier requires policy citation
- Supplement preparation needs coverage limit verification
- Endorsement changes mid-claim require re-analysis
- Bad faith allegation requires policy language documentation

## Core Workflow: 5-Phase Analysis

Execute all 5 phases for every policy review. Document findings in the Coverage Analysis Report.

### Phase 1: Document Intake & Organization

Collect and organize all policy documents:

1. **Declarations Page** (Dec Page) — primary source for limits/deductibles
2. **Coverage Form** (DP-1, DP-2, DP-3, HO-2, HO-3, HO-5, CP, etc.)
3. **Endorsements & Riders** — schedule numerically (e.g., HO 04 20, CP 01 34)
4. **Previous Policy Periods** — for prior damage exclusions
5. **Renewal Notices** — for mid-claim coverage changes

**Read:** `references/policy-analysis-framework.md` — Phase 1 detailed procedures

### Phase 2: Declarations Page Analysis

Extract and tabulate every financial element:

| Element | What to Record | Critical For |
|---------|---------------|--------------|
| Coverage A — Dwelling | Limit, % of replacement cost | Total recoverable |
| Coverage B — Other Structures | Limit (typically 10% of A) | Detached garage, shed |
| Coverage C — Personal Property | Limit (typically 50-70% of A) | Contents claims |
| Coverage D — Loss of Use / ALE | Limit and time limit | Living expenses |
| Coverage E — Liability | Per occurrence / aggregate | Third-party claims |
| Coverage F — Medical Payments | Per person limit | Guest injuries |
| Deductible | Amount, type (flat/%/split) | Client out-of-pocket |
| Ordinance or Law | Limit (typically 10-25% of A) | Code upgrade arguments |
| Special Limits | Jewelry, guns, cash, etc. | Sub-limits on categories |
| Mortgagee / Loss Payee | Name and address | Check distribution |

**Output:** Completed Declarations Summary table

**Read:** `references/coverage-types-library.md` — all coverage types with IL considerations

### Phase 3: Coverage Form Analysis

Analyze the base policy form for perils, exclusions, and conditions:

**Named Peril vs. Open Peril (All-Risk):**
- HO-3 / DP-3: Open peril on dwelling, named peril on contents
- HO-5: Open peril on both dwelling and contents
- DP-1: Named peril (fire, lightning, wind, hail only) — most restrictive
- HO-2 / DP-2: Named peril broad form

**For Each Covered Peril, Document:**
1. Peril definition in policy language
2. Any sub-limits or special deductibles (e.g., wind/hail deductible)
3. Exclusions that apply to that peril
4. Conditions precedent (duties after loss)

**Read:** `references/policy-analysis-framework.md` — Phase 3 peril-by-peril checklist

### Phase 4: Endorsement & Rider Review

Every endorsement gets a row in the Endorsement Tracking table:

| Endorsement # | Title | Effect on Coverage | Added/Modified/Excluded | Impact on Current Claim |
|--------------|-------|-------------------|------------------------|------------------------|
| HO 04 20 | Loss Assessment | Adds $X for HOA assessments | Added | Relevant if HOA shared loss |
| HO 04 54 | Ordinance or Law | Increases O&L to 25% of Cov A | Modified | Critical for code upgrades |

**Priority Endorsements to Flag:**
- Ordinance or Law (increased limits)
- Water Backup / Sump Overflow
- Foundation / Water Damage
- Mold / Fungus coverage
- Service Line Coverage
- Equipment Breakdown
- Scheduled Personal Property
- Home Business endorsement

**Read:** `references/coverage-types-library.md` — endorsement section

### Phase 5: Coverage Gap Identification & Summary

Synthesize all findings into actionable gaps:

**Gap Categories:**
1. **Underinsurance** — Coverage A < estimated replacement cost
2. **Missing Endorsements** — Gaps that could have been covered
3. **Excluded Perils** — Loss types not covered (flood, earth movement)
4. **Sublimits** — Category limits below actual loss (jewelry, cash)
5. **Deductible Issues** — Multiple deductibles, percentage-based surprises
6. **Condition Failures** — Client actions that may void coverage

**Read:** `references/exclusion-database.md` — common exclusions with counter-arguments

## Coverage Analysis Report Template

Every policy review produces this report:

```
CLAIMEDGE COVERAGE ANALYSIS REPORT
Client: [Name] | Policy #: [Number] | Carrier: [Name]
Date of Loss: [Date] | Date of Review: [Date] | Analyst: [Name]

EXECUTIVE SUMMARY
[3-4 sentences: policy form type, key limits, major gaps, overall assessment]

DECLARATIONS SUMMARY
[Table from Phase 2]

COVERAGE FORM ANALYSIS
[Peril-by-peril findings from Phase 3]

ENDORSEMENT TRACKING
[Table from Phase 4]

COVERAGE GAPS
[Table from Phase 5 with severity: HIGH / MEDIUM / LOW]

ILLINOIS LAW CONSIDERATIONS
[Relevant 215 ILCS sections, case law, regulatory guidance]

RECOMMENDATIONS
[Specific next steps for claim strategy]

CONFIDENCE LEVEL: [HIGH / MEDIUM / LOW]
[Basis for confidence assessment]
```

## Illinois Legal Framework

Key statutes governing policy interpretation in Illinois:

- **215 ILCS 5/155** — Bad faith; unreasonable delay/denial penalties
- **215 ILCS 5/154.6** — Claim handling standards; 15-day acknowledgment, 45-day decision
- **PA 103-0510** — Matching requirements; cosmetic damage amendments
- **Contra Proferentem** — Ambiguities construed against drafter (carrier)
- **Reasonable Expectations Doctrine** — Coverage based on insured's reasonable expectations

**Read:** `references/illinois-statutes.md` — full IL legal framework with case citations

## Reference Files

| File | When to Read | Content |
|------|-------------|---------|
| `references/policy-analysis-framework.md` | Every activation | 5-phase detailed procedures, checklists, document templates |
| `references/coverage-types-library.md` | Phase 2 & 4 | 14 coverage types, endorsement library, IL-specific considerations |
| `references/exclusion-database.md` | Phase 3 & 5 | Common exclusions with counter-arguments and IL case law |
| `references/illinois-statutes.md` | All phases | IL legal framework, regulatory guidance, case law index |

## Integration Points

**Upstream (triggers this skill):**
- `claimedge__intake-triage__client-intake` — completed intake, fee agreement signed

**Downstream (skills this feeds):**
- `claimedge__inspections__photo-documentation` — coverage informs inspection scope
- `claimedge__estimate-support__supplement-builder` — coverage limits inform supplement demands
- `claimedge__carrier-comms__supplement-letter-writer` — policy citations in demand letters
- `claimedge__jurisdiction__bad-faith-tracker` — coverage gaps may indicate bad faith

## Critical Rules

1. **Never assume policy language** — read actual document, not standard forms
2. **Always check endorsements** — base form is rarely the whole story
3. **Flag percentage deductibles immediately** — 2-5% of Coverage A can be massive
4. **Document everything in writing** — carrier will dispute your interpretation
5. **Cite Illinois law for every coverage argument** — 215 ILCS 5/155 is your hammer
6. **Mark confidence level** — LOW confidence means you need carrier clarification
7. **Date-stamp the analysis** — policies change, endorsements get added
8. **Check for mortgagee clauses** — they have rights that affect the claim

## Document Control

| Field | Value |
|---|---|
| Skill Name | claimedge-policy-review-coverage-analyzer |
| Pillar | 2 — Policy & Coverage Review |
| Version | 1.0 |
| Status | Production |
| IL Law Citations | 50+ |
| Author | ClaimEdge LLC |
| Review Date | July 2026 |
