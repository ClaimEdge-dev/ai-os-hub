"""Fail-closed provider-neutral routing. Host approval never implies write approval."""
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlsplit
from adapters.browser.request_policy import allowed_readonly_url

Provider = Literal["browser_use", "playwright_readonly", "disabled"]
Mode = Literal["read_only", "interactive_write"]


@dataclass(frozen=True)
class BrowserTaskRequest:
    task_id: str
    entity_scope: str
    mode: Mode
    target_url: str
    workflow_ref: str
    allowed_path_prefixes: tuple[str, ...] = ()
    allow_query_params: bool = False
    allowed_query_keys: frozenset[str] = frozenset()


def select_browser_provider(req: BrowserTaskRequest, browser_use_credits_ok: bool,
                            approved_write: bool = False,
                            allowlisted_hosts: tuple[str, ...] = ()) -> Provider:
    """Use local QA only with explicit paths; never downgrade an interactive write."""
    if not req.task_id.strip() or not req.entity_scope.strip() or not req.workflow_ref.strip():
        return "disabled"
    try:
        p = urlsplit(req.target_url)
        host = (p.hostname or "").lower()
        port = p.port
    except ValueError:
        return "disabled"
    hosts = frozenset(h.lower() for h in allowlisted_hosts)
    if (p.scheme != "https" or not host or p.username or p.password or p.fragment
            or port not in (None, 443) or host not in hosts):
        return "disabled"
    if req.mode == "read_only":
        return ("playwright_readonly" if allowed_readonly_url(
            req.target_url, hosts, req.allowed_path_prefixes, req.allow_query_params,
            req.allowed_query_keys)
            else "disabled")
    if req.mode == "interactive_write" and approved_write and browser_use_credits_ok:
        return "browser_use"
    return "disabled"
