### Ordinance & Law — Estimated Code Upgrades Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `undamaged_portion_value` | Decimal | No | Value of undamaged portion that must be brought to code |
| `demolition_cost` | Decimal | No | Cost to demolish damaged portions |
| `debris_removal_cost` | Decimal | No | Cost to remove debris |
| `increased_cost_construction` | Decimal | No | Additional cost to build to current code vs. repair to pre-loss condition |
| `specific_upgrades` | Array[Object] | No | List of specific code upgrades with costs and triggering code sections |

---

### Function 5: Coverage Argument Builder

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `disputed_issue` | Enum | Yes | Type of coverage dispute: `exclusion_applied`, `coverage_denied`, `limit_dispute`, `deductible_dispute`, `settlement_method_dispute`, `ol_dispute`, `ale_dispute`, `other` |
| `carrier_position` | String | Yes | The insurance carrier's stated position on the coverage issue |
| `policy_language` | String | Yes | The exact policy language at issue (the exclusion, limitation, or condition) |
| `broader_policy_language` | String | No | Surrounding policy context and related provisions |
| `facts_of_loss` | String | Yes | Detailed description of the loss event and damages |
| `client_expectations` | String | No | What the client reasonably understood their coverage to be |
| `carrier_representations` | String | No | Any statements, advertisements, or agent representations made by or on behalf of the carrier |
| `claim_history` | Array[Object] | No | Timeline of carrier communications and actions on this claim |
| `applicable_statutes` | Array[String] | No | Specific statutes believed to apply (defaults to standard IL insurance code provisions) |
| `jurisdiction` | String | Yes | Court jurisdiction (typically county where property is located) |
| `argument_types_requested` | Array[Enum] | No | Specific argument types to build: `contra_proferentem`, `reasonable_expectations`, `estoppel`, `waiver`, `unfair_claims_practices`, `bad_faith`, `pa_103_0510`, `case_law` (default: all) |

---

### Function 6: Coverage Opinion Memo Generator

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `client_id` | String | Yes | ClaimEdge client ID |
| `claim_number` | String | Yes | Insurance claim number |
| `policy_review_results` | Object | Yes | Complete output from Function 1 (Policy Document Review) |
| `dec_page_results` | Object | Yes | Complete output from Function 2 (Declarations Page Extractor) |
| `gap_analysis_results` | Object | Yes | Complete output from Function 3 (Coverage Gap Analysis) |
| `ol_assessment_results` | Object | No | Complete output from Function 4 (O&L Assessment) — if O&L is implicated |
| `coverage_arguments` | Array[Object] | No | Complete outputs from Function 5 (Coverage Argument Builder) — if disputes exist |
| `memo_template` | Enum | No | `comprehensive`, `abbreviated`, `dispute_focused`, `ol_focused` (default: `comprehensive`) |
| `memo_date` | Date | Yes | Date of the memo |
| `author` | String | Yes | Name and title of the memo author (Robert Krapil or designate) |
| `distribution_list` | Array[String] | No | Recipients of the memo (client, attorney, internal) |
| `confidentiality_notice` | Boolean | No | Whether to include attorney work product / confidentiality notice (default: true) |
| `include_executive_summary` | Boolean | No | Whether to include executive summary (default: true) |
| `include_recommendations` | Boolean | No | Whether to include recommendations section (default: true) |

---

## Output Schema

### Function 1 Output: Policy Document Review Results

