"""4.4 to 4.9 Signing in de parkeergarage (p30 to p35): niveauaanduiding, sectieaanduiding, overzichtsbord,
rijstvlies borden, pijlplaat, buispaal, vluchtwegplattegrond plus their atoms and components.

Scale notes (all measured from the handbook drawings, see the dimension lines on each page):
* p30, p32, p33, p34 and p35 are drawn at 1:5, so 1 pt = 1.7639 mm. The bubble is 350 mm wide, the boards are 400 mm wide.
* p31 strip: 300 mm high = 115.78 pt.
* p32 houten frame plan: 400 mm board outline = 166.3 pt.
* buispaal: 1000 mm pole = 345.1 pt (the O48 diameter measures 16.6 pt = 48 mm, consistent).
"""
import copy

from pyassets import Gradient, Path, Text, gradient_shape, affine, items_box
from pyassets.filters import any_of, callout_dot, stroke_only
from pyassets.registry import crop as _crop0, element

TP = ("third-party",)


def crop(src, pno, bbox, skip=None, **kw):
    """registry.crop that always drops callout dots (dimension and callout furniture)."""
    if skip is None:
        return _crop0(src, pno, bbox, skip=callout_dot, **kw)
    return _crop0(src, pno, bbox, skip=lambda p: callout_dot(p) or skip(p), **kw)


# ---------------------------------------------------------------- helpers
def _order(items):
    """Paint order by source sequence; live text stays on top (as crop() does)."""
    texts = [i for i in items if isinstance(i, Text)]
    rest = [i for i in items if not isinstance(i, Text)]
    rest.sort(key=lambda p: getattr(p, "seq", 1e9))
    return rest + texts


def _shape(src, pno, bbox, which=0, min_size=6.0, min_segs=0):
    """Clip outline (exact shape of an InDesign gradient fill) as a Path."""
    cs = [c for c in src.clips(pno, bbox, min_size=min_size) if len(c.segs) >= min_segs]
    return _tight(cs[which])


def _tight(p):
    """The clip scissor box can be larger than the outline itself; use the real extent of the path."""
    xs, ys = [], []
    cur = None
    for sg in p.segs:
        if sg[0] in ("M", "L"):
            cur = (sg[1], sg[2])
            xs.append(cur[0]); ys.append(cur[1])
        elif sg[0] == "C" and cur:
            for i in range(1, 21):
                t = i / 20.0
                a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
                xs.append(a * cur[0] + b * sg[1] + c * sg[3] + d * sg[5])
                ys.append(a * cur[1] + b * sg[2] + c * sg[4] + d * sg[6])
            cur = (sg[5], sg[6])
    q = copy.copy(p)
    q.box = (min(xs), min(ys), max(xs), max(ys))
    return q


def _grad(src, pno, bbox, **kw):
    return gradient_shape(src, pno, _shape(src, pno, bbox, **kw))


def _w(shape):
    return shape.box[2] - shape.box[0]


def _h(shape):
    return shape.box[3] - shape.box[1]


def _extra(scale, dims=None, notes="", status="rebuilt", **kw):
    d = dict(status=status, mm_per_pt=scale, true_scale=True, notes=notes)
    if dims:
        d["dims_mm"] = dims
    d.update(kw)
    return d


GRAD_NOTE = ("Gradient face rebuilt: outline is the clip path of the source shading, the blauw to aqua verloop is "
             "re-measured and written as a real SVG gradient. ")


# ---------------------------------------------------------------- p30 niveauaanduiding
B30 = (150, 190, 366, 445)


def _bubble30(src):
    shape = _shape(src, 30, (150, 190, 366, 445), min_segs=6)
    digit = src.texts(30, (200, 190, 330, 400))  # live Ubuntu Bold digit
    return [gradient_shape(src, 30, shape)] + digit, 350.0 / _w(shape)


@element("py-atom-tag-level-bubble-gradient", "Niveauaanduiding bel", "atom", "tag", 30, variables=("level digit",),
         built_from=("py-atom-shape-bubble-gradient",))
def _(src):
    items, sc = _bubble30(src)
    return items, _extra(sc, notes=GRAD_NOTE + "Digit is live Ubuntu Bold text. Bubble is 350 mm wide at 1:5.")


