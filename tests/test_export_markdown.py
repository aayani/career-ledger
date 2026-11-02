from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import redirect_stderr
from io import StringIO
import unittest

from scripts.export_markdown import (
    OUTPUT_DIR,
    parse_args,
    resolve_output_path,
    resolve_output_paths,
)


class ExportMarkdownTests(unittest.TestCase):
    def test_input_and_optional_output(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "resume.md"
            source.write_text("# Resume\n", encoding="utf-8")
            args = parse_args([str(source)])
            self.assertEqual(source, args.markdown_file)
            self.assertIsNone(args.output)

            output = Path(directory) / "resume.pdf"
            args = parse_args([str(source), "--output", str(output)])
            self.assertEqual(output, args.output)

    def test_missing_input_is_rejected(self):
        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit):
                parse_args(["missing.md"])

    def test_default_output_uses_output_directory(self):
        source = Path("docs/resume/backend-engineer.md")
        self.assertEqual(
            OUTPUT_DIR / "backend-engineer.pdf",
            resolve_output_path(source),
        )

    def test_docx_output_is_alongside_pdf(self):
        source = Path("docs/resume/backend-engineer.md")
        self.assertEqual(
            (
                OUTPUT_DIR / "backend-engineer.pdf",
                OUTPUT_DIR / "backend-engineer.docx",
            ),
            resolve_output_paths(source),
        )

        requested = Path("custom/resume.pdf")
        self.assertEqual(
            (requested.resolve(), requested.resolve().with_suffix(".docx")),
            resolve_output_paths(source, requested),
        )


if __name__ == "__main__":
    unittest.main()
