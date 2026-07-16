### Function 2: Declarations Page Extractor — Workflow

```
Step 1: RECEIVE DECLARATIONS PAGE
  -> Accept dec page image, PDF, or pre-extracted text
  -> If image/PDF: run OCR with field-aware extraction
  -> If pre-extracted text: validate completeness and structure

Step 2: EXTRACT NAMED INSUREDS
  -> Identify primary named insured(s)
  -> Extract any additional named insureds
  -> Validate names match intake records
  -> Flag if property owner differs from named insured (trust, LLC, etc.)

Step 3: EXTRACT ADDRESSES
  -> Extract mailing address (may differ from property address)
  -> Extract property address (the insured location)
  -> Validate property address matches intake
  -> Flag if mailing address is out of state (may affect jurisdiction)

Step 4: EXTRACT POLICY PERIOD
  -> Extract effective date and expiration date
  -> Confirm policy was in force on date of loss
  -> If policy lapsed before loss: flag as critical coverage issue
  -> If policy bound after loss: flag as potential rescission issue

Step 5: EXTRACT COVERAGE LIMITS
  -> Extract Coverage A through F limits from coverage table
  -> Validate: Coverage B should be ~10% of A, Coverage C ~50% of A (standard HO-3)
  -> Flag non-standard ratios
  -> If any coverage shows "$0" or "Excluded": flag for analysis
  -> Extract any additional coverage amounts (endorsement limits)

Step 6: EXTRACT DEDUCTIBLES
  -> Extract standard deductible amount
  -> Identify deductible type (flat, percentage, split)
  -> If percentage: extract basis and calculate dollar equivalent
  -> Extract any special deductibles (wind/hail, named storm, hurricane)
  -> Determine which deductible applies to this loss type

Step 7: EXTRACT ENDORSEMENTS
  -> Read endorsement list from dec page
  -> Extract form numbers (e.g., "HO 04 54") and descriptions
  -> Cross-reference form numbers against known endorsement database
  -> Flag any endorsements with claim impact
  -> Note any endorsements that override standard coverage

Step 8: EXTRACT MORTGAGEE INFORMATION
  -> Extract mortgagee name and address
  -> Extract loan number (partially redacted for security)
  -> Flag if multiple mortgagees or loss payees
  -> Note any special mortgagee clauses

Step 9: EXTRACT PREMIUM AND CARRIER HISTORY
  -> Extract annual premium
  -> Extract prior carrier name and expiration (if shown)
  -> Note any premium changes from prior carrier

Step 10: VALIDATE AND CROSS-CHECK
  -> Cross-validate extracted limits against policy form language
  -> Verify coverage A + B + C + D arithmetic is consistent
  -> Flag any discrepancies between dec page and policy form
  -> Assign extraction confidence level (high/medium/low)

Step 11: OUTPUT
  -> Return structured declarations data
  -> Include all extracted fields with validation notes
  -> Flag any fields requiring manual verification
  -> Status: "complete" or "partial_review_needed"
```

---

### Function 3: Coverage Gap Analysis — Workflow

