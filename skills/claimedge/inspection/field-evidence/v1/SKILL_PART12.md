### Template B: Commercial Wind Damage Field Inspection Report

```
================================================================================
                    CLAIMEDGE LLC
         FIELD INSPECTION REPORT — COMMERCIAL WIND DAMAGE
================================================================================

REPORT CONTROL INFORMATION
--------------------------
Report ID:          {{report_id}}
Claim Number:       {{claim_number}}
Policy Number:      {{policy_number}}
Date of Loss:       {{date_of_loss}}
Inspection Date:    {{inspection_date}}
Report Date:        {{report_date}}

PROPERTY INFORMATION
--------------------
Insured Name:       {{client_name}}
Property Address:   {{street_address}}
                    {{city}}, {{state}} {{zip}}
County:             {{county}}
Jurisdiction:       {{municipality}}

Building Details:
  Property Type:    Commercial
  Year Built:       {{year_built}}
  Stories:          {{stories}}
  Square Footage:   {{square_footage}}
  Roof Type:        {{roof_type}}
  Roof Squares:     {{roof_squares}}
  Construction:     {{construction_type}}

INSPECTION DETAILS
------------------
Inspector:          {{inspector_name}}
License Number:     {{license_number}}
Inspection Method:  {{inspection_method}}
Drone Survey:       {{drone_used}} (Pilot: {{pilot_name}}, FAA Cert: {{faa_cert}})
Weather Conditions: {{weather_description}}

CARRIER INFORMATION
-------------------
Carrier:            {{carrier_name}}
Claim Number:       {{claim_number}}

================================================================================
                         SECTION 1: EXECUTIVE SUMMARY
================================================================================

On {{inspection_date}}, I conducted a comprehensive field inspection of the
subject commercial property located at {{street_address}}. The inspection was
performed in response to a reported wind loss on {{date_of_loss}} with
sustained winds of {{wind_speed}} mph and gusts to {{wind_gust}} mph.

KEY FINDINGS:
{{#each key_findings}}
  • {{this}}
{{/each}}

OVERALL ASSESSMENT: The building envelope sustained wind damage consistent with
the reported weather event. The primary damage mechanism was {{damage_mechanism}}.

SCOPE RECOMMENDATION: {{scope_recommendation}}
  Total Roof Area: {{total_squares}} squares
  Slope/Elevations Requiring Replacement: {{replacement_count}}
  Interior Water Damage: {{interior_damage_present}}
  Code Upgrades Identified: {{code_upgrades_count}}

================================================================================
                      SECTION 2: INSPECTION METHODOLOGY
================================================================================

This commercial inspection employed multiple access methods:

  • Ground-level exterior documentation (all elevations)
  • Ladder access to roof perimeter (28 ft extension ladder)
  • Aerial drone survey (DJI Mavic 3 Enterprise, 4K resolution)
  • Interior walk-through with moisture mapping
  • Attic access and inspection

Standards Referenced:
  • Haag Engineering — Commercial Wind Damage Assessment
  • IBC 2021 — Building Code Requirements
  • IEBC 2021 — Existing Building Code
  • IECC 2021 — Energy Conservation Code
  • FM Global Data Sheets (wind uplift)
  • ASCE 7 — Minimum Design Loads

EQUIPMENT USED:
  • Digital SLR camera with macro lens
  • DJI Mavic 3 Enterprise drone
  • Protimeter Surveymaster moisture meter
  • FLIR C5 thermal imaging camera
  • 28 ft extension ladder with standoff
  • Safety harness and fall protection

================================================================================
                        SECTION 3: ROOF FINDINGS
================================================================================

ROOF SYSTEM: {{roof_system_description}}

MEMBRANE ASSESSMENT:
{{#each roof_sections}}
Section: {{section_name}} ({{squares}} squares)
-----------------------------------------------
Damage Observed:
  Membrane Uplift:      {{membrane_uplift_sf}} SF
  Seam Separations:     {{seam_count}} locations
  Fastener Back-Out:    {{fastener_count}}
  Punctures/Tears:      {{puncture_count}}
  Ballast Displacement: {{ballast_sf}} SF

Damage Classification: {{classification}}
Photo References: {{photo_refs}}
Recommended Action: {{action}}

{{/each}}

PARAPET / WALL ASSESSMENT:
  Parapet Condition:    {{parapet_condition}}
  Coping Damage:        {{coping_damage}}
  Wall Siding Damage:   {{wall_damage_description}}

ROOF-MOUNTED EQUIPMENT:
  HVAC Units:           {{hvac_count}} ({{hvac_damaged}} damaged)
  Exhaust Fans:         {{exhaust_count}} ({{exhaust_damaged}} damaged)
  Satellite Dishes:     {{dish_count}} ({{dish_damaged}} damaged)
  Solar Arrays:         {{solar_count}} ({{solar_damaged}} damaged)

DRONE AERIAL FINDINGS:
  Aerial photos captured: {{drone_photo_count}}
  Key aerial observations:
  {{#each drone_observations}}
    • {{this}}
  {{/each}}

================================================================================
                      SECTION 4: EXTERIOR FINDINGS
================================================================================

{{#each elevations}}
{{elevation_name}} Elevation ({{compass_bearing}})
-----------------------------------------------
Square Footage:     {{sf}}
Siding Material:    {{material}}

Damage:
  {{damage_description}}

Photo References: {{photo_refs}}
Action: {{action}}

{{/each}}

WINDOW / DOOR ASSESSMENT:
{{#each windows}}
Location:       {{location}}
Type:           {{window_type}}
Damage:         {{damage_description}}
Photo:          {{photo_ref}}
{{/each}}

LOADING DOCK / OVERHEAD DOORS:
{{#each overhead_doors}}
Door:           {{door_id}}
Damage:         {{damage_description}}
Operational:    {{operational_status}}
{{/each}}

================================================================================
                     SECTION 5: INTERIOR & MOISTURE FINDINGS
================================================================================

INTERIOR SCOPE: Full interior inspection conducted.

MOISTURE MAPPING RESULTS:
Meter: {{meter_model}} (S/N: {{meter_serial}}, Cal: {{cal_date}})
Interior Conditions: Temp {{temp_f}}F, RH {{rh_pct}}%

{{#each moisture_readings}}
Location:       {{location}}
Reading:        {{reading_pct}}% ({{classification}})
Normal Baseline: {{baseline_pct}}%
{{/each}}

ROOMS AFFECTED:
{{#each affected_rooms}}
Room:           {{room_name}}
Ceiling:        {{ceiling_condition}}
Walls:          {{wall_condition}}
Floor:          {{floor_condition}}
Mold Visible:   {{mold_visible}}
Action:         {{recommended_action}}
{{/each}}

ATTIC ASSESSMENT:
  Accessible:         {{attic_accessible}}
  Decking:            {{decking_condition}}
  Insulation:         {{insulation_condition}}
  Moisture Stains:    {{stain_count}} locations
  Ventilation:        {{ventilation_status}}

THERMAL IMAGING FINDINGS:
  Anomalies Detected: {{anomaly_count}}
  {{#each thermal_anomalies}}
  Location: {{location}} — {{temperature_delta_f}}F delta ({{interpretation}})
  {{/each}}

================================================================================
                        SECTION 6: CODE COMPLIANCE
================================================================================

JURISDICTION: {{municipality}}
Adopted Codes: IRC {{irc_year}}, IBC {{ibc_year}}, IECC {{iecc_year}}

CODE UPGRADES TRIGGERED:
{{#each code_upgrades}}
  {{code_reference}}: {{requirement}}
    Trigger: {{trigger}}
    Applicable: {{applicable}}
    Justification: {{justification}}
{{/each}}

ORDINANCE & LAW NOTE: Code upgrade items may be covered under the Ordinance
or Law endorsement at {{ol_percentage}}% of Coverage A limit.

================================================================================
                    SECTION 7: RECOMMENDED SCOPE
================================================================================

ROOF:
  Action:     {{roof_action}}
  Squares:    {{roof_squares}}
  Material:   {{roof_material_spec}}
  Code Items: {{roof_code_items}}

EXTERIOR:
  Action:     {{exterior_action}}
  SF:         {{exterior_sf}}
  Elevations: {{affected_elevations}}

INTERIOR:
  Action:     {{interior_action}}
  Rooms:      {{affected_rooms_count}}
  Duration:   {{mitigation_days}} days mitigation

ADDITIONAL ITEMS:
{{#each additional_items}}
  • {{item}}: ${{cost}} — {{justification}}
{{/each}}

================================================================================
                    SECTION 8: INSPECTOR CERTIFICATION
================================================================================

I certify that I personally inspected this property on {{inspection_date}}.
This report contains my true and accurate findings. I have no financial
interest in the outcome. My compensation is not contingent on the scope
of repairs.

Inspector:      {{inspector_name}}
License:        {{license_number}}
Haag Cert:      {{haag_cert}}
Date:           {{signature_date}}
Signature:      _________________________________

================================================================================
                    CONFIDENTIAL — WORK PRODUCT
================================================================================

This report is confidential work product. Unauthorized disclosure is
prohibited. Contact ClaimEdge LLC for inquiries.
================================================================================
```
