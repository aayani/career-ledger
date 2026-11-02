import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import redirect_stderr
from io import StringIO
from zipfile import ZipFile
import unittest

from scripts.export_markdown import (
    OUTPUT_DIR,
    parse_args,
    paths_overlap,
    resolve_output_paths,
)

EXPORT_DEPS_AVAILABLE = importlib.util.find_spec("docx") is not None


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
            (
                OUTPUT_DIR / "backend-engineer.pdf",
                OUTPUT_DIR / "backend-engineer.docx",
            ),
            resolve_output_paths(source),
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

    def test_output_collision_is_case_insensitive(self):
        self.assertTrue(paths_overlap(Path("resume.DOCX"), Path("resume.docx")))
        self.assertTrue(paths_overlap(Path("resume.md"), Path("RESUME.MD")))

    @unittest.skipUnless(EXPORT_DEPS_AVAILABLE, "export dependencies are not installed")
    def test_docx_preserves_links_and_a4_styling(self):
        from scripts.export_markdown import write_docx

        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "resume.docx"
            write_docx(
                '<h1>Resume</h1><p><a href="https://example.com">Portfolio</a></p>'
                '<p><img src="ignored.png" alt="Ignored" /></p>',
                output,
            )

            with ZipFile(output) as archive:
                document = archive.read("word/document.xml").decode()
                relationships = archive.read(
                    "word/_rels/document.xml.rels"
                ).decode()
                styles = archive.read("word/styles.xml").decode()
                names = archive.namelist()

            self.assertIn("https://example.com", relationships)
            self.assertNotIn("Portfolio https://example.com", document)
            self.assertFalse(any(name.startswith("word/media/") for name in names))
            self.assertIn('w:w="11906"', document)
            self.assertIn('w:h="16838"', document)
            self.assertIn('w:val="111111"', styles)
            title = styles.split('w:styleId="Title"', 1)[1].split("</w:style>", 1)[0]
            self.assertNotIn("w:pBdr", title)


if __name__ == "__main__":
    unittest.main()
