---
skill_id: claimedge__inspection__field-evidence__v1
name: ClaimEdge Inspection & Field Evidence
version: 1.0.0
author: ClaimEdge Technical Writing Team
domain: insurance-claims
subdomain: property-damage-inspection
risk_level: high
review_gate: supervisor-review-required
status: production-ready
last_updated: "[CURRENT_DATE]"
compliance_frameworks:
  - IRC 2021
  - IBC 2021
  - IECC 2021
  - IEBC 2021
  - Illinois Compiled Statutes 215 ILCS 5/154.6
  - Illinois Compiled Statutes 215 ILCS 5/155
  - FAA Part 107 (14 CFR Part 107)
  - Haag Engineering Damage Assessment Protocols
tags:
  - property-inspection
  - field-evidence
  - photo-documentation
  - hail-damage
  - wind-damage
  - moisture-mapping
  - drone-survey
  - building-code-compliance
  - illinois-statutes
  - carrier-ready
---

# ClaimEdge Inspection & Field Evidence

## Description

The **ClaimEdge Inspection & Field Evidence** skill provides a comprehensive, end-to-end technical framework for conducting property damage inspections, documenting field evidence, and generating carrier-ready inspection reports that comply with Illinois insurance statutes, Haag Engineering damage assessment protocols, and applicable building codes (IRC 2021, IBC 2021, IECC 2021, IEBC 2021). This skill is designed for public adjusters, field inspectors, and claims professionals who need to produce legally defensible, technically rigorous documentation for residential and commercial property claims.

The skill encompasses six integrated functions that guide the inspector from pre-inspection planning through final report generation:

1. **Pre-Inspection Planner** — Property intelligence gathering, weather verification, jurisdiction research, equipment preparation, and inspection strategy development.
2. **Field Evidence Collector** — Systematic exterior documentation including roof, siding, gutter, window, and accessory damage assessment using Haag Engineering classification protocols.
3. **Photo Documentation Manager** — CompanyCam-compatible photo indexing with CE-PH-### naming convention, geo-tagging, metadata capture, gap analysis, and minimum standard validation.
4. **Interior & Moisture Inspector** — Interior room-by-room assessment, moisture mapping with Protimeter Surveymaster readings, thermal imaging analysis with FLIR C5, attic inspection, and mold damage assessment.
5. **Drone Survey Integrator** — FAA Part 107 compliant drone operations, 10-waypoint flight planning, LAANC authorization workflows, aerial damage documentation, and risk assessment.
6. **Field Report Generator** — Complete carrier-ready inspection report with executive summary, damage findings, code compliance analysis, recommended scope of repairs, photo tables, and inspector certification.

All outputs use structured JSON schemas suitable for downstream system integration, and the skill includes three Mustache templates for rapid report generation, three detailed workflow examples (Residential Hail, Commercial Wind, Residential Water), and eight standardized error conditions for quality assurance.

## Domain

**Primary Domain:** Independent Insurance Claims Inspection & Consulting
**Legal Entity:** ClaimEdge LLC
**Service Area:** Illinois (primary), Indiana (secondary)
**Property Types:** Single-family residential, multi-family residential, commercial, industrial
**Peril Types:** Hail, Wind, Hurricane, Flood, Fire, Water Damage, Tornado, Ice/Snow
**Claim Types:** First-party property claims, appraisal, supplement, dispute resolution

## Risk Level

**HIGH** — Field inspections form the evidentiary foundation for all insurance claims. Errors in documentation, missed damage, or improper classification can destroy claim viability. Consequences include:

- **Financial:** Inadequate documentation leads to denied or underpaid claims
- **Legal:** Incomplete evidence weakens bad faith litigation under 215 ILCS 5/155
- **Professional:** Inspector certification and reputation depend on report quality
- **Liability:** Safety hazards during inspection create exposure for inspector and firm

## Review Gate

**SUPERVISOR REVIEW REQUIRED** — All field inspection reports must be reviewed by Robert Krapil or designated supervisor before submission to carrier. Review checklist:

- [ ] All required photos present and properly labeled
- [ ] Haag damage classification applied consistently
- [ ] Moisture readings within calibration date
- [ ] Drone flight log matches FAA Part 107 requirements
- [ ] Inspector certification block complete and current
- [ ] Code compliance assessment accurate for jurisdiction
- [ ] No PII in report (redact SSN, bank accounts, medical info)
- [ ] Report classification marked (Work Product / Attorney-Client Privileged)
- [ ] Chain of custody statement included

## Trigger

Activate this skill when user provides any of the following:

- "I need to inspect a property"
- "Plan an inspection for [address]"
- "Document hail damage on [roof type]"
- "Photo log for roof inspection"
- "Field report template"
- "Prepare for adjuster meeting"
- "Inspection checklist"
- "CompanyCam setup for [address]"
- "Drone survey needed"
- "Moisture mapping"
- "Interior water damage assessment"
- "Attic inspection findings"
- "Thermal imaging analysis"
- "Complete inspection report"

