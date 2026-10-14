"""3.2 / 3.3 Portalen (p15, p16, p18, p19): beeldplaat front elevations, parts and RVV signs.

Product = the front elevation of the plate (frame outline, P block, name, display, RVV tab). The extradisplay
product is the second drawing on each page. The top view, side view (posts, hoogtebalk, car), dimension
lines, callouts and 'TOEGEPASTE KLEUR' boxes are left out.

Scale: every plate is 600 mm high (frame height, the '600mm' dimension on each page, drawn from y 175.2 to
234.49 pt = 59.29 pt). That gives about 10.12 mm per point for the large drawings. The extra display drawings
of the 2-baans pages are drawn smaller (49.2 pt high for the same 600 mm), so they get their own scale.
"""
import copy
import math

from pyassets import Path, gradient_shape, rect_item
from pyassets.core import Text
from pyassets.registry import crop, element

FONTS = ("RWSTTDdx",)
DIM_600_PT = 234.49 - 175.2  # the 600 mm bracket on the pages
MM_PT = 600.0 / DIM_600_PT  # about 10.12 mm per point
TOP_H = 59.528  # white plate rect height of the large (top) drawings

# plate rectangles (white rect incl. outline) per page: top drawing, extra display drawing
PLATE = {
    15: {"top": (123.73, 174.95, 451.13, 234.47), "extra": (124.7, 343.8, 452.1, 403.3), "w_mm": 3300},
    16: {"top": (123.73, 174.95, 778.5, 234.47), "extra": (124.7, 307.7, 665.6, 356.9), "w_mm": 6600},
    18: {"top": (123.73, 174.95, 451.13, 234.47), "extra": (124.7, 337.6, 452.1, 397.2), "w_mm": 3300},
    19: {"top": (123.73, 174.95, 778.5, 234.47), "extra": (124.7, 307.7, 665.6, 356.9), "w_mm": 6600},
}

NAVY, AQUA = "#1A3580", "#32B9CD"


def scale_of(pno, kind):
    b = PLATE[pno][kind]
    return MM_PT * TOP_H / (b[3] - b[1])


def inside(b, box, tol=0.8):
    return b[0] >= box[0] - tol and b[1] >= box[1] - tol and b[2] <= box[2] + tol and b[3] <= box[3] + tol


# ------------------------------------------------------------------ annotation filters
def _dot(p):
    """Round callout bullet (3 x 3 pt, PY-zwart)."""
    w, h = p.box[2] - p.box[0], p.box[3] - p.box[1]
    return p.fill == "#1D1D1B" and p.stroke is None and 2.6 < w < 3.4 and abs(w - h) < 0.2


def _hairline(p):
    """Black 0.035 pt outline strokes that InDesign repeats on every white frame rectangle (no visible effect)."""
    return p.fill is None and p.stroke == "#1D1D1B" and p.width < 0.05 and (p.box[2] - p.box[0]) > 20


def skip_notes(p):
    return _dot(p) or _hairline(p)


# ------------------------------------------------------------------ rebuilt shapes (gradients and circle edges)
def _arc_segs(cx, cy, r, a0, a1):
    """Circle arc from angle a0 to a1 (radians, y down) as cubic segments."""
    n = max(1, int(math.ceil(abs(a1 - a0) / (math.pi / 4))))
    segs = []
    for i in range(n):
        s, e = a0 + (a1 - a0) * i / n, a0 + (a1 - a0) * (i + 1) / n
        k = 4 / 3 * math.tan((e - s) / 4)
        segs.append(("C",
                     cx + r * (math.cos(s) - k * math.sin(s)), cy + r * (math.sin(s) + k * math.cos(s)),
                     cx + r * (math.cos(e) + k * math.sin(e)), cy + r * (math.sin(e) - k * math.cos(e)),
                     cx + r * math.cos(e), cy + r * math.sin(e)))
    return segs


def circle_edge(d):
    """The source paints a big circle under a rectangular clip: the visible shape is the clip rectangle with one
    circular edge on the right. Returns (segs, xt, xb, box) with the shape as plain path segments."""
    r = d["rect"]
    sc = d["scissor"]
    cx, cy, rad = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, (r.x1 - r.x0) / 2
    x0, y0, x1, y1 = sc
    xt = cx + math.sqrt(rad * rad - (y0 - cy) ** 2)
    xb = cx + math.sqrt(rad * rad - (y1 - cy) ** 2)
    a0, a1 = math.atan2(y0 - cy, xt - cx), math.atan2(y1 - cy, xb - cx)
    segs = [("M", x0, y0), ("L", xt, y0)] + _arc_segs(cx, cy, rad, a0, a1) + [("L", x0, y1), ("Z",)]
    return segs, xt, xb, (x0, y0, max(xt, xb), y1)


