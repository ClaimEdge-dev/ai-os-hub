## Examples

### Example 1: Residential Hail Claim

**Property:** 1234 Maple Drive, Naperville, IL 60540
**Peril:** Hail, 2.5" diameter on July 12, 2026
**Carrier:** State Farm
**Roof:** Architectural asphalt shingles, GAF Timberline HDZ, 12 years old

**Function 1 — Pre-Inspection Plan Output:**

```json
{
  "plan_id": "CE-PLAN-SF-2026-12345-20260715",
  "claim_number": "SF-2026-12345",
  "property_profile": {
    "address": { "street": "1234 Maple Drive", "city": "Naperville", "state": "IL", "zip": "60540", "county": "DuPage", "jurisdiction": "City of Naperville" },
    "building_characteristics": { "property_type": "residential_single_family", "year_built": 2002, "stories_above_grade": 2, "basement_type": "full", "total_square_footage": 2850 },
    "roof_system": { "primary_covering": "architectural_asphalt", "age_years": 12, "layers": 1, "pitch_description": "medium", "condition_pre_loss": "good", "last_replacement_year": 2014 },
    "siding_system": { "primary_material": "vinyl", "age_years": 22, "condition_pre_loss": "fair" }
  },
  "peril_assessment": {
    "peril_type": "hail", "date_of_loss": "2026-07-12",
    "weather_verification": { "source": "NOAA", "verification_status": "confirmed", "noaa_event_id": "20260712-IL-DUPAGE-HAIL-001", "hail_size_inches": 2.5, "hail_size_verified": true, "wind_speed_mph": 45, "precipitation_type": "hail", "nws_warning_type": "severe_thunderstorm" },
    "damage_mechanism": "Large hail stones (2.5") impacted roof surfaces at terminal velocity, causing granule loss, fracturing, and bruising to asphalt shingles. Wind-driven hail increased impact angles on west and north-facing slopes.",
    "expected_damage_patterns": ["Granule loss on all slopes with exposed asphalt matting", "Bruising and fracturing on west and north slopes", "Siding impact marks on west elevation"]
  },
  "code_compliance_framework": {
    "adopted_codes": { "irc_version": "2021", "ibc_version": "2021", "iecc_version": "2021" },
    "jurisdiction": { "authority_having_jurisdiction": "City of Naperville", "permit_required_reroof": true, "permit_required_siding": true, "permit_fees_estimate": 350.00 },
    "applicable_code_sections": [
      { "code_reference": "IRC R905.2.1", "requirement": "Spaced sheathing must be replaced with solid decking", "triggered_by_loss": true },
      { "code_reference": "IRC R905.1.2", "requirement": "Ice barrier at eaves (2 rows Illinois)", "triggered_by_loss": true },
      { "code_reference": "IRC R905.2.8.5", "requirement": "Drip edge required", "triggered_by_loss": true }
    ]
  },
  "inspection_strategy": { "inspection_type": "initial", "estimated_duration_hours": 4, "inspector_count": 1, "equipment_checklist": { "mandatory": ["Camera 12MP+", "Ladder 28ft", "Tape measure", "Chalk", "Flashlight", "Safety gear", "Tablet"], "conditional": [{"item": "Moisture meter", "required_when": "Interior inspection"}, {"item": "Drone", "required_when": "Steep pitch or limited access"}] }, "photo_requirements": { "minimum_total_photos": 68 } },
  "risk_flags": [ { "flag_type": "CODE_UPGRADE_REQUIRED", "severity": "medium", "description": "Single-layer roof with potential spaced decking requires solid sheathing per IRC R905.2.1", "recommended_action": "Document decking condition from attic and prepare code upgrade argument" } ]
}
```

**Function 2 — Field Evidence Collection:**

Inspector arrived at 9:00 AM. Weather: 78F, clear, wind 5 mph. Roof accessed via 28 ft extension ladder. Safety harness deployed.

Test Square Results:
- Front Slope (South): 14 hail hits per TS, Haag = M (Minor)
- Rear Slope (North): 22 hail hits per TS, Haag = MO (Moderate) — granule loss 40%
- Left Slope (East): 8 hail hits per TS, Haag = M (Minor)
- Right Slope (West): 31 hail hits per TS, Haag = MA (Major) — bruising, fracturing, exposed asphalt

Roof replacement recommended: 28.5 squares, all slopes. Code upgrades: solid decking (spaced found), ice barrier (2 rows), drip edge.

**Function 3 — Photo Documentation:**

68 photos captured, all GPS-tagged. CE-PH-001 through CE-PH-068. CompanyCam sync: complete. Category minimums all met.

**Function 6 — Field Report:**

Complete report generated using Template A (Residential Hail). 10 sections. Inspector certification block signed. Delivered to client within 24 hours.

---

### Example 2: Commercial Wind Claim

**Property:** 5678 Industrial Blvd, Des Plaines, IL 60016
**Peril:** Wind, 78 mph gusts on June 3, 2026
**Carrier:** Liberty Mutual
**Building:** TPO flat roof with metal parapet, 45,000 sq ft warehouse

**Key Inspection Details:**

Function 1 identified need for drone survey (flat roof, 18 ft parapet height, no safe ladder access). Function 5 conducted drone flight with 12 waypoints, max altitude 150 ft AGL, 34 aerial photos captured.

Field Evidence (Function 2):
- Section A (East 15,000 SF): TPO membrane uplifted 2,400 SF, 14 seam separations, ballast displaced
- Section B (West 15,000 SF): 8 fastener back-outs, membrane creasing, 1 puncture
- Section C (Center 15,000 SF): Minimal damage — isolated uplift at HVAC curb
- Parapet: Coping displaced 40 LF, wall panel damage north elevation
- HVAC: 3 of 8 condensers with fin damage 15-30%

Interior (Function 4): Moisture detected in east section — 3 elevated readings (16-18%), 1 saturated (23%). Thermal imaging confirmed cold spots at membrane seams. No visible mold. Attic: N/A (flat roof structure).

Report generated using Template B (Commercial Wind). 8 sections. Drone FAA compliance verified.

---

### Example 3: Residential Water Claim

**Property:** 901 Oak Street, Oak Lawn, IL 60453
**Peril:** Ice dam water intrusion, February 2026
**Carrier:** Allstate
**Issue:** Ice dams caused water intrusion through roof edge, staining ceilings and walls

**Key Inspection Details:**

Function 1 identified interior inspection as primary scope. Attic access confirmed. Thermal imaging needed.

Interior & Moisture (Function 4):
- Kitchen: Ceiling stain 4 SF, moisture reading 18% (elevated), thermal cold spot -12F delta at north wall/ceiling junction
- Living Room: Wall swelling, paint peeling, moisture 21% (saturated) on north wall
- Master Bedroom: Ceiling stain 2 SF, moisture 16% (elevated)
- Attic: Decking stains along north eave 8 LF, insulation compressed and wet, soffit vents blocked, inadequate intake ventilation

Highest reading: 21% at Living Room north wall (saturated — material removal required).

Mold: Visible mold observed in Living Room — black patches, spotty extent, musty odor. Recommended air and surface sampling.

Thermal Imaging (FLIR C5): 4 anomalies detected, all at roof edge/decking interface. Confirmed ice dam heat loss pattern.

Report generated using Template C (Residential Water). 10 sections. IICRC S500/S520 standards referenced. Drying protocol: 5 days with 2 dehus, 6 air movers, containment in Living Room.
