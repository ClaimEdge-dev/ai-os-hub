### Function 2: Field Evidence Collector

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `claim_number` | string | Yes | Claim number from Function 1 |
| `pre_inspection_plan` | object | Yes | Complete output from Function 1 |
| `inspection_date` | string | Yes | ISO 8601 date of inspection (YYYY-MM-DD) |
| `inspection_start_time` | string | Yes | Local start time in HH:MM format |
| `weather_conditions` | object | Yes | `{ temperature_f, conditions, wind_speed_mph, precipitation, visibility_mi }` |
| `inspector_name` | string | Yes | Full name of lead inspector |
| `inspector_license` | string | Yes | State license number (e.g., "IL-PA-12345") |
| `inspector_company` | string | Yes | Company name for E&O coverage |
| `inspection_method` | enum | Yes | `ground_only`, `ladder_access`, `drone_assisted`, `drone_primary`, `cherry_picker`, `rope_access` |
| `roof_accessible` | boolean | Yes | Whether roof was safely accessible |
| `roof_access_method` | enum | No | `interior_hatch`, `exterior_ladder`, `drone_only`, `not_accessible` |
| `number_of_slopes` | integer | Yes | Count of distinct roof slopes |
| `slope_designations` | array | Yes | Array of slope identifiers (e.g., `["Front", "Rear", "Left", "Right", "Garage Front", "Garage Rear"]`) |
| `roof_dimensions` | object | Yes | `{ total_squares: number, slope_measurements: array of {slope_id, length_ft, width_ft, pitch, squares} }` |
| `siding_material` | enum | No | `vinyl`, `aluminum`, `steel`, `wood`, `fiber_cement`, `brick`, `stone`, `stucco`, `efis`, `composite` |
| `siding_exposures` | integer | No | Number of siding exposures (walls) inspected |
| `has_gutters` | boolean | No | Whether property has gutters and downspouts |
| `has_skylights` | integer | No | Count of skylights |
| `has_chimneys` | integer | No | Count of chimneys |
| `has_ventilation` | integer | No | Count of ventilation components (ridge vents, box vents, turbines) |
| `has_solar_panels` | integer | No | Count of solar panel arrays |
| `has_satellite_dishes` | integer | No | Count of satellite dishes |
| `has_fencing` | boolean | No | Whether fencing is present and needs inspection |
| `adjacent_structure_damage` | boolean | No | Whether sheds, garages, or other structures show damage |

### Function 3: Photo Documentation Manager

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `claim_number` | string | Yes | Claim number |
| `field_evidence` | object | Yes | Complete output from Function 2 |
| `photo_log` | array | Yes | Array of photo entries: `{ photo_id, filename, timestamp, description, tags, gps_coordinates, slope_id, damage_type, haag_classification }` |
| `minimum_photo_requirements` | object | Yes | `{ roof_overview_min, slope_detail_min, test_square_min, interior_min, exterior_min, total_minimum }` |
| `photo_quality_metrics` | object | No | `{ average_resolution, focus_quality, lighting_rating, coverage_completeness_pct }` |
| `companycam_project_id` | string | No | CompanyCam project identifier if applicable |
| `equipment_used` | object | Yes | `{ camera_model, lens_mm, flash_used, tripod_used, drone_model, thermal_imager_model }` |
| `geo_tagging_verified` | boolean | Yes | Whether GPS coordinates are embedded and verified |
| `chain_of_custody` | object | Yes | `{ photos_taken_by, transferred_to, transfer_timestamp, integrity_verified }` |

### Function 4: Interior & Moisture Inspector

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `claim_number` | string | Yes | Claim number |
| `field_evidence` | object | Yes | Output from Function 2 |
| `interior_scope` | enum | Yes | `full_interior`, `water_affected_only`, `attic_only`, `specific_rooms`, `none` |
| `affected_rooms` | array | No | Array of room names if specific rooms: `["Kitchen", "Master Bedroom", "Basement"]` |
| `moisture_meter_type` | enum | Yes | `protimeter_surveymaster`, `protimeter_moisture_measurement_system`, `tramex_moisture_encounter`, `delmhorst`, `flir_mr77`, `other` |
| `moisture_meter_serial` | string | Yes | Serial number of moisture meter for calibration traceability |
| `calibration_date` | string | Yes | ISO 8601 date of last calibration (YYYY-MM-DD) |
| `thermal_imager_model` | string | No | e.g., "FLIR C5", "FLIR E8-XT", "FLIR T540" |
| `thermal_imager_serial` | string | No | Serial number of thermal imager |
| `interior_temperature` | number | Yes | Indoor temperature in Fahrenheit |
| `relative_humidity_pct` | number | Yes | Indoor relative humidity percentage |
| `dew_point_f` | number | No | Calculated dew point in Fahrenheit |
| `water_source` | enum | No | `roof_leak`, `pipe_burst`, `appliance_malfunction`, `groundwater`, `storm_surge`, `backup_sewer`, `fire_suppression`, `unknown` |
| `days_since_loss` | integer | Yes | Number of days between date of loss and inspection date |
| `prior_mitigation` | boolean | No | Whether emergency mitigation has been performed |
| `mitigation_company` | string | No | Name of mitigation company if performed |
| `mold_visible` | boolean | No | Whether visible mold growth is present |
| `odor_present` | enum | No | `none`, `musty`, `wet_carpet`, `sewage`, `smoke`, `chemical` |

