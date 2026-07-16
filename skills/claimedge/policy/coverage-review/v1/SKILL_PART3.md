### Function 3 Output: Coverage Gap Analysis

```json
{
  "gap_analysis": {
    "analysis_id": "CE-CGA-{YYYY}-{NNNN}",
    "analysis_date": "2025-07-16",
    "client_id": "CE-CLI-0156",
    "claim_number": "SF-2025-789456",

    "summary": {
      "total_coverage_available": 680000.00,
      "total_estimated_damages": 847650.00,
      "total_gap": 167650.00,
      "gap_percentage": 19.8,
      "assessment": "significant_underinsurance",
      "coinsurance_penalty_risk": true
    },

    "coverage_a_analysis": {
      "coverage_limit": 425000.00,
      "estimated_damage": 485000.00,
      "gap": 60000.00,
      "gap_percentage": 12.4,
      "estimated_replacement_cost": 575000.00,
      "coinsurance_requirement": 0.80,
      "coinsurance_required_amount": 460000.00,
      "coinsurance_compliance": "non_compliant",
      "coinsurance_penalty_estimate": 42500.00,
      "notes": "Coverage A is 73.9% of replacement cost — below 80% coinsurance requirement. Estimated penalty: $42,500 if carrier invokes coinsurance."
    },

    "coverage_b_analysis": {
      "coverage_limit": 42500.00,
      "estimated_damage": 67500.00,
      "gap": 25000.00,
      "gap_percentage": 37.0,
      "components": {
        "detached_garage": 28000.00,
        "fence": 8500.00,
        "deck": 22000.00,
        "shed": 9000.00
      },
      "notes": "Coverage B at 10% of A may be insufficient for full other structures replacement in Naperville market"
    },

    "coverage_c_analysis": {
      "coverage_limit": 212500.00,
      "estimated_damage": 145000.00,
      "gap": 0,
      "gap_percentage": 0,
      "assessment": "adequate",
      "loss_settlement": "ACV",
      "rcv_recovery_gap_estimate": 35000.00,
      "notes": "Limit is adequate but ACV settlement creates ~$35,000 recovery gap vs. RCV. Recommend pursuing ACV-to-RCV argument."
    },

    "coverage_d_analysis": {
      "coverage_limit": null,
      "estimated_ale": 45000.00,
      "ale_monthly": 5500.00,
      "estimated_duration_months": 8.2,
      "assessment": "unlimited_adequate",
      "notes": "No dollar limit on Coverage D — full ALE recoverable for reasonable repair period"
    },

    "ordinance_law_analysis": {
      "ol_limit": 42500.00,
      "estimated_code_upgrades": 105000.00,
      "gap": 62500.00,
      "gap_percentage": 59.5,
      "assessment": "severely_inadequate",
      "notes": "O&L coverage at 10% of Coverage A is grossly inadequate for full IRC 2021 compliance. Key shortfalls: roof decking replacement ($28,000), electrical panel upgrade ($8,500), insulation R-value upgrade ($12,000), window egress compliance ($9,500)"
    },

    "overall_assessment": {
      "risk_level": "high",
      "primary_concerns": [
        "Significant underinsurance on Coverage A with coinsurance penalty exposure",
        "Severe O&L inadequacy — 59.5% shortfall for code compliance",
        "Coverage B insufficient for full other structures replacement",
        "ACV settlement on contents creates $35,000 recovery gap"
      ],
      "recommended_actions": [
        "Order independent replacement cost appraisal immediately",
        "Build coinsurance waiver argument under 215 ILCS 5/154.6 — carrier failed to recommend adequate Coverage A limit",
        "Pursue full O&L coverage through argument that damage percentage triggers all three O&L limits",
        "Document all contents at pre-loss condition for ACV-to-RCV fight",
        "Prepare Coverage Gap Report for client education and carrier negotiation"
      ],
      "escalation_needed": true,
      "escalation_reason": "Underinsurance and coinsurance issues require attorney consultation"
    }
  }
}
```

### Function 4 Output: Ordinance & Law Coverage Assessment

