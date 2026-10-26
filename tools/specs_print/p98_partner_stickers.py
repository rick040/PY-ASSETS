"""PM-137 module p98: the two partner stickers (window sticker small, NFC sticker) that the slide "Partner pakket" shows as mock-ups.

Source: MarketingCampagne_ParkingYouPartner.pdf (key "marketing"), ONE A4 landscape slide, mock-ups at scale 0.358 (poster 210 mm = 75.3 mm on the slide).
The real sizes are not stated anywhere: they are derived at the slide scale and are PROPOSALS (window sticker 136 x 46 mm, NFC sticker 70 mm round).
Slide numbers (mm on the slide, origin top left of the page) were measured with Source.drawings; real mm = slide mm / 0.358.
The text of both stickers is outlined in the source (only "Hofplein" is live): it is rebuilt as live Ubuntu, fitted to the ink box of the outlines.
"""
import math
import re

from pyassets import printsrc
from pyassets.apps import application
from pyassets.compose import CUT_COLOR, CUT_WIDTH
from pyassets.core import PT_MM, TF, fmt
from pyassets.registry import crop

NAVY = "#1A3580"   # py-tok-color-blauw
WHITE = "#FFFFFF"  # py-tok-color-wit
GREY_WIN = "#F0F0F0"  # window sticker body: #CCCCCE at 30 percent over white renders as 240/240/240
GREY_NFC = "#E1E1E1"  # NFC disc: flat colour of the raster, 225/225/225 (no token)
S = 0.358  # slide scale
KEY = "marketing"

# ---------------------------------------------------------------- window sticker geometry (proposal: 136 x 46 mm)
WIN_TRIM = (136.0, 46.0)
WIN_BODY = (232.17, 68.55, 280.67, 84.90)  # slide bbox of the grey body (seq 380)
WIN_ORG = ((WIN_BODY[0] + WIN_BODY[2]) / 2 - WIN_TRIM[0] * S / 2, (WIN_BODY[1] + WIN_BODY[3]) / 2 - WIN_TRIM[1] * S / 2)
WIN_SEQ = [(379, 402)]
# ---------------------------------------------------------------- NFC geometry (proposal: 70 mm round)
NFC_D = 70.0
NFC_C = (267.09, 119.62)  # centre of the disc on the slide (measured on the render, disc 24.8 mm = 69.3 mm real)
NFC_ORG = (NFC_C[0] - NFC_D * S / 2, NFC_C[1] - NFC_D * S / 2)
NFC_SEQ = [(353, 379)]


def wx(x):  # slide x to real mm, window trim relative
    return (x - WIN_ORG[0]) / S


def wy(y):
    return (y - WIN_ORG[1]) / S


def nx(x):
    return (x - NFC_ORG[0]) / S


def ny(y):
    return (y - NFC_ORG[1]) / S


def _fonts():
    return {300: "Ubuntu Light", 400: "Ubuntu", 500: "Ubuntu Medium", 700: "Ubuntu"}


def _ink(text, wt, size):
    from pyassets.core import ink_box

    return ink_box(text, _fonts()[wt], wt, False, size, 0.0, 0.0)


def _under(svg, xml):
    """Insert shapes directly under the reference artwork (the helper only appends on top)."""
    k = 'data-role="reference">'
    i = svg.index(k) + len(k)
    return svg[:i] + xml + svg[i:]


def _body_path():
    """Source path of the grey window body (seq 380; the helper skips it because it sits in a 30 percent transparency group)."""
    src = printsrc.source(KEY)
    return crop(src, 1, (-1e5, -1e5, 1e5, 1e5), partial=True, skip=lambda p: getattr(p, "seq", -1) != 380, texts=False)[0]


def _body_d_real():
    """Path data of the window body in real mm, relative to the trim corner."""
    return _body_path().d(TF(0.0, 0.0, PT_MM / S, -WIN_ORG[0] / S, -WIN_ORG[1] / S))


def _pathops(d):
    import pathops
    from fontTools.pens.transformPen import TransformPen  # noqa: F401
    from fontTools.svgLib.path import parse_path

    po = pathops.Path()
    parse_path(d, po.getPen())
    return po


