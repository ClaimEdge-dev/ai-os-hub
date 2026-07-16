### Function 1: Pre-Inspection Planner

**Output:** Pre-Inspection Plan JSON

```json
{
  "plan_id": "CE-PLAN-{{CLAIM_NUMBER}}-{{YYYYMMDD}}",
  "claim_number": "{{CLAIM_NUMBER}}",
  "generation_timestamp": "{{ISO8601_TIMESTAMP}}",
  "property_profile": {
    "address": {
      "street": "{{STREET_ADDRESS}}",
      "city": "{{CITY}}",
      "state": "{{STATE}}",
      "zip": "{{ZIP_CODE}}",
      "county": "{{COUNTY}}",
      "jurisdiction": "{{MUNICIPALITY}}"
    },
    "building_characteristics": {
      "property_type": "{{residential_single_family|residential_multi_family|commercial|industrial|agricultural}}",
      "year_built": {{YEAR_BUILT}},
      "stories_above_grade": {{STORIES}},
      "basement_type": "{{full|partial|crawl|slab|none}}",
      "total_square_footage": {{SQFT}},
      "foundation_type": "{{basement|crawl_space|slab_on_grade|pier_and_beam}}"
    },
    "roof_system": {
      "primary_covering": "{{3_tab_asphalt|architectural_asphalt|wood_shake|wood_shingle|slate|clay_tile|concrete_tile|metal_standing_seam|metal_r_panel|tpo|epdm|pvc|modified_bitumen|built_up|green|solar_tiles|unknown}}",
      "secondary_covering": "{{SAME_OPTIONS_OR_none}}",
      "age_years": {{AGE}},
      "layers": {{LAYER_COUNT}},
      "pitch_description": "{{low_slope|medium|steep|mansard|flat}}",
      "condition_pre_loss": "{{excellent|good|fair|poor|unknown}}",
      "last_replacement_year": {{YEAR_OR_null}}
    },
    "siding_system": {
      "primary_material": "{{vinyl|aluminum|steel|wood|fiber_cement|brick|stone|stucco|efis|composite|asbestos|unknown}}",
      "secondary_material": "{{SAME_OR_none}}",
      "age_years": {{AGE}},
      "condition_pre_loss": "{{excellent|good|fair|poor|unknown}}"
    }
  },
  "peril_assessment": {
    "peril_type": "{{hail|wind|hurricane|flood|fire|water|tornado|ice_snow}}",
    "date_of_loss": "{{YYYY-MM-DD}}",
    "time_of_loss": "{{HH:MM}}",
    "weather_verification": {
      "source": "NOAA Storm Events Database / NWS Local Storm Report",
      "verification_status": "{{confirmed|probable|unverified}}",
      "noaa_event_id": "{{EVENT_ID}}",
      "hail_size_inches": {{SIZE_OR_null}},
      "hail_size_verified": {{true|false}},
      "wind_speed_mph": {{SPEED_OR_null}},
      "wind_speed_verified": {{true|false}},
      "wind_gust_mph": {{GUST_OR_null}},
      "precipitation_type": "{{rain|hail|snow|sleet|none}}",
      "precipitation_amount_inches": {{AMOUNT_OR_null}},
      "nws_warning_type": "{{severe_thunderstorm|tornado|flash_flood|winter_storm|none}}"
    },
    "damage_mechanism": "{{DESCRIPTION_OF_HAIL_IMPACT|WIND_UPLIFT|WATER_INTRUSION|FIRE_SPREAD|ETC}}",
    "expected_damage_patterns": [
      "{{pattern_1}}",
      "{{pattern_2}}"
    ]
  },
  "code_compliance_framework": {
    "adopted_codes": {
      "irc_version": "{{IRC_YEAR}}",
      "ibc_version": "{{IBC_YEAR}}",
      "iecc_version": "{{IECC_YEAR}}",
      "iebc_version": "{{IEBC_YEAR}}"
    },
    "jurisdiction": {
      "authority_having_jurisdiction": "{{MUNICIPALITY_OR_COUNTY}}",
      "building_department_contact": "{{PHONE}}",
      "permit_required_reroof": {{true|false}},
      "permit_required_siding": {{true|false}},
      "permit_required_windows": {{true|false}},
      "permit_required_structural": {{true|false}},
      "permit_fees_estimate": {{AMOUNT_OR_null}}
    },
    "applicable_code_sections": [
      {
        "code_reference": "IRC R905.1",
        "requirement": "Roof covering requirements",
        "triggered_by_loss": {{true|false}}
      },
      {
        "code_reference": "IRC R703.2",
        "requirement": "Weather-resistant exterior wall envelope",
        "triggered_by_loss": {{true|false}}
      },
      {
        "code_reference": "IECC R402",
        "requirement": "Building thermal envelope",
        "triggered_by_loss": {{true|false}}
      }
    ]
  },
  "inspection_strategy": {
    "inspection_type": "{{initial|supplement|re_inspection|appraisal}}",
    "estimated_duration_hours": {{DURATION}},
    "inspector_count": {{COUNT}},
    "access_requirements": {
      "interior_access": {{true|false}},
      "attic_access": {{true|false}},
      "roof_access_method": "{{ladder|drone|cherry_picker|interior_hatch|not_accessible}}",
      "utility_access": {{true|false}},
      "special_considerations": "{{PET_WARNINGS|GATE_CODES|SECURITY|HAZARDS}}"
    },
    "equipment_checklist": {
      "mandatory": [
        "Digital camera with macro capability (minimum 12MP)",
        "Ladder (28 ft minimum for 2-story residential)",
        "Tape measure (25 ft minimum)",
        "Roof chalk or lumber crayon",
        "Flashlight/headlamp",
        "Safety equipment (hard hat, gloves, eye protection, harness)",
        "Tablet or laptop for field notes",
        "GPS unit or GPS-enabled camera"
      ],
      "conditional": [
        {
          "item": "Moisture meter (Protimeter Surveymaster or equivalent)",
          "required_when": "Interior inspection indicated or water damage suspected"
        },
        {
          "item": "Thermal imaging camera (FLIR C5 or equivalent)",
          "required_when": "Water damage, moisture intrusion, or insulation damage suspected"
        },
        {
          "item": "FAA Part 107 certified drone with 4K camera",
          "required_when": "Roof not safely accessible, steep pitch (>7/12), or 3+ stories"
        },
        {
          "item": "Core cutter or shingle gauge",
          "required_when": "Layer count verification needed for code upgrade argument"
        },
        {
          "item": "Manlift or cherry picker (40 ft minimum)",
          "required_when": "Commercial property with flat roof or multi-story"
        }
      ]
    },
    "photo_requirements": {
      "minimum_total_photos": {{MIN_COUNT}},
      "required_categories": [
        {
          "category": "Property overview",
          "minimum_count": 4,
          "description": "All four elevations from street/ground level"
        },
        {
          "category": "Roof overview",
          "minimum_count": 4,
          "description": "One per slope, showing overall condition"
        },
        {
          "category": "Roof detail — damage",
          "minimum_count": 10,
          "description": "Close-ups of all damage with chalk circles and ruler for scale"
        },
        {
          "category": "Roof detail — test squares",
          "minimum_count": 4,
          "description": "One 10x10 ft test square per slope with Haag classification"
        },
        {
          "category": "Siding overview",
          "minimum_count": 4,
          "description": "All four elevations"
        },
        {
          "category": "Siding detail — damage",
          "minimum_count": 8,
          "description": "Close-ups of damaged areas per elevation"
        },
        {
          "category": "Gutters and downspouts",
          "minimum_count": 4,
          "description": "Each run, showing damage and separations"
        },
        {
          "category": "Windows and doors",
          "minimum_count": 4,
          "description": "Each damaged unit, frame and glass"
        },
        {
          "category": "Accessories",
          "minimum_count": 4,
          "description": "Skylights, chimneys, vents, solar panels, satellite dishes"
        },
        {
          "category": "Fence and outdoor structures",
          "minimum_count": 2,
          "description": "Overall and detail of damaged sections"
        },
        {
          "category": "HVAC exterior",
          "minimum_count": 2,
          "description": "Condenser fins, overall unit, data plate"
        }
      ]
    },
    "safety_assessment": {
      "roof_pitch_safety": "{{safe|caution|unsafe}}",
      "structural_integrity_concerns": "{{NONE|SPECIFIC_CONCERNS}}",
      "electrical_hazards": "{{NONE|OVERHEAD_LINES|SERVICE_ENTRANCE|SOLAR_DISCONNECT}}",
      "weather_dependent": {{true|false}},
      "recommended_weather_window": "{{TEMP_RANGE_WIND_SPEED_VISIBILITY}}",
      "fall_protection_required": {{true|false}},
      "specialized_equipment_needed": "{{NONE|CHERRY_PICKER|SCAFFOLD|ROPE_ACCESS}}"
    }
  },
  "documentation_requirements": {
    "chain_of_custody": {
      "custodian": "{{INSPECTOR_NAME}}",
      "custodian_license": "{{LICENSE_NUMBER}}",
      "evidence_handling_procedure": "All photos timestamped and GPS-tagged. Memory cards sealed and logged. Digital files uploaded to secure cloud storage within 4 hours of inspection.",
      "retention_period_days": 2555
    },
    "report_classification": "{{work_product|attorney_client_privileged|confidential}}",
    "distribution_list": [
      "{{CLIENT_NAME}} (Policyholder)",
      "{{ATTORNEY_NAME}} (if represented)",
      "ClaimEdge LLC file"
    ],
    "statutory_notices": {
      "215_ilcs_5_154_6": "Illinois insurance code claims handling requirements",
      "215_ilcs_5_155": "Vexatious delay — attorney fee award provision",
      "duty_to_cooperate": "Policyholder obligation to allow reasonable inspection"
    }
  },
  "risk_flags": [
    {
      "flag_type": "{{CARRIER_PREVIOUSLY_INSPECTED|UNREPRESENTED_CLAIMANT|STATUTE_LIMITATIONS|PRIOR_DAMAGE|CODE_UPGRADE_REQUIRED}}",
      "severity": "{{low|medium|high|critical}}",
      "description": "{{EXPLANATION}}",
      "recommended_action": "{{ACTION}}"
    }
  ]
}
```
