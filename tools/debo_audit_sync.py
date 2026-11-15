#!/usr/bin/env python3
"""DEBO public-metadata-only audit sync. No original source bytes are archived."""
import base64
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
from urllib import error, parse, request

REPO = "ClaimEdge-dev/ai-os-hub"
BRANCH = "debo/audit-archive"
PAGE_ID = "3c6b3712-4b67-81f8-b6da-f738609e7120"  # existing DEBO 07 lane
GH = "https://api.github.com/repos/" + REPO
NOTION = "https://api.notion.com/v1"

class SyncError(Exception):
    pass


def stable_id(kind, source):
    if kind == "commit":
        if not re.fullmatch(r"[0-9a-f]{40}", source):
            raise SyncError("invalid commit SHA")
        return "commit-" + source
    if kind == "release":
        if not source or len(source) > 200:
            raise SyncError("invalid release tag")
        return "release-" + hashlib.sha256(source.encode()).hexdigest()[:24]
    raise SyncError("unsupported source kind")


def category(path):
    if path.startswith(".github/workflows/"):
        return "workflows"
    if path.startswith("tests/") or "/test_" in path:
        return "tests"
    if path.startswith(("docs/", "governance/", "records/")) or path.endswith((".md", ".rst")):
        return "documentation"
    if path.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mp4", ".pdf", ".zip")):
        return "assets_or_builds"
    if path.endswith((".py", ".js", ".ts", ".tsx", ".json", ".yml", ".yaml", ".sql", ".sh")):
        return "source"
    return "other"


def tree_summary(entries):
    files = [x for x in entries if x.get("type") == "blob"]
    counts = {k: 0 for k in ("source", "documentation", "tests", "workflows", "assets_or_builds", "other")}
    total = 0
    h = hashlib.sha256()
    for x in sorted(files, key=lambda r: r["path"]):
        path, sha = x["path"], x.get("sha", "")
        counts[category(path)] += 1
        total += int(x.get("size") or 0)
        h.update((path + "\0" + sha + "\n").encode())
    return {"file_count": len(files), "listed_bytes": total, "categories": counts, "tree_fingerprint_sha256": h.hexdigest()}


class Api:
    def __init__(self, github_token, notion_token=""):
        self.github_token = github_token
        self.notion_token = notion_token

    def call(self, service, method, url, data=None, missing_ok=False):
        token = self.github_token if service == "github" else self.notion_token
        headers = {"Authorization": "Bearer " + token,
                   "Accept": "application/vnd.github+json" if service == "github" else "application/json",
                   "User-Agent": "DEBO-Audit-Metadata-Only/1.0"}
        if service == "notion":
            headers["Notion-Version"] = "2022-06-28"
        if data is not None:
            headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode() if data is not None else None
        for attempt in range(4):
            req = request.Request(url, data=body, headers=headers, method=method)
            try:
                with request.urlopen(req, timeout=20) as resp:
                    return json.load(resp)
            except error.HTTPError as exc:
                if exc.code == 404 and missing_ok:
                    return None
                if exc.code in (429, 500, 502, 503, 504) and attempt < 3:
                    time.sleep(min(2 ** attempt, 8))
                    continue
                raise SyncError(f"{service} HTTP {exc.code} on {method}") from None
            except (error.URLError, TimeoutError):
                if attempt < 3:
                    time.sleep(min(2 ** attempt, 8))
                    continue
                raise SyncError(f"{service} transport failure on {method}") from None
        raise SyncError(f"{service} retries exhausted")

    def github(self, method, path, data=None, missing_ok=False):
        return self.call("github", method, GH + path, data, missing_ok)

    def notion(self, method, path, data=None):
        return self.call("notion", method, NOTION + path, data)


def source_from_event(event_name, event, api):
    if event_name == "release":
        release = event.get("release", {})
        tag = release.get("tag_name", "")
        stem = stable_id("release", tag)
        # Release tags are not treated as verified commit SHAs without dereferencing.
        return stem, "release", tag, None, release.get("html_url")
    if event_name not in ("push", "workflow_dispatch", "schedule"):
        raise SyncError("unapproved event")
    if event_name == "push" and event.get("ref") != "refs/heads/main":
        raise SyncError("push outside approved main branch")
    if event_name == "push":
        sha = event.get("after", "")
    else:
        ref = api.github("GET", "/git/ref/heads/main")
        sha = ref["object"]["sha"]
    return stable_id("commit", sha), "commit", sha, sha, f"https://github.com/{REPO}/commit/{sha}"


def build_manifest(api, event_name, event, run_id, observed_at):
    stem, kind, source, commit_sha, source_url = source_from_event(event_name, event, api)
    if kind == "commit":
        commit = api.github("GET", "/commits/" + commit_sha)
        tree_sha = commit["commit"]["tree"]["sha"]
        tree = api.github("GET", "/git/trees/" + tree_sha + "?recursive=1")
        if tree.get("truncated"):
            raise SyncError("GitHub tree truncated; refusing incomplete inventory")
        inventory = tree_summary(tree.get("tree", []))
        tree_url = f"https://github.com/{REPO}/tree/{commit_sha}"
    else:
        inventory = None
        tree_url = None
    return {"schema_version": 1, "audit_id": stem, "repository": REPO,
            "source_branch": "main" if kind == "commit" else None,
            "source_type": kind, "source": source, "source_commit_sha": commit_sha,
            "source_url": source_url, "tree_url": tree_url,
            "inventory": inventory, "event": event_name, "last_run_id": str(run_id),
            "last_observed_utc": observed_at, "private_material_status": "EXCLUDED_NOT_EXPORTED",
            "external_chat_threads": "NOT_VERIFIED_NO_AUTHORIZED_EXPORT",
            "redaction": "No source bytes, credentials, personal records, or private exports copied",
            "inventory_status": "VERIFIED_PUBLIC_GITHUB_METADATA" if kind == "commit" else "RELEASE_METADATA_ONLY"}


