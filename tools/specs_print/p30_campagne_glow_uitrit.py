"""PM-137 Phase 2, module p30: Hofplein campaign panel, GLOW event sign, uitrit sign and their elements.

Sources: InfoPylonBordGoed.pdf (hofplein), Tekengebied_1.pdf (glow1), Tekengebied_4_kopie_4.pdf (glow4), 15728501-1.pdf (uitrit).
All numbers below were measured from the source PDFs (page mm, origin top left of the MediaBox). Outlined text of the
Hofplein panel and the uitrit sign is rebuilt as live Ubuntu; size, weight and origin come from fitting the Ubuntu glyph
outlines to the ink box of the outlined source glyphs (width and height agree within 1 percent unless noted).
"""
import math

import re
from pyassets import printsrc
from pyassets.apps import application
from pyassets.compose import Doc
from pyassets.core import PT_MM, TF, Group, Raw, Text, font_css, hex_of, ink_box
from pyassets.registry import crop, element

NAVY = "#1A3580"
AQUA = "#32B9CD"
LIGHT_AQUA = "#69CADA"  # CMYK 54/0/14/0, no token, kept as sampled
WHITE = "#FFFFFF"

# ------------------------------------------------------------------------------------------------ source helpers


def _grab(key, pno, box_mm):
    """The single source path inside a page box (mm)."""
    ps = printsrc.source(key).paths(pno, printsrc.box_mm(*box_mm), tol=1.0)
    assert len(ps) == 1, (key, box_mm, len(ps))
    return ps[0]


def _pd(p, dx=0.0, dy=0.0):
    """SVG path data of a source path in mm, shifted by (dx, dy)."""
    return p.d(TF(0.0, 0.0, PT_MM, dx, dy))


def _pbox(p, dx=0.0, dy=0.0):
    b = p.box
    return (b[0] * PT_MM + dx, b[1] * PT_MM + dy, b[2] * PT_MM + dx, b[3] * PT_MM + dy)


def _rtext(d, x, y, s, size, fill, angle, weight=400, italic=False, variable=None, anchor="start"):
    """Rotated live text; Doc.text() boxes ignore the rotation, so the box is replaced by the rotated ink box."""
    d.text(x, y, s, size, fill, weight=weight, italic=italic, rotate=angle, variable=variable, anchor=anchor)
    ax, ay = d._p(x, y)
    b = ink_box(s, "Ubuntu", weight, italic, size, ax, ay, 0.0, anchor)
    a = math.radians(angle)
    pts = []
    for px, py in ((b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])):
        rx, ry = px - ax, py - ay
        pts.append((ax + rx * math.cos(a) - ry * math.sin(a), ay + rx * math.sin(a) + ry * math.cos(a)))
    d.boxes[-1] = (min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts))


# ================================================================================================ GLOW pieces
# pill geometry (glow1/glow4, page mm): pill 28.294..268.706 x 253.347..296.418 (240.41 x 43.07, radius = half height),
# disc 32.54..70.38 (37.84, centred vertically, 4.25 from the left edge), label Ubuntu Bold 26.458, baseline 30.99 below the pill top.
PW, PH = 240.412, 43.071
PR = PH / 2
DISC_R = 18.92
DISC_CX = 23.17  # disc centre from the pill left edge
LABEL_SIZE = 26.458
LABEL_BASE = 30.99
LABEL_CX = {"Philips stadion": 139.573, "DLL": 131.52, "TD-gebouw": 135.545, "Evoluon": 134.727}  # centre from the pill left edge, measured per row
LABEL_CX_DEFAULT = 134.727
PITCH = 51.5  # measured 51.61 and 51.41 between the three pills (brief: 51.7)
PILL_X0 = 28.294
PILL_TOPS = (253.347, 304.958, 356.365)
# arrows and pin: offset of the glyph box from the pill top left
_ARROW_SRC = {
    "left": ("glow1", (37.0, 265.0, 66.0, 285.0), PILL_TOPS[0]),
    "up": ("glow1", (41.5, 312.0, 61.5, 340.8), PILL_TOPS[1]),
}
PIN_REL = (40.298 - PILL_X0, 312.024 - PILL_TOPS[1])


