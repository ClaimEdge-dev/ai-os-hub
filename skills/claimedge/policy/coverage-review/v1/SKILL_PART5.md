### Function 1: Policy Document Review — Workflow

```
Step 1: RECEIVE POLICY DOCUMENTS
  -> Accept uploaded policy documents (PDF, images, scans)
  -> Validate minimum document set: policy form + declarations page
  -> If endorsements missing: flag and request from client/carrier
  -> Create review_id: CE-PRV-{YYYY}-{NNNN}

Step 2: IDENTIFY POLICY TYPE AND FORM
  -> Detect policy type from document headers and form numbers
  -> Look for ISO form references (HO 00 03, HO 00 05, etc.)
  -> If form edition not visible: flag for manual entry
  -> Validate policy is Illinois-issued (or flag out-of-state)

Step 3: EXTRACT COVERAGE PROVISIONS
  -> Read Coverage A through F sections
  -> For each coverage: identify limit, loss settlement method, special conditions
  -> Note percentage-based coverages (B = 10% of A, C = 50% of A, etc.)
  -> Identify any sub-limits or special limitations
  -> Flag coverage sections that are "not applicable to loss"

Step 4: ANALYZE EXCLUSIONS
  -> Read Section I Exclusions (for property coverages)
  -> For each exclusion: determine if it APPLIES to current loss
  -> If exclusion applies: check for mitigating endorsements
  -> If mitigating endorsement present: document coverage available
  -> Build rebuttal arguments for all applicable exclusions
  -> Flag exclusions for future carrier disputes

Step 5: ANALYZE ENDORSEMENTS
  -> Read all endorsement forms attached to policy
  -> Document form number, name, description, and effect
  -> Classify each as: relevant_to_claim, not_relevant, or missing_but_needed
  -> Calculate financial impact of each endorsement on claim

Step 6: ANALYZE DEDUCTIBLES
  -> Identify standard deductible amount and type
  -> Check for special deductibles (named storm, wind/hail, hurricane)
  -> Note which deductible applies to the loss type
  -> Calculate net recovery after deductible

Step 7: ANALYZE LOSS SETTLEMENT PROVISIONS
  -> Determine RCV vs ACV for each coverage
  -> Note RCV holdback conditions and timelines
  -> Identify any provisions affecting settlement timing
  -> Flag ACV settlements that could be argued to RCV

Step 8: COMPILE RISK ASSESSMENT
  -> Rate coverage adequacy: adequate / marginal / inadequate
  -> Rate underinsurance risk: none / low / moderate / high
  -> List all key concerns
  -> List all recommendations
  -> Flag any issues requiring immediate escalation

Step 9: OUTPUT
  -> Return complete Policy Document Review Results (JSON)
  -> Status: "complete" or "incomplete_pending_documents"
  -> Attach review notes and flag items for Robert's attention
```

### Function 2: Declarations Page Extractor — Workflow

```
Step 1: RECEIVE DECLARATIONS PAGE
  -> Accept dec page image or PDF
  -> If extraction_mode = full_auto: run OCR
  -> If extraction_mode = guided: prompt user to verify OCR fields
  -> If extraction_mode = manual: prompt user to enter all fields
  -> Validate against known policy number (if provided)

Step 2: EXTRACT NAMED INSURED
  -> Read named insured section (primary and additional)
  -> Validate against client intake data
  -> Flag if named insured doesn't match client (e.g., deceased spouse still listed)

Step 3: EXTRACT ADDRESSES
  -> Read mailing address and property address
  -> Validate property address matches intake
  -> Flag if addresses differ (common with rental properties)

Step 4: EXTRACT POLICY PERIOD
  -> Read effective date and expiration date
  -> Calculate days remaining until expiration
  -> Flag if policy expires within 90 days (renewal monitoring needed)
  -> Flag if policy was not in force on date of loss

Step 5: EXTRACT COVERAGE LIMITS
  -> Read all coverage limits (A through F)
  -> Validate numeric format and reasonable ranges
  -> Calculate percentages (B as % of A, C as % of A)
  -> Flag if any coverage limit is $0 or missing

Step 6: EXTRACT DEDUCTIBLES
  -> Read standard deductible
  -> Check for special deductibles (named storm, wind/hail)
  -> Note percentage-based deductibles and calculate dollar equivalent

Step 7: EXTRACT ENDORSEMENTS
  -> Read endorsement list with form numbers
  -> Cross-reference against known endorsement database
  -> Flag endorsements relevant to current loss type

Step 8: EXTRACT MORTGAGEE AND PREMIUM
  -> Read mortgagee name, address, loan number
  -> Read annual premium and payment plan
  -> Read prior carrier information (if shown)

Step 9: VALIDATE AND OUTPUT
  -> Run validation checks on all extracted data
  -> Calculate extraction_confidence score
  -> Flag any fields with low confidence for manual review
  -> Return Declarations Page Extracted Data (JSON)
```

### Function 3: Coverage Gap Analysis — Workflow

```
Step 1: RECEIVE COVERAGE AND DAMAGE DATA
  -> Accept coverage_limits from Function 2 output
  -> Accept estimated_damages from user input or inspection data
  -> Validate all required fields present
  -> Load policy type and coinsurance rules

Step 2: COMPARE COVERAGE A TO DAMAGES
  -> Coverage A limit vs estimated structural damage
  -> Coverage A limit vs estimated replacement cost
  -> Calculate coinsurance compliance percentage
  -> If < 80%: calculate estimated coinsurance penalty
  -> Flag underinsurance issues

Step 3: COMPARE COVERAGE B TO DAMAGES
  -> Coverage B limit vs estimated other structures damage
  -> Calculate gap and gap percentage
  -> Flag if damage components exceed limit

Step 4: COMPARE COVERAGE C TO DAMAGES
  -> Coverage C limit vs estimated contents damage
  -> Note loss settlement method (RCV vs ACV)
  -> If ACV: estimate RCV recovery gap
  -> Flag adequacy or inadequacy

Step 5: ANALYZE COVERAGE D (ALE)
  -> Check if Coverage D has dollar limit or is unlimited
  -> Calculate estimated ALE (monthly x duration)
  -> Flag if limited and estimate may exceed limit

Step 6: CALCULATE ORDINANCE & LAW GAP
  -> O&L total limit vs estimated code upgrade costs
  -> Calculate shortfall or excess
  -> Flag if code upgrades exceed O&L coverage

Step 7: CALCULATE TOTALS
  -> Sum all coverage available
  -> Sum all estimated damages
  -> Calculate total gap and gap percentage
  -> Rate overall risk: none / low / moderate / high / severe

Step 8: GENERATE RECOMMENDATIONS
  -> For each gap: specific recommended action
  -> If coinsurance issue: recommend waiver argument or attorney
  -> If O&L shortfall: recommend O&L argument or supplement
  -> If escalation needed: flag for Robert's review

Step 9: OUTPUT
  -> Return Coverage Gap Analysis (JSON)
  -> Include assessment, concerns, and recommendations
  -> Flag if escalation is needed
```