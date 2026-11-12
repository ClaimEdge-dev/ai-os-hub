#!/usr/bin/env python3
"""Owner-gated Apps Script source installer; does NOT execute Apps Script."""
import argparse
import base64
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request

API = "https://script.googleapis.com/v1/projects/"
# SHA-256 of the independently reviewed 15,143-byte private scanner artifact.
APPROVED_SOURCE_SHA256 = "a4ec85bf14f42f6fe04293c1edbdf1f6a922370110773c01e225d58294122abf"
REQUIRED_SCOPES = {
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/spreadsheets.currentonly",
}
FUNCTIONS = {"deboInitialize", "deboPilotPreflight", "deboScanNextBatch",
             "deboAnalyzeInventory", "deboStatus"}

def reject(reason):
    raise ValueError(reason)

def validate_source(source, manifest):
    if not source or not source.strip():
        reject("Scanner source is empty")
    if set(manifest.get("oauthScopes", [])) != REQUIRED_SCOPES:
        reject("Runtime OAuth scopes differ from approved minimal scopes")
    if manifest.get("runtimeVersion") != "V8":
        reject("V8 runtime required")
    services = manifest.get("dependencies", {}).get("enabledAdvancedServices", [])
    if not any(s.get("serviceId") == "drive" and s.get("version") == "v3" for s in services):
        reject("Advanced Drive API v3 missing")
    for name in FUNCTIONS:
        if not re.search(r"function\s+" + re.escape(name) + r"\s*\(", source):
            reject("Missing scanner function: " + name)
    if re.search(r"\b(?:Drive\.Files\.(?:delete|update|create|copy)|GmailApp|MailApp|UrlFetchApp)\s*\(", source):
        reject("Disallowed Drive mutation, mail, or network operation")
    if "PILOT_FOLDER_ID" not in source or "PAGE_SIZE: 50" not in source:
        reject("Missing direct-folder pilot scope or batch bound")
    return hashlib.sha256(source.encode("utf-8")).hexdigest()

def source_and_manifest():
    encoded = os.environ.get("DEBO_SCANNER_SOURCE_B64", "")
    if not encoded:
        reject("Missing private scanner source secret")
    source = base64.b64decode(encoded, validate=True).decode("utf-8")
    manifest = {
        "timeZone": "America/Chicago",
        "dependencies": {"enabledAdvancedServices": [
            {"userSymbol": "Drive", "version": "v3", "serviceId": "drive"}]},
        "exceptionLogging": "STACKDRIVER",
        "runtimeVersion": "V8",
        "oauthScopes": sorted(REQUIRED_SCOPES),
    }
    digest = validate_source(source, manifest)
    if digest != APPROVED_SOURCE_SHA256:
        reject("Scanner source does not match the independently approved v6.2.2 artifact")
    if not os.environ.get("DEBO_SCANNER_SHA256") or digest.lower() != os.environ["DEBO_SCANNER_SHA256"].lower():
        reject("Scanner SHA256 does not match expected private hash")
    return source, manifest, digest

def request(url, token=None, data=None, method=None):
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode("utf-8")
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(r, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))

def oauth_access_token():
    required = ("DEBO_GOOGLE_CLIENT_ID", "DEBO_GOOGLE_CLIENT_SECRET", "DEBO_GOOGLE_REFRESH_TOKEN")
    if not all(os.environ.get(k) for k in required):
        reject("Missing owner-authorized Google OAuth credentials")
    body = urllib.parse.urlencode({
        "client_id": os.environ[required[0]],
        "client_secret": os.environ[required[1]],
        "refresh_token": os.environ[required[2]],
        "grant_type": "refresh_token",
    }).encode("ascii")
    r = urllib.request.Request("https://oauth2.googleapis.com/token", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(r, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))["access_token"]

def plan_deployment(project, remote, source, manifest):
    host = os.environ.get("DEBO_HOST_SPREADSHEET_ID")
    if not host or project.get("parentId") != host:
        reject("Script project not bound to approved host")
    files = remote.get("files", [])
    by_name = {f.get("name"): f for f in files}
    if len(by_name) != len(files):
        reject("Duplicate remote Apps Script file names")
    for f in files:
        name, kind, code = f.get("name"), f.get("type"), f.get("source") or ""
        if name == "Code" and kind == "SERVER_JS" and (not code.strip() or code == source):
            continue
        if name == "appsscript" and kind == "JSON":
            try:
                obj = json.loads(code)
            except (ValueError, TypeError):
                reject("Existing manifest could not be read")
            if obj in ({}, {"timeZone": manifest["timeZone"]}, manifest):
                continue
        reject("Existing custom code or manifest detected; refusing overwrite")
    installed = (by_name.get("Code", {}).get("source") == source and
                 json.loads(by_name.get("appsscript", {}).get("source") or "{}") == manifest)
    return "ALREADY_INSTALLED" if installed else "ELIGIBLE_EMPTY_PROJECT"

def checked_remote_state(base, token, source, manifest):
    """Read source twice for a stable preflight. Not an atomic write lock."""
    p1 = request(base, token=token)
    r1 = request(base + "/content", token=token)
    state = plan_deployment(p1, r1, source, manifest)
    p2 = request(base, token=token)
    r2 = request(base + "/content", token=token)
    if p1 != p2 or r1 != r2:
        reject("Remote project changed during guarded preflight; refusing deployment")
    if plan_deployment(p2, r2, source, manifest) != state:
        reject("Remote project preflight changed")
    return state

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--deploy", action="store_true")
    args = p.parse_args()
    source, manifest, digest = source_and_manifest()
    project_id = os.environ.get("DEBO_SCRIPT_PROJECT_ID")
    if not project_id:
        reject("Missing private target Apps Script project ID")
    token = oauth_access_token()
    base = API + urllib.parse.quote(project_id, safe="")
    state = checked_remote_state(base, token, source, manifest)
    print("Preflight:", state, "scanner_sha256:", digest)
    if state == "ALREADY_INSTALLED":
        print("No-op: scanner source already matches")
        return
    if not args.deploy:
        print("DRY RUN ONLY; remote unchanged")
        return
    if os.environ.get("DEBO_DEPLOY_CONFIRM") != "INSTALL_V622":
        reject("Missing explicit installation confirmation")
    # Additional last-second check narrows but cannot eliminate updateContent races.
    state = checked_remote_state(base, token, source, manifest)
    if state != "ELIGIBLE_EMPTY_PROJECT":
        reject("Remote project no longer eligible; refusing deployment")
    # The project was confirmed empty. This API replaces all files; never use on active code.
    payload = {"files": [
        {"name": "Code", "type": "SERVER_JS", "source": source},
        {"name": "appsscript", "type": "JSON", "source": json.dumps(manifest, sort_keys=True)},
    ]}
    request(base + "/content", token=token, data=payload, method="PUT")
    after = request(base + "/content", token=token)
    files = {f["name"]: f["source"] for f in after.get("files", [])}
    if files.get("Code") != source or json.loads(files.get("appsscript", "{}")) != manifest:
        reject("CRITICAL: Apps Script source readback mismatch")
    print("SOURCE INSTALLED AND READ BACK. NOT EXECUTED. Owner runtime consent still required.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("HOLD:", str(exc), file=sys.stderr)
        sys.exit(1)
