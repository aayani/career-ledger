from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.inspect_state import inspect


class InspectStateTests(unittest.TestCase):
    def inspect_text(self, text: str):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "career.md"
            path.write_text(text, encoding="utf-8")
            return inspect(path)

    def test_missing_path(self):
        with TemporaryDirectory() as directory:
            result = inspect(Path(directory) / "missing.md")
        self.assertEqual("missing", result["content_state"])
        self.assertEqual(0, result["record_count"])

    def test_non_substantive_documents_are_empty(self):
        documents = {
            "blank": "  \n",
            "headings": "# Career\n\n## 1. Database metadata\n",
            "metadata": (
                "# Career\n\n## 1. Database metadata\n\n"
                "- Schema version: 1.0\n- Last reviewed: [YYYY-MM-DD]\n"
            ),
            "placeholder": "# Career\n\n## 2. Identity\n\n- Name: [Full name]\n",
            "placeholder-record": (
                "# Career\n\n## 4. Experience\n\n### [Employer]\n\n"
                "#### [Role]\n\n- ID: role-[employer]-[role]-[start-year]\n"
            ),
        }
        for name, text in documents.items():
            with self.subTest(name=name):
                result = self.inspect_text(text)
                self.assertEqual("empty", result["content_state"])
                self.assertEqual(0, result["record_count"])

    def test_substantive_fact_is_populated(self):
        result = self.inspect_text("# Career\n\n## 2. Identity\n\n- Name: Example Person\n")
        self.assertEqual("populated", result["content_state"])
        self.assertEqual(1, result["substantive_field_count"])

    def test_markdown_link_is_substantive(self):
        result = self.inspect_text(
            "# Career\n\n## 2. Identity\n\n"
            "- Portfolio: [Portfolio](https://example.com)\n"
        )
        self.assertEqual("populated", result["content_state"])
        self.assertEqual(1, result["substantive_field_count"])


if __name__ == "__main__":
    unittest.main()
