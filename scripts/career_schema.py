"""Load the JSON Schema for the canonical YAML career database."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import yaml


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / ".agents" / "skills" / "career-timeline" / "references" / "schema.yaml"


def load_schema(path: Path = SCHEMA_PATH) -> dict[str, Any]:
    """Load and verify the career JSON Schema stored as YAML."""
    try:
        schema = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise RuntimeError(f"Invalid career schema YAML in {path}: {error}") from error
    if not isinstance(schema, dict):
        raise RuntimeError(f"Career schema must be a YAML mapping: {path}")
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as error:
        raise RuntimeError(f"Invalid Draft 2020-12 career schema in {path}: {error}") from error
    return schema


SCHEMA = load_schema()
VALIDATOR = Draft202012Validator(
    SCHEMA,
    format_checker=Draft202012Validator.FORMAT_CHECKER,
)
