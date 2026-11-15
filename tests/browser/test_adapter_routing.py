import importlib.util
from pathlib import Path

path = Path(__file__).resolve().parents[2] / "adapters/browser/router.py"
spec = importlib.util.spec_from_file_location("debo_browser_router", path)
module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)
Request = module.BrowserTaskRequest
route = module.select_browser_provider


def request(**changes):
    args = dict(task_id="t-1", entity_scope="DEBO-CORE", mode="read_only",
                target_url="https://example.com/test", workflow_ref="repo/path@sha",
                allowed_path_prefixes=("/test",))
    args.update(changes)
    return Request(**args)


def test_readonly_uses_zero_credit_fallback():
    assert route(request(), False, allowlisted_hosts=("example.com",)) == "playwright_readonly"


def test_credit_exhaustion_blocks_write():
    assert route(request(mode="interactive_write"), False, True, ("example.com",)) == "disabled"


def test_write_requires_explicit_approval():
    assert route(request(mode="interactive_write"), True, False, ("example.com",)) == "disabled"


def test_approved_write_uses_browser_use():
    assert route(request(mode="interactive_write"), True, True, ("example.com",)) == "browser_use"


def test_wrong_tenant_or_missing_scope_denied():
    assert route(request(entity_scope=""), True, True, ("example.com",)) == "disabled"
    assert route(request(), True, True, ("another.example",)) == "disabled"


def test_unsafe_urls_denied():
    for url in ("http://example.com", "file:///etc/passwd",
                "https://user:pass@example.com", "https://example.com.evil.test"):
        assert route(request(target_url=url), True, True, ("example.com",)) == "disabled"
