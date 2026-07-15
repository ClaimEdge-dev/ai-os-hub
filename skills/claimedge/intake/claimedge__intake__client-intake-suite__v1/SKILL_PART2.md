<!-- CONTINUED FROM PART 1 -->
<!-- skill — PART 2 of 3 -->

## Function Workflows (Detailed)

### Function 2: Fee Agreement Generator — Workflow

```
Step 1: RECEIVE CLIENT DATA
  -> Accept client_id from Function 1 or manual entry
  -> Load client record
  -> Validate all required fields present

Step 2: SELECT TEMPLATE
  -> standard: Single-family residential (default)
  -> commercial: Commercial properties, higher complexity
  -> condo: Condominium units, master policy considerations
  -> complex: Multiple properties, multiple carriers, high value

Step 3: GENERATE AGREEMENT TEXT
  -> Insert client information into template
  -> Insert property and claim details
  -> Calculate fee amount (percentage of estimated settlement)
  -> Insert all IL-required disclosures (see Templates section)
  -> Add "no up-front fee" clause
  -> Generate unique agreement_id

Step 4: ADD SIGNATURE BLOCKS
  -> Client signature block (with printed name line)
  -> Robert Krapil signature block with IL PA license number
  -> Date fields for both signatures
  -> Witness line (optional, per IL practice)

Step 5: QUALITY CHECK
  -> Verify all required IL disclosures are present
  -> Verify fee does not exceed 10%
  -> Verify cancellation period is exactly 5 calendar days
  -> Flag for Robert's review

Step 6: OUTPUT
  -> Return complete fee agreement document
  -> Status: "draft_pending_review"
  -> Attach review notes for Robert
```

### Function 3: Letter of Representation — Workflow

```
Step 1: RECEIVE CLIENT AND CARRIER DATA
  -> Accept data from Function 1 (Intake) or manual entry
  -> Load appropriate LOR template based on lor_template selection

Step 2: DETERMINE TEMPLATE TYPE
  -> initial_representation: Standard first LOR to carrier
  -> supplemental: Additional LOR for new issues/supplements
  -> appraisal_notice: LOR with appraisal demand
  -> bad_faith_threat: LOR noting potential bad faith actions

Step 3: GENERATE LOR TEXT
  -> Professional letterhead with ClaimEdge LLC contact info
  -> Date and carrier address block
  -> RE: Client name, policy number, claim number, date of loss
  -> Opening: Formal representation notification
  -> Client authorization language (see Templates section)
  -> Request for communication through ClaimEdge only
  -> Request for complete claim file (if selected)
  -> Request for advance notice of inspections
  -> Professional closing with Robert Krapil's credentials

Step 4: ADD CC RECIPIENTS
  -> Always CC client (if cc_client = true)
  -> Add any additional recipients
  -> Note delivery method (certified mail recommended)

Step 5: QUALITY CHECK
  -> Verify all claim numbers and policy numbers are correct
  -> Verify carrier address is complete
  -> Verify client name matches fee agreement
  -> Flag for Robert's review

Step 6: OUTPUT
  -> Return complete LOR document
  -> Status: "draft_pending_review"
  -> Include delivery instructions
```

### Function 4: Statute of Limitations Calculator — Workflow

```
Step 1: RECEIVE CLAIM DATA
  -> Accept date_of_loss from intake or manual entry
  -> Accept claim_type and other relevant fields
  -> Load Illinois SOL rules database

Step 2: CALCULATE DEADLINES BY CLAIM TYPE
  -> Contract claim: date_of_loss + 5 years (735 ILCS 5/13-205)
  -> Property damage: date_of_loss + 5 years (735 ILCS 5/13-205)
  -> Bad faith: date_of_loss + 2 years OR date_denied + 2 years, whichever is later
  -> UM/UIM: per policy terms (typically 2-5 years, flag for review)
  -> Negligence: date_of_loss + 2 years (735 ILCS 5/13-202)

Step 3: APPLY DISCOVERY RULE (if applicable)
  -> If damage was not immediately discoverable:
     -> Use discovery_date instead of date_of_loss
     -> Add note: "SOL calculated from discovery date per discovery rule"
  -> If discovery_rule_applies but no discovery_date: flag for manual review

Step 4: GENERATE ALERT SCHEDULE
  -> 90-day alert: deadline_date - 90 days (warning level)
  -> 60-day alert: deadline_date - 60 days (urgent level)
  -> 30-day alert: deadline_date - 30 days (critical level)
  -> 7-day alert: deadline_date - 7 days (emergency level)
  -> All alerts include specific recommended actions

Step 5: CALCULATE STATUS
  -> > 180 days remaining: "safe" (green)
  -> 90-180 days remaining: "warning" (yellow)
  -> 30-89 days remaining: "urgent" (orange)
  -> < 30 days remaining: "critical" (red)
  -> Past deadline: "expired" (black — flag for attorney referral immediately)

Step 6: GENERATE RECOMMENDATIONS
  -> Based on claim status and days remaining
  -> Include specific next steps (negotiate, appraise, litigate, etc.)
  -> If < 90 days and claim unresolved: recommend attorney consultation
  -> If < 30 days: recommend immediate litigation filing or tolling agreement

Step 7: OUTPUT
  -> Return complete SOL analysis with all deadlines
  -> Return alert schedule with calendar integration notes
  -> Include legal citations for each deadline
  -> Flag any expired or near-expired deadlines
```

