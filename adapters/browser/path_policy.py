"""Segment-boundary URL path policy. Reject ambiguous encoded paths."""
import posixpath
from urllib.parse import unquote

def is_path_permitted(raw_path: str, allowed_prefixes: tuple[str, ...]) -> bool:
    if not raw_path.startswith("/") or "\\" in raw_path:
        return False
    # Encoded slash/backslash/dot may be interpreted differently by upstream servers.
    decoded = unquote(raw_path)
    if decoded != raw_path or "//" in raw_path or "/./" in raw_path or "/../" in raw_path:
        return False
    normalized = posixpath.normpath(raw_path)
    if normalized != raw_path.rstrip("/") and not (raw_path == "/"):
        return False
    for raw_prefix in allowed_prefixes:
        if not raw_prefix.startswith("/") or posixpath.normpath(raw_prefix) != raw_prefix.rstrip("/"):
            continue
        prefix = raw_prefix.rstrip("/") or "/"
        if prefix == "/" or normalized == prefix or normalized.startswith(prefix + "/"):
            return True
    return False
