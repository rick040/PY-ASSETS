"""Maashaven pyloon (Maashaven.pdf, 400 x 1000 mm panel, 3 mm bleed): third-party badge marks, badge containers, the print
components, the print product variant and the application (reference plus template).

Coordinates in this module are PAGE mm (origin top left of the MediaBox, 406 x 1006); the trim corner sits at (3, 3).
Components are tight Docs in page mm; the panel composer converts to trim relative mm (page minus 3).
"""
from functools import lru_cache

from pyassets import printsrc
from pyassets.apps import application
from pyassets.compose import Doc
from pyassets.core import (GRADIENT_STOPS, PT_MM, Defs, Path, TF, Text, _from_pathops, _to_pathops, fit_gradient, fmt,
                           items_box, make_text)
from pyassets.registry import crop, element

KEY = "maashaven"
TRIM_OFF = 3.0  # trim corner inside the page (mm)
BLUE = "#1A3580"
BLACK = "#1D1D1B"
WHITE = "#FFFFFF"
QR_URL = "https://parkingyou.nl/nl/locaties/rotterdam/parking-maashaven/id=129"
TERMS_URL = "www.parkingyou.nl/algemene-voorwaarden"
THIRD = "Third party reference only: source the official file, do not redraw."

box = printsrc.box_mm


def _src():
    return printsrc.source(KEY)


# ------------------------------------------------------------------------------------------------ helpers
def emit(d, items, dx=0.0, dy=0.0, gid=None):
    """Write extracted source Paths (points) into a Doc. (dx, dy) = page mm that maps to the Doc origin."""
    tf = TF(0.0, 0.0, PT_MM, d.ox - dx, d.oy - dy)
    for p in items:
        if not isinstance(p, Path):
            continue
        fill = p.fill if isinstance(p.fill, str) else None
        stroke = p.stroke if isinstance(p.stroke, str) else None
        a = f'd="{p.d(tf)}" fill="{fill or "none"}"'
        if fill and p.evenodd:
            a += ' fill-rule="evenodd"'
        if fill and p.fill_opacity < 0.999:
            a += f' fill-opacity="{fmt(p.fill_opacity)}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{fmt(p.width * PT_MM)}"'
            if p.cap == 1:
                a += ' stroke-linecap="round"'
            elif p.cap == 2:
                a += ' stroke-linecap="square"'
            if p.join == 1:
                a += ' stroke-linejoin="round"'
            elif p.join == 2:
                a += ' stroke-linejoin="bevel"'
        if gid:
            a += f' id="{gid}"'
        b = p.bbox
        bx_ = (b[0] * PT_MM - dx + d.ox, b[1] * PT_MM - dy + d.oy, b[2] * PT_MM - dx + d.ox, b[3] * PT_MM - dy + d.oy)
        d._emit(f"<path {a}/>", bx_)


def origin(doc):
    """Top left of a tight Doc in its own (page mm) coordinates."""
    return (min(b[0] for b in doc.boxes), min(b[1] for b in doc.boxes))


def place_var(d, ref_id, x, y, rename=None, **kw):
    """place() a library comp and rename its data-variable names (so five bars do not all carry `title`)."""
    n = len(d._stack[-1])
    r = d.place(ref_id, x, y, **kw)
    frag = d._stack[-1][n]
    for old, new in (rename or {}).items():
        frag = frag.replace(f'data-variable="{old}"', f'data-variable="{new}"')
    d._stack[-1][n] = frag
    return r


def _items_origin_mm(bbox_mm, **kw):
    its = crop(_src(), 1, box(*bbox_mm), **kw)
    b = items_box(its)
    return b[0] * PT_MM, b[1] * PT_MM


# ------------------------------------------------------------------------------------------------ third-party marks (white mark only)
MARKS = {
    # id: (name_nl, category, bbox mm of the white mark (excludes the navy badge), crop kwargs)
    "py-atom-payment-maestro-badge": ("Maestro (witte badgeversie)", "payment", (17, 566, 48, 589), {}),
    "py-atom-payment-mastercard-badge": ("Mastercard (witte badgeversie)", "payment", (62, 567, 91, 588), {}),
    "py-atom-payment-visa": ("VISA", "payment", (104, 571, 136, 585), {}),
    "py-atom-payment-vpay": ("V PAY", "payment", (155, 563, 176, 592), {}),
    "py-atom-partner-easypark": ("EasyPark", "partner", (217, 565, 239, 591), {}),
    "py-atom-partner-parkbee": ("ParkBee", "partner", (254, 572, 289, 583), {}),
    "py-atom-partner-myway": ("MyWay", "partner", (301, 566, 330, 589), {}),
    "py-atom-partner-mobian": ("Mobian", "partner", (344, 562, 374, 594), {"outline_fonts": ("ArialMT",)}),
}
MARK_NOTES = {
    "py-atom-partner-easypark": "The e mark in the partner row is EasyPark (confirmed by the owner). ",
    "py-atom-partner-mobian": "The word MOBIAN is live ArialMT in the source and is outlined here. ",
    "py-atom-payment-maestro-badge": "Older wordmark version, differs from the library colour mark py-atom-payment-maestro. ",
    "py-atom-payment-mastercard-badge": "Older wordmark version, differs from the library colour mark py-atom-payment-mastercard. ",
}


def _reg_mark(eid, name, cat, bb, kw):
    @element(eid, name, "atom", cat, 1, src=KEY, variables=("colour",), tags=("third-party",), status="extracted",
             notes=MARK_NOTES.get(eid, "") + "White mark only, without the navy badge, taken from the Maashaven print. " + THIRD +
                   " White on transparent: view on a dark background.")
    def _(src):
        return crop(src, 1, box(*bb), texts=False, **kw)


for _eid, (_n, _c, _bb, _kw) in MARKS.items():
    _reg_mark(_eid, _n, _c, _bb, _kw)


# ------------------------------------------------------------------------------------------------ badge containers
@element("py-atom-badge-round-navy", "Ronde badge navy", "atom", "badge", 1, src=KEY, variables=("colour",), status="extracted",
         notes="Container only: 36 mm disc in navy (the Maashaven print draws the payment badges in the token blue 100/83/0/17). "
               "The mark goes on top (see py-comp-pyloon-payment-row-badges).")
def _(src):
    return crop(src, 1, box(14, 559, 51, 596), texts=False, skip=lambda p: p.fill != BLUE)[:1]


@element("py-atom-badge-square-navy", "Vierkante badge navy", "atom", "badge", 1, src=KEY, variables=("colour",), status="extracted",
         notes="Container only: 36 mm square with corner radius 7.94 mm (22 percent), navy. The mark goes on top.")
def _(src):
    return crop(src, 1, box(209, 559, 246.5, 596), texts=False, skip=lambda p: p.fill != BLUE)[:1]


# badge positions in page mm (top left of each 36 mm badge)
ROUND_X = (14.4, 58.6, 102.8, 147.3)
ROUND_IDS = ("py-atom-payment-maestro-badge", "py-atom-payment-mastercard-badge", "py-atom-payment-visa", "py-atom-payment-vpay")
SQUARE_X = (209.7, 253.6, 297.4, 341.3)
SQUARE_IDS = ("py-atom-partner-easypark", "py-atom-partner-parkbee", "py-atom-partner-myway", "py-atom-partner-mobian")
BADGE_Y = 559.4
BADGE_Y_SQ = 559.5
DIVIDER_X = 196.495
DIVIDER_Y = (564.922, 593.288)
