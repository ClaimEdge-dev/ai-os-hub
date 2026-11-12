"""Shared URL safety policy; read-only is not guaranteed side effect free."""
import re
from urllib.parse import parse_qsl, unquote, urlsplit

from adapters.browser.path_policy import is_path_permitted

_UNSAFE_ACTION = re.compile(
    r"delete|remove|destroy|logout|signout|approve|reject|revoke|"
    r"disable|enable|execute|run[-_]?job|trigger|admin|auth|token|"
    r"transfer|submit|webhook|callback|reset|update|edit|create",
    re.IGNORECASE,
)
_HOST = re.compile(r"(?=.{4,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?")


def allowed_readonly_url(url: str, hosts: frozenset[str],
                         allowed_path_prefixes: tuple[str, ...],
                         allow_query_params: bool = False,
                         allowed_query_keys: frozenset[str] = frozenset()) -> bool:
    """Fail-closed exact HTTPS host + path scope, no userinfo, unsafe actions, or default query."""
    try:
        p = urlsplit(url)
        host = (p.hostname or "").lower()
        port = p.port
    except (ValueError, TypeError):
        return False
    if (p.scheme != "https" or not host or p.username or p.password or
            p.fragment or port not in (None, 443) or not _HOST.fullmatch(host) or
            host not in hosts or not allowed_path_prefixes):
        return False
    raw_path = p.path or "/"
    # One decode is enough for paths: path_policy rejects *all* percent-encoded paths.
    if _UNSAFE_ACTION.search(unquote(raw_path)):
        return False
    if p.query:
        if not allow_query_params or len(p.query) > 512:
            return False
        # Query allowlisting is exceptional; reject ambiguous encoded or action queries.
        if ("%" in p.query or ";" in p.query or _UNSAFE_ACTION.search(p.query)
                or not allowed_query_keys):
            return False
        try:
            pairs = parse_qsl(p.query, keep_blank_values=True,
                              strict_parsing=True, max_num_fields=8)
        except ValueError:
            return False
        keys = [key for key, _ in pairs]
        if (not keys or len(keys) != len(set(keys)) or
                any(key not in allowed_query_keys or not value or
                    len(value) > 128 or not re.fullmatch(r"[A-Za-z0-9_-]+", value)
                    for key, value in pairs)):
            return False
    # "/" permits only the home page, not the entire domain.
    for scope in allowed_path_prefixes:
        if scope == "/" and raw_path == "/":
            return True
        if scope != "/" and is_path_permitted(raw_path, (scope,)):
            return True
    return False
