"""Public, unauthenticated browser QA. Proxy is mandatory but not full OS isolation."""
import os
import tempfile
from dataclasses import dataclass
from adapters.browser.egress_proxy import pinned_https_proxy
from adapters.browser.request_policy import allowed_readonly_url as _allowed


@dataclass(frozen=True)
class ReadOnlyResult:
    ok: bool
    status: int | None = None
    title: str | None = None
    error: str | None = None
    blocked_requests: int = 0


ALLOWED_TYPES = frozenset({"document", "stylesheet", "image", "font"})


def execute_readonly_playwright(target_url: str, allowed_hosts: frozenset[str],
                                timeout_ms: int = 8000,
                                allowed_path_prefixes: tuple[str, ...] = (),
                                allow_query_params: bool = False,
                                allowed_query_keys: frozenset[str] = frozenset()) -> ReadOnlyResult:
    """No direct connections by design; OS egress must separately enforce proxy-only traffic."""
    if not _allowed(target_url, allowed_hosts, allowed_path_prefixes, allow_query_params, allowed_query_keys):
        return ReadOnlyResult(False, error="url_not_allowlisted")
    if not 500 <= timeout_ms <= 15000:
        return ReadOnlyResult(False, error="timeout_out_of_bounds")
    blocked = 0
    try:
        from playwright.sync_api import sync_playwright
        with tempfile.TemporaryDirectory(prefix="debo_browser_") as home:
            env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": home}
            with pinned_https_proxy(allowed_hosts) as proxy_url:
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=True, env=env,
                        proxy={"server": proxy_url},
                    )
                    try:
                        context = browser.new_context(
                            accept_downloads=False, service_workers="block",
                            storage_state=None, java_script_enabled=False,
                        )
                        try:
                            def guard(route):
                                nonlocal blocked
                                req = route.request
                                if (req.method.upper() not in {"GET", "HEAD"}
                                        or req.resource_type not in ALLOWED_TYPES
                                        or not _allowed(req.url, allowed_hosts,
                                                        allowed_path_prefixes, allow_query_params,
                                                        allowed_query_keys)):
                                    blocked += 1
                                    route.abort()
                                else:
                                    route.continue_()
                            context.route("**/*", guard)
                            page = context.new_page()
                            response = page.goto(target_url, timeout=timeout_ms,
                                                 wait_until="domcontentloaded")
                            if not response or not response.ok or not _allowed(
                                    page.url, allowed_hosts, allowed_path_prefixes,
                                    allow_query_params, allowed_query_keys):
                                return ReadOnlyResult(False, error="navigation_rejected",
                                                      blocked_requests=blocked)
                            return ReadOnlyResult(True, response.status, page.title()[:256],
                                                  blocked_requests=blocked)
                        finally:
                            context.close()
                    finally:
                        browser.close()
    except Exception as exc:
        return ReadOnlyResult(False, error=f"browser_error:{type(exc).__name__}",
                              blocked_requests=blocked)
