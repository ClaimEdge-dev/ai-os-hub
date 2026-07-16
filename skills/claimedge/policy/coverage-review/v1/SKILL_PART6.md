### Function 4: Ordinance & Law Coverage Assessment — Workflow

```
Step 1: RECEIVE O&L COVERAGE AND PROPERTY DATA
  -> Accept O&L limits A, B, C from declarations page extraction
  -> Accept property data (age, type, construction, jurisdiction)
  -> Accept estimated code upgrades (if available)
  -> Load jurisdiction-specific code adoptions

Step 2: IDENTIFY TRIGGERING CODE SECTIONS
  -> For each affected building component:
    -> Identify applicable IRC, IBC, or IECC section
    -> Check local amendments for stricter requirements
    -> Document pre-loss vs. post-loss code requirements
  -> Create code upgrade analysis table

Step 3: ESTIMATE CODE UPGRADE COSTS
  -> For each identified upgrade:
    -> Calculate cost to bring to current code
    -> Identify which O&L limit is triggered (A, B, or C)
    -> Check if upgrade cost is within applicable limit
  -> If estimates not available: flag for contractor/estimator input

Step 4: CALCULATE O&L UTILIZATION
  -> Sum all Limit A costs (undamaged portion)
  -> Sum all Limit B costs (demolition/debris)
  -> Sum all Limit C costs (increased construction cost)
  -> Compare each to its respective limit
  -> Calculate total O&L shortfall or excess

Step 5: BUILD LEGAL ARGUMENTS
  -> For each upgrade: cite specific code section
  -> Document local adoption status
  -> Reference 215 ILCS 5/154.6 (clear explanation requirement)
  -> Reference PA 103-0510 (pro-policyholder reforms)
  -> Cite relevant case law for coverage disputes

Step 6: PREPARE RECOMMENDATIONS
  -> If O&L adequate: document with confidence
  -> If O&L shortfall: build argument for full coverage
  -> Recommend building department confirmation letters
  -> Flag any upgrades that may be disputed by carrier

Step 7: OUTPUT
  -> Return O&L Coverage Assessment (JSON)
  -> Include upgrade-by-upgrade analysis
  -> Include legal arguments and recommendations
```

### Function 5: Coverage Argument Builder — Workflow

```
Step 1: RECEIVE DISPUTE INFORMATION
  -> Accept disputed_issue type and carrier_position
  -> Accept exact policy language at issue
  -> Accept facts_of_loss and claim_history
  -> Accept argument_types_requested (default: all)

Step 2: BUILD CONTRA PROFERENTEM ARGUMENT
  -> If requested and applicable:
    -> Identify ambiguity in policy language
    -> Cite Illinois rule: ambiguous language construed against drafter
    -> Reference Cramer v. Insurance Exchange Agency
    -> Draft argument text resolving ambiguity in favor of coverage
  -> If not applicable: skip with note

Step 3: BUILD REASONABLE EXPECTATIONS ARGUMENT
  -> If requested and applicable:
    -> Identify client's objectively reasonable coverage expectations
    -> Cite Illinois reasonable expectations doctrine
    -> Reference Wald v. Crusader Ins. Co.
    -> Draft argument that expectations control over technical language
  -> If not applicable: skip with note

Step 4: BUILD ESTOPPEL ARGUMENT
  -> If requested and applicable:
    -> Identify carrier/agent representations about coverage
    -> Document client's detrimental reliance
    -> Cite promissory estoppel principles
    -> Reference DiBenedetto v. St. Paul Title Ins. Corp.
    -> Draft estoppel argument
  -> If not applicable: skip with note

Step 5: BUILD WAIVER ARGUMENT
  -> If requested and applicable:
    -> Identify carrier actions/inactions that constitute waiver
    -> Cite waiver by conduct principles
    -> Draft waiver argument
  -> If not applicable: skip with note

Step 6: BUILD UNFAIR CLAIMS PRACTICES ARGUMENT
  -> If requested and applicable:
    -> Identify specific 215 ILCS 5/154.6 violations
    -> Map carrier actions to statutory violations (a through j)
    -> Cite DeLuna v. Northwestern Mut. Ins. Co.
    -> Draft unfair claims practices argument
  -> If not applicable: skip with note

Step 7: BUILD BAD FAITH ARGUMENT
  -> If requested and applicable:
    -> Identify pattern of unreasonable carrier conduct
    -> Document timeline of delays and inadequate offers
    -> Cite 215 ILCS 5/155 (attorney fees and penalties)
    -> Draft bad faith argument
  -> If not applicable: skip with note

Step 8: BUILD PA 103-0510 ARGUMENTS
  -> If requested and applicable:
    -> Identify Section 15 violations (plain language summaries)
    -> Identify Section 25 violations (technical denials)
    -> Cite enhanced penalties under revised 215 ILCS 5/155
    -> Draft statutory reform argument
  -> If not applicable: skip with note

Step 9: BUILD CASE LAW ARGUMENTS
  -> If requested:
    -> Research Illinois appellate case law on similar coverage issues
    -> Cite favorable precedents with full citations
    -> Distinguish unfavorable precedents
    -> Draft case law support section
  -> If not applicable: skip with note

Step 10: PRIORITIZE AND SUMMARIZE
  -> Rank all arguments by strength (very_strong / strong / moderate / weak)
  -> Assign priority numbers (1 = highest)
  -> Recommend lead argument and secondary argument
  -> Assess litigation risk
  -> Return Coverage Argument Builder output (JSON)
```