def _pill(d, x, y, label, kind="left", state="active", var=None, gid="py-comp-pill-destination"):
    """GLOW destination pill with its top left at (x, y). kind: left, up (print arrows) or pin. state: active or inactive (25 percent)."""
    attrs = {"data_state": state, "data_arrow": kind}
    mm = re.search(r"-(\d+)$", var or "")
    if mm:  # the arrow and state variables of this pill (variable names arrow-N, state-N)
        attrs["data_variable_arrow"] = f"arrow-{mm.group(1)}"
        attrs["data_variable_state"] = f"state-{mm.group(1)}"
    if state == "inactive":
        attrs["opacity"] = 0.25
    with d.group(gid, **attrs):
        d.rect(x, y, x + PW, y + PH, fill=WHITE, rx=PR, gid="pill")
        d.rect(x + DISC_CX - DISC_R, y + PR - DISC_R, x + DISC_CX + DISC_R, y + PR + DISC_R, fill=NAVY, rx=DISC_R, gid="disc")
        if kind == "pin":
            d.place("py-atom-icon-location-pin", x + PIN_REL[0], y + PIN_REL[1], scale=1.0, gid="pin")
        else:
            key, box, top = _ARROW_SRC[kind]
            p = _grab(key, 1, box)
            dx, dy = x - PILL_X0, y - top
            d.path(_pd(p, dx, dy), _pbox(p, dx, dy), fill=WHITE, gid="arrow")
        d.text(x + LABEL_CX.get(label, LABEL_CX_DEFAULT), y + LABEL_BASE, label,
               size=LABEL_SIZE, fill=NAVY, weight=700, anchor="middle", variable=var)


@element("py-atom-icon-location-pin", "Locatiepin", "atom", "icon", 1, src="glow4",
         notes="White location pin in the active Evoluon pill (Tekengebied_4_kopie_4 p1), one path with the round hole. White on transparent: view on a dark background. "
               "Printed size 21.3 x 29.8 mm.")
def _(src):
    return crop(src, 1, printsrc.box_mm(40, 311.5, 62, 342.5), texts=False)


@element("py-comp-pill-destination", "Bestemmingspil", "comp", "pill", 1, src="glow4", status="rebuilt",
         variables=("label", "arrow direction", "state"),
         notes="GLOW destination pill, active state: white stadium pill 240.4 x 43.1 mm (radius = half the height), navy disc 37.8 mm (4.25 mm from the left edge), "
               "white arrow or pin in the disc, bold navy label (Ubuntu Bold 26.46 mm, live text). Pill and disc are rebuilt with rx, the label is live text. "
               "The arrow is NOT the library py-atom-arrow-left-plain or py-atom-arrow-up-plain: the print arrow is a seven point block arrow 27.5 x 18.9 mm (head 10.3 mm deep, "
               "shaft 6.6 mm wide), the library arrow is a chevron arrow of 1:1 proportion. The print arrows (left, up) are the source paths, shifted into the pill. "
               "The pin is the atom py-atom-icon-location-pin. Shown here: label Philips stadion with arrow left. Arrow directions: left, up, pin. "
               "Inactive state: the same pill group at 25 percent opacity (print: whole group in a transparency group at 25 percent), applied in the template (variable: state). "
               "Labels are centred by eye in print (centre 131.5 to 139.6 mm from the pill edge, Philips stadion moved right); the label centre is part of the observed layout. "
               "White on transparent: view on a navy background.")
def _(src):
    d = Doc("py-comp-pill-destination", "Bestemmingspil", tight=True)
    d.uses("py-atom-icon-location-pin")
    _pill(d, 0.0, 0.0, "Philips stadion", "left", "active", var="label")
    d.variables["arrow-direction"] = "left"
    d.variables["state"] = "active"
    return d


