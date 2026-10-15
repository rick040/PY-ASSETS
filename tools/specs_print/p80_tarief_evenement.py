"""PM-137 module p80: tariff panel for events (TariefConcerten.pdf, 700 x 1000 mm, RGB ICC, no bleed in the source).

All numbers were measured from the source (page mm, origin top left of the MediaBox; page = trim).
Text in the source is live Ubuntu, so nothing is outlined or fitted: size, weight and origin are read from the spans.
"""
import math

from pyassets import printsrc
from pyassets.apps import application
from pyassets.compose import Doc
from pyassets.core import PT_MM, TF, Path, Raw, Text, _from_pathops, _to_pathops, font_css, ink_box
from pyassets.registry import crop, element

KEY = "tarief"
NAVY = "#1A3580"
SRC_NAVY = "#23398E"  # navy of the file (drift, RGB ICC)
BUBBLE = "#78C9DC"  # light aqua, no token, kept as sampled
WHITE = "#FFFFFF"
RING_STROKE_SRC = "#203B8B"

box = printsrc.box_mm
TRIM = (700, 1000)

# ------------------------------------------------------------------------------------------------ measured values
# calendar (first one): body 105.2..248.4 x 617.5..728.8, header 585.6..608.3, rings reach up to 573.2
CAL_SRC_BOX = (105.0, 573.0, 248.6, 729.0)
CAL_X = (105.2, 281.0, 456.9)  # body left edge of the three calendars (pitch 175.8 / 175.9)
CAL_BODY_TOP = 617.5
DAY_SIZE, MONTH_SIZE = 64.51, 23.04
DAY_BASE_REL = 678.8 - CAL_BODY_TOP  # baseline of the day number below the body top
MONTH_BASE_REL = 706.5 - CAL_BODY_TOP
CAL_W = 143.2

# price bubble (speech bubble), text rotated -6.708 degrees (matrix 0.99315, -0.11681)
ANGLE = math.degrees(math.atan2(-0.11681109666824341, 0.9931541681289673))
PRICE_ORG = (434.69, 192.97)
PRICE_SIZE = 146.52
LABEL_ORG = (481.01, 241.18)
LABEL_SIZE = 35.07
BUBBLE_BOX = (406.0, -11.0, 712.0, 345.0)


def _grab(box_mm, tol=1.0):
    ps = printsrc.source(KEY).paths(1, box(*box_mm), tol=tol)
    assert len(ps) == 1, (box_mm, len(ps))
    return ps[0]


def _pd(p, dx=0.0, dy=0.0):
    return p.d(TF(0.0, 0.0, PT_MM, dx, dy))


def _pbox(p, dx=0.0, dy=0.0):
    b = p.box
    return (b[0] * PT_MM + dx, b[1] * PT_MM + dy, b[2] * PT_MM + dx, b[3] * PT_MM + dy)


def _rtext(d, x, y, s, size, fill, angle, weight=400, variable=None, anchor="start"):
    """Rotated live text; Doc.text() boxes ignore the rotation, so the box is replaced by the rotated ink box."""
    d.text(x, y, s, size, fill, weight=weight, rotate=angle, variable=variable, anchor=anchor)
    ax, ay = d._p(x, y)
    b = ink_box(s, "Ubuntu", weight, False, size, ax, ay, 0.0, anchor)
    a = math.radians(angle)
    pts = []
    for px, py in ((b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])):
        rx, ry = px - ax, py - ay
        pts.append((ax + rx * math.cos(a) - ry * math.sin(a), ay + rx * math.sin(a) + ry * math.cos(a)))
    d.boxes[-1] = (min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts))


# ================================================================================================ elements
@element("py-atom-icon-calendar", "Kalendericoon", "atom", "icon", 1, src=KEY,
         notes="White calendar icon of the tariff panel (TariefConcerten p1, first of three): white body 143.2 x 111.3 mm with rounded corners, white header 143.2 x 22.7 mm "
               "(a 1 mm gap between header and body) and two binder rings (white fill, 4 pt = 1.41 mm stroke in the file navy #203B8B, normalised to the token #1A3580). "
               "Extracted as is, four paths, no text. White on transparent: view on a navy background (the ring strokes disappear on navy, as in print).")
def _(src):
    return crop(src, 1, box(*CAL_SRC_BOX), texts=False, recolor={RING_STROKE_SRC: NAVY})


