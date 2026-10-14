"""3.3.3 portaal spec (p20), 3.4 wandbord (p21), 3.5 hoogtebalken (p22).

p17 (3.2.3 portaal luxe spec) is a 3D render with no vector product content, so
py-prod-portaal-luxe-spec is deliberately not registered here."""
from pyassets import Gradient, Path, gradient_shape, rect_item
from pyassets.registry import crop, element

DARK = "#1D1D1B"
NAVY = "#1A3580"
NAVY_LIGHT = "#485E99"


# ================================================================== helpers
def _polylines(path):
    """Segments of a path as ((x0,y0),(x1,y1)) pairs (lines only)."""
    out, cur = [], None
    for sg in path.segs:
        if sg[0] == "M":
            cur = (sg[1], sg[2])
        elif sg[0] == "L":
            out.append((cur, (sg[1], sg[2])))
            cur = (sg[1], sg[2])
    return out


def _hits_x(segs, x):
    """y values where the non-vertical segments cross the vertical line at x."""
    ys = []
    for (ax, ay), (bx, by) in segs:
        if abs(ax - bx) < 0.02:
            continue
        lo, hi = min(ax, bx), max(ax, bx)
        if lo - 1e-9 <= x <= hi + 1e-9:
            t = (x - ax) / (bx - ax)
            ys.append(ay + t * (by - ay))
    return ys


def _hits_y(segs, y):
    xs = []
    for (ax, ay), (bx, by) in segs:
        if abs(ay - by) < 0.02:
            continue
        lo, hi = min(ay, by), max(ay, by)
        if lo - 1e-9 <= y <= hi + 1e-9:
            t = (y - ay) / (by - ay)
            xs.append(ax + t * (bx - ax))
    return xs


def _poly(pts, fill, tag="rebuilt"):
    segs = [("M", *pts[0])] + [("L", *p) for p in pts[1:]] + [("Z",)]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return Path(segs, fill=fill, box=(min(xs), min(ys), max(xs), max(ys)), tag=tag)


def _arc_segs(cx, cy, r, a0, a1, n=None):
    """Cubic Bezier arc from angle a0 to a1 (radians, y down), as segments starting after the first point."""
    import math

    n = n or max(1, int(abs(a1 - a0) / (math.pi / 2)) + 1)
    out = []
    da = (a1 - a0) / n
    k = 4 / 3 * math.tan(da / 4)
    for i in range(n):
        s, e = a0 + i * da, a0 + (i + 1) * da
        p0 = (cx + r * math.cos(s), cy + r * math.sin(s))
        p3 = (cx + r * math.cos(e), cy + r * math.sin(e))
        c1 = (p0[0] - k * r * math.sin(s), p0[1] + k * r * math.cos(s))
        c2 = (p3[0] + k * r * math.sin(e), p3[1] - k * r * math.cos(e))
        out.append(("C", c1[0], c1[1], c2[0], c2[1], p3[0], p3[1]))
    return out


# ================================================================== p20 CAD drawing
def _cad_skip(p):
    seq = getattr(p, "seq", 0)
    if 383 <= seq <= 393:  # leader lines, their dots and the R marker ring
        return True
    if 313 <= seq <= 381:  # fills hidden under a zero-area clip in the source (not visible)
        return True
    if seq == 268:  # detail C call-out ring
        return True
    if p.stroke == "#828181" or p.fill == "#828181":  # dimension lines and arrows
        return True
    if p.stroke == "#000000" and abs(p.width - 0.54) < 0.05:
        return True
    if p.fill == "#000000" and (p.box[2] - p.box[0]) < 4 and (p.box[3] - p.box[1]) < 4:
        return True
    return False


@element("py-prod-portaal-standaard-spec", "3.3.3 Portaal technische specificaties (standaard)", "prod", "portal", 20,
         variables=())
