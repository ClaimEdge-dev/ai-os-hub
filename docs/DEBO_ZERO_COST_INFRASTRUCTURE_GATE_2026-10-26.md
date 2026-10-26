# DEBO $0 infrastructure gate — 2026-10-26

**Owner instruction:** Spend $0. Do not upgrade, purchase, enable overage billing, subscribe, or create billable resources without a separate, specific owner approval.

## Verified account and plan constraints

- Supabase connected organization `xghhcwolyxovophyizgx` has two ACTIVE_HEALTHY projects, RRR and an older separate project. Supabase Free permits two active projects across owned/admin organizations; do not commandeer either project, especially RRR. Official: https://supabase.com/docs/guides/platform/billing-on-supabase .
- Vercel connected team `claimedge` has four existing projects. Pricing/plan tier for this specific team was not exposed by the connector. Vercel Hobby is $0 but its terms restrict use to non-commercial/personal projects. Official: https://vercel.com/docs/plans/hobby .
- Neon Live Bridge access remains unavailable to the exposed connection. Preserve its historical identity and data.

## Decision

Do not provision a paid Supabase third project, do not host DEBO's business workflows on a Vercel Hobby plan contrary to its terms, and do not share a database with another company or project to evade a free quota. No charge has been authorized.

## Safe $0 work path

1. Continue tested code in the canonical `ClaimEdge-dev/ai-os-hub` feature branch, with GitHub Actions and review gates.
2. Use local-only SQLite and the loopback command API for nonsensitive development/test data; this does not make DEBO accessible over the public internet.
3. Keep real customer, financial, medical and youth records out of local prototypes and public repositories.
4. Prepare a provider-independent Postgres adapter and migration tests offline; do not apply to an existing production database.
5. For an iPhone-accessible live DEBO, identify a dedicated compliant free hosting+database account with actual unused quota, or obtain a specific approval for costs. Never label an unhosted local UI as live.

## Current status

CODE: TESTED LOCALLY, CI VERIFIED.  HOSTED BACKEND: BLOCKED BY FREE-QUOTA/ACCOUNT LIMITS.  PAID CHARGES: $0 authorized, none initiated by this gate.  PRODUCTION DEPLOYMENT: NOT STARTED.
