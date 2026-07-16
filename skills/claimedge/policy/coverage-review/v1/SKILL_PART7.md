### Template 2: Coverage Gap Report

```markdown
# CLAIMEDGE COVERAGE GAP REPORT

**Prepared for:** {{client_name}}
**ClaimEdge Client ID:** {{client_id}}
**Claim Number:** {{claim_number}}
**Carrier:** {{carrier_name}}
**Policy Number:** {{policy_number}}
**Report Date:** {{report_date}}
**Prepared by:** Robert Krapil, ClaimEdge LLC

---

## EXECUTIVE SUMMARY

Your {{policy_type}} policy with {{carrier_name}} has a **{{gap_assessment}}** coverage position for this loss.

| Metric | Amount |
|--------|--------|
| Total Coverage Available | ${{total_coverage}} |
| Total Estimated Damages | ${{total_damages}} |
| **Coverage Gap** | **${{total_gap}}** |
| Gap Percentage | {{gap_pct}}% |

**Key Finding:** {{key_finding}}

---

## COVERAGE A — DWELLING ANALYSIS

| Item | Amount |
|------|--------|
| Coverage Limit | ${{coverage_a_limit}} |
| Estimated Structural Damage | ${{damage_a}} |
| Estimated Replacement Cost | ${{replacement_cost}} |
| Coinsurance Required ({{coinsurance_pct}}%) | ${{coinsurance_required}} |
| **Gap** | **${{gap_a}}** |
| Coinsurance Penalty Risk | {{coinsurance_risk}} |

**Assessment:** {{coverage_a_assessment}}

{{#coinsurance_warning}}
### ⚠️ COINSURANCE WARNING

Your Coverage A limit is {{coinsurance_actual_pct}}% of the estimated replacement cost — below the {{coinsurance_pct}}% coinsurance requirement in your policy. If your carrier invokes coinsurance, your claim payment could be reduced by approximately ${{coinsurance_penalty}}.

**Why this matters:** Insurance carriers sometimes use coinsurance penalties to reduce claim payments when the insured has not maintained adequate coverage limits. However, Illinois law (215 ILCS 5/154.6) requires carriers to provide clear guidance on adequate coverage limits at renewal. If your carrier failed to recommend adequate limits, the coinsurance penalty may be unenforceable.
{{/coinsurance_warning}}

---

## COVERAGE B — OTHER STRUCTURES ANALYSIS

| Component | Damage Estimate |
|-----------|----------------|
| {{b_component_1}} | ${{b_damage_1}} |
| {{b_component_2}} | ${{b_damage_2}} |
| {{b_component_3}} | ${{b_damage_3}} |
| **Total** | **${{damage_b}}** |
| Coverage Limit | ${{coverage_b_limit}} |
| **Gap** | **${{gap_b}}** |

---

## COVERAGE C — PERSONAL PROPERTY ANALYSIS

| Item | Amount |
|------|--------|
| Coverage Limit | ${{coverage_c_limit}} |
| Estimated Contents Damage | ${{damage_c}} |
| Loss Settlement Method | {{c_settlement}} |
| Estimated RCV Recovery Gap | ${{rcv_gap_c}} |

{{#acv_warning}}
### ⚠️ ACV SETTLEMENT WARNING

Your policy settles Coverage C claims at **Actual Cash Value (ACV)**, not Replacement Cost Value (RCV). This means depreciation will be deducted from your contents settlement — potentially reducing your recovery by ${{rcv_gap_c}}.

**What we can do:** Under Illinois law, if your carrier or agent represented that you had "full coverage" or "replacement cost coverage," we may be able to argue for RCV treatment under the reasonable expectations doctrine.
{{/acv_warning}}

---

## COVERAGE D — LOSS OF USE (ALE)

| Item | Amount |
|------|--------|
| Coverage Type | {{d_type}} |
| Estimated Monthly ALE | ${{ale_monthly}} |
| Estimated Duration | {{ale_months}} months |
| Total Estimated ALE | ${{damage_d}} |

---

## ORDINANCE & LAW COVERAGE

| Limit | Amount | Code Upgrade Need | Status |
|-------|--------|-------------------|--------|
| A — Undamaged Portion | ${{ol_a_limit}} | ${{ol_a_need}} | {{ol_a_status}} |
| B — Demolition/Debris | ${{ol_b_limit}} | ${{ol_b_need}} | {{ol_b_status}} |
| C — Increased Cost | ${{ol_c_limit}} | ${{ol_c_need}} | {{ol_c_status}} |

---

## RECOMMENDED ACTIONS

{{#recommendations}}
{{priority}}. **{{action}}** — {{timeline}}
   {{description}}
{{/recommendations}}

---

## LEGAL BASIS

This analysis is based on:
- Your {{carrier_name}} {{policy_type}} policy ({{policy_number}})
- Illinois Insurance Code (215 ILCS 5/154.6, 5/155)
- Public Act 103-0510 (2024 pro-policyholder reforms)
- ClaimEdge's independent damage assessment

---

*This report is confidential and prepared for the exclusive use of the named client.*
*ClaimEdge LLC — Coverage Gap Report v1.0*
```

