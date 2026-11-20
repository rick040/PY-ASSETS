#!/usr/bin/env python3
"""Build the print file (drukbestand) for the ParkingYou geurhanger (Aroman custom shape air freshener).

The hanger is die-cut in the shape of the official beeldmerk (svg/atom/py-atom-logo-beeldmerk-color.svg),
with a white paper border around it, like the Aroman proof. Output:

  drukwerk/geurhanger-aroman/parkingyou-geurhanger-<size>.pdf   page 1 voorkant, page 2 achterkant (mirrored shape)
  drukwerk/geurhanger-aroman/parkingyou-geurhanger-<size>-preview.png

PDF: DeviceCMYK brand values from tokens.json, no white objects (the white is paper; the URL is knocked out of the
ring), all text outlined, cut contour plus hanger hole as a 0.25 pt stroke in the spot colour "CutContour" (overprint),
TrimBox = cut contour bounds, 3 mm bleed (white).

Usage: python3 -I tools/build_geurhanger.py [--size standaard|groot]
Needs: skia-pathops, fonttools, reportlab, pymupdf (preview), fonts/Ubuntu-Medium.ttf.
"""
import argparse
import json
import math
import os
import re

import pathops
from fontTools.ttLib import TTFont
from reportlab.lib.colors import CMYKColor, CMYKColorSep
from reportlab.pdfgen import canvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "drukwerk", "geurhanger-aroman")
MM = 72.0 / 25.4

# Aroman formats: max bounding box area of the hanger (standaard 56 cm2 = 7 x 8 cm, grootformaat 64 cm2 = 8 x 8 cm)
SIZES = {"standaard": 5600.0, "groot": 6400.0}
BORDER = 3.5        # white paper border between the beeldmerk and the cut line, mm (proof: about 3.5 mm)
FILLET = 2.0        # radius on the inner corner where the tail meets the bubble, mm
BLEED = 3.0         # mm, white
HOLE_D = 3.0        # hanger hole diameter, mm; centre on the top edge of the beeldmerk (as on the proof)
URL = "www.parkingyou.nl"
URL_PT = 9.0        # Ubuntu Medium, white knock-out in the ring
URL_ANGLE = 45.0    # centre of the URL on the ring, degrees clockwise from 3 o'clock (proof: lower right)
URL_TRACK = 0.02    # extra letter spacing, em


# ---------------------------------------------------------------- geometry helpers

def parse_svg_path(d):
    """Absolute M/L/C/Z only (that is all the library logo uses). Returns list of contours of (verb, pts)."""
    toks = re.findall(r"[MLCZmlcz]|-?\d*\.?\d+(?:e-?\d+)?", d)
    contours, cur, i, cmd = [], None, 0, None
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in "Zz":
                cur.append(("Z", []))
            continue
        n = {"M": 2, "L": 2, "C": 6}[cmd]
        v = [float(x) for x in toks[i:i + n]]
        i += n
        pts = [(v[k], v[k + 1]) for k in range(0, n, 2)]
        if cmd == "M":
            cur = [("M", pts)]
            contours.append(cur)
            cmd = "L"
        else:
            cur.append((cmd, pts))
    return contours


def to_pathops(contours, xf):
    p = pathops.Path()
    for c in contours:
        for verb, pts in c:
            q = [xf(*pt) for pt in pts]
            if verb == "M":
                p.moveTo(*q[0])
            elif verb == "L":
                p.lineTo(*q[0])
            elif verb == "C":
                p.cubicTo(*q[0], *q[1], *q[2])
            elif verb == "Z":
                p.close()
        if c[-1][0] != "Z":
            p.close()
    return p


def circle(cx, cy, r):
    k = 0.5522847498 * r
    p = pathops.Path()
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.close()
    return p


def op(a, b, kind):
    r = pathops.op(a, b, kind)
    r.convertConicsToQuads()
    return r


def stroked(p, width):
    s = pathops.Path(p)
    s.stroke(width, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4.0)
    s.convertConicsToQuads()
    return s


def outset(p, w):
    return op(p, stroked(p, 2 * w), pathops.PathOp.UNION)


def inset(p, w):
    return op(p, stroked(p, 2 * w), pathops.PathOp.DIFFERENCE)


