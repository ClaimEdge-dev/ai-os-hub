<!-- CONTINUED FROM PART 2 -->
<!-- skill — PART 3 of 3 -->

## Examples

### Example 1: Complete New Client Intake (Hail Damage — Suburban Chicago)

**Context:** A homeowner in Naperville, IL contacts ClaimEdge after a hail storm. They have State Farm insurance, the claim has been filed, and an adjuster is assigned. They want ClaimEdge to represent them.

**Input:**
```json
{
  "intake_date": "2025-07-15",
  "intake_method": "phone",
  "lead_source": "contractor_referral",
  "referral_partner_name": "Mike Johnson",
  "referral_partner_company": "Premier Roofing Naperville",
  "client_primary_name": "Sarah and David Thompson",
  "client_primary_phone": "(630) 555-0142",
  "client_primary_email": "thompson.family@email.com",
  "client_secondary_name": "",
  "property_address_street": "1847 Mill Creek Drive",
  "property_address_city": "Naperville",
  "property_address_state": "IL",
  "property_address_zip": "60540",
  "property_county": "DuPage",
  "property_type": "single_family",
  "property_year_built": 2005,
  "property_occupied": true,
  "property_primary_residence": true,
  "mortgage_company_name": "Chase Bank",
  "insurance_carrier": "State Farm",
  "policy_number": "12-AB-3456-7",
  "claim_number": "SF-2025-789456",
  "claim_filed": true,
  "claim_filed_date": "2025-07-02",
  "date_of_loss": "2025-06-28",
  "type_of_loss": "hail",
  "loss_description": "Severe hailstorm on June 28, 2025. Neighbors reported golf-ball-sized hail. Roof, siding, gutters, and fence all damaged.",
  "damage_areas": ["roof", "siding", "gutters", "fence"],
  "damage_description": "Roof has numerous impact marks on shingles. Siding has dents on south and west elevations. Gutters dented and pulling away in sections. Privacy fence boards cracked and splintered.",
  "prior_repairs": false,
  "prior_claims": true,
  "prior_claims_description": "Water damage claim in 2019 for burst pipe — fully covered",
  "adjuster_assigned": true,
  "adjuster_name": "Jennifer Walsh",
  "adjuster_phone": "(312) 555-0298",
  "adjuster_email": "j.walsh@statefarm.com",
  "adjuster_type": "staff",
  "inspection_completed": true,
  "inspection_date": "2025-07-08",
  "settlement_offered": false,
  "claim_status": "inspected_pending_estimate",
  "fee_percentage": 10.0,
  "scope_of_services": ["inspection", "documentation", "estimate_preparation", "carrier_negotiation", "supplement_filing"],
  "carrier_address_street": "One State Farm Plaza",
  "carrier_address_city": "Bloomington",
  "carrier_address_state": "IL",
  "carrier_address_zip": "61710",
  "carrier_department": "Property Claims Department",
  "request_claim_file": true,
  "cc_client": true,
  "preferred_contact_method": "email",
  "preferred_contact_times": "Evenings after 6pm or weekends",
  "text_consent": true,
  "email_consent": true
}
```

**Output Summary:**
- Intake ID: `CE-INT-2025-0042`
- Client ID: `CE-CLI-0156`
- Fee Agreement: Generated with 10% fee, 5-day cancellation through July 20, 2025
- LOR: Drafted to State Farm Property Claims, Bloomington — requests claim file and communication routing
- SOL: Contract claim deadline June 28, 2030 (1,809 days). Bad faith deadline June 28, 2027 (712 days). Alert schedule generated.
- Communication preferences: Email preferred, evenings/weekends, text and email consent recorded
- Status: All drafts pending Robert's review

---

### Example 2: Fee Agreement Only — Commercial Property (Higher Complexity)

**Context:** ClaimEdge is taking on a commercial property owner with a multi-unit apartment building. The client already completed intake; only the fee agreement needs generation.

**Input:**
```json
{
  "client_id": "CE-CLI-0144",
  "client_primary_name": "Northshore Properties LLC",
  "property_address_street": "8200 N Sheridan Road",
  "property_address_city": "Chicago",
  "property_address_state": "IL",
  "property_address_zip": "60626",
  "property_type": "commercial",
  "insurance_carrier": "Liberty Mutual",
  "policy_number": "LM-C-9876543",
  "claim_number": "LM-2025-112233",
  "date_of_loss": "2025-05-15",
  "type_of_loss": "water",
  "fee_percentage": 10.0,
  "fee_basis": "percentage_of_settlement",
  "fee_minimum": 5000.00,
  "scope_of_services": ["inspection", "documentation", "estimate_preparation", "carrier_negotiation", "supplement_filing", "ale_tracking", "contents_inventory"],
  "agreement_template": "commercial",
  "effective_date": "2025-07-15",
  "additional_terms": "Client maintains their own attorney for any litigation. ClaimEdge LLC will coordinate with counsel but legal strategy decisions rest with Client and their attorney."
}
```

