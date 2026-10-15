"""PM-137 module p90: banner "dranghekspandoek dubbelzijdig" (2440 x 1570 mm, CMYK) and the two P+R Mandelapark pieces (WTC sticker and poster, RGB ICC).

All numbers were measured from the sources (page mm, origin top left of the MediaBox) with tools/print_probe.py and by pixel overlay.
Banner: page = trim + 10 mm on every side (the navy field itself stops at the trim bottom, 1560 mm: no bottom bleed in the source).
The upper half (page y 10 to 775) is the back side and is rotated 180 degrees about its own centre (1220 / 392.5 mm), the lower half is the front.
Sticker and poster: page = trim, no bleed in the source.
"""
import io
import math
import re

import numpy as np

from pyassets import printsrc
from pyassets.apps import application
from pyassets.compose import Doc, lib_svg, text_width
from pyassets.core import PT_MM, TF, Path, Raw, Text, _from_pathops, _to_pathops, font_css
from pyassets.registry import crop, element

NAVY = "#1A3580"         # py-tok-color-blauw
WHITE = "#FFFFFF"        # py-tok-color-wit
AQUA_DRANGHEK = "#71CBDF"  # light aqua CMYK 51/1/11/0 (no token, observed)
AQUA_WTC = "#78C9DC"     # light aqua of the RGB files (no token, observed)
AQUA_TAG = "#79C9DC"     # chevron of the URL tag (same colour, 1 step off in the file)

box = printsrc.box_mm


def _pd(p, dx=0.0, dy=0.0, s=PT_MM):
    return p.d(TF(0.0, 0.0, s, dx, dy))


def _pbox(p, dx=0.0, dy=0.0):
    b = p.box
    return (b[0] * PT_MM + dx, b[1] * PT_MM + dy, b[2] * PT_MM + dx, b[3] * PT_MM + dy)


# ================================================================================================ geometry helpers
def _lib_paths(ref_id):
    """(d, fill) of every path of a library SVG (own group transform not applied)."""
    inner = lib_svg(ref_id)[3]
    out = []
    for m in re.finditer(r"<path\b([^>]*)/>", inner):
        a = m.group(1)
        d = re.search(r'\sd="([^"]+)"', a).group(1)
        f = re.search(r'fill="([^"]+)"', a)
        out.append((d, f.group(1) if f else None))
    return out


def _cut_lib(ref_id, tx, ty, scale, rect, angle=0.0, flip_x=False, pre=(0.0, 0.0), recolor=None):
    """Library paths mapped like Doc.place (translate, rotate, scale, optional x flip) and cut to `rect` (doc coordinates) with pathops.
    Returns [(d, fill, box)]. Used where the placed artwork is cropped by the page (figure, price bubble)."""
    import pathops
    from fontTools.misc.transform import Transform
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.svgLib.path import parse_path

    ew = lib_svg(ref_id)[0]
    t = Transform().translate(tx, ty).rotate(math.radians(angle)).scale(scale, scale)
    if flip_x:
        t = t.translate(ew, 0).scale(-1, 1)
    t = t.translate(*pre)
    x0, y0, x1, y1 = rect
    out = []
    for d, fill in _lib_paths(ref_id):
        po = pathops.Path()
        parse_path(d, TransformPen(po.getPen(), t))
        r = pathops.Path()
        pen = r.getPen()
        pen.moveTo((x0, y0)); pen.lineTo((x1, y0)); pen.lineTo((x1, y1)); pen.lineTo((x0, y1)); pen.closePath()
        res = pathops.op(po, r, pathops.PathOp.INTERSECTION)
        sp, bp = SVGPathPen(None, ntos=lambda v: ("%.3f" % v).rstrip("0").rstrip(".")), BoundsPen(None)
        res.draw(sp)
        res.draw(bp)
        if bp.bounds is None:
            continue
        out.append((sp.getCommands(), (recolor or {}).get(fill, fill), bp.bounds))
    return out


