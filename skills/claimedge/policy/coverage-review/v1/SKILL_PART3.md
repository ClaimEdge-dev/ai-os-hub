### Function 2 Output: Declarations Page Extracted Data

```json
{
  "declarations_extraction": {
    "extraction_id": "CE-DEC-{YYYY}-{NNNN}",
    "extraction_date": "2025-07-16",
    "status": "complete",
    "confidence": "high",
    "validation_issues": [],

    "named_insureds": {
      "primary": "Sarah and David Thompson",
      "additional": []
    },

    "addresses": {
      "mailing": "1847 Mill Creek Drive, Naperville, IL 60540",
      "property": "1847 Mill Creek Drive, Naperville, IL 60540"
    },

    "policy_period": {
      "effective_date": "2025-01-15",
      "expiration_date": "2026-01-15",
      "in_force_at_loss": true
    },

    "coverage_table": [
      {
        "coverage_code": "A",
        "coverage_name": "Dwelling",
        "limit": 425000.00,
        "deductible": 2500.00
      },
      {
        "coverage_code": "B",
        "coverage_name": "Other Structures",
        "limit": 42500.00,
        "deductible": 2500.00
      },
      {
        "coverage_code": "C",
        "coverage_name": "Personal Property",
        "limit": 212500.00,
        "deductible": 2500.00
      },
      {
        "coverage_code": "D",
        "coverage_name": "Loss of Use",
        "limit": null,
        "deductible": 0.00,
        "notes": "No stated dollar limit — actual loss sustained basis"
      },
      {
        "coverage_code": "E",
        "coverage_name": "Personal Liability",
        "limit": 300000.00,
        "deductible": 0.00
      },
      {
        "coverage_code": "F",
        "coverage_name": "Medical Payments",
        "limit": 5000.00,
        "deductible": 0.00
      }
    ],

    "deductibles": {
      "all_peril": {
        "amount": 2500.00,
        "type": "flat"
      },
      "wind_hail": null,
      "named_storm": null,
      "hurricane": null
    },

    "endorsements": [
      { "form_number": "OL 01 01", "description": "Limited Coverage — Ordinance or Law" },
      { "form_number": "HO 04 73", "description": "Actual Cash Value — Personal Property" },
      { "form_number": "HO 32 31", "description": "Water Back-Up and Sump Discharge or Overflow" },
      { "form_number": "HO 04 20", "description": "Additional Coverage — miscellaneous" },
      { "form_number": "HO 04 54", "description": "Extended Replacement Cost — Dwelling" }
    ],

    "mortgagee": {
      "name": "Chase Bank",
      "loan_number": "XXXXXXXX4567",
      "address": "Chase Bank, PO Box 182065, Columbus, OH 43218"
    },

    "premium": {
      "annual_premium": 2850.00,
      "payment_plan": "escrow"
    },

    "prior_carrier": {
      "carrier": "Allstate",
      "expiration_date": "2025-01-15"
    },

    "extraction_notes": [
      "All Coverage limits confirmed against policy form language",
      "Policy in force on date of loss (June 28, 2025)",
      "No special deductibles (wind/hail/named storm) apply to this loss",
      "Five endorsements identified — recommend reviewing each for claim impact"
    ]
  }
}
```

---

### Function 3 Output: Coverage Gap Analysis

