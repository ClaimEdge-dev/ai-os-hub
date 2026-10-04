# JCT P0 — Request Service V3 Backend Receipt

Date: 2026-10-04  
Project: DEBO — JC's Towing Command, Dispatch & Growth OS  
Workstream: JCT 90 — Website & Digital / CRM  
Status: BACKEND IMPLEMENTED + REVIEW UI DEPLOYED

## Canonical Lovable CRM/database

Project ID: `2a656371-38ce-4ada-a7bf-d3b651723ef4`

The existing Lovable/Supabase CRM database was extended in place. No second operational CRM database was created.

### Lead fields added
- preferred_contact_method
- vehicle_type
- rolls
- steers
- shifts
- keys_available
- accident
- wheel_damage
- clearance_issue
- access_notes
- source_page
- referrer
- utm_source
- utm_medium
- utm_campaign
- utm_content
- device_type
- geolocation_lat
- geolocation_lng
- geolocation_accuracy_m

### Lead event ledger
Created `lead_events` as append-only lead history with RLS for staff. A trigger records:
- lead_created
- contacted
- needs_info
- dispatch_pending
- job_created
- completed
- lost
- closed
- duplicate
- quoted
- fallback status_changed

### Request Service V3 RPC
Created `submit_service_request_v3(jsonb)`.

It validates:
- consent
- name
- phone
- pickup
- email length/basic format
- preferred contact method
- vehicle-condition enum values
- recent-request throttling

It writes the expanded lead record and returns:
- lead_id
- lead_number
- upload bucket name
- upload prefix

### Evidence preparation
Extended `evidence_files` for pre-job lead evidence:
- job_id can be null
- lead_id
- mime_type
- file_size_bytes
- marketing_approved default false
- sensitive default true
- source

Created private `lead-evidence` storage bucket with image type/size restrictions.

### Business Truth
Existing business settings were extended without inventing public facts:
- tagline cleared
- public_address_mode = hidden
- public_address empty
- sms_enabled = false
- directions_enabled = false
- recovery = false
- heavy_duty = false
- semi = false
- insurance_towing = false
- property_towing = false

Existing verified values were preserved.

## End-to-end backend test

Public Request Service V3 RPC test PASSED.

Test lead:
- name: DEBO WEBSITE TEST
- source: website
- is_demo: true
- lead_number: 1
- UTM/source fields populated
- vehicle-condition fields populated

This verified anonymous public lead creation into the EXISTING JC CRM.

## Review UI

Updated:
- Higgsfield review implementation
- GitHub static Website V2 review bundle

Review UI now includes:
- Request Service V3
- Use My Location
- preferred contact method
- expanded vehicle fields
- rolls / steers / shifts / keys
- accident / wheel damage / clearance
- access notes
- consent
- first-party source/UTM capture
- DEMO-mode CRM submission
- photo selection/validation

## Photo status

Canonical lead-evidence schema and private bucket exist.

The first anonymous object-upload policy test returned RLS denial because the policy's lead lookup requires a security-definer helper. Do not weaken evidence read access.

This does NOT block Request Service V3 or CRM lead capture. The review build continues while the storage-policy helper is patched during the next database action window.

## Review deployment

Review code deployed to:
https://jcs-towing-v2-review.higgsfield.app

The host currently enforces platform authentication for direct unauthenticated HTTP access. Treat it as a review deployment, not the production public domain.

## No production changes

Not performed:
- jcstowinginc.com DNS change
- production publish
- ad spend
- SMS activation
- external customer messaging
- unsupported service claims
- destructive data migration

## Next

1. Patch lead-evidence upload authorization using a security-definer path check.
2. Apply the already-prepared Request Service V3 UI changes to the canonical Lovable app when Lovable editing capacity is available.
3. Complete Business Truth staff editor.
4. Extend staff lead UI with new P0 fields and source/event history.
5. QA the full lead -> evidence -> staff workflow.