def _bubble_fit(key, search_box):
    """Similarity transform (scale, angle in degrees, tx, ty) that maps the library bubble path (py-comp-price-bubble-speech, element coordinates)
    onto the bubble path of the source (17 control points, measured: residual 0.4 mm rms on the sticker)."""
    d = _lib_paths("py-comp-price-bubble-speech")[0][0]
    nums = np.array([float(v) for v in re.findall(r"-?\d+\.?\d*", d)]).reshape(-1, 2) + np.array([-408.096, 8.654])
    ps = [p for p in printsrc.source(key).paths(1, box(*search_box), tol=3.0) if p.fill in (AQUA_WTC, AQUA_TAG) and (p.box[2] - p.box[0]) * PT_MM > 150]
    pts = []
    for sg in ps[0].segs:
        v = [q * PT_MM for q in sg[1:]]
        pts += [(v[i], v[i + 1]) for i in range(0, len(v), 2)]
    a = nums[:, 0] + 1j * nums[:, 1]
    b = np.array(pts)[:, 0] + 1j * np.array(pts)[:, 1]
    am, bm = a.mean(), b.mean()
    z = np.vdot(a - am, b - bm) / np.vdot(a - am, a - am)
    t = bm - z * am
    return abs(z), math.degrees(np.angle(z)), t.real, t.imag


# ================================================================================================ element 1: pill with storing contact
PILL_X1, PILL_Y0, PILL_Y1 = 1427.12, 364.59, 681.82   # source mm: rounded end at the right (upside down), cut off by the page at x 0
PILL_H = PILL_Y1 - PILL_Y0
STORE_SIZE = 49.4
STORE_U, STORE_V = PILL_X1 - 1295.0, PILL_Y1 - 505.4   # text start (upright: from the rounded end) and baseline from the pill top
STORE_TEXT = "Bij storingen, bel naar "
STORE_PHONE = "085 21 30 422"


@element("py-comp-pill-storing-contact", "Pil storingen contact", "comp", "pill", 1, src="dranghek", status="rebuilt",
         variables=("text", "phone number"),
         notes="Light aqua pill of the banner back side with the storing contact and the navy logo, drawn upright (in the source it is rotated 180 degrees and cut off at "
               "the left page edge; here the rounded end is on the left and the flat end is the cut at the page edge, 1427.1 x 317.2 mm, to be placed so that the cut bleeds off). "
               "Light aqua CMYK 51/1/11/0 (viewer #71CBDF) has no token and is kept as sampled. REBUILT: the pill is constructed (full round end, radius 158.6 mm measured from the "
               "source curves; the source path is 2062 mm long and 635 mm of it lies off the page), the text is live Ubuntu Medium 49.4 mm in the navy token (start 132.1 mm from the "
               "rounded end, baseline 176.4 mm below the top), split in 'text' and 'phone number' (one span in the source, same weight and size). "
               "The logo is the print logo as drawn in the source (14 paths: beeldmerk, wordmark and registered mark, stacked, 280 mm wide, 68 mm from the cut), "
               "taken from the source and rotated: NOT py-atom-logo-stacked-black, because the print wordmark is about 3 percent narrower than the library one "
               "(the word 'you' in particular) while the beeldmerk is the library shape at 4.2x; colour normalised to the token navy. Open point: which logo drawing is the master.")
