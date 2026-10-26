"""PM-137 module p97: partner package, three print applications shown as MOCK-UPS on one presentation slide.

Source: MarketingCampagne_ParkingYouPartner.pdf (key "marketing"), ONE A4 landscape slide ("Partner pakket", RGB ICC) with the package contents as
small mock-ups. Poster, flyer front and flyer back are drawn at a slide scale of 0.35807 (poster 210 mm -> 75.194 mm, measured on the white page
rectangles: 75.194 x 106.346 mm, flyers 53.173 x 75.194 mm). The pieces are contiguous ranges of paint order numbers (seq of Source.drawings):
poster 403 to 507, flyer back 585 to 658, flyer front 664 to 778. All numbers below are REAL millimetres (slide mm divided by the scale, origin at the
top left of the piece = trim corner), measured from the vector paths and fitted by pixel overlay (IoU) for the outlined texts.
Text is outlined in the source: it is rebuilt as live Ubuntu (size, origin, tracking fitted by overlay; the only live text of the slide, "Hofplein",
belongs to the raamsticker and is not part of these pieces).
"""
import math

from pyassets import printsrc
from pyassets.apps import application
from pyassets.compose import Doc
from pyassets.core import PT_MM, TF, Defs, Element, Group, Path, affine, clip_to_rect, fmt, _esc, _from_pathops, _to_pathops
from pyassets.registry import crop, element

KEY = "marketing"
SC = 0.35807  # slide scale (mm on the slide per real mm)
NAVY = "#1A3580"
AQUA = "#32B9CD"
ORANGE = "#F08300"
WHITE = "#FFFFFF"
GREY = "#EBEBEB"  # flat photo placeholder in the references (as in p95)
QR_URL = "https://parkingyou.nl/nl"
box = printsrc.box_mm

ORG_POSTER = (119.252, 62.584)
ORG_FRONT = (150.926, 116.219)
ORG_BACK = (178.758, 92.248)
TRIM_POSTER = (210, 297)
TRIM_FLYER = (148, 210)
RANGE_POSTER = [(403, 509)]
RANGE_BACK = [(508, 663)]
RANGE_FRONT = [(664, 778)]
BLEED = 3.0

# ------------------------------------------------------------------------------------------------ price badge geometry
# offsets are relative to the circle centre; fitted by overlay (IoU 0.98 to 0.99 per run)
BADGE_FLYER = dict(r=27.985, whole=(-22.962, 3.185, 23.655), comma=(3.807, 1.577, 13.096), cents=(3.956, -2.756, 15.75), unit=(-14.545, 13.674, 8.258), angle=0.0)
BADGE_POSTER = dict(r=37.458, whole=(-31.594, 3.192, 27.841), comma=(-0.337, 7.828, 15.4), cents=(0.811, 2.848, 18.551), unit=(-24.329, 17.273, 9.712), angle=12.0)
CIRCLE_FLYER = (112.055, 114.81)  # centre on the flyer front
CIRCLE_POSTER = (182.472, 23.676)  # centre on the poster (the circle runs off the top and the right edge)

# ------------------------------------------------------------------------------------------------ pill with pin (two placements, own proportions)
PILL_POSTER = dict(x=131.56, y=269.94, w=64.57, h=15.48, pin=(5.38, 4.18, 7.70), tx=14.039, base=10.479, size=6.358)
PILL_FLYER = dict(x=85.28, y=31.46, w=41.03, h=11.08, pin=(3.31, 2.80, 5.51), tx=10.378, base=7.277, size=5.891)
PIN_H = 7.70  # real height of the pin atom (poster pin)


