"""Shared drawing helpers for the repository GIF generators."""

from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SCALE = 2
ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = ROOT / "docs" / "images"

COLORS = {
    "background": "#08111f",
    "panel": "#111a2b",
    "header": "#182238",
    "border": "#30415e",
    "disabled": "#536078",
    "muted": "#8390a8",
    "text": "#e8edf5",
    "cyan": "#5ee7f7",
    "purple": "#a881ff",
    "green": "#6ee7a8",
    "yellow": "#ffd34e",
    "pink": "#ff6b8b",
}

FONT_CANDIDATES = (
    Path("/System/Library/Fonts/SFNSMono.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    Path("C:/Windows/Fonts/consola.ttf"),
)


@lru_cache
def font(size: int):
    for path in FONT_CANDIDATES:
        if path.is_file():
            return ImageFont.truetype(path, size * SCALE)
    return ImageFont.load_default(size=size * SCALE)


def canvas(size: tuple[int, int]) -> Image.Image:
    return Image.new(
        "RGB",
        (size[0] * SCALE, size[1] * SCALE),
        COLORS["background"],
    )


def rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str | None = None,
    outline: str | None = None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(
        tuple(value * SCALE for value in box),
        radius=radius * SCALE,
        fill=fill,
        outline=outline,
        width=width * SCALE,
    )


def line(
    draw: ImageDraw.ImageDraw,
    points: tuple[tuple[int, int], ...],
    fill: str,
    width: int = 1,
) -> None:
    draw.line(
        [(x * SCALE, y * SCALE) for x, y in points],
        fill=fill,
        width=width * SCALE,
    )


def text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    value: str,
    size: int,
    fill: str,
    anchor: str | None = None,
) -> None:
    draw.text(
        (xy[0] * SCALE, xy[1] * SCALE),
        value,
        font=font(size),
        fill=fill,
        anchor=anchor,
    )


def finish(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.resize(size, Image.Resampling.LANCZOS)


class GifBuilder:
    """Quantize frames immediately to keep animation memory use low."""

    def __init__(self, output: Path):
        self.output = output
        self.frames: list[Image.Image] = []
        self.durations: list[int] = []
        self.palette: Image.Image | None = None

    def add(self, frame: Image.Image, duration: int) -> None:
        if self.palette is None:
            swatch_height = 24
            palette_source = Image.new(
                "RGB", (frame.width, frame.height + swatch_height)
            )
            palette_source.paste(frame)
            swatches = ImageDraw.Draw(palette_source)
            swatch_width = frame.width / len(COLORS)
            for index, color in enumerate(COLORS.values()):
                swatches.rectangle(
                    (
                        round(index * swatch_width),
                        frame.height,
                        round((index + 1) * swatch_width),
                        frame.height + swatch_height,
                    ),
                    fill=color,
                )
            self.palette = palette_source.convert(
                "P", palette=Image.Palette.ADAPTIVE, colors=128
            )
        quantized = frame.quantize(palette=self.palette)
        self.frames.append(quantized)
        self.durations.append(duration)

    def save(self) -> None:
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.frames[0].save(
            self.output,
            save_all=True,
            append_images=self.frames[1:],
            duration=self.durations,
            loop=0,
            optimize=True,
            disposal=1,
        )
