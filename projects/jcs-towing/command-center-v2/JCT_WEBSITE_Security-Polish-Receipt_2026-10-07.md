# JCT WEBSITE — Security + Polish Receipt — 2026-10-07

Project: DEBO — JC's Towing Command, Dispatch & Growth OS (JCT)
Workstream: JCT 90 — Website & Digital
Status: PRIVATE REVIEW / PRODUCTION LOCKED

## Recovered
- Existing Lovable/Supabase application remains canonical production-intent system.
- Existing Floot JC's Towing project remains a private build/test surface only, not a second operational CRM/database.
- Existing Request Service V3, My Tow lookup, customer-access, evidence registration and private lead-evidence backend capabilities were reused rather than rebuilt.

## Verified
- Request Service V3 backend contract was inspected read-only.
- My Tow lookup contract was inspected read-only, including its customer-verification and throttling behavior.
- Private lead-evidence bucket constraints and access-policy direction were inspected read-only.
- Production remains unpublished; no domain/DNS mutation or spend occurred.

## Private review build changes
- Browser Request Service traffic now uses a server-side redaction proxy. Customer-facing code receives only the public request reference, not internal lead/storage identifiers.
- My Tow uses a server-side proxy and returns only an allowlisted customer-safe status or generic error. Internal access tokens, timeline data and private records are not forwarded to the customer response.
- Lookup throttling uses a random session identifier rather than customer PII.
- Optional request photos accept up to four images at 8 MB each. The server re-encodes accepted images to WEBP before private storage to remove embedded image metadata.
- First-touch website attribution is session-scoped and removes referrer query strings.
- Privacy copy, Contact-to-My-Tow navigation, and sitemap coverage were refreshed.

## Verification receipts
- Fresh Floot TypeScript typecheck: CLEAN.
- Fresh default Floot tests: 4 spec files passed, 0 failed; Floot's two hook specs were excluded by its default runner.
- Live My Tow proxy smoke using an existing demo record: verified credentials returned only a customer-safe status; a wrong phone returned only generic not-found output.
- Live no-write negative smoke: invalid V3 input returned a generic failed response; a non-image upload was rejected before backend upload.

## Explicit gaps
- Successful synthetic V3 submit through the new proxy with immediate cleanup is still pending.
- Successful real binary photo upload with verified object/evidence cleanup is still pending.
- Staff auth/RLS E2E, staff provisioning, backup/restore drill, and remaining owner truth/rate/fleet gates remain open.
- A later canonical-source integration is still required. Do not treat the private review surface as production.

## Release controls
DO NOT publish, change DNS/domain, spend money, send external customer communications, weaken RLS, create a second operational database, or promote unresolved business facts without the controlling approval and verification gates.

## Related branch
`jct-90-v3-my-tow-parity-2026-10-07`

This receipt contains no secrets, private customer records, or unpublished full application source.
