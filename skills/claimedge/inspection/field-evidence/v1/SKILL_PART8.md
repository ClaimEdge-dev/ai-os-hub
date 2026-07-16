### Function 6: Field Report Generator

**Output:** Complete Field Inspection Report JSON (Part A — Sections 1-5)

```json
{
  "report_id": "CE-RPT-{{CLAIM_NUMBER}}-{{YYYYMMDD}}",
  "claim_number": "{{CLAIM_NUMBER}}",
  "report_metadata": {
    "generation_timestamp": "{{ISO8601_TIMESTAMP}}",
    "report_type": "{{initial_inspection|supplement|re_inspection|appraisal}}",
    "template_used": "{{template_a_residential_hail|template_b_commercial_wind|template_c_residential_water|custom}}",
    "addressee": "{{policyholder|carrier|appraisal_panel|legal_counsel|mediator}}",
    "confidentiality_level": "{{work_product|attorney_client|privileged|public}}",
    "turnaround_hours": {{HOURS}},
    "generated_by": "ClaimEdge LLC Inspection & Field Evidence System v1.0"
  },
  "section_1_executive_summary": {
    "property_address": "{{FULL_ADDRESS}}",
    "date_of_loss": "{{YYYY-MM-DD}}",
    "peril_type": "{{hail|wind|hurricane|flood|fire|water|tornado|ice_snow}}",
    "carrier": "{{CARRIER_NAME}}",
    "policyholder": "{{CLIENT_NAME}}",
    "inspection_date": "{{YYYY-MM-DD}}",
    "inspector": "{{INSPECTOR_NAME}}",
    "inspector_license": "{{LICENSE_NUMBER}}",
    "inspector_haag_cert": "{{HAAG_CERT_OR_null}}",
    "key_findings": [
      "{{FINDING_1}}",
      "{{FINDING_2}}",
      "{{FINDING_3}}"
    ],
    "overall_damage_classification": "{{C|M|MO|MA|S}}",
    "scope_recommendation": "{{repair|partial_replacement|full_replacement}}",
    "estimated_squares": {{SQUARES}},
    "code_upgrades_identified": {{COUNT}},
    "health_safety_concerns": {{COUNT}},
    "photo_count": {{COUNT}}
  },
  "section_2_property_information": {
    "property_profile": {
      "address": "{{STREET}}",
      "city": "{{CITY}}",
      "state": "{{STATE}}",
      "zip": "{{ZIP}}",
      "county": "{{COUNTY}}",
      "jurisdiction": "{{MUNICIPALITY}}"
    },
    "building_characteristics": {
      "property_type": "{{TYPE}}",
      "year_built": {{YEAR}},
      "stories": {{COUNT}},
      "square_footage": {{SF}},
      "foundation": "{{TYPE}}"
    },
    "construction_details": {
      "roof_covering": "{{MATERIAL}}",
      "roof_age_years": {{AGE}},
      "siding_material": "{{MATERIAL}}",
      "framing_type": "{{platform|balloon|post_and_beam|steel|concrete}}",
      "foundation_type": "{{basement|crawl|slab|pier}}"
    },
    "policy_information": {
      "carrier": "{{CARRIER}}",
      "policy_number": "{{POLICY_NUMBER}}",
      "claim_number": "{{CLAIM_NUMBER}}",
      "date_of_loss": "{{YYYY-MM-DD}}",
      "policyholder_name": "{{NAME}}",
      "policy_period": "{{START}} to {{END}}"
    }
  },
  "section_3_inspection_methodology": {
    "inspection_date": "{{YYYY-MM-DD}}",
    "inspection_duration_hours": {{DURATION}},
    "weather_conditions": "{{DESCRIPTION}}",
    "inspector_name": "{{NAME}}",
    "inspector_license": "{{LICENSE}}",
    "inspector_company": "ClaimEdge LLC",
    "inspection_methods": ["{{ground_inspection}}", "{{ladder_access}}", "{{drone_survey}}"],
    "equipment_used": ["{{equipment_1}}", "{{equipment_2}}"],
    "safety_equipment": ["{{safety_1}}", "{{safety_2}}"],
    "access_challenges": "{{DESCRIPTION_OR_none}}",
    "areas_not_accessible": ["{{AREA_OR_empty}}"],
    "chain_of_custody": "All photographic evidence was captured using a GPS-enabled camera, timestamped, and uploaded to secure cloud storage within 4 hours of inspection. Images are stored in accordance with ClaimEdge LLC evidence handling procedures.",
    "scope_limitations": "{{LIMITATIONS_OR_none}}",
    "methodology_statement": "This inspection was conducted in accordance with Haag Engineering damage assessment protocols, IRC 2021, IBC 2021, and IECC 2021. All damage was classified using the Haag classification system. Moisture readings were taken with a calibrated Protimeter Surveymaster. Thermal imaging was performed with a FLIR C5.",
    "industry_standards": [
      "Haag Engineering — Residential Wind Damage",
      "Haag Engineering — Hail Damage Assessment",
      "IRC 2021 — Roof Assemblies (Chapter 9)",
      "IRC 2021 — Exterior Walls (R703)",
      "IECC 2021 — Energy Conservation"
    ]
  },
  "section_4_roof_findings": {
    "roof_system_description": "{{NARRATIVE_DESCRIPTION_OF_ROOF_SYSTEM}}",
    "number_of_slopes": {{COUNT}},
    "total_squares": {{SQUARES}},
    "slopes": [
      {
        "slope_id": "{{SLOPE_NAME}}",
        "designation": "{{Front|Rear|Left|Right}}",
        "dimensions": "{{L}} ft x {{W}} ft ({{SQUARES}} squares)",
        "pitch": "{{PITCH}}",
        "orientation": "{{DIRECTION}}",
        "condition_pre_loss": "{{excellent|good|fair|poor}}",
        "damage_assessment": {
          "haag_classification": "{{C|M|MO|MA|S}}",
          "classification_description": "{{Cosmetic|Minor|Moderate|Major|Severe}} — {{EXPLANATION}}",
          "test_square_results": {
            "test_square_dimensions": "10 ft x 10 ft",
            "hail_hits_count": {{COUNT}},
            "bruising_count": {{COUNT}},
            "fracturing_count": {{COUNT}},
            "granule_loss_pct": {{PERCENT}},
            "punctures_count": {{COUNT}},
            "indentations_count": {{COUNT}}
          },
          "wind_damage": {
            "uplift_count": {{COUNT}},
            "creasing_count": {{COUNT}},
            "tearing_count": {{COUNT}},
            "missing_pieces_count": {{COUNT}}
          }
        },
        "photo_references": ["CE-PH-###", "CE-PH-###", "CE-PH-###"],
        "recommended_action": "{{repair|replace}}",
        "justification": "{{CODE_REFERENCE|MANUFACTURER_SPEC|FUNCTIONAL_DAMAGE|COSMETIC}}"
      }
    ],
    "roof_summary": {
      "slopes_with_damage": {{COUNT}},
      "slopes_requiring_replacement": {{COUNT}},
      "slopes_requiring_repair": {{COUNT}},
      "total_damage_classification": "{{C|M|MO|MA|S}}",
      "functional_damage_present": {{true|false}},
      "water_intrusion_risk": "{{low|medium|high|critical}}"
    },
    "roof_accessories": {
      "skylights": { "count": {{COUNT}}, "damaged": {{COUNT}}, "action": "{{repair|replace}}" },
      "chimneys": { "count": {{COUNT}}, "damaged": {{COUNT}}, "action": "{{repair|replace}}" },
      "vents": { "ridge_vent_ft": {{LF}}, "box_vent_count": {{COUNT}}, "damaged": {{COUNT}} },
      "flashings": { "condition": "{{good|fair|poor}}", "replacement_needed": {{true|false}} }
    }
  },
  "section_5_exterior_findings": {
    "siding_assessment": {
      "primary_material": "{{MATERIAL}}",
      "number_of_elevations": {{COUNT}},
      "elevations": [
        {
          "elevation": "{{FRONT|REAR|LEFT|RIGHT}}",
          "square_footage": {{SF}},
          "damage_present": {{true|false}},
          "hail_damage_description": "{{DESCRIPTION_OR_none}}",
          "wind_damage_description": "{{DESCRIPTION_OR_none}}",
          "photo_references": ["CE-PH-###"],
          "recommended_action": "{{repair|replace}}"
        }
      ],
      "code_upgrade_triggers": [
        {
          "code_reference": "IRC R703.2",
          "requirement": "Weather-resistant barrier behind new siding",
          "applicable": {{true|false}}
        }
      ]
    },
    "gutter_assessment": {
      "type": "{{TYPE}}",
      "linear_feet": {{LF}},
      "damage_description": "{{DESCRIPTION}}",
      "recommended_action": "{{repair|replace}}"
    },
    "window_door_assessment": {
      "window_count": {{COUNT}},
      "damaged_windows": [
        {
          "location": "{{ROOM_OR_ELEVATION}}",
          "damage_type": "{{TYPE}}",
          "description": "{{DESCRIPTION}}",
          "photo_reference": "CE-PH-###"
        }
      ]
    },
    "fence_assessment": {
      "type": "{{TYPE}}",
      "linear_feet": {{LF}},
      "damage_present": {{true|false}},
      "damage_description": "{{DESCRIPTION}}",
      "photo_references": ["CE-PH-###"]
    },
    "hvac_assessment": {
      "condenser_units": [
        {
          "location": "{{LOCATION}}",
          "make_model": "{{MAKE}} {{MODEL}}",
          "fins_damaged_pct": {{PERCENT}},
          "photo_reference": "CE-PH-###",
          "action": "{{repair|replace}}"
        }
      ]
    }
  }
}
```
