# DEBO Core: Cortex Semantic Memory bridge — v1.0

## Scope and hierarchy
- One DEBO Core; separate project scopes. Canonical GitHub source, authorized records, and the existing compact Resume Capsule outrank remembered summaries.
- Cortex adds durable retrieval of **non-sensitive settled operational context**, not a second master database or implicit synchronization channel.
- Connection to ChatGPT does not mean a different AI product has authenticated or can read the same memory. Record each external connector identity and successful read separately.

## Allowed memory shape
`title`, short settled decision or verified checkpoint, project scope (when non-sensitive), source URL or revision, evidence status, date if explicit, next safe action, tags. Minimize retention. A provisional concept stays PROPOSED.

## Disallowed and gated information
Do not send special-category personal data, medical details, credentials/tokens, financial account numbers, government identifiers, sensitive customer information, youth/guardian/athlete profiles, private contact lists, or third-party confidential details. Do not sync entire chat threads, Drive documents or repositories. Do not transfer across projects without permission.

## Read workflow
1. Determine whether context is in the current conversation; if yes, do not unnecessarily read Cortex.
2. For user-specific past work: search Cortex narrowly by project/decision; fetch a result only when relevant and trustworthy.
3. Check canonical GitHub or project evidence when a deployment/version/financial/business decision depends on freshness.
4. Record source and conflict; no invented current state.

## Write workflow
1. Confirm user authorization for memory use and content suitability; ordinary settled facts may be captured under ongoing authorization.
2. Deduplicate existing decision and filter sensitive contents.
3. Send one short atomic memory; include source status, no secrets. If `queued`, describe as QUEUED only.
4. On an outcome of SAVED, search and fetch the matching memory before claiming readback. If search not yet indexed, record SAVED but RETRIEVAL UNVERIFIED.
5. For conflicts, surface both candidate claims instead of overwriting silently.

## Acceptance tests
- Positive: non-sensitive governance checkpoint writes, is accepted and can be searched and fetched.
- Negative: no attempt to write credentials, youth information or private client details.
- Duplication: avoid second memory if already found. Never retry rejected duplicates by paraphrasing.
- State truth: no assumption of cross-AI sync; never call queued saved or package install production activation.
- Rollback: stop invoking adapter; use Cortex-specific forget ONLY after explicit confirmation for permanent deletion; restore prior DEBO private plugin release if needed. Canonical sources remain unchanged.

## Verified observations (2026-11-22)
- Cortex tool was callable for scoped search; saved one non-sensitive DEBO governance record (write outcome `SAVED`, ID retained in conversation checkpoint).
- After the queued job returned SAVED, a separate Cortex search found the record and fetch returned its content; the ChatGPT write, index, search and fetch flow passed.
- DEBO private plugin `debo-core-chatgpt` updated v0.3.2 to v0.3.3; readback verified 14 files and nine preserved skills. This bridge extends existing Skill Lifecycle Manager, not a tenth skill.
- GitHub canonical source integration is staged in a reviewable branch/PR, not merged or production activated. Cross-AI testing still needs independent authenticated access from another AI platform.

## Cross-AI continuity acceptance test (HOLD pending an independently connected second client)
1. Connect the same Cortex account to another authorized AI client, in that client's own authenticated environment; record only provider and permitted scope (no credentials).
2. From ChatGPT write one new uniquely labeled non-sensitive synthetic test fact; await saved verdict and verify search/fetch here.
3. In the second client's actual runtime search and fetch that exact fact; record timestamp, account-scope confirmation and citation/receipt.
4. Reverse direction: create a harmless fact from the second client, then verify search/fetch through ChatGPT. Check duplicate/conflict handling and do not promote memory over canonical project evidence.
5. Mark CROSS-AI VERIFIED only after both directions pass. Failure leaves this integration CHATGPT-ONLY TESTED. No automatic sync job, new service or paid API required for planning.

## Evidence status / ownership
- Evidence: private ChatGPT plugin v0.3.3 release; Cortex successful save, search and fetch within ChatGPT.
- Authority: canonical GitHub source plus existing project-specific evidence and Resume Capsule.
- No credentials, confidential information or live provider account IDs in this public repository.