def _d(po):
    from fontTools.pens.svgPathPen import SVGPathPen

    sp = SVGPathPen(None, ntos=lambda v: ("%.3f" % v).rstrip("0").rstrip("."))
    po.draw(sp)
    return sp.getCommands()


def _offset(d, dist):
    """Outline of the shape d moved outward (dist > 0, round joins) or inward (dist < 0). Returns path data."""
    import pathops

    po = _pathops(d)
    st = pathops.Path(po)
    st.stroke(2 * abs(dist), pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4.0)
    st.convertConicsToQuads(0.01)
    op = pathops.PathOp.UNION if dist > 0 else pathops.PathOp.DIFFERENCE
    return _d(pathops.op(po, st, op))


def _bbox(po):
    from fontTools.pens.boundsPen import BoundsPen

    bp = BoundsPen(None)
    po.draw(bp)
    return bp.bounds


# ================================================================================================ window sticker
def _win_template(ctx):
    app_id = "py-app-sticker-raam-partner-klein"
    w, h = WIN_TRIM
    d = ctx.Doc(app_id, "Raamsticker klein (partner)", trim=WIN_TRIM, bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-color-aqua", "py-tok-type-ubuntu-medium")
    body = _body_d_real()
    bleed_d = _offset(body, 3.0)
    bx = _bbox(_pathops(bleed_d))
    # body, running into the bleed (offset outline of the sticker shape, 3 mm)
    d.path(bleed_d, bx, fill=GREY_WIN, gid="bleed-background")
    with d.group("py-atom-logo-beeldmerk-color"):
        # the source beeldmerk is 3 percent wider than the library shape (stretched in the mock-up): library proportions, same height and centre
        x0, y0, x1, y1 = 234.38, 71.06, 244.56, 83.01
        d.place("py-atom-logo-beeldmerk-color", wx((x0 + x1) / 2), wy(y0), h=(y1 - y0) / S, anchor="tc")
    # white pill (construction, no library match)
    px0, py0, px1, py1 = 247.25, 76.72, 278.47, 82.88
    d.rect(wx(px0), wy(py0), wx(px1), wy(py1), fill=WHITE, rx=(py1 - py0) / S / 2, gid="pill-location")
    with d.group("py-atom-symbol-p-garage-outline"):
        gx0, gy0, gx1, gy1 = 249.90, 77.49, 254.71, 81.90
        d.place("py-atom-symbol-p-garage-outline", wx(gx0), wy(gy0), w=(gx1 - gx0) / S)
    with d.group("variables"):
        l1x0, l1x1, l1y1 = 247.61, 278.00, 75.31  # ink box of the outlined line 1 (slide)
        t1 = "Parkeer slim bij"
        s1 = 12.09
        b = _ink(t1, 500, s1)
        cx = (wx(l1x0) + wx(l1x1)) / 2
        base = wy(l1y1) - b[3]  # ink bottom is the 'j' descender
        d.text(cx, base, t1, size=s1, fill=NAVY, weight=500, anchor="middle", variable="line-1")
        d.text(wx(257.1), wy(81.3), "Hofplein", size=4.2 / S, fill=NAVY, weight=500, variable="location-name")
    # cut contour: follows the outer shape of the sticker, 0.2 mm inside the trim (proposal)
    cd = _offset(body, -0.2)
    ax, ay = d._p(0, 0)
    d._stack[-1].append(f'<g id="cut-contour" data-spot="ThruCut"><path transform="translate({fmt(ax)} {fmt(ay)})" d="{cd}" fill="none" '
                        f'stroke="{CUT_COLOR}" stroke-width="{fmt(CUT_WIDTH)}"/></g>')
    d.guides(w, h)
    return d


def _win_reference(ctx):
    svg = ctx.piece_reference(KEY, WIN_SEQ, WIN_ORG, S, WIN_TRIM)
    p = _body_path()
    dd = p.d(TF(0.0, 0.0, PT_MM / S, -WIN_ORG[0] / S, -WIN_ORG[1] / S))
    return _under(svg, f'<path id="sticker-body" d="{dd}" fill="{GREY_WIN}"/>')


@application("py-app-sticker-raam-partner-klein", "Raamsticker klein (partner)", "sticker", trim_mm=WIN_TRIM, source=[(KEY, [1])], bleed_mm=3.0,
             status="rebuilt", reference_scope="mockup",
             cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "shape": "outline of the sticker (bubble plus two pills)",
                          "corner_radius_mm": 12.4,
                          "note": "Proposal: the mock-up shows no cut contour. The contour follows the outline of the grey sticker body, 0.2 mm inside the trim; "
                                  "radii measured on the body: upper pill 12.4 mm, lower pill 14.1 mm, bubble as the beeldmerk."})
