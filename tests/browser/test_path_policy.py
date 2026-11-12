from adapters.browser.path_policy import is_path_permitted

def test_segment_boundary():
    assert is_path_permitted("/status", ("/status",))
    assert is_path_permitted("/status/live", ("/status",))
    assert not is_path_permitted("/status-delete", ("/status",))
    assert not is_path_permitted("/status_admin", ("/status",))

def test_traversal_and_encoding():
    for path in ("/status/../admin", "/status/%2e%2e/admin", "/status//admin", "/status/%2fadmin"):
        assert not is_path_permitted(path, ("/status",))

def test_root_scope():
    assert is_path_permitted("/status", ("/",))
    assert not is_path_permitted("/%2e%2e/private", ("/",))
