# DEBO R25 | Source tests and integration checkpoint

Mission DEBO-MASTER-026. 2026-11-08. Status: SOURCE TESTS COMMITTED / CI TRIGGERED, RESULT NOT YET VERIFIED.

Fresh canonical Google Drive Portfolio Work Stack read: 15 unique work IDs, 14 non-Rentals, Rentals held. Created `neon/recovery/r25_source_mapping_offline_test.py` with eight unittest cases: source count, 14 quarantines/1 hold, deterministic SHA256 fingerprint, source-change detection, duplicate rejection, missing-field rejection, priority rejection, Rentals hold and no implicit mapping approval (eight methods). Uses limited source metadata (ID, project, original status, priority); no customer details or credentials. This is a snapshot, not live polling.

Fixed a known CI regression in `governance/dashboard/test_r21_receipt_adapter.py` (hardcoded historical run #5 despite receipt now referencing #7). Added R25 test to `.github/workflows/debo-r20-turbo-ci.yml` on dev branch, which triggers on workflow changes. CI conclusion still pending independent readback; do not claim passing yet.

Earlier R24 isolated database safeguards passed (invalid status, unreviewed approval, duplicate), zero residue. No real imports, no production writes, no live dashboard sync. 14 mappings need explicit per-ID review, Rentals held. Next: verify GitHub Actions CI outcome, repair any failure, then prepare explicit per-ID mapping review and controlled first import approval.