@element("py-comp-pill-list-destinations", "Bestemmingslijst", "comp", "pill", 1, src="glow1", status="rebuilt",
         variables=("destination names", "arrow direction", "state per pill"),
         notes="Three destination pills under each other, pitch 51.5 mm (measured 51.61 and 51.41, the brief says 51.7; gap 8.4 mm). Same drawing as "
               "py-comp-pill-destination (shared construction, the labels are live text per pill, so the pill SVG itself is not placed three times). "
               "Route variant shown: Philips stadion (arrow left), DLL (arrow up), TD-gebouw (arrow up), all active. White on transparent: view on a navy background.")
def _(src):
    d = Doc("py-comp-pill-list-destinations", "Bestemmingslijst", tight=True)
    d.uses("py-comp-pill-destination", "py-atom-icon-location-pin")
    for i, (lab, kind) in enumerate((("Philips stadion", "left"), ("DLL", "up"), ("TD-gebouw", "up"))):
        _pill(d, 0.0, i * PITCH, lab, kind, "active", var=f"destination-{i + 1}")
        d.variables[f"arrow-{i + 1}"] = kind
    return d


def _glow_mark_box():
    a, b = _pbox(_grab("glow1", 1, (189, 206.5, 212.5, 230)))[:2], _pbox(_grab("glow1", 1, (85, 205.5, 187, 230.5)))[:2]
    return (min(a[0], b[0]), min(a[1], b[1]))


@element("py-atom-mark-glow", "GLOW merk", "atom", "mark", 1, src="glow1", tags=("third-party",),
         notes="Third party mark of the event GLOW: outlined wordmark (101.4 x 24.1 mm) plus the white square (22.8 mm), taken as is from Tekengebied_1 p1. "
               "Reference only, source the official file. White on transparent: view on a dark background.")
def _(src):
    return crop(src, 1, printsrc.box_mm(85, 205.5, 212.5, 230.5), texts=False)


# ================================================================================================ Hofplein pieces
# page = trim for this file (600 x 840, no bleed set in the source)
THETA = 21.8219  # rotation of the price (clockwise), from the text matrix
P0 = (377.172, 83.820)  # origin of "€7"
BUB_C = (500.756, 91.525)
BUB_R = 140.95
HEAD_X, HEAD_SIZE = 42.18, 106.25
HEAD_BASE0, HEAD_PITCH = 284.05, 90.4
URL_BASE1, URL_BASE2 = 74.01, 109.62


def _rot(x, y):
    """Point given in the price frame (origin P0, x along the text) to page mm."""
    a = math.radians(THETA)
    return (P0[0] + x * math.cos(a) - y * math.sin(a), P0[1] + x * math.sin(a) + y * math.cos(a))


def _bubble(d, price="€7", decimals=",50", unit="per dag", mark="*", var=True):
    """White circle (centre 500.8, 91.5, radius 141.0) cropped by the top right corner (incl. 3 mm bleed) plus the rotated navy price."""
    a1 = (396.192, -3.001)
    a2 = (602.939, 188.612)
    dpath = f"M{a1[0]} {a1[1]}L{a2[0]} {a1[1]}L{a2[0]} {a2[1]}A{BUB_R} {BUB_R} 0 0 1 {a1[0]} {a1[1]}Z"
    d.path(dpath, (BUB_C[0] - BUB_R, -3.001, 602.939, BUB_C[1] + BUB_R), fill=WHITE, gid="bubble")
    v = (lambda n: n) if var else (lambda n: None)
    _rtext(d, P0[0], P0[1], price, 115.18, NAVY, THETA, weight=700, italic=True, variable=v("price"))
    x2, y2 = 487.99, 128.19
    _rtext(d, x2, y2, decimals, 62.0, NAVY, THETA, weight=500, italic=True, variable=v("price-decimals"))
    ux, uy = _rot(47.845, 50.523)
    _rtext(d, ux, uy, unit, 34.17, NAVY, THETA, weight=400, italic=False, variable=v("unit"))
    mx, my = _rot(164.22, 36.41)
    _rtext(d, mx, my, mark, 11.8, NAVY, THETA, weight=400, italic=False, variable=v("footnote-mark"))


