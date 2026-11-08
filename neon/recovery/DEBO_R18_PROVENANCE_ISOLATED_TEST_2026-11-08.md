# DEBO R18 | Isolated provenance fixture test

Date 2026-11-08. Mission DEBO-MASTER-024. Status: TESTED IN ISOLATED SECONDARY BRANCH; NOT DEPLOYED.

Target original Neon project snowy-block-04251510, branch slice-day1 (br-sparkling-forest-a6n5v8rd). SQL single-statement DO block created a session-local temporary provenance fixture table with work_id PRIMARY KEY, raw_source_state NOT NULL, mapped_status constrained to five accepted statuses, and source_hash NOT NULL. Fixture WORK-CE-001 inserted with original verbose status; repeated upsert was guarded by source hash. SQL assertions required one row after insert, one row after repeat, exact original source state preserved, and zero rows after explicit deletion. SQL completed successfully (tool returned [] and did not expose intermediate assertions). Table used ON COMMIT DROP; no persistent schema change. Independent subsequent SELECT from claimedge_os.tasks returned target_rows=0. No actual Drive task imported, no production SQL.

**Important limitation:** The fixture's normalized status 'In Progress' is a synthetic test input, NOT an approved mapping for WORK-CE-001. This does not establish a reviewed mapping matrix, persistent provenance ledger, authenticated source-to-target sync, or dashboard refresh. Do not call integration accepted. Future work requires reviewed status mapping, schema design approval, durable ledger implementation, sync implementation and actual end-to-end acceptance. Rentals stays owner-PARKED.

Checkpoint: R18-PROVENANCE-TEMP-FIXTURE-PASS.
