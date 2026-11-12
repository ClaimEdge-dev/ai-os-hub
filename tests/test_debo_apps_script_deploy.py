import importlib.util
import json
import os
from pathlib import Path
from unittest import TestCase, mock

path = Path(__file__).resolve().parents[1] / "tools" / "debo_apps_script_deploy.py"
spec = importlib.util.spec_from_file_location("debo_apps_script_deploy", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
MANIFEST = {
    "timeZone": "America/Chicago",
    "runtimeVersion": "V8",
    "oauthScopes": sorted(m.REQUIRED_SCOPES),
    "dependencies": {"enabledAdvancedServices": [{"serviceId": "drive", "version": "v3"}]},
}
SOURCE = "PAGE_SIZE: 50; PILOT_FOLDER_ID; " + "".join(
    "function " + fn + "() {}\n" for fn in sorted(m.FUNCTIONS))

class AppsScriptPilotGuardTests(TestCase):
    def test_source_validates(self):
        self.assertEqual(len(m.validate_source(SOURCE, MANIFEST)), 64)

    def test_reject_broad_scopes(self):
        with self.assertRaises(ValueError):
            m.validate_source(SOURCE, {**MANIFEST, "oauthScopes": ["https://www.googleapis.com/auth/drive"]})

    def test_reject_drive_mutation(self):
        with self.assertRaises(ValueError):
            m.validate_source(SOURCE + "Drive.Files.delete('x')", MANIFEST)

    def test_reject_missing_function(self):
        with self.assertRaises(ValueError):
            m.validate_source(SOURCE.replace("deboPilotPreflight", "otherFn"), MANIFEST)

    def test_empty_bound_project_eligible(self):
        with mock.patch.dict(os.environ, {"DEBO_HOST_SPREADSHEET_ID": "host"}):
            state = m.plan_deployment({"parentId": "host"}, {
                "files": [{"name": "Code", "type": "SERVER_JS", "source": ""}]},
                SOURCE, MANIFEST)
            self.assertEqual(state, "ELIGIBLE_EMPTY_PROJECT")

    def test_reject_wrong_host(self):
        with mock.patch.dict(os.environ, {"DEBO_HOST_SPREADSHEET_ID": "host"}):
            with self.assertRaises(ValueError):
                m.plan_deployment({"parentId": "other"}, {"files": []}, SOURCE, MANIFEST)

    def test_reject_existing_code(self):
        with mock.patch.dict(os.environ, {"DEBO_HOST_SPREADSHEET_ID": "host"}):
            with self.assertRaises(ValueError):
                m.plan_deployment({"parentId": "host"}, {"files": [
                    {"name": "Code", "type": "SERVER_JS", "source": "function production() {}"}]}, SOURCE, MANIFEST)

    def test_reject_existing_manifest(self):
        with mock.patch.dict(os.environ, {"DEBO_HOST_SPREADSHEET_ID": "host"}):
            with self.assertRaises(ValueError):
                m.plan_deployment({"parentId": "host"}, {"files": [
                    {"name": "appsscript", "type": "JSON",
                     "source": json.dumps({"timeZone": "Pacific/Honolulu"})}]}, SOURCE, MANIFEST)

    def test_missing_source_secret_fails(self):
        with mock.patch.dict(os.environ, {"DEBO_SCANNER_SOURCE_B64": ""}):
            with self.assertRaises(ValueError):
                m.source_and_manifest()