def rebuilt(src, pno, box):
    """Gradient arcs (real PDF shadings) and circle-edge fills inside `box`, each carrying its paint order."""
    out = []
    # blauw to aqua shading shape: the dark band at the right edge of the P block
    for c in src.clips(pno, box):
        if len(c.segs) > 5 and (c.box[2] - c.box[0]) < 80 and (c.box[3] - c.box[1]) > 40:
            g = gradient_shape(src, pno, c)
            g.seq = c.seq
            g.clipped = False
            g.role = "pgrad"
            out.append(g)
    for d in src.drawings(pno):
        if d["type"] != "f" or not d.get("clipped") or "scissor" not in d:
            continue
        sc = d["scissor"]
        if not inside(tuple(sc), box, 1.5):
            continue
        r = d["rect"]
        if (r.x1 - r.x0) < 100 or abs((r.x1 - r.x0) - (r.y1 - r.y0)) > 1:
            continue
        col = tuple(round(v * 255) for v in d["fill"][:3])
        fill = {(26, 54, 128): NAVY, (50, 185, 205): AQUA}.get(col)
        if fill is None:
            continue
        segs, xt, xb, bx = circle_edge(d)
        p = Path(segs, fill=fill, box=bx, tag="rebuilt-circle-edge")
        p.seq = d["seq"]
        p.clipped = False
        p.role = "navy-edge" if fill == NAVY else "aqua-block"
        p.xt, p.xb = xt, xb
        out.append(p)
    return out


def take(src, pno, region, extra=(), skip=None, texts=True, outline=True, rb=None):
    """Extracted paths and text inside region plus rebuilt shapes that lie inside it, in source paint order."""
    sk = skip_notes if skip is None else (lambda p: skip_notes(p) or skip(p))
    items = crop(src, pno, region, skip=sk, texts=texts, outline_fonts=FONTS if outline else ())
    paths = [i for i in items if isinstance(i, Path)]
    txt = [i for i in items if not isinstance(i, Path)]
    rb = rebuilt(src, pno, region) if rb is None else rb
    mine = [s for s in rb if inside(s.box, region, 1.5)]
    paths += mine + list(extra)
    paths.sort(key=lambda p: getattr(p, "seq", 1e9))
    return paths + txt


def white_tab(src, pno, box):
    """White RVV tab: the part of the plate right of the navy circle edge (rebuilt, the source only shows it as
    the white plate rectangle left uncovered by the navy)."""
    nav = [s for s in rebuilt(src, pno, box) if getattr(s, "role", "") == "navy-edge"][0]
    x0, y0, x1, y1 = box
    # arc reversed: from the bottom point back up to the top point
    sg = nav.segs  # M, L, arc segments, L, Z
    arc = sg[2:-3]
    rev = []
    # walk the cubic segments backwards
    starts = [(nav.xt, y0)] + [(s[5], s[6]) for s in arc[:-1]]
    for st, s in reversed(list(zip(starts, arc))):
        rev.append(("C", s[3], s[4], s[1], s[2], st[0], st[1]))
    segs = [("M", nav.xt, y0), ("L", x1, y0), ("L", x1, y1), ("L", nav.xb, y1)] + rev + [("Z",)]
    tab = Path(segs, fill="#FFFFFF", box=(min(nav.xt, nav.xb), y0, x1, y1), tag="rebuilt-tab")
    tab.seq = 0
    tab.clipped = False
    d = 0.125
    edge = Path([("M", min(nav.xt, nav.xb) - 0.0, y0 + d), ("L", x1 - d, y0 + d), ("L", x1 - d, y1 - d),
                 ("L", nav.xb, y1 - d)], fill=None, stroke="#AEAEAE", width=0.25,
                box=(nav.xt, y0 + d, x1 - d, y1 - d), tag="rebuilt-tab")
    edge.seq = 0.1
    edge.clipped = False
    return [tab, edge]


