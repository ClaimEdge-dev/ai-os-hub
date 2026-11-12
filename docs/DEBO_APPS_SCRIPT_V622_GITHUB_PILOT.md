# DEBO v6.2.2 | Private Apps Script source deployment gate

**State: prepared source-install workflow, NOT a live Apps Script execution.**

This is a guarded `workflow_dispatch` action for an authorized, *previously created, empty, bound* Google Apps Script project. The repository is public. Do not commit private scanner source, folder IDs, spreadsheet IDs, credentials, or customer data. No scheduled trigger is created.

The GitHub workflow uses the existing canonical DEBO repository, not a new master. It cannot bypass Google sign-in or OAuth consent.

## Additional safeguards (PR #71 review)
- The installer pins the reviewed private v6.2.2 `Code.gs` SHA-256 in code. A caller-controlled secret hash alone cannot authorize an arbitrary replacement. Regular expressions are only defense-in-depth checks, not a source security proof. Any scanner update requires a new source review and explicit pinned-digest code change.
- The target is required to be a previously created empty Apps Script project **bound to the approved host**. A double-read before preflight and another double-read immediately before installation stop if source/metadata changes during either check.
- **Remaining limitation:** Google Apps Script `projects.updateContent` does not provide an atomic compare-and-swap precondition in this implementation. A concurrent external edit in the final tiny gap could still be overwritten. Therefore installation is held until the owner confirms this is an isolated project with no other editors, automation, or active workflows. Do not describe this as race-free or production-safe merely because tests pass.
- Run independent CI on the checked-in test suite and inspect the diff before enabling installation. Deployment remains HOLD until OAuth and project isolation are confirmed.

## Security and setup
An administrator must explicitly configure GitHub environment `debo-google-pilot` and make its install operation approval-gated when supported. Configure the following as encrypted **environment secrets**, never as committed values:

- `DEBO_SCANNER_SOURCE_B64`: exact private v6.2.2 Code.gs in base64 (encoding is not encryption).
- `DEBO_SCANNER_SHA256`: hash of that same source, verified against private source.
- `DEBO_SCRIPT_PROJECT_ID`: Apps Script project ID, not the host spreadsheet ID.
- `DEBO_HOST_SPREADSHEET_ID`: approved bound host workbook.
- `DEBO_GOOGLE_CLIENT_ID`, `DEBO_GOOGLE_CLIENT_SECRET`, `DEBO_GOOGLE_REFRESH_TOKEN`: authenticated owner-authorized Google OAuth credentials with Apps Script project-edit scope `https://www.googleapis.com/auth/script.projects`. The deployment API authorization is separate from scanner runtime scopes.

Use Google OAuth's official sign-in and consent. Do not ask ChatGPT or agents to receive raw tokens/passwords. A personal Gmail account must not be assumed to support service-account impersonation.

## Operation
1. Verify the correct account, approved host spreadsheet, and existing Apps Script content. Preserve any existing code and triggers.
2. Run workflow with `preflight` (default). It validates the private source/hash, OAuth, bound parent, and target. No writes.
3. If the project has *any* existing custom code, additional files, or nondefault manifest, stop. Do not use `install` until an isolated empty project is established. Back up any existing source privately.
4. Run `install` only after explicit owner review of the authenticated target and environment authorization. It performs Apps Script API `projects.updateContent` only for verified empty projects, and reads content back.
5. **Installation is not execution.** In authorized Apps Script, grant the scanner's separate runtime scopes (`drive.metadata.readonly`, `spreadsheets.currentonly`), run `deboPilotPreflight`, `deboInitialize`, one `deboScanNextBatch` (maximum 50), `deboStatus`, and `deboAnalyzeInventory` only after completeness is checked.
6. Verify six intended `Pilot_*` tabs, direct-parent IDs, counts, completeness, no Drive file mutations, and preserve four preexisting dashboard tabs. Write a real-run receipt to the **existing** Trace Run Ledger only after live verification.

Google Apps Script `projects.updateContent` replaces the entire remote project file set. The script will **refuse an existing project with nonempty code or unknown manifest** instead of clobbering it. Neither this workflow nor its tests claim a live scanner installation, authorization, or Drive mutation audit.

## Known blocker
Google OAuth owner consent, GitHub environment configuration, authenticated script project ID, and first authorized live execution are not yet verified. No tool can mint those permissions or bypass Google's security challenge on the owner's behalf.
