---
name: jct-insurance-invoice-builder
description: Build evidence-linked draft invoices and carrier-ready billing packs for JC's Towing insurance jobs without inventing rates or unsupported charges.
---
# JCT Insurance Invoice Builder

## Global JCT invariants
- Recover existing JC's Towing work before rebuilding.
- Truth states: VERIFIED, PROVISIONAL, CONFLICT, TBD.
- Never invent rates, service capabilities, licenses, authority, fleet capacity, ETAs, contracts, or public claims.
- Preserve source evidence and keep transformations traceable.
- Default to private, reversible work.
- Sending, publishing, spending, account/identity changes, and destructive actions require approval.
- File durable artifacts in the existing JC'S TOWING — DEBO BUSINESS OS structure.
- Return material state changes to JCT-OPS.

## Line-item rule
Every line requires: service basis, quantity/unit, rate source, rate or RATE TBD, extension/amount if supported, and evidence.
## Pack fields
Job summary, dispatch/request, customer/insured/account, vehicle/unit, locations, timestamps, narrative, equipment, labor, mileage, recovery, photos, tow ticket/authorization, storage chronology, itemized invoice, missing-evidence list, QA status, send-approval status.
## Output
Draft invoice + evidence pack outline + missing rate/proof flags + approval gate.