# ------------------------------------------------------------------------------------------------ helpers
def _cut_circle(cx, cy, r, rect):
    """White circle intersected with the page (trim plus bleed) with pathops: (path data, box). The circle runs off the sheet."""
    import pathops
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.svgPathPen import SVGPathPen

    k = 0.5522847498 * r
    c = pathops.Path()
    p = c.getPen()
    p.moveTo((cx + r, cy))
    p.curveTo((cx + r, cy + k), (cx + k, cy + r), (cx, cy + r))
    p.curveTo((cx - k, cy + r), (cx - r, cy + k), (cx - r, cy))
    p.curveTo((cx - r, cy - k), (cx - k, cy - r), (cx, cy - r))
    p.curveTo((cx + k, cy - r), (cx + r, cy - k), (cx + r, cy))
    p.closePath()
    x0, y0, x1, y1 = rect
    pg = pathops.Path()
    q = pg.getPen()
    q.moveTo((x0, y0)); q.lineTo((x1, y0)); q.lineTo((x1, y1)); q.lineTo((x0, y1)); q.closePath()
    res = pathops.op(c, pg, pathops.PathOp.INTERSECTION)
    sp, bp = SVGPathPen(None, ntos=lambda v: ("%.3f" % v).rstrip("0").rstrip(".")), BoundsPen(None)
    res.draw(sp)
    res.draw(bp)
    return sp.getCommands(), bp.bounds


def _badge(d, cx, cy, P, fill_text, circle=None, gid="circle"):
    """White price circle with the price (italic bold, comma and cents set smaller and raised) and the unit. circle = full path data
    (cropped circles) or None for a plain circle. Texts are live Ubuntu; the comma is a fixed part of the price block."""
    a = P["angle"]
    if circle:
        d.path(circle[0], circle[1], fill=WHITE, gid=gid)
    else:
        d.circle(cx, cy, P["r"], fill=WHITE, gid=gid)
    with d.group("price-block"):
        wx, wy, ws = P["whole"]
        d.text(cx + wx, cy + wy, "€7", ws, fill_text, weight=700, italic=True, rotate=a, variable="price")
        kx, ky, ks = P["comma"]
        d.text(cx + kx, cy + ky, ",", ks, fill_text, weight=700, italic=True, rotate=a, gid="price-comma")
        sx, sy, ss = P["cents"]
        d.text(cx + sx, cy + sy, "50", ss, fill_text, weight=700, italic=True, rotate=a, variable="price-cents")
    ux, uy, us = P["unit"]
    d.text(cx + ux, cy + uy, "per dag", us, fill_text, weight=500, rotate=a, variable="unit")


def _pill(d, P, fg, bg, label="Philips Stadion", pin_fill=None, gid="pill"):
    """Stadium pill with location pin and a name (live text)."""
    x, y, w, h = P["x"], P["y"], P["w"], P["h"]
    d.rect(x, y, x + w, y + h, fill=bg, rx=h / 2, gid=gid)
    px, py, ph = P["pin"]
    with d.group("py-atom-icon-location-pin-symmetric"):
        d.place("py-atom-icon-location-pin-symmetric", x + px, y + py, scale=ph / PIN_H, recolor={WHITE: pin_fill or fg} if (pin_fill or fg) != WHITE else None)
    d.text(x + P["tx"], y + P["base"], label, P["size"], fg, weight=500, variable="location-name")


