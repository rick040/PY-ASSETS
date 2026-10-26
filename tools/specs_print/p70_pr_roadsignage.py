"""PM-137 follow-up, module p70: P+R road sign for the closed A20 (PR_RoadSignage.pdf, A4, RGB ICC) and its elements.

Source key "pr", page mm = trim (210 x 297, no bleed set). Measured with tools/print_probe.py (page mm, origin top left):
navy field 0..210 wide, bottom at 241.35 with corner radius 17.93 (the top of the field overshoots the page to y -65.2),
P+R bars 88.0 mm wide at x 60.6 (top bar y 11.1 to 19.9, bottom bar y 65.3 to 73.3, outer corner radius 6.68), "A20 dicht?" Ubuntu Medium
24.69 mm baseline 113.9, divider white 4 pt at y 126.5 from x 7 to 203, body Ubuntu 22.22 mm centred on x 105, baselines 157.5, 184.2, 210.8.
"""
from pyassets import printsrc
from pyassets.apps import application
from pyassets.compose import Doc, text_width
from pyassets.core import PT_MM, TF, COLOR_NORMALISE
from pyassets.registry import crop, element

NAVY = "#1A3580"   # py-tok-color-blauw
AQUA = "#32B9CD"   # py-tok-color-aqua
WHITE = "#FFFFFF"  # py-tok-color-wit

TRIM = (210.0, 297.0)
CX = 105.0
FIELD_BOTTOM = 241.35   # page mm, 684.133 pt
FIELD_R = 17.925        # 50.811 pt
BAR_R = 6.68            # 18.94 pt outer corner radius of the P+R bars
SYM_X, SYM_Y = 60.592, 11.073
LABEL_ORIGIN, LABEL_BASE, LABEL_SIZE = 61.722, 59.198, 45.334
ZHB_BOX = (14.0, 246.0, 81.0, 282.0)
HEAD_BASE, HEAD_SIZE = 113.878, 24.694
BODY_SIZE, BODY_BASE = 22.225, (157.482, 184.152, 210.822)
LINE1_TRACK = -0.1  # the source sets 'Parkeer nu ' with letter-spacing -0.1 mm (about -4.5/1000 em); the other lines have none
DIV_Y, DIV_X0, DIV_X1, DIV_W = 126.5, 7.0, 203.0, 1.41


def _grab(box_mm):
    ps = printsrc.source("pr").paths(1, printsrc.box_mm(*box_mm), tol=1.0)
    assert len(ps) == 1, (box_mm, len(ps))
    return ps[0]


def _pd(p):
    return p.d(TF(0.0, 0.0, PT_MM, 0.0, 0.0))


def _pbox(p):
    b = p.box
    return (b[0] * PT_MM, b[1] * PT_MM, b[2] * PT_MM, b[3] * PT_MM)


# ================================================================================================ elements
@element("py-atom-partner-zuid-holland-bereikbaar", "Partner Zuid-Holland Bereikbaar", "atom", "partner", 1, src="pr",
         tags=("third-party",), status="extracted",
         notes="Third party logo of Zuid-Holland Bereikbaar (arcs in yellow, magenta, green and blue plus the letters Zuid Holland Bereikbaar), 63.9 x 33.0 mm, "
               "all 22 paths as printed on PR_RoadSignage p1, bottom left. Own colours kept, NOT normalised: blue #213A8F (the RGB print blue of the sign, "
               "a drift of PY-Blauw, here the partner blue), green #72A32D, yellow #F9D900, magenta #E5007D. Reference only, source the official file. "
               "Drawn for a white ground.")
def _(src):
    # the partner blue #213A8F is on the print normalise list (it is a PY drift blue); a partner mark keeps its own colours
    saved = {k: COLOR_NORMALISE.pop(k) for k in ("#213A8F",) if k in COLOR_NORMALISE}
    try:
        return crop(src, 1, printsrc.box_mm(*ZHB_BOX), texts=False)
    finally:
        COLOR_NORMALISE.update(saved)


def _bar_paths(d):
    """The two white bars, source paths in page mm."""
    top = _grab((60.0, 10.5, 149.2, 20.5))
    bot = _grab((60.0, 64.8, 149.2, 74.0))
    d.path(_pd(top), _pbox(top), fill=WHITE, gid="bar-top")
    d.path(_pd(bot), _pbox(bot), fill=WHITE, gid="bar-bottom")


