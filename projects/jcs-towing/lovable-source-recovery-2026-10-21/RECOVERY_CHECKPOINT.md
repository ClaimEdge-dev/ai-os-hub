# JCT 90 — Lovable source reconciliation checkpoint

Date: 2026-10-21
Status: PARTIAL SOURCE RECOVERY / PRIVATE BRANCH / NOT DEPLOYED

## Authorities
- Lovable project: 2a656371-38ce-4ada-a7bf-d3b651723ef4
- Lovable authoritative source ref: ad507d68129f706ef3bbb1eec0684c75b65f1294 (2026-10-11)
- GitHub branch: jct-90-lovable-source-reconciliation-2026-10-21
- Historical GitHub README under command-center-v2 is an engineering receipt, not the latest Lovable source. Preserve site-v1 and command-center-v2.

## Recovered exactly from Lovable
- src/routes/_site/contact.tsx
- src/lib/lead-photos.ts
- drizzle/migrations/0001_lead_evidence_anon_upload_fix.sql
- src/components/staff/LeadDetail.tsx
- src/routes/_authenticated/staff/settings.tsx

These are a **partial source snapshot**, not a runnable complete app. Do not deploy this directory as-is. Additional dependencies, app files, binary assets, environment and migration state remain to be reconciled.

## Current code-level findings
- Contact route calls existing submit_service_request_v3 and offers post-submit evidence upload.
- Evidence upload uses private lead-evidence bucket and register_lead_evidence RPC.
- Existing migration's lead_accepts_public_upload validates recent website lead ID/path but does not prove possession of a lead-scoped authorization secret. Treat as security review hold.
- Staff LeadDetail displays intake, attribution, events and evidence metadata.
- Staff Settings contains an admin-only Business Truth editor.

## Open blockers
- Lovable workspace out of credits; AI builder cannot edit currently.
- Live database read-only policy queries returned 504; migration application unverified.
- No live anonymous photo upload E2E success evidence.
- No full source export, build or test performed in this checkpoint.

## Merge policy
1. Keep Lovable current private app intact.
2. Continue copying and verifying the latest Lovable source to this private development branch; check repository visibility before moving secrets or sensitive content. Never copy .env, private credentials, real customer data or unapproved assets.
3. Compare code to existing command-center-v2 and site-v1; no destructive merges.
4. Fix upload authorization with an unguessable lead-scoped short-lived token, enforce count/type/size/path and staff-only read, then test.
5. Integrate lead -> job -> evidence -> invoice -> payment/collections using existing operational database and Drive artifact links; no second CRM database.
6. Keep all deployment, DNS, ads and external messaging behind explicit approval.

## Next action
Recover the remaining nonsecret Lovable source files and test a complete isolated build, then inspect the existing database policy when read access recovers. Do not report release-ready until tests pass.