**Output:**
- Agreement ID: `CE-FA-2025-0029`
- Fee: 10% of settlement, $5,000 minimum
- Uses commercial template with additional provisions for multi-unit properties
- Attorney coordination clause included per additional_terms
- 5-day cancellation through July 20, 2025
- Status: Draft pending Robert's review

---

### Example 3: SOL Calculator — Bad Faith Scenario with Denial Date

**Context:** A claim that was denied by the carrier on March 1, 2025. The date of loss was August 15, 2024. Need to calculate all SOL deadlines and generate alerts.

**Input:**
```json
{
  "date_of_loss": "2024-08-15",
  "claim_type": "bad_faith",
  "date_denied": "2025-03-01",
  "policy_type": "ho3",
  "enable_alerts": true,
  "discovery_rule_applies": false
}
```

**Output:**
```json
{
  "sol_analysis": {
    "claim_id": "CE-CLM-2025-0088",
    "date_of_loss": "2024-08-15",
    "calculated_deadlines": {
      "contract_claim": {
        "deadline_date": "2029-08-15",
        "basis": "735 ILCS 5/13-205",
        "years": 5,
        "days_remaining": 1527,
        "status": "safe"
      },
      "bad_faith_claim": {
        "deadline_date": "2027-03-01",
        "basis": "735 ILCS 5/13-202 (discovery rule — denial date)",
        "years": 2,
        "days_remaining": 595,
        "status": "safe"
      },
      "property_damage_claim": {
        "deadline_date": "2029-08-15",
        "basis": "735 ILCS 5/13-205",
        "years": 5,
        "days_remaining": 1527,
        "status": "safe"
      }
    },
    "alert_schedule": [
      { "alert_date": "2026-12-01", "days_before_deadline": 90, "level": "warning", "action": "Review bad faith claim status. Prepare litigation if not resolved." },
      { "alert_date": "2026-12-31", "days_before_deadline": 60, "level": "urgent", "action": "Escalate to attorney. Bad faith SOL approaching." },
      { "alert_date": "2027-01-30", "days_before_deadline": 30, "level": "critical", "action": "File suit or obtain tolling agreement immediately." },
      { "alert_date": "2027-02-22", "days_before_deadline": 7, "level": "emergency", "action": "FINAL DEADLINE — bad faith claim must be filed by March 1, 2027." }
    ],
    "recommendations": [
      "Bad faith claim SOL (2 years from denial) is shorter than contract SOL. Monitor closely.",
      "If pursuing bad faith claim, document all carrier unreasonable delay/denial conduct.",
      "Consider retaining counsel experienced in Illinois insurance bad faith (Cline v. Western States standard).",
      "Contract claim SOL provides backup — claim can still be pursued as contract breach through August 2029."
    ]
  }
}
```

---

## Dependencies

### Internal Skills

| Skill | Dependency Type | How Used |
|-------|----------------|----------|
| `claimedge-compliance-tracker` | **Required** | Validates Robert's IL PA license is current before generating fee agreements |
| `claimedge-vault-system` | **Required** | Stores generated documents (fee agreements, LORs, intake records) |
| `claimedge-session-manager` | **Recommended** | Maintains session context during multi-step intake process |
| `claimedge-carrier-playbooks` | **Optional** | Provides carrier-specific contact addresses and department info for LORs |
| `claimedge-sol-tracker` | **Related** | Function 4 of this skill may be extracted into standalone SOL tracker when built |

### External Systems

| System | Integration Type | How Used |
|--------|-----------------|----------|
| Airtable / CRM | **Required** | Primary client database — intake records stored here |
| DocuSign | **Recommended** | Electronic signature collection for fee agreements |
| Google Calendar / Outlook | **Recommended** | SOL alert calendar entries, cancellation deadline reminders |
| Email Service | **Recommended** | LOR delivery, client communications |
| CompanyCam | **Optional** | Photo documentation linked to intake record |

### Data Requirements

| Data Source | Purpose |
|-------------|---------|
| Robert's IL PA License Number | Required on all fee agreements and LORs |
| ClaimEdge LLC Business Address | Required on all documents |
| ClaimEdge Phone/Email | Required on all documents |
| E&O Insurance Information | Required disclosure on fee agreements |
| ZIP-to-County Lookup | Auto-populate county from ZIP code |
| Illinois SOL Rules Database | Function 4 calculation engine |

---

## Legal Notes

### Illinois Public Adjuster Statutory Requirements

**1. Licensing (215 ILCS 5/1501 et seq.)**
- Robert Krapil must hold a current Illinois Public Adjuster license
- License number must appear on all fee agreements and LORs
- License must be renewed annually
- Skill checks `claimedge-compliance-tracker` before document generation