```
Step 1: RECEIVE COVERAGE LIMITS AND DAMAGE ESTIMATES
  -> Accept coverage limits from Function 2 output
  -> Accept damage estimates from estimating workflow or manual input
  -> Validate all required fields are present
  -> If damage estimates missing: request from estimator or prompt for input

Step 2: CALCULATE COVERAGE A ADEQUACY
  -> Compare Coverage A limit to estimated structure damage
  -> Calculate Coverage A as percentage of estimated full replacement cost
  -> Apply Extended Replacement Cost or Guaranteed Replacement Cost if present
  -> Determine if damage is within available coverage

Step 3: CALCULATE COINSURANCE COMPLIANCE
  -> Identify coinsurance requirement (typically 80% for HO-3)
  -> Calculate 80% of estimated replacement cost
  -> Compare Coverage A limit to 80% threshold
  -> If Coverage A < 80% of RCV: calculate potential coinsurance penalty
  -> Coinsurance penalty formula: (Limit Carried / Limit Required) x Loss = Recovery

Step 4: CALCULATE COVERAGE B ADEQUACY
  -> Compare Coverage B limit to estimated other structures damage
  -> Note: detached garage, fences, sheds, decks, pools
  -> Calculate gap if damage exceeds limit

Step 5: CALCULATE COVERAGE C ADEQUACY
  -> Compare Coverage C limit to estimated contents damage
  -> Account for ACV settlement reducing actual recovery
  -> Check special sub-limits that may apply (jewelry, art, cash, etc.)
  -> Calculate gap if damage exceeds limit or sub-limits apply

Step 6: CALCULATE COVERAGE D ADEQUACY
  -> Compare estimated ALE to Coverage D limit (if any)
  -> Calculate monthly ALE x estimated months of displacement
  -> If Coverage D is "actual loss sustained" (no dollar limit): note unlimited but document actual expenses
  -> Calculate gap if applicable

Step 7: ASSESS UNDERINSURANCE
  -> Calculate total estimated damage across all coverages
  -> Calculate total available coverage across all coverages
  -> Determine if property is underinsured (Coverage A < full RCV)
  -> Calculate underinsurance percentage
  -> Flag if underinsurance > 20%

Step 8: IDENTIFY MISSING ENDORSEMENTS
  -> Compare policy endorsements to recommended endorsements for this property type/age
  -> Identify endorsements that would have improved coverage
  -> Estimate financial impact of each missing endorsement
  -> Draft arguments for missing endorsement coverage if carrier made representations

Step 9: BUILD COVERAGE INCREASE ARGUMENTS
  -> Identify arguments for increasing coverage applicability
  -> Reference Extended Replacement Cost, Guaranteed Replacement Cost, or similar provisions
  -> Identify ambiguity in limit language that favors broader coverage
  -> Prepare arguments for supplemental coverage under additional provisions

Step 10: GENERATE FLAGGED ISSUES
  -> Compile all coverage gaps, shortfalls, and concerns
  -> Assign severity: critical / warning / informational
  -> For each flagged issue: provide specific recommendation

Step 11: OUTPUT
  -> Return complete coverage gap analysis
  -> Include all comparisons, calculations, and flagged issues
  -> Provide specific recommendations for addressing each gap
  -> Trigger Function 6 (Memo Generator) if memo requested
```

---

### Function 4: Ordinance & Law Coverage Assessment — Workflow

