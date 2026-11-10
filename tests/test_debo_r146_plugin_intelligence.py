"""DEBO R146 source-only Plugin Intelligence review tests. No live I/O."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "projects" / "debo-05" / "plugin-intelligence-r146" / "src"

class R146PluginReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (P / "plugin-intelligence.html").read_text()
        cls.css = (P / "plugin-intelligence.css").read_text()
        cls.js = (P / "plugin-intelligence.js").read_text()
        data = (P / "plugin-intelligence-data.js").read_text()
        prefix = "window.DEBO_R146_CATALOG="
        assert data.startswith(prefix)
        cls.catalog = json.loads(data[len(prefix):].rstrip(";\\n"))
    def test_source_count(self):
        self.assertEqual(len(self.catalog), 147)
        self.assertEqual(len({x["name"] for x in self.catalog}),147)
    def test_every_item_has_fields(self):
        for row in self.catalog:
            for key in ("name","category","feature","projects","state"):
                self.assertTrue(row.get(key), f"{row.get('name')}: missing {key}")
    def test_no_blanket_installed_claim(self):
        self.assertIn("not 147 installed", self.html.lower())
        self.assertTrue(any("UNVERIFIED" in x["state"] for x in self.catalog))
    def test_top_three(self):
        self.assertEqual(self.html.count('class="priority"'),3)
        self.assertIn("owner acceptance",self.html.lower())
    def test_csp_closed(self):
        self.assertIn("default-src 'self'",self.html)
        self.assertIn("connect-src 'self'",self.html)
        self.assertIn("object-src 'none'",self.html)
        self.assertNotIn("unsafe-inline",self.html)
    def test_no_dynamic_html_injection(self):
        self.assertNotIn("innerHTML",self.js)
        self.assertIn("textContent",self.js)
        self.assertIn("replaceChildren",self.js)
    def test_six_initial_results(self):
        self.assertIn("visibleLimit=6",self.js)
        self.assertIn("visibleLimit+=12",self.js)
    def test_prompt_uses_current_compiler(self):
        self.assertIn("Make a Prompt",self.html)
        self.assertIn("R144 capability matrix",self.js)
        self.assertIn("Do not replace the Elite v2 compiler",self.js)
    def test_no_secrets_or_personal_data(self):
        for f in (self.html,self.js,self.css):
            for banned in ("DEBO_NEON_EDITOR_DSN","DEBO_EDITOR_KEY_SHA256","DATABASE_URL","PRIVATE KEY"):
                self.assertNotIn(banned,f)
    def test_responsive(self):
        self.assertIn("max-width:760px",self.css)
        self.assertIn("max-width:430px",self.css)
    def test_accessible_controls(self):
        for field in ("searchInput","category","task","project","output","generate","copy","more"):
            self.assertIn('id="'+field+'"',self.html)
        self.assertIn('aria-live="polite"',self.html)
    def test_static_only(self):
        self.assertNotIn("fetch(",self.js)
        self.assertNotIn("XMLHttpRequest",self.js)
        self.assertNotIn("WebSocket",self.js)

if __name__ == "__main__": unittest.main()
