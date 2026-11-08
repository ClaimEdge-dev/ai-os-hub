# DEBO R79 | WrestlingOS metadata counts and Bulldogs source register discovery

Date 2026-11-08 America/Chicago. Mission DEBO-MASTER-037. Checkpoint R79-METADATA-AND-SOURCE-DISCOVERY-VERIFIED.

## Fresh read-only WrestlingOS checks
Authorized Neon project wrestling-scout-db, main branch, neondb. Queried pg_stat_user_tables for seven domain tables, no athlete rows or identifying details accessed. Estimated n_live_tup: athletes 10; bouts 3; clubs 524; events 1; match_history 59; scouting_reports 0; wrestler_profiles 52. These are PostgreSQL statistics estimates, not exact COUNT(*) and not proof of data correctness. Last autoanalyze on some tables July 2026; others null. The database has 52 public tables per R78.

## Bulldogs authoritative source lead
Fresh Google Drive search found Bulldogs_Master_Source_Truth_Register_2026, spreadsheet ID 1I7pqaZz1MZD9frt6W0pq0xscs1zHfppMeR5-nc0Cmik, last modified 2026-09-25, plus the Bulldogs Build Register updated 2026-11-02. Register content and coach approval not yet read/verified in this batch. Do not promote team truth or film outputs.

## AthleteOS and BaseballOS source recovery
GitHub repository searches under ClaimEdge-dev for standalone AthleteOS and BaseballOS returned no repositories in this read. Existing ai-os-hub athleteos/video-ai/PLAYBOOK_BENCHMARK_v0.2.md is a benchmark, not full app source. BaseballOS remains an unresolved source location. No rebuild initiated.

## Next safe checks
Read Bulldogs spreadsheet metadata and limited non-sensitive provenance columns, not roster/child personal data. Compare film IDs and approval flags where present. Exact counts for selected WrestlingOS tables only if needed for integrity, avoid exporting rows. Search connected authorized builder platforms for existing AthleteOS and BaseballOS app identifiers before starting replacements. Maintain original 15 Work Stack source and 14 isolated tasks, five reported historical IDs unresolved.

## Thread Index
R77 sports sources and Neon visibility -> R78 52-table schema inventory -> R79 metadata-only record estimates and Bulldogs source register discovery.
No production writes, deployments, access changes, spending, or personal records exported.