@element("py-comp-price-bubble-corner", "Prijsbel in de hoek", "comp", "bubble", 1, src="hofplein", status="rebuilt",
         variables=("price", "price decimals", "unit", "footnote mark"),
         notes="White circle (radius 141 mm) cropped by the top right corner (shape includes the 3 mm bleed), with the price rotated 21.8 degrees clockwise: "
               "live Ubuntu Bold Italic 115.18 mm for the euro and the 7, live Ubuntu Medium Italic 62 mm for the decimals. "
               "REBUILT: the text per dag and the asterisk are outlined in the source, rebuilt as live text. Measured by fitting the glyphs: per dag is upright Ubuntu Regular 34.17 mm "
               "(not Medium Italic as in the brief: only upright Regular fits the outlines in width and height), the asterisk is 11.8 mm raised 14.1 mm. "
               "In the source the white circle is a hole in the navy field (paper), here it is drawn as a white shape. "
               "Open point: the asterisk has no footnote anywhere on the panel (kept as in the source, variable footnote mark). Navy text on white.")
def _(src):
    d = Doc("py-comp-price-bubble-corner", "Prijsbel in de hoek", tight=True)
    _bubble(d)
    return d


_CHEV = (234.5, 57.0, 266.0, 104.0)
_URL_L1 = (43.12, URL_BASE1, 37.7, 700)
_URL_L2 = (41.50, URL_BASE2, 34.4, 300)


def _url(d, line1="voordelig", line2="parkeren.nl", var=True):
    v = (lambda n: n) if var else (lambda n: None)
    d.text(_URL_L1[0], _URL_L1[1], line1, size=_URL_L1[2], fill=WHITE, weight=_URL_L1[3], variable=v("url-line-1"))
    d.text(_URL_L2[0], _URL_L2[1], line2, size=_URL_L2[2], fill=WHITE, weight=_URL_L2[3], variable=v("url-line-2"))
    p = _grab("hofplein", 1, _CHEV)
    d.path(_pd(p), _pbox(p), fill=LIGHT_AQUA, gid="chevron")


@element("py-comp-url-chevron", "URL met chevron", "comp", "url", 1, src="hofplein", status="rebuilt",
         variables=("URL line 1", "URL line 2"),
         notes="Two line URL in white plus the light aqua chevron (viewer #69CADA, CMYK 54/0/14/0, no token, kept as sampled). The chevron is the source path. "
               "REBUILT: both lines are outlined in the source, rebuilt as live text. Fitted by overlay with the outlines: line 1 Ubuntu Bold 37.7 mm, "
               "line 2 Ubuntu Light 34.4 mm (Regular does not fit: the width and the height of the glyphs agree only for Light; Light is otherwise not used in print). "
               "The URL is split inside the domain as in the source (voordelig / parkeren.nl), open point. White and light aqua on transparent: view on navy.")
def _(src):
    d = Doc("py-comp-url-chevron", "URL met chevron", tight=True)
    _url(d)
    return d


HEAD_LINES = (
    (("Midden", 400, WHITE, "headline-1"),),
    (("in de stad", 400, WHITE, "headline-2"),),
    (("parkeren", 700, AQUA, "headline-3-keyword"), (",", 400, WHITE, "headline-3-punctuation")),
    (("voor een", 400, WHITE, "headline-4"),),
    (("prikkie", 700, AQUA, "headline-5-keyword"),),
)
_COMMA_X = 502.129 - ink_box(",", "Ubuntu", 400, False, HEAD_SIZE, 0, 0)[0]


