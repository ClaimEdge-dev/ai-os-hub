"""Isolated read-only browser QA. Browser requests are not guaranteed side-effect-free."""
from dataclasses import dataclass
from urllib.parse import urlsplit
@dataclass(frozen=True)
class ReadOnlyResult:
    ok: bool
    status: int | None = None
    title: str | None = None
    error: str | None = None
    blocked_requests: int = 0

def execute_readonly_playwright(target_url: str, allowed_hosts: frozenset[str], timeout_ms: int = 8000) -> ReadOnlyResult:
    """Public allowlisted sites only; no authenticated state. Runtime browser must be installed."""
    parsed = urlsplit(target_url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.hostname.lower() not in allowed_hosts or parsed.username or parsed.password:
        return ReadOnlyResult(False, error="url_not_allowlisted")
    blocked = 0
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                context = browser.new_context(accept_downloads=False, service_workers="block", storage_state=None)
                try:
                    def guard(route):
                        nonlocal blocked
                        url = urlsplit(route.request.url)
                        if route.request.method not in ("GET", "HEAD") or url.scheme != "https" or url.hostname not in allowed_hosts:
                            blocked += 1
                            route.abort()
                        else:
                            route.continue_()
                    context.route("**/*", guard)
                    page = context.new_page()
                    response = page.goto(target_url, timeout=timeout_ms, wait_until="domcontentloaded")
                    return ReadOnlyResult(bool(response and response.ok), response.status if response else None, page.title()[:256], blocked_requests=blocked)
                finally:
                    context.close()
            finally:
                browser.close()
    except Exception as exc:
        return ReadOnlyResult(False, error=f"browser_error:{type(exc).__name__}", blocked_requests=blocked)