```json
{
  "ol_assessment": {
    "assessment_id": "CE-OLA-{YYYY}-{NNNN}",
    "assessment_date": "2025-07-16",
    "client_id": "CE-CLI-0156",
    "claim_number": "SF-2025-789456",

    "ol_coverage_summary": {
      "limit_a_undamaged_portion": 42500.00,
      "limit_b_demolition_debris": 42500.00,
      "limit_c_increased_cost": 42500.00,
      "total_ol_coverage": 127500.00,
      "assessment": "marginally_adequate"
    },

    "code_upgrade_analysis": [
      {
        "upgrade_category": "Roof Decking Replacement",
        "triggering_code": "IRC 2021 R905.2.1 — Roof deck requirements",
        "local_amendment": "Naperville Amendment: All roof decking must be minimum 7/16\" OSB or plywood",
        "estimated_cost": 28000.00,
        "ol_limit_triggered": "C",
        "covered_amount": 28000.00,
        "coverage_status": "full",
        "notes": "Spaced decking must be replaced with solid sheathing per IRC 2021"
      },
      {
        "upgrade_category": "Electrical Panel Upgrade",
        "triggering_code": "IRC 2021 E3401.2 — Service minimum 100A; E3403.3 — AFCI protection",
        "local_amendment": "Naperville requires 200A service for homes >3,000 sq ft",
        "estimated_cost": 8500.00,
        "ol_limit_triggered": "C",
        "covered_amount": 8500.00,
        "coverage_status": "full",
        "notes": "Pre-loss panel was 100A Federal Pacific — must upgrade to 200A with AFCI breakers"
      },
      {
        "upgrade_category": "Insulation R-Value Upgrade",
        "triggering_code": "IECC 2021 R402.1.2 — Ceiling R-49, Wall R-20",
        "local_amendment": "DuPage County requires R-60 ceiling for new construction",
        "estimated_cost": 12000.00,
        "ol_limit_triggered": "C",
        "covered_amount": 12000.00,
        "coverage_status": "full",
        "notes": "Pre-loss insulation was R-30 ceiling, R-11 walls — must upgrade to current code"
      },
      {
        "upgrade_category": "Window Egress Compliance",
        "triggering_code": "IRC 2021 R310.1 — Emergency escape and rescue openings",
        "local_amendment": "Naperville: All basement bedrooms require egress windows",
        "estimated_cost": 9500.00,
        "ol_limit_triggered": "C",
        "covered_amount": 9500.00,
        "coverage_status": "full",
        "notes": "Two basement bedrooms have non-egress windows — must install compliant openings"
      },
      {
        "upgrade_category": "HVAC Duct Sealing & Efficiency",
        "triggering_code": "IECC 2021 R403.3 — Ducts must be sealed and tested",
        "local_amendment": "DuPage County requires duct blaster test for all new HVAC installs",
        "estimated_cost": 4500.00,
        "ol_limit_triggered": "C",
        "covered_amount": 4500.00,
        "coverage_status": "full",
        "notes": "New HVAC install requires sealed ductwork and blower door test"
      },
      {
        "upgrade_category": "Undamaged Siding Replacement",
        "triggering_code": "IBC 2021 3403.1 — repairs must match existing or entire wall must be replaced",
        "local_amendment": "Naperville: Vinyl siding cannot be patched — full wall replacement required",
        "estimated_cost": 18000.00,
        "ol_limit_triggered": "A",
        "covered_amount": 18000.00,
        "coverage_status": "full",
        "notes": "Hail damaged 40% of siding; code requires undamaged 60% be replaced for uniformity"
      }
    ],

    "totals": {
      "total_code_upgrade_cost": 79500.00,
      "total_ol_coverage": 127500.00,
      "ol_shortfall": 0,
      "ol_excess": 48000.00,
      "assessment": "adequate_with_margin",
      "limit_a_used": 18000.00,
      "limit_b_used": 0,
      "limit_c_used": 61500.00
    },

    "legal_arguments": {
      "primary_argument": "All six code upgrades are mandated by currently adopted codes (IRC 2021, IECC 2021, IBC 2021) as interpreted by Naperville and DuPage County. Under 215 ILCS 5/154.6, carrier must provide clear explanation if any upgrade is denied.",
      "secondary_argument": "PA 103-0510 (2024) strengthened policyholder protections — carrier cannot arbitrarily deny code upgrades that are mandated by locally adopted building codes.",
      "case_law_support": [
        "Cramer v. Insurance Exchange Agency, 174 Ill. App. 3d 862 (3d Dist. 1988) — Ambiguous policy language construed against drafter",
        "Wald v. Crusader Ins. Co., 201 Ill. App. 3d 712 (2d Dist. 1990) — Reasonable expectations doctrine applies to coverage disputes"
      ]
    },

    "recommendations": [
      "O&L coverage is adequate for this claim — total upgrades ($79,500) are within total O&L limit ($127,500)",
      "Document each code upgrade with specific IRC/IBC/IECC section citations",
      "Obtain written confirmation from Naperville Building Department that each upgrade is required",
      "Prepare O&L sub-limit tracking spreadsheet for carrier negotiation",
      "If carrier disputes any upgrade, cite 215 ILCS 5/154.6 and PA 103-0510"
    ]
  }
}
```