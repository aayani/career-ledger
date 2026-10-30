"""Load the JSON Schema for the canonical YAML profile."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import yaml


ROOT = Path(__file__).resolve().parent.parent
PROFILE_SCHEMA_PATH = (
    ROOT / ".agents" / "skills" / "career-ledger" / "references" / "schema.yaml"
)


def load_profile_schema(path: Path = PROFILE_SCHEMA_PATH) -> dict[str, Any]:
    """Load and verify the profile JSON Schema stored as YAML."""
    try:
        schema = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise RuntimeError(f"Invalid profile schema YAML in {path}: {error}") from error
    if not isinstance(schema, dict):
        raise RuntimeError(f"Profile schema must be a YAML mapping: {path}")
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as error:
        raise RuntimeError(f"Invalid Draft 2020-12 profile schema in {path}: {error}") from error
    return schema


PROFILE_SCHEMA = load_profile_schema()
PROFILE_VALIDATOR = Draft202012Validator(
    PROFILE_SCHEMA,
    format_checker=Draft202012Validator.FORMAT_CHECKER,
)
