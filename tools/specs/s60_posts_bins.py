"""7.1 to 7.2 aanrijdbeveiligingen (p43 to p45) and 8.1 to 8.2 vuilnisbakken (p47, p48).

Product elevations. The outline strokes, red bands (p43, p44), the bin artwork (p47, p48) and the
sticker are real vector paths in the source. The metal and plastic fills of the posts are raster
(shaded product renders under the CAD lines); they are rebuilt here as flat or horizontal vector
gradients that are measured from the rendered page (status rebuilt). Dimension lines, callouts,
leader dots and dimension text are left out; the foot plate plan drawings are left out.
"""
from pyassets import Gradient, Path, rect_item
from pyassets.filters import callout_dot
from pyassets.registry import crop, element

BLACK = "#1D1D1B"
RED = "#C20016"  # py-tok-color-reflective-red


# ------------------------------------------------------------------ helpers
def _rgb(c):
    return "#%02X%02X%02X" % tuple(int(round(max(0, min(255, v)))) for v in c)


def hgrad(src, pno, x0, x1, y0, y1, n=14, inset=1.0, tone=None):
    """Horizontal vector gradient measured from the rendered page between x0 and x1.

    Rows y0..y1 are averaged, n columns are sampled between x0+inset and x1-inset. tone gives
    a flat target colour for the brightest sample (shape of the shading is kept, so a red band
    keeps the reflective-red token but the dark left edge of the render)."""
    s = 8.0
    arr = src.render_array(pno, (x0, y0, x1, y1), s)
    row = arr.mean(axis=0)  # W x 3
    xs = [x0 + inset + (x1 - x0 - 2 * inset) * i / (n - 1) for i in range(n)]
    cols = [row[min(row.shape[0] - 1, max(0, int((x - x0) * s)))] for x in xs]
    if tone:
        t = [int(tone[i:i + 2], 16) for i in (1, 3, 5)]
        k = max(c[0] for c in cols)  # brightest red sample maps to the token
        cols = [[t[j] * (c[0] / k) for j in range(3)] for c in cols]
    stops = [(i / (n - 1), _rgb(c)) for i, c in enumerate(cols)]
    ym = (y0 + y1) / 2
    return Gradient(xs[0], ym, xs[-1], ym, stops)


def flat(src, pno, box):
    arr = src.render_array(pno, box, 8.0)
    return _rgb(arr.reshape(-1, 3).mean(axis=0))


def poly(pts, fill, tag="rebuilt"):
    segs = [("M", *pts[0])] + [("L", *p) for p in pts[1:]] + [("Z",)]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return Path(segs, fill=fill, box=(min(xs), min(ys), max(xs), max(ys)), tag=tag)


def rect(box, fill):
    return rect_item(*box, fill=fill, tag="rebuilt")


def not_band(p):
    """Source red bands (flat red over an orange shade) are replaced by measured gradient bands."""
    return p.fill in (RED, "#F08300")


# ------------------------------------------------------------------ p43 anti-rampaal
@element("py-prod-anti-rampaal", "7.1 RVS anti-rampaal", "prod", "post", 43)
def _(src):
    pno = 43
    L, R, T, J, B = 170.0, 191.1, 484.3, 612.7, 710.9
    body = hgrad(src, pno, L, R, 560, 600)
    tab = flat(src, pno, (166.6, 659, 169.6, 665))
    under = [
        rect((166.2, 658.0, 194.8, 665.6), tab),
        rect((L, T, R, B), body),
    ]
    bands = []
    for y0, y1 in ((491.0, 504.3), (510.9, 524.2)):
        bands.append(rect((169.7, y0, 190.8, y1), hgrad(src, pno, 169.7, 190.8, y0 + 2, y1 - 2, tone=RED)))
    # fix tab fills so the plate tabs sit under the body outline like in the source
    items = crop(src, pno, (160, 480, 200, 714), texts=False,
                 skip=lambda p: not_band(p) or (p.stroke is not None and p.box[0] > 195),
                 under=under + bands)
    return items, {
        "status": "rebuilt",
        "notes": ("Outline, joint line (ground level) and fixing tabs are extracted source strokes. The shaded "
                  "stainless fill is raster in the source and is rebuilt as a measured vector gradient; the two "
                  "red reflective bands are rebuilt as gradients on the #C20016 token. 850 mm above ground, "
                  "650 mm buried (joint line at 850). Photo render, dimension lines and callouts left out."),
        "mm_per_pt": 850.0 / (J - T), "true_scale": True, "dims_mm": (139.7, 1500, 139.7),
    }