```json
{
  "policy_review": {
    "review_id": "CE-PRV-{YYYY}-{NNNN}",
    "review_date": "2025-07-16",
    "client_id": "CE-CLI-0156",
    "claim_number": "SF-2025-789456",
    "policy_type": "ho3",
    "carrier": "State Farm",
    "policy_number": "12-AB-3456-7",
    "form_edition": "ISO HO 00 03 10/00",
    "state_of_issue": "IL",
    "review_status": "complete",

    "coverage_analysis": {
      "coverage_a_dwelling": {
        "present": true,
        "limit": 425000.00,
        "description": "Coverage A — Dwelling",
        "loss_settlement": "Replacement Cost Value (RCV)",
        "special_conditions": [
          "RCV holdback released upon repair/replacement within 180 days of initial payment",
          "Dwelling under construction endorsement applies — limits may increase during construction",
          "Fungi, Wet or Dry Rot, or Bacteria limitation: $10,000 sub-limit per occurrence"
        ],
        "notable_provisions": [
          "Glass or safety glazing material covered for peril of hail",
          "Ordinance or Law exclusion applies unless Limited Coverage endorsement purchased"
        ]
      },
      "coverage_b_other_structures": {
        "present": true,
        "limit": 42500.00,
        "percentage_of_a": 10.0,
        "description": "Coverage B — Other Structures",
        "loss_settlement": "Replacement Cost Value (RCV)",
        "special_conditions": [
          "Does not cover structures used for business purposes",
          "Does not cover structures rented to non-tenant persons"
        ],
        "notable_provisions": []
      },
      "coverage_c_personal_property": {
        "present": true,
        "limit": 212500.00,
        "percentage_of_a": 50.0,
        "description": "Coverage C — Personal Property",
        "loss_settlement": "Actual Cash Value (ACV) — replacement cost available if endorsed",
        "special_conditions": [
          "Special limits apply: $200 money; $1,500 securities; $1,500 watercraft; $2,500 firearms; $2,500 silverware; $1,500 electronic apparatus in vehicles",
          "Off-premises coverage limited to 10% of Coverage C limit ($21,250)"
        ],
        "notable_provisions": [
          "Property in storage facility covered worldwide"
        ]
      },
      "coverage_d_loss_of_use": {
        "present": true,
        "limit": null,
        "description": "Coverage D — Loss of Use",
        "loss_settlement": "Actual additional expenses incurred — no stated dollar limit",
        "special_conditions": [
          "ALE payable for reasonable period to repair/rebuild dwelling",
          "Fair Rental Value coverage if portion of residence rented",
          "Civil Authority provision: 2 weeks coverage if access prohibited"
        ],
        "notable_provisions": []
      },
      "coverage_e_personal_liability": {
        "present": true,
        "limit": 300000.00,
        "description": "Coverage E — Personal Liability",
        "applicable_to_loss": false,
        "notes": "Not implicated in this property damage claim"
      },
      "coverage_f_medical_payments": {
        "present": true,
        "limit": 5000.00,
        "description": "Coverage F — Medical Payments to Others",
        "applicable_to_loss": false,
        "notes": "Not implicated in this property damage claim"
      }
    },

    "exclusion_analysis": {
      "applicable_exclusions": [
        {
          "exclusion_name": "Ordinance or Law",
          "policy_language": "We do not cover loss caused directly or indirectly by enforcement of any ordinance or law regulating the construction, repair, or demolition of a building or other structure.",
          "form_reference": "ISO HO 00 03 10/00 — Section I — Exclusions A.7.",
          "applies_to_loss": true,
          "mitigating_endorsement": "Limited Coverage — Ordinance or Law (OL 01 01)",
          "mitigating_endorsement_present": true,
          "rebuttal_arguments": [
            "O&L endorsement provides coverage; exclusion analysis shifts to whether damage triggers O&L limits",
            "Under 215 ILCS 5/154.6, carrier must provide clear explanation of O&L coverage limitations"
          ]
        },
        {
          "exclusion_name": "Flood, Surface Water, Water Backs Up",
          "policy_language": "We do not cover loss caused directly or indirectly by flood, surface water, waves, tidal water, overflow of a body of water, or spray from any of these, whether or not driven by wind. We do not cover loss caused by water or sewage that backs up through sewers or drains.",
          "form_reference": "ISO HO 00 03 10/00 — Section I — Exclusions A.2.c.",
          "applies_to_loss": false,
          "mitigating_endorsement": null,
          "mitigating_endorsement_present": false,
          "rebuttal_arguments": []
        },
        {
          "exclusion_name": "Neglect",
          "policy_language": "We do not cover loss caused by neglect of an insured to use all reasonable means to save and preserve property at and after the time of loss.",
          "form_reference": "ISO HO 00 03 10/00 — Section I — Exclusions A.5.",
          "applies_to_loss": false,
          "mitigating_endorsement": null,
          "mitigating_endorsement_present": false,
          "rebuttal_arguments": [],
          "notes": "Flag: if carrier raises neglect, document all post-loss protective measures taken by insured"
        }
      ],
      "exclusions_flagged_for_review": [
        {
          "exclusion_name": "Gradual Deterioration / Wear and Tear",
          "policy_language": "We do not cover loss caused by wear and tear, marring, deterioration, inherent vice, latent defect, or mechanical breakdown.",
          "concern": "Carrier may attempt to attribute hail damage to 'wear and tear' — rebuttal: hail is a sudden, direct physical loss; cumulative weathering does not negate concurrent hail damage",
          "rebuttal_ready": true
        }
      ]
    },

    "endorsement_analysis": {
      "endorsements_found": [
        {
          "form_number": "OL 01 01",
          "form_name": "Limited Coverage — Ordinance or Law",
          "description": "Provides 10% of Coverage A for Ordinance & Law expenses",
          "effect": "Adds $42,500 O&L coverage — CRITICAL for code upgrade arguments",
          "relevant_to_claim": true
        },
        {
          "form_number": "HO 04 77",
          "form_name": "Equipment Breakdown",
          "description": "Covers sudden mechanical/electrical breakdown of equipment",
          "effect": "May cover HVAC compressor failure if caused by power surge from storm",
          "relevant_to_claim": true
        }
      ],
      "endorsements_missing_but_recommended": [
        {
          "form_number": "HO 05 28",
          "form_name": "Additional Limits — Ordinance or Law",
          "description": "Increases O&L coverage beyond 10% of Coverage A",
          "recommendation": "Client should consider purchasing for future — current 10% may be inadequate for full code compliance"
        }
      ]
    },

    "deductible_analysis": {
      "standard_deductible": {
        "amount": 2500.00,
        "type": "flat",
        "applies_to": "All perils except named storm/hurricane"
      },
      "named_storm_deductible": {
        "amount": null,
        "type": null,
        "applies_to": "Not applicable — no named storm deductible on this policy"
      },
      "wind_hail_deductible": {
        "amount": null,
        "type": null,
        "applies_to": "Not applicable — no separate wind/hail deductible"
      },
      "special_deductibles": [],
      "notes": "Single $2,500 flat deductible applies to hail loss"
    },

    "loss_settlement_analysis": {
      "coverage_a_method": "RCV",
      "coverage_a_holdback": "Yes — holdback released upon completion within 180 days",
      "coverage_b_method": "RCV",
      "coverage_c_method": "ACV",
      "coverage_c_rcv_option": "Available via endorsement HO 04 90 — NOT currently endorsed",
      "recommendation": "Pursue ACV-to-RCV argument for contents under Illinois reasonable expectations doctrine"
    },

    "overall_risk_assessment": {
      "coverage_adequacy": "marginal",
      "underinsurance_risk": "moderate",
      "key_concerns": [
        "Coverage A limit ($425,000) may be below full replacement cost for Naperville market",
        "O&L coverage at 10% ($42,500) may be insufficient for full IRC 2021 compliance",
        "Coverage C settled at ACV — significant recovery gap for contents",
        "No Water Backup endorsement — if interior water damage from sump pump failure, no coverage"
      ],
      "recommendations": [
        "Order full replacement cost appraisal from independent estimator",
        "Calculate O&L shortfall against IRC 2021 upgrade requirements",
        "Document all contents at pre-loss condition for ACV fight",
        "Investigate interior water damage source — if roof leak, covered; if sump backup, potentially excluded"
      ]
    }
  }
}
```