def _piece_reference(ctx, ranges, origin, trim, variant, omit=None, photo_clip=None):
    """Same output as printsrc.piece_reference_svg (mock-up piece scaled to real size); the only difference: an optional photo placeholder
    (the clip outline of the photo, flat grey) is inserted at its paint order position, so that it lies below the elements that sit on the photo."""
    src = printsrc.source(KEY)
    ox, oy = origin
    k = 1.0 / SC
    tw, th = trim
    x0, y0 = printsrc.mm2pt(ox), printsrc.mm2pt(oy)
    x1, y1 = printsrc.mm2pt(ox + tw * SC), printsrc.mm2pt(oy + th * SC)
    inr = lambda q: any(a <= getattr(q, "seq", -1) <= b for a, b in ranges)

    def skip(p_):
        if not inr(p_) or getattr(p_, "gop", ()):
            return True
        return bool(omit and omit(p_))

    items = crop(src, 1, (-1e5, -1e5, 1e5, 1e5), partial=True, skip=skip, texts=False)
    if photo_clip is not None:
        c = [c for c in src.clips(1, (-1e5, -1e5, 1e5, 1e5)) if abs(c.seq - photo_clip) < 0.01][0]
        c.fill = GREY
        c.tag = ""
        g = Group(items=[c], opacity=1.0, gid="placeholder-photo")
        g.seq = photo_clip
        items.append(g)
        items.sort(key=lambda it: getattr(it, "seq", 1e9))
    items = clip_to_rect(items, (x0 - printsrc.mm2pt(2), y0 - printsrc.mm2pt(2), x1 + printsrc.mm2pt(2), y1 + printsrc.mm2pt(2)))
    items = affine(items, k, k, -x0 * k, -y0 * k)
    el = Element(id=ctx.app_id, name_nl="", level="app", category="reference", page=1, items=items)
    tf = TF(0.0, 0.0, PT_MM, 0.0, 0.0)
    defs = Defs(prefix=f"{ctx.app_id}{('-' + variant) if variant else ''}-ref-")
    body = el.body(tf, defs)
    dd = "<defs>" + "".join(defs.items) + "</defs>" if defs.items else ""
    gid = f"{ctx.app_id}-reference" + (f"-{variant}" if variant else "")
    t = f"{ctx.app_id}{(' ' + variant) if variant else ''}: reference reproduction of a mock-up piece from {printsrc.SOURCES[KEY]['file']}, scaled to real size (slide scale {SC})"
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(tw)}mm" height="{fmt(th)}mm" viewBox="0 0 {fmt(tw)} {fmt(th)}">\n'
        f"<title>{_esc(t)}</title>\n{dd}"
        f'<g id="{gid}" data-role="reference">{body}</g>\n'
        "</svg>\n"
    )


# ================================================================================================ new elements
@element("py-atom-icon-location-pin-symmetric", "Locatiepin symmetrisch", "atom", "icon", 1, src=KEY, status="extracted",
         notes="White location pin of the location pills on the partner poster and the Hofplein flyer, one path with the round hole, 5.2 x 7.7 mm. "
               "Taken from the poster mock-up (the slide draws it 1.9 x 2.8 mm; scaled by 1 / 0.35807 to the real size of the A4 poster). "
               "It is NOT the library py-atom-icon-location-pin: compared by overlay at equal height the print pin is symmetric and narrower (width 0.67 of the height, "
               "the library pin 0.72 and asymmetric); overlap only 0.93, visible at 7.7 mm. White on transparent: view on a dark background.")
def _(src):
    items = crop(src, 1, box(168.0, 160.4, 170.5, 163.9), texts=False)
    assert len(items) == 1, len(items)
    k = 1.0 / SC
    return affine(items, k, k, 0.0, 0.0)


def _pill_doc():
    d = Doc("py-comp-pill-location", "Locatiepil", tight=True)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-medium")
    P = dict(PILL_POSTER, x=0.0, y=0.0)
    _pill(d, P, WHITE, NAVY, "Philips Stadion", pin_fill=WHITE)
    return d


@element("py-comp-pill-location", "Locatiepil", "comp", "pill", 1, src=KEY, status="rebuilt", variables=("location name",),
         notes="Stadium pill (full round ends) with a location pin and a name, as on the footer of the partner poster: navy pill 64.6 x 15.5 mm, white pin "
               "(py-atom-icon-location-pin-symmetric, 7.7 mm high, 5.4 mm from the left edge), name in Ubuntu Medium 6.36 mm white (live text, variable location-name, "
               "starts 14.0 mm from the left edge). The flyer front has the same pill in white with navy pin and text (Hofplein, 41.0 x 11.1 mm, text 5.89 mm): "
               "the proportions are NOT a uniform scale of this one (pin to height 0.50 in both, but the text is 0.41 of the height on the poster and 0.53 on the flyer, "
               "the pin sits 0.35 against 0.30 of the height from the edge), so the flyer draws the same construction with its own measures instead of placing this element. "
               "The pill is narrower or wider with the name (no fixed width). Rebuilt: the print outlines the text; construction plus live text. Navy pill: view on a light background.")