def _(src):
    d = Doc("py-comp-pill-storing-contact", "Pil storingen contact", tight=True)
    r = PILL_H / 2
    w = PILL_X1
    d.path(f"M{w:.3f} 0H{r:.3f}A{r:.3f} {r:.3f} 0 0 0 {r:.3f} {PILL_H:.3f}H{w:.3f}Z", (0, 0, w, PILL_H), fill=AQUA_DRANGHEK, gid="pill")
    d.text(STORE_U, STORE_V, STORE_TEXT.rstrip(), STORE_SIZE, NAVY, weight=500, variable="text")
    d.text(STORE_U + text_width(STORE_TEXT, STORE_SIZE, 500), STORE_V, STORE_PHONE, STORE_SIZE, NAVY, weight=500, variable="phone-number")
    logo = crop(src, 1, box(60, 450, 355, 630), texts=False)
    assert len(logo) == 14, len(logo)
    tf = TF(0.0, 0.0, -PT_MM, PILL_X1, PILL_Y1)  # rotation by 180 degrees: u = 1427.12 - x, v = 681.82 - y
    with d.group("logo"):
        for p in logo:
            b = _pbox(p)
            bx = (PILL_X1 - b[2], PILL_Y1 - b[3], PILL_X1 - b[0], PILL_Y1 - b[1])
            d.path(p.d(tf), bx, fill=p.fill, evenodd=p.evenodd)
    return d


# ================================================================================================ element 2: URL tag with chevron
TAG = (458.48, 938.35, 678.12, 971.28)   # source mm
TAG_R = 1.43
TAG_SIZE = 18.4
TAG_BASE = 960.88
TAG_X1, TAG_X2 = 467.08, 551.16


@element("py-comp-url-tag-chevron", "URL label met chevron", "comp", "tag", 1, src="wtcposter", status="rebuilt", variables=("url bold", "url regular"),
         notes="Navy tag 219.6 x 32.9 mm (corner radius 1.43 mm) with the URL on one line: 'voordelig' Ubuntu Bold white and 'parkeren.nl' Ubuntu Light white, both 18.4 mm, "
               "light aqua chevron (source path, 15.9 x 23.9 mm) and a light aqua registered mark. Light aqua (viewer #79C9DC, RGB file) has no token and is kept as sampled. "
               "REBUILT: the letters are outlined in the source and rebuilt as live text, fitted by overlay (pixel overlap about 0.8 on 18 mm letters): the glyph height agrees at 18.4 mm for both "
               "words, 'voordelig' needs a tracking of -0.18 mm in Bold, 'parkeren.nl' fits Light (Regular is 2.3 percent too narrow and does not overlay), as in py-comp-url-chevron. "
               "The tag colour of the file is #374F9C (lighter than the page navy #23398E), normalised to the token navy. The tag and the registered mark are new; the chevron has the shape of "
               "py-comp-url-chevron at scale 0.54 but that comp is a two line URL (voordelig / parkeren.nl at 37.7 and 34.4 mm, no tag), so this is a separate comp. "
               "Place it on white paper (navy tag). The registered mark is the source path (2.4 mm), the library atom py-atom-mark-registered is not used because the colour is light aqua here.")
def _(src):
    d = Doc("py-comp-url-tag-chevron", "URL label met chevron", tight=True)
    x0, y0, x1, y1 = TAG
    d.rect(x0, y0, x1, y1, fill=NAVY, rx=TAG_R, gid="tag")
    d.text(TAG_X1, TAG_BASE, "voordelig", TAG_SIZE, WHITE, weight=700, spacing=-0.18, variable="url-bold")
    d.text(TAG_X2, TAG_BASE, "parkeren.nl", TAG_SIZE, WHITE, weight=300, spacing=-0.044, variable="url-regular")
    for p in crop(src, 1, box(644, 942, 672, 968), texts=False):
        d.path(_pd(p), _pbox(p), fill=AQUA_TAG, gid="chevron" if (p.box[2] - p.box[0]) * PT_MM > 10 else "registered")
    return d


# ================================================================================================ application 4: banner
PAGE = (2440.0, 1570.0)
BLEED = 10.0
TRIM = (2420.0, 1550.0)
CX, CY_BACK = 1220.0, 392.5   # rotation centre of the back half in page coordinates
LIGHT, BOLD, MED = 300, 700, 500
FOLD_Y = 775.0 - BLEED   # trim relative
SIZE_F = 172.9
SIZE_B = 127.0

# back side, upright frame (page mm, x' = 2440 - x, y' = 785 - y), measured from the source spans of the rotated texts
BACK_TEXT_X = 2440 - 1935.6
BACK_L1, BACK_L2 = 785 - 201.4, 785 - 81.5
FIG_SCALE = 20.82
FIG_PAGE = (-92.0, 122.26)   # top left of the (mirrored) figure atom in the upright frame, page mm


