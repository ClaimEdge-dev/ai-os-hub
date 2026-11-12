from scripts.browser_ci_receipt import assess, verify_receipt


SHA = "a" * 40


def test_no_skips_or_failures():
    assert assess({"tests": 30, "skipped": 0, "failures": 0, "errors": 0}, 20)
    assert not assess({"tests": 30, "skipped": 1, "failures": 0, "errors": 0}, 20)
    assert not assess({"tests": 0, "skipped": 0, "failures": 0, "errors": 0}, 1)
    assert not assess({"tests": 30, "skipped": 0, "failures": 1, "errors": 0}, 20)


def test_exact_head_and_successful_pytest_required():
    counts = {"tests": 40, "skipped": 0, "failures": 0, "errors": 0}
    assert verify_receipt(SHA, SHA, "success", counts)
    assert not verify_receipt(SHA, "b" * 40, "success", counts)
    assert not verify_receipt(SHA, SHA, "failure", counts)
    assert not verify_receipt("x" * 40, "x" * 40, "success", counts)