def _(src):
    return _pill_doc()


def _badge_doc():
    d = Doc("py-comp-price-badge-circle", "Prijscirkel", tight=True)
    d.uses("py-tok-color-wit", "py-tok-color-blauw", "py-tok-type-ubuntu-bold-italic", "py-tok-type-ubuntu-medium")
    P = BADGE_FLYER
    _badge(d, P["r"], P["r"], P, NAVY)
    return d


@element("py-comp-price-badge-circle", "Prijscirkel", "comp", "price", 1, src=KEY, status="rebuilt", variables=("price", "price cents", "unit"),
         notes="White circle of 56.0 mm with the day price: '€7' in Ubuntu Bold Italic 23.66 mm navy, the comma (13.1 mm) and the cents '50' (15.75 mm, set raised) in the same face, "
               "and the unit 'per dag' in Ubuntu Medium 8.26 mm below. Live text (variables price, price-cents, unit; the comma is fixed), fitted by overlay to the outlines of the Hofplein flyer "
               "(IoU 0.98 to 0.99 per run). The poster uses the same construction in orange on a 74.9 mm circle that is cropped by the top right corner, with the text 1.18 times larger "
               "(23.66 to 27.84 mm) and rotated 12 degrees, but with other proportions to the circle (price height 0.74 of the radius against 0.85), so it is drawn there with its own measures. "
               "NOT py-comp-price-bubble-corner (a white quarter bubble with a different arc and price size) and not the aqua speech bubbles. Rebuilt: circle plus live text. "
               "White circle: view on a navy background.")
def _(src):
    return _badge_doc()


# ================================================================================================ application 1: poster A4
JOUW = (19.158, 112.821, 30.951, -0.592)
SHOPPEN = (19.241, 143.122, 31.013, -0.628)
START = (18.881, 173.461, 31.056, -0.664)
SLIM = (19.25, 203.764, 10.452, -0.22)
VOLG = (18.863, 282.129, 10.488, -0.223)
LOGO_POSTER = (15.022, 14.363, 0.749)
FIELD_BOTTOM = 259.28


def _poster_template(ctx):
    app_id = "py-app-poster-partner-a4"
    d = ctx.Doc(app_id, "Partnerposter A4", trim=TRIM_POSTER, bleed=BLEED)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-color-oranje", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-medium",
           "py-tok-type-ubuntu-bold-italic", "py-comp-price-badge-circle", "py-comp-pill-location")
    with d.group("bleed-background"):
        d.rect(-BLEED, -BLEED, 210 + BLEED, 297 + BLEED, fill=WHITE, gid="paper")
        d.rect(-BLEED, -BLEED, 210 + BLEED, FIELD_BOTTOM, fill=NAVY, gid="field", variable="background-colour", example=NAVY)
    with d.group("py-atom-logo-horizontal-white"):
        d.place("py-atom-logo-horizontal-white", LOGO_POSTER[0], LOGO_POSTER[1], scale=LOGO_POSTER[2])
    with d.group("py-comp-price-badge-circle"):
        cx, cy = CIRCLE_POSTER
        circ = _cut_circle(cx, cy, BADGE_POSTER["r"], (-BLEED, -BLEED, 210 + BLEED, 297 + BLEED))
        _badge(d, cx, cy, BADGE_POSTER, ORANGE, circle=circ)
    for (x, y, s, sp), t, fill, var in ((JOUW, "Jouw dagje", WHITE, "headline-1"), (SHOPPEN, "shoppen", ORANGE, "headline-2"), (START, "start hier!", WHITE, "headline-3")):
        d.text(x, y, t, s, fill, weight=700, spacing=sp, variable=var)
    d.text(SLIM[0], SLIM[1], "Slim parkeren. Snel in de stad.", SLIM[2], WHITE, weight=500, spacing=SLIM[3], variable="subline")
    d.text(VOLG[0], VOLG[1], "Volg de borden", VOLG[2], NAVY, weight=500, spacing=VOLG[3], variable="footer-text")
    with d.group("py-comp-pill-location"):
        _pill(d, PILL_POSTER, WHITE, NAVY, "Philips Stadion", pin_fill=WHITE)
    d.guides(*TRIM_POSTER)
    return d