def _rotated_spans(key=("dranghek")):
    """The four rotated spans of the banner as raw svg text (Source.texts writes them unrotated)."""
    src = printsrc.source("dranghek")
    extra, names = [], []
    for b in src.page(1).get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            if l["dir"][0] > -0.5:
                continue
            for s in l["spans"]:
                fam, w, it = font_css(s["font"])
                org = s["origin"]
                t = Text(org[0], org[1], s["text"], fam, w, it, s["size"], "#" + "%06X" % s["color"], 0.0, box=(0, 0, 0, 0))
                xml = t.svg(TF(0.0, 0.0, PT_MM, 0.0, 0.0), None)
                xml = xml.replace("<text ", f'<text transform="rotate(180 {org[0] * PT_MM:.3f} {org[1] * PT_MM:.3f})" ', 1)
                extra.append(Raw(xml, box=(0, 0, 0, 0)))
                names.append(s["text"].strip())
    return extra, names


def _banner_template(ctx, app_id):
    d = ctx.Doc(app_id, "Dranghekspandoek dubbelzijdig", trim=TRIM, bleed=BLEED)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-light", "py-tok-type-ubuntu-medium", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-bold-italic")
    d.rect(-BLEED, -BLEED, TRIM[0] + BLEED, TRIM[1] + BLEED, fill=NAVY, gid="bleed-background", variable="background-colour", example=NAVY)
    # ---- front (lower half, reads normally)
    with d.group("side-front"):
        with d.group("py-atom-icon-warning-triangle"):
            d.place("py-atom-icon-warning-triangle", 73.7 - BLEED, 1058.6 - BLEED, scale=1.0)
        d.text(534.9 - BLEED, 1041.5 - BLEED, "", SIZE_F, WHITE, weight=LIGHT, variable="front-nl",
               runs=[("Alleen voor ", LIGHT), ("abonnees", BOLD), ("!", LIGHT)])
        with d.group("py-atom-line-divider"):
            d.line(534.9 - BLEED, 1126.1 - BLEED, 2294.0 - BLEED, 1126.1 - BLEED, AQUA_DRANGHEK, 7.056, gid="divider")
        d.text(534.9 - BLEED, 1351.9 - BLEED, "", SIZE_F, WHITE, weight=BOLD, variable="front-en",
               runs=[("Subscribers ", BOLD), ("only!", LIGHT)])
    # ---- back (upper half, rotated 180 degrees about its centre; the layout below is upright)
    with d.group("side-back", transform=f"rotate(180 {CX} {CY_BACK})"):
        with d.group("py-comp-pill-storing-contact"):
            d.place("py-comp-pill-storing-contact", (2440 - PILL_X1) - BLEED, (785 - PILL_Y1) - BLEED)
        d.variables.update({"text": "Bij storingen, bel naar", "phone-number": STORE_PHONE})
        d.text(BACK_TEXT_X - BLEED, BACK_L1 - BLEED, "Tot ziens", SIZE_B, WHITE, weight=BOLD, variable="back-nl")
        d.text(BACK_TEXT_X - BLEED, BACK_L2 - BLEED, "Goodbye", SIZE_B, AQUA_DRANGHEK, weight=BOLD, italic=True, variable="back-en")
        with d.group("py-atom-figure-wave"):
            d.uses("py-atom-figure-wave")
            rect = (-BLEED, -BLEED, TRIM[0] + BLEED, 775.0)   # band of the back side, upright frame, trim relative
            for dd, fill, bb in _cut_lib("py-atom-figure-wave", FIG_PAGE[0] - BLEED, FIG_PAGE[1] - BLEED, FIG_SCALE, rect, flip_x=True,
                                         recolor={NAVY: WHITE}):
                d.path(dd, bb, fill=fill)
    with d.group("fold-line"):
        d.line(-BLEED, FOLD_Y, TRIM[0] + BLEED, FOLD_Y, WHITE, 7.056, gid="fold")
    d.guides(*TRIM)
    return d


