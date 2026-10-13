# Canonical Neon Migration Order

Status: ACTIVE CONTROL

## Run only this sequence

1. `migration_v1.sql`
2. `migration_v2_event_history.sql`
3. `validation_v1.sql`
4. `temporary_test_fixture.sql` on the temporary Neon branch only

## Superseded files

Do **not** run:
- `migration_v1_1_hardening.sql`
- `validation_queries.sql`

Those files were produced in a parallel hardening pass and overlapped the canonical v2 schema with incompatible definitions for `webhook_events` and `sync_runs`.

Their original contents are preserved under:
- `../archive/migration_v1_1_hardening.superseded.sql`
- `../archive/validation_queries.superseded.sql`

## Why v2 is canonical

Canonical v2 combines the useful hardening from both parallel passes:

- job number tracking
- import idempotency keys
- webhook durability
- sync/reconciliation history
- reconciliation findings
- stage/cycle-time history
- owner snapshots
- latest-field completeness logic
- optional / not-applicable handling
- verified vs estimated vs modeled time
- strict verified-dollar filtering
- source freshness / sync health

## Production gate

Production remains blocked until:

1. Neon authorization works;
2. existing schema is inspected read-only;
3. duplicate/overlap preflight is clean or reconciled;
4. temporary branch is created;
5. canonical migrations pass;
6. read-only validation passes;
7. rollback-safe fixture passes;
8. temporary schema is compared with parent;
9. human explicitly approves production apply.