### Function 5: Client Communication Preferences — Workflow

```
Step 1: RECEIVE CLIENT DATA
  -> Accept client_id from Function 1 (Intake) or manual entry
  -> Load existing preferences (if updating)

Step 2: COLLECT PREFERENCES
  -> Prompt for preferred contact method
  -> Prompt for best contact times
  -> Prompt for do-not-call window (if phone preferred)
  -> Prompt for alternate contact (spouse, property manager, etc.)
  -> Prompt for language preference and interpreter needs
  -> Prompt for accessibility needs
  -> Obtain explicit text consent (TCPA compliance)
  -> Obtain explicit email consent (CAN-SPAM compliance)

Step 3: VALIDATE CONSENTS
  -> If text_consent = true: record date/time of consent for TCPA
  -> If email_consent = true: record date/time of consent
  -> Note: Cannot send marketing texts without explicit opt-in
  -> Note: Claim-related texts are generally permissible under TCPA

Step 4: SAVE PREFERENCES
  -> Store in client record
  -> Generate compliance note for TCPA
  -> Return confirmation with all preferences listed

Step 5: INTEGRATE WITH WORKFLOW
  -> Set communication rules for this client in all future interactions
  -> Flag if interpreter needed for appointments
  -> Flag accessibility needs for property visits
```

---

## Templates

### Template 1: Illinois-Compliant Public Adjuster Fee Agreement