@application("py-app-banner-dranghek-abonnees", "Dranghekspandoek dubbelzijdig", "banner", trim_mm=TRIM, source=[("dranghek", [1])], bleed_mm=BLEED,
             status="rebuilt")
def _(ctx):
    extra, names = _rotated_spans()
    ref = ctx.reference("dranghek", 1, omit=lambda p: p.fill == "#231F20", skip_text=lambda t: t.strip() in names, extra=extra)
    d = _banner_template(ctx, "py-app-banner-dranghek-abonnees")
    return dict(
        reference={"": ref}, template={"": d},
        omitted=["Fold band shadow: the 15901 x 112 px grayscale raster at y 766 to 784 mm (soft mask of the shadow) and the 20 percent black rectangle it masks "
                 "(-29 to 2469 x 767 to 783 mm, #231F20). Without the soft mask the rectangle would show as a hard band, so both are left out; the 20 pt white fold line at y 775 stays."],
        copy_corrections=[],
        notes=("Print file of 2440 x 1570 mm (trim 2420 x 1550, 10 mm bleed set), CMYK, ONE version that holds both sides: the lower half (page y 775 to 1560) is the front and reads "
               "normally, the upper half (page y 10 to 775) is the back side and is rotated 180 degrees in the file (the back reads upside down), the two halves meet at the white fold line at y 775. "
               "Template: front group side-front (warning triangle py-atom-icon-warning-triangle at its source position, 'Alleen voor ' Ubuntu Light + 'abonnees' Bold + '!' Light 172.9 mm white, "
               "divider light aqua 20 pt = 7.06 mm from x 534.9 to 2294, 'Subscribers ' Bold + 'only!' Light); back group side-back = the upright layout rotated 180 degrees about (1220 / 392.5) so "
               "the file reads like the source: comp py-comp-pill-storing-contact (new, upright, flat end bleeds off the page edge), 'Tot ziens' Ubuntu Bold white and 'Goodbye' Ubuntu Bold Italic light aqua "
               "127 mm (start x 504.4, baselines 583.6 and 703.5 in the upright frame), and the white figure = library py-atom-figure-wave mirrored, scaled 20.82x (fitted by pixel overlay, overlap 0.92: the source torso is about 6 mm wider and its head pointer is mirrored; "
               " the head outline gap of the source is a navy 31 pt stroke, in the library the head is a separate path), cut with pathops to the band of the back side; the body runs off the page as in the source. "
               "Group fold-line: white 20 pt (7.06 mm) at y 775 (765 trim relative). Colours: the blue of the file is CMYK 100/85/10/1 (#1A4691, text 24408F, stroke 213B86) and is the token navy in the template; "
               "light aqua CMYK 51/1/11/0 (#71CBDF: pill, triangle, divider, Goodbye) has no token and is kept as sampled. "
               "Variables: front-nl, front-en, back-nl, back-en, text, phone-number (the last two live inside the pill comp), background-colour. "
               "Open points for the owner: (1) the storing number 085 21 30 422 differs from 085 4011647 (Maashaven pyloon, posters); "
               "(2) the fold line is at y 775, not at the middle of the trim (785): the back is 765 mm and the front 785 mm high, check with the printer; "
               "(3) bleed: 10 mm is set on top, left and right, but the navy field stops at y 1560 (the trim bottom): no bottom bleed in the source, the template adds it; "
               "(4) the fold shadow is a raster in the source and is not reproduced; (5) the print logo differs slightly from the library logo (see the pill comp). "
               "No spelling errors found. No cut contour: a banner, not a sticker."),
    )


