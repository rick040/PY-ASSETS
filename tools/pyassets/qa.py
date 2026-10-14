"""Visual QA: source crop next to the extracted SVG."""
from __future__ import annotations

import io
import os

import cairosvg
import pymupdf
from PIL import Image, ImageDraw

from .core import PT_MM, Element, Source

PX_MM = 96 / 25.4


def crop_img(src: Source, pno: int, bbox, s=4.0, pad=6):
    x0, y0, x1, y1 = bbox
    r = pymupdf.Rect(x0 - pad, y0 - pad, x1 + pad, y1 + pad)
    pix = src.page(pno).get_pixmap(matrix=pymupdf.Matrix(s, s), clip=r, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def svg_img(el: Element, s=4.0, pad=6):
    """Render the element so one source point equals s pixels."""
    svg = el.svg()
    scale = (s / el.mm_per_pt) / PX_MM
    cols = set(el.colors())
    bg = "#7A7A7A" if "#FFFFFF" in cols and len(cols) <= 3 else "#FFFFFF"  # artwork with white parts is checked on grey
    png = cairosvg.svg2png(bytestring=svg.encode(), scale=scale, background_color=bg)
    im = Image.open(io.BytesIO(png)).convert("RGB")
    out = Image.new("RGB", (im.width + int(2 * pad * s), im.height + int(2 * pad * s)), bg)
    out.paste(im, (int(pad * s), int(pad * s)))
    return out


def compare(src: Source, el: Element, pno=None, bbox=None, s=4.0, path=None, maxw=1500):
    pno = pno or (el.page if isinstance(el.page, int) or el.page is None else el.page[0])
    bbox = bbox or el.bbox()
    b = svg_img(el, s)
    a = crop_img(src, pno, bbox, s) if pno else Image.new("RGB", (8, 8), "white")
    h = max(a.height, b.height)
    sheet = Image.new("RGB", (a.width + b.width + 30, h + 24), (235, 235, 235))
    sheet.paste(a, (0, 24))
    sheet.paste(b, (a.width + 30, 24))
    d = ImageDraw.Draw(sheet)
    d.text((4, 4), f"{el.id}  p{pno}  source", fill=(200, 0, 0))
    d.text((a.width + 34, 4), "extracted svg", fill=(0, 120, 0))
    if sheet.width > maxw:
        k = maxw / sheet.width
        sheet = sheet.resize((maxw, int(sheet.height * k)))
    if path:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        sheet.save(path)
    return sheet


def groups(src: Source, pno: int, region=None, gap=2.0, min_area=0.0, fills=None):
    """Cluster vector paths (and optionally text) by overlap/proximity. Returns list of (bbox, count, colours)."""
    rs = []
    for d in src.drawings(pno):
        r = d["rect"]
        if region and not (r.x0 >= region[0] - 1 and r.y0 >= region[1] - 1 and r.x1 <= region[2] + 1 and r.y1 <= region[3] + 1):
            continue
        if r.width * r.height < min_area and (r.width > 0.1 and r.height > 0.1):
            continue
        col = d.get("fill") or d.get("color")
        rs.append([r.x0, r.y0, r.x1, r.y1, 1, {tuple(round(v * 255) for v in col[:3]) if col else None}])
    changed = True
    while changed:
        changed = False
        out = []
        for r in rs:
            for o in out:
                if not (r[2] < o[0] - gap or r[0] > o[2] + gap or r[3] < o[1] - gap or r[1] > o[3] + gap):
                    o[0] = min(o[0], r[0]); o[1] = min(o[1], r[1]); o[2] = max(o[2], r[2]); o[3] = max(o[3], r[3])
                    o[4] += r[4]; o[5] |= r[5]
                    changed = True
                    break
            else:
                out.append(list(r))
        rs = out
    rs.sort(key=lambda r: (round(r[1] / 20), r[0]))
    return [((round(r[0], 1), round(r[1], 1), round(r[2], 1), round(r[3], 1)), r[4], sorted("#%02X%02X%02X" % c for c in r[5] if c)[:4]) for r in rs]