def _(src):
    bbox = (150, 262, 1100, 700)
    items = crop(src, 20, bbox, texts=False, skip=_cad_skip)
    ps = {p.seq: p for p in src.paths(20, (840, 550, 1100, 620))}

    # Detail C: the stripe fills are a raster in the source. Rebuild them from the outline.
    outline = _polylines(ps[407]) + _polylines(ps[408])
    edges = [1004.5, 1015.55, 1023.39, 1033.84, 1042.51, 1054.59, 1063.26, 1073.71, 1081.55, 1092.6]
    fills = []
    for i in range(len(edges) - 1):
        xa, xb = edges[i], edges[i + 1]
        n = 14
        xs = [xa + (xb - xa) * k / n for k in range(n + 1)]
        top, bot = [], []
        for x in xs:
            xe = min(max(x, 1004.52), 1092.58)
            ys = _hits_x(outline, xe)
            if not ys:
                continue
            top.append((x, min(ys)))
            bot.append((x, max(ys)))
        col = NAVY_LIGHT if i % 2 == 0 else NAVY
        f = _poly(top + bot[::-1], col)
        f.seq = 406.5 + i * 0.01
        fills.append(f)

    # Detail B: the soft top band is a raster. Rebuild as a vertical gradient band.
    bseg = _polylines(ps[411]) + _polylines(ps[412])
    y0, y1 = 558.0, 567.6
    left = [min(_hits_y(bseg, y)) for y in (y0 + 0.02, y1)]
    right = [max(_hits_y(bseg, y)) for y in (y0 + 0.02, y1)]
    band = _poly([(left[0], y0), (right[0], y0), (right[1], y1), (left[1], y1)], None)
    band.fill = Gradient(0, y0, 0, y1, ((0.0, NAVY), (1.0, NAVY_LIGHT)))
    band.seq = 61.5

    paths = [it for it in items if isinstance(it, Path)]
    paths += fills + [band]
    paths.sort(key=lambda p: getattr(p, "seq", 1e9))
    return paths, {"mm_per_pt": 200 / 220.6, "true_scale": True, "dims_mm": (200, 160), "status": "rebuilt",
                   "notes": "CAD drawing (isometric views, Details A, B, C). Dimension lines, leaders, call-out rings, labels and scale texts removed. Vector paths are taken from the source; the fills of Detail C (stripes) and the soft top band of Detail B are raster in the source and were rebuilt as vector shapes. Scale from the 200 mm profile width of Detail A (1:2); the isometric views and Detail C (5:1) are drawn at other scales."}


# ================================================================== hoogtebalk (p22)
RED = "#E30613"      # vector red of the source (RVV red); the raster bands are this red with a gloss overlay
BODY = "#F6F6F6"     # white of the raster bar body (RAL 9010 as drawn)
STEEL = "#9D9D9C"
STEEL_DARK = "#706F6F"
STEEL_LIGHT = "#DADADA"

# bar boxes on p22 (outline stroke rectangle) and lettering boxes, in PDF points
BARS = {
    "ketting": dict(box=(160.6, 198.1, 585.8, 217.2), edge=(160.6, 217.3, 585.9, 218.8), mm=2000,
                    letters=(270, 201, 476, 216), hangers=(213.7, 531.9)),
    "gaffel": dict(box=(160.6, 390.4, 692.0, 409.5), edge=(160.6, 409.5, 692.0, 411.0), mm=2500,
                   letters=(320, 393, 535, 410), hangers=(266.85, 585.9)),
    "pendel": dict(box=(160.6, 568.8, 798.3, 587.9), edge=(160.6, 587.9, 798.3, 589.5), mm=3000,
                   letters=(372, 571, 590, 588), hangers=(269.05, 692.05)),
}


def _mm_per_pt(key):
    b = BARS[key]
    return b["mm"] / (b["box"][2] - b["box"][0])


