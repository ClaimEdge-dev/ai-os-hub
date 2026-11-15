"""Fail-closed, loopback-only HTTPS CONNECT proxy for public browser QA.

This is one defense layer, not an OS egress sandbox. The CI/container worker
must separately deny all direct outbound traffic except to this proxy.
"""
from __future__ import annotations

from contextlib import contextmanager
import ipaddress
import re
import select
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Semaphore, Thread
from time import monotonic

_DOMAIN = re.compile(r"(?=.{4,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?")
MAX_TUNNEL_BYTES = 5 * 1024 * 1024
MAX_TUNNEL_SECONDS = 15.0


class EgressDenied(ValueError):
    """Target cannot be proven to be a permitted global public endpoint."""


def _validated_hostname(hostname: str) -> str:
    if not isinstance(hostname, str) or hostname != hostname.strip():
        raise EgressDenied("invalid_host")
    host = hostname.lower()
    if not _DOMAIN.fullmatch(host):
        raise EgressDenied("invalid_host")
    return host


def resolve_pinned_endpoints(hostname: str, approved_hosts: frozenset[str]) -> tuple[tuple[int, tuple], ...]:
    """Resolve *once*. Deny the whole hostname if *any* DNS answer is not global."""
    host = _validated_hostname(hostname)
    if host not in approved_hosts:
        raise EgressDenied("host_not_allowlisted")
    try:
        answers = socket.getaddrinfo(host, 443, family=socket.AF_UNSPEC,
                                     type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    except OSError as exc:
        raise EgressDenied("dns_failed") from exc
    out = []
    for family, kind, proto, _, sockaddr in answers:
        if family not in (socket.AF_INET, socket.AF_INET6) or kind != socket.SOCK_STREAM:
            raise EgressDenied("unexpected_dns_answer")
        try:
            ip = ipaddress.ip_address(sockaddr[0])
        except ValueError as exc:
            raise EgressDenied("non_numeric_dns_answer") from exc
        if not ip.is_global or getattr(ip, "ipv4_mapped", None):
            raise EgressDenied("non_public_dns_answer")
        if family == socket.AF_INET6 and len(sockaddr) > 3 and sockaddr[3] != 0:
            raise EgressDenied("scoped_ipv6_denied")
        out.append((family, (str(ip), 443) if family == socket.AF_INET
                    else (str(ip), 443, 0, 0)))
    if not out:
        raise EgressDenied("no_dns_answer")
    return tuple(out)


class _ConnectHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    timeout = 5

    def log_message(self, *_args):
        return  # No target URLs or authentication data in CI logs.

    def do_CONNECT(self):
        authority = self.path
        if authority.count(":") != 1:
            self.send_error(403)
            return
        host, port = authority.rsplit(":", 1)
        if port != "443":
            self.send_error(403)
            return
        try:
            endpoints = resolve_pinned_endpoints(host, self.server.approved_hosts)
        except EgressDenied:
            self.send_error(403)
            return

        upstream = None
        for family, sockaddr in endpoints:
            candidate = socket.socket(family, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            candidate.settimeout(3)
            try:
                candidate.connect(sockaddr)  # numeric IP, never the hostname
                upstream = candidate
                break
            except OSError:
                candidate.close()
        if upstream is None:
            self.send_error(502)
            return
        try:
            self.send_response(200, "Connection Established")
            self.send_header("Connection", "close")
            self.end_headers()
            self.connection.setblocking(False)
            upstream.setblocking(False)
            client_to_upstream = upstream_to_client = 0
            deadline = monotonic() + MAX_TUNNEL_SECONDS
            while monotonic() < deadline:
                readable, _, _ = select.select([self.connection, upstream], [], [], 0.2)
                if not readable:
                    continue
                for source in readable:
                    destination = upstream if source is self.connection else self.connection
                    chunk = source.recv(16384)
                    if not chunk:
                        return
                    if source is self.connection:
                        client_to_upstream += len(chunk)
                        if client_to_upstream > MAX_TUNNEL_BYTES:
                            return
                    else:
                        upstream_to_client += len(chunk)
                        if upstream_to_client > MAX_TUNNEL_BYTES:
                            return
                    destination.settimeout(2)
                    destination.sendall(chunk)
        except (OSError, ValueError):
            return
        finally:
            upstream.close()
            self.close_connection = True

    def do_GET(self):
        self.send_error(405)

    do_POST = do_GET
    do_HEAD = do_GET
    do_OPTIONS = do_GET


class _Server(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 8

    def process_request(self, request, client_address):
        if not self._slots.acquire(blocking=False):
            request.close()
            return
        try:
            super().process_request(request, client_address)
        except BaseException:
            self._slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._slots.release()

    def __init__(self, hosts: frozenset[str]):
        self._slots = Semaphore(8)
        self.approved_hosts = frozenset(_validated_hostname(h) for h in hosts)
        if not self.approved_hosts:
            raise EgressDenied("empty_allowlist")
        super().__init__(("127.0.0.1", 0), _ConnectHandler)


@contextmanager
def pinned_https_proxy(hosts: frozenset[str]):
    """Start temporary local proxy, exposing only its loopback URL to Chromium."""
    server = _Server(hosts)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
