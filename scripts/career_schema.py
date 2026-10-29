"""Load the executable schema for the canonical career database."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
CAREER_SCHEMA = (
    ROOT / ".agents" / "skills" / "career-timeline" / "references" / "career-schema.yaml"
)


@dataclass(frozen=True)
class DateRule:
    precision: str
    specials: frozenset[str] = frozenset()


@dataclass(frozen=True)
class RecordSpec:
    prefix: str
    required: frozenset[str]
    optional: frozenset[str] = frozenset()
    controlled: dict[str, frozenset[str]] = field(default_factory=dict)
    dates: dict[str, DateRule] = field(default_factory=dict)
    references: dict[str, frozenset[str]] = field(default_factory=dict)


def fields(*names: str) -> frozenset[str]:
    return frozenset(names)


def load_schema(path: Path = CAREER_SCHEMA) -> dict[str, Any]:
    """Load the canonical career schema."""
    try:
        schema = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise RuntimeError(f"Invalid career schema YAML in {path}: {error}") from error
    if not isinstance(schema, dict):
        raise RuntimeError(f"Career schema must be a YAML mapping: {path}")
    return schema


def _resolve_values(value: str | list[str], value_sets: dict[str, list[str]]) -> frozenset[str]:
    if isinstance(value, str):
        if value not in value_sets:
            raise RuntimeError(f"Unknown career schema value set: {value}")
        value = value_sets[value]
    return fields(*value)


def _record_spec(raw: dict[str, Any], value_sets: dict[str, list[str]]) -> RecordSpec:
    return RecordSpec(
        prefix=raw["prefix"],
        required=fields(*raw["required"]),
        optional=fields(*raw.get("optional", [])),
        controlled={
            name: _resolve_values(values, value_sets)
            for name, values in raw.get("controlled", {}).items()
        },
        dates={
            name: DateRule(rule["precision"], fields(*rule.get("specials", [])))
            for name, rule in raw.get("dates", {}).items()
        },
        references={
            name: _resolve_values(values, value_sets)
            for name, values in raw.get("references", {}).items()
        },
    )


SCHEMA = load_schema()
VALUE_SETS = SCHEMA["value_sets"]
SUPPORTED_SCHEMA_VERSION = SCHEMA["supported_schema_version"]
METADATA_VALUES = dict(SCHEMA["metadata_values"])
LANGUAGE_LEVELS = fields(*SCHEMA["language_levels"])
EMPTY_VALUES = fields(*SCHEMA["empty_values"])
ROLE_SCOPE_WORD_LIMIT = int(SCHEMA["limits"]["role_scope_words"])
ACHIEVEMENT_WORD_LIMIT = int(SCHEMA["limits"]["achievement_words"])

SECTIONS = SCHEMA["sections"]
METADATA_SECTION = SECTIONS["metadata"]
IDENTITY_SECTION = SECTIONS["identity"]
POSITIONING_SECTION = SECTIONS["positioning"]
EXPERIENCE_SECTION = SECTIONS["experience"]
LANGUAGES_SECTION = SECTIONS["languages"]
SECTION_KINDS = dict(SECTIONS["record_sections"])
DATA_SECTIONS = fields(
    METADATA_SECTION,
    IDENTITY_SECTION,
    POSITIONING_SECTION,
    EXPERIENCE_SECTION,
    LANGUAGES_SECTION,
    *SECTION_KINDS,
)

DOCUMENT_FIELDS = SCHEMA["document_fields"]
METADATA_FIELDS = fields(*DOCUMENT_FIELDS["metadata"])
IDENTITY_FIELDS = fields(*DOCUMENT_FIELDS["identity"])
POSITIONING_FIELDS = fields(*DOCUMENT_FIELDS["positioning"])
RECORD_SPECS = {
    kind: _record_spec(raw, VALUE_SETS)
    for kind, raw in SCHEMA["record_specs"].items()
}

ID_PATTERN = re.compile(
    rf"^({'|'.join(re.escape(spec.prefix.removesuffix('-')) for spec in RECORD_SPECS.values())})"
    r"-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
YEAR_PATTERN = re.compile(r"^\d{4}$")
MONTH_PATTERN = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])$")
DATE_PATTERN = re.compile(r"^\d{4}(?:-(?:0[1-9]|1[0-2]))?$")
TAG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