def band_items(box, total_mm):
    """White bar body plus the red 250 mm bands: half a band of white at each end, then red, white, red ...
    (2000 mm: 125 + 7 x 250 + 125, four red bands; 2500: five; 3000: six)."""
    x0, y0, x1, y1 = box
    u = (x1 - x0) / total_mm
    n_red = total_mm // 500
    items = [rect_item(x0, y0, x1, y1, fill=BODY, tag="rebuilt-pattern")]
    for k in range(n_red):
        a = x0 + (125 + 500 * k) * u
        items.append(rect_item(a, y0, a + 250 * u, y1, fill=RED, tag="rebuilt-pattern"))
    return items


def bar_outline(box, edge, width=0.21):
    x0, y0, x1, y1 = box
    return [rect_item(x0, y0, x1, y1, stroke=DARK, width=width),
            rect_item(*edge, fill=DARK)]


def lettering(src, key):
    return crop(src, 22, BARS[key]["letters"], texts=False)


def _hgrad(x0, x1, stops=((0.0, "#5E5E5D"), (0.45, "#E4E4E4"), (1.0, "#8C8C8B"))):
    return Gradient(x0, 0, x1, 0, stops)


def chain(cx, y_top, y_bot, k=1.0):
    """Simple vector chain: top tab, four links, bottom tab. k scales widths (p21 is drawn smaller)."""
    from pyassets import rect_item as R

    it = []
    w = 2.1 * k
    it.append(R(cx - w, y_top, cx + w, y_top + 8.4 * k, fill=_hgrad(cx - w, cx + w), stroke=DARK, width=0.09 * k))
    it.append(R(cx - w, y_bot - 7.6 * k, cx + w, y_bot, fill=_hgrad(cx - w, cx + w), stroke=DARK, width=0.09 * k))
    y = y_top + 6.0 * k
    for i in range(4):
        face = i % 2 == 0
        lw = (2.2 if face else 1.3) * k
        h = 15.5 * k
        it.append(R(cx - lw, y, cx + lw, y + h, stroke=STEEL if face else STEEL_DARK, width=(0.8 if face else 1.2) * k,
                    rx=lw, fill="#FFFFFF" if face else None))
        y += 13.6 * k
    it.append(R(cx + 1.5 * k, y_top + 10 * k, cx + 2.8 * k, y_top + 18 * k, fill=_hgrad(cx + 1.5 * k, cx + 2.8 * k), stroke=DARK, width=0.09 * k, rx=0.5 * k))
    it.append(R(cx + 1.5 * k, y_bot - 17 * k, cx + 2.8 * k, y_bot - 9 * k, fill=_hgrad(cx + 1.5 * k, cx + 2.8 * k), stroke=DARK, width=0.09 * k, rx=0.5 * k))
    return it


def gaffel(cx, y_top, k=1.0):
    """Gaffelset (clevis fork rod with end fittings), 89.3 pt tall at k = 1."""
    from pyassets import rect_item as R

    def X(v):
        return cx + v * k

    def Y(v):
        return y_top + v * k

    it = []
    # tube
    it.append(R(X(-2.15), Y(11.8), X(2.15), Y(77.5), fill=_hgrad(X(-2.15), X(2.15)), stroke=DARK, width=0.09 * k))
    # top fitting: two offset tabs and bolts
    it.append(R(X(-1.85), Y(0), X(1.75), Y(8.4), fill=_hgrad(X(-1.85), X(1.75)), stroke=DARK, width=0.09 * k))
    it.append(R(X(-0.2), Y(4.2), X(1.9), Y(11.8), fill=_hgrad(X(-0.2), X(1.9)), stroke=DARK, width=0.09 * k))
    it.append(R(X(-2.9), Y(5.0), X(-0.8), Y(6.8), fill=STEEL_LIGHT, stroke=DARK, width=0.09 * k, rx=0.5 * k))
    it.append(R(X(1.6), Y(5.0), X(3.5), Y(6.8), fill=STEEL_LIGHT, stroke=DARK, width=0.09 * k, rx=0.5 * k))
    # bottom fitting, mirrored
    it.append(R(X(-0.2), Y(77.5), X(1.9), Y(85.2), fill=_hgrad(X(-0.2), X(1.9)), stroke=DARK, width=0.09 * k))
    it.append(R(X(-1.85), Y(81.2), X(1.75), Y(89.3), fill=_hgrad(X(-1.85), X(1.75)), stroke=DARK, width=0.09 * k))
    it.append(R(X(-2.9), Y(82.5), X(-0.8), Y(84.3), fill=STEEL_LIGHT, stroke=DARK, width=0.09 * k, rx=0.5 * k))
    it.append(R(X(1.6), Y(82.5), X(3.5), Y(84.3), fill=STEEL_LIGHT, stroke=DARK, width=0.09 * k, rx=0.5 * k))
    return it


