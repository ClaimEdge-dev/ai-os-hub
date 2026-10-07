# JCT 90 | V3 Request + My Tow Source-Parity Overlay v1.3

**Status: DRAFT PULL REQUEST #8. NOT INTEGRATED OR DEPLOYED.**

This patch reuses the existing JC's Towing Lovable/Supabase application and existing database. The public GitHub repo holds only non-secret helper components; it is NOT a source mirror of the private app.

- Canonical Lovable project ID: 2a656371-38ce-4ada-a7bf-d3b651723ef4
- Canonical inspected code commit: 13bd3246268f74ea552a11377921132bb6054a56
- Draft PR: https://github.com/ClaimEdge-dev/ai-os-hub/pull/8
- Safe private preview: https://id-preview--2a656371-38ce-4ada-a7bf-d3b651723ef4.lovable.app

## What is staged

- src/lib/jct-v3-contract.ts: mapping for existing submit_service_request_v3(p_payload), public lead number only.
- src/lib/jct-first-touch.ts: first-touch session-based attribution and referrer URL privacy.
- src/lib/jct-my-tow-guard.ts: strict allowlist of customer-safe status text; other RPC fields discarded.
- contracts.test.cjs: regression tests for sanitization, type safety, receipt redaction and status filtering.

The current canonical frontend still calls V1. These helpers are NOT wired to it yet.

## Offline test command

Run in this directory with TypeScript installed:

tsc --strict --lib es2020,dom --module commonjs --target es2020 --skipLibCheck --outDir build src/lib/*.ts
node contracts.test.cjs

The previous private parity v1.2 archive passed 14 offline contract assertions. This branch v1.3 has not yet had its exact code independently compiled or tested in a connected CI environment. Do not mark E2E as passed.

## Release gates

1. Recover entire private app source into a suitable **private** source repository or edit Lovable in place when credits permit. Do not publish its source into this public repo.
2. Verify SQL/RPC contract, throttling, My Tow response and photo storage with read-only access.
3. Integrate safely, preserving V1 rollback route.
4. Test with approved synthetic data, staff RLS and photo binaries.
5. Use hosting authorized for commercial use. Existing Vercel claimedge team is Hobby, not suitable for JC's Towing use. No subscription upgrade, spending or deployment was approved.
6. John fact lock, formal production release approval, no DNS or public website changes until then.

**Truth:** new helper files committed, duplicate staging files consolidated, existing website unchanged, no database writes, no spend, no production deployment.