```
Step 1: RECEIVE O&L COVERAGE AND PROPERTY DATA
  -> Accept O&L limits (A, B, C) from Function 1 output
  -> Accept property data (age, type, construction, jurisdiction)
  -> Accept estimated damage information
  -> If O&L endorsement not present: flag as critical gap — standard HO-3 excludes O&L

Step 2: IDENTIFY APPLICABLE BUILDING CODES
  -> Determine state-adopted code (Illinois typically adopts IRC/IBC 3-year cycles)
  -> Identify local jurisdiction code adoptions (may exceed state minimum)
  -> Reference applicable code year (IRC 2021, IBC 2021, IEBC 2021, IECC 2021)
  -> Research any local amendments to adopted codes
  -> Document code authority having jurisdiction (AHJ)

Step 3: IDENTIFY TRIGGERED CODE UPGRADES
  -> For each damaged building component:
     -> Determine if component must be upgraded to current code when repaired/replaced
     -> Reference specific code section requiring upgrade
     -> Estimate cost of code upgrade vs. like-kind repair
     -> Assign to O&L Limit A, B, or C based on nature of upgrade
  -> Common triggers:
     -> Roof: underlayment (IRC R905), drip edge (R905.2.8.2), ventilation (R806)
     -> Siding: water-resistive barrier (R703.11), flashing (R703.11.2.1)
     -> Windows: U-factor requirements (IECC R402.3.1), egress requirements (R310)
     -> Electrical: GFCI/AFCI (IRC Chapter 39), panel upgrades (E3401)
     -> Plumbing: pipe material, fixture flow rates
     -> HVAC: efficiency requirements (IECC), combustion air (M1701)
     -> Insulation: R-value upgrades (IECC R402/R403)
     -> Structural: tie-downs, bracing, anchoring (R301, R302)
     -> Fire: smoke/CO detectors (R314, R315), egress windows (R310)

Step 4: CATEGORIZE UPGRADES BY O&L LIMIT
  -> O&L Limit A: Undamaged portion of building that must be brought to code
     -> Typically: continuous WRB, insulation in undamaged walls, electrical updates
  -> O&L Limit B: Demolition and debris removal costs
     -> Cost to demolish damaged portions; disposal fees; permit fees for demolition
  -> O&L Limit C: Increased cost of construction
     -> Additional material/labor costs to build to code vs. pre-loss condition
     -> Typically the largest limit — most code upgrades fall here

Step 5: CALCULATE O&L SHORTFALL
  -> Sum all estimated code upgrade costs
  -> Compare to available O&L limits by category
  -> Calculate shortfall for each limit (A, B, C) and total
  -> If shortfall exists: flag and prepare arguments

Step 6: BUILD O&L COVERAGE ARGUMENTS
  -> Under 215 ILCS 5/154.6: carrier must provide reasonable explanation for O&L limitation
  -> Under PA 103-0510: carrier must have clearly disclosed O&L limitations at sale
  -> Contra proferentem: ambiguous "required by ordinance or law" language construed broadly
  -> Document each code requirement with specific code section citation
  -> Obtain written confirmation from building department of code requirements

Step 7: PREPARE DOCUMENTATION RECOMMENDATIONS
  -> Recommend pre-demolition photos of all pre-code conditions
  -> Recommend written confirmation from AHJ of all triggered upgrades
  -> Recommend meeting with carrier adjuster and building official
  -> Recommend permit applications document all code requirements

Step 8: OUTPUT
  -> Return complete O&L assessment
  -> Include all triggered upgrades with code citations and cost estimates
  -> Include shortfall calculation and legal arguments
  -> Provide specific documentation recommendations
```

---

### Function 5: Coverage Argument Builder — Workflow

```
Step 1: RECEIVE DISPUTE INFORMATION
  -> Accept disputed issue type, carrier position, and policy language
  -> Accept facts of loss and claim history
  -> Accept any carrier representations or client expectations
  -> Validate all required fields for argument generation

Step 2: BUILD CONTRA PROFERENTEM ARGUMENT
  -> Analyze policy language for ambiguity
  -> Identify multiple reasonable interpretations
  -> Cite Cramer v. Insurance Exchange Agency (174 Ill. App. 3d 862)
  -> Draft argument that ambiguous language is construed against drafter (carrier)
  -> Flag if policy language is unambiguous (argument may be weak)

Step 3: BUILD REASONABLE EXPECTATIONS ARGUMENT
  -> Identify what a reasonable purchaser would expect from policy language
  -> Document any carrier marketing, agent statements, or sales materials
  -> Cite Wald v. Crusader Ins. Co. (201 Ill. App. 3d 712)
  -> Draft argument that reasonable expectations control over technical exclusions
  -> Include any agent representations as supporting evidence

Step 4: BUILD UNFAIR CLAIMS PRACTICES ARGUMENT
  -> Map carrier conduct to specific 215 ILCS 5/154.6 violations:
     -> (a) Misrepresenting policy provisions
     -> (b) Failing to acknowledge claim within 15 working days
     -> (c) Failing to adopt reasonable standards for investigation
     -> (d) Refusing to pay without reasonable investigation
     -> (e) Failing to affirm or deny coverage within 15 working days
     -> (f) Failing to provide reasonable explanation for denial
     -> (g) Failing to offer compromise settlement when liability is clear
     -> (h) Unreasonable delay in settlement offer
  -> Document timeline of carrier conduct
  -> Draft statutory violation argument with specific citations

Step 5: BUILD PA 103-0510 ARGUMENT
  -> Identify any violations of PA 103-0510 (2024 reforms):
     -> Failure to provide plain language summary at inception/renewal
     -> Technical denial that defeats reasonable expectations
     -> Inadequate notice of coverage limitations
  -> Cite specific sections of PA 103-0510
  -> Note enhanced penalties under revised 215 ILCS 5/155

Step 6: BUILD BAD FAITH ARGUMENT
  -> Identify pattern of unreasonable carrier conduct
  -> Document: delays, inadequate investigations, lowball offers, wrongful denials
  -> Cite 215 ILCS 5/155 (attorney fees, statutory penalties up to $10,000/day)
  -> Calculate potential bad faith damages
  -> Note: bad faith requires more than simple negligence — need pattern or outrageous conduct

Step 7: PRIORITIZE AND ASSEMBLE ARGUMENTS
  -> Rank all arguments by strength: very strong / strong / moderate / weak
  -> Assign priority order for presentation
  -> Recommend lead argument (strongest) and supporting arguments
  -> Flag any arguments that require additional documentation

Step 8: OUTPUT
  -> Return complete set of coverage arguments
  -> Include: argument type, legal basis, applicable facts, drafted text, strength rating
  -> Provide argument priority ranking
  -> Include litigation risk assessment
```

