### Template C: Residential Water Damage Field Inspection Report

```
================================================================================
                    CLAIMEDGE LLC
         FIELD INSPECTION REPORT — RESIDENTIAL WATER DAMAGE
================================================================================

REPORT CONTROL INFORMATION
--------------------------
Report ID:          {{report_id}}
Claim Number:       {{claim_number}}
Date of Loss:       {{date_of_loss}}
Inspection Date:    {{inspection_date}}
Report Date:        {{report_date}}

PROPERTY INFORMATION
--------------------
Insured:            {{client_name}}
Address:            {{street_address}}
                    {{city}}, {{state}} {{zip}}
Property Type:      Single-Family Residential
Year Built:         {{year_built}}
Stories:            {{stories}}
Sq Ft:              {{square_footage}}

INSPECTION DETAILS
------------------
Inspector:          {{inspector_name}}
License:            {{license_number}}
Scope:              Interior + Moisture Mapping + Attic
Moisture Meter:     {{meter_model}} (S/N: {{meter_serial}}, Cal: {{cal_date}})
Thermal Imager:     {{thermal_model}} (S/N: {{thermal_serial}})
Interior Temp:      {{temp_f}}F
Relative Humidity:  {{rh_pct}}%

================================================================================
                         SECTION 1: EXECUTIVE SUMMARY
================================================================================

On {{inspection_date}}, I conducted a comprehensive interior water damage
inspection of the subject property. The loss occurred on {{date_of_loss}}
due to {{water_source}}.

KEY FINDINGS:
{{#each key_findings}}
  • {{this}}
{{/each}}

MOISTURE SUMMARY:
  Total Readings:     {{total_readings}}
  Normal (<15%):      {{normal_count}}
  Elevated (15-20%):  {{elevated_count}}
  Saturated (>20%):   {{saturated_count}}
  Highest Reading:    {{highest_reading_pct}}% at {{highest_location}}

MOLD ASSESSMENT:
  Visible Mold:       {{mold_visible}}
  Locations:          {{mold_locations}}
  Recommended Testing: {{mold_testing}}

SCOPE RECOMMENDATION:
  Interior Remediation:     {{interior_action}}
  Affected Rooms:           {{affected_rooms_count}}
  Mitigation Duration:      {{mitigation_days}} days
  Attic Work Required:      {{attic_work}}
  Health/Safety Concerns:   {{safety_concerns_count}}

================================================================================
                      SECTION 2: INSPECTION METHODOLOGY
================================================================================

This water damage inspection included:

  • Interior walk-through with room-by-room assessment
  • Moisture mapping using Protimeter Surveymaster (pin and non-invasive modes)
  • Thermal imaging with FLIR C5 to detect hidden moisture
  • Attic inspection for source identification and decking assessment
  • Moisture reading baseline establishment in unaffected areas
  • Photo documentation with CE-PH-### numbering and GPS tagging

Moisture Reading Classifications:
  Normal:     < 15% (dry — no action needed)
  Elevated:   15-20% (moist — drying required)
  Saturated:  > 20% (wet — material removal likely required)

Standards: IICRC S500 (Water Damage Restoration), IICRC S520 (Mold Remediation),
IRC 2021, Illinois Insurance Code 215 ILCS 5/154.6

================================================================================
                   SECTION 3: MOISTURE MAPPING RESULTS
================================================================================

MOISTURE READING LOG:
Room/Location              Reading   Baseline   Delta    Status
----------------------------------------------------------------
{{#each moisture_readings}}
{{location_pad}}   {{reading_pct}}%      {{baseline_pct}}%        {{delta}}      {{status}}
{{/each}}

SUMMARY BY ROOM:
{{#each room_summaries}}
{{room_name}}:
  Readings Taken:     {{reading_count}}
  Range:              {{min_reading}}% — {{max_reading}}%
  Average:            {{avg_reading}}%
  Status:             {{overall_status}}
  Photo Refs:         {{photo_refs}}
{{/each}}

================================================================================
                     SECTION 4: ROOM-BY-ROOM FINDINGS
================================================================================

{{#each rooms}}
{{room_name}} ({{level}} Floor)
{{line}}

Ceiling Condition:
  {{ceiling_description}}
  {{#if ceiling_damage_type}}Damage Type: {{ceiling_damage_type}}{{/if}}
  {{#if ceiling_affected_sf}}Affected Area: {{ceiling_affected_sf}} SF{{/if}}

Wall Condition:
  {{wall_description}}
  {{#if wall_damage_type}}Damage Type: {{wall_damage_type}}{{/if}}
  {{#if wall_affected_sf}}Affected Area: {{wall_affected_sf}} SF{{/if}}

Floor Condition:
  {{floor_description}}
  {{#if floor_damage_type}}Damage Type: {{floor_damage_type}}{{/if}}

Moisture Readings:
{{#each room_readings}}
  {{location}}: {{reading_pct}}% ({{classification}})
{{/each}}

{{#if thermal_anomalies}}
Thermal Anomalies:
{{#each thermal_anomalies}}
  {{location}}: {{temperature_delta_f}}F delta — {{interpretation}}
{{/each}}
{{/if}}

{{#if mold_visible}}
MOLD FINDINGS:
  Location:       {{mold_location}}
  Color:          {{mold_color}}
  Extent:         {{mold_extent}}
  Musty Odor:     {{musty_odor}}
  Testing Rec:    {{mold_testing_recommendation}}
{{/if}}

Recommended Action: {{recommended_action}}
Photo References: {{photo_refs}}

{{/each}}

================================================================================
                        SECTION 5: ATTIC FINDINGS
================================================================================

Attic Accessible:   {{attic_accessible}}
{{#if attic_accessible}}
Access Method:      {{access_method}}
Approximate SF:     {{attic_sf}}

DECKING CONDITION:
  Material:         {{decking_material}}
  Water Stains:     {{water_stains_observed}}
  {{#if stain_description}}Stain Description: {{stain_description}}{{/if}}
  Soft Spots:       {{soft_spots_count}}
  Delamination:     {{decking_delamination}}

INSULATION CONDITION:
  Type:             {{insulation_type}}
  Depth:            {{insulation_depth}} inches
  R-Value Est:      {{r_value}}
  Water Damage:     {{insulation_water_damage}}
  Settlement:       {{insulation_settlement}}

VENTILATION:
  Soffit Vents:     {{soffit_vent_count}} ({{soffit_condition}})
  Baffles Present:  {{baffles_present}}
  Ridge Vent:       {{ridge_vent_ft}} LF
  Box Vents:        {{box_vent_count}}
  Exhaust Condition: {{exhaust_condition}}

STRUCTURAL:
  Rafters:          {{rafter_condition}}
  Trusses:          {{truss_condition}}

MOLD:
  Visible:          {{attic_mold_visible}}
  Location:         {{attic_mold_location}}
  Extent:           {{attic_mold_extent}}
  Ventilation Adequacy: {{ventilation_adequacy}}
{{/if}}

================================================================================
                   SECTION 6: THERMAL IMAGING FINDINGS
================================================================================

Equipment: {{thermal_model}}
Conditions: Temp {{temp_f}}F, RH {{rh_pct}}%, Dew Point {{dew_point}}F

{{#each thermal_anomalies}}
Location:           {{location}}
Anomaly Type:       {{anomaly_type}}
Temperature Delta:  {{temperature_delta_f}}F
Interpretation:     {{interpretation}}
Photo Reference:    {{photo_ref}}
Recommended Action: {{action}}

{{/each}}

================================================================================
                     SECTION 7: HEALTH & SAFETY ASSESSMENT
================================================================================

{{#each safety_concerns}}
Concern:    {{concern}}
Severity:   {{severity}}
Action:     {{recommended_action}}
{{/each}}

MOLD HEALTH RISKS:
  Visible mold was {{#if mold_visible}}observed{{else}}not observed{{/if}} during
  this inspection. {{#if mold_testing_recommended}}Air and/or surface sampling
  is recommended to determine mold species and spore counts.{{/if}}

  Occupant Precautions:
    {{#if mold_visible}}• Limit access to affected areas
    • Use N95 respirators if entering affected rooms
    • Run HEPA air filtration if available{{else}}• No specific precautions
      required at this time{{/if}}

================================================================================
                        SECTION 8: CODE COMPLIANCE
================================================================================

{{#each code_upgrades}}
{{code_reference}}: {{requirement}}
  Applicable: {{applicable}}
  {{#if applicable}}Justification: {{justification}}{{/if}}
{{/each}}

================================================================================
                     SECTION 9: RECOMMENDED SCOPE
================================================================================

IMMEDIATE ACTIONS (First 48 Hours):
  • {{immediate_action_1}}
  • {{immediate_action_2}}
  • Deploy dehumidifiers: {{dehu_count}} units
  • Deploy air movers: {{air_mover_count}} units

DRYING PROTOCOL:
  Estimated Duration: {{drying_days}} days
  Containment Required: {{containment_needed}}
  Daily Moisture Monitoring: Yes

MATERIAL REMOVAL:
{{#each removal_items}}
  • {{material}} in {{location}} — {{sf}} SF
{{/each}}

MOLD REMEDIATION:
  {{#if mold_remediation_needed}}
  Required: Yes
  Scope: {{mold_remediation_scope}}
  Containment: {{mold_containment}}
  Contractor Requirements: IICRC S520 certified
  {{else}}
  Required: No
  {{/if}}

REBUILD SCOPE:
{{#each rebuild_items}}
  • {{item}} in {{location}} — {{sf}} SF
{{/each}}

ATTIC WORK:
  {{#if attic_work_needed}}
  Decking Repair: {{decking_repair_sf}} SF
  Insulation Replacement: {{insulation_replace_sf}} SF
  Ventilation Upgrades: {{ventilation_upgrades}}
  {{else}}
  No attic work required.
  {{/if}}

================================================================================
                    SECTION 10: INSPECTOR CERTIFICATION
================================================================================

I certify that I personally inspected this property on {{inspection_date}}.
This report contains my true findings. No financial interest in outcome.

Inspector:      {{inspector_name}}
License:        {{license_number}}
Company:        ClaimEdge LLC
Date:           {{signature_date}}
Signature:      _________________________________

Contact: {{inspector_phone}} | {{inspector_email}}
================================================================================
              CONFIDENTIAL — WORK PRODUCT — CLAIMEDGE LLC
================================================================================
```
