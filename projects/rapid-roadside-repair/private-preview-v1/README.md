# Rapid Roadside Repair — Private Preview v2

Status: **PRIVATE PROTOTYPE / NOT PRODUCTION**

This is the current zero-dependency RRR prototype for:

**Website Preview → Request Service → Triage → Dispatch → Job → Event/Evidence → Invoice Ready → Fleet Follow-Up**

## What v2 adds
- expanded mobile-first public website preview
- truth-gated service cards driven by `data.js`
- Request Service V2 demo with:
  - name / phone / email
  - company / fleet
  - address/location
  - optional browser geolocation
  - asset class
  - unit / VIN / year-make-model
  - problem category
  - loaded state
  - preferred contact
  - fault codes / scene notes
  - local photo metadata only
- dispatch/job board
- automatic demo dispatch/job IDs as records move through workflow
- append-only local event ledger
- one-click synthetic test scenario
- fleet-account lead intake
- Business Truth gate panel
- production-release checklist

## Safety
Do **not** publish this folder as the live Rapid Roadside Repair website until:
- Billy confirms public business truth
- phone/email/domain are approved
- hours / 24-7 status are approved
- service territory is approved
- public services and exclusions are approved
- equipment/tools and credentials are verified
- an approved RRR rate source exists
- privacy/legal terms are reviewed
- production backend/auth is connected
- request/photo handling passes E2E testing
- owner approves release

## Prototype data behavior
The browser prototype stores demo records in `localStorage` only.

Do not enter:
- real customer personal data
- real payment information
- real confidential fleet data
- real job evidence

The photo input records file names/count only. It does not upload image bytes.

## Files
- `index.html` — private website + CRM shell
- `styles.css` — Rapid black/red/chrome responsive theme
- `data.js` — truth-gated services, Business Truth and release checks
- `app.js` — request, dispatch, event-ledger, fleet and synthetic-test behavior

## Parallel operational CRM
The current private Google Sheet CRM remains the structured operational control surface:

`RRR — Operations CRM + Dispatch — PRIVATE v0.1`

It contains:
Dashboard, Leads, Customers, Assets, Service Requests, Dispatch, Jobs, Job Events, Evidence, Charges, Invoices, Payments, Fleet Accounts, PM Schedule, Vendors, Approvals, Business Truth and Service Capabilities.

A synthetic workflow test was written there on 2026-10-07 using DEMO-only records and zero-dollar charges. It intentionally stops at **INVOICE READY / HOLD** because no owner-approved RRR rate authority exists.

## Production migration
Before production:
1. recover/confirm the approved backend target;
2. connect Request Service to the approved CRM/database;
3. preserve append-only job/lead events;
4. use private evidence storage;
5. implement staff authentication/authorization;
6. connect Business Truth to public page visibility;
7. keep rate authority separate from market benchmarks;
8. complete E2E and rollback tests.

## Explicitly not done
- no public production deployment
- no DNS/domain changes
- no customer outreach
- no ad spend
- no rate publication
- no payment processing
- no unsupported 24/7, credential, service-area or specialty-service claims
