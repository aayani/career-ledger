#!/usr/bin/env python3
"""Inspect whether a YAML career database is missing, empty, invalid, or populated."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

try:
    from scripts.career_document import CareerDocumentError, load_document
    from scripts.career_schema import VALIDATOR
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from career_document import CareerDocumentError, load_document
    from career_schema import VALIDATOR


PLACEHOLDER_PATTERN = re.compile(r"^\s*\[[^\]\n]+\]\s*$")


def _base(path: Path, state: str) -> dict[str, object]:
    return {
        "path": str(path),
        "content_state": state,
        "record_count": 0,
        "employment_count": 0,
        "education_count": 0,
        "project_count": 0,
        "skill_usage_count": 0,
        "note_count": 0,
        "private_record_count": 0,
        "substantive_field_count": 0,
        "validation_error_count": 0,
    }


def _substantive_scalars(value: Any) -> int:
    if isinstance(value, dict):
        return sum(_substantive_scalars(item) for item in value.values())
    if isinstance(value, list):
        return sum(_substantive_scalars(item) for item in value)
    if isinstance(value, bool) or value is None:
        return 0
    if isinstance(value, str):
        return int(bool(value.strip()) and not PLACEHOLDER_PATTERN.fullmatch(value))
    return 1


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def inspect(path: Path) -> dict[str, object]:
    if not path.exists():
        return _base(path, "missing")
    try:
        document = load_document(path)
    except CareerDocumentError as error:
        result = _base(path, "invalid")
        result["error"] = str(error)
        return result

    employment = _list(document.get("employment"))
    education = _list(document.get("education"))
    projects = _list(document.get("projects"))
    notes = _list(document.get("notes"))
    skill_usages = [
        skill
        for project in projects if isinstance(project, dict)
        for skill in _list(project.get("skills"))
    ]
    private_records = [
        record
        for record in [*education, *employment, *skill_usages]
        if isinstance(record, dict) and record.get("private") is True
    ]
    substantive = _substantive_scalars(document)
    validation_error_count = sum(1 for _ in VALIDATOR.iter_errors(document))
    state = "empty" if not substantive else "invalid" if validation_error_count else "populated"
    return {
        "path": str(path),
        "content_state": state,
        "record_count": len(education) + len(employment),
        "employment_count": len(employment),
        "education_count": len(education),
        "project_count": len(projects),
        "skill_usage_count": len(skill_usages),
        "note_count": len(notes),
        "private_record_count": len(private_records),
        "substantive_field_count": substantive,
        "validation_error_count": validation_error_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="career.yaml", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.path), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