def pendel(cx, y_top, y_bar):
    """Starre pendel: RVS koker 40x40 with top flange, a short chain and an eye on the bar."""
    from pyassets import rect_item as R

    it = []
    it.append(R(cx - 4.25, y_top + 1.3, cx + 4.25, y_top + 60.6, fill=STEEL, stroke=DARK, width=0.09))
    it.append(R(cx - 8.55, y_top, cx + 8.55, y_top + 1.3, fill=STEEL, stroke=DARK, width=0.09))
    it.append(R(cx - 4.25, y_top + 60.6, cx + 4.25, y_top + 61.4, fill=DARK, stroke=DARK, width=0.09))
    it.append(R(cx - 1.1, y_top + 57.5, cx + 1.1, y_top + 59.4, fill=STEEL_LIGHT, stroke=DARK, width=0.09, rx=0.9))
    y = y_top + 61.4
    # shackle ring, two links, barrel and the eye on the bar
    it.append(R(cx - 2.6, y + 0.3, cx + 2.6, y + 5.3, stroke=STEEL, width=0.9, rx=2.5))
    it.append(R(cx - 2.6, y + 3.6, cx + 2.6, y + 14.6, stroke=STEEL, width=0.9, rx=2.5, fill="#FFFFFF"))
    it.append(R(cx - 2.2, y + 11.0, cx + 2.2, y + 22.0, stroke=STEEL_DARK, width=0.9, rx=2.2))
    it.append(R(cx + 1.9, y + 15.5, cx + 3.1, y + 19.9, fill=_hgrad(cx + 1.9, cx + 3.1), stroke=DARK, width=0.09, rx=0.4))
    it.append(R(cx - 1.4, y + 19.5, cx + 1.0, y_bar, fill=_hgrad(cx - 1.4, cx + 1.0), stroke=DARK, width=0.09))
    it.append(R(cx - 3.4, y_bar - 3.0, cx - 1.4, y_bar, fill=STEEL_DARK, stroke=DARK, width=0.09))
    return it


def _bar(src, key, with_hw=True):
    b = BARS[key]
    items = []
    if with_hw:
        y0 = b["box"][1]
        for cx in b["hangers"]:
            if key == "ketting":
                items += chain(cx, 134.5, y0)
            elif key == "gaffel":
                items += gaffel(cx, 301.1)
            else:
                items += pendel(cx, 481.4, y0)
    items += band_items(b["box"], b["mm"])
    items += bar_outline(b["box"], b["edge"])
    items += lettering(src, key)
    return items


_NOTE_HW = ("Bar outline, bottom edge and snijletters follow the source drawing; the white body and the red 250 mm bands "
            "(raster strips in the source) are rebuilt as vector rectangles in the source red #E30613, half a band of white "
            "at each end. The {hw} hardware is raster in the source and is rebuilt here as simple vector shapes.")


def _prod(src, key, hw):
    b = BARS[key]
    return _bar(src, key), {"status": "rebuilt", "mm_per_pt": _mm_per_pt(key), "true_scale": True,
                            "dims_mm": (b["mm"], 90), "notes": _NOTE_HW.format(hw=hw)
                            + " Scale from the bar length of %d mm. The handbook labels the bar height 900 mm, which is a typo for 90 mm and is not reproduced." % b["mm"]}