# ================================================================================================ application 5: P+R sticker Mandelapark
S_SYM = (143.0, 132.7)
S_SYM_SCALE = 4.968
S_LABEL = (148.6, 371.8, 225.2)
S_LOCK = (122.8, 541.6, 1.314)
S_NAME = (285.9, 615.9, 665.7, 49.8)
S_FIELD_H = 516.1
TXT_ANG = -6.9
S_PRICE = (65.7, 149.07, 103.75)
S_SUFFIX = (183.24, 134.66, 38.8)
S_LABEL2 = (81.44, 184.81, 28.84)


def _price_texts(d, price, suffix, label):
    d.text(price[0], price[1], "€6", price[2], WHITE, weight=BOLD, rotate=TXT_ANG, variable="price")
    d.text(suffix[0], suffix[1], ",-", suffix[2], WHITE, weight=BOLD, rotate=TXT_ANG, variable="price-suffix")
    d.text(label[0], label[1], "per dag", label[2], WHITE, weight=BOLD, rotate=TXT_ANG, variable="label")


@application("py-app-sticker-pr-mandelapark", "P+R sticker Mandelapark", "sticker", trim_mm=(700, 700), source=[("wtcsticker", [1])], bleed_mm=3.0,
             status="rebuilt",
             cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": 4.2,
                          "note": "Proposal: the source has no cut contour. Corner radius 4.2 mm is borrowed from the diefstal footer bar (4.23 mm); to be confirmed by the owner."})
