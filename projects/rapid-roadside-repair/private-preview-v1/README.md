# Rapid Roadside Repair — Private Preview v1

Status: PRIVATE PROTOTYPE / NOT PRODUCTION

This is a zero-dependency private prototype for the RRR workflow:

Request Service → Triage → Dispatch → Job → Evidence → Invoice Ready → Close

## Purpose
- mobile-first Rapid Roadside Repair public-request concept
- internal dispatch/status board
- Business Truth review panel
- local-only synthetic/demo workflow when opened directly

## Safety / release
Do not publish this folder as the public website until:
- Billy confirms public business truth
- service area, hours, services, credentials and rates are approved
- a production backend/auth/privacy model is connected
- request/photo handling is tested
- owner approves release

## Prototype behavior
The form stores submitted demo records in browser localStorage only.
Do not enter real customer personal data into an unapproved/local prototype.

## Files
- index.html — private preview shell
- styles.css — Rapid black/red/chrome theme
- app.js — request intake and dispatch-state demo

## Production migration
Replace browser localStorage with the approved RRR operational CRM/Supabase data model.
Preserve append-only job events and Business Truth gating.
