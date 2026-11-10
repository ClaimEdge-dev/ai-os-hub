# DEBO R153 | Codex Hooks v0.1 review-only candidate

Mission: DEBO-MASTER-153. This source is **not installed**, trusted, approved
or live merely because it is committed. Keep the existing DEBO Core, adapter,
skills, prompt compiler, router and approval gates; this adds no second brain.

## Scope

Project-local hooks in `.codex/hooks.json` invoke
`tools/debo_codex_hook.py` with the existing canonical
`tools/debo_bootstrap_check.py`. Supported events in this candidate:

- **SessionStart**: read the canonical generated brief for the explicitly
  selected `DEBO_PROJECT_ID` (defaults to DEBO); compare the generated view to
  the checked-in brief; inject a short source-based rules excerpt. Private
  checkpoint state remains UNKNOWN until separately retrieved with authorization.
- **PreToolUse**: deny a narrow set of explicitly identifiable high-impact
  shell/MCP actions such as direct PR merge, force push, repo deletion,
  publication or sending. It deliberately **never grants** tool permission.
  It is a heuristic guardrail, not a security boundary or complete command parser.
- **PostToolUse**: produce a short bounded-QA reminder only when a tool response
  clearly indicates failure. It never retries, alters files or logs raw outputs.

No automatic continuation, new schedule, external calls, secret reads, Notion
writeback, customer contact, billing operations or deployment are configured.
Stop/PreCompact/PostCompact are deliberately deferred until their safety and
boundedness can be proven. R149 permission/cost preflight already exists in
review PR #54; no duplicate implementation is introduced here.

## Exact validation

```sh
python3 -m unittest tests.test_debo_codex_hook -v
python3 -m unittest discover -s tests -p 'test_debo*.py' -v
python3 tools/debo_bootstrap_check.py --brief --project DEBO
```

After the review branch passes CI, load it in a **supported local Codex
project** (not an unrelated Work Cloud environment). Inspect project trust,
hooks feature setting and configuration conflicts. Open `/hooks` in the Codex
CLI or Settings > Hooks in the desktop app, review and explicitly trust the
exact definition. Do not use `--dangerously-bypass-hook-trust` for acceptance.

Runtime acceptance, to be performed by an authorized operator:

1. Start a session and verify `SessionStart` provides a source-based brief,
   and labels the private checkpoint UNKNOWN.
2. Invoke a harmless shell command and confirm normal sandbox/permission checks
   still apply.
3. In an **isolated dry test** present a synthetic `PreToolUse` input for
   `gh pr merge` and verify a deny result; do not actually attempt a merge.
4. Supply a synthetic failing command response and verify the `PostToolUse`
   bounded QA hint without echoing private details.
5. Reopen the exact branch/config and compare test and runtime receipts.
   Record what was actually loaded and tested.

Known limitations: project-local hooks need project trust, supported Codex
runtime and configured Python 3; the `python3` command here targets Unix-like
shell environments. Windows and cloud orchestration are not acceptance-tested.
Hook errors or unsupported tool paths may fail open; keep application-level
permissions, GitHub protections, CI and sensitive-data gates. Never call this a
standalone security layer.

Release hold: no merge, public deployment, secret/credential provisioning,
paid service, deletion, sharing, access change or external AI installation
without separate owner-governed approval. Source review does not equal release.

**Next after source CI:** independent source review and local Codex hook trust /
runtime acceptance; add more hooks only if verified value exceeds added risk.
