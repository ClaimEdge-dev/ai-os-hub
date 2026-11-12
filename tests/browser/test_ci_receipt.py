from scripts.browser_ci_receipt import assess

def test_no_skips_or_failures():
    assert assess({"tests": 10, "skipped": 0, "failures": 0, "errors": 0}, 10)
    assert not assess({"tests": 10, "skipped": 1, "failures": 0, "errors": 0}, 10)
    assert not assess({"tests": 0, "skipped": 0, "failures": 0, "errors": 0}, 1)
    assert not assess({"tests": 10, "skipped": 0, "failures": 1, "errors": 0}, 10)
