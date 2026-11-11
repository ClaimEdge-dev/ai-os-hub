# DEBO R1 private-export recovery candidate (source review only)

Purpose: safely repair a truncated ZIP that still contains complete local-header members, then inventory authorized ChatGPT export metadata. This is a narrow additive capability, not another master, registry, agent, scheduler, data store, or automatic loader.

## Canon

- Recover DEBO_BOOTSTRAP.md and governance/runtime-briefs/DEBO.md before DEBO project work.
- Reuse the existing skill-lifecycle-manager and tools/debo_skill_delta.py to reconcile registries; do not install bulk historical skill packs without overlap/claims review.
- Never modify or destroy the original archive. Recovered ZIP files are derived, partial copies.
- Private conversation titles, content, asset data, IDs, upload hashes and private receipts must remain out of this public repository and CI logs.

## Usage in a private authorized environment

python tools/debo_zip_salvage.py ORIGINAL.zip --output RECOVERED.zip --report PRIVATE_CRC_REPORT.json

python tools/debo_export_inventory.py RECOVERED.zip --private-report PRIVATE_INVENTORY.json

Run the synthetic tests:

python -m unittest tests.test_debo_zip_salvage tests.test_debo_export_inventory -v

And canonical skill checks:

python tools/debo_skill_delta.py --include-projects --validate-contracts

## Constraints

- Local-header ZIP recovery is intentionally limited to member entries with known sizes, method 0 or 8, no encryption, and no ZIP64 or data descriptors.
- CRC32 ensures decompression/integrity under ZIP rules, not SHA authenticity or full original archive completeness.
- The inventory reads metadata from the export; it never uploads or automatically archives/deletes threads, merges conversations, or grants app access.
- It does not install ChatGPT skills, change account Memory, or run in the background.
- Any release requires exact-head CI, independent source/security review, separate owner-governed merge decision and a real runtime activation/readback test.
- Mac .dmg media, screenshots, claim/customer/youth records and export bytes are not public code dependencies.

## Current disposition

Source-review candidate only. A passing local unittest run does not establish exact-head GitHub CI, independent code review, private-vault save or production activation.