@element("py-prod-niveauaanduiding", "4.4 Niveauaanduiding", "prod", "signage", 30, variables=("level digit",),
         built_from=("py-atom-tag-level-bubble-gradient",))
def _(src):
    items, sc = _bubble30(src)
    return items, _extra(sc, dims=(350, 420), notes=GRAD_NOTE + "Front view of the 420 x 350 sandwich panel (example digit 0). "
                         "Side section, wall, drop shadows, 3D render and dimension lines left out.")


# ---------------------------------------------------------------- p31 sectieaanduiding
S31 = 300.0 / 115.78  # 300 mm strip height measured in points
T31 = {
    "bubble": (285, 242, 342, 310),
    "circle": (322, 242, 418, 338),
    "tag": (285, 241, 418, 338),
}


@element("py-atom-tag-level-bubble-small", "Niveau bel klein", "atom", "tag", 31, variables=("level digit",),
         built_from=("py-atom-shape-bubble-solid",))
def _(src):
    return crop(src, 31, T31["bubble"]), _extra(S31, status="extracted", notes="White bubble with navy digit (live Ubuntu Bold). Drawn on the gradient strip, so it is white-on-transparent here.")


@element("py-atom-tag-section-circle", "Sectie cirkel", "atom", "tag", 31, variables=("section letter",),
         built_from=("py-atom-shape-circle",))
def _(src):
    return crop(src, 31, T31["circle"]), _extra(S31, status="extracted", notes="White circle with aqua letter (live Ubuntu Bold).")


@element("py-atom-tag-section-1a", "Sectieaanduiding 1A", "atom", "tag", 31, variables=("level digit", "section letter"),
         built_from=("py-atom-tag-level-bubble-small", "py-atom-tag-section-circle"))
def _(src):
    return crop(src, 31, T31["tag"]), _extra(S31, status="extracted", notes="Level bubble plus section circle, live Ubuntu Bold digit and letter. White artwork, meant for the gradient strip.")


def _strip31(src):
    shape = _shape(src, 31, (150, 225, 932, 349))
    sc = 300.0 / _h(shape)
    items = crop(src, 31, (150, 225, 932, 349), skip=callout_dot) + [gradient_shape(src, 31, shape)]
    return _order(items), sc, round(_w(shape) * sc)


@element("py-comp-section-wrap-strip", "Kolomband sectie", "comp", "signage", 31, variables=("level", "section", "repeats", "width"),
         built_from=("py-atom-tag-section-1a", "py-tok-gradient-verloop-vertical"))
def _(src):
    items, sc, wmm = _strip31(src)
    return items, _extra(sc, dims=(wmm, 300), notes="Vertical gradient strip rebuilt from the clip path of the source shading, three '1A' tags as drawn (live text). Width is variable (depends on column diameter), the drawn example is about %d mm." % wmm)


@element("py-prod-sectieaanduiding-kolomband", "4.5 Sectieaanduiding", "prod", "signage", 31, variables=("level", "section", "width"),
         built_from=("py-comp-section-wrap-strip",))
def _(src):
    items, sc, wmm = _strip31(src)
    return items, _extra(sc, dims=(wmm, 300), notes="300 mm high wall foil strip glued on columns; width variable, drawn example about %d mm. Column mock-ups, dimension lines and callout left out. " % wmm + GRAD_NOTE)


# ---------------------------------------------------------------- p32 overzichtsbord
def _s32(src):
    shape = _shape(src, 32, (150, 150, 392, 475))
    return shape, 400.0 / _w(shape)


@element("py-prod-overzichtsbord", "4.6 Overzichtsbord", "prod", "signage", 32, variables=("levels", "icons per level"),
         built_from=("py-comp-overview-level-header", "py-comp-overview-level-row-filled", "py-comp-overview-level-row-outlined"))
def _(src):
    shape, sc = _s32(src)
    items = crop(src, 32, (150, 150, 388, 475), skip=callout_dot) + [gradient_shape(src, 32, shape)]
    return _order(items), _extra(sc, dims=(400, 550), notes=GRAD_NOTE + "400 x 550 plus 90 per extra level. Two level rows (1 and 0) as drawn; row digits are outlined glyphs in the source (not live text). Houten frame, 3D render and dimension lines left out.")