# ------------------------------------------------------------------ p43 bolderpaal
@element("py-prod-bolderpaal", "RVS bolderpaal", "prod", "post", 43)
def _(src):
    pno = 43
    L, R, T, B = 686.5, 715.1, 526.8, 699.3
    body = hgrad(src, pno, L, R, 600, 680)
    plate = flat(src, pno, (680, 699.4, 720, 700.8))
    bolt = flat(src, pno, (681, 697.5, 683.5, 698.7))
    under = [rect((678.2, 699.3, 723.3, 700.9), plate), rect((L, T, R, B), body)]
    for x in (680.7, 699.1, 717.6):
        under.append(rect((x, 697.2, x + 3.2, 699.3), bolt))
    for y0, y1 in ((535.3, 553.3), (562.2, 580.3)):
        under.append(rect((686.8, y0, 715.4, y1), hgrad(src, pno, 686.8, 715.4, y0 + 2, y1 - 2, tone=RED)))
    items = crop(src, pno, (674, 524, 727, 704), texts=False, skip=not_band, under=under)
    return items, {
        "status": "rebuilt",
        "notes": ("Outline, foot plate and bolt heads are extracted source strokes. The shaded stainless fill is "
                  "raster in the source and is rebuilt as a measured vector gradient; the two red reflective bands "
                  "are rebuilt as gradients on the #C20016 token. Scale from the 850 mm dimension (top of tube to "
                  "underside of the plate); checks: tube 139.6 mm, plate 220 mm. Photo render, plan view of the foot "
                  "plate (O220), dimension lines and callouts left out."),
        "mm_per_pt": 850.0 / (700.9 - T), "true_scale": True, "dims_mm": (220, 850, 220),
    }


# ------------------------------------------------------------------ p44 PMS beschermpaal
@element("py-prod-pms-beschermpaal", "PMS beschermpaal", "prod", "post", 44)
def _(src):
    pno = 44
    L, R, T, B = 166.4, 195.6, 501.3, 709.1
    body = hgrad(src, pno, L, R, 580, 690)
    plate = flat(src, pno, (160, 709.3, 202, 710.6))
    under = [rect((157.9, 709.1, 204.1, 710.8), plate), rect((L, T, R, B), body)]
    for y0, y1 in ((513.8, 532.1), (541.1, 559.3)):
        under.append(rect((166.7, y0, 195.6, y1), hgrad(src, pno, 166.7, 195.6, y0 + 2, y1 - 2, tone=RED)))
    items = crop(src, pno, (155, 499, 207, 714), texts=False, skip=not_band, under=under)
    return items, {
        "status": "rebuilt",
        "notes": ("Outline and foot plate edge are extracted source strokes (clean left elevation of the pair). The "
                  "shaded stainless fill is raster in the source and is rebuilt as a measured vector gradient; the "
                  "two red reflective bands are rebuilt as gradients on the #C20016 token. Scale from the 1000 mm "
                  "dimension (top of tube to underside of the 8 mm plate); check: plate 220 mm. Photo render, "
                  "dimensioned elevation, plate plan (220 x 220, holes O14 at 180), dimension lines and callouts "
                  "left out."),
        "mm_per_pt": 1000.0 / (710.8 - T), "true_scale": True, "dims_mm": (220, 1000, 220),
    }


# ------------------------------------------------------------------ p45 flexposten
def _flex_items(src, pno, outline_bbox, outline_skip, left, right, band_gradients, bands, silhouette):
    under = [poly(silhouette, BLACK)]
    for (yt, yb, xlt, xrt, xlb, xrb), g in zip(bands, band_gradients):
        under.append(poly([(xlt, yt), (xrt, yt), (xrb, yb), (xlb, yb)], g))
    return crop(src, pno, outline_bbox, texts=False, skip=outline_skip, under=under)


@element("py-prod-flexpost-klein", "7.2 Flexpost klein", "prod", "post", 45)
def _(src):
    pno = 45
    sil = [
        (193.74, 404.15), (202.24, 404.15), (202.24, 406.99), (207.93, 406.99), (209.35, 408.39),
        (209.48, 421.17), (209.70, 441.04), (209.85, 455.19), (210.07, 475.06), (210.22, 489.21),
        (210.43, 509.08), (211.46, 604.03), (212.17, 604.60), (212.17, 606.87), (226.31, 617.18),
        (225.98, 618.21), (170.00, 618.21), (169.67, 617.18), (183.81, 606.87), (183.81, 604.60),
        (184.52, 604.03), (185.55, 509.08), (185.76, 489.21), (185.92, 475.06), (186.13, 455.19),
        (186.28, 441.04), (186.50, 421.17), (186.64, 408.39), (188.05, 406.99), (193.74, 406.99),
    ]
    bands = [(421.17, 441.04, 186.50, 209.48, 186.28, 209.70),
             (455.19, 475.06, 186.13, 209.85, 185.92, 210.07),
             (489.21, 509.08, 185.76, 210.22, 185.55, 210.43)]
    grads = [hgrad(src, pno, b[2], b[3], b[0] + 3, b[1] - 3, n=16, inset=1.0) for b in bands]
    items = _flex_items(src, pno, (165, 402, 230, 620.5), lambda p: p.stroke == "#414141", 0, 0, grads, bands, sil)
    return items, {
        "status": "rebuilt",
        "notes": ("Outline and edge lines are extracted source strokes (CAD sketch lines). The black plastic body and "
                  "the three white reflective bands are raster in the source and are rebuilt as a flat PY-Zwart "
                  "silhouette and measured vector band gradients. Scale from the 750 mm height; the drawing is not "
                  "perfectly uniform (top O80 measures 80 mm, foot measures about 200 mm against the stated 210). "
                  "Photo render, plan view of the foot, dimension lines and callouts left out."),
        "mm_per_pt": 750.0 / (618.21 - 404.15), "true_scale": True, "dims_mm": (210, 750, 210),
    }