**2. Fee Limitations (215 ILCS 5/1554)**
- Maximum fee: 10% of the insurance settlement (typical standard)
- Fee must be contingent on recovery (no fee if no recovery)
- No up-front fees, retainers, or hourly charges permitted
- Fee must be clearly stated in the written contract

**3. Cancellation Rights (815 ILCS 525/15)**
- Client has 5 calendar days to cancel the contract
- Cancellation period begins on the date the client signs
- If cancelled within 5 days: no fee owed, any payments refunded within 10 business days
- A separate cancellation notice must be provided (two-document requirement)
- This skill generates both the agreement AND the standalone cancellation notice

**4. Written Contract Requirement (815 ILCS 525/10)**
- All public adjuster contracts MUST be in writing
- Contract must include: scope of services, fee amount, cancellation rights, PA license number
- No oral agreements are binding

**5. No Referral Fees (815 ILCS 525/20)**
- Public adjusters cannot pay referral fees to contractors, roofers, or other third parties
- Fee agreement includes explicit acknowledgment of this prohibition
- Violation is a Class A misdemeanor

**6. Fiduciary Duty (Common Law / 215 ILCS 5/1556)**
- Public adjuster owes a fiduciary duty to the client
- Must act in client's best interest at all times
- Must keep client informed of material developments
- Cannot settle without client's express written authorization

**7. Errors & Omissions Insurance (215 ILCS 5/1553)**
- IL public adjusters must maintain E&O insurance
- E&O carrier and policy number disclosed on fee agreement
- Minimum coverage amounts per Illinois Department of Insurance

**8. Unauthorized Practice of Law**
- Public adjusters CANNOT provide legal advice
- Must refer clients to attorneys for legal matters
- Fee agreement includes clear disclaimer
- LOR language is limited to representation, not legal advocacy

### Illinois Statute of Limitations Reference

| Cause of Action | Statute | Limitation Period | Notes |
|-----------------|---------|-------------------|-------|
| Breach of insurance contract | 735 ILCS 5/13-205 | 5 years | From date of loss or denial |
| Property damage | 735 ILCS 5/13-205 | 5 years | From date of loss |
| Bad faith | 735 ILCS 5/13-202 | 2 years | Discovery rule — from date of denial or unreasonable delay |
| Negligence | 735 ILCS 5/13-202 | 2 years | If applicable to third parties |
| UM/UIM | Varies by policy | 2-5 years | Check policy language; skill flags for manual review |
| Consumer fraud | 815 ILCS 505/10a | 3 years | If carrier misrepresented coverage |

**Discovery Rule:** Under Illinois law, the SOL may be tolled until the plaintiff knew or should have known of the injury. For insurance claims, this typically means the SOL runs from the date of denial or unreasonable delay, not the date of loss. Skill accounts for this in bad faith calculations.

**Tolling Agreements:** When SOL is approaching, a written tolling agreement with the carrier can extend the deadline. Skill recommends this at the 60-day alert level.

### Document Retention

- All fee agreements must be retained for minimum 5 years per IL DOI requirements
- Client intake records retained for 7 years post-claim resolution
- SOL alert logs retained indefinitely for malpractice protection
- Cancellation notices retained for 5 years

---

## Related Skills

| Skill | Relationship | Handoff Trigger |
|-------|-------------|-----------------|
| `claimedge-document-engine` | **Downstream** | After fee agreement signed, generates POL, demand letters, appraisal demands |
| `claimedge-carrier-playbooks` | **Downstream** | After LOR sent, provides carrier-specific negotiation tactics |
| `claimedge-supplement-aging` | **Downstream** | After claim active, tracks supplement submissions and aging |
| `claimedge-bad-faith-tracker` | **Downstream** | If claim denied or unreasonably delayed, documents bad faith timeline |
| `claimedge-xactimate-connector` | **Downstream** | After intake, imports estimate data for line-item analysis |
| `claimedge-photodoc-suite` | **Downstream** | After intake, manages photo documentation for the claim |
| `claimedge-ale-tracker` | **Downstream** | If displacement claim, tracks ALE expenses |
| `claimedge-compliance-tracker` | **Upstream** | Validates license status before document generation |
| `claimedge-referral-network` | **Lateral** | Records referral partner activity for business development |
| `claimedge-master-command-center` | **Orchestrator** | This skill is called from the master command center on new client triggers |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-07-15 | Initial release — all 5 functions (Intake, Fee Agreement, LOR, SOL Calculator, Communication Preferences) |

---

*This skill is proprietary to ClaimEdge LLC. All document templates incorporate Illinois public adjuster law as of July 2025. Robert Krapil must review all generated documents before delivery to clients or insurance carriers. This skill does not constitute legal advice; consult qualified Illinois counsel for legal questions.*

<!-- END PART 3 -->
