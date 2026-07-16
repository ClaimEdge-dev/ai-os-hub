## Error Handling

| Error Condition | Detection Method | Resolution Steps | Documentation Requirements | Escalation Path |
|-----------------|-----------------|------------------|---------------------------|-----------------|
| **EH-01: Property Inaccessible** | Inspector arrives at property; locked gate, no answer at door, wrong address | 1. Contact policyholder via phone (3 attempts, 10 min apart) 2. Contact ClaimEdge office for alternate contact info 3. If still no access, document attempt with timestamped photo of property 4. Reschedule within 48 hours 5. Notify carrier of delay if statutory deadline approaching | Timestamped photo of property front, call log with times, email/SMS to policyholder, rescheduled date in claim file | Escalate to Robert Krapil if 2nd attempt also fails or if carrier deadline < 5 days |
| **EH-02: Weather Conditions Unsafe** | Pre-inspection weather check or on-site observation: lightning within 5 miles, sustained winds >25 mph, ice on roof, temperature >95F with no shade | 1. Do NOT access roof under unsafe conditions 2. Document weather conditions with timestamp and source 3. Complete ground-level inspection only if safe 4. Schedule return visit for roof access 5. If drone available, conduct aerial survey from ground if wind <20 mph | Weather data screenshot (NOAA/NWS), timestamp, photos of conditions, rescheduled date | Escalate if 3rd attempt fails due to weather — recommend alternate inspection method |
| **EH-03: Insufficient Photos Taken** | Photo index validation fails minimum count for one or more categories; blurry images; no scale reference; no chalk circles on damage | 1. Run gap analysis immediately after field work 2. Identify missing categories and critical photos 3. If still on-site, capture missing photos immediately 4. If already departed, schedule return visit for specific photos 5. Use drone for inaccessible areas if available | Gap analysis report, retake checklist, before/after photo comparison, reason for deficiency in file | Escalate to supervisor if return visit cost > $200 — may proceed with available photos if damage is clear |
| **EH-04: Equipment Failure** | Drone crash, moisture meter dead battery, thermal camera malfunction, camera SD card corruption, ladder damage | 1. Immediately stop using failed equipment 2. Switch to backup equipment if available 3. Document failure: equipment model, serial number, nature of failure, time 4. For drone: follow emergency procedures, recover aircraft, document crash scene 5. Complete inspection with remaining equipment 6. Schedule follow-up if critical data missing | Equipment failure report, serial number, photos of damage (if drone crash), rental receipt for backup | Robert Krapil for drone insurance claim; equipment replacement if under warranty |
| **EH-05: Evidence Tampered** | Homeowner patched roof, cleaned up debris, repaired siding before inspection; evidence of recent work | 1. Document current condition thoroughly — may still show repair marks, new materials, color mismatch 2. Interview policyholder: when was repair done, who did it, why 3. Photograph any signs of recent work (new shingles, fresh caulk, tool marks) 4. Check for permits — unauthorized repair may violate policy conditions 5. Interview neighbors for photos of pre-repair damage 6. Request any photos policyholder took of original damage | Interview notes with timestamps, photos of repair work, permit search results, neighbor statements, policyholder photos if available | Escalate to Robert Krapil immediately — potential coverage issue under policyholder's duty to protect property |
| **EH-06: Hazardous Materials Discovered** | Asbestos siding, lead paint, vermiculite insulation, structural instability, exposed electrical, gas leak | 1. STOP WORK IMMEDIATELY in affected area 2. Evacuate if gas leak or structural collapse risk 3. Notify property owner of hazard 4. Do NOT disturb asbestos or lead materials 5. Document hazard with photos from safe distance 6. Recommend certified abatement contractor 7. Note hazard in report with safety warnings 8. Update PPE requirements for return visit | Hazard photos, safety data sheet if available, recommendation letter for certified testing, incident report | Robert Krapil for carrier notification; refer to claimedge-material-hazards skill for full assessment |
| **EH-07: Client Disputes Findings** | Policyholder disagrees with damage assessment severity, scope recommendation, or cause of loss | 1. Listen to client's concerns without argument 2. Review findings together — show photos, explain Haag classification 3. Document client's specific objections verbatim 4. Offer to re-inspect specific areas of concern 5. Note dispute in field notes with client statements 6. Do NOT alter findings — report what was observed 7. Escalate to supervisor before report finalization | Client statement verbatim, photos reviewed together, re-inspection results if performed, email summary to client | Robert Krapil — may involve attorney if client threatens complaint or if dispute affects coverage |
| **EH-08: Carrier Adjuster Present** | Carrier adjuster arrives on-site during ClaimEdge inspection | 1. Remain professional at all times 2. Do NOT share preliminary findings or opinions with adjuster 3. Coordinate schedules to avoid interference — separate roof access if possible 4. Document adjuster's name, company, actions observed 5. Do NOT allow adjuster to influence inspection methodology 6. If adjuster requests joint inspection, defer to policyholder's attorney 7. Note dual inspection in field notes | Adjuster name and company, time of arrival, actions observed, any statements made, photos of adjuster's activities (if client consents) | Robert Krapil immediately — dual inspection requires legal strategy coordination |

## Integration Points

