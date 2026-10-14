"""4.1 Autoroutebord (p27), 4.2 Voetgangersroutebord (p28), 4.3 technische gegevens (p29).

All route boards are 200 mm high. The p27 and p28 drawings are 1:1.0 of the stated board sizes, so
mm_per_pt is derived from the board width measured in points (1000 mm board on p27/p28, 600 mm board on p27).
The p29 side view has its own scale, derived from the stated 200 mm board height.
"""
from pyassets import Path, affine, rect_item
from pyassets.filters import callout_dot
from pyassets.registry import crop, element

NAVY = "#1A3580"
ANNOT_LINE = "#1D1D1B"  # dimension lines, callouts and the die-cut outline are drawn in this colour

# ---------------------------------------------------------------- p27 geometry (PDF points)
B600 = (158.7, 253.4, 413.9, 338.5)  # navy pill, 600 mm
B1000 = (158.7, 394.4, 583.9, 479.5)  # navy pill, 1000 mm
BBACK = (158.7, 567.2, 583.9, 652.3)  # navy pill, back side
H27 = B1000[3] - B1000[1]  # 200 mm = one module square
MM27_1000 = 1000.0 / (B1000[2] - B1000[0])
MM27_600 = 600.0 / (B600[2] - B600[0])
MM27_H = 200.0 / H27

# ---------------------------------------------------------------- p28 geometry
V_FRONT = (158.7, 273.1, 583.9, 358.2)
V_BACK = (158.7, 445.9, 583.9, 530.9)
MM28 = 1000.0 / (V_FRONT[2] - V_FRONT[0])

# ---------------------------------------------------------------- p29 side view
SIDE = (1026.1, 305.5, 1063.0, 589.0)  # outer aluminium panels, 200 mm high
MM29 = 200.0 / (SIDE[3] - SIDE[1])


def pad(b, d=0.8):
    return (b[0] - d, b[1] - d, b[2] + d, b[3] + d)


def no_annot(p):
    """Strip dimension/callout furniture on p27: every #1D1D1B stroke (dimension lines, die-cut) and callout dots."""
    return p.stroke == ANNOT_LINE or callout_dot(p)


def no_annot_p28(p):
    """p28 keeps the thin #1D1D1B board outline (white board) but drops the die-cut line and dimension lines."""
    if callout_dot(p):
        return True
    if p.stroke == ANNOT_LINE:
        if p.dashes:
            return True
        w = p.box[2] - p.box[0]
        h = p.box[3] - p.box[1]
        return not (w > 400 and h > 80)  # keep only the full board outline
    return False


def slot(x0, x1, y0, y1, end=None):
    """Rebuilt navy module backdrop: a square slot, optionally with a semicircular end (pill cap)."""
    if end is None:
        return rect_item(x0, y0, x1, y1, fill=NAVY, tag="rebuilt-backdrop")
    r = (y1 - y0) / 2
    k = 0.5522847498 * r
    ym = (y0 + y1) / 2
    segs = [("M", x0, y0), ("L", x1 - r, y0),
            ("C", x1 - r + k, y0, x1, ym - k, x1, ym),
            ("C", x1, ym + k, x1 - r + k, y1, x1 - r, y1),
            ("L", x0, y1), ("Z",)]
    return Path(segs, fill=NAVY, box=(x0, y0, x1, y1), tag="rebuilt-backdrop")


# ================================================================ products p27
@element("py-prod-routebord-auto-600-front", "4.1 Autoroutebord 600", "prod", "routebord", 27,
         variables=("pictos", "label", "arrow"), built_from=("py-comp-route-panel-pill", "py-comp-route-module-picto",
                                                               "py-comp-route-module-text", "py-comp-route-module-arrow"))
def _(src):
    items = crop(src, 27, pad(B600), skip=no_annot, texts=False)
    return items, {"mm_per_pt": MM27_600, "true_scale": True, "dims_mm": (600, 200),
                   "notes": "Scale from the stated 600 mm board width. Die-cut outline, dimension lines and callout dot stripped. 'in' is outlined in the source."}


@element("py-prod-routebord-auto-1000-front", "4.1 Autoroutebord 1000", "prod", "routebord", 27,
         variables=("pictos", "label", "arrow"), built_from=("py-comp-route-panel-pill", "py-comp-route-module-picto",
                                                               "py-comp-route-module-text", "py-comp-route-module-arrow"))
def _(src):
    items = crop(src, 27, pad(B1000), skip=no_annot, texts=False)
    return items, {"mm_per_pt": MM27_1000, "true_scale": True, "dims_mm": (1000, 200),
                   "notes": "Scale from the stated 1000 mm board width. Five modules: car, in, accessible, EV, arrow."}


def _back(src):
    return crop(src, 27, pad(BBACK), skip=no_annot, texts=False)


@element("py-prod-routebord-auto-back", "4.1 Autoroutebord achterzijde", "prod", "routebord", 27,
         built_from=("py-comp-route-back-noentry",))
