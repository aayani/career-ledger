from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.career_schema import CAREER_SCHEMA, SCHEMA, load_schema
from scripts.validate_career import validate


VALID_DATABASE = (
    Path(__file__).parent / "fixtures" / "career-valid.md"
).read_text(encoding="utf-8")


class CareerValidationTests(unittest.TestCase):
    def validate_text(self, text: str, require_complete: bool = False):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "career.md"
            path.write_text(text, encoding="utf-8")
            return validate(path, require_complete=require_complete)

    def errors(self, text: str, require_complete: bool = False):
        return [
            item.message
            for item in self.validate_text(text, require_complete=require_complete)
            if item.level == "ERROR"
        ]

    def test_valid_database_has_no_errors(self):
        findings = self.validate_text(VALID_DATABASE)
        self.assertEqual([], [item for item in findings if item.level == "ERROR"])

    def test_duplicate_id_is_an_error(self):
        text = VALID_DATABASE.replace(
            "- ID: skill-python", "- ID: role-example-engineer-2024"
        )
        findings = self.validate_text(text)
        self.assertTrue(any("duplicate ID" in item.message for item in findings))

    def test_broken_skill_reference_is_an_error(self):
        text = VALID_DATABASE.replace(
            "- Skills: skill-python", "- Skills: skill-missing", 1
        )
        findings = self.validate_text(text)
        self.assertTrue(any("broken reference" in item.message for item in findings))

    def test_wrong_id_prefix_is_an_error(self):
        text = VALID_DATABASE.replace(
            "- ID: skill-python", "- ID: ach-python"
        ).replace("skill-python", "ach-python")
        findings = self.validate_text(text)
        self.assertTrue(any("ID prefix does not match" in item.message for item in findings))

    def test_record_specific_dates_are_enforced(self):
        for replacement in ("- Start: 2024", "- Start: Unknown"):
            with self.subTest(replacement=replacement):
                errors = self.errors(
                    VALID_DATABASE.replace("- Start: 2024-01", replacement)
                )
                self.assertTrue(any("invalid start value" in message for message in errors))
        errors = self.errors(
            VALID_DATABASE.replace("- End: Present", "- End: Does not expire")
        )
        self.assertTrue(any("invalid end value" in message for message in errors))

    def test_record_specific_status_is_enforced(self):
        text = VALID_DATABASE + """

## 12. Data-quality follow-up

### Invalid status

- ID: followup-invalid-status
- Related records: role-example-engineer-2024
- Priority: High
- Issue: Confirm a fact.
- Resolution: Ask the candidate.
- Status: Active
"""
        self.assertTrue(any("invalid Status" in message for message in self.errors(text)))

    def test_reference_types_are_enforced(self):
        text = VALID_DATABASE.replace(
            "- Skills: skill-python", "- Skills: ach-example-latency", 1
        )
        self.assertTrue(
            any("invalid Skills reference type" in message for message in self.errors(text))
        )

    def test_duplicate_and_unknown_fields_are_errors(self):
        duplicate = VALID_DATABASE.replace(
            "- Title: Engineer", "- Title: Wrong\n- Title: Engineer"
        )
        self.assertTrue(any("duplicate field: Title" in message for message in self.errors(duplicate)))
        unknown = VALID_DATABASE.replace(
            "- Technologies: Python", "- Technologies: Python\n- Surprise: value"
        )
        self.assertTrue(any("unknown role field: Surprise" in message for message in self.errors(unknown)))

        misplaced = VALID_DATABASE.replace(
            "### Example Ltd\n\n#### Engineer",
            "### Example Ltd\n\n- Title: Misplaced\n\n#### Engineer",
        )
        self.assertTrue(any("field outside record: Title" in message for message in self.errors(misplaced)))

    def test_unknown_record_section_is_an_error(self):
        text = VALID_DATABASE + """

## 7. Project

### Invisible project

- ID: project-invisible
"""
        self.assertTrue(
            any("unknown section: 7. Project" in message for message in self.errors(text))
        )

    def test_legacy_schema_rules_section_is_an_error(self):
        text = VALID_DATABASE + """

## Schema rules
"""
        self.assertTrue(
            any("unknown section: Schema rules" in message for message in self.errors(text))
        )

    def test_experience_hierarchy_is_enforced(self):
        orphan_achievement = VALID_DATABASE.replace(
            "#### Engineer",
            "##### Orphan achievement\n\n#### Engineer",
            1,
        )
        self.assertTrue(
            any(
                "achievement heading without a role" in message
                for message in self.errors(orphan_achievement)
            )
        )

        orphan_role = VALID_DATABASE.replace("### Example Ltd\n\n", "", 1)
        self.assertTrue(
            any("role heading without an employer" in message for message in self.errors(orphan_role))
        )

    def test_markdown_links_are_not_template_placeholders(self):
        text = VALID_DATABASE.replace(
            "Performance review, 2025",
            "[Performance review](https://example.com/review), 2025",
        )
        self.assertFalse(
            any("unresolved template placeholder" in message for message in self.errors(text))
        )

    def test_schema_version_is_required_and_supported(self):
        blank = VALID_DATABASE.replace("- Schema version: 1.0", "- Schema version:")
        self.assertTrue(any("empty metadata" in message for message in self.errors(blank)))
        newer = VALID_DATABASE.replace("- Schema version: 1.0", "- Schema version: 99.0")
        self.assertTrue(any("unsupported schema version" in message for message in self.errors(newer)))

    def test_schema_is_loaded_from_yaml(self):
        schema = CAREER_SCHEMA.read_text(encoding="utf-8")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "career-schema.yaml"
            path.write_text(
                schema.replace(
                    'supported_schema_version: "1.0"',
                    'supported_schema_version: "9.9"',
                    1,
                ),
                encoding="utf-8",
            )
            self.assertEqual("9.9", load_schema(path)["supported_schema_version"])

    def test_schema_rejects_a_non_mapping_root(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "career-schema.yaml"
            path.write_text("- not\n- a\n- mapping\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "YAML mapping"):
                load_schema(path)

    def test_every_record_field_has_authoring_guidance(self):
        guidance = SCHEMA["field_guidance"]
        for kind, spec in SCHEMA["record_specs"].items():
            with self.subTest(kind=kind):
                fields = set(spec["required"]) | set(spec.get("optional", []))
                self.assertEqual(set(), fields - guidance.keys())

    def test_every_document_field_has_authoring_guidance(self):
        guidance = SCHEMA["field_guidance"]
        for section, fields in SCHEMA["document_fields"].items():
            with self.subTest(section=section):
                self.assertEqual(set(), set(fields) - guidance.keys())

    def test_language_levels_are_enforced(self):
        text = VALID_DATABASE + """

## 9. Languages

- English: Expert
"""
        self.assertTrue(any("invalid language level" in message for message in self.errors(text)))

    def test_role_scope_word_limit_is_enforced(self):
        long_scope = " ".join(["scope"] * 81)
        text = VALID_DATABASE.replace("- Scope: Builds services.", f"- Scope: {long_scope}")
        findings = self.validate_text(text)
        self.assertTrue(any(
            item.level == "WARNING" and "scope exceeds 80 words" in item.message
            for item in findings
        ))

    def test_partial_database_is_structurally_valid_but_not_complete(self):
        text = """# Canonical Career Evidence Database

## 1. Database metadata

- Schema version: 1.0
- Last reviewed: 2026-10-28
- Default disclosure: Application-safe
- Language policy: Region-neutral English

## 2. Identity

- Name: Example Person
"""
        self.assertEqual([], self.errors(text))
        errors = self.errors(text, require_complete=True)
        self.assertIn("no role records found", errors)
        self.assertIn("no skill records found", errors)

    def test_reversed_dates_are_an_error(self):
        text = VALID_DATABASE.replace("- End: Present", "- End: 2023-12")
        findings = self.validate_text(text)
        self.assertTrue(any("end date precedes start date" in item.message for item in findings))

    def test_open_followup_is_a_warning(self):
        text = VALID_DATABASE + """

## 12. Data-quality follow-up

### Confirm metric

- ID: followup-confirm-metric
- Related records: ach-example-latency
- Priority: High
- Issue: Exact metric is missing.
- Resolution: Locate the performance report.
- Status: Open
"""
        findings = self.validate_text(text)
        self.assertTrue(
            any(item.level == "WARNING" and "open follow-up" in item.message for item in findings)
        )

    def test_skill_without_evidence_is_a_warning(self):
        text = VALID_DATABASE.replace(
            "- Evidence: role-example-engineer-2024, ach-example-latency",
            "- Evidence: Not documented",
        )
        findings = self.validate_text(text)
        self.assertTrue(
            any(item.level == "WARNING" and "no linked evidence" in item.message for item in findings)
        )


if __name__ == "__main__":
    unittest.main()