def segments(p):
    """pathops Path -> list of contours [(verb, [pts])] with only M/L/C/Z (quads and conics raised to cubics)."""
    p = pathops.Path(p)
    p.convertConicsToQuads()
    V = pathops.PathVerb
    out, cur, last = [], None, None
    for verb, pts in p:
        if verb == V.MOVE:
            cur = [("M", [pts[0]])]
            out.append(cur)
        elif verb == V.LINE:
            cur.append(("L", [pts[0]]))
        elif verb == V.CUBIC:
            cur.append(("C", list(pts)))
        elif verb == V.QUAD:
            (q1, q2), q0 = pts, last
            c1 = (q0[0] + 2 / 3 * (q1[0] - q0[0]), q0[1] + 2 / 3 * (q1[1] - q0[1]))
            c2 = (q2[0] + 2 / 3 * (q1[0] - q2[0]), q2[1] + 2 / 3 * (q1[1] - q2[1]))
            cur.append(("C", [c1, c2, q2]))
        elif verb == V.CLOSE:
            cur.append(("Z", []))
            continue
        else:
            raise ValueError(verb)
        last = pts[-1]
    return out


def _split_qcurve(start, pts):
    """TrueType style qCurveTo (implied on-curve points) -> list of (p0, ctrl, p1)."""
    offs, end = list(pts[:-1]), pts[-1]
    res, p0 = [], start
    for i, c in enumerate(offs):
        p1 = end if i == len(offs) - 1 else ((c[0] + offs[i + 1][0]) / 2, (c[1] + offs[i + 1][1]) / 2)
        res.append((p0, c, p1))
        p0 = p1
    return res


def bounds(p):
    return p.bounds  # (xmin, ymin, xmax, ymax)


# ---------------------------------------------------------------- logo and URL

def load_beeldmerk():
    svg = open(os.path.join(ROOT, "svg", "atom", "py-atom-logo-beeldmerk-color.svg"), encoding="utf8").read()
    paths = re.findall(r'<path d="([^"]+)" fill="(#[0-9A-Fa-f]{6})"', svg)
    (ring_d, ring_fill), (dot_d, dot_fill) = paths
    assert ring_fill.upper() == "#1A3580" and dot_fill.upper() == "#32B9CD", "library beeldmerk colours changed"
    ring = parse_svg_path(ring_d)
    # ring_d = inner circle contour + outer silhouette contour; the silhouette is the contour that starts at (18, 0)
    sil = [c for c in ring if abs(c[0][1][0][1]) < 1e-6]
    hole = [c for c in ring if c not in sil]
    return sil, hole, parse_svg_path(dot_d)


def glyph_path(font, text, pt, centre, rho_mid, rho_base, ang_mid_deg):
    """Outlined text on the lower arc of a circle, read left to right, letter tops towards the centre (screen mm, y down)."""
    upm = font["head"].unitsPerEm
    k = pt / MM / upm * 1.0  # font units -> mm  (pt -> mm: pt / MM)
    cmap, hmtx, gs = font.getBestCmap(), font["hmtx"], font.getGlyphSet()
    names = [cmap[ord(ch)] for ch in text]
    adv = [hmtx[n][0] * k for n in names]
    track = URL_TRACK * pt / MM
    total = sum(adv) + track * (len(adv) - 1)
    phi0 = math.radians(ang_mid_deg) + total / 2 / rho_mid  # reading direction = decreasing phi (clockwise angle, y down)
    cx, cy = centre
    out = pathops.Path()
    cursor = 0.0
    for n, a in zip(names, adv):
        phi = phi0 - (cursor + a / 2) / rho_mid
        u = (math.sin(phi), -math.cos(phi))      # baseline direction
        up = (-math.cos(phi), -math.sin(phi))    # glyph up = towards the centre
        bx, by = cx + rho_base * math.cos(phi), cy + rho_base * math.sin(phi)

        def xf(gx, gy, bx=bx, by=by, u=u, up=up, a=a):
            x = gx * k - a / 2
            y = gy * k
            return (bx + x * u[0] + y * up[0], by + x * u[1] + y * up[1])

        pen = _XfPen(out, xf)
        gs[n].draw(pen)
        cursor += a + track
    return pathops.simplify(out, fix_winding=True), math.degrees(total / rho_mid)