| Direction | Skill Name | Integration Type | Data Flow | Trigger Condition |
|-----------|-----------|-----------------|-----------|-------------------|
| **Upstream** | `claimedge__intake__client-intake-suite__v1` | Data Input | Client name, property address, claim number, carrier info, policy number, date of loss | Pre-Inspection Planner receives client and claim data from intake output |
| **Upstream** | `claimedge__policy__coverage-review__v1` | Data Input | Coverage limits, O&L endorsement status, deductible, policy period, exclusions | Pre-Inspection Planner loads policy data to inform inspection scope and code upgrade documentation |
| **Upstream** | `claimedge__weather-researcher` | Data Input | NOAA storm verification, hail size, wind speed, storm track, NWS warnings | Pre-Inspection Planner pulls verified weather data to support damage causation arguments |
| **Upstream** | `claimedge__code-compliance__municipal-toolkit` | Data Input | Adopted IRC/IBC/IECC versions, permit requirements, building department contacts | Pre-Inspection Planner queries jurisdiction data for code compliance framework |
| **Downstream** | `claimedge__estimate-support__supplement-builder` | Data Output | Complete field evidence, damage counts, Haag classifications, photo references, code upgrade triggers | Field Evidence Collector output feeds directly into Xactimate supplement line item generation |
| **Downstream** | `claimedge__carrier-comms__supplement-letter-writer` | Data Output | Field report sections, photo index, code compliance analysis, recommended scope | Field Report Generator output is incorporated into carrier dispute and supplement correspondence |
| **Downstream** | `claimedge__document-assembly__proof-of-loss-generator` | Data Output | Photo evidence, moisture readings, damage assessments, inspector certification | Field Report and Photo Index serve as exhibits for Proof of Loss assembly |
| **Downstream** | `claimedge__negotiation-support__appraisal-prep` | Data Output | All inspection findings, code analysis, photo evidence | Complete report package used for appraisal preparation and umpire presentations |
| **Downstream** | `claimedge__litigation-support__expert-testimony` | Data Output | Inspector qualifications, methodology, findings, chain of custody | Inspector may be deposed; report serves as expert witness foundation |
| **Parallel** | `claimedge-material-hazards` | Cross-Reference | Hazardous material identification, asbestos risk assessment, abatement requirements | Triggered when EH-06 (hazardous materials) is detected during inspection |
| **External** | CompanyCam API | Photo Sync | Photo uploads, project creation, geo-tagging, timestamp verification | Photo Documentation Manager syncs to CompanyCam if client uses platform |
| **External** | NOAA / NWS | Weather Data | Storm event verification, hail size reports, wind speed data | Pre-Inspection Planner queries NOAA Storm Events Database |
| **External** | Municipal Building Dept | Permit Data | Permit requirements, adopted code versions, fee schedules | Pre-Inspection Planner researches jurisdiction before inspection |
| **External** | FAA LAANC System | Drone Authorization | Airspace authorization, altitude limits, time windows | Drone Survey Integrator requests LAANC authorization through UAS Facility Maps |
| **External** | DuPage County GIS / Cook County Assessor | Property Data | Year built, square footage, permit history, property characteristics | Pre-Inspection Planner queries county records for property profile |

## Related Skills

| Relationship | Skill Name | Purpose | When to Reference |
|--------------|-----------|---------|-------------------|
| **Parent** | `robert-master-os` | Master orchestration | Session initialization, context recovery |
| **Prerequisite** | `claimedge__intake__client-intake-suite__v1` | Client intake | Before any inspection — provides client data, claim context |
| **Prerequisite** | `claimedge__policy__coverage-review__v1` | Policy review | Before inspection — informs coverage limits, O&L status, exclusions |
| **Cross-Reference** | `claimedge-material-hazards` | Hazardous materials | During inspection if asbestos, lead, or other hazards discovered |
| **Cross-Reference** | `claimedge__weather-researcher` | Weather verification | Pre-inspection — storm data for causation arguments |
| **Downstream** | `claimedge__estimate-support__supplement-builder` | Supplement generation | After inspection — field evidence drives Xactimate line items |
| **Downstream** | `claimedge__carrier-comms__supplement-letter-writer` | Carrier correspondence | After inspection — report sections used in carrier letters |
| **Downstream** | `claimedge__document-assembly__proof-of-loss-generator` | POL assembly | After inspection — evidence packaged for formal claim submission |
| **Downstream** | `claimedge__negotiation-support__appraisal-prep` | Appraisal support | After inspection — complete package for appraisal panel |
| **Downstream** | `claimedge__litigation-support__expert-testimony` | Expert witness | If claim proceeds to litigation — inspector may testify |
| **Downstream** | `claimedge__code-compliance__municipal-toolkit` | Code compliance | During inspection — specific code section verification |

## Quality Assurance Checklist

Before any field report is delivered, the following must be verified:

- [ ] All 10 report sections present and complete
- [ ] Executive summary accurately reflects findings
- [ ] Every slope/elevation documented with photos
- [ ] Haag classification applied to all damaged slopes
- [ ] Test square results included for each slope
- [ ] Moisture readings within calibration date (Function 4)
- [ ] Photo index matches actual photo count
- [ ] GPS coordinates present on all exterior photos
- [ ] Inspector certification block complete with license number
- [ ] Confidentiality notice and statutory citations included
- [ ] Code upgrade triggers verified against jurisdiction's adopted codes
- [ ] Chain of custody statement included
- [ ] Report classification marked (Work Product / Attorney-Client)
- [ ] No PII exposed (SSN, bank accounts, medical information)
- [ ] Spell check and grammar review complete
- [ ] Client/attorney review copy delivered within turnaround window
