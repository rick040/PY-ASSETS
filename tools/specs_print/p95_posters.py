"""PM-137 module p95: two posters (storing A3 and app A2) and the new elements they need.

Sources: posters_297x420_3_1.pdf (posterA3, page 303 x 426 mm) and posters_420x594_3_1.pdf (posterA2, page 426 x 600 mm); both RGB (ICC sRGB), trim offset 3 mm.
All numbers were measured from the sources (page mm, origin top left of the MediaBox; the trim corner sits at (3, 3)).
Headline and URL texts are outlined in the sources: they are rebuilt as live Ubuntu (size and origin fitted to the ink box of the outlines).
Coordinates of components in this module are PAGE mm (tight docs); templates convert to trim relative mm (page minus 3).
"""
import re

from pyassets import printsrc
from pyassets.apps import application
from pyassets.compose import Doc, text_width
from pyassets.core import PT_MM, TF, Defs, Element, Path, _esc, _from_pathops, _to_pathops, fmt, make_text
from pyassets.registry import crop, element

A3, A2 = "posterA3", "posterA2"
OFF = 3.0  # trim corner inside the page (mm)
NAVY = "#1A3580"
AQUA = "#32B9CD"
WHITE = "#FFFFFF"
LIGHT_AQUA_A3 = "#83CBE1"  # CMYK-less RGB sample on the A3 poster, no token, kept as sampled
LIGHT_AQUA_A2 = "#8CCDDF"  # chevron on the A2 poster, no token, kept as sampled
GREY = "#EBEBEB"  # location placeholder box (A3) and the flat photo placeholder in the references
TINT_SRC = "#F7F8FA"  # pale bubble as rendered from the raster (raw palette value #F5F6F9)
TINT_OPACITY = 0.035  # navy at 3.5 percent over white gives #F7F8FA
QR_URL = "https://parkingyou.nl/nl"
box = printsrc.box_mm
TRIM_A3 = (297, 420)
TRIM_A2 = (420, 594)


# ------------------------------------------------------------------------------------------------ helpers
def _emit(d, items, dx=0.0, dy=0.0, gid=None):
    """Write extracted source Paths (points) into a Doc. (dx, dy) = page mm that maps to the Doc origin."""
    from pyassets.core import PRINT_NORMALISE

    tf = TF(0.0, 0.0, PT_MM, d.ox - dx, d.oy - dy)
    for p in items:
        if not isinstance(p, Path):
            continue
        fill = p.fill if isinstance(p.fill, str) else None
        fill = PRINT_NORMALISE.get(fill.upper(), fill) if fill else fill
        a = f'd="{p.d(tf)}" fill="{fill or "none"}"'
        if fill and p.evenodd:
            a += ' fill-rule="evenodd"'
        if gid:
            a += f' id="{gid}"'
        b = p.box
        d._emit(f"<path {a}/>", (b[0] * PT_MM - dx + d.ox, b[1] * PT_MM - dy + d.oy, b[2] * PT_MM - dx + d.ox, b[3] * PT_MM - dy + d.oy))


def _origin(doc):
    return (min(b[0] for b in doc.boxes), min(b[1] for b in doc.boxes))


def _atom_path(ref_id):
    """Path data of the first path of a library atom as a list of absolute segments (M, L, C, Z) in atom units."""
    import os

    s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "svg", "atom", ref_id + ".svg"), encoding="utf8").read()
    dd = re.search(r'<path d="([^"]+)"', s).group(1)
    toks = re.findall(r"[MLCZ]|-?\d+\.?\d*", dd)
    segs, i = [], 0
    n = {"M": 2, "L": 2, "C": 6, "Z": 0}
    while i < len(toks):
        c = toks[i]
        i += 1
        k = n[c]
        segs.append((c, *[float(v) for v in toks[i:i + k]]))
        i += k
    return segs


