# DEBO R22 | Isolated synthetic rollback acceptance

Mission DEBO-MASTER-026. Date 2026-11-08. Status: VERIFIED ISOLATED FIXTURE ROLLBACK.

## Scope and approval
Owner explicitly approved temporary test writes **only** on isolated Neon branch slice-day1. Project snowy-block-04251510, branch br-sparkling-forest-a6n5v8rd. No main/production writes authorized.

## Test executed
One PostgreSQL DO statement with nested PL/pgSQL exception subtransaction:
1. Insert synthetic task `DEBO-R22-SYNTHETIC-ROLLBACK-ONLY` with title `DEBO isolated rollback fixture`, Backlog/P3/QA-FIXTURE/DEBO-TEST.
2. Inside subtransaction assert fixture visible exactly once.
3. Raise controlled `DEBO_ROLLBACK_SENTINEL` error; catch it at enclosing block to force PostgreSQL to roll back nested subtransaction.
4. Within same DO statement assert fixture count zero after rollback.
5. Connector returned successful empty result `[]` (not individual SQL assertion output).

## Independent post-test reads
- `SELECT count(*) AS fixture_residue FROM claimedge_os.tasks WHERE task_id='DEBO-R22-SYNTHETIC-ROLLBACK-ONLY'` -> **0**.
- `SELECT count(*) AS all_tasks_after_test FROM claimedge_os.tasks` -> **0**.

## Interpretation
The isolated branch accepted the synthetic fixture and rollback control flow without residue. No real Work Stack IDs were inserted. This does **not** approve status mappings, establish provenance persistence, prove dashboard live sync, or authorize production changes. Rentals remains held.

## Next step
Create a source-preserving offline provenance/mapping proposal; request separate approval before any persistent schema or real-task imports. Existing 14 statuses remain quarantined.
