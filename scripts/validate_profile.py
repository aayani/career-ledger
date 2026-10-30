#!/usr/bin/env python3
"""Validate the canonical YAML profile."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from scripts.profile_document import ProfileDocumentError, load_profile
    from scripts.profile_schema import PROFILE_VALIDATOR
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from profile_document import ProfileDocumentError, load_profile
    from profile_schema import PROFILE_VALIDATOR


@dataclass(frozen=True)
class Finding:
    level: str
    path: str
    message: str

    @property
    def line(self) -> int:
        """Compatibility shim for callers of the former Markdown validator."""
        return 1


def _json_path(parts: Iterable[object]) -> str:
    path = "$"
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        elif isinstance(part, str) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part):
            path += f".{part}"
        else:
            path += f"[{part!r}]"
    return path


def _employment_reference_findings(document: dict[str, object]) -> list[Finding]:
    employment = document.get("employment", [])
    projects = document.get("projects", [])
    if not isinstance(employment, list) or not isinstance(projects, list):
        return []

    employment_ids = {
        job.get("id")
        for job in employment
        if isinstance(job, dict) and isinstance(job.get("id"), str)
    }
    findings = []
    for index, project in enumerate(projects):
        if not isinstance(project, dict):
            continue
        project_employment_ids = project.get("employmentId")
        if not isinstance(project_employment_ids, list):
            continue
        for employment_index, employment_id in enumerate(project_employment_ids):
            if (
                isinstance(employment_id, str)
                and re.fullmatch(r"employment-[a-z0-9]+(?:-[a-z0-9]+)*", employment_id)
                and employment_id not in employment_ids
            ):
                findings.append(
                    Finding(
                        "ERROR",
                        f"$.projects[{index}].employmentId[{employment_index}]",
                        "employmentId does not match any employment record",
                    )
                )
    return findings


def _duplicate_record_id_findings(document: dict[str, object]) -> list[Finding]:
    findings = []
    for collection, label in (("education", "education"), ("projects", "project")):
        records = document.get(collection, [])
        if not isinstance(records, list):
            continue
        seen = set()
        for index, record in enumerate(records):
            if not isinstance(record, dict) or not isinstance(record.get("id"), str):
                continue
            record_id = record["id"]
            if record_id in seen:
                findings.append(
                    Finding(
                        "ERROR",
                        f"$.{collection}[{index}].id",
                        f"duplicate {label} id {record_id!r}",
                    )
                )
            seen.add(record_id)
    return findings


def validate_profile(path: Path, require_complete: bool = False) -> list[Finding]:
    """Return schema and completeness findings for a profile YAML file."""
    try:
        document = load_profile(path)
    except ProfileDocumentError as error:
        return [Finding("ERROR", "$", str(error))]

    findings = [
        Finding("ERROR", _json_path(error.absolute_path), error.message)
        for error in PROFILE_VALIDATOR.iter_errors(document)
    ]
    findings.extend(_employment_reference_findings(document))
    findings.extend(_duplicate_record_id_findings(document))

    if require_complete:
        has_content = any(
            isinstance(document.get(key), list) and bool(document[key])
            for key in ("education", "employment", "projects")
        )
        if not has_content:
            findings.append(
                Finding(
                    "ERROR",
                    "$",
                    "no education, employment, or project records found",
                )
            )

    unique = {(item.level, item.path, item.message): item for item in findings}
    return sorted(unique.values(), key=lambda item: (item.path, item.level, item.message))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="data/profile.yaml", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args()
    if not args.path.is_file():
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        return 2
    findings = validate_profile(args.path, require_complete=args.require_complete)
    for finding in findings:
        print(f"{finding.level} {args.path}:{finding.path}: {finding.message}")
    errors = sum(item.level == "ERROR" for item in findings)
    warnings = sum(item.level == "WARNING" for item in findings)
    print(f"Validation complete: {errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.warnings_as_errors and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
