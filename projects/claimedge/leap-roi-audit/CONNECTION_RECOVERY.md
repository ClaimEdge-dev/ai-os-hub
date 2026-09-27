# Connection Recovery — Neon / Opera

Status: BLOCKED BY CONNECTOR AUTHORIZATION

## Neon

Observed state:
- Neon app is installed and enabled in ChatGPT.
- Connection is unscoped, so project_id is required.
- Canonical recovered project target: `snowy-block-04251510` (`claimedge-prod`).
- `describe_project`, `list_branches`, and `get_database_tables` all fail before database access with authorization-layer HTTP 404.
- Calling Neon without a project ID confirms the connector is alive but unscoped.
- The connector error references a `list_projects` action, but that action is not exposed in the current tool session.
- No production database write has been attempted.

Required user-side recovery:
1. Open ChatGPT Settings -> Plugins.
2. Open Neon.
3. Reconnect / re-authorize the Neon account that owns `claimedge-prod`.
4. If multiple Neon accounts are available, select the account containing project ID `snowy-block-04251510`.
5. Return to this thread and rerun the read-only project inspection.

Resume sequence after Neon access works:
1. describe project
2. list branches
3. list `neondb` tables
4. inspect existing `claimedge_os` schema and check for `leap_roi` overlap
5. prepare temporary migration branch
6. apply v1 + v2 there
7. run `validation_v1.sql`
8. run rollback-safe `temporary_test_fixture.sql`
9. compare temp branch to parent
10. human approval before production apply

## Opera Browser Connector

Observed state:
- Connector call returns: browser not connected.
- Required user-side recovery:
  1. Open Opera's Browser Connector.
  2. Enable **Allow AI connection**.
  3. Sign in with the Opera account used for the connected browser session.

Opera is optional for Neon if the Neon ChatGPT app is repaired. It is only the fallback lane for checking the signed-in Neon console.

## Safety state

Still intentionally not done:
- no Neon production migration
- no production webhook deployment
- no PR merge
- no recurring reconciliation activation

## 2026-09-27 partial browser recovery

New verified observations:
- Opera Browser Connector briefly connected successfully.
- Signed-in Neon console account label observed: `bobby.huuso`.
- Existing open Neon console tabs were on project `damp-math-10052614`.
- DEBO opened the intended target URL `https://console.neon.tech/app/projects/snowy-block-04251510` in a new Neon Console tab.
- Accessibility tree for that target tab loaded only the shell/account controls before the browser connector disconnected again.
- Browser connector then reverted to: "Browser not connected. Make sure to enable Allow AI connection ... and sign in with your Opera account."

Interpretation:
- target project route is reachable from the current signed-in browser context;
- account/project mismatch is no longer the only hypothesis;
- live schema inspection is still NOT COMPLETE;
- do not claim access to tables/branches/schema until page content or Neon API confirms them.

Resume:
1. reconnect Opera Browser Connector;
2. reopen/read the already-created target project tab if preserved;
3. inspect project identity, branches, databases, and schema read-only;
4. continue normal temporary-branch validation sequence if confirmed.

## 2026-09-27 ChatGPT plugin-state inconsistency confirmed

Verified against the same Neon plugin ID:
`plugin_asdk_app_69e0086d87088191a3edc052fa50c29f`

Observed:
- Plugin directory search reports:
  - display name: Neon
  - status: ENABLED
  - installed: true
- ChatGPT app-permission service reports:
  - same app ID
  - status: not_installed
  - global permission: Allow read actions
- Neon project calls continue to fail before database access with authorization-layer HTTP 404.

Conclusion:
- this is not adequately explained by a bad Neon project ID;
- this is not a SQL/schema failure;
- the ChatGPT Neon connection record is internally inconsistent/stale;
- live Neon access should be treated as CONNECTION_BROKEN until the app is reconnected/re-authorized in ChatGPT.

Do not keep retrying project IDs as the primary recovery strategy.

Required repair:
1. Open ChatGPT Settings -> Plugins.
2. Open Neon.
3. Reconnect/re-authorize the Neon account.
4. If the UI only offers remove/reinstall, preserve current project IDs first, then reconnect deliberately.
5. Resume read-only project inspection immediately after reconnection.

No production Neon changes have occurred.
