<!-- skill — PART 1 of 3 -->
# SKILL: claimedge__intake__client-intake-suite__v1

> **Domain:** ClaimEdge (Public Adjusting & Insurance Claims)
> **Pillar:** Claim Intake & Triage (CIT)
> **Sub-pillar:** Client Onboarding & Fee Agreements
> **Version:** 1.0
> **Built:** 2026-07-16
> **Status:** P0 — Production Ready
> **Owner:** Robert Krapil, ClaimEdge LLC

---

## Skill Definition

### Name
`claimedge__intake__client-intake-suite__v1`

### Trigger Phrases
- "new client"
- "new claim"
- "client intake"
- "fee agreement"
- "letter of representation"
- "LOR"
- "statute of limitations"
- "SOL calculator"
- "onboard client"
- "sign up client"
- "client questionnaire"
- "representation letter"
- "cancellation notice"

### What This Skill Does
Comprehensive client intake and onboarding system for ClaimEdge LLC. Handles the entire initial client engagement from first contact through signed fee agreement and letter of representation. Includes Illinois public adjuster law compliance, statute of limitations tracking, and communication preference management.

### What This Skill Does NOT Do
- Does NOT provide legal advice (refers to attorneys)
- Does NOT negotiate with insurance carriers (separate skill)
- Does NOT prepare estimates or scopes of loss (separate skill)
- Does NOT handle supplement submissions (separate skill)
- Does NOT file claims with carriers (client or separate skill)

---

## Functions (5 Total)

### Function 1: Client Intake Questionnaire
**Purpose:** Collect all required information from a new prospective client.

**Input Schema:**
```json
{
  "intake_date": "2026-01-15",
  "intake_method": "phone|email|referral|walk-in|website",
  "lead_source": "contractor_referral|attorney_referral|previous_client|google|website|other",
  "referral_partner_name": "",
  "referral_partner_company": "",
  "client_primary_name": "",
  "client_primary_phone": "",
  "client_primary_email": "",
  "client_secondary_name": "",
  "property_address_street": "",
  "property_address_city": "",
  "property_address_state": "IL",
  "property_address_zip": "",
  "property_county": "",
  "property_type": "single_family|multi_family|condo|townhouse|commercial|other",
  "property_year_built": 0,
  "property_occupied": true,
  "property_primary_residence": true,
  "mortgage_company_name": "",
  "insurance_carrier": "",
  "policy_number": "",
  "claim_number": "",
  "claim_filed": false,
  "claim_filed_date": "",
  "date_of_loss": "",
  "type_of_loss": "hail|wind|water|fire|theft|vandalism|other",
  "loss_description": "",
  "damage_areas": ["roof", "siding", "gutters", "interior", "other"],
  "damage_description": "",
  "prior_repairs": false,
  "prior_claims": false,
  "prior_claims_description": "",
  "adjuster_assigned": false,
  "adjuster_name": "",
  "adjuster_phone": "",
  "adjuster_email": "",
  "adjuster_type": "staff|independent|unknown",
  "inspection_completed": false,
  "inspection_date": "",
  "settlement_offered": false,
  "settlement_amount": 0,
  "claim_status": "new|filed|inspected|estimate_received|denied|pending|other"
}
```

**Output:**
- Intake ID (auto-generated: CE-INT-YYYY-NNNN)
- Client ID (auto-generated: CE-CLI-NNNN)
- Complete intake record
- Data validation report (missing required fields flagged)
- Next step recommendations

---

### Function 2: Fee Agreement Generator
**Purpose:** Generate an Illinois-compliant public adjuster fee agreement.

**Input Schema:**
```json
{
  "client_id": "",
  "client_primary_name": "",
  "property_address_street": "",
  "property_address_city": "",
  "property_address_state": "IL",
  "property_address_zip": "",
  "insurance_carrier": "",
  "policy_number": "",
  "claim_number": "",
  "date_of_loss": "",
  "type_of_loss": "",
  "fee_percentage": 10.0,
  "fee_basis": "percentage_of_settlement|flat_fee|hybrid",
  "fee_minimum": 0,
  "fee_cap": 0,
  "scope_of_services": ["inspection", "documentation", "estimate_preparation", "carrier_negotiation", "supplement_filing"],
  "agreement_template": "standard|commercial|condo|complex",
  "effective_date": "",
  "additional_terms": "",
  "pa_license_number": "",
  "claimedge_address": "",
  "claimedge_phone": "",
  "claimedge_email": "",
  "eo_carrier": "",
  "eo_policy_number": "",
  "dispute_resolution_county": "Cook",
  "payment_due_days": 10,
  "termination_notice_days": 30
}
```

**Illinois Compliance Built-in:**
- Maximum fee validation (cannot exceed reasonable percentage)
- 5-day cancellation period (815 ILCS 525/15)
- Separate cancellation notice generation
- No up-front fee clause
- No referral fee acknowledgment (815 ILCS 525/20)
- Fiduciary duty disclosure
- E&O insurance disclosure
- License number on all pages

**Output:**
- Complete fee agreement document
- Separate cancellation notice
- Agreement ID (CE-FA-YYYY-NNNN)
- Compliance checklist (all IL requirements verified)
- Status: "draft_pending_review"

---

### Function 3: Letter of Representation (LOR)
**Purpose:** Generate a professional letter of representation to the insurance carrier.

