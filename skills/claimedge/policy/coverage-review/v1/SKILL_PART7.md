### Template 3: Coverage Opinion Memo (Full)

```
{{claimedge_letterhead}}

                                    COVERAGE OPINION MEMO

To:         {{client_primary_name}}
From:       Robert Krapil, Licensed Public Adjuster
Date:       {{memo_date}}
Re:         Coverage Opinion — {{claim_number}}
            Policy: {{policy_number}} ({{carrier_name}})
            Property: {{property_address}}
            Date of Loss: {{date_of_loss}}
            Type of Loss: {{type_of_loss}}

Ref:        ClaimEdge File No. {{client_id}}

---

CONFIDENTIALITY NOTICE

{{#if confidentiality_notice}}
This Coverage Opinion Memorandum is prepared for the benefit of {{client_primary_name}} and their designated representatives. This document may constitute attorney work product if transmitted to or prepared at the direction of legal counsel. It is not intended for disclosure to the insurance carrier or any third party without the express written consent of the insured and ClaimEdge LLC.
{{/if}}

---

1. EXECUTIVE SUMMARY

{{executive_summary}}

2. POLICY INFORMATION

   A. Policy Identification

      Insurance Carrier:        {{carrier_name}}
      Policy Number:            {{policy_number}}
      Policy Type:              {{policy_type}} (Form: {{form_edition}})
      Policy Period:            {{policy_period_start}} through {{policy_period_end}}
      Named Insured(s):         {{named_insured_primary}}
      Property Address:         {{property_address}}
      State of Issue:           {{state_of_issue}}

   B. Coverage Summary

      Coverage A — Dwelling:           ${{coverage_a_limit}} ({{coverage_a_settlement}})
      Coverage B — Other Structures:   ${{coverage_b_limit}} ({{coverage_b_settlement}})
      Coverage C — Personal Property:  ${{coverage_c_limit}} ({{coverage_c_settlement}})
      Coverage D — Loss of Use:        {{coverage_d_limit}} ({{coverage_d_settlement}})
      Coverage E — Personal Liability: ${{coverage_e_limit}}
      Coverage F — Medical Payments:   ${{coverage_f_limit}}

   C. Deductibles

      Standard Deductible:     ${{deductible_amount}} ({{deductible_type}})
      Applicable to This Loss: ${{applicable_deductible}}

   D. Key Endorsements

{{#each endorsements}}
      {{form_number}}: {{description}}
{{/each}}

   E. Mortgagee/Loss Payee

      {{mortgagee_name}}
      Loan No.: {{mortgagee_loan_number}}

3. FACTUAL BACKGROUND

   A. Date of Loss: {{date_of_loss}}

   B. Cause of Loss: {{type_of_loss}}

   C. Description of Loss Event:

      {{loss_description}}

   D. Property Description:

      {{property_description}}

   E. Damage Observed:

      {{damage_description}}

   F. Current Claim Status: {{claim_status}}

4. COVERAGE ANALYSIS

   A. Coverage A — Dwelling / Building

      The policy provides Coverage A — Dwelling with a limit of ${{coverage_a_limit}}, subject to {{coverage_a_settlement}} loss settlement.

      {{coverage_a_analysis}}

      {{#if extended_rc_available}}
      Extended Replacement Cost: The policy includes an Extended Replacement Cost endorsement providing {{extended_rc_percentage}}% above the Coverage A limit, for a total available coverage of ${{extended_rc_total}}.
      {{/if}}

      Conclusion: {{coverage_a_conclusion}}

   B. Coverage B — Other Structures

      The policy provides Coverage B — Other Structures with a limit of ${{coverage_b_limit}}, subject to {{coverage_b_settlement}} loss settlement.

      {{coverage_b_analysis}}

      Conclusion: {{coverage_b_conclusion}}

   C. Coverage C — Personal Property

      The policy provides Coverage C — Personal Property with a limit of ${{coverage_c_limit}}, subject to {{coverage_c_settlement}} loss settlement.

      {{coverage_c_analysis}}

      {{#if coverage_c_acv}}
      Important Note: Coverage C is settled on an Actual Cash Value basis. This means the carrier will apply depreciation to personal property claims, reducing the recovery by the estimated useful life of each item. The insured must keep detailed records of all damaged personal property, including age, condition, and replacement cost, to challenge unreasonable depreciation.
      {{/if}}

      Conclusion: {{coverage_c_conclusion}}

   D. Coverage D — Loss of Use / Additional Living Expenses

      The policy provides Coverage D — Loss of Use {{#if coverage_d_limit}}with a limit of ${{coverage_d_limit}}{{else}}on an actual loss sustained basis with no stated dollar limit{{/if}}.

      {{coverage_d_analysis}}

      Conclusion: {{coverage_d_conclusion}}

5. EXCLUSION ANALYSIS

{{#each applicable_exclusions}}
   {{index}}. {{exclusion_name}}

      Policy Language: "{{policy_language}}"
      Form Reference: {{form_reference}}

      Analysis: {{analysis}}

      {{#if rebuttal_arguments}}
      Rebuttal Arguments:
{{#each rebuttal_arguments}}
      - {{this}}
{{/each}}
      {{/if}}

      Conclusion: {{conclusion}}

{{/each}}

6. ORDINANCE & LAW COVERAGE ASSESSMENT

   {{#if ol_assessment_included}}
   A. O&L Coverage Available

      Limit A — Undamaged Portion:    ${{ol_limit_a}}
      Limit B — Demolition/Debris:    ${{ol_limit_b}}
      Limit C — Increased Cost:       ${{ol_limit_c}}
      Total O&L Coverage:             ${{ol_total}}

   B. Applicable Building Codes

      The property is located in {{jurisdiction}}, which has adopted the following building codes:
{{#each applicable_codes}}
      - {{this}}
{{/each}}

   C. Triggered Code Upgrades

{{#each triggered_upgrades}}
      {{index}}. {{building_component}}
         Triggering Code: {{triggering_code}}
         Description: {{description}}
         Estimated Cost: ${{estimated_cost}}
         O&L Limit: {{ol_limit_triggered}}
{{/each}}

   D. O&L Shortfall Analysis

      Total Estimated Code Upgrades: ${{total_code_upgrades}}
      Total O&L Coverage Available:  ${{ol_total}}
      Shortfall:                     ${{ol_shortfall}}

      {{ol_shortfall_conclusion}}

   E. Legal Arguments for O&L Coverage

{{#each ol_legal_arguments}}
      - {{argument}}
        Application: {{application}}
        Strength: {{strength}}
{{/each}}

   {{else}}
   Ordinance & Law coverage is not implicated in this claim as the damage does not trigger building code upgrade requirements.
   {{/if}}

7. COVERAGE GAP ANALYSIS

   A. Coverage vs. Damage Comparison

      Coverage                Limit          Damage         Status
      -----------------------------------------------------------------
      Coverage A (Dwelling)   ${{coverage_a_limit}}    ${{damage_a}}    {{status_a}}
      Coverage B (Other)      ${{coverage_b_limit}}     ${{damage_b}}     {{status_b}}
      Coverage C (Contents)   ${{coverage_c_limit}}    ${{damage_c}}     {{status_c}}
      Coverage D (ALE)        {{coverage_d_display}}    ${{damage_d}}     {{status_d}}
      -----------------------------------------------------------------
      TOTALS                  ${{total_limit}}    ${{total_damage}}    {{overall_status}}

   B. Coinsurance Analysis

      Estimated Replacement Cost:     ${{estimated_rcv}}
      80% Coinsurance Requirement:    ${{eighty_pct_rcv}}
      Coverage A Limit:               ${{coverage_a_limit}}
      Coverage as % of RCV:           {{coverage_pct_rcv}}%
      Coinsurance Penalty Risk:       {{coinsurance_risk}}

   C. Missing Endorsements

{{#each missing_endorsements}}
      - {{endorsement}}: {{impact}}
{{/each}}

8. RECOMMENDATIONS

{{#each recommendations}}
   {{index}}. {{priority}}: {{recommendation}}
{{/each}}

9. LEGAL AUTHORITY

   The following statutes and cases are cited in this opinion:

   Statutes:
{{#each cited_statutes}}
   - {{this}}
{{/each}}

   Case Law:
{{#each cited_cases}}
   - {{this}}
{{/each}}

   Building Codes:
{{#each cited_codes}}
   - {{this}}
{{/each}}

10. CONCLUSION

{{conclusion}}

This opinion is based on the policy documents and information provided to ClaimEdge LLC as of {{memo_date}}. If additional policy endorsements, amendments, or facts become available, this opinion should be reviewed and may be subject to revision.

---

Respectfully submitted,

_________________________________
Robert Krapil
Licensed Public Adjuster
Illinois License No. {{pa_license_number}}
ClaimEdge LLC

Date: {{memo_date}}

---

DISTRIBUTION:
{{#each distribution_list}}
{{this}}
{{/each}}

FILE: {{client_id}}
```