def _headline(d, lines=HEAD_LINES):
    for i, segs in enumerate(lines):
        for j, (s, w, col, var) in enumerate(segs):
            x = _COMMA_X if (j == 1 and s == ",") else HEAD_X
            d.text(x, HEAD_BASE0 + i * HEAD_PITCH, s, size=HEAD_SIZE, fill=col, weight=w, variable=var)


@element("py-comp-headline-two-colour", "Kop in twee kleuren", "comp", "headline", 1, src="hofplein", status="rebuilt",
         variables=("headline words", "aqua keywords"),
         notes="Headline Midden in de stad parkeren, voor een prikkie in five lines: white Ubuntu Regular lines and aqua Ubuntu Bold keywords (parkeren, prikkie), the comma after parkeren white. "
               "REBUILT: outlined in the source, rebuilt as live text. Fitted by overlay: size 106.25 mm for all lines (ink height of the M is 73.6 mm = 0.693 em; the 78.1 mm of the "
               "brief is the height of the i with dot), line pitch 90.4 mm, left origin 42.2 mm. Segments are variables (headline-N, keyword segments headline-N-keyword are the aqua ones). "
               "White and aqua on transparent: view on navy.")
def _(src):
    d = Doc("py-comp-headline-two-colour", "Kop in twee kleuren", tight=True)
    _headline(d)
    return d


@element("py-atom-symbol-p-garage-outline", "P in garageomtrek", "atom", "symbol", 1, src="hofplein",
         notes="Outline house (garage) with the letter P, two paths, navy (normalised from the print blue to #1A3580). Extracted from InfoPylonBordGoed p1 "
               "next to Parking Hofplein, 101.8 x 94.5 mm. Differs from py-atom-symbol-p-roof. Navy: view on a light background.")
def _(src):
    return crop(src, 1, printsrc.box_mm(130, 725, 236, 824), texts=False)



def _lockup(d, x, y, line1="Parking", line2="Hofplein"):
    """Symbol with its top left at (x, y) plus the two line name (source: symbol 132.1, 727.4; name origin 272.19, baselines 764.9 and 811.57)."""
    with d.group("py-atom-symbol-p-garage-outline"):
        d.place("py-atom-symbol-p-garage-outline", x, y, scale=1.0)
    nx = x + (272.19 - 132.1)
    d.text(nx, y + (764.9 - 727.4), line1, size=46.7, fill=NAVY, weight=700, variable="location-line-1")
    d.text(nx, y + (811.57 - 727.4), line2, size=46.7, fill=NAVY, weight=700, variable="location-line-2")


@element("py-comp-lockup-location-garage", "Garagelockup", "comp", "lockup", 1, src="hofplein", status="rebuilt",
         variables=("location name line 1", "location name line 2"),
         notes="Garage symbol (py-atom-symbol-p-garage-outline) plus the two line bold navy name. REBUILT: the name is outlined in the source, rebuilt as live "
               "Ubuntu Bold 46.7 mm (fitted by overlay: widths 46.5 and 46.8 mm, ink height 46.7 mm), baselines 46.7 mm apart. "
               "Symbol 101.8 mm wide, name starts 140 mm right of the symbol edge. Navy: view on a light background.")
def _(src):
    d = Doc("py-comp-lockup-location-garage", "Garagelockup", tight=True)
    d.uses("py-atom-symbol-p-garage-outline")
    _lockup(d, 0.0, 0.0)
    return d


# ================================================================================================ uitrit extra variant
@element("py-comp-route-module-separator-uitrit", "Scheidingsboog uitrit (dunne lijn)", "comp", "route-module", 1, src="uitrit",
         notes="Aqua separator arc as printed on the uitrit sign: stroke 3.0 mm, chord 215.5 mm, depth 44.6 mm. Extracted as a variant: the shape is the same as "
               "py-comp-route-module-separator (depth to chord ratio 0.207), but at the size of the uitrit sign the library arc would have a stroke of 5.3 mm instead of 3.0 mm. "
               "Stroke only, to be placed on navy.")
def _(src):
    return crop(src, 1, printsrc.box_mm(268, 25, 317, 245), texts=False)


