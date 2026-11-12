from contextlib import contextmanager
import sys
from types import SimpleNamespace

from adapters.browser import playwright_readonly as browser


def test_browser_launch_requires_proxy(monkeypatch):
    captured = {}
    @contextmanager
    def proxy(hosts):
        captured["hosts"] = hosts
        yield "http://127.0.0.1:12345"
    monkeypatch.setattr(browser, "pinned_https_proxy", proxy)

    class FakePage:
        url = "https://example.com/status"
        def goto(self, url, **opts):
            return SimpleNamespace(ok=True, status=200)
        def title(self):
            return "DEBO Status"

    class FakeContext:
        def __init__(self):
            self.page = FakePage()
        def route(self, path, fn):
            captured["route"] = fn
        def new_page(self):
            return self.page
        def close(self):
            pass

    class FakeBrowser:
        def new_context(self, **kwargs):
            captured["context"] = kwargs
            return FakeContext()
        def close(self):
            pass

    class FakeChromium:
        def launch(self, **kwargs):
            captured["launch"] = kwargs
            return FakeBrowser()

    class FakePlaywright:
        chromium = FakeChromium()
        def __enter__(self):
            return self
        def __exit__(self, *a):
            pass

    monkeypatch.setitem(sys.modules, "playwright.sync_api", SimpleNamespace(sync_playwright=lambda: FakePlaywright()))
    result = browser.execute_readonly_playwright(
        "https://example.com/status", frozenset({"example.com"}),
        allowed_path_prefixes=("/status",))
    assert result.ok and result.title == "DEBO Status"
    assert captured["launch"]["proxy"]["server"] == "http://127.0.0.1:12345"
    assert captured["context"]["java_script_enabled"] is False
    assert captured["context"]["service_workers"] == "block"
