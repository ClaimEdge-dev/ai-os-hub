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


## v2 P1 routing
- Commercial/fleet account terms → jct-commercial-rate-contract-manager
- Motor club / roadside network → jct-motor-club-network-manager
- Police/municipal application packet → jct-municipal-rotation-application-builder
- Commercial prospect pipeline → jct-b2b-pipeline-manager
- Invoice aging/payment follow-up → jct-ar-payment-collections
- Dispatcher quote decision → jct-dispatch-pricing-guardrail
- CRM object/schema work → jct-crm-data-model
- CRM automation/workflow → jct-crm-workflow-automation
- Missed inbound call → jct-missed-call-recovery

### P1 chaining
- New commercial account: B2B pipeline → rate intelligence/margin → contract manager → CRM.
- Dispatcher quote: CRM/account lookup → pricing guardrail → approved rate/contract → dispatch.
- Invoice lifecycle: invoice/evidence QA → AR → payment evidence → denial recovery when reduced.
- Municipal opportunity: municipal intelligence → rotation application builder → John approval before submission.


## v2 document + digital routing
- Website pre-release audit → jct-website-release-qa
- Website lead/form to CRM mapping → jct-website-crm-sync
- Reusable template governance → jct-template-library-manager
- Brand QA → jct-brand-consistency-qa
- Verified-data template population → jct-document-auto-fill
- Artifact version/status lineage → jct-document-version-controller

### Document chain
template-library-manager → document-auto-fill → brand-consistency-qa → domain/evidence QA → document-version-controller → approval gate.

### Website chain
business-truth-auditor → brand-consistency-qa → website-release-qa → website-crm-sync → approval gate → deployment.
