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
