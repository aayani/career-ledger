#!/usr/bin/env python3
"""Generate the animated terminal walkthrough used in the README."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

from gif_utils import (
    COLORS,
    GifBuilder,
    IMAGE_DIR,
    SCALE,
    canvas,
    finish,
    font,
    rounded,
    text,
)


SIZE = (900, 500)

SCENES = (
    (
        "/career-ledger import",
        (
            ("Reconciling career evidence...", COLORS["muted"]),
            ("✓ Updated data/profile.yaml", COLORS["green"]),
        ),
    ),
    (
        "/career-ledger clarify",
        (
            ("Inspecting profile gaps...", COLORS["muted"]),
            ("✓ Profile is ready", COLORS["green"]),
        ),
    ),
    (
        "/career-ledger generate",
        (
            ("Generating focused resume...", COLORS["muted"]),
            ("✓ Saved docs/resume/product-engineer.md", COLORS["green"]),
        ),
    ),
    (
        "make pdf path=docs/resume/product-engineer.md",
        (
            ("Rendering compact A4 resume...", COLORS["muted"]),
            ("✓ Saved output/product-engineer.pdf", COLORS["green"]),
        ),
    ),
    (
        "make docx path=docs/resume/product-engineer.md",
        (
            ("Rendering editable A4 resume...", COLORS["muted"]),
            ("✓ Saved output/product-engineer.docx", COLORS["green"]),
        ),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=IMAGE_DIR / "terminal-demo.gif",
    )
    return parser.parse_args()


def create_frame(
    scene_index: int,
    command: str,
    visible: int,
    results: tuple[tuple[str, str], ...],
) -> Image.Image:
    image = canvas(SIZE)
    draw = ImageDraw.Draw(image)

    rounded(draw, (29, 29, 871, 471), 15, COLORS["panel"], COLORS["border"], 2)
    rounded(draw, (29, 29, 871, 78), 15, COLORS["header"])
    draw.rectangle(
        (29 * SCALE, 63 * SCALE, 871 * SCALE, 78 * SCALE),
        fill=COLORS["header"],
    )

    for x, color in (
        (52, COLORS["pink"]),
        (73, COLORS["yellow"]),
        (94, COLORS["green"]),
    ):
        draw.ellipse(
            ((x - 6) * SCALE, 41 * SCALE, (x + 6) * SCALE, 53 * SCALE),
            fill=color,
        )
    text(draw, (450, 51), "AI Agent", 13, COLORS["muted"], "mm")

    text(draw, (64, 123), "$", 20, COLORS["cyan"], "lm")
    typed = command[:visible]
    text(draw, (87, 123), typed, 20, COLORS["text"], "lm")
    cursor_x = 87 + draw.textlength(typed, font=font(20)) / SCALE + 3
    draw.rectangle(
        (cursor_x * SCALE, 112 * SCALE, (cursor_x + 10) * SCALE, 134 * SCALE),
        fill=COLORS["purple"],
    )

    if visible >= len(command):
        for row, (message, color) in enumerate(results):
            text(draw, (64, 180 + row * 38), message, 15, color, "lm")

    bar_width = 96
    gap = 14
    left = (SIZE[0] - (bar_width * len(SCENES) + gap * (len(SCENES) - 1))) // 2
    for index in range(len(SCENES)):
        color = COLORS["purple"] if index == scene_index else COLORS["border"]
        x = left + index * (bar_width + gap)
        rounded(draw, (x, 442, x + bar_width, 448), 3, color)

    return finish(image, SIZE)


def create_gif(output: Path) -> None:
    gif = GifBuilder(output)
    for scene_index, (command, results) in enumerate(SCENES):
        gif.add(create_frame(scene_index, command, 0, results), 260)
        for visible in range(2, len(command) + 1, 2):
            gif.add(
                create_frame(scene_index, command, min(visible, len(command)), results),
                55,
            )
        if len(command) % 2:
            gif.add(create_frame(scene_index, command, len(command), results), 55)
        gif.add(create_frame(scene_index, command, len(command), results), 1100)

    gif.save()


def main() -> None:
    create_gif(parse_args().output)


if __name__ == "__main__":
    main()