def _bubble_path(s, tx, ty, cut_x, fill):
    """The beeldmerk bubble silhouette (shape of py-atom-logo-beeldmerk-watermark) scaled by s, top left at (tx, ty) page mm,
    cut at x = cut_x (page mm). Returns a Path in source points."""
    import pathops

    k = 1 / PT_MM
    segs = []
    for sg in _atom_path("py-atom-logo-beeldmerk-watermark"):
        if sg[0] == "Z":
            segs.append(("Z",))
            continue
        v = list(sg[1:])
        segs.append((sg[0], *[((tx + v[j] * s) if j % 2 == 0 else (ty + v[j] * s)) * k for j in range(len(v))]))
    if segs[-1][0] != "Z":
        segs.append(("Z",))
    xs = [sg[j] for sg in segs if sg[0] != "Z" for j in range(1, len(sg), 2)]
    ys = [sg[j] for sg in segs if sg[0] != "Z" for j in range(2, len(sg), 2)]
    p = Path(segs, fill=fill, box=(min(xs), min(ys), max(xs), max(ys)))
    x1 = cut_x * k
    page = Path([("M", -10.0, -10.0), ("L", x1, -10.0), ("L", x1, 2000.0), ("L", -10.0, 2000.0), ("Z",)], fill=fill, box=(-10.0, -10.0, x1, 2000.0))
    return _from_pathops(pathops.op(_to_pathops(p), _to_pathops(page), pathops.PathOp.INTERSECTION), p)


def _reference_svg(app_id, key, items, title):
    """Same output as printsrc.reference_svg for a prepared item list (the bubble must sit under the page content, so the
    list is assembled here instead of appending extras on top)."""
    info = printsrc.SOURCES[key]
    el = Element(id=app_id, name_nl="", level="app", category="reference", page=1, items=items)
    tf = TF(0.0, 0.0, PT_MM, 0.0, 0.0)
    defs = Defs(prefix=f"{app_id}-ref-")
    body = el.body(tf, defs)
    W, H = info["page_mm"]
    tx, ty = info["trim_off"]
    tw, th = info["trim_mm"]
    dd = "<defs>" + "".join(defs.items) + "</defs>" if defs.items else ""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(W)}mm" height="{fmt(H)}mm" viewBox="0 0 {fmt(W)} {fmt(H)}">\n'
        f"<title>{_esc(title)}</title>\n{dd}"
        f'<g id="{app_id}-reference" data-role="reference">{body}</g>\n'
        f'<g id="trim-guide" visibility="hidden"><rect x="{fmt(tx)}" y="{fmt(ty)}" width="{fmt(tw)}" height="{fmt(th)}" fill="none" stroke="#00A0E0" stroke-width="0.2"/></g>\n'
        "</svg>\n"
    )


# ================================================================================================ A3 storing: new elements
BOX = (17.453, 340.879, 285.508, 385.376)  # centre line of the outline (page mm)
BOX_RX, BOX_RY = 2.966, 1.343  # corner radii, the source box is stretched: not circular
BOX_SW = 1.0322
TRI_THIN = (29.947, 354.681)  # top left of the small outline triangle
HEAD = (60.83, 359.77, 9.1)  # "Storing?" origin x, baseline, size
PHONE = (60.87, 372.97, 8.64)
PHONE_SPACING = -0.17
TEXT_SIZE = 8.64
TEXT_X = 128.946  # origin of the sentence part in the print
TEXT_GAP = TEXT_X - (PHONE[0] + text_width("Bel 085 4011647", PHONE[2], 700, False, PHONE_SPACING))  # space between the phone part and the sentence


@element("py-atom-icon-warning-triangle-thin", "Waarschuwingsdriehoek dun", "atom", "icon", 1, src=A3, status="extracted",
         notes="Small outline warning triangle with exclamation mark, navy (the print blue #2B529F is normalised to the token #1A3580), 22.0 x 18.8 mm, two paths. "
               "Extracted from the A3 storing poster (inside the contact box). It is NOT the library py-atom-icon-warning-triangle scaled down: "
               "compared by overlay at 22.0 mm the print outline is thinner, the corners are rounder and the exclamation mark is smaller and set lower, "
               "so the library icon would print visibly different. Navy: view on a light background.")
def _(src):
    return crop(src, 1, box(29.0, 354.0, 53.0, 374.0), texts=False)


