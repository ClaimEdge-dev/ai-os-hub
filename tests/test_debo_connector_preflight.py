"""R149-001 offline, synthetic negative/positive authorization-routing tests."""
import unittest
from tools.debo_connector_preflight import evaluate_route

PUBLIC = {"tool": "public_docs", "operation": "public_read",
          "action_exposed": True, "capability_verified": True, "estimated_cost_usd": 0}
PRIVATE = {"tool": "notion", "operation": "private_read",
           "action_exposed": True, "capability_verified": True,
           "identity_verified": True, "authorization_verified": True,
           "required_scope": "read", "granted_scopes": ["read"],
           "expected_tenant": "authorized-demo", "observed_tenant": "authorized-demo",
           "estimated_cost_usd": 0}

class TestConnectorPreflight(unittest.TestCase):
    def test_public_source_read(self):
        self.assertEqual(evaluate_route(PUBLIC)["decision"], "ALLOW_READ_ONLY")

    def test_private_read_when_fully_verified(self):
        self.assertEqual(evaluate_route(PRIVATE)["decision"], "ALLOW_READ_ONLY")

    def test_unverified_action_blocks_even_if_listed(self):
        self.assertIn("ACTION_NOT_VERIFIED", evaluate_route({**PUBLIC, "action_exposed": False})["reason_codes"])

    def test_identity_fails_closed(self):
        self.assertIn("IDENTITY_UNVERIFIED", evaluate_route({**PRIVATE, "identity_verified": False})["reason_codes"])

    def test_scope_mismatch_blocks(self):
        self.assertIn("SCOPE_NOT_VERIFIED", evaluate_route({**PRIVATE, "required_scope": "write"})["reason_codes"])

    def test_tenant_mismatch_blocks(self):
        self.assertIn("TENANT_NOT_VERIFIED", evaluate_route({**PRIVATE, "observed_tenant": "different"})["reason_codes"])

    def test_missing_tenant_blocks(self):
        self.assertIn("TENANT_NOT_VERIFIED", evaluate_route({**PRIVATE, "expected_tenant": None})["reason_codes"])

    def test_paid_browser_requires_approval(self):
        r = evaluate_route({**PUBLIC, "tool": "browser", "metered": True,
                            "estimated_cost_usd": 0.16})
        self.assertIn("COST_APPROVAL_REQUIRED", r["reason_codes"])

    def test_unknown_metered_cost_blocks(self):
        r = evaluate_route({**PUBLIC, "metered": True, "estimated_cost_usd": None})
        self.assertIn("COST_NOT_VERIFIED", r["reason_codes"])

    def test_zero_cost_metered_verified(self):
        r = evaluate_route({**PUBLIC, "metered": True, "estimated_cost_usd": 0})
        self.assertTrue(r["allowed"])

    def test_write_needs_scope_and_identity(self):
        r = evaluate_route({**PRIVATE, "operation": "write", "required_scope": "write"})
        self.assertFalse(r["allowed"])

    def test_external_contact_stays_held(self):
        r = evaluate_route({**PRIVATE, "operation": "send", "required_scope": "send",
                            "granted_scopes": ["send"], "owner_approved": True})
        self.assertIn("CUSTOMER_CONTACT_HELD", r["reason_codes"])

    def test_deploy_requires_owner_approval(self):
        r = evaluate_route({**PRIVATE, "operation": "deploy",
                            "required_scope": "deploy", "granted_scopes": ["deploy"]})
        self.assertIn("OWNER_APPROVAL_REQUIRED", r["reason_codes"])

    def test_sensitive_export_requires_distinct_gate(self):
        r = evaluate_route({**PRIVATE, "external_transfer": True, "data_classes": ["minor"]})
        self.assertIn("SENSITIVE_TRANSFER_NOT_AUTHORIZED", r["reason_codes"])

    def test_never_transfer_secrets(self):
        r = evaluate_route({**PRIVATE, "data_classes": ["secret"],
                            "external_transfer": True, "data_release_approved": True,
                            "destination_verified": True})
        self.assertIn("SECRET_TRANSFER_PROHIBITED", r["reason_codes"])

    def test_result_does_not_echo_private_identifiers(self):
        r = evaluate_route(PRIVATE)
        self.assertNotIn("authorized-demo", str(r))

    def test_invalid_operation_fails_closed(self):
        self.assertFalse(evaluate_route({**PUBLIC, "operation": "arbitrary_admin"})["allowed"])

    def test_no_boolean_cost_bypass(self):
        self.assertIn("COST_NOT_VERIFIED", evaluate_route({**PUBLIC, "metered": True, "estimated_cost_usd": True})["reason_codes"])

    def test_non_mapping_rejected(self):
        with self.assertRaises(TypeError):
            evaluate_route(None)

if __name__ == "__main__":
    unittest.main()