```json
{
  "coverage_gap_analysis": {
    "analysis_id": "CE-CGA-{YYYY}-{NNNN}",
    "analysis_date": "2025-07-16",
    "client_id": "CE-CLI-0156",
    "claim_number": "SF-2025-789456",

    "coverage_vs_damage_comparison": {
      "coverage_a_dwelling": {
        "coverage_limit": 425000.00,
        "extended_replacement_cost": 106250.00,
        "total_available": 531250.00,
        "estimated_damage": 187500.00,
        "gap_amount": 0.00,
        "gap_status": "adequate",
        "percentage_of_damage_covered": 100.0,
        "notes": "Damage well within limits including Extended Replacement Cost buffer"
      },
      "coverage_b_other_structures": {
        "coverage_limit": 42500.00,
        "estimated_damage": 28500.00,
        "gap_amount": 0.00,
        "gap_status": "adequate",
        "percentage_of_damage_covered": 100.0
      },
      "coverage_c_personal_property": {
        "coverage_limit": 212500.00,
        "estimated_damage": 67500.00,
        "gap_amount": 0.00,
        "gap_status": "adequate",
        "percentage_of_damage_covered": 100.0,
        "notes": "ACV settlement will reduce recovery — recommend depreciated value analysis"
      },
      "coverage_d_loss_of_use": {
        "coverage_limit": null,
        "ale_monthly_estimate": 4500.00,
        "ale_duration_months": 4.5,
        "estimated_ale_total": 20250.00,
        "gap_amount": 0.00,
        "gap_status": "adequate_unlimited",
        "notes": "Coverage D has no dollar limit — actual loss sustained basis"
      }
    },

    "coinsurance_analysis": {
      "coinsurance_percentage_required": 80.0,
      "coverage_a_limit": 425000.00,
      "minimum_required_coverage": 340000.00,
      "estimated_replacement_cost": 485000.00,
      "coverage_as_percentage_of_rcv": 87.6,
      "coinsurance_penalty_risk": false,
      "replacement_cost_80_percent": 388000.00,
      "notes": "Coverage A at $425,000 represents 87.6% of estimated RCV — above 80% threshold. No coinsurance penalty anticipated.",
      "warning": "If RCV exceeds $531,250, Coverage A + Extended Replacement Cost may be exhausted. Monitor supplementary dwelling cost estimates."
    },

    "underinsurance_assessment": {
      "is_underinsured": false,
      "coverage_a_shortfall": 0.00,
      "coverage_a_as_percent_of_rcv": 87.6,
      "recommended_coverage_a": 485000.00,
      "underinsurance_percentage": 0.0,
      "action_required": "None — coverage adequate for current loss. Recommend client increase Coverage A to $485,000 at renewal to match full replacement cost."
    },

    "total_damage_summary": {
      "total_estimated_damage": 303750.00,
      "total_coverage_available": 786250.00,
      "net_after_deductible": 301250.00,
      "applicable_deductible": 2500.00,
      "coverage_shortfall": 0.00,
      "overall_status": "adequate"
    },

    "missing_endorsements": [
      {
        "endorsement": "Replacement Cost — Personal Property (HO 04 90)",
        "impact": "Client will receive ACV only on personal property — estimated depreciation penalty: $18,000–$25,000",
        "recommendation": "Cannot add retroactively. Argue reasonable expectations if carrier represented 'full replacement' during sale."
      }
    ],

    "coverage_increase_arguments": [
      "Extended Replacement Cost endorsement provides 25% buffer above Coverage A — ensure carrier applies before exhausting base limit",
      "If repair costs exceed $531,250, argue under 215 ILCS 5/154.6 that carrier must provide clear explanation of limit exhaustion and options",
      "Recommend client increase Coverage A to $485,000 at renewal; document this recommendation for E&O protection"
    ],

    "flagged_issues": [
      {
        "severity": "warning",
        "issue": "ACV on personal property will reduce recovery by estimated $18,000–$25,000",
        "recommendation": "Build reasonable expectations argument; document any carrier representations about 'full replacement' coverage"
      }
    ]
  }
}
```

---

### Function 4 Output: Ordinance & Law Coverage Assessment