def _contact(d, heading="Storing?", phone="Bel 085 4011647", text="en wij lossen het zo snel mogelijk op"):
    """Outlined contact box in PAGE mm (free coordinates of a tight doc)."""
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-medium")
    x0, y0, x1, y1 = BOX
    d.rect(x0, y0, x1, y1, fill=WHITE, rx=BOX_RX, ry=BOX_RY, stroke=NAVY, sw=BOX_SW, gid="box")
    h = BOX_SW / 2
    d.boxes.append((x0 - h, y0 - h, x1 + h, y1 + h))  # the stroke overhangs the path box
    with d.group("py-atom-icon-warning-triangle-thin"):
        d.place("py-atom-icon-warning-triangle-thin", TRI_THIN[0], TRI_THIN[1])
    d.text(HEAD[0], HEAD[1], heading, size=HEAD[2], fill=NAVY, weight=700, variable="heading")
    d.text(PHONE[0], PHONE[1], phone, size=PHONE[2], fill=NAVY, weight=700, spacing=PHONE_SPACING, variable="phone")
    tx = PHONE[0] + text_width(phone, PHONE[2], 700, False, PHONE_SPACING) + TEXT_GAP
    d.text(tx, PHONE[1], text, size=TEXT_SIZE, fill=NAVY, weight=500, variable="text")


def _contact_doc():
    d = Doc("py-comp-box-storing-contact", "Storingsbox met contact", tight=True)
    _contact(d)
    return d


@element("py-comp-box-storing-contact", "Storingsbox met contact", "comp", "box", 1, src=A3, status="rebuilt",
         variables=("heading", "phone", "text"),
         notes="Outlined box (navy stroke 1.03 mm, white fill, 268.1 x 44.5 mm) with the small outline triangle (py-atom-icon-warning-triangle-thin) and two text lines: "
               "heading Ubuntu Bold 9.1 mm ('Storing?'), then a bold phone part 'Bel 085 4011647' (Ubuntu Bold 8.64 mm, tracking -0.17 mm) followed by the sentence in Ubuntu Medium 8.64 mm. "
               "Text is live: the heading, the phone line and the sentence carry data-variable heading, phone and text; the sentence starts a fixed gap (about 3.4 mm) after the phone line. "
               "The print outlines the two bold lines, size and origin are fitted by overlay (Storing? 9.1 mm, Bel line 8.64 mm with about 2 percent tighter spacing than the font default). "
               "The source box corners are elliptical (2.97 mm wide, 1.34 mm high): the box was stretched in the print, kept as printed. "
               "Rebuilt: composed from the thin triangle atom plus live text. Navy on white: view on a light background.")
def _(src):
    return _contact_doc()


QR_PLATE = 87.889
QR_PLATE_R = 5.769
QR_INSET = 6.18


def _qr_plate(d):
    d.uses("py-tok-color-blauw", "py-tok-color-wit")
    d.rect(0, 0, QR_PLATE, QR_PLATE, fill=NAVY, rx=QR_PLATE_R, gid="plate")
    with d.group("qr-target", data_variable="qr-target"):
        d.placeholder("qr", QR_INSET, QR_INSET, QR_PLATE - QR_INSET, QR_PLATE - QR_INSET, "QR", variable="qr-target", example=QR_URL)


@element("py-comp-qr-plate", "QR plaat navy", "comp", "qr", 1, src=A2, status="rebuilt", variables=("QR target",),
         notes="Navy rounded square 87.89 mm (corner radius 5.77 mm, 6.6 percent) with a 75.5 mm placeholder group (placeholder-qr, data-variable qr-target) for the QR code, "
               "inset 6.18 mm on all sides; the print QR (white modules on navy, modules as vector fills) has the same inset. "
               "The library py-comp-qr-reserveer plate does not match: it is 118.6 mm with a corner radius of 11.95 mm (10 percent) and belongs to a block with slogan and arc. "
               "Rebuilt: construction (rounded rectangle plus placeholder). The placeholder is dashed magenta and not for print: place the QR modules in white on the plate "
               "(inverted codes may fail on older scanners, see py-comp-qr-reserveer). Navy plate: view on a light background.")