@element("py-comp-overview-level-header", "Overzichtsbord niveaukop", "comp", "signage", 32, variables=("level digit",),
         built_from=("py-atom-tag-level-bubble-white",))
def _(src):
    return crop(src, 32, (200, 180, 345, 348)), _extra(400.0 / 226.77, status="extracted", notes="White bubble with aqua digit (live Ubuntu Bold). White artwork, meant for the gradient face; scale 1:5.")


@element("py-atom-tag-level-bubble-white", "Niveau bel wit", "atom", "tag", 32, variables=("level digit",),
         built_from=("py-atom-shape-bubble-solid",))
def _(src):
    return crop(src, 32, (200, 180, 345, 348)), _extra(400.0 / 226.77, status="extracted", notes="Big white bubble with aqua digit (live Ubuntu Bold) from the overzichtsbord. Scale 1:5.")


@element("py-comp-overview-level-row-filled", "Niveaurij gevuld", "comp", "signage", 32, variables=("level", "icons"),
         built_from=("py-atom-shape-pill-solid", "py-atom-tag-level-circle-white"))
def _(src):
    return crop(src, 32, (168, 366, 376, 409)), _extra(400.0 / 226.77, status="extracted", notes="Navy pill, white level circle, white icons (rolltrap, lift, betaalautomaat). The level digit is an outlined glyph in the source. Scale 1:5.")


@element("py-comp-overview-level-row-outlined", "Niveaurij wit", "comp", "signage", 32, variables=("level", "icons"),
         built_from=("py-atom-shape-pill-solid", "py-atom-tag-level-circle-navy"))
def _(src):
    return crop(src, 32, (168, 417, 376, 460)), _extra(400.0 / 226.77, status="extracted", notes="White pill, navy level circle, aqua icons. The level digit is an outlined glyph in the source. Scale 1:5.")


@element("py-atom-tag-level-circle-navy", "Niveau cirkel navy", "atom", "tag", 32, variables=("level digit",),
         built_from=("py-atom-shape-circle",))
def _(src):
    return crop(src, 32, (171, 420, 209, 457)), _extra(400.0 / 226.77, status="extracted", notes="Navy circle with white digit (row on white pill). The digit is an outlined glyph in the source. Scale 1:5.")


@element("py-atom-tag-level-circle-white", "Niveau cirkel wit", "atom", "tag", 32, variables=("level digit",),
         built_from=("py-atom-shape-circle",))
def _(src):
    return crop(src, 32, (171, 369, 209, 406)), _extra(400.0 / 226.77, status="extracted", notes="White circle with digit (row on navy pill). The source digit is aqua (#32B9CD), not navy, and an outlined glyph. White circle is invisible on a white page. Scale 1:5.")


# ---------------------------------------------------------------- houten frame (p32)
@element("py-prod-overzichtsbord-frame", "Houten frame overzichtsbord", "prod", "signage", 32)
def _(src):
    plan = crop(src, 32, (157, 513, 327, 744), texts=False, skip=any_of(stroke_only, callout_dot))
    detail = crop(src, 32, (548, 513, 779, 744), texts=False, skip=any_of(stroke_only, callout_dot))
    pb = items_box(plan)
    db = items_box(detail)
    detail = affine(detail, 1, 1, (pb[2] + 40) - db[0], 0)
    sc = 400.0 / (pb[2] - pb[0])
    return plan + detail, _extra(sc, dims=(400, 550), status="extracted",
                                 notes="Left: plan of the wooden frame (multiplex 20 mm, 50 mm strips, 10 mm inset) in front of the 400 x 550 board, at 1:5 of the board scale given here. "
                                       "Right: corner detail, drawn in the handbook at about 5.1 times the plan scale and moved next to the plan; it is NOT at the stated scale. Dimension lines and break lines left out.")


# ---------------------------------------------------------------- p33/p34 rijstvlies borden
def _s33(src, pno):
    shape = _shape(src, pno, (150, 185, 392, 535))
    return shape, 400.0 / _w(shape)


