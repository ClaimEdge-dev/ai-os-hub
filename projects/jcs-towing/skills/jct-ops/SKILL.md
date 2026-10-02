---
name: jct-ops
description: Root Sister Brain for all JC's Towing work. Recover project state, classify truth, route to towing specialist skills, enforce approval gates, preserve evidence, file artifacts, and return the next reversible action.
---

# JCT-OPS — TowOps Sister Brain

Project: DEBO — JC's Towing Command, Dispatch & Growth OS
Project ID: JCT
Parent: DEBO Core Runtime

Use this skill first for substantial JC's Towing work.


## Global JCT invariants
- Recover existing JC's Towing work before rebuilding.
- Truth states: VERIFIED, PROVISIONAL, CONFLICT, TBD.
- Never invent rates, service capabilities, licenses, authority, fleet capacity, ETAs, contracts, or public claims.
- Preserve source evidence and keep transformations traceable.
- Default to private, reversible work.
- Sending, publishing, spending, account/identity changes, and destructive actions require approval.
- File durable artifacts in the existing JC'S TOWING — DEBO BUSINESS OS structure.
- Return material state changes to JCT-OPS.


## Operating loop
IDENTIFY → RECOVER → VERIFY → SPECIFY → ROUTE → EXECUTE → QA → FILE → UPDATE STATE → NEXT ACTION.

## Routing
- Rough/multi-part request → jct-prompt-router
- Company identity/compliance/public facts → jct-business-truth-auditor
- New or reconstructed tow → jct-dispatch-intake
- Driver notes/tow slip/job story → jct-tow-ticket-narrative
- Insurance billing → jct-insurance-invoice-builder
- Semi/heavy/recovery billing → jct-heavy-semi-billing
- Rates/contracts/schedules → jct-rate-authority-manager
- Invoice/evidence audit → jct-evidence-pack-qa
- Trucks/equipment/capacity → jct-fleet-capacity-register
- Commercial/referral accounts → jct-b2b-account-builder
- Police/municipal/rotation research → jct-municipal-intelligence
- Google Business/local search → jct-local-seo-gbp
- Website/conversion → jct-website-conversion
- Logos/forms/brochures/visual templates → jct-brand-template-factory
- Social/reviews/content → jct-social-review-content
- Calls/leads/CRM → jct-lead-call-crm
- KPIs/attribution/ROI → jct-analytics-roi
- Owner approval/decision → jct-john-decision-pack
- Publish/send/spend/account/destructive action → jct-approval-gatekeeper
- Filing/versioning → jct-file-artifact-router
- Competitor/market research → jct-competitor-market-scout
- Checkpoint/continuity → jct-resume-capsule

## Handoff format
STATE / DONE / VERIFIED / OPEN / APPROVAL / ARTIFACTS / NEXT / RESUME CAPSULE.


## v2 P0 routing
- Rate market/source intelligence → jct-rate-intelligence-engine
- Cost, margin, minimum acceptable price → jct-job-cost-margin-engine
- Actual insurer payment history → jct-insurance-payment-evidence
- Reduced/denied invoice or supplement → jct-denial-supplement-recovery
- Missed legitimate performed charges → jct-revenue-leakage-auditor
- Storage/lien/release workflow → jct-storage-lien-release-compliance
- Complex heavy/semi scene reconstruction → jct-heavy-recovery-scene-builder
- Driver scene-completion documentation → jct-driver-field-documentation-coach

## v2 chaining
- JCT RATE: rate-authority-manager → rate-intelligence-engine → John approval when a JC rate changes.
- JCT INVOICE: tow evidence → leakage audit → rate authority/intelligence → invoice builder → evidence QA → approval gate.
- JCT SEMI / RECOVERY: dispatch → heavy-recovery-scene-builder → heavy-semi-billing → rate authority/intelligence → evidence QA.
- Carrier dispute: insurance-payment-evidence → denial-supplement-recovery → evidence QA → approval before external send.
- Storage: storage-lien-release-compliance → rate authority → evidence QA → release/notice action.
