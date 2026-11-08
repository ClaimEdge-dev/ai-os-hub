# DEBO R23 | Provenance schema isolated installation acceptance

Mission DEBO-MASTER-026. 2026-11-08. Status VERIFIED INSTALLED ON ISOLATED BRANCH ONLY.

Owner explicitly approved persistent schema installation on isolated Neon branch slice-day1, project snowy-block-04251510, branch br-sparkling-forest-a6n5v8rd. Production/main not changed.

Executed CREATE TABLE IF NOT EXISTS claimedge_os.task_source_provenance according to R23 design. Independent readback: 17 columns, zero rows, four constraints: primary key, import_state CHECK, mapped_status CHECK, and approved/imported reviewer gate CHECK.

Executed synthetic INSERT into provenance table inside a nested PL/pgSQL subtransaction, verified fixture visible once inside it, raised a controlled exception to roll back, and asserted zero fixture residue in outer block. Connector completed successfully. Independent post-test reads: provenance rows **0**, target task rows **0**.

This proves schema creation and basic synthetic rollback, **not** invalid-value constraint rejection, duplicate rejection, persistent approved mapping, real import, dashboard live sync, production migration or production security/RLS. No real Work Stack IDs inserted. Rentals remains owner held.

Next: test invalid status/approval constraint and duplicate primary key using rollback-only fixtures, then review exact per-ID mapping proposals and provenance permissions before real import. Never silently coerce compound statuses.
