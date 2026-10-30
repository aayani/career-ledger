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
                invalid["employment"][0]["projects"][0]["weightage"] = value
                self.assertNotEqual([], self.errors(invalid))

        missing = deepcopy(VALID_DATABASE)
        missing["employment"][0]["projects"][0].pop("weightage")
        self.assertTrue(any("weightage" in message for message in self.errors(missing)))

    def test_unnamed_work_item_requires_description(self):
        valid = deepcopy(VALID_DATABASE)
        valid["employment"][0]["projects"][0].pop("name")
        self.assertEqual([], self.errors(valid))

        invalid = deepcopy(valid)
        invalid["employment"][0]["projects"][0].pop("description")
        self.assertNotEqual([], self.errors(invalid))

    def test_exact_duplicate_arrays_are_rejected(self):
        cases = []

        employment = deepcopy(VALID_DATABASE)
        employment["employment"].append(deepcopy(employment["employment"][0]))
        cases.append(employment)

        project = deepcopy(VALID_DATABASE)
        project["employment"][0]["projects"].append(
            deepcopy(project["employment"][0]["projects"][0])
        )
        cases.append(project)

        skill = deepcopy(VALID_DATABASE)
        skill["employment"][0]["projects"][0]["skills"].append(
            deepcopy(skill["employment"][0]["projects"][0]["skills"][0])
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
        valid["employment"][0]["projects"][0]["skills"][0]["private"] = True
        self.assertEqual([], self.errors(valid))

        invalid = deepcopy(valid)
        invalid["employment"][0]["private"] = "yes"
        self.assertNotEqual([], self.errors(invalid))

    def test_duplicate_yaml_key_is_an_error(self):
        text = """person: {}
person: {}
location: {}
education: []
employment: []
"""
        findings = self.validate_text(text)
        self.assertTrue(any("duplicate key" in item.message for item in findings))

    def test_non_mapping_root_is_an_error(self):
        findings = self.validate_text("- not\n- a\n- mapping\n")
        self.assertTrue(any("must be a YAML mapping" in item.message for item in findings))

    def test_partial_database_is_valid_but_not_complete(self):
        partial = deepcopy(VALID_DATABASE)
        partial["employment"] = []
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
