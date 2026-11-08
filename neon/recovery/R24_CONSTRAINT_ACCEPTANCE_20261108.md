# DEBO R24 | Isolated provenance constraint acceptance

Mission DEBO-MASTER-026. 2026-11-08. Status: THREE REJECTION GUARDS VERIFIED; LIVE IMPORT NOT APPROVED.

## Verified tests
On isolated Neon slice-day1 only, a PostgreSQL DO block attempted three synthetic cases in independent exception subtransactions:
1. Invalid mapped_status = MadeUp -> CHECK violation caught.
2. import_state = APPROVED without mapped_status/reviewer/timestamp -> CHECK violation caught.
3. Duplicate (source_system,work_id) synthetic inserts -> unique violation caught, enclosing subtransaction rolled back.

The DO block asserted exactly three expected rejections and zero R24 synthetic residue; connector completed successfully. Separate readback confirmed provenance_rows=0 and task_rows=0. Production/main untouched.

## Remaining gates
14 source statuses still require human-reviewed explicit mapping; Rentals remains held. Source objective/owner/project_id to target title/assignee_role/pillar correspondences are proposals, not approved. No real task import or live dashboard transport. Before any import: mapping review, source row hashes/version, provenance permissions and explicit owner import authorization.