@application("py-app-poster-partner-a4", "Partnerposter A4", "poster", trim_mm=TRIM_POSTER, source=[(KEY, [1])], bleed_mm=BLEED, status="rebuilt",
             reference_scope="mockup")
def _(ctx):
    d = _poster_template(ctx)
    ref = ctx.piece_reference(KEY, RANGE_POSTER, ORG_POSTER, SC, TRIM_POSTER)
    return dict(
        reference={"": ref}, template={"": d},
        omitted=["Soft shadow of the mock-up (transparency groups, black at 5 to 30 percent) and the three raster images of the slide (two photos, one shadow): not drawn.",
                 "The slide labels (A4 poster, A5 flyer ...) and the other mock-ups (raamsticker, NFC sticker, flyers) around the poster. The poster is partly hidden under the flyers "
                 "on the slide, its paths are complete and drawn in full here.",
                 "The poster has no separate white circle in the source: the navy field is one path with a circle shaped notch (top right) through which the white sheet shows. "
                 "The template draws the white circle as its own shape on the navy field."],
        copy_corrections=[],
        notes=("A4 poster 210 x 297 mm, shown as a MOCK-UP on the slide 'Partner pakket' at a scale of 0.35807 (white sheet 75.194 x 106.346 mm on the slide, so 210.0 x 297.0 mm real, "
               "A4 is a standard format). The reference is the mock-up taken from the slide at real size (viewBox 210 x 297 mm, no bleed: the mock-up shows the trimmed sheet; "
               "the template adds 3 mm bleed). REBUILT: all texts are outlined in the source and are live Ubuntu in the template, fitted by overlay (IoU 0.88 to 0.99): headline "
               "'Jouw dagje' / 'shoppen' (orange) / 'start hier!' Ubuntu Bold 31.0 mm, tracking -0.02 em, line pitch 30.3 mm; 'Slim parkeren. Snel in de stad.' Ubuntu Medium 10.45 mm white; "
               "'Volg de borden' Ubuntu Medium 10.49 mm navy (the brief says regular and bold: the overlay fits Medium best for both); the price circle and the location pill come from "
               "the new comps. Library: py-atom-logo-horizontal-white at scale 0.749 (78.5 mm wide, overlap 0.99), py-comp-price-badge-circle construction (white circle 74.9 mm, "
               "centre 182.5 / 23.7 mm, cropped by the corner with pathops at the bleed edge; '€7' Ubuntu Bold Italic 27.84 mm, comma 15.4 mm and cents '50' 18.55 mm in the orange token, "
               "'per dag' Ubuntu Medium 9.71 mm, all rotated 12 degrees (the brief estimated 10)), py-comp-pill-location (navy pill 64.6 x 15.5 mm, new atom "
               "py-atom-icon-location-pin-symmetric, 'Philips Stadion' Ubuntu Medium 6.36 mm white). The navy field ends at y 259.3 mm (white footer 37.7 mm). "
               "Colours: the slide blue #192AA2 is drift (template #1A3580), the slide orange #FF8401 is the token PY-Oranje #F08300 in the template (first print piece with the orange token), "
               "white. Variables: price, price-cents, unit, headline-1, headline-2, headline-3, subline, footer-text, location-name, background-colour. "
               "Open points: price 7,50 per dag is the same as on the Hofplein panel; the location name is an example value; the tracking of the headline is -0.02 em in the print."),
    )


