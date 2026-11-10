"""Offline contract checks for Perplexity Pro routing and account boundaries."""
import unittest
from tools.debo_perplexity_pro_route import route


class TestPerplexityProRouter(unittest.TestCase):
    def test_fast_uses_best_automatic(self):
        result = route("quick_fact")
        self.assertEqual(result["mode"], "Best")
        self.assertFalse(result["model_confirmed_from_input_menu"])

    def test_research_uses_automatic(self):
        result = route("deep_research")
        self.assertEqual(result["mode"], "Research")
        self.assertIn("Automatic", result["model"])

    def test_source_compare_uses_sonar_only_if_observed(self):
        result = route("source_comparison", ["Sonar", "Gemini 3.1 Pro"])
        self.assertEqual(result["model"], "Sonar")
        self.assertTrue(result["model_confirmed_from_input_menu"])

    def test_technical_model_is_actual_input_label(self):
        result = route("technical_research", ["GPT-5.2", "Claude Sonnet 4.6"])
        self.assertEqual(result["model"], "GPT-5.2")

    def test_claude_for_documents_only_if_observed(self):
        result = route("document_analysis", ["Claude Sonnet 4.6 Thinking"])
        self.assertEqual(result["model"], "Claude Sonnet 4.6 Thinking")

    def test_gemini_fallback_does_not_invent_access(self):
        result = route("multimodal_comparison", ["Sonar"])
        self.assertFalse(result["model_confirmed_from_input_menu"])
        self.assertIn("verify", result["model"])

    def test_account_inventory_is_not_web_search(self):
        result = route("private_account_inventory", available_models=["Sonar"])
        self.assertEqual(result["status"], "NOT_AN_ACCOUNT_READ")
        self.assertEqual(result["account_read_state"], "ACCESS_NOT_VERIFIED")
        self.assertIsNone(result["model"])

    def test_authorization_is_not_readback(self):
        result = route("private_account_inventory", account_read_authorized=True)
        self.assertEqual(result["account_read_state"], "AUTHORIZED_ROUTE_REQUIRES_READBACK")

    def test_no_research_and_no_pro_fallback(self):
        result = route("deep_research", research_available=False, pro_search_available=False)
        self.assertEqual(result["mode"], "Best")

    def test_pro_search_unavailable(self):
        result = route("technical_research", ["GPT-5.2"], pro_search_available=False)
        self.assertEqual(result["mode"], "Best")
        self.assertFalse(result["model_confirmed_from_input_menu"])

    def test_all_routes_exclude_computer(self):
        for task in ("quick_fact", "source_comparison", "technical_research",
                     "document_analysis", "multimodal_comparison", "deep_research",
                     "private_account_inventory"):
            with self.subTest(task=task):
                result = route(task)
                self.assertNotIn("Computer", result["mode"])
                self.assertEqual(result["computer"], "UNAVAILABLE_PER_OWNER")

    def test_unknown_task_fails_closed(self):
        with self.assertRaises(ValueError):
            route("secret_account_scrape")


if __name__ == "__main__":
    unittest.main()
