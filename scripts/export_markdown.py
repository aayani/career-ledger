#!/usr/bin/env python3
"""Export a Markdown file to PDF or DOCX."""

import argparse
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"
MARKDOWN_EXTENSIONS = ("extra", "sane_lists", "toc")

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
    parser.add_argument("--format", choices=("docx", "pdf"), required=True)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args(argv)
    if not args.markdown_file.is_file():
        parser.error(f"Markdown file not found: {args.markdown_file}")
    return args


def resolve_output_path(
    source: Path, output_format: str, requested: Path | None = None
) -> Path:
    return (
        requested.resolve()
        if requested
        else OUTPUT_DIR / f"{source.stem}.{output_format}"
    )


def paths_overlap(*paths: Path) -> bool:
    """Return whether paths may address the same case-insensitive file."""
    normalized = [str(path).casefold() for path in paths]
    return len(normalized) != len(set(normalized))


def _append_hyperlink(paragraph: Any, text: str, url: str) -> None:
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.opc.constants import RELATIONSHIP_TYPE

    relationship = paragraph.part.relate_to(
        url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship)
    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")
    for tag, value in (("w:color", "111111"), ("w:u", "none")):
        property_node = OxmlElement(tag)
        property_node.set(qn("w:val"), value)
        properties.append(property_node)
    run.append(properties)
    text_node = OxmlElement("w:t")
    text_node.text = text
    run.append(text_node)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def _append_inline(
    paragraph: Any,
    element: Any,
    *,
    bold: bool = False,
    italic: bool = False,
    code: bool = False,
) -> None:
    def add_text(text: str | None) -> None:
        if not text:
            return
        run = paragraph.add_run(text)
        if bold:
            run.bold = True
        if italic:
            run.italic = True
        if code:
            run.font.name = "Courier New"

    add_text(element.text)
    for child in element:
        if not isinstance(child.tag, str):
            add_text(child.tail)
            continue
        tag = child.tag.lower()
        if tag == "a":
            _append_hyperlink(paragraph, "".join(child.itertext()), child.get("href", ""))
        elif tag == "br":
            paragraph.add_run().add_break()
        elif tag not in {"img", "ol", "ul"}:
            _append_inline(
                paragraph,
                child,
                bold=bold or tag in {"b", "strong"},
                italic=italic or tag in {"em", "i"},
                code=code or tag == "code",
            )
        add_text(child.tail)


def _append_blocks(document: Any, elements: list[Any], level: int = 1) -> None:
    for element in elements:
        if not isinstance(element.tag, str):
            continue
        tag = element.tag.lower()
        if tag in {"ul", "ol"}:
            kind = "Bullet" if tag == "ul" else "Number"
            suffix = f" {min(level, 3)}" if level > 1 else ""
            for item in element.findall("li"):
                paragraph = document.add_paragraph(style=f"List {kind}{suffix}")
                _append_inline(paragraph, item)
                nested = [
                    child
                    for child in item
                    if isinstance(child.tag, str) and child.tag.lower() in {"ul", "ol"}
                ]
                _append_blocks(document, nested, level + 1)
        elif tag not in {"hr", "img", "table"}:
            style = {"h1": "Title", "h2": "Heading 2"}.get(tag)
            if style is None and tag.startswith("h"):
                style = "Heading 3"
            paragraph = document.add_paragraph(style=style)
            _append_inline(paragraph, element)


def _style_docx(document: Any) -> None:
    from docx.oxml.ns import qn
    from docx.shared import Inches, Mm, Pt, RGBColor

    for section in document.sections:
        section.page_width = Mm(210)
        section.page_height = Mm(297)
        section.top_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)

    styles = {
        "Normal": (9, 0, 5, False),
        "Title": (21, 0, 6, True),
        "Heading 2": (14, 9, 4, True),
        "Heading 3": (11, 7, 3, True),
    }
    for name, (size, before, after, keep_with_next) in styles.items():
        style = document.styles[name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = keep_with_next
        style.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
        style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = keep_with_next
    document.styles["Normal"].paragraph_format.line_spacing = 1.18

    title_properties = document.styles["Title"]._element.pPr
    title_border = title_properties.find(qn("w:pBdr"))
    if title_border is not None:
        title_properties.remove(title_border)

    for kind in ("Bullet", "Number"):
        for level in ("", " 2", " 3"):
            style = document.styles[f"List {kind}{level}"]
            style.font.name = "Arial"
            style.font.size = Pt(9)
            style.paragraph_format.space_after = Pt(1)


def write_docx(html: str, output: Path) -> None:
    """Write an editable, styled DOCX. Images are intentionally omitted."""
    from docx import Document
    from lxml import html as lxml_html

    root = lxml_html.fragment_fromstring(html, create_parent="body")
    document = Document()
    _append_blocks(document, list(root))
    _style_docx(document)
    document.save(output)


def write_pdf(html: str, source: Path, output: Path) -> None:
    import pymupdf

    page = pymupdf.paper_rect("a4")
    content = page + (36, 36, -36, -36)
    story = pymupdf.Story(
        html=html,
        user_css=RESUME_CSS,
        archive=pymupdf.Archive(str(source.parent)),
    )
    document = story.write_with_links(lambda _number, _filled: (page, content, None))
    try:
        document.save(str(output))
    finally:
        document.close()


def main() -> None:
    args = parse_args()
    source = args.markdown_file.resolve()
    output = resolve_output_path(source, args.format, args.output)

    if paths_overlap(source, output):
        raise SystemExit("Input and output paths must be different.")

    try:
        import markdown
    except ImportError as error:
        message = "Install dependencies from requirements/export.txt"
        raise SystemExit(message) from error

    html = markdown.markdown(
        source.read_text(encoding="utf-8"), extensions=MARKDOWN_EXTENSIONS
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        if args.format == "pdf":
            write_pdf(html, source, output)
        else:
            write_docx(html, output)
    except ImportError as error:
        message = "Install dependencies from requirements/export.txt"
        raise SystemExit(message) from error

    print(output)


if __name__ == "__main__":
    main()