---

### Function 6: Coverage Opinion Memo Generator — Workflow

```
Step 1: RECEIVE ALL ANALYSIS INPUTS
  -> Accept outputs from Functions 1-5
  -> Validate all required inputs present
  -> Determine memo type: comprehensive, dispute-focused, or abbreviated
  -> Load client and claim information

Step 2: DRAFT EXECUTIVE SUMMARY
  -> One-paragraph summary of coverage conclusion
  -> State clear answer: covered / not covered / partially covered
  -> Highlight key dollar amounts and concerns
  -> Note any immediate action items

Step 3: DRAFT POLICY INFORMATION SECTION
  -> List carrier, policy number, type, effective dates
  -> Identify named insured and property address
  -> Note any relevant endorsement or form edition

Step 4: DRAFT FACTUAL BACKGROUND
  -> Summarize loss event with date, cause, and damages
  -> Note carrier's claim handling to date
  -> Include relevant client statements or documentation

Step 5: DRAFT COVERAGE ANALYSIS (by Coverage)
  -> For each applicable coverage (A, B, C, D):
     -> State whether loss falls within coverage grant
     -> Address any applicable exclusions
     -> Reference policy language
     -> Calculate available recovery after deductible

Step 6: DRAFT EXCLUSION ANALYSIS
  -> Address each exclusion raised by carrier or applicable to loss
  -> Apply contra proferentem if language is ambiguous
  -> Reference rebuttal arguments from Function 5
  -> Cite supporting case law

Step 7: DRAFT O&L ASSESSMENT (if applicable)
  -> Summarize O&L coverage and limits
  -> List triggered code upgrades with citations
  -> State adequacy conclusion

Step 8: DRAFT COVERAGE GAP SUMMARY
  -> Summarize any underinsurance or coverage gaps
  -> Quantify financial impact to insured
  -> Note coinsurance penalty exposure

Step 9: DRAFT RECOMMENDATIONS
  -> List prioritized action items with timelines
  -> Include: formal demand, IDOI complaint, attorney consultation, appraisal
  -> Note escalation triggers
  -> Assign responsibility for each action

Step 10: FINALIZE AND OUTPUT
  -> Apply ClaimEdge memo formatting and headers
  -> Add confidentiality notice (Attorney Work Product)
  -> Set status: "draft_pending_review"
  -> Return complete Coverage Opinion Memo
```