def _calendar(d, x, y, day, month, var_day="day", var_month="month", gid=None):
    """Calendar icon whose body top left is at (x, y) (page mm), with the day and month centred on the body."""
    ax, ay = x + AT_OFF[0], y + AT_OFF[1]
    d.place("py-atom-icon-calendar", ax, ay, scale=1.0)
    cx = x + CAL_W / 2
    d.text(cx, y + DAY_BASE_REL, day, DAY_SIZE, NAVY, weight=500, anchor="middle", variable=var_day)
    d.text(cx, y + MONTH_BASE_REL, month, MONTH_SIZE, NAVY, weight=400, anchor="middle", variable=var_month)


AT_OFF = (0.0, 572.5 - 617.5)  # atom ink box top (ring stroke included) 45.0 mm above the body top


@element("py-comp-calendar-date", "Kalender met datum", "comp", "icon", 1, src=KEY, status="rebuilt", variables=("day", "month"),
         notes="py-atom-icon-calendar with the date as live Ubuntu text, navy (token #1A3580), both centred on the body width: day Ubuntu Medium 64.51 mm "
               "(baseline 61.3 mm below the top of the body), month Ubuntu Regular 23.04 mm (baseline 89.0 mm below the top of the body). "
               "Rebuilt: composed from the library atom plus new live text. In the source the first calendar (20 juni) has its text 3.3 mm left of the centre "
               "(calendars 2 and 3 are centred), the component centres all three. Shown: 20 juni. Navy text on a white icon: view on a navy background "
               "(the date is then navy on white).")
def _(src):
    d = Doc("py-comp-calendar-date", "Kalender met datum", tight=True)
    _calendar(d, 0.0, 0.0, "20", "juni")
    return d


def _bubble(d, price="€20", label="inrijdtarief"):
    """Light aqua speech bubble (source path, whole shape, sticks out of the page at top and right) plus the two rotated white texts."""
    p = _grab(BUBBLE_BOX, tol=2.0)
    d.path(_pd(p), _pbox(p), fill=BUBBLE, gid="bubble")
    _rtext(d, *PRICE_ORG, price, PRICE_SIZE, WHITE, ANGLE, weight=700, variable="price")
    _rtext(d, *LABEL_ORG, label, LABEL_SIZE, WHITE, ANGLE, weight=400, variable="label")


@element("py-comp-price-bubble-speech", "Prijsbel spraakwolk", "comp", "bubble", 1, src=KEY, status="rebuilt", variables=("price", "label"),
         notes="Light aqua speech bubble (viewer #78C9DC in this RGB file, no token, kept as sampled) 301 x 351 mm with a rounded pointer at the bottom right "
               "(source path, whole shape: in the source it is cropped by the page at the top and the right edge, 8.7 mm and 9.1 mm stick out). "
               "Texts rotated 6.71 degrees counter clockwise (matrix 0.9932 / -0.1168, measured from the spans, both texts share the angle): "
               "price live Ubuntu Bold 146.52 mm white (origin 434.7 / 193.0 on the page), label live Ubuntu Regular 35.07 mm white. "
               "REBUILT: shape is the source path, the text is rebuilt as live text with the measured angle (the source text is live too, "
               "but rotated text is written by this module). Not py-comp-price-bubble-corner (white circle with navy price). White text on light aqua.")
def _(src):
    d = Doc("py-comp-price-bubble-speech", "Prijsbel spraakwolk", tight=True)
    _bubble(d)
    return d


@element("py-atom-mark-live-at-philips-stadium", "Merk Live at Philips Stadium", "atom", "mark", 1, src=KEY, tags=("third-party",),
         notes="Third party mark of the event Live at Philips Stadium: 26 outlined navy paths (letters, two stars, two chevron brackets) about 187 x 74 mm, taken as is from "
               "TariefConcerten p1. The navy of the file (#23398E) is normalised to the token #1A3580. Reference only, source the official file. "
               "Navy: view on a light background.")
def _(src):
    return crop(src, 1, box(47.0, 900.0, 236.0, 976.5), texts=False)