# ================================================================================================ applications
HOF_TRIM = (600, 840)


@application("py-app-panel-campagne-hofplein", "Campagnebord Parking Hofplein", "panel", trim_mm=HOF_TRIM, source=[("hofplein", [1])], bleed_mm=3.0,
             status="rebuilt")
def _(ctx):
    src = printsrc.source("hofplein")
    # price spans are live but rotated: Source.texts() writes them unrotated, so they are skipped and added back rotated
    extra = []
    for s in src.spans(1):
        if s["text"] in ("€7", ",50"):
            fam, w, it = font_css(s["font"])
            org = s["origin"]
            t = Text(org[0], org[1], s["text"], fam, w, it, s["size"], "#" + "%06X" % s["color"], 0.0, box=(0, 0, 0, 0))
            xml = t.svg(TF(0.0, 0.0, PT_MM, 0.0, 0.0), None)
            ox, oy = org[0] * PT_MM, org[1] * PT_MM
            xml = xml.replace("<text ", f'<text transform="rotate({THETA} {ox:.3f} {oy:.3f})" ', 1)
            extra.append(Raw(xml, box=(0, 0, 0, 0)))
    ref = ctx.reference("hofplein", 1, skip_text=lambda t: t in ("€7", ",50"), extra=extra)

    d = ctx.Doc("py-app-panel-campagne-hofplein", "Campagnebord Parking Hofplein", trim=HOF_TRIM, bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", "py-tok-type-ubuntu-regular", "py-tok-type-ubuntu-bold",
           "py-tok-type-ubuntu-light", "py-tok-type-ubuntu-bold-italic", "py-tok-type-ubuntu-medium-italic")
    d.rect(-3, -3, 603, 714.3, fill=NAVY, gid="bleed-background", variable="background-colour", example=NAVY)
    with d.group("py-comp-price-bubble-corner"):
        _bubble(d)
    with d.group("py-comp-url-chevron"):
        _url(d)
    d.uses("py-comp-url-chevron", "py-comp-price-bubble-corner", "py-comp-headline-two-colour", "py-comp-lockup-location-garage")
    with d.group("py-comp-headline-two-colour"):
        _headline(d)
    with d.group("py-comp-lockup-location-garage"):
        _lockup(d, 132.1, 727.4)
    d.guides(*HOF_TRIM)
    return dict(
        reference={"": ref}, template={"": d},
        omitted=[],
        copy_corrections=[],
        notes=("Navy field 600 x 714.3 mm (runs 3 mm into the bleed at top, left and right), the lower 125.7 mm is white paper (no ink) with the garage lockup. "
               "The white price circle is a hole in the navy field in the source (paper shows through); the template draws it as a white shape. "
               "Reference keeps all outlines as extracted paths (headline, url, per dag, name); only the price is live text, rotated 21.8 degrees. "
               "Template: headline, url, price, unit and name are live Ubuntu text with data-variable. "
               "OPEN POINT (copy): the asterisk after per dag has no footnote anywhere on the panel; kept as in the source (variable footnote-mark). "
               "OPEN POINT (copy): the URL is split inside the domain (voordelig / parkeren.nl), kept as in the source. "
               "Fitted fonts (measured by overlay with the outlines): headline Ubuntu Regular/Bold 106.25 mm, URL line 1 Bold 37.7 mm, URL line 2 Light 34.4 mm, "
               "per dag upright Regular 34.17 mm, name Bold 46.7 mm. The Light weight and the upright Regular (instead of Medium Italic) differ from the brief and from the "
               "observed rule that Light is not used: owner to confirm. "
               "Blue in the source is CMYK 100/83/0/17 (equal to the token), light aqua chevron kept as sampled #69CADA."),
    )


