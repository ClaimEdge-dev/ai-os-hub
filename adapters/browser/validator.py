"""Validate DEBO browser workflow specifications."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
SCHEMA = Path(__file__).resolve().parents[2] / "schemas/browser_workflow.schema.json"
def validate_workflow_spec(payload):
    Draft202012Validator(json.loads(SCHEMA.read_text()), format_checker=FormatChecker()).validate(payload)
