# GB-013 / GB-029 / GB-043 / GB-133 — verified and unknown boundaries

Date: 2026-11-15. REVIEW EVIDENCE ONLY. No user identity, secret values, account configuration, API calls, migrations, hosting changes or spend.

## GB-013 — host identity / resource / issuer / audience

Observed private synthetic Site uses protected Sites dispatch and a scoped owner identity. The source-side flags and identity headers are **not** a cryptographic attestation outside that protected host. Public Sites/plugin documentation describes publishing, access, connection and workspace permissions but does not independently prove the current tenant's actual resource/issuer/audience enforcement or identify an OAuth grant in this runtime.

Status: **PARTIAL / HOST PROOF HOLD**. Before any production provider route, inspect approved actual Site/plugin binding, owner allowlist, authentication propagation and resource/issuer/audience guarantees; perform sanctioned negative tests. No new OAuth server should be created solely to fill a documentary gap. Do not expose an identity-header-trusting Worker publicly.

Reference: https://help.openai.com/en/articles/20001547-hosting-a-plugin-with-chatgpt-sites

## GB-029 — actual managed host limits

The existing repository package uses the managed private ChatGPT Site route, not an owner-proven ordinary Cloudflare Workers account. Public Cloudflare Workers Free D1 or CPU limits cannot establish quotas for that managed destination. Official ChatGPT Sites documentation states Plus/Pro Site hosting is included subject to usage/storage limits; this does NOT reveal the specific remaining allowance, host-side D1 allocation, quota, timer behavior or contractual billing authority.

Actual per-owner/per-Site allowance and remaining usage: **UNKNOWN**. Provider financial eligibility and authorized costs: **UNKNOWN**. No requested account upgrade or billing change. Document exact source entitlement and quota only after an authorized runtime readback.

References:
- https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites
- https://developers.cloudflare.com/workers/runtime-apis/performance/

## GB-043 — non-stored result reconciliation feasibility

Google's Interactions API allows store:false. The official overview states this disables the stored state required for previous_interaction_id continuation and background interactions. The staged transport deliberately uses store:false and background:false. The API also documents a GET endpoint for retrieval, but that **does not** establish retrievability of a non-stored object or any response whose ID/acknowledgment was lost.

Feasibility verdict: **NO RELIABLE AUTOMATIC RECOVERY PROOF** for this staged privacy mode. Maintain UNCERTAIN/CLAIMED durable barriers after timeouts/cancellation, no redispatch or key rotation. Any attempted provider read would require a separate authorized private project, financial and data-retention review. No live GET was made.

References:
- https://ai.google.dev/gemini-api/docs/interactions-overview
- https://ai.google.dev/api/interactions-api

## GB-133 — minimal dependency decision

The existing private package manifest declares zero runtime dependencies and ships web-standard ESM; tests use Node's test runner and built-in SQLite. The current task, which is a staged and unactivated policy/contract layer, needs **no new SDK**, credential manager, OAuth framework, public proxy, paid browser, database, or second agent framework. Reuse its existing modules and the canonical R19 adapter. Change this decision only for a reproduced gap with a pinned version, license, security review, cost evaluation and a rollback.

Evidence: packages/debo-gemini-mcp/package.json and scripts/build.mjs in PR #81. This does not assert that future hosted source has no managed dependencies.

## Follow-up owner gates

Host attestation, actual provider eligibility, credential-project binding, any nonbillable live contract test, independent review, private migration, release, and separate-chat R19 acceptance are all **not performed**. This document is not an activation instruction.