def _(ctx):
    return dict(
        reference={"": _win_reference(ctx)}, template={"": _win_template(ctx)},
        omitted=["Window sticker mock-up shadow: the transparency group at 30 percent (#CCCCCE) is not omitted in the reference, see notes: it is the flat grey sticker body "
                 "(no blurred edge exists in the file), drawn here as flat #F0F0F0 under the artwork (30 percent of #CCCCCE over white). "
                 "The helper skips transparency groups, the body path is written by this module.",
                 "Mock-up caption 'Raamsticker klein' (slide text under the sticker): not part of the piece."],
        copy_corrections=[],
        notes=("Window sticker small of the partner package, shown as a mock-up on the slide 'Partner pakket'. REAL SIZE IS A PROPOSAL: the slide has no dimensions; the grey body "
               "measures 48.5 x 16.4 mm at the slide scale 0.358 (poster 210 mm = 75.3 mm), so 135.5 x 45.8 mm real, proposed 136 x 46 mm (trim, 3 mm bleed). "
               "Layout: colour beeldmerk (left) on a light grey base, two stacked pills: the upper one holds 'Parkeer slim bij', the lower one is white with the garage symbol and 'Hofplein'. "
               "Body: the light grey base is ONE flat shape, the beeldmerk bubble and the two pills merged (no blurred edge); in the file it sits in a 30 percent transparency group "
               "(#CCCCCE), which renders as #F0F0F0 and is read as the sticker body, not as a shadow (owner to confirm; if the sticker is transparent or white instead, only the body "
               "colour changes). The template draws the body flat in #F0F0F0 (no token, observed) and 3 mm bleed as the outline moved outward. "
               "Library: py-atom-logo-beeldmerk-color (same height as the source, centred; the mock-up beeldmerk is 3 percent wider than the library shape, so it was stretched in the "
               "slide: library proportions kept) and py-atom-symbol-p-garage-outline (compared: same drawing, 13.4 mm wide). The white pill is a construction (rounded rectangle, 87.2 x 17.2 mm); "
               "no library pill matches (py-comp-pill-destination has a disc and a bold label, py-comp-lockup-location-garage has a two line bold name and other spacing), so no new element. "
               "Text: 'Parkeer slim bij' is outlined in the source; fitted by overlay it is Ubuntu Medium (not bold: Bold at the same width is 0.5 mm too low), 12.09 mm, centred in the "
               "pill; 'Hofplein' is live in the source (Ubuntu Medium 4.2 mm = 11.7 mm real). Colours: the slide blue #192AA2 and cyan #0AD3E6 are drift, the template uses #1A3580 "
               "and #32B9CD (inside the library beeldmerk). Cut contour: proposal, no contour in the mock-up; it follows the sticker outline 0.2 mm inside the trim, 1 pt ThruCut. "
               "Variables: line-1 (first line), location-name."))


