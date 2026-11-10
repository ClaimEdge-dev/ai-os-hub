---
name: debo-career-opportunity-scout
description: Recover and qualify verified contract, freelance and employment leads for DEBO CAREER without duplicating listings, inventing fit or submitting applications.
---

# DEBO Career Opportunity Scout v1.0 (STAGED)

## Trigger
Use for user-requested paid-work discovery and each authorized recurring job-search run. Recover DEBO Core and the DEBO CAREER checkpoint first. Not a background agent until separately scheduled and verified.

## Inputs
- Source-backed career facts and proof, including unknowns (never invent employment)
- User geography, schedule, compensation preference if actually known
- Current job pages and original link, company, dated listing, eligibility and location
- The existing lead register for duplicate checks

## Contract
1. Search one or more authorized sources, with cost and privacy gates. Do not claim unsupported Upwork/Contra/Fiverr API connectivity.
2. Keep freelance project, employment, and sell-my-services lanes separate.
3. Preserve original posting URL, date observed, whether an application page was directly checked, salary in its actual units, employer/client, location, work setting, skill requirements and approval gate.
4. Deduplicate by normalized URL and company/title when URL changes. Do not turn a search-index result into a confirmed open slot. If link returns 403, mark STATUS_UNKNOWN; if 410/404, hold or exclude.
5. Exclude location-ineligible roles, licensing-restricted positions and pay-to-work schemes. Flag low-pay and vague-scope work for judgment.
6. Compare credentials against verified evidence; score prospect fit only with explicit uncertainty. Avoid false precision. Treat production engineering claims as unproven unless there is tested delivery evidence.
7. Select up to five best eligible leads and one highest-value next task. Link originals, show fit, pay as published, deal-breakers and freshness. Never apply, message, share client material, or spend without specific owner approval.
8. Save one delta in existing DEBO CAREER registry; read back. Statuses: FOUND / DIRECTLY_VERIFIED / QUALIFIED / READY_FOR_APPROVAL / APPLIED_WITH_RECEIPT.

## Proof tests
- Source link and observed date present
- Eligibility and compensation units checked or UNKNOWN
- Zero duplicate lead keys
- No user identity/client secret in public GitHub
- No application claim without platform submission receipt

## References
Canonical DEBO bootstrap, DEBO communications standard, DEBO CAREER Notion registry. Do not duplicate DEBO Core, task registry or scheduler.