def _(src):
    return _back(src), {"mm_per_pt": MM27_1000, "true_scale": True, "dims_mm": (1000, 200),
                        "notes": "Back side of the 1000 mm board: red no-entry sign on navy pill. Same scale as the front."}


# ================================================================ products p28
@element("py-prod-routebord-voet-front", "4.2 Voetgangersroutebord voorzijde", "prod", "routebord", 28,
         variables=("exit names", "pictos", "arrow directions"),
         built_from=("py-comp-route-panel-pill", "py-comp-walk-route-figure-block", "py-comp-walk-route-row"))
def _(src):
    items = crop(src, 28, pad(V_FRONT), skip=no_annot_p28)
    return items, {"mm_per_pt": MM28, "true_scale": True, "dims_mm": (1000, 200),
                   "notes": "Scale from the stated 1000 mm board width. Live Ubuntu text. The thin board outline is kept so the white board stays visible; die-cut dashes and dimension lines are removed."}


@element("py-prod-routebord-voet-back", "4.2 Voetgangersroutebord achterzijde", "prod", "routebord", 28,
         variables=("exit names", "pictos", "arrow directions"),
         built_from=("py-comp-route-panel-pill", "py-comp-walk-route-figure-block", "py-comp-walk-route-row"))
def _(src):
    # The source back face carries a stray grey rectangle and a white pill shifted by 0.6 pt that pokes out of its clip.
    # Both are replaced by the white pill of the front face moved down onto the back face (same source geometry).
    white = [p for p in src.paths(28, pad(V_FRONT)) if p.fill == "#FFFFFF" and (p.box[2] - p.box[0]) > 400]
    under = affine(white, 1, 1, 0, V_BACK[1] - V_FRONT[1])
    items = crop(src, 28, pad(V_BACK), skip=lambda p: no_annot_p28(p) or (p.fill in ("#AEAEAE", "#FFFFFF") and (p.box[2] - p.box[0]) > 400),
                 under=under)
    return items, {"mm_per_pt": MM28, "true_scale": True, "dims_mm": (1000, 200),
                   "status": "rebuilt",
                   "notes": "Mirrored back side: figure and arrows point left. Same scale as the front. The back face white pill is the source white pill of the front face moved down (the source back face has a stray grey rectangle and a shifted white pill); everything else is extracted."}


# ================================================================ product p29
@element("py-prod-routebord-spec", "4.3 Routeborden technische gegevens (zijaanzicht)", "prod", "routebord", 29)
def _(src):
    def skip(p):
        if p.stroke == ANNOT_LINE or callout_dot(p):
            return True
        # hatch frame between the two ceiling blocks (ceiling blocks themselves are outside the crop)
        return p.stroke is not None and p.box[1] < 150 and p.box[3] < 190 and (p.box[2] - p.box[0]) > 12

    items = crop(src, 29, (1025.0, 146.0, 1064.5, 590.5), skip=skip, texts=False)
    return items, {"mm_per_pt": MM29, "true_scale": True, "dims_mm": (None, 200),
                   "notes": ("Side view only: two aluminium sandwich panels with the wooden core between them (set back 10 mm top and bottom, "
                             "10/180/10 mm) and the hanging wire with screw eyes. Scale from the stated 200 mm board height. "
                             "The layered 3D render and the radius 100 detail are raster or annotation and are left out, as are "
                             "the ceiling blocks, dimension lines, labels and callouts.")}


# ================================================================ components
@element("py-comp-route-panel-pill", "routebord paneel", "comp", "routebord", (27, 28, 29), variables=("width", "fill"),
         built_from=("py-atom-shape-pill-solid",))
def _(src):
    items = crop(src, 27, pad(B1000), skip=lambda p: p.fill != NAVY, texts=False)
    return items, {"mm_per_pt": MM27_1000, "true_scale": True, "dims_mm": (1000, 200),
                   "notes": "Navy pill panel, 200 mm high, shown at 1000 mm wide. 600 and 800 mm panels use the same ends with a shorter straight; the white pedestrian panel is the same shape filled white. Radius 100 mm."}


@element("py-comp-route-module-picto", "route module pictogram", "comp", "routebord", 27, variables=("picto",),
         built_from=("py-atom-picto-accessible", "py-atom-shape-separator-arc"))
def _(src):
    x0, x1 = B1000[0] + 2 * H27, B1000[0] + 3 * H27  # third module of the 1000 board (accessible picto)
    items = crop(src, 27, (x0, B1000[1] - 0.5, x1, B1000[3] + 0.5), skip=no_annot, texts=False,
                 under=[slot(x0, x1, B1000[1], B1000[3])])
    return items, {"mm_per_pt": MM27_1000, "true_scale": True, "dims_mm": (200, 200), "status": "rebuilt",
                   "notes": "200 x 200 mm module slot: aqua separator arc on the left edge plus one white picto (accessible shown). Picto and arc are source paths; the navy slot square is rebuilt."}


