# Trackwrestling Public Evidence Intake — Source-Only Adapter (2026-11-22)

Extends the existing `wrestling-extraction-suite`; it is NOT a new scraper brain, licensed provider integration or live data service.

## Trigger and source route
When an authorized owner asks to research one wrestler's public bouts or event history: official Trackwrestling season-match viewer → public event brackets → FloWrestling public athlete overview → approved saved HTML/CSV/PDF → source reconciliation. Track viewer: https://support.trackwrestling.com/en/article/22f6d5-view-season-matches-viewer . Premium scouting overview: https://support.trackwrestling.com/en/article/6addaa-access-and-use-flowrestling-scouting-reports .

## Enforcement
- Public visibility != automated copying permission. Check provider terms, robots, licensing and exact account permissions before collection. Stop at sign-in, paid features/paywalls, CAPTCHA, forbidden robots or ambiguous permission. Do not use proxies, stealth, session cookies, private endpoints or bulk crawling.
- Prefer official exports and human-saved public source snapshots. Only if allowed: one read-only Playwright-rendered page at a time with conservative pacing.
- Keep original source URL (sanitize `twSessionId`, `TIM`, access tokens), capture UTC, SHA-256, event/date/division/weight/round, wrestler identity as listed, opponent, result, score perspective and method. Never infer a record from a page title alone.
- `RAW → PARSED → CANDIDATE_MATCH → REVIEWED → CANONICAL`; each review must be attributable. Never silently merge by child name, delete duplicate candidates, count BYEs as contested wins, or treat unverified scrape counts as official career totals.
- Output `source_manifest`, `match_candidates`, `reconciliation_queue` and a short checkpoint, marked SOURCE_ONLY / REVIEW / VERIFIED separately.

## Approved research code candidates
Playwright (Apache-2.0) for permitted dynamic pages, Python standard library + BeautifulSoup for owner-provided HTML/CSV; `vehbiu/opentw-api` (MIT code) is an independent reference to audit, not automatically install. GitHub source license does not license Trackwrestling data.

## QA
Local synthetic fixtures, no-network default, URL token refusal, score/forfeit conflict handling, source pointer SHA, negative/no-permission case, and exact artifact readback. Owner-specific wrestling records stay outside public DEBO code. Existing project release and youth-privacy gates remain.

**State:** RESEARCH/REFERENCE READY; parser and mobile adapter are locally tested in the separate private owner package, NOT installed in DEBO runtime or continuously fetching.
