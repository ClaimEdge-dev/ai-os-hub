# Policy Analysis Framework
## Detailed 5-Phase Workflow for Coverage Analysis

## Table of Contents
1. [Phase 1: Document Intake](#phase-1-document-intake--organization)
2. [Phase 2: Declarations Page Analysis](#phase-2-declarations-page-analysis)
3. [Phase 3: Coverage Form Analysis](#phase-3-coverage-form-analysis)
4. [Phase 4: Endorsement Review](#phase-4-endorsement--rider-review)
5. [Phase 5: Gap Identification](#phase-5-coverage-gap-identification--summary)
6. [Output Templates](#output-templates)

---

## Phase 1: Document Intake & Organization

### Required Documents Checklist

| # | Document | Priority | Source |
|---|----------|----------|--------|
| 1 | Current Declarations Page | CRITICAL | Client or carrier |
| 2 | Policy Jacket / Coverage Form | CRITICAL | Client or carrier |
| 3 | All Endorsements (numbered) | CRITICAL | Client or carrier |
| 4 | Previous Policy Period Dec Page | HIGH | Client |
| 5 | Renewal Notices (last 2 years) | HIGH | Client |
| 6 | Premium Invoices | MEDIUM | Client |
| 7 | Correspondence with Carrier | MEDIUM | Client |
| 8 | Mortgagee / Loss Payee Info | MEDIUM | Dec page |
| 9 | Agent of Record Contact | LOW | Client |

### Document Organization Protocol

1. **Create Policy File** — Name: `[ClientLastName]_[Policy#]_CoverageAnalysis_[Date].md`
2. **Chronological Order** — Sort endorsements by effective date, not form number
3. **Redundancy Check** — Flag if same endorsement appears multiple times (superseded?)
4. **Completeness Check** — If endorsements skip numbers (HO 04 20, HO 04 54 but missing HO 04 30), note gap

### Common Policy Forms by Type

**Homeowners:**
- HO-2: Broad Form (named peril)
- HO-3: Special Form (open peril dwelling, named peril contents)
- HO-5: Comprehensive Form (open peril both)
- HO-8: Modified Coverage Form (actual cash value, limited perils)

**Dwelling Property:**
- DP-1: Basic Form (fire, lightning, internal explosion)
- DP-2: Broad Form (named peril + burglary, weight of ice/snow)
- DP-3: Special Form (open peril dwelling, named peril contents)

**Commercial Property:**
- CP 00 10: Building & Personal Property Coverage Form
- CP 00 20: Building Coverage Form only
- CP 00 30: Business Personal Property only
- CP 10 30: Causes of Loss — Special Form (all-risk)
- CP 10 20: Causes of Loss — Broad Form (named peril)

**Condominium:**
- HO-6: Unit-Owners Form (interior walls-in, personal property, liability)

### Phase 1 Output

```markdown
## Phase 1: Document Inventory

Policy Type: [HO-3 / DP-3 / CP / etc.]
Carrier: [Name]
Policy Number: [Number]
Effective Date: [Date]
Expiration Date: [Date]
Agent: [Name, Agency, Phone]

Documents Received:
- [x] Declarations Page
- [x] Coverage Form (Form #)
- [x] Endorsements (count: [N])
- [ ] Previous Period (if missing, note)
- [ ] Renewal Notices (if missing, note)

Completeness Assessment: [COMPLETE / PARTIAL — list gaps]
```

---

## Phase 2: Declarations Page Analysis

### Element-by-Element Extraction

#### Coverage A — Dwelling / Building

| Field | Value | Notes |
|-------|-------|-------|
| Limit | $[amount] | Compare to estimated replacement cost |
| Coinsurance | [80% / 100% / None] | Commercial policies typically 80% or 90% |
| Agreed Value | [Yes / No] | If yes, no coinsurance penalty |
| Functional Replacement Cost | [Yes / No] | Older homes may have FRC option |
| Inflation Guard | [% automatic increase] | Check if applied |

**Red Flag:** If Coverage A < 80% of estimated replacement cost → underinsurance issue

#### Coverage B — Other Structures

| Field | Value | Notes |
|-------|-------|-------|
| Limit | [Amount or % of A] | Typically 10% of Coverage A |
| Included Structures | [List] | Detached garage, shed, fence, gazebo |
| Excluded Structures | [List] | Structures used for business |

**Common Issue:** Detached garage with hail damage — verify B limit covers it

#### Coverage C — Personal Property / Contents

| Field | Value | Notes |
|-------|-------|-------|
| Limit | [Amount or % of A] | Typically 50-70% of Coverage A |
| Valuation | [RCV / ACV] | RCV = replacement cost, ACV = depreciated |
| Special Limits | [List each] | See Special Limits section below |
| Off-Premises | [% of C limit] | Usually 10% for items away from home |

**Special Limits to Extract:**
- Money / bank notes / coins: typically $200
- Securities / deeds / evidence of debt: typically $1,500
- Jewelry / watches / furs: typically $1,500 (total)
- Firearms: typically $2,500
- Silverware / goldware / pewterware: typically $2,500
- Electronic apparatus (vehicle/boat): typically $1,500
- Business property on premises: typically $2,500
- Business property off premises: typically $500
- Watercraft: typically $1,500
- Trailers not used with watercraft: typically $1,500

#### Coverage D — Loss of Use / ALE / Fair Rental Value

| Field | Value | Notes |
|-------|-------|-------|
| Limit | [Amount or % of A / time limit] | Typically 20-30% of A, no time limit |
| ALE vs. Fair Rental | [Which applies] | Owner-occupied = ALE; Rental = Fair Rental |
| Time Limit | [None / X months] | Some policies cap duration |
| Additional Coverage | [Any extensions] | Check endorsements |

**Critical for Client:** ALE pays for temporary housing, meals, storage. No dollar limit on most HO policies, but time limits may apply.

#### Deductibles

| Type | Amount | Applies To |
|------|--------|-----------|
| Standard (All Peril) | $[amount] | Most losses |
| Wind/Hail | $[amount or %] | May be separate, higher |
| Named Storm | $[amount or %] | Hurricane/named storm specific |
| Percentage | [% of Coverage A] | Common in coastal areas — can be huge |

**RED FLAG — Percentage Deductible Example:**
- Coverage A: $400,000
- 2% wind/hail deductible: $8,000 out-of-pocket
- Client may not realize this — flag immediately

#### Ordinance or Law Coverage

| Field | Value | Notes |
|-------|-------|-------|
| Coverage Amount | [% of A or $ limit] | Typically 10% of A default |
| Increased Limit Endorsement | [Yes / No] | Can increase to 25% or 50% |
| Separate Deductible | [Yes / No] | Some policies have separate O&L deductible |

**Critical for Supplements:** O&L is your primary code upgrade funding source.
- No O&L = no code upgrade argument
- Limited O&L = limited code upgrade scope
- Flag immediately if missing or insufficient

#### Additional Coverages (Built-in)

Extract these even though not on dec page — they're in the coverage form:
- Debris Removal: typically $[amount] additional
- Trees/Shrubs: typically $500 per tree, $[total] max
- Fire Department Service Charge: typically $500
- Property Removed: typically $[amount] for 30 days
- Credit Card / ATM / Forgery: typically $500
- Collapse: check if included or endorsement
- Glass: check if included or endorsement
- Landlord's Furnishings: typically $2,500 per unit
- Building Additions/Alterations: typically 10% of A

### Phase 2 Output

```markdown
## Phase 2: Declarations Summary

### Coverage Limits
| Coverage | Limit | Deductible | Notes |
|----------|-------|-----------|-------|
| A — Dwelling | $XXX | $X,XXX | |
| B — Other Structures | $XXX or X% of A | Same as A | |
| C — Personal Property | $XXX or X% of A | Same as A | RCV/ACV: |
| D — Loss of Use | $XXX or X% of A / Unlimited | None | |
| E — Liability | $XXX | None | |
| F — Med Pay | $XXX / person | None | |
| Ordinance & Law | $XXX or X% of A | | |

### Special Limits
[Table of all special limits from policy]

### Deductible Analysis
- Standard: $X,XXX
- Wind/Hail: $X,XXX (or X%)
- Effective for this loss: $X,XXX

### Red Flags
- [List any issues]

### Underinsurance Assessment
- Coverage A: $XXX
- Estimated Replacement Cost: $XXX
- Coinsurance %: XX%
- Minimum Required: $XXX
- Status: [ADEQUATE / UNDERINSURED by $XXX]
```

---

## Phase 3: Coverage Form Analysis

### Peril-by-Peril Checklist

For each covered peril, document: definition, sub-limits, exclusions, conditions.

#### Fire & Lightning
- Definition: [Policy language]
- Sub-limits: [Any]
- Exclusions: [List — e.g., smoke from agricultural smudging]
- Conditions: [Duties after loss]

#### Windstorm & Hail
- Definition: [Policy language — includes hail?]
- Sub-limits: [Separate deductible?]
- Exclusions: [Interior damage unless opening created?]
- Conditions: [Timeline for reporting]

**Illinois Note:** Wind and hail are the most common Chicagoland claims. Check for cosmetic damage exclusions (PA 103-0510 requires matching).

#### Explosion
- Definition: [Internal vs. external?]
- Sub-limits: [Any]
- Exclusions: [Business-related?]
- Conditions: []

#### Riot / Civil Commotion
- Definition: [Policy language]
- Sub-limits: [Any]
- Exclusions: []
- Conditions: []

#### Aircraft / Vehicle Damage
- Definition: [Striking building]
- Sub-limits: [Any]
- Exclusions: [Owned vehicle?]
- Conditions: []

#### Smoke
- Definition: [Sudden/accidental only?]
- Sub-limits: [Any]
- Exclusions: [Agricultural smudging, industrial operations]
- Conditions: []

#### Vandalism / Malicious Mischief
- Definition: [Policy language]
- Sub-limits: [Any]
- Exclusions: [Vacant dwelling > 60 days]
- Conditions: [Police report required?]

#### Theft
- Definition: [Policy language]
- Sub-limits: [Special limits apply]
- Exclusions: [Dwelling under construction, rented to others]
- Conditions: [Police report, proof of ownership]

#### Falling Objects
- Definition: [Policy language — tree branches?]
- Sub-limits: [Any]
- Exclusions: [Interior unless roof/wall penetrated]
- Conditions: []

#### Weight of Ice/Snow/Sleet
- Definition: [Policy language]
- Sub-limits: [Any]
- Exclusions: [Retaining walls, awnings, patio covers?]
- Conditions: []

**Critical for Illinois:** Ice dam claims — check if water damage from ice dams is covered as part of this peril or excluded under water damage.

#### Accidental Discharge (Water)
- Definition: [Plumbing, heating, AC, appliance]
- Sub-limits: [Any]
- Exclusions: [Gradual leakage, foundation, below-ground pipes]
- Conditions: [Repair source, reasonable care]

#### Freezing
- Definition: [Plumbing freezing]
- Sub-limits: [Any]
- Exclusions: [If heat was maintained?]
- Conditions: [Reasonable care to maintain heat]

#### Sudden & Accidental Tearing Asunder
- Definition: [Steam/hot water system]
- Sub-limits: [Any]
- Exclusions: [Age-related deterioration]
- Conditions: []

#### Electrical Current
- Definition: [Artificially generated electrical current]
- Sub-limits: [Any]
- Exclusions: [Power surge from utility — check]
- Conditions: []

### Open Peril Analysis (HO-3 Dwelling, HO-5, DP-3)

For open peril policies, reverse the analysis:
1. List ALL exclusions in the coverage form
2. For each exclusion, assess relevance to current loss
3. Determine if exclusion applies or if there's a counter-argument
4. Document carrier's likely position vs. your argument

**Common Open Peril Exclusions:**
- Ordinance or Law (unless endorsement)
- Earth movement (including sinkholes)
- Water damage (flood, surface water, sewer backup)
- Power failure (off premises)
- Neglect / failure to preserve property
- War / nuclear hazard
- Intentional loss
- Governmental action
- Faulty workmanship
- Wear and tear / deterioration
- Rust / corrosion
- Mold / fungus (limited coverage, usually $10,000)
- Birds / vermin / insects

### Phase 3 Output

```markdown
## Phase 3: Coverage Form Analysis

### Policy Form: [HO-3 / DP-3 / CP / etc.]
### Peril Type: [Named / Open / Mixed]

### Covered Perils Analysis
[Table of all covered perils with definitions, sub-limits, exclusions]

### Exclusion Analysis
[Table of all exclusions with applicability to current loss]

### Conditions Precedent
[Duties after loss — what client must do]

### Carrier Likely Position vs. Our Argument
[For each contested coverage element]
```

---

## Phase 4: Endorsement & Rider Review

### Endorsement Priority Matrix

Review in this order of claim impact:

**TIER 1 — Always Critical:**
| Endorsement | Form # | What It Does | Impact |
|-------------|--------|-------------|--------|
| Ordinance or Law | Various | Code upgrade coverage | Affects supplement scope |
| Water Backup | HO 04 95 / DP 04 95 | Sump/sewer backup | Water damage claims |
| Foundation/Water | Various | Foundation water damage | Basement/foundation claims |
| Mold/Fungus | HO 04 26 | Mold remediation | Water damage claims |

**TIER 2 — Often Critical:**
| Endorsement | Form # | What It Does | Impact |
|-------------|--------|-------------|--------|
| Scheduled Property | HO 04 60 | Agreed values on items | High-value contents |
| Replacement Cost | HO 04 90 | RCV on contents | Contents claims |
| Home Business | HO 07 01 | Business equipment | Mixed-use properties |
| Equipment Breakdown | HO 04 26 | Mechanical breakdown | HVAC, appliances |
| Service Line | Various | Underground utility lines | Water/sewer line breaks |

**TIER 3 — Situational:**
| Endorsement | Form # | What It Does | Impact |
|-------------|--------|-------------|--------|
| Loss Assessment | HO 04 20 | HOA special assessments | Condo/townhome |
| Identity Theft | HO 04 55 | ID theft recovery | Any claim with stolen docs |
| Earthquake | Various | Earthquake coverage | Rare in IL |
| Personal Injury | HO 24 82 | Libel/slander/defamation | Liability claims |

### Endorsement Analysis Template

For each endorsement, complete:

```markdown
### Endorsement: [Name]
Form Number: [e.g., HO 04 95]
Effective Date: [Date]
Added/Modified/Excluded: [Category]

What It Does:
[Plain English explanation]

Policy Language:
[Exact or summarized language from endorsement]

Impact on Current Claim:
[Specific effect on this loss]

Our Position:
[How we argue this coverage applies]

Carrier Likely Counter:
[What they'll argue]

IL Law Support:
[Relevant statute or case law]
```

### Mid-Claim Endorsement Changes

If carrier changes endorsements mid-claim:
1. **Document the change** — effective date, what changed
2. **Check retroactivity** — can they apply to existing loss?
3. **215 ILCS 5/154.6** — 15-day notice required for material changes
4. **Contra Proferentem** — ambiguities favor the insured
5. **Bad faith indicator** — mid-claim changes to avoid coverage = red flag

---

## Phase 5: Coverage Gap Identification & Summary

### Gap Severity Matrix

| Severity | Definition | Action |
|----------|-----------|--------|
| **HIGH** | No coverage for major component of loss | Immediate client notification; consider bad faith |
| **MEDIUM** | Partial coverage or sub-limit applies | Work within limits; argue for expansion |
| **LOW** | Coverage exists but may be insufficient | Document; monitor as claim develops |

### Common Gap Patterns

**Pattern 1: Underinsurance**
- Coverage A < 80% replacement cost
- Coinsurance penalty applies
- Client thinks they're fully covered
- **Action:** Document immediately; consider agent E&O claim

**Pattern 2: Missing Water Backup**
- No HO 04 95 endorsement
- Sewer backup / sump pump failure not covered
- Very common in Chicagoland basements
- **Action:** Check if loss can be characterized as plumbing overflow (covered) vs. backup (excluded)

**Pattern 3: Cosmetic Damage Exclusion**
- Carrier denies matching siding/roofing
- PA 103-0510 requires reasonable matching in Illinois
- **Action:** Cite PA 103-0510; demand full replacement for reasonable uniform appearance

**Pattern 4: Ordinance or Law Insufficient**
- O&L limit = 10% of A on $400,000 policy = $40,000
- Full code compliance costs $60,000+
- **Action:** Argue for increased limits endorsement; separate O&L claim if available

**Pattern 5: Foundation Exclusion**
- Foundation water damage excluded
- Loss was actually plumbing overflow (covered)
- **Action:** Characterize loss as covered peril, not excluded peril

### Gap Documentation Template

```markdown
## Coverage Gaps

### Gap 1: [Title]
Severity: [HIGH / MEDIUM / LOW]
Description: [What the gap is]
Financial Impact: $[amount]
IL Law Argument: [Statute/case]
Recommended Action: [Specific next step]

### Gap 2: [Title]
[...]
```

---

## Output Templates

### Coverage Analysis Report (Full)

```markdown
# CLAIMEDGE COVERAGE ANALYSIS REPORT

**Client:** [Name]
**Property Address:** [Address]
**Policy Number:** [Number]
**Carrier:** [Name]
**Agent:** [Name, Agency]
**Date of Loss:** [Date]
**Date of Analysis:** [Date]
**Analyst:** [ClaimEdge Analyst]
**Confidence Level:** [HIGH / MEDIUM / LOW]

---

## EXECUTIVE SUMMARY

[3-4 sentences summarizing: policy type, key limits, major gaps, and overall
assessment of coverage adequacy for this loss.]

---

## PHASE 1: DOCUMENT INVENTORY

[Documents received, completeness assessment]

---

## PHASE 2: DECLARATIONS SUMMARY

[Coverage limits table, deductible analysis, underinsurance assessment]

---

## PHASE 3: COVERAGE FORM ANALYSIS

[Peril analysis, exclusion analysis, conditions]

---

## PHASE 4: ENDORSEMENT TRACKING

[Endorsement table, tier analysis]

---

## PHASE 5: COVERAGE GAPS

[Gap table with severity and recommendations]

---

## ILLINOIS LAW CONSIDERATIONS

[Relevant statutes and case law]

---

## RECOMMENDATIONS

1. [Immediate action]
2. [Short-term strategy]
3. [Long-term consideration]

---

## DOCUMENT CONTROL
Analyst: [Name]
Review Date: [Date]
Next Review: [Trigger event]
```

### Quick Coverage Check (Abbreviated)

For fast turnaround (e.g., intake call):

```markdown
## QUICK COVERAGE CHECK

Policy: [Number] | Carrier: [Name]

**Key Limits:**
- Cov A: $XXX (Deductible: $X,XXX)
- Cov B: $XXX
- O&L: $XXX ([%] of A)

**Critical Gaps:**
- [ ] [Gap 1]
- [ ] [Gap 2]

**Bottom Line:** [Coverage adequate / gaps identified / immediate action needed]

**Next Step:** [Specific action]
```
