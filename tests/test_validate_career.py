from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from scripts.career_schema import SCHEMA, SCHEMA_PATH, load_schema
from scripts.validate_career import validate


VALID_DATABASE = yaml.safe_load(
    (Path(__file__).parent / "fixtures" / "career-valid.yaml").read_text(encoding="utf-8")
)


class CareerValidationTests(unittest.TestCase):
    def validate_data(self, data, require_complete: bool = False):
        return self.validate_text(
            yaml.safe_dump(data, sort_keys=False),
            require_complete=require_complete,
        )

    def validate_text(self, text: str, require_complete: bool = False):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "career.yaml"
            path.write_text(text, encoding="utf-8")
            return validate(path, require_complete=require_complete)

    def errors(self, data, require_complete: bool = False):
        return [
            item.message
            for item in self.validate_data(data, require_complete=require_complete)
            if item.level == "ERROR"
        ]

    def test_valid_database_has_no_findings(self):
        self.assertEqual([], self.validate_data(VALID_DATABASE))

    def test_required_fields_and_unknown_fields_are_enforced(self):
        missing = deepcopy(VALID_DATABASE)
        missing["person"].pop("contact")
        self.assertTrue(any("required property" in message for message in self.errors(missing)))

        unknown = deepcopy(VALID_DATABASE)
        unknown["surprise"] = True
        self.assertTrue(any("Additional properties" in message for message in self.errors(unknown)))

    def test_formats_enums_and_id_patterns_are_enforced(self):
        invalid = deepcopy(VALID_DATABASE)
        invalid["person"]["contact"]["email"] = "not-an-email"
        invalid["employment"][0]["type"] = "casual"
        invalid["employment"][0]["id"] = "bad id"
        messages = self.errors(invalid)
        self.assertTrue(any("does not match" in message for message in messages))
        self.assertTrue(any("is not one of" in message for message in messages))

    def test_weightage_is_required_integer_from_one_to_ten(self):
        for value in (0, 4.5, 11):
            with self.subTest(value=value):
                invalid = deepcopy(VALID_DATABASE)
                invalid["projects"][0]["weightage"] = value
                self.assertNotEqual([], self.errors(invalid))

        missing = deepcopy(VALID_DATABASE)
        missing["projects"][0].pop("weightage")
        self.assertTrue(any("weightage" in message for message in self.errors(missing)))

    def test_unnamed_project_requires_description(self):
        valid = deepcopy(VALID_DATABASE)
        valid["projects"][0].pop("name")
        self.assertEqual([], self.errors(valid))

        invalid = deepcopy(valid)
        invalid["projects"][0].pop("description")
        self.assertNotEqual([], self.errors(invalid))

    def test_project_uses_star_fields(self):
        for field in ("situation", "task", "action", "result"):
            with self.subTest(field=field):
                valid = deepcopy(VALID_DATABASE)
                valid["projects"][0][field] = f"Example {field}."
                self.assertEqual([], self.errors(valid))

        for legacy_field in ("contribution", "outcome", "evidence"):
            with self.subTest(legacy_field=legacy_field):
                invalid = deepcopy(VALID_DATABASE)
                invalid["projects"][0][legacy_field] = "Legacy value."
                self.assertTrue(
                    any(
                        "Additional properties" in message
                        for message in self.errors(invalid)
                    )
                )

        blank = deepcopy(VALID_DATABASE)
        blank["projects"][0]["action"] = "   "
        self.assertTrue(any("does not match" in message for message in self.errors(blank)))

        for field in ("situation", "task", "action", "result"):
            with self.subTest(field=field, length=100):
                boundary = deepcopy(VALID_DATABASE)
                boundary["projects"][0][field] = "x" * 100
                self.assertEqual([], self.errors(boundary))

            with self.subTest(field=field, length=101):
                too_long = deepcopy(VALID_DATABASE)
                too_long["projects"][0][field] = "x" * 101
                self.assertTrue(
                    any("is too long" in message for message in self.errors(too_long))
                )

    def test_exact_duplicate_arrays_are_rejected(self):
        cases = []

        employment = deepcopy(VALID_DATABASE)
        employment["employment"].append(deepcopy(employment["employment"][0]))
        cases.append(employment)

        project = deepcopy(VALID_DATABASE)
        project["projects"].append(deepcopy(project["projects"][0]))
        cases.append(project)

        skill = deepcopy(VALID_DATABASE)
        skill["projects"][0]["skills"].append(
            deepcopy(skill["projects"][0]["skills"][0])
        )
        cases.append(skill)

        language = deepcopy(VALID_DATABASE)
        language["person"]["languages"].append(
            deepcopy(language["person"]["languages"][0])
        )
        cases.append(language)

        for data in cases:
            with self.subTest(data=data):
                self.assertTrue(any("non-unique" in message for message in self.errors(data)))

    def test_education_fields_follow_type(self):
        base = {
            "city": {"name": "Online", "country": "Online"},
            "type": "certification",
            "startDate": "2025-01",
            "credentialId": "ABC-123",
            "credentialUrl": "https://example.com/credential",
        }
        valid = deepcopy(VALID_DATABASE)
        valid["education"] = [base]
        self.assertEqual([], self.errors(valid))

        invalid = deepcopy(valid)
        invalid["education"][0]["degree"] = "Bachelor"
        self.assertNotEqual([], self.errors(invalid))

        invalid = deepcopy(VALID_DATABASE)
        invalid["education"] = [{**base, "type": "course", "credentialId": "ABC-123"}]
        self.assertNotEqual([], self.errors(invalid))

    def test_private_is_optional_boolean(self):
        valid = deepcopy(VALID_DATABASE)
        valid["employment"][0]["private"] = True
        valid["projects"][0]["skills"][0]["private"] = True
        self.assertEqual([], self.errors(valid))

        invalid = deepcopy(valid)
        invalid["employment"][0]["private"] = "yes"
        self.assertNotEqual([], self.errors(invalid))

    def test_skill_group_requires_unique_nonblank_keywords(self):
        missing = deepcopy(VALID_DATABASE)
        missing["projects"][0]["skills"][0].pop("keywords")
        self.assertTrue(any("keywords" in message for message in self.errors(missing)))

        duplicate = deepcopy(VALID_DATABASE)
        duplicate["projects"][0]["skills"][0]["keywords"] = [
            "Python",
            "Python",
        ]
        self.assertTrue(
            any("non-unique" in message for message in self.errors(duplicate))
        )

        blank = deepcopy(VALID_DATABASE)
        blank["projects"][0]["skills"][0]["keywords"] = ["   "]
        self.assertTrue(any("does not match" in message for message in self.errors(blank)))

    def test_project_employment_id_is_optional_and_validated(self):
        independent = deepcopy(VALID_DATABASE)
        independent["projects"][0].pop("employmentId")
        self.assertEqual([], self.errors(independent))

        invalid = deepcopy(VALID_DATABASE)
        invalid["projects"][0]["employmentId"] = ["bad id"]
        self.assertTrue(any("does not match" in message for message in self.errors(invalid)))

        scalar = deepcopy(VALID_DATABASE)
        scalar["projects"][0]["employmentId"] = "employment-example"
        self.assertTrue(any("is not of type" in message for message in self.errors(scalar)))

        duplicate = deepcopy(VALID_DATABASE)
        duplicate["projects"][0]["employmentId"] *= 2
        self.assertTrue(any("non-unique" in message for message in self.errors(duplicate)))

        dangling = deepcopy(VALID_DATABASE)
        dangling["projects"][0]["employmentId"] = ["employment-does-not-exist"]
        self.assertIn(
            "employmentId does not match any employment record",
            self.errors(dangling),
        )

        multiple = deepcopy(VALID_DATABASE)
        second_employment = deepcopy(multiple["employment"][0])
        second_employment["id"] = "employment-example-university-research-assistant-2020"
        multiple["employment"].append(second_employment)
        multiple["projects"][0]["employmentId"].append(second_employment["id"])
        self.assertEqual([], self.errors(multiple))

        nested = deepcopy(VALID_DATABASE)
        nested["employment"][0]["projects"] = [deepcopy(nested["projects"][0])]
        self.assertTrue(
            any("Additional properties" in message for message in self.errors(nested))
        )

    def test_duplicate_yaml_key_is_an_error(self):
        text = """person: {}
person: {}
location: {}
education: []
employment: []
projects: []
"""
        findings = self.validate_text(text)
        self.assertTrue(any("duplicate key" in item.message for item in findings))

    def test_non_mapping_root_is_an_error(self):
        findings = self.validate_text("- not\n- a\n- mapping\n")
        self.assertTrue(any("must be a YAML mapping" in item.message for item in findings))

    def test_partial_database_is_valid_but_not_complete(self):
        partial = deepcopy(VALID_DATABASE)
        partial["employment"] = []
        partial["projects"] = []
        self.assertEqual([], self.errors(partial))
        messages = self.errors(partial, require_complete=True)
        self.assertIn("no employment records found", messages)
        self.assertIn("no skill usages found", messages)

    def test_schema_is_loaded_from_schema_yaml(self):
        self.assertEqual("schema.yaml", SCHEMA_PATH.name)
        self.assertEqual("Career", SCHEMA["title"])
        with TemporaryDirectory() as directory:
            path = Path(directory) / "schema.yaml"
            schema = deepcopy(SCHEMA)
            schema["title"] = "Test Career"
            path.write_text(yaml.safe_dump(schema, sort_keys=False), encoding="utf-8")
            self.assertEqual("Test Career", load_schema(path)["title"])

    def test_schema_rejects_non_mapping_root(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "schema.yaml"
            path.write_text("- not\n- a\n- mapping\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "YAML mapping"):
                load_schema(path)


if __name__ == "__main__":
    unittest.main()