# ================================================================================================ NFC sticker
def _nfc_template(ctx):
    app_id = "py-app-sticker-nfc-partner"
    D = NFC_D
    d = ctx.Doc(app_id, "NFC sticker (partner)", trim=(D, D), bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-type-ubuntu-bold")
    d.circle(D / 2, D / 2, D / 2 + 3.0, fill=GREY_NFC, gid="bleed-background")
    with d.group("py-atom-logo-beeldmerk-color"):
        x0, y0, x1, y1 = 262.34, 110.95, 271.86, 122.44
        d.place("py-atom-logo-beeldmerk-color", D / 2, ny(y0), h=(y1 - y0) / S, anchor="tc")
    with d.group("variables"):
        size = 6.68
        for t, box, v in (("Reserveer je", (260.13, 123.59, 274.21, 125.88), "line-1"), ("parkeerplek", (260.34, 125.97, 274.06, 128.28), "line-2")):
            b = _ink(t, 700, size)
            d.text(D / 2, ny(box[3]) - b[3], t, size=size, fill=NAVY, weight=700, anchor="middle", variable=v)
    # cut contour: circle, radius = half the diameter, 0.2 mm inside the trim (proposal)
    ax, ay = d._p(D / 2, D / 2)
    r = D / 2 - 0.2
    d._stack[-1].append(f'<g id="cut-contour" data-spot="ThruCut"><circle cx="{fmt(ax)}" cy="{fmt(ay)}" r="{fmt(r)}" fill="none" '
                        f'stroke="{CUT_COLOR}" stroke-width="{fmt(CUT_WIDTH)}"/></g>')
    d.guides(D, D)
    return d


def _nfc_reference(ctx):
    svg = ctx.piece_reference(KEY, NFC_SEQ, NFC_ORG, S, (NFC_D, NFC_D))
    return _under(svg, f'<circle id="sticker-disc-rebuilt" cx="{fmt(NFC_D / 2)}" cy="{fmt(NFC_D / 2)}" r="{fmt(NFC_D / 2)}" fill="{GREY_NFC}"/>')


@application("py-app-sticker-nfc-partner", "NFC sticker (partner)", "sticker", trim_mm=(NFC_D, NFC_D), source=[(KEY, [1])], bleed_mm=3.0,
             status="rebuilt", reference_scope="mockup",
             cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "shape": "circle", "corner_radius_mm": NFC_D / 2,
                          "note": "Proposal: the mock-up shows no cut contour. Circle, radius half the diameter (35 mm), 0.2 mm inside the trim."})
def _(ctx):
    return dict(
        reference={"": _nfc_reference(ctx)}, template={"": _nfc_template(ctx)},
        omitted=["Round grey sticker body with its soft shadow: ONE raster image (254.7 to 279.5 x 107.3 to 132.1 mm on the slide), NOT copied. "
                 "Rebuilt as a flat vector circle in light grey #E1E1E1 (measured from the render: 225/225/225), diameter 70 mm; the slight darker rim and the soft shadow "
                 "of the raster are not reproduced.",
                 "Mock-up caption 'NFC sticker' (slide text under the sticker): not part of the piece."],
        copy_corrections=[],
        notes=("NFC sticker of the partner package, shown as a mock-up on the slide 'Partner pakket'. REAL SIZE IS A PROPOSAL: the disc measures 24.8 mm on the slide "
               "(horizontal 254.68 to 279.49 mm, vertical 24.7 mm), 69.3 mm at the scale 0.358, proposed 70 mm round (trim 70 x 70, 3 mm bleed, the reference is scaled so that 70 mm "
               "equals the measured disc, 1 percent). REBUILT: in the source the grey sticker body and its shadow are one raster image; the disc is a flat vector circle "
               "(#E1E1E1, no token) and the raster is not used. Only the beeldmerk and the text are vector in the source. "
               "Library: py-atom-logo-beeldmerk-color (compared: same drawing, 26.6 mm wide, 32.1 mm high, centred, top 24.2 mm above the centre). "
               "Text: 'Reserveer je' / 'parkeerplek' is outlined in the source; fitted by overlay as Ubuntu Bold 6.68 mm (ink width 39.3 and 38.3 mm, ink height agrees), navy, centred, "
               "baseline pitch about 7.7 mm; live text in the template. "
               "NFC chip: its type and position are NOT drawn (unknown); keep a chip free zone (to be defined by the supplier) before the artwork is sent to print. "
               "Cut contour: circle with radius half the diameter, 0.2 mm inside the trim, 1 pt ThruCut: proposal. "
               "Colours: slide blue #192AA2 and cyan #0AD3E6 are drift, the template uses #1A3580 and #32B9CD (inside the beeldmerk). Variables: line-1, line-2."))