### Function 6: Coverage Opinion Memo Generator — Workflow

```
Step 1: RECEIVE ALL PRIOR ANALYSIS
  -> Accept outputs from Functions 1-5
  -> Validate all required inputs present
  -> Load memo_template selection
  -> Set memo_date and author

Step 2: GENERATE EXECUTIVE SUMMARY
  -> Draft 1-2 paragraph summary of coverage opinion
  -> Include clear conclusion (coverage confirmed/denied/partial)
  -> Highlight key strengths and concerns
  -> Note any immediate actions required

Step 3: DRAFT POLICY INFORMATION SECTION
  -> Format policy details (carrier, number, type, dates)
  -> List named insured and property address
  -> Include form edition if known

Step 4: DRAFT FACTUAL BACKGROUND
  -> Summarize loss event with dates and damages
  -> Include claim number and carrier actions to date
  -> Note ClaimEdge retention date

Step 5: DRAFT COVERAGE ANALYSIS
  -> For each coverage type (A through D):
    -> State whether loss is covered
    -> Reference specific policy language
    -> Note any limitations or conditions
    -> Include dollar impact

Step 6: DRAFT EXCLUSION ANALYSIS
  -> Address each exclusion raised by carrier
  -> State whether exclusion applies
  -> Reference rebuttal arguments from Function 5
  -> Cite case law and statute

Step 7: DRAFT O&L ASSESSMENT (if applicable)
  -> Summarize O&L coverage status
  -> List identified code upgrades
  -> State adequacy conclusion

Step 8: DRAFT GAP ANALYSIS SUMMARY
  -> Summarize underinsurance findings
  -> Note coinsurance exposure
  -> Include dollar gaps by coverage

Step 9: DRAFT RECOMMENDATIONS
  -> List specific, prioritized action items
  -> Include timeline for each action
  -> Note escalation triggers
  -> Flag any attorney consultation needs

Step 10: DRAFT LEGAL AUTHORITY AND CONCLUSION
  -> List all cited statutes and cases
  -> Draft clear conclusion paragraph
  -> Include confidentiality notice

Step 11: FORMAT AND OUTPUT
  -> Apply ClaimEdge memo formatting
  -> Add classification header (Confidential / Attorney Work Product)
  -> Add review_status: "draft_pending_review"
  -> Return Coverage Opinion Memo (JSON)
  -> Flag for Robert's review before delivery
```

---

## Templates

### Template 1: Policy Review Checklist