def _board(src, pno):
    shape, sc = _s33(src, pno)
    items = crop(src, pno, (150, 185, 392, 535), skip=callout_dot) + [gradient_shape(src, pno, shape)]
    return _order(items), sc


@element("py-prod-bord-mindervaliden", "4.7 Mindervaliden parkeerplek aanduiding", "prod", "signage", 33, variables=("caption",),
         built_from=("py-comp-bord-picto-bubble-face",))
def _(src):
    items, sc = _board(src, 33)
    return items, _extra(sc, dims=(400, 600), notes=GRAD_NOTE + "Rijstvlies board 400 x 600 with white bubble, wheelchair pictogram and live Ubuntu Bold caption. Pole mock-up, callouts and dimension lines left out.")


@element("py-prod-bord-ev", "4.8 EV-laad parkeerplek aanduiding", "prod", "signage", 34, variables=("caption",),
         built_from=("py-comp-bord-picto-bubble-face",))
def _(src):
    items, sc = _board(src, 34)
    return items, _extra(sc, dims=(400, 600), notes=GRAD_NOTE + "Rijstvlies board 400 x 600 with white bubble, EV pictogram and live caption 'Oplaadpunt'. Pole mock-up, callouts and dimension lines left out.")


@element("py-comp-bord-picto-bubble-face", "Rijstvlies bord voorzijde", "comp", "signage", (33, 34), variables=("picto", "caption"),
         built_from=("py-atom-shape-bubble-solid",))
def _(src):
    items, sc = _board(src, 33)
    return items, _extra(sc, notes=GRAD_NOTE + "Face with the p33 pictogram (accessible) and caption; the p34 variant swaps the pictogram (EV) and caption. Scale 1:5.")


def _plate(src, pno):
    items = crop(src, pno, (150, 535, 392, 653), skip=lambda p: (p.stroke == "#FFFFFF" and p.fill is None) or callout_dot(p))
    for p in items:  # the white face carries a 2.8 pt white stroke that overshoots the plate edge (invisible on white)
        if isinstance(p, Path) and p.fill == "#FFFFFF" and p.stroke == "#FFFFFF":
            p.stroke = None
    shape = _shape(src, pno, (150, 535, 392, 653))
    return items, 400.0 / _w(shape)


@element("py-prod-bord-pijlplaat", "Pijlplaat", "prod", "signage", (33, 34), built_from=("py-comp-bord-arrow-plate",))
def _(src):
    items, sc = _plate(src, 33)
    return items, _extra(sc, dims=(400, 200), status="extracted", notes="400 x 200 plate with two black diagonal arrows, white face and grey 2 pt edge as drawn. Same on p33 and p34.")


@element("py-comp-bord-arrow-plate", "Pijlplaat", "comp", "signage", (33, 34), built_from=("py-atom-arrow-diagonal-pair-black",))
def _(src):
    items, sc = _plate(src, 33)
    return items, _extra(sc, status="extracted", notes="White plate (white face, grey edge) with the black arrow pair. Scale 1:5.")


@element("py-atom-arrow-diagonal-pair-black", "Zwarte diagonale pijlen", "atom", "arrow", (33, 34))
def _(src):
    items = crop(src, 33, (180, 553, 365, 636), skip=callout_dot)
    return items, _extra(400.0 / 226.77, status="extracted", notes="Pair of heavy black arrows (down-left and down-right), source colour #0D0E10. Scale 1:5 of the plate.")


# ---------------------------------------------------------------- buispaal (p33, same on p34)
POLE_STOPS = [(0.0, "#3B3B3A"), (0.25, "#787878"), (0.5, "#A9A9A9"), (0.75, "#D6D6D6"), (1.0, "#FFFFFF")]


