---
name: debo-private-export-recovery
description: Recover and inventory authorized private ChatGPT ZIP exports and historical skill attachments when an archive is truncated or an existing conversation's evidence needs reconciling. Use for incomplete ChatGPT exports, original attachment-byte recovery, private archive inventories, or export-to-checkpoint reconciliation. This is a narrow adapter to the canonical DEBO skill-lifecycle-manager, not a new master brain.
---

# DEBO Private Export Recovery

## Before starting

1. Load DEBO_BOOTSTRAP.md, the DEBO runtime brief, the selected project checkpoint, and the existing skill-lifecycle-manager workflow. Do not create a second brain, registry, or scheduled task.
2. Confirm the user owns or is authorized to process the input. Keep chat archives, conversations, attachments, IDs, hashes that identify private records, and sensitive outputs in private user-controlled storage. Never push them to a public GitHub repository.
3. Recover read-only first. Do not delete, archive, overwrite or automatically install anything found in an export.

## Procedure

1. Inventory each input: original filename, byte size, SHA-256, file signature, archive integrity and private destination. Verify the original source is preserved unchanged.
2. If a ZIP is missing its central directory, use the local tool tools/debo_zip_salvage.py with --output PRIVATE_RECOVERED_ZIP and --report PRIVATE_REPORT. The tool supports only complete unencrypted stored/deflated members with known local-header sizes and rebuilds the central directory. It does NOT recover partial members or prove authenticity. Fail closed on encryption, unknown sizes or unsupported compression.
3. Require crc_all_complete_members_pass=true, inspect recovered member count, and explicitly label the archive PARTIAL when any original entries are missing.
4. For an accessible ChatGPT export, use tools/debo_export_inventory.py with --private-report PRIVATE_REPORT to count conversations, message nodes and missing indexed assets. Keep thread names/IDs in the private report only.
5. For recovered skills, compare source contents with the canonical GitHub skill registry and private Notion registry. A SKILL.md file or legacy ACTIVE label is not an installed or tested skill. Protect overlapping skill names and unverified legal, financial, insurance and medical claims from blind activation.
6. Prepare an evidence-based delta: source bytes/hashes, recovered files, unresolved missing members, duplicate/provenance decisions, applicable tests, public-safe source changes, owner gates, and one exact next action.
7. Update the existing private Thread Index/checkpoint only through an authorized connector; verify its readback. Otherwise label NOT_SAVED. Do not claim automatic fresh-chat activation.

## Verification and release

- Test on a synthetic normal ZIP and a synthetic truncated ZIP; test preserved original, excluded incomplete member and CRC readback.
- Keep recovered private ZIP bytes and metadata out of CI logs and public PRs; never process untrusted archive members by executing them. Avoid automatic extraction of paths or symlinks.
- Use separate gates for source created, tested locally, code reviewed, merged to GitHub, installed in an actual AI runtime, and production live.
- No spend, outbound message, production write, public deployment, permission change or sensitive-data transfer without the owner-approved gates.

## Output

Return recovered artifact references, integrity proof, missing items, exact destination, skill overlap findings, runtime installation truth and the smallest next action. Route general skill authoring back to skill-lifecycle-manager.
