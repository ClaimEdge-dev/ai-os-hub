### Function 3: Photo Documentation Manager

**Output:** Photo Documentation Index JSON

```json
{
  "index_id": "CE-PHOTO-{{CLAIM_NUMBER}}-{{YYYYMMDD}}",
  "claim_number": "{{CLAIM_NUMBER}}",
  "generation_timestamp": "{{ISO8601_TIMESTAMP}}",
  "naming_convention": "CE-PH-### (ClaimEdge Photo, sequential 3-digit)",
  "photo_count_summary": {
    "total_photos": {{TOTAL_COUNT}},
    "total_with_gps": {{GPS_COUNT}},
    "total_with_timestamp": {{TS_COUNT}},
    "photos_meeting_minimum": {{MEETING_COUNT}},
    "categories_covered": {{CATEGORY_COUNT}},
    "categories_missing": ["{{CATEGORY_NAME}}"]
  },
  "photo_index": [
    {
      "photo_id": "CE-PH-001",
      "filename": "{{ORIGINAL_FILENAME}}",
      "timestamp": "{{YYYY-MM-DD HH:MM:SS}}",
      "gps_coordinates": {
        "latitude": {{LAT}},
        "longitude": {{LON}},
        "altitude_ft": {{ALT}}
      },
      "description": "{{DETAILED_DESCRIPTION}}",
      "system": "{{roof|siding|gutter|window|fence|hvac|interior|attic|drone}}",
      "subsystem": "{{Front_slope|Rear_elevation|Kitchen|etc}}",
      "damage_type": "{{hail_bruise|wind_uplift|water_stain|none}}",
      "haag_classification": "{{C|M|MO|MA|S|N/A}}",
      "tags": ["{{tag1}}", "{{tag2}}"],
      "scale_reference": {{true|false}},
      "chalk_circle_visible": {{true|false}},
      "quality_rating": "{{excellent|good|fair|poor}}",
      "resolution_pixels": "{{WIDTHxHEIGHT}}",
      "file_size_mb": {{SIZE}}
    }
  ],
  "category_summaries": {
    "property_overview": {
      "photos_count": {{COUNT}},
      "required_minimum": 4,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "roof_overview": {
      "photos_count": {{COUNT}},
      "required_minimum": 4,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "roof_detail_damage": {
      "photos_count": {{COUNT}},
      "required_minimum": 10,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "roof_test_squares": {
      "photos_count": {{COUNT}},
      "required_minimum": 4,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"],
      "test_square_results": [
        {
          "slope": "{{SLOPE_NAME}}",
          "photo_id": "CE-PH-###",
          "hail_hits_count": {{COUNT}},
          "classification": "{{C|M|MO|MA|S}}"
        }
      ]
    },
    "siding_overview": {
      "photos_count": {{COUNT}},
      "required_minimum": 4,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "siding_detail_damage": {
      "photos_count": {{COUNT}},
      "required_minimum": 8,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "gutters_downspouts": {
      "photos_count": {{COUNT}},
      "required_minimum": 4,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "windows_doors": {
      "photos_count": {{COUNT}},
      "required_minimum": 4,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "accessories": {
      "photos_count": {{COUNT}},
      "required_minimum": 4,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "fence_outdoor": {
      "photos_count": {{COUNT}},
      "required_minimum": 2,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "hvac_exterior": {
      "photos_count": {{COUNT}},
      "required_minimum": 2,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "interior": {
      "photos_count": {{COUNT}},
      "required_minimum": 5,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "attic": {
      "photos_count": {{COUNT}},
      "required_minimum": 4,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    },
    "drone_aerial": {
      "photos_count": {{COUNT}},
      "required_minimum": 6,
      "meets_minimum": {{true|false}},
      "photo_ids": ["CE-PH-###"]
    }
  },
  "gap_analysis": {
    "gaps_found": {{true|false}},
    "missing_categories": ["{{CATEGORY}}"],
    "missing_critical_photos": ["{{DESCRIPTION}}"],
    "recommendations": ["{{ACTION_TO_RESOLVE}}"]
  },
  "quality_assessment": {
    "average_resolution": "{{WIDTHxHEIGHT}}",
    "focus_quality": "{{excellent|good|fair|poor}}",
    "lighting_rating": "{{excellent|good|fair|poor}}",
    "scale_reference_pct": {{PERCENT_WITH_SCALE}},
    "chalk_circle_pct": {{PERCENT_WITH_CHALK}},
    "gps_embedded_pct": {{PERCENT_WITH_GPS}},
    "overall_quality_score": "{{A|B|C|D|F}}",
    "improvement_recommendations": ["{{RECOMMENDATION}}"]
  },
  "companycam_sync": {
    "project_id": "{{PROJECT_ID_OR_null}}",
    "sync_status": "{{synced|pending|failed|not_applicable}}",
    "last_sync_timestamp": "{{ISO8601_OR_null}}",
    "photos_synced_count": {{COUNT}},
    "sync_errors": ["{{ERROR_OR_empty}}"]
  },
  "chain_of_custody": {
    "photos_taken_by": "{{INSPECTOR_NAME}}",
    "camera_model": "{{MODEL}}",
    "camera_serial": "{{SERIAL}}",
    "memory_card_id": "{{CARD_ID}}",
    "transfer_method": "{{USB|WIFI|CLOUD_UPLOAD}}",
    "transferred_to": "ClaimEdge LLC Secure Storage",
    "transfer_timestamp": "{{ISO8601}}",
    "integrity_hash_verified": {{true|false}}
  }
}
```
