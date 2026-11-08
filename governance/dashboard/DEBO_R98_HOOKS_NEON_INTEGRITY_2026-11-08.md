# DEBO R98 | Cross-project hook tests and WrestlingOS data integrity
Date 2026-11-08 America/Chicago. Mission DEBO-MASTER-039.
Checkpoint R98-6-HOOK-SPECS-NEON-REFERENCES-CLEAN.
Parent R97.

## Actual completed work
Fresh Floot explicit hook specs: AthleteOS useMediaQuery and useDebounce PASS 2/2; Bulldogs Football useMediaQuery and useDebounce PASS 2/2; Morgan's useMediaQuery and useDebounce PASS 2/2. Six files passed, zero failures. This is separate from prior default tests (R94 20 standard files across four apps). No production or published site changes.

Fresh Automations peek: 25 saved tasks. Do not assume they are all enabled, nor reactivate disabled schedules without review.

WrestlingOS Neon dry-recipe-96095818 branch br-mute-sound-ajxbozxr neondb: read-only information_schema columns and foreign key inventory retrieved. Read-only aggregates: athletes 10 rows/10 distinct IDs; bouts 3/3; wrestler_profiles 52/52; clubs 524/524. Zero missing referenced parents for athlete club_id, bout event_id, winner_id, loser_id. These are selected checks, not all-table integrity or real authorization tests. No personal youth rows returned, no SQL mutation.

## Open gates
JCT native Higgsfield authenticated staff + isolated backend E2E and John's approval; dashboard independent logged-out SSO and physical iPhone VoiceOver; AthleteOS guardian server auth; missing BaseballOS canonical build; D-Wing original CRM integration; Perplexity 125-entry audit; release/rollback acceptance. Bulldogs Week 3 accessible tree private verified in R97. Fifty additional batches were requested, but only executed and verified actions can be counted; do not mark future batches completed.
## Next
Check existing CI failures and registry consistency, continue independent tests, checkpoint each meaningful batch, keep releases held.
Thread Index R97 Bulldogs privacy -> R98 cross-app hooks and Neon referential checks.
