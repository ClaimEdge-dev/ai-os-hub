# DEBO Browser Use × GitHub | Governed Adapter Pilot

Status: PROPOSED / BRANCH-ONLY. Date: 2026-11-12 (America/Chicago).
Mission: Extend existing DEBO tool routing, **not** fork Browser Use, replace DEBO Core, or create a second dashboard.

## Verified inputs
- Main repo `ClaimEdge-dev/ai-os-hub`, `DEBO_BOOTSTRAP.md` and `governance/DEBO_TOOL_SELECTION_REGISTER_v1.md` were read directly through GitHub on 2026-11-12.
- Browser Use read-only public trial failed with `insufficient_credits`, meaning its hosted workflow is BLOCKED. No paid upgrade authorized.
- GitHub's code search found no exact `browser-adapter` result; this is not proof that no such component exists elsewhere. Existing guidance already references Playwright for browser E2E and a browser-fallback routing policy.
- Do not infer that Playwright, a runtime, cloud credentials, or browser-plugin backend are installed.

## Proposed delta to existing tool selection (pilot only)
1. **Preferred route:** Native app connector for authenticated structured actions; browser only when UI interaction is truly necessary.
2. **Read-only public route:** Native web/connector first; Browser Use if available and within approved spend limit; on credit exhaustion, fallback to allowed public web research, not a hosted retry.
3. **Reproducible browser QA:** Existing GitHub review + Playwright *if already installed and authorized* on an isolated staging target. If absent, leave an install proposal, not a silent dependency.
4. **Execution card:** project_id, site allowlist, purpose, sensitivity, account identity, operation mode (read-only / reversible / gated write), spend ceiling, required reviewer, timeout, job id, idempotency key, evidence reference, observed result, blocker, rollback.
5. **Security:** Never store cookies, passwords, OAuth tokens, private customer documents, youth data, or signed-in browser traces in the public repo, GitHub artifacts, or public logs. Do not bypass SSO/CAPTCHA, rate limits, payment gates, or tenant permissions. Enforce owner approval before sending, spending, permission changes, public deployment, and production writes.
6. **Fail closed:** Treat unavailable browser credits, missing authorization, unexpected domain redirects, sign-in prompts and ambiguous account identity as BLOCKED. Allow at most one *materially distinct* authorized fallback.
7. **Browser evidence:** Save sanitized observations only to the existing authorized project checkpoint. Label source versions and `PROPOSED/BUILT/TESTED/DEPLOYED/LIVE` separately. UI screenshots are not proof that backend changes occurred.

## First acceptance pilot (on staging, not DEBO-05 production)
- Recover the exact existing deployed dashboard source and staging URL before building any UI test.
- Test safe read-only browser actions: target-domain check, landing-page load, visible read-only task status, duplicate-ID count, stale/unknown labels, and refusal of unauthorized edit controls.
- Negative tests: unrelated domain redirect, missing authentication, expired browser credit, wrong tenant, attempt to upload sensitive files, attempted mutation without approval.
- Preserve v0.2.2 rollback and existing R126/R127 holds. **Do not** expose or activate the editor merely because the UI loads.
- Pilot completion proof: test commands and exact-commit CI receipts, sanitized fixture data, one browser readback if access exists, and no unauthorized writes.

## Execution gates and next action
1. Read-only compare against current Core and existing browser route; avoid duplicate adapter if discovered.
2. Implement the minimum change on this feature branch and run isolated tests.
3. Request review via draft PR only after an actual source change + tests.
4. Do not merge to main or deploy without the normal DEBO review/security gates. Hosted Browser Use remains BLOCKED on credits; GitHub does not resolve billing.

No public/customer website automations are authorized by this proposal.