class _XfPen:
    """fontTools pen that writes transformed outlines into a pathops Path."""

    def __init__(self, path, xf):
        self.p, self.xf, self.cur = path, xf, None

    def moveTo(self, pt):
        self.p.moveTo(*self.xf(*pt))
        self.cur = pt

    def lineTo(self, pt):
        self.p.lineTo(*self.xf(*pt))
        self.cur = pt

    def curveTo(self, *pts):
        q = [self.xf(*pt) for pt in pts]
        self.p.cubicTo(*q[0], *q[1], *q[2])
        self.cur = pts[-1]

    def qCurveTo(self, *pts):
        if pts[-1] is None:  # closed contour of off-curve points only (does not occur in Ubuntu)
            raise ValueError("unsupported implied contour")
        for p0, c, p1 in _split_qcurve(self.cur, pts):
            self.p.quadTo(*self.xf(*c), *self.xf(*p1))
        self.cur = pts[-1]

    def closePath(self):
        self.p.close()

    endPath = closePath

    def addComponent(self, *a):
        raise ValueError("composite glyph")


# ---------------------------------------------------------------- build

def build(size):
    tokens = json.load(open(os.path.join(ROOT, "tokens.json"), encoding="utf8"))["colors"]
    blauw = [v / 100 for v in tokens["py-tok-color-blauw"]["cmyk"]]   # 100/83/0/17
    aqua = [v / 100 for v in tokens["py-tok-color-aqua"]["cmyk"]]     # 69/0/21/0

    sil_c, hole_c, dot_c = load_beeldmerk()
    def cut_for(scale):
        sil_c2 = to_pathops(sil_c, lambda x, y: (x * scale, y * scale))
        return inset(outset(sil_c2, BORDER + FILLET), FILLET)   # offset with a rounded inner corner

    # largest beeldmerk (rounded down to 0.5 mm width) whose cut contour bounding box fits the Aroman area
    lo, hi = 0.5, 3.0
    for _ in range(40):
        mid = (lo + hi) / 2
        b = bounds(cut_for(mid))
        if (b[2] - b[0]) * (b[3] - b[1]) <= SIZES[size]:
            lo = mid
        else:
            hi = mid
    width = math.floor(36.0 * lo * 2) / 2
    scale = width / 36.0
    cut = cut_for(scale)
    bx0, by0, bx1, by1 = bounds(cut)
    W, H = bx1 - bx0 + 2 * BLEED, by1 - by0 + 2 * BLEED
    ox, oy = BLEED - bx0, BLEED - by0     # shift so the page starts at the bleed edge

    def place(x, y):
        return (x * scale + ox, y * scale + oy)

    sil = to_pathops(sil_c, place)
    inner = to_pathops(hole_c, place)
    dot = to_pathops(dot_c, place)
    cut = cut.transform(1, 0, 0, 1, ox, oy)
    centre = place(18, 18)
    r_out, r_in = 18 * scale, 10.8 * scale
    hole = circle(centre[0], place(18, 0)[1], HOLE_D / 2)

    ring = op(sil, inner, pathops.PathOp.DIFFERENCE)

    # URL, knocked out of the ring on the front
    font = TTFont(os.path.join(ROOT, "fonts", "Ubuntu-Medium.ttf"))
    upm = font["head"].unitsPerEm
    xh = font["OS/2"].sxHeight / upm * URL_PT / MM
    rho_mid = (r_out + r_in) / 2
    rho_base = rho_mid + xh / 2
    url, arc_deg = glyph_path(font, URL, URL_PT, centre, rho_mid, rho_base, URL_ANGLE)
    ring_front = op(ring, url, pathops.PathOp.DIFFERENCE)

    # back: the die-cut piece seen from behind = mirror image of the front around the page centre
    def mirrored(p):
        return pathops.simplify(p.transform(-1, 0, 0, 1, W, 0), fix_winding=True)

    pages = [
        ("Voorkant", ring_front, dot, cut, hole),
        ("Achterkant", mirrored(ring), mirrored(dot), mirrored(cut), mirrored(hole)),
    ]

    os.makedirs(OUT, exist_ok=True)
    pdf_path = os.path.join(OUT, f"parkingyou-geurhanger-{size}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=(W * MM, H * MM), pageCompression=1)
    c.setTitle(f"ParkingYou geurhanger {size} ({(bx1 - bx0) / 10:.2f} x {(by1 - by0) / 10:.2f} cm) - drukbestand Aroman")
    c.setAuthor("ParkingYou")
    c.setSubject("Voorkant en achterkant, CMYK, snijlijn als steunkleur CutContour")
    cutcol = CMYKColorSep(0, 1, 0, 0, spotName="CutContour", density=1)
    for name, ring_p, dot_p, cut_p, hole_p in pages:
        trim = (BLEED * MM, BLEED * MM, (W - BLEED) * MM, (H - BLEED) * MM)
        c.setTrimBox(trim)
        c.setBleedBox((0, 0, W * MM, H * MM))
        draw(c, ring_p, H, fill=CMYKColor(*blauw))
        draw(c, dot_p, H, fill=CMYKColor(*aqua))
        c.saveState()
        c.setStrokeOverprint(True)
        c.setOverprintMask(True)
        draw(c, cut_p, H, stroke=cutcol)
        draw(c, hole_p, H, stroke=cutcol)
        c.restoreState()
        c.showPage()
    c.save()
    strip_unused_font(pdf_path)

    info = {
        "size": size,
        "page_mm": [round(W, 2), round(H, 2)],
        "cut_bbox_mm": [round(bx1 - bx0, 2), round(by1 - by0, 2)],
        "cut_bbox_cm2": round((bx1 - bx0) * (by1 - by0) / 100, 2),
        "cut_area_cm2": round(abs(cut.area) / 100, 2),
        "beeldmerk_mm": [width, round(43.423 * scale, 2)],
        "ring_mm": round(r_out - r_in, 2),
        "url_pt": URL_PT,
        "url_arc_deg": round(arc_deg, 1),
        "url_xheight_mm": round(xh, 2),
        "pdf": os.path.relpath(pdf_path, ROOT),
    }
    return info


def strip_unused_font(pdf_path):
    """reportlab always lists Helvetica (not embedded) in the page resources; all text here is outlined, so drop it
    to keep preflight free of 'font not embedded' warnings."""
    import pymupdf
    doc = pymupdf.open(pdf_path)
    for page in doc:
        assert not page.get_text().strip(), "live text found, expected outlines only"
        doc.xref_set_key(page.xref, "Resources/Font", "null")
    tmp = pdf_path + ".tmp"
    doc.save(tmp, garbage=4, deflate=True)
    doc.close()
    os.replace(tmp, pdf_path)


def draw(c, p, H, fill=None, stroke=None):
    path = c.beginPath()
    for contour in segments(p):
        for verb, pts in contour:
            q = [(x * MM, (H - y) * MM) for x, y in pts]
            if verb == "M":
                path.moveTo(*q[0])
            elif verb == "L":
                path.lineTo(*q[0])
            elif verb == "C":
                path.curveTo(*q[0], *q[1], *q[2])
            elif verb == "Z":
                path.close()
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(0.25)
        c.setLineJoin(1)
    c.drawPath(path, fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0, fillMode=1)


def preview(info):
    """Front and back side by side on a light grey sheet, 300 dpi (RGB approximation of the CMYK file)."""
    import fitz
    from PIL import Image, ImageDraw, ImageFont

    doc = fitz.open(os.path.join(ROOT, info["pdf"]))
    imgs = []
    for page in doc:
        pix = page.get_pixmap(dpi=300, alpha=False)
        imgs.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    w, h = imgs[0].size
    pad, top = 120, 220
    sheet = Image.new("RGB", (2 * w + 3 * pad, h + top + pad + 160), (238, 240, 243))
    d = ImageDraw.Draw(sheet)
    fb = ImageFont.truetype(os.path.join(ROOT, "fonts", "Ubuntu-Bold.ttf"), 64)
    fr = ImageFont.truetype(os.path.join(ROOT, "fonts", "Ubuntu-Regular.ttf"), 38)
    for i, (img, label) in enumerate(zip(imgs, ["Voorkant", "Achterkant"])):
        x = pad + i * (w + pad)
        sheet.paste(img, (x, top))
        d.text((x, 90), label, fill=(26, 53, 128), font=fb)
    cw, ch = info["cut_bbox_mm"]
    d.text((pad, top + h + 40),
           f"Formaat {cw / 10:.2f} x {ch / 10:.2f} cm = {info['cut_bbox_cm2']:.1f} cm²  ·  CMYK PY-Blauw 100/83/0/17, PY-Aqua 69/0/21/0",
           fill=(60, 60, 60), font=fr)
    d.text((pad, top + h + 95), "Magenta lijn = snijlijn en ophanggat (steunkleur CutContour, drukt niet)",
           fill=(60, 60, 60), font=fr)
    out = os.path.join(OUT, f"parkingyou-geurhanger-{info['size']}-preview.png")
    sheet.save(out, optimize=True)
    return os.path.relpath(out, ROOT)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", choices=sorted(SIZES), default="standaard")
    ap.add_argument("--no-preview", action="store_true")
    a = ap.parse_args()
    info = build(a.size)
    if not a.no_preview:
        info["preview"] = preview(info)
    print(json.dumps(info, indent=1, ensure_ascii=False))