# ================================================================================================ application 2: flyer A5 (front and back)
LOGO_FRONT = (5.96, 8.45, 0.3404)
BEELD_FRONT = (5.962, 174.918, 0.4524)
PHOTO_FRONT = (23.13, 25.47, 2.8403)  # bubble silhouette of the photo clip: top left and scale of py-atom-shape-bubble-image-mask
FRONT_FIELD_BOTTOM = 167.92
FRONT_CLAIM1 = (30.176, 183.047, 10.452, -0.028)
FRONT_CLAIM2 = (30.603, 192.667, 10.433, -0.02)
FRONT_SMALL = (30.474, 201.054, 4.132)
LOGO_BACK = (8.726, 6.522, 0.4423)
PHOTO_BACK = (21.205, 20.638, 3.0384)
BACK_H1 = (9.3, 174.387, 9.862, -0.047)
BACK_H2 = (9.137, 183.617, 9.86, -0.007)
BACK_SUB = (9.252, 195.829, 7.871, -0.01)
QR_PLATE = (107.93, 166.65, 138.56, 197.29)
QR_R = 3.85
QR_INSET = 2.22


def _front_template(ctx):
    app_id = "py-app-flyer-partner-a5"
    d = ctx.Doc(app_id + "-front", "Partnerflyer A5 voorkant", trim=TRIM_FLYER, bleed=BLEED)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-color-aqua", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-medium", "py-tok-type-ubuntu-regular",
           "py-comp-price-badge-circle", "py-comp-pill-location")
    with d.group("bleed-background"):
        d.rect(-BLEED, -BLEED, 148 + BLEED, 210 + BLEED, fill=WHITE, gid="paper")
        d.rect(-BLEED, -BLEED, 148 + BLEED, FRONT_FIELD_BOTTOM, fill=NAVY, gid="field", variable="background-colour", example=NAVY)
    with d.group("py-atom-logo-horizontal-white"):
        d.place("py-atom-logo-horizontal-white", LOGO_FRONT[0], LOGO_FRONT[1], scale=LOGO_FRONT[2])
    with d.group("placeholder-photo", data_placeholder="photo", data_variable="photo"):
        d.place("py-atom-shape-bubble-image-mask", PHOTO_FRONT[0], PHOTO_FRONT[1], scale=PHOTO_FRONT[2])
    d.variables["photo"] = "foto van het Hofpleingebouw (bubbelvorm)"
    with d.group("py-atom-logo-beeldmerk-color"):
        d.place("py-atom-logo-beeldmerk-color", BEELD_FRONT[0], BEELD_FRONT[1], scale=BEELD_FRONT[2])
    cx, cy = CIRCLE_FLYER
    r = BADGE_FLYER["r"]
    with d.group("py-comp-price-badge-circle"):
        d.place("py-comp-price-badge-circle", cx - r, cy - r, scale=1.0)
    d.variables.update({"price": "€7", "price-cents": "50", "unit": "per dag"})
    with d.group("py-comp-pill-location"):
        _pill(d, PILL_FLYER, NAVY, WHITE, "Hofplein", pin_fill=NAVY)
    with d.group("footer-claim"):
        d.text(FRONT_CLAIM1[0], FRONT_CLAIM1[1], "Parkeren en shopping", FRONT_CLAIM1[2], NAVY, weight=700, spacing=FRONT_CLAIM1[3], variable="claim-1")
        d.text(FRONT_CLAIM2[0], FRONT_CLAIM2[1], "maar dan voordelig", FRONT_CLAIM2[2], NAVY, weight=700, spacing=FRONT_CLAIM2[3], variable="claim-2")
        d.text(FRONT_SMALL[0], FRONT_SMALL[1], "Geldig vanaf 1 januari, niet op wedstrijddagen", FRONT_SMALL[2], AQUA, weight=400, variable="validity")
    d.guides(*TRIM_FLYER)
    return d