def _symbol(d, label_var="label"):
    _bar_paths(d)
    # start anchored at the measured origin: text-anchor middle is laid out 1.4 mm off by cairosvg for this text
    d.text(LABEL_ORIGIN, LABEL_BASE, "P+R", size=LABEL_SIZE, fill=WHITE, weight=700, variable=label_var, gid="label")


@element("py-comp-symbol-pr", "P+R symbool", "comp", "symbol", 1, src="pr", status="rebuilt", variables=("label",),
         notes="P+R symbol of the road sign: two white bars 88.0 mm wide (top 8.8 mm high with rounded top corners, bottom 8.0 mm high with rounded bottom corners, "
               "outer corner radius 6.68 mm; both are the source paths) with the label P+R between them as live text, Ubuntu Bold 45.33 mm white "
               "(centred between the bars, 61.7 mm from the left edge of the page in the source). REBUILT: the bars are extracted, the text is live (variable label). "
               "Overall 88.0 x 62.2 mm. White on transparent: view on a navy background.")
def _(src):
    d = Doc("py-comp-symbol-pr", "P+R symbool", tight=True)
    _symbol(d)
    return d


# ================================================================================================ application
def _field_path(bleed):
    """Navy field: top and sides run into the bleed, the bottom edge and its two rounded corners (radius 17.925, centres at x 17.925 and 192.075)
    are the trim shape as in the source (the bottom edge is inside the page, so it gets no bleed offset)."""
    r, yb, w = FIELD_R, FIELD_BOTTOM, TRIM[0]
    x0, x1 = -bleed, w + bleed
    return (f"M{x0} {-bleed}H{x1}V{yb - r:.3f}H{w}A{r} {r} 0 0 1 {w - r:.3f} {yb}H{r}A{r} {r} 0 0 1 0 {yb - r:.3f}H{x0}Z"), (x0, -bleed, x1, yb)


def _logo_box():
    """Beeldmerk of the source logo (the only #273A7C shape of that size): top left and height in page mm."""
    ps = printsrc.source("pr").paths(1, printsrc.box_mm(119.5, 258.3, 138.5, 280.6), tol=1.0)
    p = max(ps, key=lambda q: (q.box[2] - q.box[0]) * (q.box[3] - q.box[1]))
    b = _pbox(p)
    return b[0], b[1], b[3] - b[1]


def _zhb_origin():
    ps = printsrc.source("pr").paths(1, printsrc.box_mm(*ZHB_BOX), tol=1.0)
    bs = [_pbox(p) for p in ps]
    return min(b[0] for b in bs), min(b[1] for b in bs)


def _body(d):
    """Three centred lines of live text; keywords in bold aqua. Pieces are start anchored from the computed centred width."""
    lines = (
        ((("Parkeer nu ", 400, WHITE, "body-line-1"), ("tijdelijk", 700, AQUA, "keyword-1")), BODY_BASE[0]),
        ((("gratis", 700, AQUA, "keyword-2"), (" op P+R", 400, WHITE, "body-line-2")), BODY_BASE[1]),
        ((("Schiedam", 400, WHITE, "city"), (".", 400, WHITE, "punctuation")), BODY_BASE[2]),
    )
    for pieces, base in lines:
        total = sum(text_width(s, BODY_SIZE, w) for s, w, _, _ in pieces)
        x = CX - total / 2
        for s, w, col, var in pieces:
            if var == "keyword-1":
                x = 120.826  # measured origin in the source
            elif var == "body-line-1":
                x = 7.323
            sp = LINE1_TRACK if var == "body-line-1" else 0.0
            d.text(x, base, s, size=BODY_SIZE, fill=col, weight=w, spacing=sp, variable=var)
            x += text_width(s, BODY_SIZE, w, spacing=sp)


@application("py-app-sign-pr-gratis-a20", "P+R bord A20 dicht, tijdelijk gratis", "sign", trim_mm=TRIM, source=[("pr", [1])], bleed_mm=3.0,
             status="rebuilt")