### Template 3: Coverage Opinion Memo (Comprehensive)

```markdown
# CONFIDENTIAL — ATTORNEY WORK PRODUCT PRIVILEGE

# CLAIMEDGE COVERAGE OPINION MEMORANDUM

| | |
|---|---|
| **Memo ID:** | {{memo_id}} |
| **Date:** | {{memo_date}} |
| **To:** | {{client_name}} (ClaimEdge Client {{client_id}}) |
| **From:** | Robert Krapil, ClaimEdge LLC |
| **Re:** | Coverage Opinion — {{carrier_name}} Claim {{claim_number}} |
| **Classification:** | CONFIDENTIAL — ATTORNEY WORK PRODUCT |

---

## I. EXECUTIVE SUMMARY

Based on our comprehensive review of the insurance policy, applicable Illinois law, and the facts of the loss, our opinion is:

**{{executive_conclusion}}**

Key points:
{{#key_points}}
- {{point}}
{{/key_points}}

---

## II. POLICY INFORMATION

| Field | Detail |
|-------|--------|
| Insurance Company | {{carrier_name}} |
| Policy Number | {{policy_number}} |
| Policy Type | {{policy_type}} ({{form_edition}}) |
| Policy Period | {{policy_period}} |
| Named Insured | {{named_insured}} |
| Property Address | {{property_address}} |

---

## III. FACTUAL BACKGROUND

{{factual_background}}

---

## IV. COVERAGE ANALYSIS

### A. Coverage A — Dwelling

**Policy Language:** "We cover dwelling on the 'residence premises' shown in the Declarations against direct physical loss..."

**Analysis:** {{coverage_a_analysis}}

**Conclusion:** {{coverage_a_conclusion}}

### B. Coverage B — Other Structures

**Analysis:** {{coverage_b_analysis}}

**Conclusion:** {{coverage_b_conclusion}}

### C. Coverage C — Personal Property

**Analysis:** {{coverage_c_analysis}}

**Conclusion:** {{coverage_c_conclusion}}

### D. Coverage D — Loss of Use

**Analysis:** {{coverage_d_analysis}}

**Conclusion:** {{coverage_d_conclusion}}

---

## V. EXCLUSION ANALYSIS

{{#exclusions}}
### {{exclusion_name}}

**Policy Language:** "{{exclusion_language}}"

**Carrier's Position:** {{carrier_position}}

**Our Analysis:** {{our_analysis}}

**Conclusion:** {{exclusion_conclusion}}

{{/exclusions}}

---

## VI. ORDINANCE & LAW COVERAGE ASSESSMENT

{{ol_assessment}}

---

## VII. COVERAGE GAP ANALYSIS

{{gap_analysis_summary}}

---

## VIII. RECOMMENDATIONS

{{#recommendations}}
{{number}}. **{{title}}**
   
   Timeline: {{timeline}}
   
   {{description}}

{{/recommendations}}

---

## IX. LEGAL AUTHORITY

This opinion is based on the following authorities:

### Statutes:
{{#statutes}}
- {{citation}}
{{/statutes}}

### Case Law:
{{#case_law}}
- {{citation}}
{{/case_law}}

### Building Codes:
{{#building_codes}}
- {{code_reference}}
{{/building_codes}}

---

## X. CONCLUSION

{{conclusion}}

---

**Robert Krapil**
ClaimEdge LLC
Licensed Illinois Public Adjuster
[Signature]

---

*CONFIDENTIALITY NOTICE: This memorandum and all attachments are protected by the attorney work product privilege and the common interest doctrine. This document was prepared in anticipation of litigation and contains legal analysis, strategy, and opinions. Unauthorized disclosure is prohibited.*

*ClaimEdge LLC — Coverage Opinion Memorandum v1.0*
```