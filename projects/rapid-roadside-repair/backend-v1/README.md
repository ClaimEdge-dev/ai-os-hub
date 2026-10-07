# Rapid Roadside Repair — Backend v1 Migration Pack

Status: **PREPARED / NOT APPLIED**

This folder converts the current private browser + Google Sheet prototype into a production-ready Supabase/Postgres shape without touching an unidentified production database.

## Why this is not applied yet

The connected Supabase account currently exposes one project named `bobbyhuuso-alt's Project`. Its database metadata calls timed out during recovery and there is no verified evidence that it belongs to Rapid Roadside Repair. DEBO therefore did **not** migrate it.

## Target flow

Request Service
→ Lead
→ Service Request
→ Dispatch
→ Job
→ append-only Events
→ Evidence
→ Charges
→ Invoice
→ Payment
→ Fleet Follow-Up

## Files

- `001_core_schema.sql` — RRR tables, enums, indexes and updated_at triggers
- `002_rls.sql` — deny-by-default RLS with authenticated staff access
- `003_submit_service_request.sql` — public RPC for minimum safe service-request intake
- `004_business_truth_public_view.sql` — public truth view exposing only approved fields
- `005_private_evidence_storage.sql` — private evidence bucket + staff policies only
- `006_seed_hold_defaults.sql` — non-public starter truth/service rows
- `007_synthetic_test.sql` — rollback-only demo request-chain test

## Release rules

Do not apply to any database until:
1. the correct RRR backend project is identified;
2. a backup/branch or other reversible path exists;
3. owner truth is loaded;
4. privacy and staff-access design is approved;
5. synthetic tests pass;
6. production deployment is explicitly approved.

## Evidence upload

This pack intentionally does **not** allow anonymous direct photo uploads. Request Service can be launched without weakening evidence privacy. Add a signed-upload or security-definer path after the backend target is verified and tested.

## Rates

No RRR dollar rate is present in this schema. Rate authority is stored as a separate source reference and official pricing remains owner-controlled.


## Frontend adapter

The private preview contains `config.js` and `backend.js`.

Default mode is `local`, so the preview keeps demo data in the browser. The adapter is ready to call the RRR request RPC after the correct backend is verified and configured. It must not be pointed at an unidentified database.

## Current verification

- private preview JavaScript syntax: PASS
- required local file references: PASS
- noindex/private preview guard: PASS
- Google Sheet CRM synthetic workflow to INVOICE READY / HOLD: PASS
- Supabase/Postgres migrations: NOT APPLIED
