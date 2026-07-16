### Function 4: Interior & Moisture Inspector

**Output:** Interior & Moisture Report JSON

```json
{
  "report_id": "CE-INT-{{CLAIM_NUMBER}}-{{YYYYMMDD}}",
  "claim_number": "{{CLAIM_NUMBER}}",
  "inspection_metadata": {
    "inspection_date": "{{YYYY-MM-DD}}",
    "inspector_name": "{{INSPECTOR_NAME}}",
    "interior_scope": "{{full_interior|water_affected_only|attic_only|specific_rooms|none}}",
    "moisture_meter": {
      "model": "{{METER_MODEL}}",
      "serial_number": "{{SERIAL}}",
      "calibration_date": "{{YYYY-MM-DD}}",
      "calibration_current": {{true|false}}
    },
    "thermal_imager": {
      "model": "{{THERMAL_MODEL_OR_null}}",
      "serial_number": "{{SERIAL_OR_null}}"
    },
    "interior_conditions": {
      "temperature_f": {{TEMP}},
      "relative_humidity_pct": {{RH}},
      "dew_point_f": {{DEW_POINT}}
    }
  },
  "room_by_room_assessment": [
    {
      "room_name": "{{ROOM_NAME}}",
      "level": "{{basement|first|second|third|attic}}",
      "ceiling_condition": {
        "observed_damage": {{true|false}},
        "damage_type": "{{water_stain|sagging|crack|paint_peel|mold|none}}",
        "damage_description": "{{DESCRIPTION}}",
        "affected_area_sf": {{SF_OR_null}},
        "photo_reference": "CE-PH-###"
      },
      "wall_condition": {
        "observed_damage": {{true|false}},
        "damage_type": "{{water_stain|swelling|crack|paint_peel|mold|efflorescence|none}}",
        "damage_description": "{{DESCRIPTION}}",
        "affected_area_sf": {{SF_OR_null}},
        "photo_reference": "CE-PH-###"
      },
      "floor_condition": {
        "observed_damage": {{true|false}},
        "damage_type": "{{warping|buckling|stain|soft_spots|mold|none}}",
        "damage_description": "{{DESCRIPTION}}",
        "photo_reference": "CE-PH-###"
      },
      "window_condition": {
        "observed_damage": {{true|false}},
        "damage_type": "{{leak|seal_failure|frame_damage|none}}",
        "damage_description": "{{DESCRIPTION}}"
      },
      "moisture_readings": [
        {
          "location": "{{WALL_OR_CEILING_LOCATION}}",
          "reading_pct": {{PERCENTAGE}},
          "classification": "{{normal|elevated|saturated}}",
          "normal_baseline_pct": {{BASELINE}},
          "delta_from_baseline": {{DELTA}},
          "timestamp": "{{HH:MM}}"
        }
      ],
      "thermal_anomalies": [
        {
          "location": "{{AREA_DESCRIPTION}}",
          "anomaly_type": "{{cold_spot|hot_spot|moisture_pattern}}",
          "temperature_delta_f": {{DELTA}},
          "interpretation": "{{LIKELY_CAUSE}}",
          "photo_reference": "CE-PH-###"
        }
      ],
      "mold_assessment": {
        "visible_mold": {{true|false}},
        "mold_location": "{{SURFACE_DESCRIPTION}}",
        "mold_color": "{{black|green|white|brown|other}}",
        "mold_extent": "{{spotty|patchy|extensive}}",
        "musty_odor": {{true|false}},
        "recommended_testing": "{{air_sample|surface_sample|ERMI|none}}",
        "photo_reference": "CE-PH-###"
      },
      "room_summary": "{{NARRATIVE_SUMMARY}}",
      "recommended_action": "{{dry_out|remove_materials|mold_remediation|monitor|no_action}}"
    }
  ],
  "attic_assessment": {
    "attic_accessible": {{true|false}},
    "access_method": "{{hatch|scuttle|pull_down_stairs|walk_up}}",
    "attic_dimensions": {
      "approximate_square_footage": {{SF}},
      "peak_height_ft": {{HEIGHT}},
      "rafter_spacing_inches": {{SPACING}}
    },
    "roof_decking_condition": {
      "material": "{{plywood|osb|plank|skip_sheathing}}",
      "water_stains_observed": {{true|false}},
      "stain_description": "{{DESCRIPTION_OR_none}}",
      "decking_delamination": {{true|false}},
      "soft_spots_count": {{COUNT}},
      "photo_reference": "CE-PH-###"
    },
    "insulation_condition": {
      "type": "{{fiberglass_batt|blown_fiberglass|blown_cellulose|spray_foam|rigid_board|mineral_wool|vermiculite}}",
      "depth_inches": {{DEPTH}},
      "r_value_estimated": {{RVALUE}},
      "water_damage": {{true|false}},
      "compaction": {{true|false}},
      "settlement": {{true|false}},
      "displacement": {{true|false}},
      "photo_reference": "CE-PH-###"
    },
    "ventilation_assessment": {
      "intake_ventilation": {
        "soffit_vent_count": {{COUNT}},
        "soffit_vent_condition": "{{clear|blocked|damaged}}",
        "baffle_present": {{true|false}}
      },
      "exhaust_ventilation": {
        "ridge_vent_linear_ft": {{LF}},
        "box_vent_count": {{COUNT}},
        "turbine_count": {{COUNT}},
        "power_vent_count": {{COUNT}},
        "condition": "{{functional|blocked|damaged|inoperable}}"
      }
    },
    "structural_assessment": {
      "rafter_condition": "{{sound|minor_water_stain|delamination|rot|insect_damage}}",
      "truss_condition": "{{sound|damaged|modified|none}}",
      "collar_ties_present": {{true|false}},
      "ceiling_joist_condition": "{{sound|sagging|damaged}}"
    },
    "attic_mold_assessment": {
      "visible_mold": {{true|false}},
      "mold_location": "{{rafters|decking|insulation|hvac_ducts|none}}",
      "mold_extent": "{{none|spotty|patchy|extensive}}",
      "ventilation_contribution": "{{adequate|inadequate|poor}}",
      "recommended_action": "{{none|surface_cleaning|remediation|full_removal}}"
    }
  },
  "moisture_summary": {
    "total_readings_taken": {{COUNT}},
    "readings_normal": {{COUNT}},
    "readings_elevated": {{COUNT}},
    "readings_saturated": {{COUNT}},
    "highest_reading_pct": {{MAX}},
    "highest_reading_location": "{{LOCATION}}",
    "moisture_map_description": "{{NARRATIVE_DESCRIPTION_OF_MOISTURE_PATTERN}}",
    "water_source_opinion": "{{roof_leak|pipe_burst|groundwater|condensation|unknown}}",
    " drying_recommendations": {
      "dehumidifiers_needed": {{COUNT}},
      "air_movers_needed": {{COUNT}},
      "estimated_drying_days": {{DAYS}},
      "containment_required": {{true|false}}
    }
  },
  "health_safety_concerns": [
    {
      "concern": "{{DESCRIPTION}}",
      "severity": "{{low|medium|high|critical}}",
      "recommended_action": "{{ACTION}}"
    }
  ],
  "code_upgrade_opportunities": [
    {
      "code_reference": "IRC R302.6",
      "requirement": "Fire separation between garage and living space — 1/2 inch gypsum minimum",
      "applicable": {{true|false}},
      "justification": "{{IF_APPLICABLE}}"
    },
    {
      "code_reference": "IECC R402",
      "requirement": "Insulation R-value upgrade if wall/ceiling opened",
      "applicable": {{true|false}},
      "justification": "{{IF_APPLICABLE}}"
    }
  ]
}
```
