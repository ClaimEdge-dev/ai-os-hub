## Workflow

### Function 1 Workflow: Pre-Inspection Planner

```
START
  |
  v
[RECEIVE property address + peril type from trigger]
  |
  v
[QUERY CountyGIS / County Assessor for property data]
  |-> year_built, square footage, stories, roof type, siding type
  |
  v
[VERIFY date_of_loss with NOAA Storm Events Database]
  |-> hail size, wind speed, storm track, NWS warning type
  |
  v
[RESEARCH jurisdiction building department]
  |-> adopted IRC/IBC/IECC versions, permit requirements, fees
  |
  v
[GATHER client contact info from intake skill output]
  |-> client_name, phone, email, special instructions
  |
  v
[DETERMINE inspection strategy]
  |-> roof access method, interior scope, drone need, equipment list
  |
  v
[ASSESS safety requirements]
  |-> fall protection, electrical hazards, weather window
  |
  v
[GENERATE risk flags]
  |-> carrier previously inspected, statute limitations, prior damage
  |
  v
[OUTPUT Pre-Inspection Plan JSON]
  |
  v
[NOTIFY client of inspection date/time via SMS/email]
  |
  v
[ARCHIVE plan to claim file]
  |
  v
END
```

### Function 2 Workflow: Field Evidence Collector

```
START
  |
  v
[LOAD Pre-Inspection Plan]
  |
  v
[ARRIVE on-site — confirm address, introduce to policyholder]
  |
  v
[CONDUCT exterior walk-around]
  |-> 4 elevations, overall photos, identify damage patterns
  |
  v
[ACCESS ROOF via ladder, drone, or interior hatch]
  |-> Safety check, harness on, ladder secured
  |
  v
[PERFORM test squares — 10x10 ft per slope]
  |-> Chalk circles, ruler for scale, Haag classification
  |
  v
[DOCUMENT each slope]
  |-> Overview, detail damage, accessories, photo log
  |
  v
[INSPECT siding — each elevation]
  |-> Hail impacts, wind damage, separation, photo log
  |
  v
[INSPECT gutters, downspouts, accessories]
  |-> Dents, separations, damage count
  |
  v
[INSPECT windows, doors, fence, HVAC]
  |-> Each unit assessed, photo documented
  |
  v
[COMPLETE field notes]
  |-> Inspector observations, client statements, weather notes
  |
  v
[OUTPUT Field Evidence Collection JSON]
  |
  v
[TRANSFER photos to secure storage — chain of custody log]
  |
  v
END
```

### Function 3 Workflow: Photo Documentation Manager

```
START
  |
  v
[RECEIVE photo batch from Function 2]
  |
  v
[IMPORT photos to processing system]
  |-> Extract EXIF: GPS, timestamp, camera model, resolution
  |
  v
[RENAME to CE-PH-### convention]
  |-> Sequential numbering, maintain original filename in metadata
  |
  v
[ASSIGN categories per photo]
  |-> System, subsystem, damage type, Haag classification
  |
  v
[VALIDATE against minimum requirements]
  |-> Compare to category minimums, flag gaps
  |
  v
[RUN quality assessment]
  |-> Resolution, focus, lighting, scale reference, GPS
  |
  v
[PERFORM gap analysis]
  |-> Identify missing categories, recommend retakes
  |
  v
[SYNC to CompanyCam if applicable]
  |-> Upload with tags, verify sync status
  |
  v
[GENERATE Photo Documentation Index JSON]
  |
  v
[CREATE photo reference tables for report]
  |
  v
END
```

### Function 4 Workflow: Interior & Moisture Inspector