def info(pno, kind, notes):
    s = scale_of(pno, kind)
    box = PLATE[pno][kind]
    return {
        "status": "rebuilt",
        "mm_per_pt": s,
        "true_scale": True,
        "dims_mm": (round((box[2] - box[0]) * s), 600),
        "notes": notes,
    }


NOTE_PLATE = ("Front elevation of the plate, extracted from the source paths with live Ubuntu text and RVV numerals as "
              "outlines. Rebuilt parts: the blauw to aqua band at the P block edge (measured real vector gradient from the "
              "clip of the source shading) and the P block and navy right edges (clip rectangle with circular edge, "
              "the source paints them as a circle under a clip). Scale from the 600 mm frame height of the drawing; ")


def _plate_product(pno, kind):
    def fn(src):
        box = PLATE[pno][kind]
        items = take(src, pno, box)
        s = scale_of(pno, kind)
        txt = (NOTE_PLATE + "the handbook states a width of %d mm in the illustration, measured %d mm."
               % (PLATE[pno]["w_mm"], round((box[2] - box[0]) * s)))
        e = info(pno, kind, txt)
        e["dims_mm"] = ((PLATE[pno]["w_mm"] if kind == "top" else round((box[2] - box[0]) * s)), 600, 200)
        return items, e
    return fn


PRODUCTS = [
    ("py-prod-portaal-1baans-luxe", "3.2.1 Portaal 1-baans luxe", 15, "top", ("py-comp-portal-face-1baans",)),
    ("py-prod-portaal-1baans-luxe-extradisplay", "3.2.1 Portaal 1-baans luxe met extra display", 15, "extra",
     ("py-comp-portal-face-1baans", "py-comp-portal-display-slot-dual")),
    ("py-prod-portaal-2baans-luxe", "3.2.2 Portaal 2-baans luxe", 16, "top", ("py-comp-portal-face-2baans",)),
    ("py-prod-portaal-2baans-luxe-extradisplay", "3.2.2 Portaal 2-baans luxe met extra display", 16, "extra",
     ("py-comp-portal-face-2baans", "py-comp-portal-display-slot-dual")),
    ("py-prod-portaal-1baans-standaard", "3.3.1 Portaal 1-baans standaard", 18, "top", ("py-comp-portal-face-1baans",)),
    ("py-prod-portaal-1baans-standaard-extradisplay", "3.3.1 Portaal 1-baans standaard met extra display", 18, "extra",
     ("py-comp-portal-face-1baans", "py-comp-portal-display-slot-dual")),
    ("py-prod-portaal-2baans-standaard", "3.3.2 Portaal 2-baans standaard", 19, "top", ("py-comp-portal-face-2baans",)),
    ("py-prod-portaal-2baans-standaard-extradisplay", "3.3.2 Portaal 2-baans standaard met extra display", 19, "extra",
     ("py-comp-portal-face-2baans", "py-comp-portal-display-slot-dual")),
]
for _id, _name, _p, _k, _bf in PRODUCTS:
    element(_id, _name, "prod", "portaal", _p,
            variables=("location name", "width", "max height", "speed", "post height"), built_from=_bf)(_plate_product(_p, _k))


# ------------------------------------------------------------------ components (all taken from page 15, scale of that page)
P15 = PLATE[15]["top"]
S15 = scale_of(15, "top")
SCALE = {"mm_per_pt": S15, "true_scale": True}

PBLOCK = (123.7, 174.9, 185.5, 234.5)
DISPLAY = (351.9, 184.3, 388.6, 201.2)
NAMEBOX = (186.0, 186.0, 383.5, 232.0)
SIGNS = (399.0, 181.0, 447.5, 228.5)
EXTRA = PLATE[15]["extra"]


@element("py-comp-portal-p-block", "portaal P blok links", "comp", "portaal", (15, 16, 18, 19, 37),
         built_from=("py-atom-symbol-p-roof",))
def _(src):
    items = take(src, 15, PBLOCK, texts=False)
    return items, dict(SCALE, status="rebuilt", dims_mm=(round((PBLOCK[2] - PBLOCK[0]) * S15), 600),
                       notes="Aqua block with circular right edge and the blauw to aqua edge band are rebuilt (measured real vector gradient, "
                             "clip shapes from the source); the P with roof is extracted. Same artwork on all four portal pages.")


def _not_display(p):
    return inside(p.box, DISPLAY, 0.5)


@element("py-comp-portal-name-block", "portaal naamblok", "comp", "portaal", (15, 16),
         variables=("location name",), built_from=("py-atom-logo-horizontal-white",))
