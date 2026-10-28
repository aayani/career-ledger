"""Parse the Markdown career database into a shared document model."""

from __future__ import annotations

from dataclasses import dataclass, field
import re

try:
    from scripts.career_schema import IDENTITY_FIELDS, METADATA_FIELDS, POSITIONING_FIELDS
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from career_schema import IDENTITY_FIELDS, METADATA_FIELDS, POSITIONING_FIELDS


FIELD_PATTERN = re.compile(r"^- ([^:]+):\s*(.*)$")
PLACEHOLDER_PATTERN = re.compile(r"\[[^\]\n]+\](?!\()")
SECTION_KINDS = {
    "5. Education": "education",
    "6. Certifications and licenses": "certification",
    "7. Projects": "project",
    "8. Other professional activities": "activity",
    "10. Career breaks": "break", "11. Skills index": "skill",
    "12. Data-quality follow-up": "followup",
}
DATA_SECTIONS = {
    "1. Database metadata", "2. Identity", "3. Positioning facts",
    "4. Experience", "9. Languages", *SECTION_KINDS,
}
KNOWN_SECTIONS = {"Schema rules", *DATA_SECTIONS}


@dataclass(frozen=True)
class FieldValue:
    value: str
    line: int


@dataclass
class Record:
    kind: str
    title: str
    line: int
    fields: dict[str, FieldValue] = field(default_factory=dict)


@dataclass(frozen=True)
class ParseIssue:
    line: int
    message: str


@dataclass
class Document:
    metadata: dict[str, FieldValue] = field(default_factory=dict)
    identity: dict[str, FieldValue] = field(default_factory=dict)
    positioning: dict[str, FieldValue] = field(default_factory=dict)
    languages: dict[str, FieldValue] = field(default_factory=dict)
    records: list[Record] = field(default_factory=list)
    issues: list[ParseIssue] = field(default_factory=list)


def _store(target: dict[str, FieldValue], name: str, value: str, line: int, issues: list[ParseIssue]) -> None:
    if name in target:
        issues.append(ParseIssue(line, f"duplicate field: {name}"))
        return
    target[name] = FieldValue(value.strip(), line)


def _section_kind(section: str) -> str | None:
    return SECTION_KINDS.get(section)


def is_placeholder(value: str) -> bool:
    """Return whether text contains a bracketed template placeholder, not a Markdown link."""
    return bool(PLACEHOLDER_PATTERN.search(value))


def parse_document(text: str) -> Document:
    document = Document()
    section = ""
    current: Record | None = None
    employer: str | None = None
    current_role: Record | None = None
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if line.startswith("## "):
            section = line[3:].strip()
            current = None
            employer = None
            current_role = None
            if section not in KNOWN_SECTIONS:
                document.issues.append(ParseIssue(number, f"unknown section: {section}"))
            continue
        if line.startswith("##### "):
            if section == "4. Experience" and current_role is not None:
                current = Record("achievement", line[6:].strip(), number)
                document.records.append(current)
            elif section == "4. Experience":
                document.issues.append(ParseIssue(number, "achievement heading without a role"))
                current = None
            else:
                document.issues.append(ParseIssue(number, "achievement heading outside Experience"))
                current = None
            continue
        if line.startswith("#### "):
            if section == "4. Experience" and employer is not None:
                current = Record("role", line[5:].strip(), number)
                current_role = current
                document.records.append(current)
            elif section == "4. Experience":
                document.issues.append(ParseIssue(number, "role heading without an employer"))
                current = None
                current_role = None
            else:
                document.issues.append(ParseIssue(number, "role heading outside Experience"))
                current = None
            continue
        if line.startswith("### "):
            title = line[4:].strip()
            if section == "4. Experience":
                employer = title
                current = None
                current_role = None
            else:
                kind = _section_kind(section)
                current = Record(kind, title, number) if kind else None
                if current:
                    document.records.append(current)
            continue
        match = FIELD_PATTERN.match(line)
        if not match:
            continue
        name, value = match.groups()
        name = name.strip()
        if section == "1. Database metadata":
            _store(document.metadata, name, value, number, document.issues)
        elif section == "2. Identity":
            _store(document.identity, name, value, number, document.issues)
        elif section == "3. Positioning facts":
            _store(document.positioning, name, value, number, document.issues)
        elif section == "9. Languages":
            _store(document.languages, name, value, number, document.issues)
        elif current:
            _store(current.fields, name, value, number, document.issues)
        elif section == "4. Experience" or _section_kind(section):
            document.issues.append(ParseIssue(number, f"field outside record: {name}"))
    return document


def unknown_section_fields(document: Document) -> list[ParseIssue]:
    issues = []
    for values, allowed, label in (
        (document.metadata, METADATA_FIELDS, "metadata"),
        (document.identity, IDENTITY_FIELDS, "identity"),
        (document.positioning, POSITIONING_FIELDS, "positioning"),
    ):
        for name, entry in values.items():
            if name not in allowed:
                issues.append(ParseIssue(entry.line, f"unknown {label} field: {name}"))
    return issues