@element("py-prod-hoogtebalk-ketting", "3.5 Hoogtebalk met ketting", "prod", "hoogtebalk", 22,
         variables=("length", "height text"), built_from=("py-comp-hoogtebalk-bar",))
def _(src):
    return _prod(src, "ketting", "chain")


@element("py-prod-hoogtebalk-gaffel", "Hoogtebalk met gaffelset", "prod", "hoogtebalk", 22,
         variables=("length", "height text"), built_from=("py-comp-hoogtebalk-bar",))
def _(src):
    return _prod(src, "gaffel", "gaffelset")


@element("py-prod-hoogtebalk-pendel", "Hoogtebalk met starre pendel", "prod", "hoogtebalk", 22,
         variables=("length", "height text"), built_from=("py-comp-hoogtebalk-bar",))
def _(src):
    return _prod(src, "pendel", "pendel and chain")


@element("py-comp-hoogtebalk-bar", "hoogtebalk", "comp", "hoogtebalk", 22, variables=("length", "height text"),
         built_from=("py-atom-pattern-hoogtebalk-bands", "py-atom-text-hoogtebalk-lettering"))
def _(src):
    b = BARS["ketting"]
    return _bar(src, "ketting", with_hw=False), {
        "status": "rebuilt", "mm_per_pt": _mm_per_pt("ketting"), "true_scale": True, "dims_mm": (2000, 90),
        "notes": "Bar without hanging hardware, shown at 2000 mm. Outline, bottom edge and snijletters follow the source; the body and red bands are rebuilt vector rectangles (raster in the source). The handbook height label 900 mm is a typo for 90 mm and is not reproduced."}


@element("py-atom-pattern-hoogtebalk-bands", "hoogtebalk rode banden", "atom", "pattern", 22, variables=("bar length",))
def _(src):
    b = BARS["ketting"]
    return band_items(b["box"], b["mm"]), {
        "status": "rebuilt", "mm_per_pt": _mm_per_pt("ketting"), "true_scale": True, "dims_mm": (2000, 90),
        "notes": "Red/white pattern of 250 mm bands over a 2000 mm bar: half a band of white at each end, then red, white, red, white, red, white, red. The bands are raster strips in the source; rebuilt here as vector rectangles in the source red #E30613 on the bar white #F6F6F6. For 2500 mm the bar carries five red bands, for 3000 mm six."}


@element("py-atom-text-hoogtebalk-lettering", "snijletters", "atom", "text", 22, variables=("height value",))
def _(src):
    items = crop(src, 22, (150, 648, 586, 682.5), texts=False)
    return items, {"mm_per_pt": 1000 / 426.0, "true_scale": True, "dims_mm": (1000, 65),
                   "notes": "Outlined letters 'maximale doorrijhoogte 2,1m' (outlines in the source, kept as outlines). Clean sample at the bottom of p22, 1000 mm wide."}


# ================================================================== wandbord (p21)
PLATE = (186.8, 253.0, 631.2, 293.4)   # plate face, 300 mm high
WB_BARS = (
    dict(box=(219.7, 316.0, 376.3, 321.6), edge=(219.7, 321.6, 376.3, 322.1), letters=None, hangers=(250.85, 344.8)),
    dict(box=(442.9, 316.0, 599.5, 321.6), edge=(442.9, 321.6, 599.5, 322.1), letters=(490.5, 317.0, 552.0, 321.6),
         hangers=(474.05, 568.0)),
)


def _wb_skip(p):
    seq = getattr(p, "seq", 0)
    if p.stroke == "#C4C4C4":          # brick wall joints
        return True
    if 667 <= seq <= 680:              # hairline frame rectangles around the plate (no visible content)
        return True
    if seq >= 1000:                    # soft-mask shadow strokes (clipped in the source)
        return True
    if seq == 739:                     # hairline around the display face
        return True
    if 741 <= seq <= 875 and p.stroke in ("#711515", "#E30613"):   # unlit/red LED dots, hidden in the source render
        return True
    return False