@element("py-prod-buispaal", "Optionele buispaal", "prod", "signage", (33, 34))
def _(src):
    bb = (760, 185, 905, 570)
    items = crop(src, 33, bb, texts=False, skip=callout_dot)
    pole = src.clips(33, bb, min_size=2.0)
    shapes = {}
    for c in pole:
        key = (round(c.box[0]), round(c.box[1]), round(c.box[2]), round(c.box[3]))
        if key == (825, 219, 842, 564):
            shapes["pole"] = c
        elif key == (808, 216, 859, 219):
            shapes["plate"] = c
    extra = []
    for name in ("pole", "plate"):
        c = shapes[name]
        g = copy.copy(c)
        g.fill = Gradient(c.box[0], 0, c.box[2], 0, POLE_STOPS)
        g.tag = "rebuilt-gradient"
        extra.append(g)
    # board top view above the foot plate: #878787 at 50 percent group opacity in the source, clipped to the plate width
    top = Path(segs=[("M", 766.8, 189.9), ("L", 900.3, 189.9), ("L", 900.3, 211.8), ("L", 766.8, 211.8), ("Z",)],
               fill="#878787", fill_opacity=0.5, box=(766.8, 189.9, 900.3, 211.8), tag="rebuilt")
    top.seq = 129
    extra.append(top)
    pole_len = shapes["pole"].box[3] - shapes["pole"].box[1]
    sc = 1000.0 / pole_len
    return _order(items + extra), _extra(sc, dims=(48, 1000), notes="Side view of the optional buispaal (1000 mm long, O48, round foot plate, RAL 9006) with the board seen edge-on on top. "
                                         "Cylinder shading rebuilt as vector grey gradients (source shading plus raster soft shadow), the soft shadow is left out. "
                                         "Scale from the pole length 1000 mm; the board strip on top is not at that scale reference. Callout left out.")


# ---------------------------------------------------------------- p35 vluchtwegplattegrond
EXIT_BOX_LEGEND = (523.64, 280.0, 540.30, 287.75)
EXIT_BOX_PLAN = (389.80, 381.38, 402.17, 387.13)

# pictogram of the raster exit sign, in crop units of a 60x render (origin 523.2, 279.6), green field 26..1027 x 24..490
_X0, _X1, _Y0, _Y1 = 26.4, 1027.0, 24.0, 490.0


def _exit_symbol(box):
    """Vector rebuild of the green 'uitgang' sign (door with arrow), which is a 47 x 22 px raster in the source."""
    x0, y0, x1, y1 = box

    def P(cx, cy):
        return (x0 + (cx - _X0) / (_X1 - _X0) * (x1 - x0), y0 + (cy - _Y0) / (_Y1 - _Y0) * (y1 - y0))

    def poly(pts, fill):
        segs = []
        for i, (cx, cy) in enumerate(pts):
            x, y = P(cx, cy)
            segs.append(("M" if i == 0 else "L", x, y))
        segs.append(("Z",))
        xs = [s[1] for s in segs if len(s) > 1]
        ys = [s[2] for s in segs if len(s) > 1]
        pth = Path(segs=segs, fill=fill, box=(min(xs), min(ys), max(xs), max(ys)), tag="rebuilt")
        pth.seq = 1e7
        return pth

    field = poly([(_X0, _Y0), (_X1, _Y0), (_X1, _Y1), (_X0, _Y1)], "#00913E")
    frame = poly([(410, 66), (644, 66), (644, 88), (665, 88), (665, 362), (580, 362), (580, 321), (623, 321), (623, 108),
                  (431, 108), (431, 321), (473, 321), (473, 362), (388, 362), (388, 88), (410, 88)], "#FFFFFF")
    stem = poly([(516, 194), (537, 194), (537, 384), (516, 384)], "#FFFFFF")
    head = poly([(473, 384), (580, 384), (526.5, 468)], "#FFFFFF")
    return [field, frame, stem, head]


def _fix(items):
    """The blue frame of the beheerder sign is a rect plus an inner polygon that the PDF fills as a ring; mark it even-odd."""
    for p in items:
        if isinstance(p, Path) and p.fill == "#005A8F" and len(p.segs) > 6:
            p.evenodd = True
    return items


UITGANG_NOTE = "The source sign is a 47 x 22 px raster; rebuilt as a vector (green field, door outline, arrow down), shape traced from the raster."


@element("py-atom-escape-exit", "Uitgang", "atom", "picto", 35, tags=TP)
def _(src):
    return _exit_symbol(EXIT_BOX_LEGEND), dict(status="rebuilt", notes="Standard safety symbol (third party). " + UITGANG_NOTE)