@element("py-prod-flexpost-groot", "Flexpost groot", "prod", "post", 45)
def _(src):
    pno = 45
    sil = [
        (753.6, 416.3), (784.2, 416.3), (786.4, 418.5), (786.4, 625.6), (786.9, 626.1), (786.9, 628.9),
        (801.6, 634.3), (736.2, 634.3), (750.9, 628.9), (750.9, 626.1), (751.4, 625.6), (751.5, 418.5),
    ]
    ys = [420.7, 455.6, 490.4, 525.3, 560.2, 595.1]
    bands = [(ys[i], ys[i + 1], 751.5, 786.4, 751.5, 786.4) for i in (0, 2, 4)]
    grads = [hgrad(src, pno, 751.5, 786.4, b[0] + 4, b[1] - 4, n=16, inset=1.0) for b in bands]
    items = _flex_items(src, pno, (733, 414, 805, 636), None, 0, 0, grads, bands, sil)
    return items, {
        "status": "rebuilt",
        "notes": ("Outline and edge lines are extracted source strokes (CAD sketch lines). The black plastic body and "
                  "the three white reflective bands are raster in the source and are rebuilt as a flat PY-Zwart "
                  "silhouette and measured vector band gradients. Scale from the 1000 mm height; checks: tube "
                  "160 mm, foot 300 mm. Photo render, plan view of the foot (300 x 220), dimension lines and "
                  "callouts left out."),
        "mm_per_pt": 1000.0 / (634.3 - 416.3), "true_scale": True, "dims_mm": (300, 1000, 220),
    }


# ------------------------------------------------------------------ p47, p48 bins
def _dot(p):
    """Leader dot at the end of a callout line (black round bullet, about 3 pt)."""
    return p.fill == BLACK and p.stroke is None and (p.box[2] - p.box[0]) < 4 and (p.box[3] - p.box[1]) < 4


def _dim_tick(p):
    """Hairlines of the 400 mm dimension under the front view."""
    return p.fill is None and p.box[1] >= 381 and p.box[3] <= 385


@element("py-atom-sticker-trash", "vuilnisbak sticker", "atom", "sticker", (47, 24, 48),
         built_from=("py-atom-shape-bubble-solid",))
def _(src):
    items = crop(src, 47, (214, 192, 276.5, 266.5), texts=False)
    return items, {
        "status": "extracted",
        "notes": ("White bubble (volvlak) with the aqua bin pictogram, taken from the p47 front elevation. The source "
                  "holds no separate cut ring path: the faint ring in the render is the seam of a white circle "
                  "(O36) laid over the white bubble, which is kept as drawn. Scale from the stated sticker size on p24 "
                  "('200x16,6mm', read as 166 x 200 mm: the artwork is 60 x 72.3 pt, which gives 2.77 mm per pt on both "
                  "axes). Also used on p24 and p48. Intended on a navy (RAL 5002) bin face."),
        "mm_per_pt": 200.0 / 72.333, "true_scale": True, "dims_mm": (166, 200),
    }


@element("py-prod-vuilnisbak-wand", "8.1 Vuilnisbak wandmontage", "prod", "bin", 47,
         built_from=("py-atom-sticker-trash",))
def _(src):
    items = crop(src, 47, (170, 133.5, 463, 377.5), texts=False, skip=_dot)
    return items, {
        "status": "extracted",
        "notes": ("Front and side elevation of the Dulce 50 L bin as drawn in the handbook (RAL 5002 swatch drawn as "
                  "#082E7A, normalised to PY-Blauw #1A3580), including the trash sticker on the front. Scale from the "
                  "675 mm height dimension line (400 mm wide, 265 mm deep). The open-bin technical view, 3D render, "
                  "dimension lines, callouts and dots are left out."),
        "mm_per_pt": 675.0 / (373.9 - 135.5), "true_scale": True, "dims_mm": (400, 675, 265),
    }


@element("py-prod-vuilnisbak-staanders", "8.2 Vuilnisbak op staanders", "prod", "bin", 48,
         built_from=("py-atom-sticker-trash",))
def _(src):
    items = crop(src, 48, (150, 133.5, 463, 456), texts=False, skip=lambda p: _dot(p) or _dim_tick(p))
    return items, {
        "status": "extracted",
        "notes": ("Front elevation of the Dulce bin between the two RVS posts (koker 40 x 40 with 80 x 80 foot "
                  "plate, grey RAL 9006 drawn as #A0A1A0, normalised to #AEAEAE) plus the bin side view, with the "
                  "trash sticker on the front. Scale from the 850 mm dimension line (post top to foot plate, the "
                  "bin top sits about 50 mm higher). The open-bin technical view, 3D render, dimension lines and "
                  "callouts are left out."),
        "mm_per_pt": 850.0 / (453.4 - 153.4), "true_scale": True, "dims_mm": (400, 850, 265),
    }
