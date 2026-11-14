#!/usr/bin/env python3
"""Static safety check only; Gradle and emulator checks are separate."""
from pathlib import Path
from xml.etree import ElementTree as ET
import re
ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "app/src/main"
manifest = ET.parse(MAIN / "AndroidManifest.xml").getroot()
ns = "{http://schemas.android.com/apk/res/android}"
app = manifest.find("application")
source = (MAIN / "java/com/debo/roadside/RoadsideCarAppService.kt").read_text()
readme = (ROOT / "README.md").read_text()
features = {x.get(ns + "name"): x.get(ns + "required") for x in manifest.findall("uses-feature")}
tests = {
    "valid manifest": app is not None,
    "valid car template XML": bool(ET.parse(MAIN / "res/xml/automotive_app_desc.xml")),
    "requires automotive hardware": features.get("android.hardware.type.automotive") == "true",
    "requires car templates host": features.get("android.software.car.templates_host") == "true",
    "declares legitimate POI category": any(e.get(ns + "name") == "androidx.car.app.category.POI" for e in app.iter("category")),
    "registers CarAppActivity": any(e.get(ns + "name") == "androidx.car.app.activity.CarAppActivity" for e in app.findall("activity")),
    "declares min car API": any(e.get(ns + "name") == "androidx.car.app.minCarApiLevel" for e in app.findall("meta-data")),
    "declares template descriptor": "template" in (MAIN / "res/xml/automotive_app_desc.xml").read_text(),
    "no private vehicle facts": not any(s in source.lower() for s in ["192741", "54189", "54,189", "vin:", "carstar", "p0073", "u0284"]),
    "no network/vehicle sensors": not any(x in ET.tostring(manifest, encoding="unicode") for x in ["android.permission.INTERNET", "android.permission.ACCESS_FINE_LOCATION"]) and "CarPropertyManager" not in source,
    "valid car navigation action": "CarContext.ACTION_NAVIGATE" in source and "geo:0,0?q=" in source,
    "release host validation": "if (debug)" in source and "hosts_allowlist_sample" in source,
    "no fraudulent NAVIGATION category": "androidx.car.app.category.NAVIGATION" not in ET.tostring(manifest, encoding="unicode"),
    "not claiming live store app": "not compiled" in readme.lower() and "not installed" in readme.lower()  # claim is status-gated in README
}
for name, value in tests.items(): print(("PASS" if value else "FAIL") + " " + name)
print(f"{sum(tests.values())}/{len(tests)} static source checks")
raise SystemExit(0 if all(tests.values()) else 1)