def _(ctx):
    d = ctx.Doc("py-app-sign-pr-gratis-a20", "P+R bord A20 dicht, tijdelijk gratis", trim=TRIM, bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", "py-tok-type-ubuntu-regular", "py-tok-type-ubuntu-medium",
           "py-tok-type-ubuntu-bold", "py-atom-line-divider")
    dp, box = _field_path(3.0)
    with d.group("bleed-background", data_variable="background-colour"):
        d.path(dp, box, fill=NAVY, gid="field")
    d.variables["background-colour"] = NAVY
    with d.group("py-comp-symbol-pr"):
        d.place("py-comp-symbol-pr", SYM_X, SYM_Y, scale=1.0)
    d.text(45.475, HEAD_BASE, "A20 dicht?", size=HEAD_SIZE, fill=WHITE, weight=500, variable="headline")
    with d.group("py-atom-line-divider"):
        d.line(DIV_X0, DIV_Y, DIV_X1, DIV_Y, WHITE, DIV_W, gid="divider")
    with d.group("variables"):
        _body(d)
    zx, zy = _zhb_origin()
    with d.group("py-atom-partner-zuid-holland-bereikbaar"):
        d.place("py-atom-partner-zuid-holland-bereikbaar", zx, zy, scale=1.0)
    lx, ly, lh = _logo_box()
    with d.group("py-comp-lockup-logo-tagline-color"):
        d.place("py-comp-lockup-logo-tagline-color", lx, ly, h=lh)  # the lockup is as high as its beeldmerk (28.949 mm at scale 1)
    d.guides(*TRIM)
    return dict(
        reference={"": ctx.reference("pr", 1)}, template={"": d},
        omitted=[],
        copy_corrections=[],
        notes=("A4 210 x 297 mm, no bleed in the source (the BleedBox is not set). Navy field with rounded bottom corners (radius 17.93 mm, measured from the path, bottom edge at 241.35 mm); "
               "the lower 55.7 mm is white paper (no ink) with the partner mark left and the colour lockup right. In the source the field overshoots the page at the top (to y -65.2 mm, "
               "the shape continues with rounded top corners off the page) and its sides lie exactly on the page edge (x 0 and 210); the template runs the field 3 mm into the bleed at top, left and right "
               "and keeps the trim shape of the bottom edge and corners (a small step at the corner centre height lies in the bleed and is cut off). "
               "P+R symbol: comp py-comp-symbol-pr placed at its source position (bars 88.0 mm wide, the label is live text, variable label). "
               "Headline A20 dicht? Ubuntu Medium 24.69 mm white (variable headline). Divider: white stroke 4 pt (1.41 mm) from x 7 to 203 mm at y 126.5, the pattern of py-atom-line-divider "
               "(the library atom is 0.706 mm, here drawn with Doc.line at 1.41 mm). Body Ubuntu Regular 22.22 mm white, centred on x 105, leading 26.65 mm (1.2), three lines; the keywords tijdelijk gratis are Ubuntu Bold "
               "in PY-Aqua. Variables: headline, body-line-1, keyword-1, keyword-2, body-line-2, city (Schiedam), punctuation, background-colour. Text is start anchored at the printed origins (text-anchor middle is laid out "
               "wrongly by cairosvg for this text), so a changed word needs the line re-centred by hand. The source sets the first piece of line 1 with letter-spacing -0.1 mm (observed, kept). "
               "Partner mark: py-atom-partner-zuid-holland-bereikbaar (third party, reference only, own colours kept, so the template carries the partner blue #213A8F, green, yellow and magenta). "
               "Logo: py-comp-lockup-logo-tagline-color at scale 0.735 (beeldmerk 17.6 x 21.3 mm at x 120.1, y 258.8), navy logo and aqua tagline in tokens. "
               "OBSERVED drift (RGB ICC file, sRGB values): the navy field is #273A7C and the printed logo (beeldmerk and wordmark) is #213A8F, two different blues on one sign, neither equals PY-Blauw "
               "(#1A3580); the template uses the token. The aqua of the logo tagline is #2DB8CD and the keyword aqua #32B9CD. No spelling errors found. "
               "No cut contour: the source has none and a road sign is not a sticker (not added)."),
    )
