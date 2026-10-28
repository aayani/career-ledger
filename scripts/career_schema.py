"""Executable schema for the canonical career database."""

from __future__ import annotations

from dataclasses import dataclass, field
import re


SUPPORTED_SCHEMA_VERSION = "1.0"


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


VERIFICATION = frozenset({"Verified", "Estimated", "Unverified"})
OWNERSHIP = frozenset({"Lead", "Primary", "Shared", "Contributor", "Support"})
DISCLOSURE = frozenset({"Interview-only", "Do not disclose"})
SKILL_REFERENCE = frozenset({"skill"})
EVIDENCE_REFERENCE = frozenset({"role", "achievement", "project", "activity"})


def fields(*names: str) -> frozenset[str]:
    return frozenset(names)


RECORD_SPECS = {
    "role": RecordSpec(
        "role-",
        fields(
            "ID", "Employer", "Title", "Location", "Employment type", "Start",
            "End", "Career stage", "Scope", "Responsibilities", "Skills",
            "Technologies", "Tags",
        ),
        optional=fields("Practices", "Disclosure"),
        controlled={
            "Employment type": fields(
                "Permanent", "Contract", "Internship", "Self-employed", "Not documented"
            ),
            "Career stage": fields("Early", "Professional", "Not documented"),
            "Disclosure": DISCLOSURE,
        },
        dates={
            "Start": DateRule("month"),
            "End": DateRule("month", fields("Present")),
        },
        references={"Skills": SKILL_REFERENCE},
    ),
    "achievement": RecordSpec(
        "ach-",
        fields(
            "ID", "Context", "Contribution", "Outcome", "Scope", "Ownership",
            "Skills", "Tags", "Verification", "Evidence",
        ),
        optional=fields("Disclosure"),
        controlled={
            "Ownership": OWNERSHIP,
            "Verification": VERIFICATION,
            "Disclosure": DISCLOSURE,
        },
        references={"Skills": SKILL_REFERENCE},
    ),
    "education": RecordSpec(
        "edu-",
        fields(
            "ID", "Institution", "Location", "Start", "End", "Focus", "Awards",
            "Verification", "Evidence",
        ),
        optional=fields("Disclosure"),
        controlled={"Verification": VERIFICATION, "Disclosure": DISCLOSURE},
        dates={"Start": DateRule("year"), "End": DateRule("year", fields("Unknown"))},
    ),
    "certification": RecordSpec(
        "cert-",
        fields(
            "ID", "Issuer", "Issued", "Expires", "Credential ID", "Credential URL",
            "Verification", "Evidence",
        ),
        optional=fields("Disclosure"),
        controlled={"Verification": VERIFICATION, "Disclosure": DISCLOSURE},
        dates={
            "Issued": DateRule("month"),
            "Expires": DateRule("month", fields("Does not expire", "Unknown")),
        },
    ),
    "project": RecordSpec(
        "project-",
        fields(
            "ID", "Start", "End", "Status", "Purpose", "Contribution", "Outcome",
            "Collaborators", "URL", "Repository", "Skills", "Technologies", "Tags",
            "Verification", "Evidence",
        ),
        optional=fields("Disclosure"),
        controlled={
            "Status": fields("Active", "Complete", "Paused", "Not documented"),
            "Verification": VERIFICATION,
            "Disclosure": DISCLOSURE,
        },
        dates={
            "Start": DateRule("month", fields("Unknown")),
            "End": DateRule("month", fields("Present", "Unknown")),
        },
        references={"Skills": SKILL_REFERENCE},
    ),
    "activity": RecordSpec(
        "activity-",
        fields(
            "ID", "Type", "Organization", "Date", "Contribution", "Outcome", "URL",
            "Skills", "Verification", "Evidence",
        ),
        optional=fields("Disclosure"),
        controlled={
            "Type": fields(
                "Open source", "Award", "Speaking", "Publication", "Volunteering",
                "Membership",
            ),
            "Verification": VERIFICATION,
            "Disclosure": DISCLOSURE,
        },
        dates={"Date": DateRule("year-or-month", fields("Unknown"))},
        references={"Skills": SKILL_REFERENCE},
    ),
    "break": RecordSpec(
        "break-",
        fields("ID", "Start", "End", "Description", "Activities"),
        optional=fields("Disclosure"),
        controlled={"Disclosure": DISCLOSURE},
        dates={"Start": DateRule("month"), "End": DateRule("month")},
    ),
    "skill": RecordSpec(
        "skill-",
        fields("ID", "Category", "First used", "Last used", "Context", "Capabilities", "Evidence"),
        optional=fields("Disclosure"),
        controlled={
            "Context": fields("Production", "Commercial", "Academic", "Personal", "Mixed"),
            "Disclosure": DISCLOSURE,
        },
        dates={
            "First used": DateRule("year-or-month", fields("Unknown")),
            "Last used": DateRule("year-or-month", fields("Present", "Unknown")),
        },
        references={"Evidence": EVIDENCE_REFERENCE},
    ),
    "followup": RecordSpec(
        "followup-",
        fields("ID", "Related records", "Priority", "Issue", "Resolution", "Status"),
        controlled={
            "Priority": fields("High", "Medium", "Low"),
            "Status": fields("Open", "Resolved"),
        },
        references={
            "Related records": fields(
                "role", "achievement", "education", "certification", "project",
                "activity", "break", "skill",
            )
        },
    ),
}

METADATA_FIELDS = fields("Schema version", "Last reviewed", "Default disclosure", "Language policy")
IDENTITY_FIELDS = fields("Name", "Location", "Email", "Phone", "LinkedIn", "GitHub", "Portfolio")
POSITIONING_FIELDS = fields(
    "Career start", "Primary specializations", "Secondary specializations",
    "Differentiators", "Leadership scope", "Industry experience",
)
EMPTY_VALUES = fields("", "Unknown", "Not documented", "Not applicable")

ID_PATTERN = re.compile(
    rf"^({'|'.join(re.escape(spec.prefix.removesuffix('-')) for spec in RECORD_SPECS.values())})"
    r"-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
YEAR_PATTERN = re.compile(r"^\d{4}$")
MONTH_PATTERN = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])$")
DATE_PATTERN = re.compile(r"^\d{4}(?:-(?:0[1-9]|1[0-2]))?$")
TAG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