def github_archive(api, manifest):
    stem = manifest["audit_id"]
    path = f"audits/debo/entries/{stem}.json"
    ref = api.github("GET", "/git/ref/heads/" + BRANCH, missing_ok=True)
    if ref is None:
        default_ref = api.github("GET", "/git/ref/heads/main")
        api.github("POST", "/git/refs", {"ref": "refs/heads/" + BRANCH, "sha": default_ref["object"]["sha"]})
    route = "/contents/" + path
    old = api.github("GET", route + "?ref=" + parse.quote(BRANCH, safe=""), missing_ok=True)
    data = json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    if old is None or base64.b64decode(old["content"]).decode() != data:
        payload = {"message": "audit(debo): upsert public metadata " + stem,
                   "branch": BRANCH, "content": base64.b64encode(data.encode()).decode()}
        if old:
            payload["sha"] = old["sha"]
        api.github("PUT", route, payload)
    readback = api.github("GET", route + "?ref=" + parse.quote(BRANCH, safe=""))
    if base64.b64decode(readback["content"]).decode() != data:
        raise SyncError("GitHub audit file readback mismatch")
    return f"https://github.com/{REPO}/blob/{BRANCH}/{path}"


def notion_record_text(manifest, archive_url):
    inv = manifest["inventory"] or {}
    return (f'DEBO-AUDIT-ID:{manifest["audit_id"]} | {manifest["inventory_status"]} | '
            f'{manifest["source_type"]}={manifest["source"]} | files={inv.get("file_count", "n/a")} | '
            f'run={manifest["last_run_id"]} | UTC={manifest["last_observed_utc"]} | '
            f'GitHub archive: {archive_url} | original private files and ChatGPT exports: NOT VERIFIED/EXCLUDED')


def notion_upsert(api, page_id, manifest, archive_url):
    target = notion_record_text(manifest, archive_url)
    if len(target) > 1900:
        raise SyncError("Notion audit record exceeds text limit")
    marker = "DEBO-AUDIT-ID:" + manifest["audit_id"]
    cursor, existing = None, None
    while True:
        query = "?page_size=100" + ("&start_cursor=" + parse.quote(cursor) if cursor else "")
        response = api.notion("GET", "/blocks/" + page_id + "/children" + query)
        for block in response.get("results", []):
            texts = block.get("paragraph", {}).get("rich_text", [])
            combined = "".join(t.get("plain_text", t.get("text", {}).get("content", "")) for t in texts)
            if marker in combined:
                if existing:
                    raise SyncError("duplicate Notion audit IDs exist; manual reconciliation needed")
                existing = (block["id"], combined)
        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")
        if not cursor:
            raise SyncError("Notion pagination missing cursor")
    paragraph = {"rich_text": [{"type": "text", "text": {"content": target}}]}
    if existing:
        block_id = existing[0]
        if existing[1] != target:
            api.notion("PATCH", "/blocks/" + block_id, {"paragraph": paragraph})
    else:
        response = api.notion("PATCH", "/blocks/" + page_id + "/children",
                              {"children": [{"object": "block", "type": "paragraph", "paragraph": paragraph}]})
        block_id = response["results"][0]["id"]
    saved = api.notion("GET", "/blocks/" + block_id)
    actual = "".join(t.get("plain_text", t.get("text", {}).get("content", ""))
                     for t in saved.get("paragraph", {}).get("rich_text", []))
    if actual != target:
        raise SyncError("Notion record readback mismatch")
    return f"https://www.notion.so/{page_id.replace('-', '')}#" + block_id.replace("-", "")


def main():
    dry = "--dry-run" in sys.argv
    event_name = os.environ.get("GITHUB_EVENT_NAME", "workflow_dispatch")
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    event = json.load(open(event_path, encoding="utf-8")) if event_path else {}
    if dry:
        # Deterministic offline fixture: no network, credentials, or destination writes.
        fixture = {"repository": REPO, "source_type": "commit", "audit_id": stable_id("commit", "a" * 40),
                   "inventory": tree_summary([{"type": "blob", "path": "docs/README.md", "sha": "abc", "size": 20}])}
        print(json.dumps({"dry_run": True, "id": fixture["audit_id"], "count": fixture["inventory"]["file_count"]}))
        return 0
    gh_token = os.environ.get("GITHUB_TOKEN", "")
    notion_token = os.environ.get("NOTION_TOKEN", "")
    notion_page = os.environ.get("DEBO_NOTION_AUDIT_PAGE_ID", PAGE_ID)
    if not gh_token or not notion_token:
        raise SyncError("required GitHub or Notion CI secret unavailable; nothing marked synchronized")
    if not re.fullmatch(r"[a-fA-F0-9-]{32,36}", notion_page):
        raise SyncError("invalid Notion page ID")
    api = Api(gh_token, notion_token)
    observed = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    manifest = build_manifest(api, event_name, event, os.environ.get("GITHUB_RUN_ID", "manual"), observed)
    archive_url = github_archive(api, manifest)
    notion_url = notion_upsert(api, notion_page, manifest, archive_url)
    print(json.dumps({"status": "VERIFIED_BOTH_DESTINATIONS", "audit_id": manifest["audit_id"],
                      "git": archive_url, "notion": notion_url, "redactions": "private content excluded"}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (SyncError, KeyError, ValueError, OSError) as exc:
        # Do not emit provider responses or request headers to CI logs.
        print("DEBO_AUDIT_FAILED: " + str(exc).splitlines()[0][:160], file=sys.stderr)
        raise SystemExit(1)