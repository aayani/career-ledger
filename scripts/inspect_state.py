#!/usr/bin/env python3
"""Inspect whether a career database is missing, semantically empty, or populated."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from scripts.career_document import is_placeholder, parse_document
    from scripts.career_schema import EMPTY_VALUES
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from career_document import is_placeholder, parse_document
    from career_schema import EMPTY_VALUES


def inspect(path: Path) -> dict[str, object]:
    if not path.exists():
        return {
            "path": str(path), "content_state": "missing", "schema_version": None,
            "last_reviewed": None, "record_count": 0, "open_followup_count": 0,
            "substantive_field_count": 0,
        }
    document = parse_document(path.read_text(encoding="utf-8"))
    values = [*document.identity.values(), *document.positioning.values(), *document.languages.values()]
    values.extend(entry for record in document.records for entry in record.fields.values())
    substantive = sum(
        entry.value not in EMPTY_VALUES and not is_placeholder(entry.value) for entry in values
    )
    schema = document.metadata.get("Schema version")
    reviewed = document.metadata.get("Last reviewed")
    return {
        "path": str(path),
        "content_state": "populated" if substantive else "empty",
        "schema_version": schema.value if schema and not is_placeholder(schema.value) else None,
        "last_reviewed": reviewed.value if reviewed and not is_placeholder(reviewed.value) else None,
        "record_count": sum(
            "ID" in record.fields
            and bool(record.fields["ID"].value)
            and not is_placeholder(record.fields["ID"].value)
            for record in document.records
        ),
        "open_followup_count": sum(
            record.kind == "followup" and record.fields.get("Status") is not None
            and record.fields["Status"].value == "Open" for record in document.records
        ),
        "substantive_field_count": substantive,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="docs/career.md", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.path), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