# ================================================================================================ application
def _navy_shape():
    """The huge navy speech bubble shape of the source (956 x 1272 mm, mostly off the page) cut to the page plus 3 mm bleed."""
    import pathops

    src = printsrc.source(KEY)
    big = [p for p in src.paths(1, (-3000, -3000, 6000, 6000), partial=True) if p.fill == SRC_NAVY and (p.box[2] - p.box[0]) * PT_MM > 900][0]
    k = 1 / PT_MM
    x0, y0, x1, y1 = -3 * k, -3 * k, 703 * k, 1003 * k
    page = Path([("M", x0, y0), ("L", x1, y0), ("L", x1, y1), ("L", x0, y1), ("Z",)], fill=big.fill, box=(x0, y0, x1, y1))
    return _from_pathops(pathops.op(_to_pathops(big), _to_pathops(page), pathops.PathOp.INTERSECTION), big)


def _lockup_args():
    return dict(x=58.7, y=58.1)


LOGO = (58.7, 58.1, 73.0 / 28.949)  # beeldmerk top left and scale of the library logo (beeldmerk 60.6 x 73.0 mm in the source)

HEAD = (56.1, 336.1, 111.9)
BODY = ((56.1, 443.5, "Aangepast inrijdtarief"), (56.1, 497.2, "op de volgende data:"))
BODY_SIZE = 55.95


def _template(ctx, app_id):
    d = ctx.Doc(app_id, "Tariefbord evenement", trim=TRIM, bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-medium", "py-tok-type-ubuntu-regular")
    n = _navy_shape()
    d.path(_pd(n), _pbox(n), fill=NAVY, gid="bleed-background")
    d.variables["background-colour"] = NAVY
    with d.group("py-comp-tagline-lockup"):
        d.place("py-comp-tagline-lockup", LOGO[0], LOGO[1], scale=LOGO[2])
    with d.group("py-comp-price-bubble-speech"):
        _bubble(d)
    d.uses("py-comp-price-bubble-speech", "py-comp-calendar-date", "py-atom-icon-calendar", "py-atom-mark-live-at-philips-stadium")
    d.text(HEAD[0], HEAD[1], "Let op!", HEAD[2], WHITE, weight=700, variable="headline")
    d.text(BODY[0][0], BODY[0][1], BODY[0][2], BODY_SIZE, WHITE, weight=500, variable="body-line-1")
    d.text(BODY[1][0], BODY[1][1], BODY[1][2], BODY_SIZE, WHITE, weight=500, variable="body-line-2")
    for i, (x, day) in enumerate(zip(CAL_X, ("20", "26", "27"))):
        with d.group("py-comp-calendar-date"):
            _calendar(d, x, CAL_BODY_TOP, day, "juni", f"day-{i + 1}", f"month-{i + 1}")
    with d.group("py-atom-mark-live-at-philips-stadium"):
        m = _mark_box()
        d.place("py-atom-mark-live-at-philips-stadium", m[0], m[1], scale=1.0)
    d.guides(*TRIM)
    return d


def _mark_box():
    items = crop(printsrc.source(KEY), 1, box(47.0, 900.0, 236.0, 976.5), texts=False)
    b = [p for p in items if isinstance(p, Path)]
    return (min(p.box[0] for p in b) * PT_MM, min(p.box[1] for p in b) * PT_MM)


@application("py-app-panel-tarief-evenement", "Tariefbord evenement (aangepast inrijdtarief)", "panel", trim_mm=TRIM, source=[(KEY, [1])], bleed_mm=3.0,
             status="rebuilt")
def _(ctx):
    src = printsrc.source(KEY)
    # the two rotated spans are live in the source, Source.texts() writes them unrotated: skip and add back rotated
    extra = []
    for s in src.spans(1):
        if s["text"].strip() in ("€20", "inrijdtarief"):
            fam, w, it = font_css(s["font"])
            org = s["origin"]
            t = Text(org[0], org[1], s["text"], fam, w, it, s["size"], "#" + "%06X" % s["color"], 0.0, box=(0, 0, 0, 0))
            xml = t.svg(TF(0.0, 0.0, PT_MM, 0.0, 0.0), None)
            ox, oy = org[0] * PT_MM, org[1] * PT_MM
            xml = xml.replace("<text ", f'<text transform="rotate({ANGLE:.3f} {ox:.3f} {oy:.3f})" ', 1)
            extra.append(Raw(xml, box=(0, 0, 0, 0)))
    ref = ctx.reference(KEY, 1, skip_text=lambda t: t.strip() in ("€20", "inrijdtarief"), extra=extra)
    d = _template(ctx, "py-app-panel-tarief-evenement")
    return dict(reference={"": ref}, template={"": d}, omitted=[], copy_corrections=[], notes="")