**Required trigger data:**
- `property_address` (string): Full street address
- `peril_type` (enum): hail | wind | hurricane | flood | fire | water | tornado | ice_snow

**Optional trigger data:**
- `carrier` (string): Insurance carrier name
- `claim_number` (string): Carrier-assigned claim number
- `date_of_loss` (string): ISO 8601 date
- `property_type` (enum): residential | commercial | industrial

## Input Schema

### Function 1: Pre-Inspection Planner

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `property_address` | string | Yes | Full street address including ZIP |
| `property_type` | enum | Yes | residential_single_family, residential_multi_family, commercial, industrial, agricultural |
| `peril_type` | enum | Yes | hail, wind, hurricane, flood, fire, water, tornado, ice_snow, multi |
| `carrier` | string | No | Insurance carrier name |
| `claim_number` | string | No | Carrier-assigned claim number |
| `date_of_loss` | string | No | ISO 8601 date string |
| `prior_inspection` | boolean | No | Has carrier adjuster already inspected? |
| `access_instructions` | string | No | Gate codes, pet warnings, contact person |
| `special_equipment` | array | No | drone, moisture_meter, thermal_camera, ladder_40ft, core_cutter, manlift |
| `weather_verified` | boolean | No | Has storm event been verified with NOAA? |
| `client_name` | string | No | Property owner name |
| `client_phone` | string | No | Property owner phone |
| `inspector_name` | string | No | Assigned inspector |
| `inspection_date` | string | No | Scheduled inspection date |
| `building_age` | number | No | Year built or approximate age |
| `stories` | number | No | Number of stories |
| `roof_type` | string | No | Known roof type |
| `siding_type` | string | No | Known siding type |

### Function 2: Field Evidence Collector

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `inspection_photos` | array | Yes | Photo metadata with IDs, slopes/elevations, damage types |
| `roof_data` | object | Yes | Slopes, materials, age, test square results |
| `siding_data` | object | Yes | Elevations, materials, damage by elevation |
| `accessory_data` | object | Yes | Gutters, windows, fences, HVAC, etc. |
| `peril_type` | enum | Yes | hail, wind, hurricane, flood, fire, water, tornado, ice_snow |
| `date_of_loss` | string | Yes | ISO 8601 date |
| `property_age` | number | Yes | Years since construction |
| `weather_conditions` | object | No | Temperature, wind, precipitation at time of inspection |
| `equipment_used` | array | No | List of tools used during inspection |

### Function 3: Photo Documentation Manager

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `photos` | array | Yes | Each with id, filename, timestamp, gps_coords, description, tags |
| `project_type` | enum | Yes | residential, commercial |
| `systems_photographed` | array | Yes | roof, siding, windows, gutters, fence, hvac, interior, attic, drone |
| `companycam_project_url` | string | No | CompanyCam project link |
| `naming_convention` | string | No | Preferred naming scheme (default: CE-PH-###) |
| `minimum_counts` | object | No | Override default minimum photo requirements |

### Function 4: Interior & Moisture Inspector

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `interior_rooms` | array | Yes | Room names, ceiling/wall/window conditions |
| `moisture_readings` | array | Yes | Location, percentage, timestamp |
| `thermal_images` | array | No | Location, anomaly description |
| `attic_access` | boolean | Yes | Whether attic was inspected |
| `attic_conditions` | object | No | Decking stains, insulation condition, ventilation, mold |
| `odor_detected` | boolean | No | Musty or mold smell |
| `prior_water_damage` | boolean | No | Known history of water damage |
| `basement_access` | boolean | No | Whether basement was inspected |
| `mold_visible` | boolean | No | Visible mold observed |
| `hvac_operational` | boolean | No | HVAC system operational status |

### Function 5: Drone Survey Integrator

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `property_address` | string | Yes | Full street address |
| `roof_complexity` | enum | Yes | simple_gable, complex_hip, flat_mixed, multi_level |
| `flight_restrictions` | array | Yes | airport_proximity, no_fly_zone, height_limit, weather |
| `pilot_certification` | string | Yes | FAA Part 107 certificate number |
| `drone_model` | string | Yes | Equipment used (e.g., DJI Mavic 3 Enterprise) |
| `flight_date` | string | Yes | ISO 8601 date |
| `weather_conditions` | object | Yes | Wind speed, visibility, ceiling |
| `lanc_approved` | boolean | No | LAANC authorization obtained |
| `insurance_certificate` | string | No | Liability insurance certificate number |

### Function 6: Field Report Generator

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pre_inspection_plan` | object | Yes | Output from Function 1 |
| `field_evidence` | object | Yes | Output from Function 2 |
| `photo_documentation` | object | Yes | Output from Function 3 |
| `interior_moisture` | object | Yes | Output from Function 4 |
| `drone_survey` | object | No | Output from Function 5 (if drone used) |
| `inspector_info` | object | Yes | Name, Haag cert #, IL license #, company |
| `report_date` | string | Yes | ISO 8601 date |
| `client_info` | object | Yes | From intake skill |
| `policy_info` | object | Yes | From policy review skill |
| `confidentiality_level` | enum | No | work_product, attorney_client, standard |
