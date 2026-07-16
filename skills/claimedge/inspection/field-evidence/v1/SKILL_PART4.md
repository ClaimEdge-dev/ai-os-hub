### Function 2: Field Evidence Collector

**Output:** Field Evidence Collection JSON

```json
{
  "collection_id": "CE-FIELD-{{CLAIM_NUMBER}}-{{YYYYMMDD}}",
  "claim_number": "{{CLAIM_NUMBER}}",
  "inspection_metadata": {
    "inspection_date": "{{YYYY-MM-DD}}",
    "start_time": "{{HH:MM}}",
    "end_time": "{{HH:MM}}",
    "duration_minutes": {{DURATION}},
    "inspector_name": "{{INSPECTOR_NAME}}",
    "inspector_license": "{{LICENSE_NUMBER}}",
    "inspector_company": "ClaimEdge LLC",
    "inspection_method": "{{ground_only|ladder_access|drone_assisted|drone_primary|cherry_picker|rope_access}}",
    "weather_conditions": {
      "temperature_f": {{TEMP}},
      "conditions": "{{clear|partly_cloudy|overcast|rain|snow}}",
      "wind_speed_mph": {{WIND}},
      "precipitation": "{{none|light|moderate|heavy}}",
      "visibility_mi": {{VIS}}
    }
  },
  "roof_assessment": {
    "roof_accessible": {{true|false}},
    "access_method": "{{interior_hatch|exterior_ladder|drone_only|not_accessible}}",
    "number_of_slopes": {{COUNT}},
    "total_squares": {{SQUARES}},
    "primary_covering": "{{MATERIAL}}",
    "estimated_age_years": {{AGE}},
    "layer_count": {{LAYERS}},
    "manufacturer": "{{MANUFACTURER_OR_unknown}}",
    "product_line": "{{PRODUCT_OR_unknown}}",
    "warranty_status": "{{active|expired|unknown}}",
    "slopes": [
      {
        "slope_id": "{{IDENTIFIER}}",
        "designation": "{{Front|Rear|Left|Right|Garage_Front|Garage_Rear|Dormer_Front|Dormer_Rear}}",
        "dimensions": {
          "length_ft": {{L}},
          "width_ft": {{W}},
          "pitch": "{{X_Y}}",
          "squares": {{SQ}}
        },
        "orientation": "{{N|NE|E|SE|S|SW|W|NW}}",
        "solar_exposure": "{{full_sun|partial_sun|shaded}}",
        "condition_pre_loss": "{{excellent|good|fair|poor}}",
        "haag_hail_damage_assessment": {
          "test_square_performed": {{true|false}},
          "test_square_dimensions": "10 ft x 10 ft",
          "hail_hits_per_test_square": {{COUNT}},
          "damage_classification": "{{C|M|MO|MA|S}}",
          "classification_meaning": "{{Cosmetic|Minor|Moderate|Major|Severe}}",
          "bruising_count": {{COUNT}},
          "fracturing_count": {{COUNT}},
          "granule_loss_pct": {{PERCENT}},
          "punctures_count": {{COUNT}},
          "indentations_count": {{COUNT}},
          "damage_description": "{{DETAILED_DESCRIPTION}}",
          "photo_references": ["CE-PH-###", "CE-PH-###"]
        },
        "haag_wind_damage_assessment": {
          "uplift_damage_count": {{COUNT}},
          "creasing_count": {{COUNT}},
          "tearing_count": {{COUNT}},
          "missing_pieces_count": {{COUNT}},
          "membrane_displacement_sf": {{SF_OR_null}},
          "damage_description": "{{DETAILED_DESCRIPTION}}",
          "photo_references": ["CE-PH-###", "CE-PH-###"]
        },
        "slope_summary": "{{NARRATIVE_SUMMARY_OF_DAMAGE}}",
        "recommended_action": "{{repair|replace|monitor}}",
        "replacement_justification": "{{CODE|MANUFACTURER|FUNCTIONAL|COSMETIC|None}}"
      }
    ],
    "roof_summary": {
      "overall_damage_classification": "{{C|M|MO|MA|S}}",
      "slopes_requiring_replacement": {{COUNT}},
      "slopes_requiring_repair": {{COUNT}},
      "slopes_with_no_damage": {{COUNT}},
      "total_hail_hits_all_test_squares": {{COUNT}},
      "primary_damage_type": "{{hail|wind|combined|other}}",
      "functional_damage_present": {{true|false}},
      "code_upgrade_triggers": [
        {
          "code_reference": "IRC R905.2.1",
          "trigger": "Spaced decking requires solid sheathing for new roof covering",
          "applicable": {{true|false}}
        },
        {
          "code_reference": "IRC R905.1.2",
          "trigger": "Ice barrier required at eaves (2 rows in Illinois)",
          "applicable": {{true|false}}
        },
        {
          "code_reference": "IRC R905.2.8.5",
          "trigger": "Drip edge required at eaves and rakes",
          "applicable": {{true|false}}
        }
      ]
    }
  },
  "siding_assessment": {
    "primary_material": "{{MATERIAL}}",
    "number_of_elevations": {{COUNT}},
    "elevations": [
      {
        "elevation_id": "{{FRONT|REAR|LEFT|RIGHT}}",
        "compass_bearing": "{{DIRECTION}}",
        "square_footage": {{SF}},
        "condition_pre_loss": "{{excellent|good|fair|poor}}",
        "damage_observed": {
          "hail_damage": {
            "present": {{true|false}},
            "impact_marks_count": {{COUNT}},
            "cracking_count": {{COUNT}},
            "chipping_count": {{COUNT}},
            "holes_count": {{COUNT}},
            "damage_description": "{{DESCRIPTION}}"
          },
          "wind_damage": {
            "present": {{true|false}},
            "loose_panels_count": {{COUNT}},
            "missing_panels_count": {{COUNT}},
            "warping_count": {{COUNT}},
            "damage_description": "{{DESCRIPTION}}"
          }
        },
        "photo_references": ["CE-PH-###"],
        "recommended_action": "{{repair|replace|no_action}}"
      }
    ],
    "siding_summary": {
      "elevations_with_damage": {{COUNT}},
      "total_damage_area_sf": {{SF}},
      "primary_damage_type": "{{hail|wind|combined|none}}",
      "code_upgrade_triggers": [
        {
          "code_reference": "IRC R703.2",
          "trigger": "Weather-resistant barrier required behind new siding",
          "applicable": {{true|false}}
        }
      ]
    }
  },
  "gutter_assessment": {
    "gutter_type": "{{aluminum_k_style|aluminum_half_round|copper|vinyl|steel|galvanized|unknown}}",
    "downspout_count": {{COUNT}},
    "linear_feet": {{LF}},
    "damage": {
      "dents_from_hail": {{true|false}},
      "dented_sections_count": {{COUNT}},
      "separations_count": {{COUNT}},
      "loose_hangers_count": {{COUNT}},
      "holes_count": {{COUNT}},
      "damage_description": "{{DESCRIPTION}}"
    },
    "recommended_action": "{{repair|replace|no_action}}"
  },
  "window_door_assessment": {
    "window_count": {{COUNT}},
    "door_count": {{COUNT}},
    "damaged_windows": [
      {
        "location": "{{ROOM_OR_ELEVATION}}",
        "window_type": "{{single_hung|double_hung|casement|slider|fixed|bay|bow}}",
        "frame_material": "{{vinyl|wood|aluminum|fiberglass|composite}}",
        "damage_type": "{{glass_crack|frame_dent|screen_tear|seal_failure|operational}}",
        "damage_description": "{{DESCRIPTION}}",
        "photo_reference": "CE-PH-###",
        "recommended_action": "{{repair|replace}}"
      }
    ]
  },
  "accessory_assessment": {
    "skylights": {
      "count": {{COUNT}},
      "damaged_count": {{COUNT}},
      "damage_description": "{{DESCRIPTION}}"
    },
    "chimneys": {
      "count": {{COUNT}},
      "damaged_count": {{COUNT}},
      "damage_description": "{{DESCRIPTION}}"
    },
    "vents": {
      "ridge_vent_ft": {{LF}},
      "box_vent_count": {{COUNT}},
      "turbine_count": {{COUNT}},
      "damaged_count": {{COUNT}}
    },
    "solar_panels": {
      "count": {{COUNT}},
      "damaged_count": {{COUNT}},
      "damage_description": "{{DESCRIPTION}}"
    },
    "satellite_dishes": {
      "count": {{COUNT}},
      "damaged_count": {{COUNT}}
    }
  },
  "outdoor_structures": {
    "fencing": {
      "type": "{{wood|vinyl|aluminum|chain_link|wrought_iron}}",
      "linear_feet": {{LF}},
      "damaged": {{true|false}},
      "damage_description": "{{DESCRIPTION}}"
    },
    "sheds": {
      "count": {{COUNT}},
      "damaged_count": {{COUNT}},
      "damage_description": "{{DESCRIPTION}}"
    },
    "garage": {
      "attached": {{true|false}},
      "door_count": {{COUNT}},
      "door_damage": "{{DESCRIPTION}}"
    }
  },
  "hvac_assessment": {
    "condenser_units": [
      {
        "location": "{{LOCATION}}",
        "make": "{{MAKE}}",
        "model": "{{MODEL}}",
        "serial": "{{SERIAL}}",
        "manufacture_date": "{{YYYY-MM}}",
        "age_years": {{AGE}},
        "fins_damaged_pct": {{PERCENT}},
        "fan_blades_damaged": {{true|false}},
        "refrigerant_lines_damaged": {{true|false}},
        "pad_shifted": {{true|false}},
        "operational_status": "{{operational|inoperable|unknown}}",
        "photo_reference": "CE-PH-###",
        "recommended_action": "{{repair|replace|no_action}}"
      }
    ]
  },
  "field_notes": "{{FREE_FORM_INSPECTOR_NOTES}}",
  "chain_of_custody": {
    "inspection_performed_by": "{{INSPECTOR_NAME}}",
    "license_number": "{{LICENSE}}",
    "date_time": "{{YYYY-MM-DD HH:MM}}",
    "evidence_integrity": "All photos GPS-tagged and timestamped. Memory card sealed.",
    "next_custodian": "ClaimEdge LLC Evidence Management"
  }
}
```
