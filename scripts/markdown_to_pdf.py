#!/usr/bin/env python3
"""Convert a Markdown file to PDF."""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"

RESUME_CSS = """
body {
    color: #111;
    font-family: sans-serif;
    font-size: 9pt;
    line-height: 1.18;
}
h1 {
    font-size: 21pt;
    margin: 0 0 6pt;
}
h2 {
    font-size: 14pt;
    margin: 9pt 0 4pt;
}
h3 {
    font-size: 11pt;
    margin: 7pt 0 3pt;
}
h1, h2, h3, h3 + p {
    break-after: avoid;
    page-break-after: avoid;
}
p {
    margin: 0 0 5pt;
}
ul {
    margin: 2pt 0 5pt;
    padding-left: 16pt;
}
li {
    break-inside: avoid;
    page-break-inside: avoid;
    margin: 0 0 1pt;
}
a {
    color: #111;
    text-decoration: none;
}
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown_file", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args(argv)
    if not args.markdown_file.is_file():
        parser.error(f"Markdown file not found: {args.markdown_file}")
    return args


def resolve_output_path(source: Path, requested: Path | None = None) -> Path:
    return requested.resolve() if requested else OUTPUT_DIR / f"{source.stem}.pdf"


def main() -> None:
    args = parse_args()
    source = args.markdown_file.resolve()
    output = resolve_output_path(source, args.output)

    if source == output:
        raise SystemExit("Input and output paths must be different.")

    try:
        import markdown
        import pymupdf
    except ImportError as error:
        message = "Install dependencies from requirements/base.txt"
        raise SystemExit(message) from error

    html = markdown.markdown(
        source.read_text(encoding="utf-8"), extensions=["extra", "sane_lists"]
    )
    page = pymupdf.paper_rect("a4")
    content = page + (36, 36, -36, -36)
    story = pymupdf.Story(
        html=html,
        user_css=RESUME_CSS,
        archive=pymupdf.Archive(str(source.parent)),
    )
    document = story.write_with_links(lambda _number, _filled: (page, content, None))

    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        document.save(str(output))
    finally:
        document.close()
    print(output)


if __name__ == "__main__":
    main()
