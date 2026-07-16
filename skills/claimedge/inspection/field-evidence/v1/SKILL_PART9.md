  "section_6_interior_findings": {
    "inspection_scope": "{{full_interior|water_affected_only|attic_only|specific_rooms}}",
    "moisture_equipment": "{{METER_MODEL}} (S/N: {{SERIAL}}, Cal: {{DATE}})",
    "interior_conditions": "Temperature: {{TEMP}}F, Relative Humidity: {{RH}}%, Dew Point: {{DEW_POINT}}F",
    "rooms_inspected": [
      {
        "room_name": "{{NAME}}",
        "level": "{{basement|first|second|third}}",
        "ceiling_condition": "{{DESCRIPTION}}",
        "wall_condition": "{{DESCRIPTION}}",
        "floor_condition": "{{DESCRIPTION}}",
        "moisture_readings": [
          {
            "location": "{{WALL_OR_CEILING}}",
            "reading_pct": {{PERCENT}},
            "classification": "{{normal|elevated|saturated}}"
          }
        ],
        "thermal_anomalies": [
          {
            "location": "{{AREA}}",
            "type": "{{cold_spot|hot_spot|moisture}}",
            "temperature_delta_f": {{DELTA}}
          }
        ],
        "mold_assessment": {
          "visible_mold": {{true|false}},
          "location": "{{SURFACE}}",
          "extent": "{{spotty|patchy|extensive}}",
          "recommended_testing": "{{air_sample|surface_sample|ERMI|none}}"
        },
        "photo_references": ["CE-PH-###"],
        "recommended_action": "{{dry_out|remove|remediate|monitor}}"
      }
    ],
    "attic_assessment": {
      "accessible": {{true|false}},
      "decking_condition": "{{DESCRIPTION}}",
      "insulation_condition": "{{DESCRIPTION}}",
      "ventilation_assessment": "{{DESCRIPTION}}",
      "mold_observed": {{true|false}},
      "photo_references": ["CE-PH-###"]
    },
    "moisture_summary": {
      "total_readings": {{COUNT}},
      "elevated_readings": {{COUNT}},
      "saturated_readings": {{COUNT}},
      "highest_reading": "{{PERCENT}}% at {{LOCATION}}",
      "water_source_opinion": "{{SOURCE}}",
      "drying_recommendation": "{{RECOMMENDATION}}"
    }
  },
  "section_7_code_compliance": {
    "jurisdiction": "{{MUNICIPALITY}}",
    "adopted_codes": {
      "irc": "{{YEAR}}",
      "ibc": "{{YEAR}}",
      "iecc": "{{YEAR}}"
    },
    "code_upgrades_triggered": [
      {
        "code_reference": "IRC R905.2.1",
        "requirement": "Spaced sheathing must be replaced with solid decking for new roof covering",
        "trigger": "{{CONDITION}}",
        "estimated_cost": ${{AMOUNT}},
        "justification": "{{EXPLANATION}}"
      },
      {
        "code_reference": "IRC R905.1.2",
        "requirement": "Ice barrier membrane required at eaves (extend 24"" inside exterior wall line, or to the end of the last joist, whichever is greater — in Illinois, typically 2 rows)",
        "trigger": "Roof replacement in Climate Zone 5 (Illinois)",
        "estimated_cost": ${{AMOUNT}},
        "justification": "Illinois is in Climate Zone 5 per IRC Figure R301.1. Two rows of ice barrier are standard for this region to prevent ice dam water intrusion."
      },
      {
        "code_reference": "IRC R905.2.8.5",
        "requirement": "Drip edge required at eaves and rakes",
        "trigger": "Roof replacement",
        "estimated_cost": ${{AMOUNT}},
        "justification": "IRC 2021 mandates drip edge for all asphalt shingle installations to prevent water infiltration at roof edges."
      },
      {
        "code_reference": "IRC R703.2",
        "requirement": "Weather-resistant exterior wall envelope (housewrap) required behind new siding",
        "trigger": "{{CONDITION}}",
        "estimated_cost": ${{AMOUNT}},
        "justification": "{{EXPLANATION}}"
      },
      {
        "code_reference": "IECC R402",
        "requirement": "Insulation R-value compliance if wall/ceiling opened",
        "trigger": "Interior remediation requires removal of drywall or ceiling",
        "estimated_cost": ${{AMOUNT}},
        "justification": "IECC 2021 requires upgraded insulation when building envelope is opened for repair."
      }
    ],
    "ordinance_law_coverage_note": "The above code upgrade items may be covered under the Ordinance or Law endorsement of the subject policy. Coverage for code-required upgrades is typically provided at 10%, 25%, or 50% of the Coverage A limit. Policyholders should verify their specific endorsement limits with their carrier."
  },
  "section_8_recommended_scope": {
    "scope_summary": "Based on the findings documented in this report, the following scope of repairs is recommended:",
    "roof_scope": {
      "action": "{{repair|partial_replace|full_replace}}",
      "squares": {{SQUARES}},
      "slopes_affected": ["{{SLOPE_1}}", "{{SLOPE_2}}"],
      "material_specification": "{{SHINGLE_TYPE_AND_GRADE}}",
      "code_upgrades_included": ["{{UPGRADE_1}}", "{{UPGRADE_2}}"],
      "accessories": {
        "drip_edge": {{true|false}},
        "ice_barrier": {{true|false}},
        "synthetic_underlayment": {{true|false}},
        "ridge_vent": {{true|false}},
        "skylights_replace": {{COUNT}}
      }
    },
    "siding_scope": {
      "action": "{{repair|partial_replace|full_replace}}",
      "square_footage": {{SF}},
      "elevations_affected": ["{{ELEV_1}}", "{{ELEV_2}}"],
      "code_upgrades_included": ["{{UPGRADE_1}}"]
    },
    "gutter_scope": {
      "action": "{{repair|replace}}",
      "linear_feet": {{LF}}
    },
    "window_scope": {
      "units_to_replace": {{COUNT}},
      "units_to_repair": {{COUNT}}
    },
    "interior_scope": {
      "action": "{{dry_out|remove|remediate}}",
      "affected_rooms": ["{{ROOM_1}}", "{{ROOM_2}}"],
      "mitigation_duration_days": {{DAYS}},
      "mold_remediation_needed": {{true|false}}
    },
    "attic_scope": {
      "decking_repair_sf": {{SF}},
      "insulation_replace_sf": {{SF}},
      "ventilation_upgrades": "{{DESCRIPTION}}"
    },
    "additional_items": [
      {
        "item": "{{ITEM_NAME}}",
        "justification": "{{REASON}}",
        "estimated_cost": ${{AMOUNT}}
      }
    ]
  },
  "section_9_photo_index": {
    "total_photos": {{COUNT}},
    "photo_table": [
      {
        "photo_id": "CE-PH-###",
        "description": "{{DESCRIPTION}}",
        "system": "{{roof|siding|interior|attic|drone}}",
        "slope_or_elevation": "{{SLOPE_NAME}}",
        "damage_type": "{{TYPE_OR_none}}",
        "scale_reference": {{true|false}}
      }
    ]
  },
  "section_10_inspector_certification": {
    "certification_statement": "I hereby certify that I personally inspected the subject property on the date stated above. This report contains my true and accurate findings based on my professional inspection. I have no financial interest in the outcome of this claim. My compensation is not contingent upon the amount of loss or scope of repairs determined.",
    "inspector_name": "{{INSPECTOR_NAME}}",
    "inspector_title": "Senior Field Inspector",
    "company": "ClaimEdge LLC",
    "license_number": "{{IL_LICENSE_NUMBER}}",
    "haag_certification": "{{HAAG_CERT_NUMBER}}",
    "signature_date": "{{YYYY-MM-DD}}",
    "digital_signature": "{{SIGNATURE_HASH}}",
    "contact_information": {
      "phone": "{{PHONE}}",
      "email": "{{EMAIL}}",
      "company_address": "ClaimEdge LLC, Chicagoland, IL"
    }
  },
  "confidentiality_notice": "THIS REPORT IS CONFIDENTIAL AND PROPRIETARY. This document contains work product prepared in anticipation of litigation or for claims resolution purposes. Unauthorized disclosure, distribution, or reproduction is strictly prohibited. All photographic evidence is the property of ClaimEdge LLC and is subject to chain of custody protocols. For inquiries regarding this report, contact ClaimEdge LLC directly.",
  "statutory_compliance": {
    "215_ilcs_5_154_6": "This inspection was conducted in compliance with Illinois Insurance Code Section 154.6, which requires carriers to effectuate prompt, fair, and equitable settlement of claims. The findings herein are provided to support the policyholder's claim for property damage.",
    "215_ilcs_5_155": "Pursuant to Illinois Insurance Code Section 155, if the carrier unreasonably delays or denies the claim supported by this report, the policyholder may be entitled to attorney fees, costs, and prejudgment interest.",
    "duty_to_cooperate": "The policyholder has fulfilled their duty to cooperate under the insurance policy by allowing this inspection and providing reasonable access to the property."
  },
  "chain_of_custody": {
    "evidence_collected_by": "{{INSPECTOR_NAME}}",
    "collection_date": "{{YYYY-MM-DD}}",
    "evidence_type": "Digital photographs, moisture readings, thermal images",
    "storage_method": "Secure cloud storage with access logging",
    "retention_period": "7 years per Illinois record retention requirements"
  }
}
```