def _glow_template(ctx, app_id, rows):
    d = ctx.Doc(app_id, "Evenementbord Parkeren GLOW", trim=(297, 420), bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-bold")
    d.rect(-3, -3, 300, 423, fill=NAVY, gid="bleed-background", variable="background-colour", example=NAVY)
    s = 173.442 / 91.722  # P atom: Ubuntu Bold 91.722 mm scaled to the 173.442 mm of the sign
    with d.group("py-atom-symbol-p-plain"):
        d.place("py-atom-symbol-p-plain", 95.699 + 7.338 * s, 150.521 - 64.297 * s, scale=s)
    d.text(148.5, 198.439, "Parkeren", size=35.278, fill=WHITE, weight=700, anchor="middle", gid="title")
    gx, gy = _glow_mark_box()
    with d.group("py-atom-mark-glow"):
        d.place("py-atom-mark-glow", gx, gy, scale=1.0)
    with d.group("py-comp-pill-list-destinations"):
        for i, (lab, kind, state) in enumerate(rows):
            _pill(d, PILL_X0, PILL_TOPS[0] + i * PITCH, lab, kind, state, var=f"destination-{i + 1}")
            d.variables[f"arrow-{i + 1}"] = kind
            d.variables[f"state-{i + 1}"] = state
    d.uses("py-comp-pill-destination", "py-comp-pill-list-destinations", "py-atom-icon-location-pin")
    d.guides(297, 420)
    return d


def _glow_omit(p):
    """Off-page copies of the navy beeldmerk shape (blue on blue, partly on the page): any navy path sticking out of the page."""
    b = [v * PT_MM for v in p.box]
    return p.fill == "#174797" and (b[0] < -1 or b[1] < -1 or b[2] > 298 or b[3] > 421)


GLOW_ROWS_ROUTE = (("Philips stadion", "left", "active"), ("DLL", "up", "active"), ("TD-gebouw", "up", "active"))
GLOW_ROWS_DEST = (("Philips stadion", "left", "inactive"), ("Evoluon", "pin", "active"), ("TD-gebouw", "left", "inactive"))


@application("py-app-event-sign-glow", "Evenementbord Parkeren GLOW", "event-sign", trim_mm=(297, 420), source=[("glow1", [1]), ("glow4", [1])],
             bleed_mm=3.0, variants=("route", "bestemming"), status="rebuilt")
def _(ctx):
    return dict(
        reference={"route": ctx.reference("glow1", 1, variant="route", omit=_glow_omit),
                   "bestemming": ctx.reference("glow4", 1, variant="bestemming", omit=_glow_omit)},
        template={"route": _glow_template(ctx, "py-app-event-sign-glow", GLOW_ROWS_ROUTE),
                  "bestemming": _glow_template(ctx, "py-app-event-sign-glow", GLOW_ROWS_DEST)},
        omitted=["route (Tekengebied_1): 1 off-page copy of the navy beeldmerk shape (x 256 to 653 mm, y 408 to 887 mm, blue on blue, partly on the page)",
                 "bestemming (Tekengebied_4_kopie_4): 4 off-page copies of the navy beeldmerk shape (x -352 to 653 mm, y -19 to 887 mm, blue on blue, partly on the page)"],
        copy_corrections=[],
        notes=("A3 297 x 420 mm, no bleed in the source (background is exactly the trim), template adds 3 mm bleed. Navy background is the token #1A3580 "
               "(the source GLOW blue is CMYK 100/84.4/5.5/0.4, viewer #174797). White P is py-atom-symbol-p-plain scaled from 91.7 to 173.44 mm; Parkeren is Ubuntu Bold 35.28 mm. "
               "GLOW is the third party mark (reference only, source the official file). Pills: route = three active pills (Philips stadion arrow left, DLL arrow up, TD-gebouw arrow up); "
               "bestemming = Evoluon active with pin, Philips stadion and TD-gebouw inactive (25 percent, arrow left in print). Print arrows differ from the library arrows, see "
               "py-comp-pill-destination. Source details: the DLL label has a trailing space in the file (DLL and a space), label centres are set by eye per pill, pill pitch measured 51.61 and "
               "51.41 mm (template uses 51.5). Variables: destination-N, arrow-N (left, up, pin), state-N (active, inactive)."),
    )


UIT_TRIM = (800, 250)
UIT_CAR = (38.19, 55.457, 190.117 / 27.988)
UIT_CIRCLE = (564.626, 17.382, 215.469 / 169.947)


@application("py-app-sign-uitrit", "Uitritbord", "sign", trim_mm=UIT_TRIM, source=[("uitrit", [1])], bleed_mm=10.0, status="rebuilt",
             cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": None, "ends": "elliptical, rx 133.3 mm, ry 125 mm",
                          "note": "source contour 799.6 x 249.6 mm, magenta 1 pt stroke on the spot ThruCut"})