@element("py-atom-escape-emergency-exit", "Nooduitgang", "atom", "picto", 35, tags=TP)
def _(src):
    return crop(src, 35, (522.5, 290.5, 541.5, 300), texts=False), dict(notes="Standard safety symbol (third party).")


@element("py-atom-escape-first-aid", "EHBO middelen", "atom", "picto", 35, tags=TP)
def _(src):
    return crop(src, 35, (522.5, 303, 533.5, 313.6), texts=False), dict(notes="Standard safety symbol (third party).")


@element("py-atom-escape-route", "Vluchtroute", "atom", "picto", 35, tags=TP)
def _(src):
    return crop(src, 35, (522.5, 316.5, 543, 324.5), texts=False), dict(notes="Standard safety symbol (third party). Light green band is #AED6B7 as drawn.")


@element("py-atom-escape-door-release", "Noodontgrendeling deur", "atom", "picto", 35, tags=TP)
def _(src):
    return crop(src, 35, (522.5, 327.5, 533.5, 338), texts=False), dict(notes="Standard safety symbol (third party).")


@element("py-atom-escape-extinguisher", "Brandblusser", "atom", "picto", 35, tags=TP)
def _(src):
    return crop(src, 35, (522.5, 339.5, 533.5, 350), texts=False), dict(notes="Standard safety symbol (third party).")


@element("py-atom-escape-manager", "Beheerder", "atom", "picto", 35, tags=TP)
def _(src):
    return _fix(crop(src, 35, (522.5, 352.5, 533.5, 362.5), texts=False)), dict(notes="Standard information symbol (third party).")


@element("py-atom-escape-lift-no-use", "Bij brand lift niet gebruiken", "atom", "picto", 35, tags=TP)
def _(src):
    return crop(src, 35, (522.5, 365, 534, 376.5), texts=False), dict(notes="Standard prohibition symbol (third party).")


LEG = (520, 268, 606, 379)
SAF = (520, 395, 616, 518)


@element("py-comp-escape-legend", "Legenda vluchtweg", "comp", "signage", 35, variables=("which symbols",),
         built_from=("py-atom-escape-exit", "py-atom-escape-emergency-exit", "py-atom-escape-first-aid", "py-atom-escape-route",
                     "py-atom-escape-door-release", "py-atom-escape-extinguisher", "py-atom-escape-manager", "py-atom-escape-lift-no-use"))
def _(src):
    items = _order(_fix(crop(src, 35, LEG)) + _exit_symbol(EXIT_BOX_LEGEND))
    return items, dict(status="rebuilt", tags=TP, notes="Title LEGENDA, eight third-party safety symbols and labels (labels partly outlined glyphs, partly live text in the source). White text, meant for the gradient panel. " + UITGANG_NOTE)


@element("py-comp-escape-safety-instructions", "Veiligheidsinstructies", "comp", "signage", 35, variables=("text",))
def _(src):
    return crop(src, 35, SAF), dict(status="extracted", notes="Safety text block (ongeval/letsel, bij ontruiming, bij brand). Mixed outlined glyphs and live Ubuntu Bold in the source. White text, meant for the gradient panel.")


@element("py-prod-vluchtwegplattegrond", "4.9 Vluchtwegplattegrond", "prod", "signage", 35, variables=("floor plan", "symbols"),
         built_from=("py-comp-escape-legend", "py-comp-escape-safety-instructions", "py-atom-logo-horizontal-color"))
def _(src):
    bb = (157, 207, 622, 533)
    shape = _shape(src, 35, bb, min_segs=6)
    items = _fix(crop(src, 35, bb, skip=lambda p: (p.stroke == "#FFFFFF" and p.fill is None and p.width < 0.3) or callout_dot(p)))
    items += [gradient_shape(src, 35, shape)] + _exit_symbol(EXIT_BOX_LEGEND) + _exit_symbol(EXIT_BOX_PLAN)
    return _order(items), dict(status="rebuilt", tags=(), notes=GRAD_NOTE + "No dimension in the handbook, default scale. The floor plan inside the white area is a location-specific placeholder, kept as drawn. "
                               "The two 'uitgang' signs (legend and plan) are rebuilt as vectors because they are rasters in the source. The pink annotation and the callout are left out.")
