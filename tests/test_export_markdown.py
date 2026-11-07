import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import redirect_stderr
from io import StringIO
from zipfile import ZipFile
import unittest

from scripts.export_markdown import (
    MARKDOWN_EXTENSIONS,
    OUTPUT_DIR,
    parse_args,
    paths_overlap,
    resolve_output_path,
)

EXPORT_DEPS_AVAILABLE = importlib.util.find_spec("docx") is not None
PDF_DEPS_AVAILABLE = all(
    importlib.util.find_spec(dependency) is not None
    for dependency in ("markdown", "pymupdf")
)


class ExportMarkdownTests(unittest.TestCase):
    def test_input_and_optional_output(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "resume.md"
            source.write_text("# Resume\n", encoding="utf-8")
            args = parse_args([str(source), "--format", "pdf"])
            self.assertEqual(source, args.markdown_file)
            self.assertEqual("pdf", args.format)
            self.assertIsNone(args.output)

            output = Path(directory) / "resume.pdf"
            args = parse_args(
                [str(source), "--format", "pdf", "--output", str(output)]
            )
            self.assertEqual(output, args.output)

    def test_missing_input_is_rejected(self):
        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit):
                parse_args(["missing.md", "--format", "pdf"])

    def test_default_outputs_use_output_directory(self):
        source = Path("docs/resume/backend-engineer.md")
        self.assertEqual(
            OUTPUT_DIR / "backend-engineer.pdf",
            resolve_output_path(source, "pdf"),
        )
        self.assertEqual(
            OUTPUT_DIR / "backend-engineer.docx",
            resolve_output_path(source, "docx"),
        )

        requested = Path("custom/resume.pdf")
        self.assertEqual(
            requested.resolve(),
            resolve_output_path(source, "pdf", requested),
        )

    def test_output_collision_is_case_insensitive(self):
        self.assertTrue(paths_overlap(Path("resume.DOCX"), Path("resume.docx")))
        self.assertTrue(paths_overlap(Path("resume.md"), Path("RESUME.MD")))

    @unittest.skipUnless(PDF_DEPS_AVAILABLE, "PDF dependencies are not installed")
    def test_pdf_resolves_heading_links(self):
        import markdown

        from scripts.export_markdown import write_pdf

        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "resume.md"
            output = root / "resume.pdf"
            source.write_text(
                "[Experience](#experience)\n\n## Experience\n", encoding="utf-8"
            )
            html = markdown.markdown(
                source.read_text(encoding="utf-8"),
                extensions=MARKDOWN_EXTENSIONS,
            )

            self.assertIn('id="experience"', html)
            write_pdf(html, source, output)
            self.assertTrue(output.read_bytes().startswith(b"%PDF"))

    @unittest.skipUnless(EXPORT_DEPS_AVAILABLE, "export dependencies are not installed")
    def test_docx_preserves_links_and_a4_styling(self):
        from scripts.export_markdown import write_docx

        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "resume.docx"
            write_docx(
                '<!-- note --><h1>Resume</h1>'
                '<p><a href="https://example.com">Portfolio</a><!-- note --></p>'
                '<p>First line<br>Second line</p>'
                '<p><img src="ignored.png" alt="Ignored"></p>',
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
            self.assertIn("First line", document)
            self.assertIn("Second line", document)
            self.assertNotIn("note", document)
            self.assertNotIn("Portfolio https://example.com", document)
            self.assertFalse(any(name.startswith("word/media/") for name in names))
            self.assertIn('w:w="11906"', document)
            self.assertIn('w:h="16838"', document)
            self.assertIn('w:val="111111"', styles)
            title = styles.split('w:styleId="Title"', 1)[1].split("</w:style>", 1)[0]
            self.assertNotIn("w:pBdr", title)


if __name__ == "__main__":
    unittest.main()
