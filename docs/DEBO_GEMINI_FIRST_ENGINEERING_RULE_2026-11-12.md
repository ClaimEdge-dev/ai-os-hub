# DEBO Golden Rule #22 | Gemini-first, evidence-verified engineering

Status: PROPOSED for adoption into canonical Core governance; feature-branch implementation only.
Date: 2026-11-12 America/Chicago.

## Rule
DEBO Core routes and coordinates. Gemini is the preferred **first-pass implementation candidate** for suitable code, Google Apps Script, integration, and automation work when authenticated access, privacy, cost, and actual performance justify it. GitHub preserves version-controlled evidence and CI. GPT-6 independently reviews consequential changes. Existing owner approvals and security vetoes remain authoritative.

This is a routing preference, not an assertion that Gemini is connected to this runtime or can be invoked directly. Do not pretend a handoff occurred. Prefer the least-cost capable authorized tool; measure turnaround, test pass rate, defects, rework and expense before making routing permanent.

## Provider-neutral browser adapter
- Reuse existing DEBO tool-selection register, project adapters, and browser guidance. No second brain, registry, or dashboard.
- Explicit task ID, entity scope, mode, HTTPS target, exact workflow source ref, and allowlisted destination required.
- Default read-only deterministic tasks to an authorized headless browser when available; credit exhaustion never causes an interactive write to be rerouted silently.
- Writes require separate affirmative approval, authenticated tenant, approved provider, and adequate credits.
- Browser state/cookies/credentials must be isolated per entity and must never be committed or published. GitHub Actions is CI, not an authenticated production browser worker.
- No customer or youth data in public repo or CI logs. No SSO/CAPTCHA bypass, credential transfer, or unrestricted URL fetching.
- Browser Use credit exhaustion: BLOCKED or authorized read-only fallback, never fabricated success.
- Scope isolation is a runtime requirement, not established merely by a routing function.

## Release gates
1. Exact-commit tests and security review.
2. Browser staging readback, scope isolation and negative tests.
3. Independent review of diff and CI.
4. DEBO-05 integration only after verified real task refresh with zero duplicates.
5. Owner approval for protected merge, credentials, spending, production changes or public release.

## Handoff contract
Return: MISSION | SOURCE COMMIT | FILES | TEST COMMANDS/RESULTS | SECURITY FINDINGS | BLOCKERS | NEXT ACTION.
State: PROPOSED / BUILT / TESTED / APPROVED / MERGED / DEPLOYED / LIVE.

## Activation boundary
A committed policy is **not** ChatGPT account-wide memory, global custom instructions, Gemini installation, or automatically synchronized behavior. To make it global, update the existing ChatGPT custom instructions through supported settings and verify readback; likewise independently activate it in Gemini and other runtimes. Do not claim activation without proof.