def _(src):
    items = take(src, 15, NAMEBOX, skip=_not_display)
    return items, dict(SCALE, status="extracted", notes="White parkingyou logo (pin hole in navy, dot in aqua as drawn) and the "
                       "location name as live Ubuntu Bold, white, no background. The plate behind it is navy RAL 5002.")


@element("py-comp-portal-display-slot", "portaal displayvak", "comp", "portaal", (15, 16),
         variables=("state",), built_from=("py-atom-display-volvrij-vrij",))
def _(src):
    items = take(src, 15, DISPLAY, texts=False)
    return items, dict(SCALE, status="extracted", notes="VOL/VRIJ display, 200x400 mm with 170x370 mm view area: bezel and "
                       "all LED dots as drawn (state shown: VRIJ).")


@element("py-comp-portal-display-slot-dual", "portaal displayvak dubbel", "comp", "portaal", (15, 16, 18, 19),
         variables=("labels", "states"), built_from=("py-atom-display-volvrij-vrij",))
def _(src):
    # the two displays and their labels from the extra display drawing: region between the labels row and the LEDs
    reg = (292.0, 349.5, 381.5, 376.5)
    items = take(src, 15, reg, outline=False)
    return items, dict(SCALE, status="extracted", notes="Two displays with live Ubuntu Bold labels Bezoekers and Vergunninghouders.")


@element("py-comp-rvv-cluster-portal", "RVV icon cluster portaal", "comp", "portaal", (15, 16, 18, 19),
         variables=("speed", "height", "signs"),
         built_from=("py-atom-rvv-a01", "py-atom-rvv-c07", "py-atom-rvv-max-height", "py-atom-sign-ev-allowed-green"))
def _(src):
    tab = white_tab(src, 15, P15)
    items = take(src, 15, SIGNS, extra=tab)
    return items, dict(SCALE, status="rebuilt", notes="Four signs (max speed 5, no trailers, max height 2,4 m, EV allowed) as extracted "
                       "paths with RVV numerals as outlines. The white tab with its curved edge is rebuilt from the plate geometry; "
                       "its outline is the thin grey line of the plate.")


@element("py-comp-portal-face-1baans", "portaal beeldplaat 1-baans", "comp", "portaal", (15, 18),
         variables=("location name", "width", "extra display"),
         built_from=("py-comp-portal-p-block", "py-comp-portal-name-block", "py-comp-portal-display-slot", "py-comp-rvv-cluster-portal"))
def _(src):
    items = take(src, 15, P15)
    return items, dict(info(15, "top", NOTE_PLATE + "luxe artwork of page 15; page 18 differs only by the navy aluminium profile edge."),
                       dims_mm=(3300, 600))


@element("py-comp-portal-face-2baans", "portaal beeldplaat 2-baans", "comp", "portaal", (16, 19),
         variables=("location name", "width"),
         built_from=("py-comp-portal-p-block", "py-comp-portal-name-block", "py-comp-portal-display-slot", "py-comp-rvv-cluster-portal"))
def _(src):
    box = PLATE[16]["top"]
    items = take(src, 16, box)
    return items, dict(info(16, "top", NOTE_PLATE + "luxe artwork of page 16 (name centred, display and 2x2 RVV on the right)."),
                       dims_mm=(6600, 600))


# ------------------------------------------------------------------ atoms (signs of the cluster, page 15)
MAXH = (401.4, 206.6, 421.4, 226.6)
EVG = (425.3, 206.6, 445.3, 226.6)


@element("py-atom-rvv-max-height", "maximale doorrijhoogte bord", "atom", "rvv", (15, 16, 23), variables=("height value",))
def _(src):
    items = crop(src, 15, MAXH, skip=skip_notes, outline_fonts=FONTS)
    return items, dict(SCALE, status="extracted", notes="Sign C21 style with max height 2,4 m; numerals are RWSTTDdx glyphs converted to outlines. "
                       "Drawn at 200 mm diameter in the portal cluster.")


@element("py-atom-sign-ev-allowed-green", "groene cirkel auto met stekker", "atom", "rvv", (15, 16))
def _(src):
    items = crop(src, 15, EVG, skip=skip_notes, outline_fonts=FONTS)
    return items, dict(SCALE, status="extracted", notes="Green ring with car and plug (EV allowed), as drawn in the portal RVV cluster, 200 mm diameter.")
