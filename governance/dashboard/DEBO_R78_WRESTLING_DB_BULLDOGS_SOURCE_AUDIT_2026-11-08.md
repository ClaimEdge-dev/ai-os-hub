# DEBO R78 | WrestlingOS DB schema and Bulldogs build-register audit

Date 2026-11-08 America/Chicago. Mission DEBO-MASTER-037.
Checkpoint R78-WRESTLING-DB-52-TABLES-BULLDOGS-BUILD-REGISTER-VERIFIED.
Status READ-ONLY INVENTORY VERIFIED; no record restoration or release.

## WrestlingOS historical database
Neon authorized claimedge connection, project wrestling-scout-db (dry-recipe-96095818). list_branches returned one default main branch br-mute-sound-ajxbozxr, state ready, no protected flag. list_postgres_databases returned one neondb. get_database_tables and independent read-only information_schema count verified 52 public base tables, of which 6 are zz_deprecated-prefixed and 7 are named core domain tables (athletes, wrestler_profiles, events, bouts, clubs, match_history, scouting_reports). Other tables include tournament, opponent, audit, waiver, and operational data. Do not infer row counts or quality from table presence. No personal/youth rows fetched or exported. No writes, restores, migrations, role or permission changes. The default main branch is not the isolated 14-task dashboard branch.

## Bulldogs source evidence
Fresh Google Drive fetch of DEBO — Tinley Park Bulldogs — Build Register, file 18FNalNejHNYdXayMYVjIsfYXSP0O-mvAMzzP8Gx8gLg (modified 2026-11-02). Explicitly records DEBO-TPB-OS parent brain ACTIVE, Team Truth/Playbook RECOVERY REQUIRED, AthleteOS ACTIVE + RECOVERY REQUIRED, QB warm-up ACTIVE, Chase development ACTIVE CHILD LAYER, Film Intelligence ACTIVE + RECOVERY REQUIRED. These are the document's own historical labels, not freshly tested deployed runtime. Preserve coach approvals, youth privacy and original film source.

## GitHub code recovery
GitHub search in ClaimEdge-dev/ai-os-hub located athleteos/video-ai/PLAYBOOK_BENCHMARK_v0.2.md, a benchmark, not full AthleteOS app. No verified application repository recovered in this run.
BaseballOS appears in governance role/coverage documents as Buddy Boy Sports / BaseballOS umbrella, but this is organizational grouping and not proof of shared database or a working app. Prior Drive Hitters UDC folder listing was empty; full canonical source remains unresolved.

## Security
Earlier unauthenticated browser check of R61 deployment reported Vercel login for both main page and API, with no exposed task JSON. That is R61-specific evidence; do not substitute it for a fresh R69 anonymous denial test. R69 currently has project SSO enabled by Vercel config, but independent negative test still outstanding.

## Next batch
1. Read-only metadata-only row counts for WrestlingOS domain tables if necessary; do not expose athlete details.
2. Locate Bulldogs film ledger and coach-approved source register; verify provenance before importing.
3. Recover AthleteOS code via approved connected source, and BaseballOS source without rebuilding.
4. Complete R69 anonymous negative test and accessible browser QA with an appropriate test context.
5. Keep public project health UNKNOWN until live operational tests, and preserve R66 rollback.

Thread Index: R76 fresh Work Stack -> R77 project source and Neon visibility -> R78 DB schema and Bulldogs build-register recovery.