def _back_template(ctx):
    app_id = "py-app-flyer-partner-a5"
    d = ctx.Doc(app_id + "-back", "Partnerflyer A5 achterkant", trim=TRIM_FLYER, bleed=BLEED)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-regular")
    d.rect(-BLEED, -BLEED, 148 + BLEED, 210 + BLEED, fill=WHITE, gid="bleed-background")
    with d.group("py-atom-logo-horizontal-color"):
        d.place("py-atom-logo-horizontal-color", LOGO_BACK[0], LOGO_BACK[1], scale=LOGO_BACK[2], recolor={AQUA: NAVY})
    with d.group("placeholder-photo", data_placeholder="photo", data_variable="photo"):
        d.place("py-atom-shape-bubble-image-mask", PHOTO_BACK[0], PHOTO_BACK[1], scale=PHOTO_BACK[2])
    d.variables["photo"] = "foto van handen met telefoon (bubbelvorm)"
    d.text(BACK_H1[0], BACK_H1[1], "Makkelijk parkeren", BACK_H1[2], NAVY, weight=700, spacing=BACK_H1[3], variable="headline-1")
    d.text(BACK_H2[0], BACK_H2[1], "vanuit je broekzak", BACK_H2[2], NAVY, weight=700, spacing=BACK_H2[3], variable="headline-2")
    d.text(BACK_SUB[0], BACK_SUB[1], "Download nu onze app", BACK_SUB[2], NAVY, weight=400, spacing=BACK_SUB[3], variable="subline")
    x0, y0, x1, y1 = QR_PLATE
    with d.group("qr-plate"):
        d.rect(x0, y0, x1, y1, fill=NAVY, rx=QR_R, gid="plate")
        with d.group("qr-target", data_variable="qr-target"):
            d.placeholder("qr", x0 + QR_INSET, y0 + QR_INSET, x1 - QR_INSET, y1 - QR_INSET, "QR", variable="qr-target", example=QR_URL)
    d.guides(*TRIM_FLYER)
    return d


@application("py-app-flyer-partner-a5", "Partnerflyer A5", "flyer", trim_mm=TRIM_FLYER, source=[(KEY, [1])], bleed_mm=BLEED, variants=("front", "back"),
             status="rebuilt", reference_scope="mockup")
