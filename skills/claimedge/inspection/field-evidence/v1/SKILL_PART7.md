### Function 5: Drone Survey Integrator

**Output:** Drone Survey Results JSON

```json
{
  "survey_id": "CE-DRONE-{{CLAIM_NUMBER}}-{{YYYYMMDD}}",
  "claim_number": "{{CLAIM_NUMBER}}",
  "flight_metadata": {
    "flight_date": "{{YYYY-MM-DD}}",
    "start_time": "{{HH:MM}}",
    "end_time": "{{HH:MM}}",
    "duration_minutes": {{DURATION}},
    "drone_model": "{{MODEL}}",
    "drone_serial": "{{SERIAL}}",
    "operator_name": "{{PILOT_NAME}}",
    "operator_cert_number": "{{FAA_CERT_NUMBER}}",
    "laanc_authorization": "{{AUTH_NUMBER}}",
    "airspace_class": "{{class_g|class_e_surface|class_d|class_c|class_b}}",
    "max_altitude_agl_ft": {{ALTITUDE}},
    "insurance_endorsement_active": {{true|false}}
  },
  "weather_at_flight": {
    "temperature_f": {{TEMP}},
    "wind_speed_mph": {{WIND}},
    "wind_gust_mph": {{GUST}},
    "visibility_mi": {{VIS}},
    "cloud_ceiling_ft": {{CEILING}}
  },
  "flight_plan": {
    "waypoints": [
      {
        "waypoint_id": "WP-01",
        "sequence": 1,
        "latitude": {{LAT}},
        "longitude": {{LON}},
        "altitude_ft_agl": {{ALT}},
        "action": "{{photo|video|hover|return}}",
        "photo_taken": {{true|false}},
        "video_taken": {{true|false}}
      }
    ],
    "total_waypoints": {{COUNT}},
    "flight_pattern": "{{perimeter|grid|orbital|manual}}",
    "overlap_percentage": {{OVERLAP}},
    "ground_sample_distance_cm": {{GSD}}
  },
  "aerial_photos": [
    {
      "photo_id": "CE-PH-###",
      "waypoint_id": "WP-##",
      "timestamp": "{{HH:MM:SS}}",
      "gps_coordinates": {
        "latitude": {{LAT}},
        "longitude": {{LON}},
        "altitude_ft_agl": {{ALT}}
      },
      "heading_degrees": {{HEADING}},
      "gimbal_pitch": {{PITCH}},
      "description": "{{DETAILED_DESCRIPTION}}",
      "view_type": "{{overhead|oblique|perimeter|detail}}",
      "system_visible": "{{roof|siding|full_property}}",
      "damage_observed": {{true|false}},
      "damage_description": "{{DESCRIPTION_OR_none}}"
    }
  ],
  "hazards_identified": [
    {
      "hazard_type": "{{POWER_LINES|TREES|STRUCTURES|ANTENNA|BIRDS|WIND_GUST|RF_INTERFERENCE}}",
      "description": "{{DESCRIPTION}}",
      "severity": "{{low|medium|high}}",
      "mitigation_action": "{{ACTION_TAKEN}}",
      "waypoint_affected": "WP-##"
    }
  ],
  "emergency_procedures": {
    "emergency_landing_zones": [
      {
        "zone_id": "ELZ-01",
        "latitude": {{LAT}},
        "longitude": {{LON}},
        "description": "{{DESCRIPTION}}",
        "suitability": "{{safe|caution|unsafe}}"
      }
    ],
    "signal_interference": {{true|false}},
    "interference_description": "{{DESCRIPTION_OR_none}}",
    "lost_link_procedure_followed": {{true|false}}
  },
  "battery_log": {
    "cycles_used": {{COUNT}},
    "starting_charge_pct": {{PERCENT}},
    "ending_charge_pct": {{PERCENT}},
    "flight_time_per_battery_min": [{{MIN1}}, {{MIN2}}]
  },
  "pre_flight_checklist": {
    "aircraft_inspection": {{true|false}},
    "propeller_check": {{true|false}},
    "battery_charge_verified": {{true|false}},
    "sd_card_space_verified": {{true|false}},
    "gps_lock_acquired": {{true|false}},
    "compass_calibration_current": {{true|false}},
    "firmware_up_to_date": {{true|false}},
    "weather_conditions_acceptable": {{true|false}},
    "airspace_authorization_confirmed": {{true|false}},
    "insurance_current": {{true|false}}
  },
  "faa_compliance": {
    "part_107_compliant": {{true|false}},
    "visual_line_of_sight_maintained": {{true|false}},
    "max_altitude_400ft_agl": {{true|false}},
    "no_flight_over_people": {{true|false}},
    "no_flight_in_moving_vehicle": {{true|false}},
    "daylight_only_operation": {{true|false}},
    "right_of_way_to_manned_aircraft": {{true|false}},
    "remote_id_operational": {{true|false}},
    "violations": ["{{VIOLATION_OR_empty}}"]
  }
}
```