@element("py-comp-route-module-separator", "route module scheiding", "comp", "routebord", (27, 29),
         built_from=("py-atom-shape-separator-arc",))
def _(src):
    items = crop(src, 27, (330.0, 400.0, 346.5, 473.8), skip=no_annot, texts=False)
    return items, {"mm_per_pt": MM27_1000, "true_scale": True,
                   "notes": "Aqua separator arc between two modules, taken from the 1000 mm board. Stroke only, to be placed on navy."}


@element("py-comp-route-module-text", "route module tekst", "comp", "routebord", 27, variables=("label text",))
def _(src):
    x0, x1 = B600[0] + H27, B600[0] + 2 * H27  # second module of the 600 board ("in")
    items = crop(src, 27, (x0, B600[1] - 0.5, x1, B600[3] + 0.5), skip=no_annot, texts=False,
                 under=[slot(x0, x1, B600[1], B600[3])])
    return items, {"mm_per_pt": MM27_600, "true_scale": True, "dims_mm": (200, 200), "status": "rebuilt",
                   "notes": "200 x 200 mm text module with separator arc and the label 'in'. The label is outlined in the source (no live text), so it is kept as paths. The navy slot square is rebuilt."}


@element("py-comp-route-module-arrow", "route module pijl", "comp", "routebord", 27, variables=("direction",),
         built_from=("py-atom-arrow-up-circle",))
def _(src):
    x0 = B600[0] + 2 * H27
    items = crop(src, 27, (x0, B600[1] - 0.5, B600[2] + 0.5, B600[3] + 0.5), skip=no_annot, texts=False,
                 under=[slot(x0, B600[2], B600[1], B600[3], end="right")])
    return items, {"mm_per_pt": MM27_600, "true_scale": True, "dims_mm": (200, 200), "status": "rebuilt",
                   "notes": "End module of the panel: aqua arrow in a white circle on the navy pill end (radius 100 mm). Circle and arrow are source paths; the navy end cap is rebuilt."}


@element("py-comp-route-back-noentry", "achterzijde routebord", "comp", "routebord", 27,
         built_from=("py-comp-route-panel-pill", "py-atom-rvv-c02"))
def _(src):
    return _back(src), {"mm_per_pt": MM27_1000, "true_scale": True, "dims_mm": (1000, 200),
                        "notes": "Red no-entry sign (RVV C02 look) centred on the navy pill."}


@element("py-comp-walk-route-figure-block", "voetgangersfiguur blok", "comp", "routebord", 28, variables=("direction",),
         built_from=("py-atom-picto-pedestrian", "py-atom-shape-separator-arc"))
def _(src):
    items = crop(src, 28, (183.0, 281.0, 236.5, 347.0), skip=no_annot_p28, texts=False)
    return items, {"mm_per_pt": MM28, "true_scale": True,
                   "notes": "Navy pedestrian figure with the aqua arc, facing right (front side). The back side mirrors it."}


@element("py-comp-walk-route-row", "voetgangersroute regel", "comp", "routebord", 28,
         variables=("exit name", "pictos", "arrow direction"),
         built_from=("py-atom-picto-lift", "py-atom-picto-escalator", "py-atom-picto-stairs", "py-atom-picto-payment-machine",
                     "py-atom-arrow-up-plain"))
def _(src):
    items = crop(src, 28, (238.5, 287.0, 563.5, 316.5), skip=no_annot_p28)
    return items, {"mm_per_pt": MM28, "true_scale": True,
                   "notes": "One row: picto strip (lift, escalator, stairs, payment), live Ubuntu 'Uitgang Naam', up arrow, and the aqua rule below the row. A board carries two rows."}


# ================================================================ atoms
@element("py-atom-arrow-up-circle", "pijl omhoog in witte cirkel", "atom", "arrow", 27, variables=("direction", "colour"))
def _(src):
    items = crop(src, 27, (B600[0] + 2 * H27 + 5.5, B600[1] + 5.5, B600[2] - 5.5, B600[3] - 5.5), skip=no_annot, texts=False)
    return items, {"mm_per_pt": MM27_600, "true_scale": True,
                   "notes": "Aqua arrow in a white circle (white on transparent: view on a dark background)."}


@element("py-atom-arrow-up-plain", "pijl omhoog", "atom", "arrow", 28, variables=("colour",))
def _(src):
    items = crop(src, 28, (541.0, 287.5, 563.5, 310.0), skip=no_annot_p28, texts=False)
    return items, {"mm_per_pt": MM28, "true_scale": True}


@element("py-atom-arrow-left-plain", "pijl links", "atom", "arrow", 28, variables=("colour",))
def _(src):
    items = crop(src, 28, (179.5, 460.0, 202.0, 483.0), skip=no_annot_p28, texts=False)
    return items, {"mm_per_pt": MM28, "true_scale": True}