def _(ctx):
    app_id = "py-app-sticker-pr-mandelapark"
    d = ctx.Doc(app_id, "P+R sticker Mandelapark", trim=(700, 700), bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-bold")
    with d.group("bleed-background"):
        d.path(f"M-3 -3H703V{S_FIELD_H}H-3Z", (-3, -3, 703, S_FIELD_H), fill=NAVY, gid="field", variable="background-colour", example=NAVY)
    with d.group("py-comp-symbol-pr"):
        d.place("py-comp-symbol-pr", S_SYM[0], S_SYM[1], scale=S_SYM_SCALE, strip_text=True)
        d.text(S_LABEL[0], S_LABEL[1], "P+R", S_LABEL[2], WHITE, weight=BOLD, variable="label-pr")
    sc, ang, tx, ty = _bubble_fit("wtcsticker", (20, 10, 240, 260))
    with d.group("py-comp-price-bubble-speech"):
        d.place("py-comp-price-bubble-speech", tx, ty, scale=sc, rotate=ang, strip_text=True)
        _price_texts(d, S_PRICE, S_SUFFIX, S_LABEL2)
    with d.group("py-comp-lockup-location-garage"):
        d.place("py-comp-lockup-location-garage", S_LOCK[0], S_LOCK[1], scale=S_LOCK[2], strip_text=True)
        d.text(S_NAME[0], S_NAME[1], "Parking", S_NAME[3], NAVY, weight=BOLD, variable="location-line-1")
        d.text(S_NAME[0], S_NAME[2], "Mandelapark", S_NAME[3], NAVY, weight=BOLD, variable="location-line-2")
    d.cut_contour(0, 0, 700, 700, rx=4.2)
    d.guides(700, 700)
    return dict(
        reference={"": ctx.reference("wtcsticker", 1)}, template={"": d},
        omitted=[],
        copy_corrections=[],
        notes=("700 x 700 mm, no bleed in the source (page = trim, RGB ICC). The navy field is 700 x 516.1 mm and runs to the top and the sides (template: 3 mm into the bleed), the lower 183.9 mm is "
               "white paper (no ink, no white fill in the template). The reference keeps a navy rectangle (118.7 to 596.2 x 176.6 to 402.1 mm, #233A89) between the two bars: navy on navy, invisible, "
               "left out of the template. P+R symbol: py-comp-symbol-pr scaled 4.968x at 143.0 / 132.7 mm, the label P+R is live Ubuntu Bold 225.2 mm white (variable label-pr, source text is live). "
               "Price bubble: py-comp-price-bubble-speech MATCHES: the 17 control points of the source path equal the library bubble at scale %.4f and rotation %.2f degrees (residual 0.44 mm rms), "
               "so it is placed (strip_text) with that scale and rotation. The price numerals are outlined in the source and rebuilt as live Ubuntu Bold, fitted by overlay "
               "(pixel overlap 0.99 / 0.94 / 0.97): '€6' 103.75 mm, ',-' 38.8 mm (a separate smaller text, the comma and hyphen are 37 percent of the price height in the source), 'per dag' 28.84 mm, all white, "
               "rotated %.1f degrees (the library bubble text is rotated 6.7 degrees). Lockup: the garage symbol is py-comp-lockup-location-garage at scale 1.314 (symbol 133.7 mm wide), but the "
               "proportions of the library lockup do not hold here (name 49.8 mm against 46.7 mm at symbol width 101.8 in the library, name start 163.1 mm from the symbol edge against 140 mm, "
               "baseline pitch 49.8 mm): the name is drawn as own live text with strip_text, Ubuntu Bold 49.8 mm navy, two lines (Parking / Mandelapark, baselines 615.9 and 665.7 mm). "
               "The file blue #233A89 (RGB ICC) is the token navy in the template, light aqua #78C9DC (no token) is kept as sampled. Variables: label-pr, price, price-suffix, label, location-line-1, "
               "location-line-2, background-colour. The cut contour (ThruCut, 1 pt, 0.2 mm inside the trim, radius 4.2 mm) is a PROPOSAL: the source has none and the corner radius is borrowed from the diefstal sticker."
               % (sc, ang, TXT_ANG)),
    )


# ================================================================================================ application 6: P+R poster Mandelapark
P_SYM = (100.0, 59.8)
P_SYM_SCALE = 5.964
P_LABEL = (106.7, 346.9, 270.4)
P_PILL = (201.77, 465.17, 512.96, 552.19)
P_PILL_SW = 2.1167
P_LOCK = (235.0, 473.0, 0.66)
P_NAME = (313.1, 512.2, 537.2, 27.8)
P_PRICE = (45.28, 799.98, 181.2)
P_SUFFIX = (250.5, 774.7, 67.6)
P_LABEL2 = (73.09, 862.6, 50.5)
P_TAG = (TAG[0], TAG[1])


def _cut_to_bleed(p, bleed=3.0, size=(700, 1000)):
    import pathops

    k = 1 / PT_MM
    x0, y0, x1, y1 = -bleed * k, -bleed * k, (size[0] + bleed) * k, (size[1] + bleed) * k
    page = Path([("M", x0, y0), ("L", x1, y0), ("L", x1, y1), ("L", x0, y1), ("Z",)], fill=p.fill, box=(x0, y0, x1, y1))
    return _from_pathops(pathops.op(_to_pathops(p), _to_pathops(page), pathops.PathOp.INTERSECTION), p)


def _poster_navy():
    src = printsrc.source("wtcposter")
    big = [p for p in src.paths(1, (-3000, -3000, 6000, 6000), partial=True) if p.fill == "#23398E" and (p.box[2] - p.box[0]) * PT_MM > 800][0]
    return _cut_to_bleed(big)


@application("py-app-poster-pr-mandelapark", "P+R poster Mandelapark", "poster", trim_mm=(700, 1000), source=[("wtcposter", [1])], bleed_mm=3.0,
             status="rebuilt")
def _(ctx):
    app_id = "py-app-poster-pr-mandelapark"
    d = ctx.Doc(app_id, "P+R poster Mandelapark", trim=(700, 1000), bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-light")
    n = _poster_navy()
    d.path(_pd(n), _pbox(n), fill=NAVY, gid="bleed-background", variable="background-colour", example=NAVY)
    with d.group("py-comp-symbol-pr"):
        d.place("py-comp-symbol-pr", P_SYM[0], P_SYM[1], scale=P_SYM_SCALE, strip_text=True)
        d.text(P_LABEL[0], P_LABEL[1], "P+R", P_LABEL[2], WHITE, weight=BOLD, variable="label-pr")
    with d.group("py-comp-lockup-location-garage"):
        x0, y0, x1, y1 = P_PILL
        d.rect(x0, y0, x1, y1, fill=None, rx=(y1 - y0) / 2, stroke=WHITE, sw=P_PILL_SW, gid="pill-outline")
        d.place("py-comp-lockup-location-garage", P_LOCK[0], P_LOCK[1], scale=P_LOCK[2], strip_text=True, recolor={NAVY: WHITE})
        d.text(P_NAME[0], P_NAME[1], "Parking", P_NAME[3], WHITE, weight=BOLD, variable="location-line-1")
        d.text(P_NAME[0], P_NAME[2], "Mandelapark", P_NAME[3], WHITE, weight=BOLD, variable="location-line-2")
    sc, ang, tx, ty = _bubble_fit("wtcposter", (-30, 560, 350, 990))
    with d.group("py-comp-price-bubble-speech"):
        d.uses("py-comp-price-bubble-speech")
        for dd, fill, bb in _cut_lib("py-comp-price-bubble-speech", tx, ty, sc, (-3, -3, 703, 1003), angle=ang, pre=(-408.096, 8.654)):
            d.path(dd, bb, fill=fill, gid="bubble")
        _price_texts(d, P_PRICE, P_SUFFIX, P_LABEL2)
    with d.group("py-comp-url-tag-chevron"):
        d.place("py-comp-url-tag-chevron", P_TAG[0], P_TAG[1])
    d.variables.update({"url-bold": "voordelig", "url-regular": "parkeren.nl"})
    d.guides(700, 1000)
    return dict(
        reference={"": ctx.reference("wtcposter", 1)}, template={"": d},
        omitted=[],
        copy_corrections=[],
        notes=("700 x 1000 mm, no bleed in the source (page = trim, RGB ICC). Navy field: one source path of 847 x 1127 mm (-117 / -177 to 730 / 949.5) of which only the part on the page is visible: "
               "the top and the sides run off the page, the lower left is cut by an arc, white paper below it up to x 349, a vertical edge and a pointed bottom right. The template rebuilds the visible part "
               "as a path (source path intersected with the page plus 3 mm bleed with pathops, as in the tariff panel). The reference also keeps a navy rectangle (70.8 to 644.1 x 112.5 to 383.2 mm, #233A89 "
               "against the field #23398E) that is faintly visible in the source as a slightly different blue; it is a leftover and is not in the template. "
               "P+R symbol: py-comp-symbol-pr scaled 5.964x at 100.0 / 59.8 mm, live label P+R Ubuntu Bold 270.4 mm white. Location: white outline pill 311.2 x 87.0 mm (stroke 6 pt = 2.12 mm, full round) with the garage "
               "symbol of py-comp-lockup-location-garage (white, scale 0.66, strip_text) and own live text, Ubuntu Bold 27.8 mm white (Parking / Mandelapark, baselines 512.2 and 537.2): the proportions of the library "
               "lockup do not hold here either (see the sticker). Price bubble: py-comp-price-bubble-speech at scale %.4f and rotation %.2f degrees (matches the source path), cut to the bleed at the left page edge "
               "(it sticks out 21 mm in the source); live Ubuntu Bold white, rotated %.1f degrees: '€6' 181.2 mm, ',-' 67.6 mm, 'per dag' 50.5 mm (outlined in the source, fitted by overlay; the suffix is scaled from "
               "the sticker, 1.75x). URL tag: new comp py-comp-url-tag-chevron at 458.5 / 938.4 mm (on white paper). Colours: file blue #23398E and tag #374F9C are the token navy, light aqua #78C9DC (no token) as sampled. "
               "Variables: label-pr, price, price-suffix, label, location-line-1, location-line-2, url-bold, url-regular, background-colour. Same location name and price as the sticker; "
               "the web address voordeligparkeren.nl is not the www.parkingyou.nl used elsewhere (open point for the owner). No spelling errors found. No cut contour: a poster."
               % (sc, ang, TXT_ANG)),
    )
