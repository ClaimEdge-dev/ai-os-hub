"""DEBO gate and batch runner regression tests, standard library only."""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
GATE = ROOT / "tools/debo_durable_save_gate.py"
RUNNER = ROOT / "tools/debo_verify_all.py"

class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.original = self.root / "original.zip"
        self.readback = self.root / "readback.zip"
        for p in (self.original, self.readback):
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("proof.txt", "DEBO verification")
        self.expected = hashlib.sha256(self.original.read_bytes()).hexdigest()
        self.manifest = self.root / "manifest.json"
        self.receipt = self.root / "receipt.json"

    def run_batch(self, artifacts):
        self.manifest.write_text(json.dumps({"artifacts": artifacts}))
        proc = subprocess.run([sys.executable, str(RUNNER), str(self.manifest),
                               "--gate", str(GATE), "--receipt", str(self.receipt)],
                              capture_output=True, text=True)
        return proc, json.loads(proc.stdout)

    def entry(self, **kw):
        return {"id": "example", "original": str(self.original),
                "readback": str(self.readback), "expected_sha256": self.expected, **kw}

    def test_valid_readback(self):
        proc, result = self.run_batch([self.entry()])
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(result["status"], "VERIFIED")
        self.assertEqual(result["results"][0]["result"]["local_sha256"], self.expected)
        self.assertEqual(json.loads(self.receipt.read_text()), result)

    def test_wrong_expected_hash(self):
        proc, result = self.run_batch([self.entry(expected_sha256="0"*64)])
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(result["results"][0]["result"]["status"], "FAILED_VERIFICATION")

    def test_mutated_readback(self):
        self.readback.write_bytes(b"changed")
        proc, result = self.run_batch([self.entry()])
        self.assertEqual(proc.returncode, 1)
        self.assertFalse(result["results"][0]["result"]["matching"])

    def test_missing_readback(self):
        self.readback.unlink()
        proc, result = self.run_batch([self.entry()])
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(result["results"][0]["result"]["status"], "BLOCKED")

    def test_invalid_zip(self):
        self.original.write_bytes(b"not a zip")
        self.readback.write_bytes(b"not a zip")
        proc, result = self.run_batch([self.entry(expected_sha256=hashlib.sha256(b"not a zip").hexdigest())])
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(result["results"][0]["result"]["status"], "FAILED_VERIFICATION")

    def test_empty_manifest(self):
        proc, result = self.run_batch([])
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(result["status"], "BLOCKED")

    def test_mixed_batch_fails_closed(self):
        second = self.root / "second.zip"
        second.write_bytes(b"changed")
        proc, result = self.run_batch([self.entry(), self.entry(id="second", readback=str(second))])
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual([r["exit_code"] for r in result["results"]], [0, 1])

if __name__ == "__main__":
    unittest.main(verbosity=2)