```
START
  |
  v
[RECEIVE field evidence + client authorization for interior]
  |
  v
[CONDUCT interior walk-through]
  |-> Identify affected rooms, water stains, odors
  |
  v
[PERFORM moisture mapping]
  |-> Protimeter readings at 16-20 points per affected room
  |-> Record: location, reading %, classification, timestamp
  |
  v
[CAPTURE thermal images with FLIR C5]
  |-> Cold spots, moisture patterns, insulation gaps
  |
  v
[INSPECT attic]
  |-> Decking, insulation, ventilation, mold assessment
  |
  v
[DOCUMENT mold findings if present]
  |-> Location, color, extent, odor, testing recommendations
  |
  v
[ASSESS health and safety concerns]
  |-> Structural, electrical, mold, slip hazards
  |
  v
[IDENTIFY code upgrade opportunities]
  |-> Fire separation, insulation, ventilation
  |
  v
[OUTPUT Interior & Moisture Report JSON]
  |
  v
[RECOMMEND drying protocol or mitigation if needed]
  |
  v
END
```

### Function 5 Workflow: Drone Survey Integrator

```
START
  |
  v
[VERIFY FAA Part 107 certification current]
  |-> Cert number, expiration date, flight currency
  |
  v
[CHECK airspace via B4UFLY / LAANC]
  |-> Airspace class, restrictions, authorization needed
  |
  v
[REQUEST LAANC authorization if required]
  |-> Altitude, time window, authorization number
  |
  v
[PERFORM pre-flight inspection]
  |-> 10-point checklist: aircraft, props, battery, SD, GPS, compass,
  |   firmware, weather, airspace, insurance
  |
  v
[PROGRAM flight plan]
  |-> Waypoints, altitude, overlap, pattern type
  |
  v
[CONDUCT flight — maintain VLOS]
  |-> Execute waypoints, capture photos/video, monitor hazards
  |
  v
[PERFORM post-flight procedures]
  |-> Download media, verify data integrity, battery log
  |
  v
[DOCUMENT FAA compliance]
  |-> All Part 107 requirements verified, violations logged
  |
  v
[OUTPUT Drone Survey Results JSON]
  |
  v
[TRANSFER aerial photos to photo documentation manager]
  |
  v
END
```

### Function 6 Workflow: Field Report Generator

```
START
  |
  v
[COLLECT all inputs from Functions 1-5]
  |-> Pre-inspection plan, field evidence, photo index,
  |   interior report, drone survey (if applicable)
  |
  v
[SELECT template based on property type + peril]
  |-> Template A (residential hail), B (commercial wind),
  |   C (residential water), or custom
  |
  v
[GENERATE Section 1: Executive Summary]
  |-> Key findings, damage classification, scope recommendation
  |
  v
[GENERATE Section 2: Property Information]
  |-> Address, building characteristics, policy info
  |
  v
[GENERATE Section 3: Inspection Methodology]
  |-> Methods, equipment, standards referenced, chain of custody
  |
  v
[GENERATE Section 4: Roof Findings]
  |-> Slope-by-slope damage assessment with Haag classification
  |
  v
[GENERATE Section 5: Exterior Findings]
  |-> Siding, gutters, windows, fence, HVAC per elevation
  |
  v
[GENERATE Section 6: Interior Findings (if applicable)]
  |-> Room-by-room, moisture readings, thermal anomalies, mold
  |
  v
[GENERATE Section 7: Code Compliance Assessment]
  |-> Jurisdiction, adopted codes, upgrades triggered, O&L note
  |
  v
[GENERATE Section 8: Recommended Scope of Repairs]
  |-> Roof, siding, gutters, windows, interior, attic scope
  |
  v
[GENERATE Section 9: Photo Index]
  |-> Complete photo table with IDs, descriptions, systems
  |
  v
[GENERATE Section 10: Inspector Certification]
  |-> Certification statement, signature block, contact info
  |
  v
[ADD confidentiality notice + statutory compliance]
  |-> Work product marking, 215 ILCS citations
  |
  v
[REVIEW GATE: Supervisor review required]
  |-> Check all photos present, Haag classification consistent,
  |   moisture readings current, certification complete
  |
  v
[OUTPUT Complete Field Inspection Report JSON]
  |
  v
[DELIVER to client/attorney via secure portal]
  |
  v
[ARCHIVE to claim file with chain of custody]
  |
  v
END
```