@element("py-prod-wandbord", "3.4 Wandbord", "prod", "wandbord", 21, variables=("location name", "width"),
         built_from=("py-comp-portal-face-2baans", "py-comp-hoogtebalk-bar"))
def _(src):
    import math

    x0, y0, x1, y1 = PLATE
    items = crop(src, 21, (186, 252, 632, 294), skip=_wb_skip, outline_fonts=("RWSTTDdx",))
    paths = [it for it in items if isinstance(it, Path)]
    texts = [it for it in items if not isinstance(it, Path)]

    # P block: the verloop crescent is a clip + shading in the source; aqua and navy discs are clipped by the plate.
    cres = [c for c in src.clips(21, (186, 252, 232, 295)) if getattr(c, "seq", 0) == 692.5]
    r = 49.35
    # aqua disc (centre 177.85, 272.6) cut to the plate: left edge x0, top y0, bottom y1
    cx, cy = 177.85, 272.55
    at = math.asin((cy - y0) / r)      # arc meets the plate top edge at -at, the bottom edge at +ab
    ab = math.asin((y1 - cy) / r)
    xt = cx + r * math.cos(at)
    xb = cx + r * math.cos(ab)
    segs = [("M", x0, y0), ("L", xt, y0)] + _arc_segs(cx, cy, r, -at, ab) + [("L", x0, y1), ("Z",)]
    aqua = Path(segs, fill="#32B9CD", box=(x0, y0, cx + r, y1), tag="rebuilt")
    aqua.seq = 694
    # navy disc on the right (centre 537.2, 272.6) cut to the plate, joined with the navy bar
    cx2 = 537.2
    xt2 = cx2 + r * math.cos(at)
    segs = [("M", 213.7, y0), ("L", xt2, y0)] + _arc_segs(cx2, cy, r, -at, ab) + [("L", 213.7, y1), ("Z",)]
    navy = Path(segs, fill=NAVY, box=(213.7, y0, cx2 + r, y1), tag="rebuilt")
    navy.seq = 691.1
    extra = [aqua, navy]
    # display housing (raster glow in the source): simple dark bezel behind the LED face
    hous = rect_item(547.6, 264.6, 578.8, 281.6, fill=DARK, rx=1.3, tag="rebuilt")
    hous.seq = 737.5
    extra.append(hous)
    for c in cres:
        extra.append(gradient_shape(src, 21, c))
    paths = [p for p in paths if getattr(p, "seq", 0) != 691]   # the plain navy rectangle is replaced by the rounded shape
    paths += extra
    paths.sort(key=lambda p: getattr(p, "seq", 1e9))

    # two hoogtebalken with gaffelsets (rebuilt, the bands and hardware are raster in the source)
    bars = []
    for b in WB_BARS:
        for cx_ in b["hangers"]:
            bars += gaffel(cx_, 297.2, 18.8 / 89.3)
        bars += band_items(b["box"], 2500)
        bars += bar_outline(b["box"], b["edge"], width=0.06)
        if b["letters"]:
            bars += crop(src, 21, b["letters"], texts=False)
    return paths + bars + texts, {
        "status": "rebuilt", "mm_per_pt": 300 / (y1 - y0), "true_scale": True, "dims_mm": (3300, 300),
        "notes": "Wandbord plate (300 mm high; width variable, 3300 mm as drawn) with display and RVV cluster, plus two hoogtebalken. Brick wall, dark wall gradient, dimension and call-out lines are left out. Plate vector paths are taken from the source; the P block and right navy edge (discs clipped by the plate) and the verloop crescent (clip and shading in the source) are rebuilt. The hoogtebalken (red bands and gaffelsets are raster in the source) are rebuilt as vectors. Scale from the 300 mm plate height; the hoogtebalken are drawn schematically in the handbook (2500 x 90 mm per its call-out) and are not at plate scale."}