### Function 5: Drone Survey Integrator

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `claim_number` | string | Yes | Claim number |
| `field_evidence` | object | Yes | Output from Function 2 |
| `drone_operator_name` | string | Yes | Name of FAA Part 107 certified pilot |
| `drone_operator_cert_number` | string | Yes | FAA Remote Pilot Certificate number |
| `drone_model` | enum | Yes | `dji_mavic_3_pro`, `dji_mavic_3t`, `dji_air_3`, `dji_mini_4_pro`, `autel_evo_ii_pro`, `skydio_x10`, `other` |
| `drone_serial` | string | Yes | Aircraft serial number |
| `flight_date` | string | Yes | ISO 8601 date of flight (YYYY-MM-DD) |
| `flight_start_time` | string | Yes | Local time in HH:MM (24-hour) |
| `flight_end_time` | string | Yes | Local time in HH:MM (24-hour) |
| `flight_duration_minutes` | number | Yes | Total flight time in minutes |
| `laanc_authorization` | string | Yes | LAANC authorization number or "Class G — No Authorization Required" |
| `airspace_class` | enum | Yes | `class_g`, `class_e_surface`, `class_d`, `class_c`, `class_b` |
| `max_altitude_agl_ft` | integer | Yes | Maximum altitude above ground level in feet (max 400 ft per Part 107) |
| `weather_at_flight` | object | Yes | `{ temperature_f, wind_speed_mph, wind_gust_mph, visibility_mi, cloud_ceiling_ft }` |
| `flight_waypoints` | array | Yes | Array of `{ waypoint_id, lat, lon, altitude_ft, photo_taken, video_taken }` |
| `number_of_photos` | integer | Yes | Total aerial photos captured |
| `number_of_videos` | integer | No | Total aerial videos captured |
| `hazards_identified` | array | No | Array of `{ hazard_type, description, severity, mitigation_action }` |
| `emergency_landing_zones` | array | No | Array of `{ zone_id, lat, lon, description }` |
| `battery_cycles_used` | integer | Yes | Number of battery cycles consumed |
| `signal_interference` | boolean | No | Whether GPS or control signal interference was encountered |
| `insurance_endorsement` | boolean | Yes | Whether hull and liability insurance is active for drone operations |

### Function 6: Field Report Generator

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `claim_number` | string | Yes | Claim number |
| `pre_inspection_plan` | object | Yes | Output from Function 1 |
| `field_evidence` | object | Yes | Output from Function 2 |
| `photo_documentation` | object | Yes | Output from Function 3 |
| `interior_moisture_report` | object | No | Output from Function 4 (null if no interior inspection performed) |
| `drone_survey` | object | No | Output from Function 5 (null if no drone survey performed) |
| `report_type` | enum | Yes | `initial_inspection`, `supplement`, `re_inspection`, `appraisal`, `litigation_support`, `carrier_response` |
| `addressee` | string | Yes | Report recipient: `policyholder`, `carrier`, `appraisal_panel`, `legal_counsel`, `mediator` |
| `template_id` | enum | Yes | `template_a_residential_hail`, `template_b_commercial_wind`, `template_c_residential_water`, `custom` |
| `include_code_analysis` | boolean | Yes | Whether to include full building code compliance analysis |
| `include_photo_index` | boolean | Yes | Whether to include complete photo index table |
| `include_repair_scope` | boolean | Yes | Whether to include recommended scope of repairs |
| `statute_warnings` | boolean | Yes | Whether to include Illinois statute compliance warnings |
| `confidentiality_level` | enum | Yes | `work_product`, `attorney_client`, `privileged`, `public` |
| `inspector_signature_required` | boolean | Yes | Whether to include digital signature block |
| `turnaround_hours` | integer | Yes | Required delivery timeframe in business hours |

---

## Output Schema
