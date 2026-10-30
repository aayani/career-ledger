from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from scripts.inspect_profile import inspect_profile


class ProfileInspectionTests(unittest.TestCase):
    def inspect_text(self, text: str):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "profile.yaml"
            path.write_text(text, encoding="utf-8")
            return inspect_profile(path)

    def test_missing_path(self):
        with TemporaryDirectory() as directory:
            result = inspect_profile(Path(directory) / "missing.yaml")
        self.assertEqual("missing", result["content_state"])
        self.assertEqual(0, result["record_count"])

    def test_blank_and_empty_mapping_are_empty(self):
        for text in (
            "",
            "{}\n",
            "notes: []\neducation: []\nemployment: []\nprojects: []\n",
        ):
            with self.subTest(text=text):
                result = self.inspect_text(text)
                self.assertEqual("empty", result["content_state"])
                self.assertEqual(0, result["record_count"])

    def test_placeholders_are_not_substantive(self):
        result = self.inspect_text("person:\n  name:\n    first: '[First name]'\n")
        self.assertEqual("empty", result["content_state"])

    def test_populated_database_reports_counts(self):
        fixture = Path(__file__).parent / "fixtures" / "profile-valid.yaml"
        data = yaml.safe_load(fixture.read_text(encoding="utf-8"))
        data["employment"][0]["private"] = True
        data["notes"] = ["Confirm dates."]
        result = self.inspect_text(yaml.safe_dump(data, sort_keys=False))
        self.assertEqual("populated", result["content_state"])
        self.assertEqual(2, result["record_count"])
        self.assertEqual(1, result["employment_count"])
        self.assertEqual(1, result["education_count"])
        self.assertEqual(2, result["project_count"])
        self.assertEqual(2, result["skill_usage_count"])
        self.assertEqual(1, result["private_record_count"])
        self.assertEqual(1, result["note_count"])

    def test_invalid_yaml_is_reported(self):
        result = self.inspect_text("person: [\n")
        self.assertEqual("invalid", result["content_state"])
        self.assertIn("invalid profile YAML", result["error"])

    def test_invalid_collection_shapes_do_not_crash_inspection(self):
        result = self.inspect_text(
            "employment: not-a-list\neducation: {}\nprojects: bad\nnotes: 3\n"
        )
        self.assertEqual("invalid", result["content_state"])
        self.assertEqual(0, result["record_count"])
        self.assertGreater(result["validation_error_count"], 0)


if __name__ == "__main__":
    unittest.main()
