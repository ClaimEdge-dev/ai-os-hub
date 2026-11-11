# DEBO audit sync: public metadata only

The canonical DEBO Notion audit lane is [07 — Threads, Projects & Branch Control](https://app.notion.com/p/3c6b37124b6781f8b6daf738609e7120). The authoritative code is the [DEBO bootstrap](../../DEBO_BOOTSTRAP.md), and this complements (does not replace) [AUTO_SYNC_PROTOCOL.md](../../AUTO_SYNC_PROTOCOL.md).

This is an additive, audit-only adapter. It does **not** export ChatGPT conversations, move private files, install plugins, deploy apps, change source branches, or prove cross-app activation.

- Source: `main` push, published release, manual run or Sunday 13:00 UTC reconciliation. Pull requests run offline tests only, never access credentials.
- GitHub output: `debo/audit-archive` at `audits/debo/entries/`; one record per source SHA or release tag, updated in place, with readback.
- Notion output: one paragraph block per stable audit ID in existing 07 page. Readback verifies text content; duplicate IDs fail safely.
- Record contents: existing **public repository metadata**, source links, file-category counts and source-tree fingerprint. No original file bytes, private threads, confidential attachments or credential values.
- Release records intentionally do **not** assert a verified source commit or source-tree inventory unless independently verified.
- Auth: GitHub's Actions `GITHUB_TOKEN` with job-scoped contents write for the separate audit branch; `DEBO_NOTION_AUDIT_TOKEN` GitHub Actions secret with edit access to only the designated Notion page. Credentials are never logged.
- Validation: `python -m unittest discover -s tests -p test_debo_audit_sync.py -v` and `python tools/debo_audit_sync.py --dry-run`.
- Partial failures: Action exits nonzero and must not be marked synchronized. Re-running the same key updates existing records rather than adding duplicates.
- Existing main source branches and branch protection are never modified by archive code. No application code is deployed.

**Activation:** Review isolated PR and passing CI first. Add the Notion token to the approved GitHub Actions secret store through an authorized administrator. Merge only after required source/security review and owner promotion. Until then, this is source-built/tested, not live. Never copy any tokens into chat, source files, or Notion blocks.

**Limit:** This is a bounded **GitHub public-source archive**, not the comprehensive private ChatGPT/Drive/Notion project evidence archive. Those sources require separate authorized acquisition, confidentiality classification, and provenance checks.