def _(ctx):
    ref_front = _piece_reference(ctx, RANGE_FRONT, ORG_FRONT, TRIM_FLYER, "front", photo_clip=679.5)
    # back: the navy bubble (598) under the photo is replaced by the grey photo placeholder; the QR modules sit twice in the source
    # (a white path and a white rectangle clipped to the same modules): the clipped duplicate (660) is left out
    ref_back = _piece_reference(ctx, RANGE_BACK, ORG_BACK, TRIM_FLYER, "back", omit=lambda p: getattr(p, "seq", 0) in (598, 660), photo_clip=599.5)
    return dict(
        reference={"front": ref_front, "back": ref_back}, template={"front": _front_template(ctx), "back": _back_template(ctx)},
        omitted=["Soft shadows of the mock-up (transparency groups, black at 5 to 30 percent, including the black rectangles behind the flyers) and the raster images of the slide: not drawn.",
                 "The two photos (building at the Hofplein on the front, hands with a phone on the back) are rasters clipped to the beeldmerk bubble: never copied. The references show the clip "
                 "outline as a flat #EBEBEB placeholder (group placeholder-photo).",
                 "Back: navy bubble (#192AA2, same outline as the photo clip, 109 x 132 mm) directly under the photo: hidden underlay, replaced by the placeholder. "
                 "Back: a white rectangle clipped to the QR modules, a duplicate of the white module path directly before it.",
                 "The A5 labels of the slide ('A5 flyer - voorkant', 'A5 flyer - achterkant') and the other mock-ups. The back flyer is partly hidden behind the front flyer on the slide, "
                 "its paths are complete and drawn in full here."],
        copy_corrections=[{"original": "Geldig vanaf 1 januari - niet op wedstrijddagen", "corrected": "Geldig vanaf 1 januari, niet op wedstrijddagen",
                           "reason": "The spaced hyphen is a typographic dash; the house rule is no dashes in copy, so the template uses a comma. The reference keeps the original."}],
        notes=("A5 flyer 148 x 210 mm, two sides (variants front and back), shown as MOCK-UPS on the slide 'Partner pakket' at a scale of 0.35807 (white sheets 53.173 x 75.194 mm). "
               "The mock-up is 148.5 mm wide at that scale (the standard A5 is 148 x 210, rounded from 148.5): the template and the reference viewBox use 148 x 210 as specified, "
               "so the reference cuts 0.5 mm off the right edge and the right hand elements sit 0.5 mm closer to the edge than in the mock-up. The mock-up shows no bleed, the template adds 3 mm. "
               "FRONT (voorkant): navy field 167.9 mm high, white footer; py-atom-logo-horizontal-white at scale 0.340 (overlap 0.99), photo placeholder = py-atom-shape-bubble-image-mask at scale 2.840 "
               "(the clip outline of the building photo, 102 x 124 mm; placeholder-photo with data-variable photo), py-comp-price-badge-circle placed 1:1 (white circle 56.0 mm, navy italic "
               "price '€7,50' and 'per dag'), py-comp-pill-location construction in white with navy pin and 'Hofplein' (the pill is 41.0 x 11.1 mm; own measures, see the comp note; the "
               "slide's one live text 'Hofplein' belongs to the raamsticker, on the flyer it is outlined like the rest), footer: py-atom-logo-beeldmerk-color at scale 0.452 (overlap 0.999), "
               "'Parkeren en shopping' / 'maar dan voordelig' Ubuntu Bold 10.45 mm navy (leading 9.6 mm) and the small line in aqua Ubuntu Regular 4.13 mm. "
               "BACK (achterkant): white sheet, py-atom-logo-horizontal-color at scale 0.442 (overlap 0.97; the print logo has a navy dot where the library colour logo has the aqua dot, so the dot is recoloured to navy, a one colour navy logo that the library does not have), large photo bubble placeholder (py-atom-shape-bubble-image-mask at scale 3.038, overlap 1.00), "
               "'Makkelijk parkeren' / 'vanuit je broekzak' Ubuntu Bold 9.86 mm navy (pitch 9.2 mm), 'Download nu onze app' Ubuntu Regular 7.87 mm navy, QR plate 30.6 mm. "
               "QR: the source draws a real QR code (white modules on a navy rounded square, vector paths, 1193 sub paths); the reference keeps it, the template has the plate and a "
               "placeholder group qr-target (data-variable qr-target, example " + QR_URL + "). The library plate py-comp-qr-plate does NOT match: corner radius 3.85 mm on 30.6 mm (12.6 percent) against "
               "5.77 on 87.9 (6.6 percent), the other plate py-comp-qr-reserveer is 10 percent: the plate is drawn inline (owner: add a plate variant with 12.6 percent?). "
               "Texts are outlined in the source and live Ubuntu in the template, fitted by overlay (IoU 0.86 to 0.99). Colours: slide blue #192AA2 is drift (template #1A3580), slide cyan #0AD3E6 "
               "(small line, beeldmerk dot) is not PY-Aqua; the template uses the token #32B9CD. Variables front: price, price-cents, unit, location-name, claim-1, claim-2, validity, photo, "
               "background-colour; back: headline-1, headline-2, subline, photo, qr-target. Open points: the building photo (Hofplein) and the hands photo are placeholders; "
               "the price 7,50 per dag appears here and on the Hofplein panel."),
    )