```
FEE AGREEMENT AND CONTRACT FOR PUBLIC ADJUSTING SERVICES

Agreement ID: {{agreement_id}}
Date: {{agreement_date}}
Effective Date: {{effective_date}}

BETWEEN:

CLIENT:
Name: {{client_primary_name}}
Address: {{property_address_street}}, {{property_address_city}}, {{property_address_state}} {{property_address_zip}}
Phone: {{client_primary_phone}}
Email: {{client_primary_email}}

AND:

ClaimEdge LLC
Public Adjusting Firm
Attn: Robert Krapil, Licensed Public Adjuster
Illinois Public Adjuster License No. {{pa_license_number}}
Address: {{claimgedge_address}}
Phone: {{claimgedge_phone}}
Email: {{claimgedge_email}}

Errors & Omissions Insurance: {{eo_carrier}}, Policy {{eo_policy_number}}

---

1. SCOPE OF SERVICES

ClaimEdge LLC agrees to provide the following public adjusting services to Client:
{{#each scope_of_services}}
- {{this}}
{{/each}}

ClaimEdge LLC shall act as the Client's representative in all dealings with the insurance carrier regarding the claim described herein.

2. PROPERTY AND CLAIM INFORMATION

Property Address: {{property_address_street}}, {{property_address_city}}, {{property_address_state}} {{property_address_zip}}
Insurance Carrier: {{insurance_carrier}}
Policy Number: {{policy_number}}
Claim Number: {{claim_number}}
Date of Loss: {{date_of_loss}}
Type of Loss: {{type_of_loss}}

3. FEE STRUCTURE

Client agrees to pay ClaimEdge LLC a fee equal to {{fee_percentage}}% of the total insurance settlement recovered.

The fee is calculated on the gross amount of the insurance settlement, including any supplemental payments, recoverable depreciation, and additional living expense payments recovered as a result of ClaimEdge LLC's services.

{{#if fee_minimum}}
Minimum Fee: ${{fee_minimum}}
{{/if}}

{{#if fee_cap}}
Maximum Fee: ${{fee_cap}}
{{/if}}

NO UP-FRONT FEE: Client acknowledges that ClaimEdge LLC charges no up-front fees, retainer, or hourly charges. The fee is due only upon recovery of insurance proceeds.

4. PAYMENT TERMS

The fee shall be due and payable within {{payment_due_days}} days of Client's receipt of each insurance settlement payment. If the settlement check is issued jointly to Client and ClaimEdge LLC, the fee shall be deducted at that time. If the settlement check is issued solely to Client, Client shall promptly remit the fee to ClaimEdge LLC.

If Client's mortgage company is named as a loss payee on the settlement check, Client shall use best efforts to facilitate endorsement and promptly remit ClaimEdge LLC's fee upon receipt of funds.

5. CANCELLATION RIGHT — IMPORTANT NOTICE

ILLINOIS LAW GIVES YOU THE RIGHT TO CANCEL THIS CONTRACT WITHIN FIVE (5) CALENDAR DAYS AFTER THE DATE YOU SIGN IT. IF YOU WISH TO CANCEL, YOU MUST SEND A WRITTEN NOTICE OF CANCELLATION TO:

ClaimEdge LLC
Attn: Robert Krapil
{{claimgedge_address}}

The notice must be postmarked no later than {{cancellation_deadline_date}}. If you cancel within this period, you will owe ClaimEdge LLC nothing.

Cancellation Period Begins: {{cancellation_start_date}}
Cancellation Period Ends: {{cancellation_deadline_date}} (11:59 PM)

6. TERMINATION AFTER CANCELLATION PERIOD

After the five-day cancellation period expires, either party may terminate this agreement upon {{termination_notice_days}} days' written notice. If Client terminates after ClaimEdge LLC has performed substantial services, Client shall remain responsible for the fee based on work completed, not to exceed the agreed-upon percentage.

7. NO GUARANTEE OF RECOVERY

ClaimEdge LLC makes no guarantee that any specific amount will be recovered from the insurance carrier. The fee is based on actual recovery, and if no recovery is made, no fee is owed (except as noted in Section 6 for post-cancellation-period termination).

8. NO REFERRAL FEES

Client acknowledges that ClaimEdge LLC does not pay referral fees to contractors, attorneys, or other third parties for referring this claim, as prohibited by 815 ILCS 525/20.

9. FIDUCIARY DUTY

ClaimEdge LLC owes Client a fiduciary duty to act in Client's best interests at all times. ClaimEdge LLC shall keep Client informed of all material developments in the claim and shall not settle the claim without Client's express written authorization.

10. LEGAL SERVICES DISCLAIMER

ClaimEdge LLC is a public adjusting firm, not a law firm. Robert Krapil is a licensed public adjuster, not an attorney. This agreement does not create an attorney-client relationship. If legal advice or representation is needed, ClaimEdge LLC will refer Client to a qualified attorney.

11. RECORDS AND DOCUMENTATION

ClaimEdge LLC shall maintain complete records of all claim-related activities and shall provide copies to Client upon request. All claim documents, photographs, estimates, and correspondence shall remain the property of Client.

12. DISPUTE RESOLUTION

Any dispute arising from this agreement shall first be subject to good-faith negotiation. If unresolved, disputes shall be mediated in {{dispute_resolution_county}} County, Illinois. If mediation fails, either party may pursue legal remedies available under Illinois law.

13. ENTIRE AGREEMENT

This agreement constitutes the entire agreement between the parties and supersedes all prior negotiations, representations, and agreements.

---

CLIENT SIGNATURE:

_________________________________
Signature

{{client_primary_name}} (Print)

Date: _______________

---

PUBLIC ADJUSTER SIGNATURE:

_________________________________
Robert Krapil, Licensed Public Adjuster
Illinois License No. {{pa_license_number}}
On behalf of ClaimEdge LLC

Date: _______________

---

WITNESS (Optional):

_________________________________
Signature

Name (Print): _______________

Date: _______________
```

### Template 2: Letter of Representation — Initial

