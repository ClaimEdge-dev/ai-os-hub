"""Private fixture and firewall regression tests. No real user/company records."""
import json
import unittest
from tools.debo_factory_pilot import validate_adapter,run_jct,run_morgans

JCT={"project_id":"JCT","industry":"FIELD_OPERATIONS",
     "source_refs":["Drive:JCT Operations Pack 1cre4DuYXNmZ9zURCVcY3ebh2rexQha8Zu3Mn7bNURNw"],
     "modules":{"Dispatch":"REQUIRED","Billing":"REQUIRED","Heavy Recovery":"CONDITIONAL",
                "Hospitality POS":"NOT_APPLICABLE"},
     "approval_gates":{"external_send_publish_spend":True}}
MOL={"project_id":"MORGANS","industry":"HOSPITALITY",
     "source_refs":["Drive:MOL Brain 1zhooJ8uKI-DSH07AZPOXBQlfJAtsZZcpkB4nRSqM4qo"],
     "modules":{"Brand":"REQUIRED","Inquiry/CRM":"REQUIRED","Events":"CONDITIONAL",
                "Towing Dispatch":"NOT_APPLICABLE"},
     "approval_gates":{"external_send_publish_spend":True}}

class FactoryPilotTests(unittest.TestCase):
    def test_jct_hold_preserves_no_rate_or_actual_invoice(self):
        case={"scenario_id":"SYN-JCT-LEAD-001","synthetic":True,"source":"WEBSITE TEST",
              "pickup":"SIMULATED PICKUP","destination":"SIMULATED DROP","vehicle_class":"HEAVY DUTY",
              "authorized":False,"evidence_present":False,"rate_approved":False}
        r=run_jct(JCT,case)
        self.assertEqual(r.result,"HOLD")
        self.assertIn("RATE_AUTHORITY_MISSING",r.blocking_gaps)
        self.assertIsNone(r.proposed_outputs["amount_billed"])
        self.assertIsNone(r.proposed_outputs["rate"])
        self.assertFalse(r.proposed_outputs["publish_or_send"])
        self.assertFalse(r.proposed_outputs["crm_write"])
        self.assertFalse(r.proposed_outputs["actual_work_performed"])

    def test_morgans_brand_gate(self):
        case={"scenario_id":"SYN-MOL-LEAD-001","synthetic":True,
              "inquiry_type":"PRIVATE EVENT INQUIRY","owner_approved_assets":False,
              "public_business_truth_verified":False,"owner_approved_copy":False}
        r=run_morgans(MOL,case)
        self.assertEqual(r.result,"HOLD")
        self.assertIn("APPROVED_BRAND_ASSET_MISSING",r.blocking_gaps)
        self.assertFalse(r.proposed_outputs["public_claims_included"])
        self.assertFalse(r.proposed_outputs["publish_or_send"])

    def test_no_real_records(self):
        case={"scenario_id":"LIVE1","synthetic":False,"source":"test","pickup":"A","destination":"B",
              "vehicle_class":"LIGHT","authorized":True,"evidence_present":True,"rate_approved":True}
        with self.assertRaises(ValueError): run_jct(JCT,case)

    def test_bad_module_classification_rejected(self):
        bad=dict(JCT,modules={"Billing":"ALWAYS LIVE"})
        with self.assertRaises(ValueError):validate_adapter(bad)

    def test_no_approval_firewall_rejected(self):
        bad=dict(MOL,approval_gates={"external_send_publish_spend":False})
        with self.assertRaises(ValueError):validate_adapter(bad)

if __name__=="__main__": unittest.main()