def _(ctx):
    src = printsrc.source("uitrit")
    # the contour is the stroke path of width 1 pt (the only stroke of that width and colour); the aqua arc is the other stroke
    cut = [p for p in src.paths(1, (-100, -100, 3000, 1000), partial=True) if p.stroke and abs(p.width - 1.0) < 0.05]
    assert len(cut) == 1
    ref = ctx.reference("uitrit", 1, omit=lambda p: bool(p.stroke and abs(p.width - 1.0) < 0.05),
                        extra=[Group(items=cut, opacity=1.0, gid="cut-contour")])

    d = ctx.Doc("py-app-sign-uitrit", "Uitritbord", trim=UIT_TRIM, bleed=10.0)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", "py-tok-type-ubuntu-bold")
    d.rect(-10, -10, 810, 260, fill=NAVY, rx=143.3, ry=135, gid="bleed-background", variable="background-colour", example=NAVY)
    with d.group("py-atom-picto-car"):
        d.place("py-atom-picto-car", UIT_CAR[0], UIT_CAR[1], scale=UIT_CAR[2], recolor={NAVY: WHITE})
    with d.group("py-comp-route-module-separator-uitrit"):
        d.place("py-comp-route-module-separator-uitrit", 259.995 - 1.5, 27.384 - 10 - 1.5, scale=1.0)
    d.text(293.12, 182.29, "Uit", size=167.84, fill=WHITE, weight=700, variable="destination-word", gid="destination")
    with d.group("py-atom-arrow-up-circle"):
        d.place("py-atom-arrow-up-circle", UIT_CIRCLE[0], UIT_CIRCLE[1], scale=UIT_CIRCLE[2])
    d.cut_contour(0, 0, 800, 250, rx=133.3, ry=125)
    d.guides(*UIT_TRIM)
    return dict(
        reference={"": ref}, template={"": d},
        omitted=[],
        copy_corrections=[],
        notes=("800 x 250 mm trim, 10 mm bleed (page 820 x 270). Navy stadium with elliptical ends (rx 133.3, ry 125 mm); the template draws one navy shape into the bleed "
               "(rx 143.3, ry 135 mm, the 10 mm offset of the trim shape; the source bleed shape is 820 x 273.5 mm and sticks 1.7 mm out of the page). "
               "Cut contour: ThruCut, 1 pt magenta stroke, 0.2 mm inside the trim, elliptical ends (the source contour is the stroke path, kept in the reference as group cut-contour). "
               "Library check: py-atom-picto-car matches the print car (same proportion, scale 6.79) and py-atom-arrow-up-circle matches the print circle and arrow (scale 1.268, arrow share 0.706). "
               "The library arc py-comp-route-module-separator has the same shape but would print with a 5.3 mm stroke instead of 3.0 mm, so the print arc is extracted as the variant "
               "py-comp-route-module-separator-uitrit (py-atom-shape-separator-arc is the handbook illustration in grey and navy, not the aqua arc). "
               "Uit is live Ubuntu Bold 167.84 mm, white (fitted by overlay, width and height agree). Blue in the source is CMYK 100/92.5/19.2/5.9 (the most drifted blue), "
               "aqua CMYK 67.8/3.1/19.2/0; the template uses the tokens #1A3580 and #32B9CD."),
    )