### Function 2 Output: Declarations Page Extracted Data

```json
{
  "declarations": {
    "extraction_id": "CE-DEC-{YYYY}-{NNNN}",
    "extraction_date": "2025-07-16",
    "extraction_confidence": 0.94,
    "validation_status": "passed_with_notes",

    "named_insured": {
      "primary": "John and Mary Smith",
      "additional": ["John Smith Jr. (son, age 17)"]
    },

    "addresses": {
      "mailing_address": "1234 Oak Lane, Naperville, IL 60540",
      "property_address": "1234 Oak Lane, Naperville, IL 60540",
      "match": true
    },

    "policy_period": {
      "effective_date": "2024-09-01",
      "expiration_date": "2025-09-01",
      "status": "active",
      "days_remaining": 47
    },

    "coverage_limits": {
      "coverage_a_dwelling": 425000.00,
      "coverage_b_other_structures": 42500.00,
      "coverage_c_personal_property": 212500.00,
      "coverage_d_loss_of_use": null,
      "coverage_e_personal_liability": 300000.00,
      "coverage_f_medical_payments": 5000.00
    },

    "deductibles": {
      "standard": {
        "amount": 2500.00,
        "type": "flat"
      },
      "special": []
    },

    "endorsements": [
      {
        "form_number": "OL 01 01",
        "description": "Limited Coverage — Ordinance or Law",
        "effective_date": "2024-09-01"
      },
      {
        "form_number": "HO 04 77",
        "description": "Equipment Breakdown",
        "effective_date": "2024-09-01"
      },
      {
        "form_number": "PP 03 01",
        "description": "Scheduled Personal Property",
        "effective_date": "2024-09-01"
      }
    ],

    "mortgagee": {
      "name": "Chase Bank, N.A.",
      "loan_number": "4567891234",
      "address": "P.O. Box 1820, Wilmington, DE 19899"
    },

    "premium": {
      "annual_premium": 2850.00,
      "payment_plan": "monthly",
      "fees": 75.00
    },

    "prior_carrier": {
      "name": "Allstate Insurance Company",
      "expiration_date": "2024-09-01"
    },

    "validation_notes": [
      "Coverage A limit ($425,000) should be cross-checked against current Marshall & Swift/local builder estimates for Naperville",
      "Policy expires in 47 days — flag for Robert to monitor renewal and ensure no coverage changes",
      "No Water Backup endorsement — interior water damage from drainage systems may be excluded",
      "No Flood endorsement — if any flood-related damage, no coverage"
    ]
  }
}
```