**Input Schema:**
```json
{
  "client_id": "",
  "client_primary_name": "",
  "property_address_street": "",
  "property_address_city": "",
  "property_address_state": "IL",
  "property_address_zip": "",
  "insurance_carrier": "",
  "carrier_department": "Property Claims Department",
  "carrier_address_street": "",
  "carrier_address_city": "",
  "carrier_address_state": "",
  "carrier_address_zip": "",
  "policy_number": "",
  "claim_number": "",
  "date_of_loss": "",
  "type_of_loss": "",
  "pa_license_number": "",
  "claimedge_address": "",
  "claimedge_phone": "",
  "claimedge_email": "",
  "lor_template": "initial_representation|supplemental|appraisal_notice|bad_faith_threat",
  "request_claim_file": true,
  "inspection_notice_days": 3,
  "cc_client": true,
  "additional_cc": [],
  "urgent_response_needed": false,
  "urgent_response_days": 5,
  "authorization_attached": true,
  "delivery_method": "certified_mail|email|fax"
}
```

**Output:**
- Complete LOR document
- Delivery instructions
- CC list
- Tracking log entry
- Status: "draft_pending_review"

---

### Function 4: Statute of Limitations Calculator
**Purpose:** Calculate all relevant SOL deadlines for an Illinois insurance claim.

**Input Schema:**
```json
{
  "date_of_loss": "",
  "claim_type": "contract|property_damage|bad_faith|negligence|um_uim|consumer_fraud",
  "policy_type": "ho3|ho5|dp3|commercial|condo|other",
  "date_denied": "",
  "discovery_rule_applies": false,
  "discovery_date": "",
  "enable_alerts": true
}
```

**Illinois SOL Rules:**
- Contract: 5 years (735 ILCS 5/13-205)
- Property damage: 5 years (735 ILCS 5/13-205)
- Bad faith: 2 years from denial (735 ILCS 5/13-202)
- Negligence: 2 years (735 ILCS 5/13-202)
- UM/UIM: Varies by policy (flag for manual review)
- Consumer fraud: 3 years (815 ILCS 505/10a)

**Alert Schedule:**
- 90 days: Warning
- 60 days: Urgent
- 30 days: Critical
- 7 days: Emergency

**Output:**
- Complete SOL analysis with all deadlines
- Alert schedule
- Recommendations based on days remaining
- Legal citations for each deadline

---

### Function 5: Communication Preferences
**Purpose:** Record and manage client communication preferences and consents.

**Input Schema:**
```json
{
  "client_id": "",
  "preferred_contact_method": "email|phone|text|mail",
  "preferred_contact_times": "",
  "do_not_call_before": "",
  "do_not_call_after": "",
  "alternate_contact_name": "",
  "alternate_contact_phone": "",
  "alternate_contact_relationship": "",
  "language_preference": "english|spanish|polish|other",
  "interpreter_needed": false,
  "accessibility_needs": "",
  "text_consent": false,
  "text_consent_date": "",
  "email_consent": false,
  "email_consent_date": "",
  "mail_consent": true
}
```

**TCPA Compliance:**
- Explicit opt-in required for text messages
- Consent date/time recorded
- Opt-out mechanism provided
- Claim-related texts generally permissible

**Output:**
- Complete preference record
- TCPA compliance note
- Communication rules for future interactions

---

## Workflows

### Complete New Client Onboarding Workflow

```
Step 1: FUNCTION 1 — Client Intake Questionnaire
  -> Collect all client, property, claim, and damage information
  -> Validate required fields
  -> Generate intake_id and client_id

Step 2: FUNCTION 2 — Fee Agreement Generator
  -> Use data from Step 1
  -> Generate Illinois-compliant fee agreement
  -> Generate separate cancellation notice
  -> Flag for Robert's review

Step 3: FUNCTION 3 — Letter of Representation
  -> Use data from Step 1
  -> Generate carrier-specific LOR
  -> Include claim file request
  -> Flag for Robert's review

Step 4: FUNCTION 4 — SOL Calculator
  -> Calculate all relevant deadlines
  -> Generate alert schedule
  -> Set calendar reminders

Step 5: FUNCTION 5 — Communication Preferences
  -> Record client preferences
  -> Obtain text/email consent
  -> Set communication rules

Step 6: ROBERT REVIEW
  -> Review all generated documents
  -> Approve or request revisions
  -> Sign fee agreement

Step 7: DELIVERY
  -> Send LOR to carrier
  -> Provide cancellation notice to client
  -> File all documents in client folder
```

---

## Illinois Legal Citations Used

| Citation | Subject | Used In |
|----------|---------|---------|
| 215 ILCS 5/1501 | PA licensing requirements | Fee agreement, LOR |
| 215 ILCS 5/1553 | E&O insurance requirement | Fee agreement |
| 215 ILCS 5/1554 | Fee limitations (max 10%) | Fee agreement |
| 215 ILCS 5/1556 | Fiduciary duty | Fee agreement |
| 815 ILCS 525/10 | Written contract requirement | Fee agreement |
| 815 ILCS 525/15 | 5-day cancellation right | Fee agreement, cancellation notice |
| 815 ILCS 525/20 | No referral fees | Fee agreement |
| 735 ILCS 5/13-202 | 2-year SOL (bad faith, negligence) | SOL calculator |
| 735 ILCS 5/13-205 | 5-year SOL (contract, property) | SOL calculator |
| 815 ILCS 505/10a | 3-year SOL (consumer fraud) | SOL calculator |

---

*Continue to PART 2 for function workflows, templates, and legal notes.*

<!-- END PART 1 -->
