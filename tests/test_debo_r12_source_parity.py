"""R12: byte-exact source-parity acceptance against recovered private originals.

These public expected hashes identify the approved local R4/R5/R6 source snapshots.
"""
import hashlib
import os
from pathlib import Path
import unittest

EXPECTED = {
    "debo_recover.py": ("c03ca662f299359f44d4a02b68a565d3b090418ce4bc32348f68063a824a4fcf", 5723),
    "debo_recovery_bridge.py": ("7e85239b7975e620b38ff1dd39e829c0f73460afd4a2379fa1f0a4a40ff651c2", 6988),
    "run_pinned_acceptance.py": ("c3b8c2caa20920649d24b6fd3f76773d76a8077198a96ea03b1c33f816d3fad6", 4950),
}

class TestDEBOR12SourceParity(unittest.TestCase):
    def test_all_three_originals(self):
        root = Path(__file__).resolve().parent / "r10"
        for name, (expected_hash, expected_size) in EXPECTED.items():
            with self.subTest(name=name):
                data = (root / name).read_bytes()
                self.assertEqual(len(data), expected_size)
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected_hash)
        print("DEBO_R12_SOURCE_PARITY PASS 3/3 original SHA256 hashes, no source modification")

if __name__ == "__main__":
    unittest.main()