```json
{
  "ol_assessment": {
    "assessment_id": "CE-OLA-{YYYY}-{NNNN}",
    "assessment_date": "2025-07-16",
    "client_id": "CE-CLI-0156",
    "claim_number": "SF-2025-789456",

    "ol_coverage_summary": {
      "limit_a_undamaged_portion": 14167.00,
      "limit_b_demolition_debris": 14167.00,
      "limit_c_increased_cost": 14166.00,
      "total_ol_coverage": 42500.00,
      "percentage_of_coverage_a": 10.0,
      "endorsement_form": "OL 01 01"
    },

    "code_upgrade_analysis": {
      "property_age": 20,
      "construction_type": "frame",
      "applicable_codes": ["IRC 2021", "IECC 2021", "IBC 2021"],
      "jurisdiction": "Naperville, IL (DuPage County)",

      "triggered_code_upgrades": [
        {
          "building_component": "Roof",
          "triggering_code": "IRC 2021 R905.1.1 — Underlayment requirements",
          "description": "Self-adhering polymer modified bitumen underlayment required in entirety, not just valleys/eaves",
          "estimated_cost": 4200.00,
          "ol_limit_triggered": "C",
          "notes": "Pre-2005 roof likely had only #15 felt underlayment"
        },
        {
          "building_component": "Roof",
          "triggering_code": "IRC 2021 R905.2.8.2 — Drip edge requirements",
          "description": "Drip edge at eaves and gables with 1/4 inch extension minimum",
          "estimated_cost": 1800.00,
          "ol_limit_triggered": "C"
        },
        {
          "building_component": "Roof",
          "triggering_code": "IRC 2021 R806.2 — Roof ventilation (1:150 ratio)",
          "description": "Continuous ridge and soffit ventilation may be required if not existing",
          "estimated_cost": 3500.00,
          "ol_limit_triggered": "C"
        },
        {
          "building_component": "Siding",
          "triggering_code": "IRC 2021 R703.11 — Water-resistive barrier",
          "description": "House wrap or equivalent water-resistive barrier behind all siding",
          "estimated_cost": 5800.00,
          "ol_limit_triggered": "C"
        },
        {
          "building_component": "Siding",
          "triggering_code": "IRC 2021 R703.11.2.1 — Flashing at penetrations",
          "description": "Self-adhered flashing tape at all windows, doors, and penetrations",
          "estimated_cost": 2400.00,
          "ol_limit_triggered": "C"
        },
        {
          "building_component": "Insulation",
          "triggering_code": "IECC 2021 R402.1.1 — Wall insulation R-value",
          "description": "Wall insulation must meet R-13 minimum (cavity) or R-20 (continuous); existing may be R-11",
          "estimated_cost": 6500.00,
          "ol_limit_triggered": "C"
        },
        {
          "building_component": "Insulation",
          "triggering_code": "IECC 2021 R402.1.2 — Ceiling insulation R-value",
          "description": "Ceiling insulation R-49 minimum; existing may be R-30 or less",
          "estimated_cost": 4800.00,
          "ol_limit_triggered": "C"
        },
        {
          "building_component": "Electrical",
          "triggering_code": "IRC 2021 E3901.2 — GFCI protection",
          "description": "GFCI protection required for all exterior outlets; may require AFCI upgrade on affected circuits",
          "estimated_cost": 1200.00,
          "ol_limit_triggered": "C"
        },
        {
          "building_component": "Demolition/Debris",
          "triggering_code": "IRC 2021 Chapter 33 — Demolition safety requirements",
          "description": "Permitted demolition with debris removal to approved facility; disposal restrictions on asphalt shingles",
          "estimated_cost": 3800.00,
          "ol_limit_triggered": "B"
        },
        {
          "building_component": "Windows",
          "triggering_code": "IECC 2021 R402.3.1 — Window U-factor",
          "description": "Replacement windows must meet U-0.30 maximum; existing may exceed this",
          "estimated_cost": 2800.00,
          "ol_limit_triggered": "C"
        }
      ]
    },

    "ol_shortfall_calculation": {
      "total_estimated_code_upgrades": 36800.00,
      "limit_c_available": 14166.00,
      "limit_b_available": 14167.00,
      "total_ol_available": 42500.00,
      "total_ol_needed": 36800.00,
      "shortfall_amount": 0.00,
      "shortfall_status": "adequate",
      "limit_c_shortfall": 22634.00,
      "limit_b_shortfall": 0.00,
      "notes": "O&L coverage appears adequate IF carrier accepts all code upgrade triggers. Risk: carrier may dispute which upgrades are 'required by ordinance or law' vs. merely 'desirable'.",
      "recommendation": "Document each code requirement with municipal building department written confirmation. Obtain permit requirements in writing before repairs begin."
    },

    "legal_arguments": [
      {
        "argument": "215 ILCS 5/154.6 requires carrier to provide 'a reasonable explanation for the denial or offer of a compromise settlement'",
        "application": "If carrier disputes any code upgrade as not 'required by ordinance or law,' demand written explanation citing specific policy language and code provisions",
        "strength": "strong"
      },
      {
        "argument": "PA 103-0510 (2024) strengthens policyholder protections for code upgrade coverage",
        "application": "Cite PA 103-0510 reforms requiring carriers to clearly explain O&L coverage at policy inception and renewal",
        "strength": "moderate"
      },
      {
        "argument": "Contra proferentem — ambiguous O&L language construed against drafter (carrier)",
        "application": "If 'required by ordinance or law' is ambiguous as to whether it means 'mandatory by code official' or 'required to obtain permit,' argue for broader interpretation favoring insured",
        "strength": "moderate"
      }
    ],

    "recommendations": [
      "Obtain written confirmation from Naperville Building Department of all applicable code requirements for 20-year-old dwelling",
      "Photograph all pre-code conditions before demolition to prove code upgrade necessity",
      "Request carrier adjuster meet with building official to confirm code triggers",
      "If carrier disputes O&L applicability, cite 215 ILCS 5/154.6 and demand written coverage position",
      "Consider appraisal if O&L dispute exceeds $10,000"
    ]
  }
}
```

---
