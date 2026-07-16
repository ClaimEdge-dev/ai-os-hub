## Templates

### Template A: Residential Hail Damage Field Inspection Report

```
================================================================================
                    CLAIMEDGE LLC
          FIELD INSPECTION REPORT — RESIDENTIAL HAIL DAMAGE
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
  Year Built:       {{year_built}}
  Stories:          {{stories}}
  Square Footage:   {{square_footage}}
  Foundation:       {{foundation_type}}

INSPECTION DETAILS
------------------
Inspector:          {{inspector_name}}
License Number:     {{license_number}}
Haag Certification: {{haag_cert_number}}
Inspection Method:  {{inspection_method}}
Weather Conditions: {{weather_description}}

CARRIER INFORMATION
-------------------
Carrier:            {{carrier_name}}
Claim Number:       {{claim_number}}
Adjuster Name:      {{adjuster_name}}
Adjuster Phone:     {{adjuster_phone}}

================================================================================
                         SECTION 1: EXECUTIVE SUMMARY
================================================================================

On {{inspection_date}}, I conducted a field inspection of the subject property
located at {{street_address}} in {{city}}, {{state}}. The inspection was
performed in response to a reported {{peril_type}} loss on {{date_of_loss}}.

KEY FINDINGS:
{{#each key_findings}}
  • {{this}}
{{/each}}

OVERALL DAMAGE CLASSIFICATION: {{overall_damage_classification}}
  (C=Cosmetic, M=Minor, MO=Moderate, MA=Major, S=Severe)

SCOPE RECOMMENDATION: {{scope_recommendation}}
  Total Roof Area: {{total_squares}} squares
  Slopes Requiring Replacement: {{slopes_replacement_count}}
  Slopes Requiring Repair: {{slopes_repair_count}}
  Code Upgrades Identified: {{code_upgrades_count}}

PHOTO EVIDENCE: {{total_photo_count}} photographs captured and catalogued.

================================================================================
                      SECTION 2: INSPECTION METHODOLOGY
================================================================================

This inspection was conducted in accordance with the following standards and
protocols:

  • Haag Engineering Damage Assessment Protocols
  • IRC 2021 (International Residential Code) — Roof Assemblies, Chapter 9
  • IRC 2021 — Exterior Walls (Section R703)
  • IECC 2021 — Energy Conservation Requirements
  • Illinois Compiled Statutes 215 ILCS 5/154.6 — Claims Handling Requirements

INSPECTION METHODS EMPLOYED:
{{#each inspection_methods}}
  • {{this}}
{{/each}}

EQUIPMENT USED:
{{#each equipment_used}}
  • {{this}}
{{/each}}

SAFETY EQUIPMENT:
{{#each safety_equipment}}
  • {{this}}
{{/each}}

CHAIN OF CUSTODY:
All photographic evidence was captured using a GPS-enabled camera, timestamped,
and uploaded to secure cloud storage within 4 hours of inspection. Images are
stored in accordance with ClaimEdge LLC evidence handling procedures. Memory
cards were sealed and logged at the conclusion of the inspection.

================================================================================
                        SECTION 3: ROOF FINDINGS
================================================================================

ROOF SYSTEM DESCRIPTION:
{{roof_system_description}}

{{#each slopes}}
SLOPE: {{slope_designation}} ({{orientation}})
-----------------------------------------------
Dimensions:     {{length_ft}} ft x {{width_ft}} ft = {{squares}} squares
Pitch:          {{pitch}}
Condition Pre-Loss: {{condition_pre_loss}}

HAIL DAMAGE ASSESSMENT:
  Test Square:          10 ft x 10 ft performed
  Hail Hits per TS:     {{hail_hits_count}}
  Bruising:             {{bruising_count}}
  Fracturing:           {{fracturing_count}}
  Granule Loss:         {{granule_loss_pct}}%
  Punctures:            {{punctures_count}}
  Indentations:         {{indentations_count}}

  HAAG CLASSIFICATION:  {{haag_classification}}
  ({{classification_description}})

WIND DAMAGE ASSESSMENT:
  Uplift:               {{wind_uplift_count}}
  Creasing:             {{creasing_count}}
  Tearing:              {{tearing_count}}
  Missing Pieces:       {{missing_pieces_count}}

RECOMMENDED ACTION: {{recommended_action}}
JUSTIFICATION: {{justification}}

PHOTO REFERENCES: {{photo_references}}

{{/each}}

ROOF SUMMARY:
  Total Slopes:                   {{total_slopes}}
  Slopes with Damage:             {{slopes_with_damage}}
  Slopes Requiring Replacement:   {{slopes_replacement}}
  Slopes Requiring Repair:        {{slopes_repair}}
  Overall Classification:         {{overall_classification}}
  Functional Damage Present:      {{functional_damage}}
  Water Intrusion Risk:           {{water_intrusion_risk}}

================================================================================
                      SECTION 4: EXTERIOR FINDINGS
================================================================================

SIDING ASSESSMENT:
Primary Material: {{siding_material}}

{{#each elevations}}
{{elevation_name}} Elevation ({{compass_bearing}})
-----------------------------------------------
Square Footage:     {{sf}}
Damage Present:     {{damage_present}}

{{#if hail_damage}}
Hail Damage:
  Impact Marks:     {{impact_marks}}
  Cracking:         {{cracking}}
  Chipping:         {{chipping}}
  Description:      {{damage_description}}
{{/if}}

{{#if wind_damage}}
Wind Damage:
  Loose Panels:     {{loose_panels}}
  Missing Panels:   {{missing_panels}}
  Description:      {{wind_description}}
{{/if}}

Photo References: {{photo_refs}}
Recommended Action: {{action}}

{{/each}}

GUTTER ASSESSMENT:
Type:           {{gutter_type}}
Linear Feet:    {{gutter_linear_ft}}
Damage:         {{gutter_damage_description}}
Action:         {{gutter_action}}

WINDOW/DOOR ASSESSMENT:
{{#each damaged_windows}}
Location:       {{location}}
Damage Type:    {{damage_type}}
Description:    {{description}}
Photo:          {{photo_ref}}
{{/each}}

ACCESSORIES:
  Skylights:    {{skylight_count}} ({{skylight_damaged}} damaged)
  Chimneys:     {{chimney_count}} ({{chimney_damaged}} damaged)
  Vents:        {{vent_description}}
  Solar Panels: {{solar_count}} ({{solar_damaged}} damaged)

OUTDOOR STRUCTURES:
  Fence:        {{fence_type}}, {{fence_lf}} LF — {{fence_damage}}
  Sheds:        {{shed_count}} ({{shed_damaged}} damaged)

================================================================================
                        SECTION 5: PHOTO INDEX
================================================================================

{{#each photos}}
{{photo_id}}    {{description}}
                System: {{system}} | Slope/Elevation: {{slope}}
                Damage Type: {{damage_type}} | Scale Ref: {{scale_ref}}

{{/each}}

================================================================================
                    SECTION 6: INSPECTOR CERTIFICATION
================================================================================

I hereby certify that I personally inspected the subject property on the date
stated above. This report contains my true and accurate findings based on my
professional inspection. I have no financial interest in the outcome of this
claim. My compensation is not contingent upon the amount of loss or scope of
repairs determined.

Inspector:          {{inspector_name}}
Title:              Senior Field Inspector
Company:            ClaimEdge LLC
License:            {{license_number}}
Haag Cert:          {{haag_cert_number}}
Date:               {{signature_date}}

Signature:          _________________________________

Contact:
  Phone:            {{inspector_phone}}
  Email:            {{inspector_email}}
  Company Address:  ClaimEdge LLC, Chicagoland, IL

================================================================================
                      CONFIDENTIALITY NOTICE
================================================================================

THIS REPORT IS CONFIDENTIAL AND PROPRIETARY. This document contains work
product prepared in anticipation of litigation or for claims resolution
purposes. Unauthorized disclosure, distribution, or reproduction is strictly
prohibited. All photographic evidence is the property of ClaimEdge LLC and is
subject to chain of custody protocols.

================================================================================
         Generated by ClaimEdge LLC Inspection & Field Evidence System v1.0
================================================================================
```
