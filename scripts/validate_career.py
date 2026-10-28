#!/usr/bin/env python3
"""Validate the canonical Markdown career evidence database."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

try:
    from scripts.career_document import (
        Document, Record, is_placeholder, parse_document, unknown_section_fields,
    )
    from scripts.career_schema import (
        DATE_PATTERN, ID_PATTERN, METADATA_FIELDS, MONTH_PATTERN, RECORD_SPECS,
        SUPPORTED_SCHEMA_VERSION, TAG_PATTERN, YEAR_PATTERN,
    )
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from career_document import (
        Document, Record, is_placeholder, parse_document, unknown_section_fields,
    )
    from career_schema import (
        DATE_PATTERN, ID_PATTERN, METADATA_FIELDS, MONTH_PATTERN, RECORD_SPECS,
        SUPPORTED_SCHEMA_VERSION, TAG_PATTERN, YEAR_PATTERN,
    )


@dataclass(frozen=True)
class Finding:
    level: str
    line: int
    message: str


def split_references(value: str) -> list[str]:
    if value in {"", "Not applicable", "Not documented", "Unknown"}:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def month_index(value: str) -> int | None:
    if not MONTH_PATTERN.fullmatch(value):
        return None
    year, month = (int(part) for part in value.split("-"))
    return year * 12 + month


def date_is_valid(value: str, precision: str) -> bool:
    patterns = {"year": YEAR_PATTERN, "month": MONTH_PATTERN, "year-or-month": DATE_PATTERN}
    return bool(patterns[precision].fullmatch(value))


def validate_metadata(document: Document, text: str) -> list[Finding]:
    findings = [
        Finding("ERROR", 1, f"missing metadata field: {name}")
        for name in sorted(METADATA_FIELDS - document.metadata.keys())
    ]
    for name, entry in document.metadata.items():
        if not entry.value:
            findings.append(Finding("ERROR", entry.line, f"empty metadata field: {name}"))
    schema = document.metadata.get("Schema version")
    if schema and schema.value and schema.value != SUPPORTED_SCHEMA_VERSION:
        findings.append(Finding(
            "ERROR", schema.line,
            f"unsupported schema version: {schema.value} (supported: {SUPPORTED_SCHEMA_VERSION})",
        ))
    reviewed = document.metadata.get("Last reviewed")
    if reviewed and reviewed.value:
        try:
            date.fromisoformat(reviewed.value)
        except ValueError:
            findings.append(Finding("ERROR", reviewed.line, f"invalid last-reviewed date: {reviewed.value}"))
    for name, expected in {
        "Default disclosure": "Application-safe",
        "Language policy": "Region-neutral English",
    }.items():
        entry = document.metadata.get(name)
        if entry and entry.value and entry.value != expected:
            findings.append(Finding("ERROR", entry.line, f"invalid {name.lower()}: {entry.value}"))
    if is_placeholder(text):
        findings.append(Finding("ERROR", 1, "unresolved template placeholder found"))
    return findings


def validate_record_shape(record: Record) -> list[Finding]:
    findings = []
    spec = RECORD_SPECS[record.kind]
    allowed = spec.required | spec.optional
    for name, entry in record.fields.items():
        if name not in allowed:
            findings.append(Finding("ERROR", entry.line, f"unknown {record.kind} field: {name}"))
    for name in sorted(spec.required - record.fields.keys()):
        findings.append(Finding("ERROR", record.line, f"{record.kind} '{record.title}' missing {name}"))
    for name in sorted(spec.required & record.fields.keys()):
        entry = record.fields[name]
        if not entry.value and name != "Responsibilities":
            findings.append(Finding("ERROR", entry.line, f"{record.kind} '{record.title}' has empty {name}"))
    identifier = record.fields.get("ID")
    if identifier:
        if not ID_PATTERN.fullmatch(identifier.value):
            findings.append(Finding("ERROR", identifier.line, f"invalid semantic ID: {identifier.value}"))
        elif not identifier.value.startswith(spec.prefix):
            findings.append(Finding("ERROR", identifier.line, f"ID prefix does not match {record.kind}: {identifier.value}"))
    for name, allowed_values in spec.controlled.items():
        entry = record.fields.get(name)
        if entry and entry.value not in allowed_values:
            findings.append(Finding("ERROR", entry.line, f"invalid {name}: {entry.value}"))
    for name, rule in spec.dates.items():
        entry = record.fields.get(name)
        if entry and entry.value not in rule.specials and not date_is_valid(entry.value, rule.precision):
            findings.append(Finding("ERROR", entry.line, f"invalid {name.lower()} value: {entry.value}"))
    start, end = record.fields.get("Start"), record.fields.get("End")
    if start and end and DATE_PATTERN.fullmatch(start.value) and DATE_PATTERN.fullmatch(end.value):
        normalized_start = start.value + ("-01" if len(start.value) == 4 else "")
        normalized_end = end.value + ("-12" if len(end.value) == 4 else "")
        if normalized_end < normalized_start:
            findings.append(Finding("ERROR", end.line, "end date precedes start date"))
    tags = record.fields.get("Tags")
    if tags:
        for tag in split_references(tags.value):
            if not TAG_PATTERN.fullmatch(tag):
                findings.append(Finding("ERROR", tags.line, f"invalid tag: {tag}"))
    return findings


def validate(path: Path, require_complete: bool = False) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    document = parse_document(text)
    findings = [Finding("ERROR", issue.line, issue.message) for issue in document.issues]
    findings.extend(Finding("ERROR", issue.line, issue.message) for issue in unknown_section_fields(document))
    findings.extend(validate_metadata(document, text))
    all_ids: dict[str, Record] = {}
    for record in document.records:
        findings.extend(validate_record_shape(record))
        identifier = record.fields.get("ID")
        if not identifier or not ID_PATTERN.fullmatch(identifier.value):
            continue
        if identifier.value in all_ids:
            findings.append(Finding("ERROR", identifier.line, f"duplicate ID: {identifier.value}"))
        else:
            all_ids[identifier.value] = record
    for record in document.records:
        spec = RECORD_SPECS[record.kind]
        for name, allowed_kinds in spec.references.items():
            entry = record.fields.get(name)
            if not entry:
                continue
            for reference in split_references(entry.value):
                target = all_ids.get(reference)
                if target is None:
                    findings.append(Finding("ERROR", entry.line, f"broken reference: {reference}"))
                elif target.kind not in allowed_kinds:
                    findings.append(Finding("ERROR", entry.line, f"invalid {name} reference type: {reference}"))
        if record.kind == "achievement":
            outcome = record.fields.get("Outcome")
            verification = record.fields.get("Verification")
            evidence = record.fields.get("Evidence")
            word_count = sum(len(entry.value.split()) for entry in record.fields.values())
            if word_count > 130:
                findings.append(Finding("WARNING", record.line, f"achievement '{record.title}' is {word_count} words"))
            if verification and verification.value == "Verified" and outcome and re.search(r"\d", outcome.value):
                if not evidence or evidence.value in {"", "Not documented"}:
                    findings.append(Finding("ERROR", outcome.line, "verified numerical outcome needs an evidence reference"))
            if verification and verification.value != "Verified":
                findings.append(Finding("WARNING", record.line, f"achievement '{record.title}' is {verification.value.lower()}"))
            if outcome and outcome.value in {"", "Not documented", "Unknown"}:
                findings.append(Finding("WARNING", outcome.line, f"achievement '{record.title}' has no documented outcome"))
        elif record.kind == "skill":
            evidence = record.fields.get("Evidence")
            if not evidence or not split_references(evidence.value):
                findings.append(Finding("WARNING", record.line, f"skill '{record.title}' has no linked evidence"))
        elif record.kind == "followup":
            status = record.fields.get("Status")
            if status and status.value == "Open":
                findings.append(Finding("WARNING", record.line, f"open follow-up: {record.title}"))
    if require_complete:
        if not any(record.kind == "role" for record in document.records):
            findings.append(Finding("ERROR", 1, "no role records found"))
        if not any(record.kind == "skill" for record in document.records):
            findings.append(Finding("ERROR", 1, "no skill records found"))
    roles = [
        record for record in document.records
        if record.kind == "role" and record.fields.get("Career stage")
        and record.fields["Career stage"].value == "Professional"
    ]
    starts = [record.fields["Start"].value for record in roles if "Start" in record.fields]
    dated_starts = [value for value in starts if MONTH_PATTERN.fullmatch(value)]
    if dated_starts != sorted(dated_starts, reverse=True):
        findings.append(Finding("WARNING", 1, "professional roles are not reverse chronological"))
    for newer, older in zip(roles, roles[1:]):
        newer_start = month_index(newer.fields.get("Start").value if newer.fields.get("Start") else "")
        older_end = month_index(older.fields.get("End").value if older.fields.get("End") else "")
        if newer_start is None or older_end is None:
            continue
        separation = newer_start - older_end
        if separation <= 0:
            findings.append(Finding("WARNING", older.line, f"role chronology overlaps with newer role '{newer.title}'"))
        elif separation > 7:
            findings.append(Finding("WARNING", older.line, f"career gap longer than six months before newer role '{newer.title}'"))
    return sorted(findings, key=lambda item: (item.line, item.level, item.message))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="docs/career.md", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args()
    if not args.path.is_file():
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        return 2
    findings = validate(args.path, require_complete=args.require_complete)
    for finding in findings:
        print(f"{finding.level} {args.path}:{finding.line}: {finding.message}")
    errors = sum(item.level == "ERROR" for item in findings)
    warnings = sum(item.level == "WARNING" for item in findings)
    print(f"Validation complete: {errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.warnings_as_errors and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