```
{{claimedge_letterhead}}

Date: {{letter_date}}

{{carrier_department}}
{{insurance_carrier}}
{{carrier_address_street}}
{{carrier_address_city}}, {{carrier_address_state}} {{carrier_address_zip}}

Re: Representation of {{client_primary_name}}
    Policy No.: {{policy_number}}
    Claim No.: {{claim_number}}
    Date of Loss: {{date_of_loss}}
    Property: {{property_address_street}}, {{property_address_city}}, {{property_address_state}} {{property_address_zip}}

Dear Claims Representative:

Please be advised that {{client_primary_name}} has retained ClaimEdge LLC to represent their interests in connection with the above-referenced insurance claim. Robert Krapil, Illinois Licensed Public Adjuster (License No. {{pa_license_number}}), is the assigned representative.

Pursuant to this representation, we hereby request the following:

1. COMMUNICATION DIRECTIVE
Please direct ALL communications regarding this claim to ClaimEdge LLC at the address and contact information below. Do not contact our client directly without first coordinating through our office. All settlement offers, correspondence, requests for documentation, and claim-related inquiries should be directed to:

    ClaimEdge LLC
    Attn: Robert Krapil, Public Adjuster
    {{claimgedge_address}}
    Phone: {{claimgedge_phone}}
    Email: {{claimgedge_email}}

2. CLAIM FILE REQUEST
{{#if request_claim_file}}
Please provide a complete copy of the claim file, including but not limited to:
- All policy documents and endorsements
- All adjuster reports and inspection notes
- All photographs and videos
- All estimates and scopes of loss
- All correspondence to date
- All coverage determinations and denial letters (if any)
- All reserve information
{{/if}}

3. INSPECTION NOTICE
Please provide at least {{inspection_notice_days}} days' advance notice of any scheduled inspections, including the name and contact information of the inspecting adjuster.

4. ESTIMATE SHARING
Please forward a copy of any estimates or scopes of loss prepared by the carrier or its representatives as soon as they are completed.

Our client has authorized ClaimEdge LLC to act on their behalf in all matters related to this claim. A copy of our client's signed authorization is {{#if authorization_attached}}attached{{else}}forthcoming{{/if}}.

We look forward to working cooperatively with you to resolve this claim fairly and efficiently. Please acknowledge receipt of this letter and confirm that all future communications will be directed to our office.

{{#if urgent_response_needed}}
URGENT: This matter requires prompt attention. Please respond within {{urgent_response_days}} business days.
{{/if}}

Sincerely,

_________________________________
Robert Krapil
Licensed Public Adjuster
Illinois License No. {{pa_license_number}}
ClaimEdge LLC

---

CC: {{client_primary_name}} (Client)
{{#each additional_cc}}
    {{this}}
{{/each}}

---

DELIVERY INSTRUCTIONS:
Method: {{delivery_method}}
Tracking: _______________
Date Sent: _______________
```

### Template 3: 5-Day Cancellation Notice (Standalone)

```
NOTICE OF RIGHT TO CANCEL

To: {{client_primary_name}}
Address: {{property_address_street}}, {{property_address_city}}, {{property_address_state}} {{property_address_zip}}
Date: {{agreement_date}}
Re: Fee Agreement No. {{agreement_id}}

YOU HAVE THE RIGHT TO CANCEL THIS CONTRACT WITHIN FIVE (5) CALENDAR DAYS.

You may cancel this contract for any reason by mailing or delivering a signed and dated copy of this cancellation notice or any other written notice to:

    ClaimEdge LLC
    Attn: Robert Krapil
    {{claimgedge_address}}

Your cancellation must be postmarked or delivered by:

    {{cancellation_deadline_date}} at 11:59 PM

If you cancel within this five-day period, you will owe ClaimEdge LLC NOTHING. Any payments made will be refunded within ten (10) business days.

If you do NOT cancel within this five-day period, this contract will remain in effect as written.

---

To cancel, complete and return this form:

[  ] I HEREBY CANCEL the Fee Agreement dated {{agreement_date}} between myself and ClaimEdge LLC.

_________________________________
Client Signature

{{client_primary_name}} (Print)

Date: _______________

---

RETAIN THIS NOTICE FOR YOUR RECORDS.
```

### Template 4: SOL Alert Notification

```
STATUTE OF LIMITATIONS ALERT — ClaimEdge LLC

Alert ID: {{alert_id}}
Claim: {{claim_number}}
Client: {{client_primary_name}}
Property: {{property_address_street}}, {{property_address_city}}, {{property_address_state}}

DEADLINE TYPE: {{deadline_type}}
DEADLINE DATE: {{deadline_date}}
DAYS REMAINING: {{days_remaining}}
ALERT LEVEL: {{alert_level}}

LEGAL BASIS: {{legal_citation}}

RECOMMENDED ACTION:
{{recommended_action}}

CURRENT CLAIM STATUS: {{claim_status}}

This is an automated alert. Please review immediately and take appropriate action. If you have questions about this deadline, consult with counsel.

Generated: {{alert_generated_date}}
```

---

*Continue to PART 3 for examples, dependencies, and legal notes.*

<!-- END PART 2 -->
