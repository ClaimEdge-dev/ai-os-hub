import unittest
from validate_registry import validate
class RegistryTests(unittest.TestCase):
 def test_valid(self):
  validate({"skill_id":"jct-readonly","version":"0.1","source_path":"skills/jct","status":"DRAFT"})
 def test_missing_field(self):
  with self.assertRaises(ValueError): validate({"skill_id":"jct","version":"1","status":"DRAFT"})
 def test_invalid_status(self):
  with self.assertRaises(ValueError): validate({"skill_id":"jct","version":"1","source_path":"x","status":"LIVE"})
 def test_verification_requires_evidence(self):
  with self.assertRaises(ValueError): validate({"skill_id":"jct","version":"1","source_path":"x","status":"VERIFIED"})
 def test_verified_with_evidence(self):
  validate({"skill_id":"jct","version":"1","source_path":"x","status":"VERIFIED","evidence_url":"https://example.org/receipt"})
if __name__=="__main__":unittest.main()
