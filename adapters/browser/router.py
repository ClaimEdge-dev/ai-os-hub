"""Fail-closed, provider-neutral DEBO browser routing. No network side effects."""
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlsplit

Provider = Literal["browser_use", "playwright_readonly", "disabled"]
Mode = Literal["read_only", "interactive_write"]

@dataclass(frozen=True)
class BrowserTaskRequest:
    task_id: str
    entity_scope: str
    mode: Mode
    target_url: str
    workflow_ref: str

def select_browser_provider(req: BrowserTaskRequest, browser_use_credits_ok: bool,
                            approved_write: bool = False,
                            allowlisted_hosts: tuple[str, ...] = ()) -> Provider:
    """Only approved scoped HTTPS targets may run. Never downgrade a write to read-only."""
    if not req.task_id.strip() or not req.entity_scope.strip() or not req.workflow_ref.strip():
        return "disabled"
    parsed = urlsplit(req.target_url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        return "disabled"
    if not allowlisted_hosts or parsed.hostname.lower() not in {h.lower() for h in allowlisted_hosts}:
        return "disabled"
    if req.mode == "read_only":
        return "playwright_readonly"
    if req.mode == "interactive_write" and approved_write and browser_use_credits_ok:
        return "browser_use"
    return "disabled"
