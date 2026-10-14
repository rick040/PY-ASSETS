"""Maashaven pyloon (Maashaven.pdf, 400 x 1000 mm panel, 3 mm bleed): third-party badge marks, badge containers, the print
components, the print product variant and the application (reference plus template).

Coordinates in this module are PAGE mm (origin top left of the MediaBox, 406 x 1006); the trim corner sits at (3, 3).
Components are tight Docs in page mm; the panel composer converts to trim relative mm (page minus 3).
"""
from functools import lru_cache

from pyassets import printsrc
from pyassets.apps import application
from pyassets.compose import Doc
from pyassets.core import (GRADIENT_STOPS, PRINT_NORMALISE, PT_MM, Defs, Gradient, Path, TF, Text, _from_pathops, _to_pathops, fmt,
                           items_box, make_text)
from pyassets.registry import crop, element

KEY = "maashaven"
TRIM_OFF = 3.0  # trim corner inside the page (mm)
BLUE = "#1A3580"
BLACK = "#1D1D1B"
WHITE = "#FFFFFF"
QR_URL = "https://parkingyou.nl/nl/locaties/rotterdam/parking-maashaven/id=129"
TERMS_URL = "www.parkingyou.nl/algemene-voorwaarden"
THIRD = "Third party reference only: source the official file, do not redraw."

box = printsrc.box_mm


def _src():
    return printsrc.source(KEY)


# ------------------------------------------------------------------------------------------------ helpers
def emit(d, items, dx=0.0, dy=0.0, gid=None):
    """Write extracted source Paths (points) into a Doc. (dx, dy) = page mm that maps to the Doc origin."""
    tf = TF(0.0, 0.0, PT_MM, d.ox - dx, d.oy - dy)
    for p in items:
        if not isinstance(p, Path):
            continue
        fill = p.fill if isinstance(p.fill, str) else None
        stroke = p.stroke if isinstance(p.stroke, str) else None
        fill = PRINT_NORMALISE.get(fill.upper(), fill) if fill else fill  # also when called outside the element build context
        stroke = PRINT_NORMALISE.get(stroke.upper(), stroke) if stroke else stroke
        a = f'd="{p.d(tf)}" fill="{fill or "none"}"'
        if fill and p.evenodd:
            a += ' fill-rule="evenodd"'
        if fill and p.fill_opacity < 0.999:
            a += f' fill-opacity="{fmt(p.fill_opacity)}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{fmt(p.width * PT_MM)}"'
            if p.cap == 1:
                a += ' stroke-linecap="round"'
            elif p.cap == 2:
                a += ' stroke-linecap="square"'
            if p.join == 1:
                a += ' stroke-linejoin="round"'
            elif p.join == 2:
                a += ' stroke-linejoin="bevel"'
        if gid:
            a += f' id="{gid}"'
        b = p.bbox
        bx_ = (b[0] * PT_MM - dx + d.ox, b[1] * PT_MM - dy + d.oy, b[2] * PT_MM - dx + d.ox, b[3] * PT_MM - dy + d.oy)
        d._emit(f"<path {a}/>", bx_)


def origin(doc):
    """Top left of a tight Doc in its own (page mm) coordinates."""
    return (min(b[0] for b in doc.boxes), min(b[1] for b in doc.boxes))


def place_var(d, ref_id, x, y, rename=None, texts=None, **kw):
    """place() a library comp, rename its data-variable names (so five bars do not all carry `title`) and replace example
    texts (a placed SVG is static, the template carries the example values of this application)."""
    from pyassets.core import _esc

    n = len(d._stack[-1])
    r = d.place(ref_id, x, y, **kw)
    frag = d._stack[-1][n]
    for old, new in (rename or {}).items():
        frag = frag.replace(f'data-variable="{old}"', f'data-variable="{new}"')
    for old, new in (texts or {}).items():
        frag = frag.replace(f">{_esc(old)}<", f">{_esc(new)}<")
    d._stack[-1][n] = frag
    return r


