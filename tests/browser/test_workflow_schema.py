import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

BASE = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((BASE / "schemas/browser_workflow.schema.json").read_text())
FIXTURE = json.loads((BASE / "fixtures/browser/readonly_public_status.json").read_text())


def test_staging_fixture_schema_is_valid():
    Draft202012Validator(SCHEMA).validate(FIXTURE)


def test_readonly_requires_explicit_paths():
    bad = FIXTURE.copy()
    bad.pop("allowed_path_prefixes")
    with pytest.raises(Exception):
        Draft202012Validator(SCHEMA).validate(bad)


def test_query_opt_in_requires_specific_allowed_keys():
    bad = {**FIXTURE, "allow_query_params": True}
    with pytest.raises(Exception):
        Draft202012Validator(SCHEMA).validate(bad)
