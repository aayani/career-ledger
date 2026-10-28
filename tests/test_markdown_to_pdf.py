from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import redirect_stderr
from io import StringIO
import unittest

from scripts.markdown_to_pdf import parse_args


class MarkdownToPdfTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