def edge_gradient(c0=BLUE, c1="#32B9CD", n=10):
    """The header edge shading of the source (Sh0): horizontal axis from x -527.007 to 1525.759 pt (page), colour c1 at the
    start and c0 at the end, exponential interpolation with N 1.91 (the function in the PDF is c0 + (1-t)^1.91 (c1-c0)).
    Returns a Gradient in source points."""
    a = [int(c0[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    stops = []
    for k in range(n + 1):
        t = k / n
        m = (1 - t) ** 1.91
        stops.append((round(t, 4), "#%02X%02X%02X" % tuple(round(a[j] + m * (b[j] - a[j])) for j in range(3))))
    return Gradient(-527.007, 0.0, 1525.759, 0.0, tuple(stops))


def _items_origin_mm(bbox_mm, **kw):
    its = crop(_src(), 1, box(*bbox_mm), **kw)
    b = items_box(its)
    return b[0] * PT_MM, b[1] * PT_MM


# ------------------------------------------------------------------------------------------------ third-party marks (white mark only)
MARKS = {
    # id: (name_nl, category, bbox mm of the white mark (excludes the navy badge), crop kwargs)
    "py-atom-payment-maestro-badge": ("Maestro (witte badgeversie)", "payment", (17, 566, 48, 589), {}),
    "py-atom-payment-mastercard-badge": ("Mastercard (witte badgeversie)", "payment", (62, 567, 91, 588), {}),
    "py-atom-payment-visa": ("VISA", "payment", (104, 571, 136, 585), {}),
    "py-atom-payment-vpay": ("V PAY", "payment", (155, 563, 176, 592), {}),
    "py-atom-partner-easypark": ("EasyPark", "partner", (217, 565, 239, 591), {}),
    "py-atom-partner-parkbee": ("ParkBee", "partner", (254, 572, 289, 583), {}),
    "py-atom-partner-myway": ("MyWay", "partner", (301, 566, 330, 589), {}),
    "py-atom-partner-mobian": ("Mobian", "partner", (344, 562, 374, 594), {"outline_fonts": ("ArialMT",)}),
}
MARK_NOTES = {
    "py-atom-partner-easypark": "The e mark in the partner row is EasyPark (confirmed by the owner). ",
    "py-atom-partner-mobian": "The word MOBIAN is live ArialMT in the source and is outlined here. ",
    "py-atom-payment-maestro-badge": "Older wordmark version, differs from the library colour mark py-atom-payment-maestro. ",
    "py-atom-payment-mastercard-badge": "Older wordmark version, differs from the library colour mark py-atom-payment-mastercard. ",
}


def _reg_mark(eid, name, cat, bb, kw):
    @element(eid, name, "atom", cat, 1, src=KEY, variables=("colour",), tags=("third-party",), status="extracted",
             notes=MARK_NOTES.get(eid, "") + "White mark only, without the navy badge, taken from the Maashaven print. " + THIRD +
                   " White on transparent: view on a dark background.")
    def _(src):
        return crop(src, 1, box(*bb), texts=False, **kw)


for _eid, (_n, _c, _bb, _kw) in MARKS.items():
    _reg_mark(_eid, _n, _c, _bb, _kw)


# ------------------------------------------------------------------------------------------------ badge containers
@element("py-atom-badge-round-navy", "Ronde badge navy", "atom", "badge", 1, src=KEY, variables=("colour",), status="extracted",
         notes="Container only: 36 mm disc in navy (the Maashaven print draws the payment badges in the token blue 100/83/0/17). "
               "The mark goes on top (see py-comp-pyloon-payment-row-badges).")
def _(src):
    return crop(src, 1, box(14, 559, 51, 596), texts=False, skip=lambda p: p.fill != BLUE)[:1]


@element("py-atom-badge-square-navy", "Vierkante badge navy", "atom", "badge", 1, src=KEY, variables=("colour",), status="extracted",
         notes="Container only: 36 mm square with corner radius 7.94 mm (22 percent), navy. The mark goes on top.")
def _(src):
    return crop(src, 1, box(209, 559, 246.5, 596), texts=False, skip=lambda p: p.fill != BLUE)[:1]


# badge positions in page mm (top left of each 36 mm badge)
ROUND_X = (14.4, 58.6, 102.8, 147.3)
ROUND_IDS = ("py-atom-payment-maestro-badge", "py-atom-payment-mastercard-badge", "py-atom-payment-visa", "py-atom-payment-vpay")
SQUARE_X = (209.7, 253.6, 297.4, 341.3)
SQUARE_IDS = ("py-atom-partner-easypark", "py-atom-partner-parkbee", "py-atom-partner-myway", "py-atom-partner-mobian")
BADGE_Y = 559.4
BADGE_Y_SQ = 559.5
DIVIDER_X = 196.495
DIVIDER_Y = (564.922, 593.288)


# ------------------------------------------------------------------------------------------------ section bar
BAR_H = 35.148
BAR_W = 400.0
BAR_TITLE_X = 14.792 - TRIM_OFF  # 11.792 from the trim edge (14.792 on the page)
BAR_TITLE_DY = 25.787  # baseline below the bar top
BAR_TOPS = {"openingstijden": 241.084, "tarieven": 366.657, "betalingsmogelijkheden": 514.631,
            "calamiteiten": 739.873, "algemene-voorwaarden": 847.276}  # page mm
BAR_TITLES = {"openingstijden": "Openingstijden", "tarieven": "Tarieven", "betalingsmogelijkheden": "Betalingsmogelijkheden",
              "calamiteiten": "Calamiteiten", "algemene-voorwaarden": "Algemene voorwaarden"}


def _section_bar(title="Openingstijden"):
    d = Doc("py-comp-section-bar", "Sectiebalk", tight=True)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-bold", "py-tok-gradient-verloop")
    # optional verloop fill: gradient is defined, switch the fill variable to url(#py-comp-section-bar-verloop)
    stops = "".join(f'<stop offset="{fmt(o)}" stop-color="{c}"/>' for o, c in GRADIENT_STOPS)
    d.defs["py-comp-section-bar-verloop"] = (
        f'<linearGradient id="py-comp-section-bar-verloop" gradientUnits="userSpaceOnUse" x1="0" y1="{fmt(BAR_H / 2)}" '
        f'x2="{fmt(BAR_W)}" y2="{fmt(BAR_H / 2)}">{stops}</linearGradient>')
    d.rect(0, 0, BAR_W, BAR_H, fill=BLUE, gid="bar", variable="fill", example=BLUE)
    d.text(BAR_TITLE_X, BAR_TITLE_DY, title, size=21.167, fill=WHITE, weight=700, variable="title")
    return d


@element("py-comp-section-bar", "Sectiebalk (titel variabel)", "comp", "pyloon", 1, src=KEY, status="rebuilt",
         variables=("title", "fill"),
         notes="One generic bar, 400 x 35.15 mm, navy token #1A3580 (solid in the print), title live Ubuntu Bold 21.17 mm white, "
               "baseline 25.79 mm below the top, left edge at 11.79 mm from the trim edge (14.79 mm on the page, which includes the 3 mm bleed). "
               "The print draws the bar 415.8 mm wide so that it runs through the bleed; templates extend it into the bleed. "
               "Variable fill: solid (default) or verloop: set the bar fill to url(#py-comp-section-bar-verloop), "
               "a horizontal blauw to aqua gradient defined in this file (py-tok-gradient-verloop). "
               "The five title bound gradient bars py-comp-pyloon-section-bar-* stay unchanged.")
def _(src):
    return _section_bar()


# ------------------------------------------------------------------------------------------------ opening hours and tariffs
COL_L = 25.088  # page mm, left text column
COL_R = 388.7  # right edge of the right column (hours and prices)
ROW_PITCH = 21.167  # 1.2 x 17.639
TXT = 17.639
HOURS_Y0 = 300.502
TARIFF_Y0 = 426.074
HOURS_ROWS = [("Maandag t/m vrijdag", "07:00 - 23:00 uur"), ("Zaterdag", "09:00 - 18:00 uur"), ("Zondag", "09:00 - 17:00 uur")]
TARIFF_ROWS = [("Per 60 minuten", "€ 8,00"), ("Dagtarief", "€ 50,00"), ("Verloren kaart", "€ 50,00"),
               ("Dagtarief met reservering", "€ 25,00")]
TARIFF_HIGHLIGHT = 4  # row number (1 based), navy in the print


def hours_block(d, dx=0.0, dy=0.0, rows=HOURS_ROWS):
    d.uses("py-tok-color-zwart", "py-tok-type-ubuntu-medium")
    for i, (day, hrs) in enumerate(rows):
        y = HOURS_Y0 + i * ROW_PITCH - dy
        with d.group(f"hours-row-{i + 1}"):
            d.text(COL_L - dx, y, day, size=TXT, fill=BLACK, weight=500, variable=f"day-{i + 1}")
            d.text(COL_R - dx, y, hrs, size=TXT, fill=BLACK, weight=500, anchor="end", variable=f"hours-{i + 1}")


def tariff_block(d, dx=0.0, dy=0.0, rows=TARIFF_ROWS, highlight=TARIFF_HIGHLIGHT):
    d.uses("py-tok-color-zwart", "py-tok-color-blauw", "py-tok-type-ubuntu-medium")
    for i, (lab, price) in enumerate(rows):
        y = TARIFF_Y0 + i * ROW_PITCH - dy
        col = BLUE if i + 1 == highlight else BLACK
        with d.group(f"tariff-row-{i + 1}", data_highlighted=str(i + 1 == highlight).lower()):
            d.text(COL_L - dx, y, lab, size=TXT, fill=col, weight=500, variable=f"label-{i + 1}")
            d.text(COL_R - dx, y, price, size=TXT, fill=col, weight=500, anchor="end", variable=f"price-{i + 1}")
    d.variables["highlighted-row"] = str(highlight)


def _hours():
    d = Doc("py-comp-pyloon-opening-hours-multirow", "Openingstijden meerdere rijen", tight=True)
    hours_block(d)
    return d


def _tariffs():
    d = Doc("py-comp-pyloon-tariff-rows", "Tariefrijen", tight=True)
    tariff_block(d)
    return d


@element("py-comp-pyloon-opening-hours-multirow", "Openingstijden meerdere rijen", "comp", "pyloon", 1, src=KEY, status="rebuilt",
         variables=("days", "hours"),
         notes="Variant of py-comp-pyloon-opening-hours (which stays untouched): three day rows without the subscriber note. "
               "Live Ubuntu Medium 17.64 mm in black token #1D1D1B (the print uses rich black, drift), row pitch 21.17 mm (1.2 x size). "
               "Real columns: day left aligned, hours right aligned (text-anchor end at the right edge); the print aligns them with runs of spaces, "
               "which break when a text changes. Rebuilt for that reason.")
def _(src):
    return _hours()


@element("py-comp-pyloon-tariff-rows", "Tariefrijen", "comp", "pyloon", 1, src=KEY, status="rebuilt",
         variables=("rows", "highlighted row"),
         notes="Label left, price right, same style and columns as py-comp-pyloon-opening-hours-multirow. Four rows as printed: Per 60 minuten 8,00, "
               "Dagtarief 50,00, Verloren kaart 50,00, Dagtarief met reservering 25,00 (highlighted in navy). Each row is a group "
               "tariff-row-N with data-highlighted. Rebuilt for real columns (the print uses runs of spaces).")
def _(src):
    return _tariffs()


# ------------------------------------------------------------------------------------------------ header band
def _header(src):
    import pathops

    from pyassets.core import rounded_rect_segs

    d = Doc("py-comp-pyloon-header-band-plain", "Kopband zonder dak", tight=True)
    d.uses("py-tok-gradient-verloop", "py-tok-color-blauw")
    clip = [c for c in src.clips(1, box(-1, -1, 407, 121)) if abs(c.seq - 1.5) < 0.1][0]
    g = edge_gradient()
    defs = Defs(prefix="py-comp-pyloon-header-band-plain-")
    ref = defs.gradient(g, TF(0.0, 0.0, PT_MM, 0.0, 0.0))
    d.defs["py-comp-pyloon-header-band-plain-grad1"] = defs.items[0]
    clip.fill = ref
    # navy ellipse of the print, cut to the page
    ell = [p for p in src.paths(1, (-4000, -4000, 5000, 400), partial=True) if p.box[1] < -400 and p.box[3] < 340][0]
    page = Path(rounded_rect_segs(0.0, 0.0, 1150.866, 340.0), fill=ell.fill, box=(0, 0, 1150.866, 340))
    cut = _from_pathops(pathops.op(_to_pathops(ell), _to_pathops(page), pathops.PathOp.INTERSECTION), ell)
    with d.group("header-edge"):
        emit(d, [clip])
    with d.group("header-navy"):
        emit(d, [cut])
    # plain P: the library atom (live text, 91.72 mm) at the position of the print (text origin 169.263, 90.779)
    d.place("py-atom-symbol-p-plain", 169.263 + 7.338, 90.779 - 64.297, scale=1.0)
    return d


@element("py-comp-pyloon-header-band-plain", "Kopband zonder dak", "comp", "pyloon", 1, src=KEY, status="rebuilt",
         notes="Navy header with the plain P (py-atom-symbol-p-plain, white 91.72 mm) and a convex curved lower edge with the thin blauw to aqua "
               "gradient edge. 406 mm wide and 118.8 mm high: it includes the 3 mm bleed at the left, right and top (the trim starts at x 3, y 3 "
               "inside this element; place it at -3, -3 relative to the trim corner). 115.9 mm of navy ends 2.9 mm above the lowest point of the edge. "
               "The edge is a Sh0 shading in the source (the clip path is the exact outline, the navy ellipse is cut to the page). "
               "Rebuilt: the shading becomes a real vector gradient with the exact axis and exponential curve of the PDF (horizontal, aqua at the left, "
               "navy at the right) written in the token colours of py-tok-gradient-verloop (#1A3580 to #32B9CD); the navy shape is "
               "an ellipse cut to the page, the P is a library atom. Handbook band: py-comp-pyloon-header-band (225 mm, with roof).")
def _(src):
    return _header(src)


# ------------------------------------------------------------------------------------------------ location lockup
LOCATION = "Maashaven"


def _lockup(src, name=LOCATION):
    d = Doc("py-comp-pyloon-location-lockup-stacked", "Locatielockup gestapeld", tight=True)
    d.uses("py-atom-logo-beeldmerk-color", "py-atom-logo-wordmark-color", "py-tok-color-blauw", "py-tok-type-ubuntu-bold")
    with d.group("logo"):
        emit(d, crop(src, 1, box(19, 146, 225, 219), texts=False))
    d.text(85.944, 205.987, name, size=38.464, fill=BLUE, weight=700, variable="location-name")
    d.boxes.append((289.9, 176.1, 289.9, 206.5))  # keep the last glyph of the default name inside the viewBox
    return d


@element("py-comp-pyloon-location-lockup-stacked", "Locatielockup gestapeld", "comp", "pyloon", 1, src=KEY, status="rebuilt",
         variables=("location name",),
         notes="Beeldmerk and parkingyou wordmark with the location name stacked below the wordmark (Ubuntu Bold 38.46 mm navy, live text). "
               "The logo paths are taken from the print as drawn: the beeldmerk is the shape of py-atom-logo-beeldmerk-color at 1.474x "
               "(53.1 x 64.0 mm) and the wordmark the shape of py-atom-logo-wordmark-color at 2.072x (134.2 mm wide). "
               "Proportion drift: wordmark width is 2.10 x the beeldmerk height here, 2.55 x in the library horizontal logo "
               "(py-atom-logo-horizontal-color), so the wordmark is about 18 percent smaller relative to the beeldmerk. "
               "Not the library logo: do not replace by it without a decision. Rebuilt: logo paths as drawn plus live name text.")
def _(src):
    return _lockup(src)


# ------------------------------------------------------------------------------------------------ payment and partner badges
def _badge_origin(x):
    its = crop(_src(), 1, box(x - 1, 559, x + 37, 596), texts=False, skip=lambda p: abs((p.box[2] - p.box[0]) * PT_MM - 36) > 0.3)
    b = its[0].box
    return b[0] * PT_MM, b[1] * PT_MM


def badges_block(d, show=None):
    """Four round badges, divider, four square badges with the third-party marks. `show` = ids of marks to include (default all)."""
    d.uses("py-tok-color-blauw")
    allids = list(ROUND_IDS) + list(SQUARE_IDS)
    show = allids if show is None else show
    for i, (x, mid) in enumerate(zip(ROUND_X, ROUND_IDS)):
        if mid not in show:
            continue
        slug = mid.split("-", 3)[3]
        with d.group(f"badge-{slug}", data_badge=slug):
            bx_, by_ = _badge_origin(x)
            d.place("py-atom-badge-round-navy", bx_, by_)
            mx, my = _items_origin_mm(MARKS[mid][2], **MARKS[mid][3])
            d.place(mid, mx, my)
    d.line(DIVIDER_X, DIVIDER_Y[0], DIVIDER_X, DIVIDER_Y[1], stroke=BLUE, sw=0.9 * PT_MM, gid="divider")
    for i, (x, mid) in enumerate(zip(SQUARE_X, SQUARE_IDS)):
        if mid not in show:
            continue
        slug = mid.split("-", 3)[3]
        with d.group(f"badge-{slug}", data_badge=slug):
            bx_, by_ = _badge_origin(x)
            d.place("py-atom-badge-square-navy", bx_, by_)
            mx, my = _items_origin_mm(MARKS[mid][2], **MARKS[mid][3])
            d.place(mid, mx, my)
    d.variables["badges"] = ", ".join(m.split("-", 3)[3] for m in show)


def _badges(src):
    d = Doc("py-comp-pyloon-payment-row-badges", "Betaalrij met badges", tight=True)
    badges_block(d)
    return d


@element("py-comp-pyloon-payment-row-badges", "Betaalrij met badges", "comp", "pyloon", 1, src=KEY, status="rebuilt",
         variables=("which badges",),
         notes="Variant of py-comp-pyloon-payment-row (which stays untouched): four round payment badges (Maestro, MasterCard, VISA, V PAY), "
               "a divider (navy line 0.32 mm, 28.4 mm high) and four square partner badges (EasyPark, ParkBee, MyWay, Mobian), 36 mm each, "
               "pitch 44.2 mm round and 43.9 mm square. Composed from py-atom-badge-round-navy, py-atom-badge-square-navy and the third party "
               "reference atoms (which stay reference only: source the official files). Each badge is a group badge-<name> with data-badge, "
               "remove a group to change which badges show. Rebuilt: composed.")
def _(src):
    return _badges(src)


# ------------------------------------------------------------------------------------------------ QR block
def qr_block(d, dx=0.0, dy=0.0, mode="modules"):
    """Reserveer block: slogan text, arc, QR plate and (mode modules) the QR modules or (mode placeholder) a placeholder group.
    (dx, dy) = page mm that maps to the Doc origin."""
    src = _src()
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-regular", "py-tok-type-ubuntu-bold")
    with d.group("slogan"):
        x = 29.023 - dx
        d.text(x, 655.243 - dy, "", size=22.931, fill=BLUE, weight=400, runs=[("Reserveer ", 700), ("je", 400)])
        d.text(x, 679.595 - dy, "parkeerplaats", size=22.931, fill=BLUE, weight=400)
        d.text(x, 703.947 - dy, "voordelig online", size=22.931, fill=BLUE, weight=400)
    with d.group("bracket-arc"):
        emit(d, crop(src, 1, box(189, 626, 215, 727), texts=False), dx, dy)
    with d.group("qr-plate"):
        emit(d, crop(src, 1, box(241, 611, 362, 732), texts=False,
                     skip=lambda p: abs((p.box[2] - p.box[0]) * PT_MM - 118.6) > 0.3), dx, dy)
    if mode == "modules":
        mods = [c for c in src.clips(1, box(240, 610, 365, 735)) if len(c.segs) > 1000]
        for c in mods:
            c.fill = WHITE
        with d.group("qr-modules", data_variable="qr-target"):
            emit(d, mods, dx, dy)
        d.variables["qr-target"] = QR_URL
    else:
        d.placeholder("qr", 250.3 - dx, 619.4 - dy, 354.3 - dx, 723.4 - dy, "QR", variable="qr-target", example=QR_URL)


def _qr(src):
    d = Doc("py-comp-qr-reserveer", "Reserveer QR blok", tight=True)
    qr_block(d, 0.0, 0.0, "modules")
    return d


@element("py-comp-qr-reserveer", "Reserveer QR blok", "comp", "pyloon", 1, src=KEY, status="rebuilt", variables=("QR target",),
         notes="Block 'Reserveer je parkeerplaats voordelig online': slogan in live Ubuntu 22.93 mm navy ('Reserveer' bold, ' je' regular), "
               "bracket arc to the right of the text (stroke 1.94 mm, navy) and the QR plate (navy rounded square 118.6 mm, radius 11.95 mm) "
               "with the QR modules in white (group qr-modules, data-variable qr-target). Sample QR: "
               + QR_URL + ". The modules are a clip path in the source (about 2800 segments), taken with Source.clips and filled white: "
               "an inverted QR (white on navy), which some older scanners fail to read. "
               "The arc is extracted, not the library atom: py-atom-shape-bracket-arc has the same curve (mirrored, scale about 2.1, stroke 0.906 mm "
               "x 2.1 = 1.9 mm) but is one object with its slogan text 'Voordelig parkeren zonder gedoe?', so it cannot be placed alone. "
               "Rebuilt: live text, clip path as fill, composed.")
def _(src):
    return _qr(src)


# ------------------------------------------------------------------------------------------------ the panel (one function for prod and template)
PANEL = (400.0, 1000.0)
COMP_BUILDERS = {
    "py-comp-pyloon-header-band-plain": lambda: _header(_src()),
    "py-comp-pyloon-location-lockup-stacked": lambda: _lockup(_src()),
    "py-comp-section-bar": lambda: _section_bar(),
    "py-comp-pyloon-opening-hours-multirow": lambda: _hours(),
    "py-comp-pyloon-tariff-rows": lambda: _tariffs(),
    "py-comp-pyloon-payment-row-badges": lambda: _badges(_src()),
    "py-comp-qr-reserveer": lambda: _qr(_src()),
}


@lru_cache(maxsize=None)
def _comp_info(cid):
    doc = COMP_BUILDERS[cid]()
    return origin(doc), dict(doc.variables)


def place_comp(d, cid, rename=None, texts=None, page_xy=None):
    """Place a comp of this module at its position in the print (page mm minus the trim offset)."""
    (ox, oy), variables = _comp_info(cid)
    x, y = (ox, oy) if page_xy is None else page_xy
    place_var(d, cid, x - TRIM_OFF, y - TRIM_OFF, rename=rename, texts=texts)
    for k, v in variables.items():
        d.variables[(rename or {}).get(k, k)] = v


def compose_panel(d, mode="prod"):
    """Compose the Maashaven panel (trim 400 x 1000) into a Doc. mode "prod": QR comp with sample QR; "template": QR placeholder.
    Coordinates are trim relative (page mm minus 3). Bleed (d.bleed) extends the background and the bars."""
    bl = d.bleed
    W, H = PANEL
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-color-zwart", "py-tok-type-ubuntu-regular", "py-tok-type-ubuntu-medium",
           "py-tok-type-ubuntu-bold")
    if bl:
        d.rect(-bl, -bl, W + bl, H + bl, fill=WHITE, gid="bleed-background")
    with d.group("py-comp-pyloon-header-band-plain"):
        place_comp(d, "py-comp-pyloon-header-band-plain")
    with d.group("py-comp-pyloon-location-lockup-stacked"):
        place_comp(d, "py-comp-pyloon-location-lockup-stacked")
    for name, top in BAR_TOPS.items():
        y = top - TRIM_OFF
        with d.group(f"section-bar-{name}"):
            if bl:  # the print draws the bars through the bleed
                d.rect(-bl, y, 0, y + BAR_H, fill=BLUE)
                d.rect(W, y, W + bl, y + BAR_H, fill=BLUE)
            place_comp(d, "py-comp-section-bar", rename={"title": f"title-{name}", "fill": f"fill-{name}"},
                       texts={"Openingstijden": BAR_TITLES[name]}, page_xy=(TRIM_OFF, top))
            d.variables[f"title-{name}"] = BAR_TITLES[name]
    with d.group("py-comp-pyloon-opening-hours-multirow"):
        place_comp(d, "py-comp-pyloon-opening-hours-multirow")
    with d.group("py-comp-pyloon-tariff-rows"):
        place_comp(d, "py-comp-pyloon-tariff-rows")
    with d.group("py-comp-pyloon-payment-row-badges"):
        place_comp(d, "py-comp-pyloon-payment-row-badges")
    if mode == "prod":
        with d.group("py-comp-qr-reserveer"):
            place_comp(d, "py-comp-qr-reserveer")
    else:
        d.uses("py-comp-qr-reserveer")
        with d.group("py-comp-qr-reserveer"):
            qr_block(d, TRIM_OFF, TRIM_OFF, "placeholder")
    # emergency: built live here (the library block py-comp-pyloon-emergency has another size, weight and colour for the number)
    with d.group("emergency"):
        d.text(14.792 - TRIM_OFF, 797.432 - TRIM_OFF, "Bij storing of calamiteiten bel:", size=17.639, fill=BLACK, weight=500)
        d.text(14.792 - TRIM_OFF, 818.599 - TRIM_OFF, "085 4011647", size=17.639, fill=BLUE, weight=700, variable="phone")
    # terms: print copy with live text, corrected copy (library py-comp-pyloon-terms is not used: other size, rewrapped, RVV signs)
    with d.group("terms"):
        lines = ["Op deze parkeervoorziening zijn de algemene voorwaarden voor", "het gebruik van parkeervoorzieningen van toepassing en geldt",
                 "het reglement verkeersregels en verkeerstekens uit de", "wegenverkeerswet.", None,
                 "De algemene voorwaarden zijn na te lezen op:"]
        ys = [900.168, 914.281, 928.394, 942.507, None, 970.733]
        for t, yy in zip(lines, ys):
            if t:
                d.text(14.792 - TRIM_OFF, yy - TRIM_OFF, t, size=12.347, fill=BLACK, weight=500)
        d.text(14.792 - TRIM_OFF, 984.846 - TRIM_OFF, TERMS_URL, size=12.347, fill=BLUE, weight=700, variable="terms-url")
    return d


@element("py-prod-pyloon-laag-front-qr", "Informatiepyloon voorzijde met reservering-QR (printpaneel 400 x 1000)", "prod", "pyloon", 1,
         src=KEY, status="rebuilt",
         variables=("location name", "opening hours", "tariffs", "highlighted tariff row", "badges", "QR target", "phone", "terms URL"),
         notes="Print variant of py-prod-pyloon-laag-front, owner request: the 400 x 1000 mm panel of the Maashaven print (trim size, no bleed here), "
               "composed with the same function as the application template. Differences from the handbook front: plain P header 116 mm, solid navy bars "
               "(py-comp-section-bar, the five py-comp-pyloon-section-bar-* are not used), stacked location lockup, three opening hour rows without the "
               "subscriber note, tariffs per 60 minutes with Verloren kaart, 8 payment and partner badges, the reserve block with QR, no RVV signs. "
               "Calamiteiten and terms are live text built here: py-comp-pyloon-emergency (15.9 mm, number in black medium) and py-comp-pyloon-terms "
               "(9.9 mm, rewrapped, with RVV signs, URL with /nl/) do not match the print, they stay untouched. The copy is corrected "
               "(na te lezen op, wegenverkeerswet); the print has 'na de lezen' and 'wegverkeerswet'. Terms URL as in the print: "
               "www.parkingyou.nl/algemene-voorwaarden. The header comp is 406 x 118.8 mm (3 mm bleed included) and overhangs the trim by 3 mm at the left, "
               "top and right. Example values: Maashaven.")
def _(src):
    d = Doc("py-prod-pyloon-laag-front-qr", "Informatiepyloon voorzijde met reservering-QR", trim=PANEL, bleed=0.0)
    return compose_panel(d, "prod")


# ------------------------------------------------------------------------------------------------ application
def _reference_extra(src):
    """Header edge (shading), navy header shape, P and the QR modules: things that get_drawings does not return as they appear."""
    import copy

    import pathops

    from pyassets.core import rounded_rect_segs

    clip = [c for c in src.clips(1, box(-1, -1, 407, 121)) if abs(c.seq - 1.5) < 0.1][0]
    clip.fill = edge_gradient("#1F4383", "#24BDCD")  # source colours as a viewer shows them (CMYK 100/86/21/4 to 69/1/20/0)
    ell = [p for p in src.paths(1, (-4000, -4000, 5000, 400), partial=True) if p.box[1] < -400 and p.box[3] < 340][0]
    page = Path(rounded_rect_segs(0.0, 0.0, 1150.866, 340.0), fill=ell.fill, box=(0, 0, 1150.866, 340))
    cut = _from_pathops(pathops.op(_to_pathops(ell), _to_pathops(page), pathops.PathOp.INTERSECTION), ell)
    ptxt = make_text(169.263 / PT_MM, 90.779 / PT_MM, "P", family="Ubuntu", weight=700, size=91.722 / PT_MM, fill="#FFFFFF")
    mods = [c for c in src.clips(1, box(240, 610, 365, 735)) if len(c.segs) > 1000]
    for c in mods:
        c.fill = "#FFFFFF"
    return [clip, cut, ptxt] + mods


def _space_run_texts(src):
    """Spans that align columns with runs of spaces: the extractor would measure that as letter spacing. Reproduce each word group at its
    true position instead (source characters), no tracking."""
    from pyassets.core import font_css

    out = []
    for b in src.page(1).get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            for sp in l["spans"]:
                txt = "".join(c["c"] for c in sp["chars"])
                if "  " not in txt:
                    continue
                fam, w, it = font_css(sp["font"])
                col = "#%06X" % sp["color"]
                # split on runs of >= 2 spaces
                cur, spaces = [], 0
                groups = []
                for c in sp["chars"]:
                    if c["c"] == " ":
                        spaces += 1
                        cur.append(c)
                        continue
                    if spaces >= 2 and cur:
                        groups.append([x for x in cur])
                        cur = []
                    spaces = 0
                    cur.append(c)
                groups.append(cur)
                for g in groups:
                    t = "".join(c["c"] for c in g).strip()
                    if not t:
                        continue
                    first = next(c for c in g if c["c"] != " ")
                    out.append(make_text(first["origin"][0], first["origin"][1], t, family=fam, weight=w, italic=it, size=sp["size"], fill=col))
    return out


def _omit(p):
    w = (p.box[2] - p.box[0]) * PT_MM
    y0 = p.box[1] * PT_MM
    if p.box[1] < -400 and p.box[3] < 340:  # the navy ellipse of the header (re-added cut to the page)
        return True
    if isinstance(p.fill, str) and p.fill.upper() == "#FFFFFF" and abs(w - 114.8) < 1.5 and (abs(y0 - 881.0) < 1.0 or abs(y0 - 613.9) < 1.0):
        return True  # white square y 881 (unused) and the white QR rectangle (replaced by its clip path)
    return False


@application("py-app-panel-pyloon-maashaven", "Informatiepaneel pyloon Maashaven", "panel", trim_mm=(400, 1000),
             source=[("maashaven", [1])], bleed_mm=3.0, status="rebuilt")
def _(ctx):
    d = ctx.Doc("py-app-panel-pyloon-maashaven", "Informatiepaneel pyloon Maashaven", trim=PANEL, bleed=3.0)
    compose_panel(d, "template")
    d.guides(*PANEL)
    ref = ctx.reference("maashaven", 1, omit=_omit, outline_fonts=("ArialMT",), skip_text=lambda t: t.strip() == "P" or "  " in t,
                        extra=_reference_extra(_src()) + _space_run_texts(_src()))
    return dict(
        reference={"": ref}, template={"": d},
        omitted=["White 115 mm square at x 237.3 to 352.1, y 881.0 to 995.8 (page mm): white on white, unused.",
                 "White 115.3 mm rectangle at y 613.9 (page mm) that the source clips to the QR modules: replaced by the clip path itself (the modules), so the QR is drawn as vector modules.",
                 "Navy header ellipse (it extends 700 mm beyond the page): re-added cut to the page."],
        copy_corrections=[{"original": "De algemene voorwaarden zijn na de lezen op:", "corrected": "De algemene voorwaarden zijn na te lezen op:"},
                          {"original": "uit de wegverkeerswet", "corrected": "uit de wegenverkeerswet"}],
        notes=("Print panel 400 x 1000 mm with 3 mm bleed (page 406 x 1006). Reference: faithful reproduction in source colours (drifted blues #1F4383 "
               "for header, bars, text and QR plate; token blue #0B3D8A in the badges; rich black as #000000), ArialMT (MOBIAN) outlined, "
               "the header edge shading rebuilt as vector gradient with the exact axis and curve of the PDF, QR modules from the clip path. "
               "Template: token colours only (#1A3580 all blues, #1D1D1B text), live Ubuntu text, every variable has data-variable "
               "(title-<bar>, day-N, hours-N, label-N, price-N, location-name, phone, terms-url), QR as placeholder group inside the navy plate "
               "(variable qr-target, example " + QR_URL + "). Bars run through the bleed; header band comp includes its own bleed. "
               "OPEN: terms URL. The print has www.parkingyou.nl/algemene-voorwaarden, the handbook (3.6) www.parkingyou.nl/nl/algemene-voorwaarden; "
               "the print value is kept as the variable value, the owner decides which one is correct. "
               "Positions: page mm minus 3 mm trim offset (the Phase 1 note 'text starts at 14.8 mm' is the page coordinate: 11.8 mm from the trim edge). "
               "The inverted QR (white on navy) may fail on some scanners; the sample decodes with zxing. "
               "Layout fact: bars 35.15 mm high, rows pitch 21.17 mm (1.2 x 17.64 mm)."))