def _(src):
    d = Doc("py-comp-qr-plate", "QR plaat navy", tight=True)
    _qr_plate(d)
    return d


# ================================================================================================ A3 storing: application
# measured from the print (page mm); the baselines come from the live spans, the bold texts are fitted to their outlines
LOGO_A3 = (168.2, 26.3, 1.1253)  # lockup top left and scale (library lockup 104.86 mm wide, print 118.0 mm)
TRI_A3 = (23.5, 33.9, 87.0)  # big warning triangle: top left and width
LETOP = (17.45, 162.42, 46.79)  # x, baseline, size of "Let op!" (Ubuntu Bold)
SENT_X = 17.33
SENT_BASE = (220.98, 252.28, 283.59)
SENT_SIZE = 21.95
IS_HET_X = 211.64
GREY_BOX = (59.569, 197.01, 203.633, 231.179, 5.08)  # x0, y0, x1, y1, radius
WWW = (151.5, 409.27, 9.0)  # centre x, baseline, size (Ubuntu Medium)
BUBBLE = (6.069, 111.351, 20.245)  # scale, x, y of the silhouette (fitted to the raster, IoU 0.9998)
SENT_LINES = ("niet mogelijk om op deze", "locatie te parkeren.")


def _a3_template(ctx):
    app_id = "py-app-poster-storing-a3"
    d = ctx.Doc(app_id, "Poster storing A3", trim=TRIM_A3, bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-medium", "py-atom-logo-beeldmerk-watermark")
    d.rect(-3, -3, 300, 423, fill=WHITE, gid="bleed-background")
    s, bx, by = BUBBLE
    bp = _bubble_path(s, bx, by, 303.0, NAVY)
    d.path(bp.d(TF(0.0, 0.0, PT_MM, -OFF, -OFF)), tuple(v * PT_MM - OFF for v in bp.box), fill=NAVY, opacity=TINT_OPACITY, gid="background-bubble")
    with d.group("py-comp-lockup-logo-tagline-color"):
        d.place("py-comp-lockup-logo-tagline-color", LOGO_A3[0] - OFF, LOGO_A3[1] - OFF, scale=LOGO_A3[2])
    with d.group("py-atom-icon-warning-triangle"):
        d.place("py-atom-icon-warning-triangle", TRI_A3[0] - OFF, TRI_A3[1] - OFF, w=TRI_A3[2], recolor={"#71CBDF": LIGHT_AQUA_A3})
    d.text(LETOP[0] - OFF, LETOP[1] - OFF, "Let op!", size=LETOP[2], fill=NAVY, weight=700, variable="headline")
    with d.group("sentence"):
        d.text(SENT_X - OFF, SENT_BASE[0] - OFF, "Op", size=SENT_SIZE, fill=NAVY, weight=500, variable="sentence-start")
        x0, y0, x1, y1, r = GREY_BOX
        with d.group("placeholder-location-name", data_placeholder="location-name", data_variable="location-name"):
            d.rect(x0 - OFF, y0 - OFF, x1 - OFF, y1 - OFF, fill=GREY, rx=r, gid="location-box")
        d.variables["location-name"] = "locatie"
        d.text(IS_HET_X - OFF, SENT_BASE[0] - OFF, "is het", size=SENT_SIZE, fill=NAVY, weight=500, variable="sentence-1-end")
        for yb, t, v in zip(SENT_BASE[1:], SENT_LINES, ("sentence-line-2", "sentence-line-3")):
            d.text(SENT_X - OFF, yb - OFF, t, size=SENT_SIZE, fill=NAVY, weight=500, variable=v)
    ox, oy = _origin(_contact_doc())
    with d.group("py-comp-box-storing-contact"):
        d.place("py-comp-box-storing-contact", ox - OFF, oy - OFF, scale=1.0)
    for k, v in (("heading", "Storing?"), ("phone", "Bel 085 4011647"), ("text", "en wij lossen het zo snel mogelijk op")):
        d.variables["contact-" + k] = v
    d.uses("py-atom-icon-warning-triangle-thin")
    d.text(WWW[0] - OFF, WWW[1] - OFF, "www.parkingyou.nl", size=WWW[2], fill=NAVY, weight=500, anchor="middle", variable="url")
    d.guides(*TRIM_A3)
    return d


def _a3_reference(ctx):
    app_id = "py-app-poster-storing-a3"
    src = printsrc.source(A3)

    def omit(p):  # the full page navy rectangle under the white one
        return isinstance(p.fill, str) and p.fill.upper() == "#23398E" and (p.box[2] - p.box[0]) * PT_MM > 300

    # not printsrc.reference_items: its regroup() would put the live text into the 70 percent group of the raster (the raster is not drawn here)
    W, H = printsrc.page_pt(A3)

    def skip(p):
        b = p.box
        return b[2] < 0 or b[0] > W or b[3] < 0 or b[1] > H or omit(p)

    items = crop(src, 1, (-W, -H, 2 * W, 2 * H), partial=True, skip=skip, skip_text=lambda t: "  " in t)
    s, bx, by = BUBBLE
    bubble = _bubble_path(s, bx, by, 303.0, TINT_SRC)
    items.insert(1, bubble)  # directly above the white page rectangle
    # the first sentence line aligns "Op" and "is het" with a run of spaces: write both words at their true positions
    from pyassets.core import font_css

    for b in src.page(1).get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            for sp in l["spans"]:
                txt = "".join(c["c"] for c in sp["chars"])
                if "  " not in txt:
                    continue
                fam, w, it = font_css(sp["font"])
                # split on runs of two or more spaces
                parts, buf, sp_run = [], [], 0
                for c in sp["chars"]:
                    if c["c"] == " ":
                        sp_run += 1
                        buf.append(c)
                        continue
                    if sp_run >= 2 and buf:
                        parts.append(buf)
                        buf = []
                    sp_run = 0
                    buf.append(c)
                parts.append(buf)
                for part in parts:
                    t = "".join(c["c"] for c in part).strip()
                    if not t:
                        continue
                    first = next(c for c in part if c["c"] != " ")
                    items.append(make_text(first["origin"][0], first["origin"][1], t, family=fam, weight=w, italic=it, size=sp["size"], fill="#%06X" % sp["color"]))
    return _reference_svg(app_id, A3, items, f"{app_id}: reference reproduction of posters_297x420_3_1.pdf page 1")


@application("py-app-poster-storing-a3", "Poster storing A3", "poster", trim_mm=TRIM_A3, source=[(A3, [1])], bleed_mm=3.0, status="rebuilt")
def _(ctx):
    d = _a3_template(ctx)
    ref = _a3_reference(ctx)
    return dict(
        reference={"": ref}, template={"": d},
        omitted=["Full page navy rectangle (#23398E, 303 x 428.4 mm) directly under the white page rectangle of the same size: hidden underlay.",
                 "Raster image 740 x 1527 px (indexed, 111.3 to 303.0 mm by 20.1 to 415.8 mm) with the pale bubble: replaced by a vector shape (same silhouette, flat #F7F8FA), "
                 "the raster is not copied.",
                 "Trailing space and the run of spaces in the first sentence span ('Op' + spaces + 'is het'): the words are written at their true positions."],
        copy_corrections=[],
        notes=("A3 297 x 420 mm, the source has the 3 mm bleed (page 303 x 426) and a TrimBox. REBUILT because the large pale bubble in the background is a raster in the source: "
               "it is rebuilt as a vector, the silhouette of the beeldmerk (shape of py-atom-logo-beeldmerk-watermark) scaled by 6.069 with the top left at 111.35 / 20.25 mm "
               "(page mm), cut at the right edge of the page. Fitted to the raster mask (overlap 99.98 percent, so the print bubble is the beeldmerk bubble, uniformly scaled "
               "to a 329.6 mm circle). Colour: the raster is flat #F5F6F9 in its palette and renders as #F7F8FA; the reference uses the rendered value, the template draws the navy token "
               "#1A3580 at 3.5 percent (same result, a tint as in observed rule 8; the library watermark is aqua at 5 percent and would look different). "
               "Library: py-comp-lockup-logo-tagline-color at scale 1.125 (118.0 mm wide), py-atom-icon-warning-triangle at 87.0 mm wide, recoloured to the light aqua sample #83CBE1 "
               "(no token, kept as sampled; the library triangle uses #71CBDF). New: py-comp-box-storing-contact (box, small triangle, two text lines) and py-atom-icon-warning-triangle-thin. "
               "Live text: Let op! Ubuntu Bold 46.79 mm, sentence Ubuntu Medium 21.95 mm (three lines, baseline pitch 31.3 mm), URL Ubuntu Medium 9.0 mm centred (in the source "
               "'Let op!', the contact lines and the URL are outlined and fitted by overlay). The location name is a grey rounded box #EBEBEB (59.6 to 203.6 mm, radius 5.1 mm) "
               "in the source: the template keeps it as the placeholder group placeholder-location-name (data-placeholder and data-variable location-name); "
               "'is het' stays at its printed position, a longer location name needs a reflow (open point). "
               "Colours: the source blues #2B3D91 (text, outline), #374F9E (contact text), #2B529F (small triangle) and #273A7C (logo) are drift, the template uses #1A3580 only. "
               "Open: the contact text colour #374F9E and the text blue #2B3D91 are two different blues on one poster. "
               "Variables: headline, sentence-start, sentence-1-end, sentence-line-2, sentence-line-3, location-name, contact-heading, contact-phone, contact-text, url."),
    )


# ================================================================================================ A2 app download
URL_A2 = (27.7, 27.3, 0.456)  # url comp top left and scale (library comp 221.66 mm wide)
BEELD_A2 = (368.0, 22.1, 0.578)  # beeldmerk top left and scale
WORD_A2 = (346.4, 53.5, 0.988)  # wordmark top left and scale
PHOTO = (65.4, 61.5, 8.7167)  # bubble outline (clip path of the photo): top left and scale of py-atom-shape-bubble-image-mask
HL = (31.05, 502.4, 26.75, 28.2)  # x, baseline line 1, line pitch, size (Ubuntu Bold)
DL = (31.05, 564.15, 22.58)  # x, baseline, size (Ubuntu Regular)
QR_ORIGIN = (314.22, 480.445)


def _a2_template(ctx):
    app_id = "py-app-poster-app-a2"
    d = ctx.Doc(app_id, "Poster app downloaden A2", trim=TRIM_A2, bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-regular")
    d.rect(-3, -3, 423, 597, fill=WHITE, gid="bleed-background")
    with d.group("py-comp-url-chevron"):
        d.place("py-comp-url-chevron", URL_A2[0] - OFF, URL_A2[1] - OFF, scale=URL_A2[2], recolor={"#FFFFFF": NAVY, "#69CADA": LIGHT_AQUA_A2})
    with d.group("logo-stacked"):
        d.place("py-atom-logo-beeldmerk-color", BEELD_A2[0] - OFF, BEELD_A2[1] - OFF, scale=BEELD_A2[2])
        d.place("py-atom-logo-wordmark-color", WORD_A2[0] - OFF, WORD_A2[1] - OFF, scale=WORD_A2[2])
    with d.group("placeholder-photo", data_placeholder="photo", data_variable="photo"):
        d.place("py-atom-shape-bubble-image-mask", PHOTO[0] - OFF, PHOTO[1] - OFF, scale=PHOTO[2])
    d.variables["photo"] = "foto van handen met telefoon (bubbelvorm)"
    d.text(HL[0] - OFF, HL[1] - OFF, "Makkelijk parkeren", size=HL[3], fill=NAVY, weight=700, variable="headline-1")
    d.text(HL[0] - OFF, HL[1] + HL[2] - OFF, "vanuit je broekzak", size=HL[3], fill=NAVY, weight=700, variable="headline-2")
    d.text(DL[0] - OFF, DL[1] - OFF, "Download nu onze app", size=DL[2], fill=NAVY, weight=400, variable="subline")
    with d.group("py-comp-qr-plate"):
        d.place("py-comp-qr-plate", QR_ORIGIN[0] - OFF, QR_ORIGIN[1] - OFF, scale=1.0)
    d.variables["qr-target"] = QR_URL
    d.guides(*TRIM_A2)
    return d


def _a2_reference(ctx):
    app_id = "py-app-poster-app-a2"
    src = printsrc.source(A2)

    def omit(p):  # navy bubble under the photo (hidden)
        return isinstance(p.fill, str) and p.fill.upper() == "#2A3282" and (p.box[2] - p.box[0]) * PT_MM > 300

    items = printsrc.reference_items(A2, 1, omit=omit)
    clip = [c for c in src.clips(1, (-100, -100, 2000, 2000)) if len(c.segs) == 10 and (c.box[2] - c.box[0]) * PT_MM > 300][0]
    clip.fill = GREY
    clip.tag = ""
    from pyassets.core import Group

    items.insert(1, Group(items=[clip], opacity=1.0, gid="placeholder-photo"))
    return _reference_svg(app_id, A2, items, f"{app_id}: reference reproduction of posters_420x594_3_1.pdf page 1")


@application("py-app-poster-app-a2", "Poster app downloaden A2", "poster", trim_mm=TRIM_A2, source=[(A2, [1])], bleed_mm=3.0, status="rebuilt")
def _(ctx):
    d = _a2_template(ctx)
    ref = _a2_reference(ctx)
    return dict(
        reference={"": ref}, template={"": d},
        omitted=["Photo: JPEG 824 x 988 px (hands holding a phone, 64.8 to 379.8 mm by 60.9 to 438.6 mm) clipped to the bubble outline: not copied. "
                 "The reference shows the clip outline as a flat #EBEBEB placeholder (group placeholder-photo).",
                 "Navy bubble fill (#2A3282, same outline as the photo clip, 313.8 x 378.6 mm) directly under the photo: hidden underlay, not drawn.",
                 "Two white specks (0.1 mm) next to the QR code at x 358 / y 524 mm: kept in the reference (part of the source), no meaning."],
        copy_corrections=[],
        notes=("A2 420 x 594 mm, the source has the 3 mm bleed (page 426 x 600) and a TrimBox. REBUILT in the template: the headline and the subline are outlined in the source and "
               "are rebuilt as live Ubuntu (Bold 28.2 mm for both headline lines, line pitch 26.75 mm, Regular 22.58 mm for the subline; fitted by overlay, width and height agree). "
               "The only listed font in the source is Helvetica for the QR, there is no live text. "
               "Library: py-comp-url-chevron at scale 0.456 (white text and chevron recoloured to navy and the light aqua sample #8CCDDF; the library chevron is #69CADA), "
               "py-atom-shape-bubble-image-mask at scale 8.717 (the photo clip outline has the same bubble shape; the tail tip differs by under 2 mm), "
               "py-atom-logo-beeldmerk-color (scale 0.578) and py-atom-logo-wordmark-color (scale 0.988). The library stacked logo py-atom-logo-stacked-color is NOT used: "
               "the print has 6.3 mm between the beeldmerk and the wordmark, the library 3.0 mm, so the two atoms are placed separately (group logo-stacked). "
               "New: py-comp-qr-plate (navy plate 87.9 mm, radius 5.77 mm): the plate of py-comp-qr-reserveer (118.6 mm, radius 11.95 mm) does not match. "
               "Reference: faithful, QR modules as vector fills (white on navy, inverted), photo as flat placeholder. Template: placeholder-photo (data-variable photo, library afbeeldingsmasker) "
               "and the QR as placeholder group inside the plate (data-variable qr-target, example " + QR_URL + "). "
               "Colours: source blues #2A3282 (text, QR plate) and #23398E (logo) are drift, the template uses #1A3580; the chevron light aqua is kept as sampled. "
               "Variables: url-line-1, url-line-2 (in the placed url component), headline-1, headline-2, subline, photo, qr-target."),
    )
