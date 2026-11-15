import http.client
import ipaddress
import socket

import pytest

from adapters.browser.egress_proxy import (
    EgressDenied, pinned_https_proxy, resolve_pinned_endpoints,
)
from adapters.browser.request_policy import allowed_readonly_url
from adapters.browser.router import BrowserTaskRequest, select_browser_provider


def _dns(ip, family=socket.AF_INET):
    return [(family, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", (ip, 443))]


@pytest.mark.parametrize("ip", [
    "127.0.0.1", "10.1.2.3", "172.16.0.1", "192.168.1.1",
    "169.254.169.254", "0.0.0.0", "100.64.0.1",
])
def test_private_dns_is_rejected(monkeypatch, ip):
    monkeypatch.setattr(socket, "getaddrinfo", lambda *a, **kw: _dns(ip))
    with pytest.raises(EgressDenied, match="non_public_dns_answer"):
        resolve_pinned_endpoints("example.com", frozenset({"example.com"}))


def test_mixed_public_private_dns_fails_entire_target(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", lambda *a, **kw: _dns("93.184.216.34") + _dns("127.0.0.1"))
    with pytest.raises(EgressDenied, match="non_public_dns_answer"):
        resolve_pinned_endpoints("example.com", frozenset({"example.com"}))


def test_public_answer_returns_numeric_socket_address(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", lambda *a, **kw: _dns("93.184.216.34"))
    assert resolve_pinned_endpoints("example.com", frozenset({"example.com"})) == (
        (socket.AF_INET, ("93.184.216.34", 443)),)


def test_dns_not_queried_if_host_not_approved(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("unapproved hostname caused a DNS lookup")
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)
    with pytest.raises(EgressDenied, match="host_not_allowlisted"):
        resolve_pinned_endpoints("evil.example", frozenset({"example.com"}))


@pytest.mark.parametrize("url", [
    "https://example.com/delete", "https://example.com/logout",
    "https://example.com/approve/123", "https://example.com/status/../admin",
    "https://example.com/status/%2e%2e/approve",
    "https://example.com/status?token=secret",
    "https://example.com/status?approved=true",
    "https://example.com:444/status", "https://user:password@example.com/status",
    "https://example.com.evil.test/status",
])
def test_readonly_url_fails_closed(url):
    assert not allowed_readonly_url(url, frozenset({"example.com"}), ("/status",))


def test_query_opt_in_does_not_allow_mutating_queries():
    assert allowed_readonly_url("https://example.com/status?sort=asc",
                               frozenset({"example.com"}), ("/status",), True, frozenset({"sort"}))
    assert not allowed_readonly_url("https://example.com/status?token=abc",
                                   frozenset({"example.com"}), ("/status",), True, frozenset({"sort"}))


def test_root_scope_matches_home_only():
    assert allowed_readonly_url("https://example.com/", frozenset({"example.com"}), ("/",))
    assert not allowed_readonly_url("https://example.com/unknown", frozenset({"example.com"}), ("/",))


def test_router_requires_explicit_readonly_path_allowlist():
    req = BrowserTaskRequest(task_id="t1", entity_scope="DEBO", mode="read_only",
                             target_url="https://example.com/status", workflow_ref="src@sha")
    assert select_browser_provider(req, False, allowlisted_hosts=("example.com",)) == "disabled"
    req2 = BrowserTaskRequest(task_id="t1", entity_scope="DEBO", mode="read_only",
                              target_url="https://example.com/status", workflow_ref="src@sha",
                              allowed_path_prefixes=("/status",))
    assert select_browser_provider(req2, False, allowlisted_hosts=("example.com",)) == "playwright_readonly"


def test_proxy_rejects_plain_http_without_external_network():
    from urllib.parse import urlsplit
    with pinned_https_proxy(frozenset({"example.com"})) as proxy:
        p = urlsplit(proxy)
        c = http.client.HTTPConnection(p.hostname, p.port, timeout=3)
        c.request("GET", "http://example.com/status")
        r = c.getresponse()
        assert r.status == 405
        c.close()


def test_proxy_rejects_non_allowed_connect_without_dns(monkeypatch):
    from urllib.parse import urlsplit
    original = socket.getaddrinfo
    def guarded(host, *a, **kw):
        if host == "127.0.0.1":
            return original(host, *a, **kw)
        raise AssertionError("unapproved hostname caused DNS lookup")
    monkeypatch.setattr(socket, "getaddrinfo", guarded)
    with pinned_https_proxy(frozenset({"example.com"})) as proxy:
        p = urlsplit(proxy)
        c = http.client.HTTPConnection(p.hostname, p.port, timeout=3)
        c.set_tunnel("evil.example", 443)
        with pytest.raises(OSError):
            c.request("GET", "/")
        c.close()


@pytest.mark.parametrize("url", [
    "https://example.com/status?other=asc",
    "https://example.com/status?sort=asc&sort=desc",
    "https://example.com/status?sort=",
    "https://example.com/status?sort=asc;other=bad",
    "https://example.com/status?sort=asc&other=bad",
    "https://example.com/status?sort=asc/../delete",
])
def test_query_allowlist_rejects_unapproved_values(url):
    assert not allowed_readonly_url(url, frozenset({"example.com"}),
                                   ("/status",), True, frozenset({"sort"}))

def test_query_optin_without_keys_is_denied():
    assert not allowed_readonly_url("https://example.com/status?sort=asc",
                                   frozenset({"example.com"}), ("/status",), True)
