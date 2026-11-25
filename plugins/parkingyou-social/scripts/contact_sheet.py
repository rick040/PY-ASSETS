#!/usr/bin/env python3
"""Contact sheet: every rendered image of a batch on one page, with the post id, format and QA status.

Usage:  python3 contact_sheet.py <post-dir or parent-dir> [...] --out sheet.png [--format feed] [--cols 6]
A parent dir is searched for post folders (folders with spec.json). The status bar under each tile is
green (pass), amber (warn), red (blocked) or grey (no qa.json).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

STATUS = {"pass": (46, 160, 67), "warn": (230, 160, 20), "blocked": (210, 40, 40), None: (160, 160, 160)}
ORDER = {"feed": 0, "story": 1, "square": 2, "landscape": 3}


def post_dirs(paths: list[Path]) -> list[Path]:
    out = []
    for p in paths:
        if (p / "spec.json").exists():
            out.append(p)
        else:
            out += sorted(d.parent for d in p.glob("*/spec.json"))
    return out


def images(d: Path, only: str | None) -> list[Path]:
    imgs = [p for p in d.glob("*.png") if "@2x" not in p.name]
    if only:
        imgs = [p for p in imgs if p.name.split("-")[0].split(".")[0] == only]
    return sorted(imgs, key=lambda p: (ORDER.get(p.stem.split("-")[0], 9), p.name))


def font(size: int):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


def build(dirs: list[Path], out: Path, only: str | None, cols: int, tile_h: int = 420) -> Path:
    tiles = []
    for d in dirs:
        spec = json.loads((d / "spec.json").read_text(encoding="utf-8"))
        qa = json.loads((d / "qa.json").read_text(encoding="utf-8")) if (d / "qa.json").exists() else {}
        for img in images(d, only):
            tiles.append((img, f"{spec['id']} · {spec.get('theme', '')} · {img.stem}", qa.get("status")))
    if not tiles:
        raise SystemExit("no images found")
    widths = []
    for img, _, _ in tiles:
        with Image.open(img) as im:
            widths.append(int(im.width * tile_h / im.height))
    col_w = max(widths) + 16
    rows = (len(tiles) + cols - 1) // cols
    label_h, bar_h = 28, 8
    sheet = Image.new("RGB", (cols * col_w + 16, rows * (tile_h + label_h + bar_h + 16) + 16), (245, 246, 250))
    draw = ImageDraw.Draw(sheet)
    f = font(15)
    for i, (img, label, status) in enumerate(tiles):
        x = 16 + (i % cols) * col_w
        y = 16 + (i // cols) * (tile_h + label_h + bar_h + 16)
        with Image.open(img) as im:
            t = im.convert("RGB").resize((int(im.width * tile_h / im.height), tile_h), Image.LANCZOS)
        sheet.paste(t, (x, y))
        draw.rectangle([x, y + tile_h, x + t.width, y + tile_h + bar_h], fill=STATUS.get(status, STATUS[None]))
        draw.text((x, y + tile_h + bar_h + 4), label, fill=(30, 30, 30), font=f)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--format", choices=list(ORDER), help="only this format")
    ap.add_argument("--cols", type=int, default=6)
    a = ap.parse_args(argv)
    print(build(post_dirs(a.paths), a.out, a.format, a.cols))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