```markdown
# CLAIMEDGE POLICY REVIEW CHECKLIST

**Client:** {{client_name}} | **ClaimEdge ID:** {{client_id}}
**Carrier:** {{carrier_name}} | **Policy #:** {{policy_number}}
**Claim #:** {{claim_number}} | **Review Date:** {{review_date}}
**Reviewer:** {{reviewer_name}} | **Status:** ☐ Complete ☐ Pending

---

## A. POLICY IDENTIFICATION

| Item | Data | Status |
|------|------|--------|
| Policy Type | {{policy_type}} | ☐ Verified |
| Form Edition | {{form_edition}} | ☐ Verified |
| State of Issue | {{state_of_issue}} | ☐ Verified |
| Policy Period | {{effective_date}} to {{expiration_date}} | ☐ Verified |
| Days to Expiration | {{days_remaining}} | ☐ Verified |

## B. NAMED INSURED VERIFICATION

| Item | Data | Status |
|------|------|--------|
| Primary Named Insured | {{named_insured_primary}} | ☐ Match Intake |
| Additional Insureds | {{named_insured_additional}} | ☐ Verified |
| Property Address | {{property_address}} | ☐ Match Intake |

## C. COVERAGE LIMITS ANALYSIS

| Coverage | Limit | % of A | Loss Settlement | Status |
|----------|-------|--------|-----------------|--------|
| A — Dwelling | ${{coverage_a_limit}} | 100% | {{a_settlement}} | {{a_status}} |
| B — Other Structures | ${{coverage_b_limit}} | {{b_pct}}% | {{b_settlement}} | {{b_status}} |
| C — Personal Property | ${{coverage_c_limit}} | {{c_pct}}% | {{c_settlement}} | {{c_status}} |
| D — Loss of Use | ${{coverage_d_limit}} | N/A | {{d_settlement}} | {{d_status}} |
| E — Liability | ${{coverage_e_limit}} | N/A | N/A | {{e_status}} |
| F — Medical | ${{coverage_f_limit}} | N/A | N/A | {{f_status}} |

**Coinsurance Status:** {{coinsurance_status}} | **Underinsurance Risk:** {{underinsurance_risk}}

## D. DEDUCTIBLES

| Type | Amount | Applies To | Notes |
|------|--------|------------|-------|
| Standard | ${{standard_deductible}} | {{standard_applies}} | {{standard_notes}} |
| Named Storm | ${{storm_deductible}} | {{storm_applies}} | {{storm_notes}} |
| Wind/Hail | ${{wind_deductible}} | {{wind_applies}} | {{wind_notes}} |

## E. EXCLUSIONS ANALYSIS

| Exclusion | Applies? | Mitigating Endorsement | Rebuttal Ready? |
|-----------|----------|----------------------|-----------------|
| Ordinance or Law | {{ol_applies}} | {{ol_endorsement}} | {{ol_rebuttal}} |
| Flood / Water Backup | {{flood_applies}} | {{flood_endorsement}} | {{flood_rebuttal}} |
| Neglect | {{neglect_applies}} | {{neglect_endorsement}} | {{neglect_rebuttal}} |
| Wear and Tear | {{wear_applies}} | {{wear_endorsement}} | {{wear_rebuttal}} |
| Earth Movement | {{earth_applies}} | {{earth_endorsement}} | {{earth_rebuttal}} |

## F. ENDORSEMENTS

| Form # | Name | Relevant? | Financial Impact |
|--------|------|-----------|-----------------|
| {{e1_form}} | {{e1_name}} | {{e1_relevant}} | {{e1_impact}} |
| {{e2_form}} | {{e2_name}} | {{e2_relevant}} | {{e2_impact}} |
| {{e3_form}} | {{e3_name}} | {{e3_relevant}} | {{e3_impact}} |

## G. ORDINANCE & LAW COVERAGE

| Limit | Amount | Estimated Need | Adequate? |
|-------|--------|----------------|-----------|
| A — Undamaged Portion | ${{ol_a}} | ${{ol_a_need}} | {{ol_a_ok}} |
| B — Demolition/Debris | ${{ol_b}} | ${{ol_b_need}} | {{ol_b_ok}} |
| C — Increased Cost | ${{ol_c}} | ${{ol_c_need}} | {{ol_c_ok}} |
| **TOTAL** | **${{ol_total}}** | **${{ol_need_total}}** | **{{ol_ok}}** |

## H. RED FLAGS & ESCALATIONS

{{#red_flags}}
- [ ] **{{severity}}:** {{description}} — Action: {{recommended_action}}
{{/red_flags}}

{{^red_flags}}
- [ ] No red flags identified
{{/red_flags}}

## I. REVIEWER SIGN-OFF

| | |
|---|---|
| Reviewer | Robert Krapil, ClaimEdge LLC |
| Date | {{signoff_date}} |
| Coverage Adequacy | ☐ Adequate ☐ Marginal ☐ Inadequate |
| Escalation Needed | ☐ Yes ☐ No |
| Next Steps | {{next_steps}} |

---
*ClaimEdge LLC — Policy Review Checklist v1.0*
*This document is confidential and privileged.*
```