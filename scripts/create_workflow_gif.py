#!/usr/bin/env python3
"""Generate the animated career workflow used as the README cover."""

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
    line,
    rounded,
    text,
)


SIZE = (1100, 250)
CARD_WIDTH = 174
CARDS = (
    (31, "EVIDENCE", "CVs · notes", "evidence", COLORS["cyan"]),
    (247, "PROFILE", "profile.yaml", "profile", COLORS["purple"]),
    (463, "VALIDATE", "schema checks", "validate", COLORS["green"]),
    (679, "RESUME", "tailored output", "resume", COLORS["yellow"]),
    (895, "EXPORT", "PDF or DOCX", "export", COLORS["pink"]),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=IMAGE_DIR / "workflow.gif",
    )
    return parser.parse_args()


def draw_arrow(draw: ImageDraw.ImageDraw, x1: int, x2: int, y: int) -> None:
    line(draw, ((x1, y), (x2, y)), COLORS["border"], 3)
    draw.polygon(
        (
            (x2 * SCALE, y * SCALE),
            ((x2 - 8) * SCALE, (y - 6) * SCALE),
            ((x2 - 8) * SCALE, (y + 6) * SCALE),
        ),
        fill=COLORS["border"],
    )


def draw_icon(
    draw: ImageDraw.ImageDraw,
    kind: str,
    center: tuple[int, int],
    color: str,
) -> None:
    x, y = center
    if kind == "evidence":
        for offset in (8, 4, 0):
            rounded(
                draw,
                (x - 25 + offset, y - 24 - offset, x + 17 + offset, y + 25 - offset),
                3,
                None,
                color,
                2,
            )
        line(draw, ((x - 13, y - 11), (x + 11, y - 11)), color, 2)
        line(draw, ((x - 13, y - 2), (x + 11, y - 2)), color, 2)
    elif kind == "profile":
        draw.ellipse(
            ((x - 26) * SCALE, (y - 23) * SCALE, (x + 26) * SCALE, (y - 8) * SCALE),
            outline=color,
            width=2 * SCALE,
        )
        line(draw, ((x - 26, y - 15), (x - 26, y + 19)), color, 2)
        line(draw, ((x + 26, y - 15), (x + 26, y + 19)), color, 2)
        draw.arc(
            ((x - 26) * SCALE, (y + 10) * SCALE, (x + 26) * SCALE, (y + 26) * SCALE),
            0,
            180,
            fill=color,
            width=2 * SCALE,
        )
        draw.arc(
            ((x - 26) * SCALE, (y - 3) * SCALE, (x + 26) * SCALE, (y + 13) * SCALE),
            0,
            180,
            fill=color,
            width=2 * SCALE,
        )
    elif kind == "validate":
        points = (
            (x, y - 30),
            (x + 28, y - 15),
            (x + 23, y + 18),
            (x, y + 31),
            (x - 23, y + 18),
            (x - 28, y - 15),
        )
        draw.polygon(
            [(px * SCALE, py * SCALE) for px, py in points],
            outline=color,
        )
        line(draw, ((x - 13, y), (x - 3, y + 11), (x + 17, y - 13)), color, 5)
    elif kind == "resume":
        rounded(draw, (x - 23, y - 30, x + 23, y + 30), 3, None, color, 2)
        draw.ellipse(
            ((x - 13) * SCALE, (y - 18) * SCALE, (x - 3) * SCALE, (y - 8) * SCALE),
            outline=color,
            width=2 * SCALE,
        )
        line(draw, ((x + 4, y - 14), (x + 14, y - 14)), color, 2)
        line(draw, ((x - 13, y + 1), (x + 14, y + 1)), color, 2)
        line(draw, ((x - 13, y + 11), (x + 14, y + 11)), color, 2)
    else:
        rounded(draw, (x - 35, y - 25, x - 3, y + 25), 3, None, color, 2)
        rounded(draw, (x + 3, y - 25, x + 35, y + 25), 3, None, color, 2)
        text(draw, (x - 19, y), "P", 15, color, "mm")
        text(draw, (x + 19, y), "D", 15, color, "mm")


def create_frame(active: int, progress: float) -> Image.Image:
    image = canvas(SIZE)
    draw = ImageDraw.Draw(image)
    for index, (x, label, subtitle, icon, accent) in enumerate(CARDS):
        executed = index <= active
        border = accent if index == active else COLORS["border"]
        border_width = 4 if index == active else 2
        icon_color = accent if executed else COLORS["disabled"]
        label_color = COLORS["text"] if executed else COLORS["disabled"]
        subtitle_color = COLORS["muted"] if executed else COLORS["border"]
        rounded(
            draw,
            (x, 39, x + CARD_WIDTH, 212),
            15,
            COLORS["panel"],
            border,
            border_width,
        )
        draw_icon(draw, icon, (x + CARD_WIDTH // 2, 95), icon_color)
        text(draw, (x + CARD_WIDTH // 2, 153), label, 17, label_color, "mm")
        text(
            draw,
            (x + CARD_WIDTH // 2, 184),
            subtitle,
            13,
            subtitle_color,
            "mm",
        )
        if index < len(CARDS) - 1:
            draw_arrow(draw, x + CARD_WIDTH + 8, CARDS[index + 1][0] - 9, 125)

    x, _, _, _, accent = CARDS[active]
    if active < len(CARDS) - 1:
        start = x + CARD_WIDTH + 9
        end = CARDS[active + 1][0] - 10
        dot_x = start + (end - start) * progress
        dot_y = 125
    else:
        dot_x = x + CARD_WIDTH // 2
        dot_y = 231
    radius = 10 + int(2 * progress)
    draw.ellipse(
        (
            (dot_x - radius) * SCALE,
            (dot_y - radius) * SCALE,
            (dot_x + radius) * SCALE,
            (dot_y + radius) * SCALE,
        ),
        fill=accent,
    )
    draw.ellipse(
        (
            (dot_x - 3) * SCALE,
            (dot_y - 3) * SCALE,
            (dot_x + 3) * SCALE,
            (dot_y + 3) * SCALE,
        ),
        fill="white",
    )
    return finish(image, SIZE)


def create_gif(output: Path) -> None:
    gif = GifBuilder(output)
    for active in range(len(CARDS)):
        for frame_index in range(10):
            progress = max(0, (frame_index - 4) / 5)
            gif.add(create_frame(active, progress), 110 if frame_index < 9 else 500)
    gif.save()


def main() -> None:
    create_gif(parse_args().output)


if __name__ == "__main__":
    main()
