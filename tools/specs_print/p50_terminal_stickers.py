"""Terminal stickers (TerminalStickers_September2026.pdf): one sheet of 21 stickers for the payment terminal (automaat), 15 applications.

New atoms: info bubble, left arrow, arrow down in a circle, headset and phone icons, phone with QR, QR reader plate, subscription card with barcode,
pass card (third party branding), contactless hand (navy line art). Payment and partner badges reuse the library atoms (py-atom-badge-*, py-atom-payment-*, py-atom-partner-*).
Every sticker is a white sticker with a hairline die line in the source; the template replaces that line by a cut-contour group.
"""
from pyassets import printsrc
from pyassets.apps import APP_META, application
from pyassets.compose import CUT_COLOR, CUT_WIDTH
from pyassets.core import PT_MM, TF, Gradient, Path, _from_pathops, _to_pathops, regroup
from pyassets.registry import crop, element

KEY = "terminal"
NAVY = "#1A3580"   # py-tok-color-blauw
WHITE = "#FFFFFF"  # py-tok-color-wit
BLACK = "#1D1D1B"  # py-tok-color-zwart
SRC = "terminal"
BLEED = 3.0
MARGIN = 1.5  # reference viewBox margin around the die line, mm

box = printsrc.box_mm


# ---------------------------------------------------------------- atoms
def _nostroke(items):
    for it in items:
        if isinstance(it, Path):
            it.stroke = None
    return items


@element("py-atom-icon-info-bubble", "Infobubbel met i", "atom", "icon", 1, src=KEY, variables=("colour",),
         notes="Round speech bubble with the tail at the bottom right and a white lowercase i (live Ubuntu Bold 23.4 mm). 26.5 x 31.9 mm on the sticker. "
               "The bubble path is navy (token), the i is white and sits on the bubble: view on a light background.")
def _(src):
    return crop(src, 1, box(21.5, 28.5, 48.5, 61.5), texts=True)


@element("py-atom-arrow-left-solid", "Pijl links (sticker)", "atom", "arrow", 1, src=KEY, variables=("colour",),
         notes="Chunky left arrow, navy, as used in the round arrow sticker (6.5 mm). The source draws a 0.25 pt black hairline around it; it is left out here.")
def _(src):
    return _nostroke(crop(src, 1, box(133.5, 28.0, 141.0, 35.5), texts=False))


@element("py-atom-icon-arrow-down-circle", "Pijl omlaag in cirkel", "atom", "icon", 1, src=KEY, variables=("colour disc", "colour arrow"),
         notes="Navy disc (7.7 mm) with a white arrow pointing down, drawn for the bankpas invoeren sticker. The navy sticker uses it 1.19 times larger with the colours swapped "
               "(white disc, navy arrow): place with recolor.")
def _(src):
    return crop(src, 1, box(56.5, 134.7, 64.6, 142.8), texts=False)


@element("py-atom-icon-headset-agent", "Servicemedewerker met headset", "atom", "icon", 1, src=KEY, variables=("colour",),
         notes="Customer service agent with headset, navy line and fill, 9 mm. Used next to the phone number on the storing bar.")
def _(src):
    return crop(src, 1, box(18.5, 225.3, 29.0, 237.6), texts=False)


@element("py-atom-badge-icon-headset-navy", "Ronde badge met headset", "atom", "badge", 1, src=KEY, variables=("colour",),
         notes="Navy disc (14.8 mm) with a white agent with headset. Used on the storing pill.")
def _(src):
    return crop(src, 1, box(16.0, 247.5, 31.5, 263.0), texts=False)


@element("py-atom-badge-icon-phone-navy", "Ronde badge met telefoon", "atom", "badge", 1, src=KEY, variables=("colour",),
         notes="Navy disc (14.8 mm) with a handset as a hole in the disc (single compound path, works on any background). Used on the storing pill.")
def _(src):
    return crop(src, 1, box(16.0, 270.0, 31.5, 285.5), texts=False)


@element("py-atom-illustration-phone-qr", "Telefoon met QR", "atom", "illustration", 1, src=KEY, variables=("qr target",),
         notes="Phone outline (17.1 x 30.4 mm) with a QR plate and QR modules. The plate is a navy tint on white, drawn as a transparency group in the source. "
               "The QR modules are an illustration, not a working code. The smaller phone on the scan code sticker is this drawing at 0.885.")
def _(src):
    return regroup(src, 1, crop(src, 1, box(238.5, 104.7, 256.0, 135.5), texts=False))


@element("py-atom-illustration-reader-qr", "QR leesvlak", "atom", "illustration", 1, src=KEY, variables=("qr target",),
         notes="Rounded reader plate (16.7 x 11.4 mm) with navy outline and a QR illustration, as drawn next to the phone on the scan code sticker.")
def _(src):
    return regroup(src, 1, crop(src, 1, box(241.3, 70.1, 258.4, 81.9), texts=False))


@element("py-atom-illustration-card-barcode", "Abonnementspas met barcode", "atom", "illustration", 1, src=KEY, variables=("card title",),
         notes="Subscription pass with a navy header ('Parkeer Abonnement', outlined in the source), a barcode and an aqua button, 20.2 x 29.9 mm. "
               "The header text is outlined, the barcode is an illustration.")
def _(src):
    # a red bar (fill #EB1E26) lies under the navy header in the source: hidden, left out
    return regroup(src, 1, crop(src, 1, box(208.9, 104.7, 229.5, 135.4), texts=False, skip=lambda p: p.fill == "#EB1E26"))


@element("py-atom-illustration-contactless-hand", "Contactloos betalen met hand", "atom", "illustration", 1, src=KEY, variables=("colour",),
         tags=("third-party",),
         notes="Contactless payment line art in navy: oval, waves and a hand holding a card, 59 x 37 mm as a single path. Contactless is a third party mark, "
               "reference only: source the official file. The black variant from the handbook is py-atom-payment-contactless.")
def _(src):
    return crop(src, 1, box(163.0, 233.5, 223.0, 271.0), texts=False)


def _card_pas(src):
    items = []
    clip = [c for c in src.clips(1, box(222.0, 21.0, 257.0, 44.0))][0]
    import copy

    g = copy.copy(clip)
    g.fill = Gradient.for_box(clip.box, "diag", [(0.0, "#0A699F"), (0.5, "#073D63"), (1.0, "#030B13")])  # sampled on the card: top left, centre, bottom right
    g.tag = "rebuilt-gradient"
    items.append(g)
    art = crop(src, 1, box(216.5, 18.0, 261.5, 48.1), texts=False)
    # the star and hexagon pattern (first path) runs 4 mm past the card and is clipped by the card in the source: cut it to the card outline (no clipPath in the library)
    import pathops

    art[0] = _from_pathops(pathops.op(_to_pathops(art[0]), _to_pathops(clip), pathops.PathOp.INTERSECTION), art[0])
    items += regroup(src, 1, art)
    return items


@element("py-atom-illustration-card-pas", "Pas met Philips Stadion", "atom", "illustration", 1, src=KEY, tags=("third-party",), status="rebuilt",
         variables=("card design",),
         notes="Pass card (33.7 x 21.8 mm) as shown on the scan pas sticker: blue to dark gradient, white P under a roof, 'Operated by parkingyou' and the Philips Stadion logo. "
               "The card carries third party branding (Philips Stadion), reference only: source the official files. Rebuilt: the background gradient is a vector gradient from three sampled colours "
               "(the source writes it as a shading, which the vector reader does not export); the star and hexagon pattern (10 percent white) and the logos are source paths.")
def _(src):
    return _card_pas(src)


# ---------------------------------------------------------------- helpers for the applications
def cut_path(d, x0, y0, x1, y1, r=(0, 0, 0, 0), inset=0.2):
    """ThruCut contour with individual corner radii (tl, tr, br, bl), as its own group cut-contour. Trim relative mm."""
    a, b, c, e = x0 + inset, y0 + inset, x1 - inset, y1 - inset
    tl, tr, br, bl = [max(v - inset, 0) if v else 0 for v in r]
    p = f"M{a + tl:.3f} {b:.3f}H{c - tr:.3f}"
    p += f"A{tr:.3f} {tr:.3f} 0 0 1 {c:.3f} {b + tr:.3f}" if tr else ""
    p += f"V{e - br:.3f}"
    p += f"A{br:.3f} {br:.3f} 0 0 1 {c - br:.3f} {e:.3f}" if br else ""
    p += f"H{a + bl:.3f}"
    p += f"A{bl:.3f} {bl:.3f} 0 0 1 {a:.3f} {e - bl:.3f}" if bl else ""
    p += f"V{b + tl:.3f}"
    p += f"A{tl:.3f} {tl:.3f} 0 0 1 {a + tl:.3f} {b:.3f}" if tl else ""
    p += "Z"
    with d.group("cut-contour", data_spot="ThruCut"):
        d.path(p, (a, b, c, e), stroke=CUT_COLOR, sw=CUT_WIDTH)


def rrect(x0, y0, x1, y1, r=(0, 0, 0, 0)):
    """Path d of a rectangle with corner radii (tl, tr, br, bl)."""
    tl, tr, br, bl = r
    p = f"M{x0 + tl:.3f} {y0:.3f}H{x1 - tr:.3f}"
    p += f"A{tr:.3f} {tr:.3f} 0 0 1 {x1:.3f} {y0 + tr:.3f}" if tr else ""
    p += f"V{y1 - br:.3f}"
    p += f"A{br:.3f} {br:.3f} 0 0 1 {x1 - br:.3f} {y1:.3f}" if br else ""
    p += f"H{x0 + bl:.3f}"
    p += f"A{bl:.3f} {bl:.3f} 0 0 1 {x0:.3f} {y1 - bl:.3f}" if bl else ""
    p += f"V{y0 + tl:.3f}"
    p += f"A{tl:.3f} {tl:.3f} 0 0 1 {x0 + tl:.3f} {y0:.3f}" if tl else ""
    return p + "Z"


class Sticker:
    """One sticker of the sheet: die line box in page mm, helpers convert page mm to trim relative mm."""

    def __init__(self, ctx, app_id, title, die, uses=()):
        self.die = die
        self.x0, self.y0, self.x1, self.y1 = die
        self.w, self.h = APP_META[app_id]["trim_mm"]  # exact die size as declared (die box above is rounded to 0.1 mm)
        self.d = ctx.Doc(app_id, title, trim=(self.w, self.h), bleed=BLEED)
        self.d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-regular", *uses)

    def t(self, x, y):
        return x - self.x0, y - self.y0

    def region(self):
        return (self.x0 - MARGIN, self.y0 - MARGIN, self.x1 + MARGIN, self.y1 + MARGIN)

    def text(self, x, y, runs, size, fill, variable, weight=400, italic=False, spacing=0.0):
        x, y = self.t(x, y)
        self.d.text(x, y, "", size=size, fill=fill, weight=weight, italic=italic, spacing=spacing, variable=variable, runs=runs)

    def place(self, ref, x, y, **kw):
        x, y = self.t(x, y)
        return self.d.place(ref, x, y, **kw)

    def bg(self, fill, r=0.0):
        self.d.rect(-BLEED, -BLEED, self.w + BLEED, self.h + BLEED, fill=fill, gid="background", variable="background-colour", example=fill)


def make_ref(ctx, key, st, outline=("ArialMT",), omit=None, under=()):
    return ctx.reference(KEY, 1, region=st.region(), trim_box=st.die, outline_fonts=outline, omit=omit, under=under)


# ---------------------------------------------------------------- applications
CUT_BASE = {"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2}


def _cut(r, note="Proposal: the source has only a 0.25 pt hairline as die line, no ThruCut contour. Radius measured on the die line, to be confirmed by the printer."):
    return dict(CUT_BASE, corner_radius_mm=r, note=note)


SHEET_NOTE = ("Sheet TerminalStickers_September2026.pdf (271 x 391 mm, no bleed, no trim marks): a hairline die line (black, 0.25 to 0.74 pt) around each white sticker. "
              "The template replaces that line by a ThruCut contour 0.2 mm inside the trim and adds a 3 mm bleed. Source blue CMYK 99.5/85/21.4/6.8 (drift, see tokens.json observed): "
              "the template uses the token blue.")


@application("py-app-sticker-terminal-druk-3-seconden", "Terminalsticker druk 3 seconden", "sticker", trim_mm=(56.44, 21.31),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(4.78))
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-druk-3-seconden", "Terminalsticker druk 3 seconden (NL/EN)", (6.7, 4.2, 63.1, 25.5), ("py-tok-type-ubuntu-bold",))
    st.text(12.74 - 0.35, 12.97, [("Druk 3 seconden", 700)], 5.96, NAVY, "text-nl", weight=700, spacing=-0.085)
    st.text(15.35 - 0.6, 20.52, [("Press 3 seconds", 500)], 5.96, NAVY, "text-en", weight=500, italic=True)
    st.d.cut_contour(0, 0, st.w, st.h, rx=4.78)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[],
                copy_corrections=[],
                notes=("White sticker, navy text centred, two lines: 'Druk 3 seconden' bold and 'Press 3 seconds' italic. The source outlines the text; the template sets it as live Ubuntu "
                       "(bold 5.96 mm with slight negative tracking, medium italic 5.96 mm) fitted to the outlined glyphs. The sheet holds the sticker twice, identical. " + SHEET_NOTE))


@application("py-app-sticker-terminal-info", "Terminalsticker info", "sticker", trim_mm=(26.4, 32.0),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt",
             cut_contour=_cut(0, "Proposal: the die contour follows the bubble outline exactly (free shape, no inset); the source has no die line for this sticker. To be confirmed by the printer."))
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-info", "Terminalsticker info (i in bubbel)", (21.7, 29.0, 48.1, 61.0))
    st.d.uses("py-tok-type-ubuntu-bold")
    st.d.variables["colour"] = NAVY
    with st.d.group("py-atom-icon-info-bubble", data_variable="colour"):
        st.place("py-atom-icon-info-bubble", 21.7, 29.0)
    bub = [p for p in printsrc.source(KEY).paths(1, box(21.5, 28.5, 48.5, 61.5)) if p.fill and len(p.segs) > 4][0]
    with st.d.group("cut-contour", data_spot="ThruCut"):
        st.d.path(bub.d(TF(st.x0 / PT_MM, st.y0 / PT_MM, PT_MM, 0.0, 0.0)), (0, 0, st.w, st.h), stroke=CUT_COLOR, sw=CUT_WIDTH)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes="Die cut sticker in the shape of the bubble, navy with a white i, no die line in the source. The cut-contour group is the bubble outline traced from the source path. " + SHEET_NOTE)


def org(x0, y0, x1, y1):
    """Top left (page mm) of the ink of a crop box: where a library atom extracted from that box has to be placed."""
    src = printsrc.source(KEY)
    ps = src.paths(1, box(x0, y0, x1, y1))
    return min(p.box[0] for p in ps) * PT_MM, min(p.box[1] for p in ps) * PT_MM


@application("py-app-sticker-terminal-pijl-links", "Terminalsticker pijl links", "sticker", trim_mm=(12.09, 12.09),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(6.045))
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-pijl-links", "Terminalsticker pijl links (rond)", (131.1, 25.6, 143.2, 37.7))
    st.d.variables["arrow-direction"] = "links"
    with st.d.group("arrow", data_variable="arrow-direction"):
        st.place("py-atom-arrow-left-solid", 133.9, 28.4)
    st.d.cut_contour(0, 0, st.w, st.h, rx=6.045)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes="Round sticker 12.1 mm, navy arrow 6.5 mm, no text. The sheet holds the sticker twice, identical. " + SHEET_NOTE)


@application("py-app-sticker-terminal-scan-pas", "Terminalsticker scan hier je pas", "sticker", trim_mm=(109.0, 33.76),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(4.65))
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-scan-pas", "Terminalsticker scan hier je pas", (152.2, 15.7, 261.2, 49.5), ("py-tok-type-ubuntu-bold",))
    st.text(158.1, 35.5, [("Scan hier je ", 400), ("pas", 700)], 7.62, NAVY, "text")
    st.d.variables["card-image"] = "py-atom-illustration-card-pas"
    with st.d.group("card", data_variable="card-image"):
        st.place("py-atom-illustration-card-pas", 222.6, 21.7)
    st.d.cut_contour(0, 0, st.w, st.h, rx=4.65)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st, under=[_card_pas(printsrc.source(KEY))[0]])}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes=("Text 'Scan hier je pas' (Ubuntu 7.62 mm, 'pas' bold) left, pass card right. The card is a third party branded illustration (Philips Stadion), swap the card group "
                       "for the pass of the location. The card background is a sampled vector gradient (the source shading is not exported by the vector reader, see py-atom-illustration-card-pas), in the reference as well as in the template. "
                       + SHEET_NOTE))


@application("py-app-sticker-terminal-scan-code-qr", "Terminalsticker scan hier je code (telefoon of lezer)", "sticker", trim_mm=(109.0, 33.76),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(4.65))
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-scan-code-qr", "Terminalsticker scan hier je code, QR", (152.4, 59.0, 261.4, 92.8), ("py-tok-type-ubuntu-bold",))
    st.text(158.6, 78.8, [("Scan hier je ", 400), ("code", 700)], 7.62, NAVY, "text")
    st.text(236.8, 77.5, [("of", 400)], 3.88, NAVY, "text-of")
    with st.d.group("py-atom-illustration-phone-qr"):
        st.place("py-atom-illustration-phone-qr", 221.0, 62.6, w=15.1)
    with st.d.group("py-atom-illustration-reader-qr"):
        st.place("py-atom-illustration-reader-qr", 241.5, 70.3)
    st.d.cut_contour(0, 0, st.w, st.h, rx=4.65)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes="Text 'Scan hier je code' (code bold), 'of', then a phone with QR (the library phone at 0.88) and a QR reader plate. " + SHEET_NOTE)


@application("py-app-sticker-terminal-scan-code-abonnement", "Terminalsticker scan hier je code (abonnement of telefoon)", "sticker", trim_mm=(130.67, 38.11),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(4.7))
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-scan-code-abonnement", "Terminalsticker scan hier je code, abonnement", (130.6, 100.9, 261.3, 139.0),
                 ("py-tok-type-ubuntu-bold",))
    st.text(136.1, 123.3, [("Scan hier je ", 400), ("code", 700)], 8.6, NAVY, "text")
    st.text(231.1, 122.0, [("of", 400)], 5.16, NAVY, "text-of")
    with st.d.group("py-atom-illustration-card-barcode"):
        st.place("py-atom-illustration-card-barcode", *org(208.9, 104.7, 229.5, 135.4))
    with st.d.group("py-atom-illustration-phone-qr"):
        st.place("py-atom-illustration-phone-qr", *org(238.5, 104.7, 256.0, 135.5))
    st.d.cut_contour(0, 0, st.w, st.h, rx=4.7)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes="Text 'Scan hier je code' (Ubuntu 8.6 mm, code bold), 'of' (5.16 mm), subscription pass with barcode and phone with QR. Die line 0.5 pt. " + SHEET_NOTE)


@application("py-app-sticker-terminal-bankpas-voorhouden", "Terminalsticker bankpas voorhouden", "sticker", trim_mm=(85.0, 43.0),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(4.7))
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-bankpas-voorhouden", "Terminalsticker bankpas minimaal 3 seconden voorhouden", (16.4, 68.2, 101.4, 111.2),
                 ("py-tok-type-ubuntu-bold",))
    st.bg(NAVY)
    st.text(30.1, 80.9, [("Bankpas minimaal", 400)], 7.06, WHITE, "text-1")
    st.text(19.9, 89.4, [("3 seconden", 700), (" voorhouden", 400)], 7.06, WHITE, "text-2")
    with st.d.group("py-atom-icon-arrow-down-circle"):
        st.place("py-atom-icon-arrow-down-circle", 54.3, 96.5, w=9.2, recolor={NAVY: WHITE, WHITE: NAVY})
    st.d.cut_contour(0, 0, st.w, st.h, rx=4.7)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes="Navy sticker, white text centred ('3 seconden' bold), arrow in a white disc. The arrow icon is the library atom with the colours swapped. Die line 0.5 pt. " + SHEET_NOTE)


@application("py-app-sticker-terminal-bankpas-invoeren", "Terminalsticker bankpas invoeren", "sticker", trim_mm=(69.6, 25.74),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(3.59))
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-bankpas-invoeren", "Terminalsticker bankpas invoeren", (25.8, 119.0, 95.4, 144.7), ("py-tok-type-ubuntu-bold",))
    st.text(31.5, 129.6, [("Bankpas", 700), (" invoeren", 400)], 7.06, NAVY, "text")
    with st.d.group("py-atom-icon-arrow-down-circle"):
        st.place("py-atom-icon-arrow-down-circle", 56.7, 134.9)
    st.d.cut_contour(0, 0, st.w, st.h, rx=3.59)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes="White sticker, navy text ('Bankpas' bold) and a navy disc with a white arrow down. " + SHEET_NOTE)


ROUND = ("py-atom-payment-maestro-badge", "py-atom-payment-mastercard-badge", "py-atom-payment-visa", "py-atom-payment-vpay")
SQUARE = ("py-atom-partner-easypark", "py-atom-partner-parkbee", "py-atom-partner-myway", "py-atom-partner-mobian")


def badge_row(st, badge, marks, xs, y, size):
    k = size / 36.0
    for x, mid in zip(xs, marks):
        slug = mid.split("-", 3)[3]
        with st.d.group(f"badge-{slug}", data_badge=slug):
            st.place(badge, x, y, w=size)
            st.place(mid, x + size / 2, y + size / 2, scale=k, anchor="cc")
    st.d.variables["badges"] = ", ".join(m.split("-", 3)[3] for m in marks)


@application("py-app-sticker-terminal-betaalmerken", "Terminalsticker betaalmerken", "sticker", trim_mm=(104.97, 30.61),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(6.93), tags=["third-party"])
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-betaalmerken", "Terminalsticker betaalmerken", (12.4, 156.3, 117.4, 186.9))
    st.d.uses("py-atom-badge-round-navy")
    with st.d.group("badges", data_variable="badges"):
        badge_row(st, "py-atom-badge-round-navy", ROUND, (18.9, 42.9, 67.0, 91.3), 161.8, 19.6)
    st.d.cut_contour(0, 0, st.w, st.h, rx=6.93)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes=("Four round navy badges (19.6 mm) with Maestro, Mastercard, VISA and V PAY, composed from py-atom-badge-round-navy and the third party mark atoms (reference only, "
                       "source the official files). Each badge is a group badge-<name>: remove a group to change the accepted cards. " + SHEET_NOTE))


@application("py-app-sticker-terminal-partnermerken", "Terminalsticker partnermerken", "sticker", trim_mm=(104.97, 30.61),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(6.93), tags=["third-party"])
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-partnermerken", "Terminalsticker partnermerken", (138.1, 157.6, 243.1, 188.2))
    st.d.uses("py-atom-badge-square-navy")
    with st.d.group("badges", data_variable="badges"):
        badge_row(st, "py-atom-badge-square-navy", SQUARE, (142.7, 167.8, 192.9, 218.0), 162.6, 20.6)
    st.d.cut_contour(0, 0, st.w, st.h, rx=6.93)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes=("Four square navy badges (20.6 mm, radius 22 percent) with EasyPark, ParkBee, MyWay and Mobian, composed from py-atom-badge-square-navy and the third party "
                       "partner atoms (reference only, source the official files). Order on the sheet: EasyPark, ParkBee, MyWay, Mobian. " + SHEET_NOTE))


@application("py-app-sticker-terminal-wacht-lampjes", "Terminalsticker wacht tot alle lampjes groen zijn", "sticker", trim_mm=(123.32, 83.67),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(1.85), tags=["third-party"])
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-wacht-lampjes", "Terminalsticker wacht tot alle lampjes groen zijn", (131.4, 197.9, 254.7, 281.5),
                 ("py-tok-type-ubuntu-bold",))
    st.text(162.1, 212.1, [("Wacht tot alle ", 400)], 9.78, NAVY, "text-1")
    st.text(152.4, 223.9, [("lampjes ", 400), ("groen ", 700), ("zijn", 400)], 9.78, NAVY, "text-2")
    with st.d.group("py-atom-illustration-contactless-hand"):
        st.place("py-atom-illustration-contactless-hand", *org(163.0, 233.5, 223.0, 271.0))
    st.d.cut_contour(0, 0, st.w, st.h, rx=1.85)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes="White sticker, two lines of navy text ('groen' bold) and the contactless line art in navy (third party mark, reference only). " + SHEET_NOTE)


@application("py-app-sticker-terminal-storing-balk", "Terminalsticker storing met telefoonnummer (balk)", "sticker", trim_mm=(91.22, 30.7),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(8.0, "Proposal: the source has only a 0.65 to 0.74 pt hairline; radii measured (top 7.47 mm, bottom 8.58 mm), a single 8 mm radius is used for the contour. To be confirmed by the printer."))
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-storing-balk", "Terminalsticker storing met telefoonnummer (balk)", (12.4, 209.9, 103.6, 240.6),
                 ("py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-medium"))
    st.d.rect(-BLEED, -BLEED, st.w + BLEED, 13.5, fill=NAVY, gid="header-bar", variable="header-colour", example=NAVY)
    st.text(45.2, 220.0, [("Storing?", 500)], 7.06, WHITE, "header-text", weight=500)
    with st.d.group("py-atom-icon-headset-agent"):
        st.place("py-atom-icon-headset-agent", *org(18.5, 225.3, 29.0, 237.6))
    st.text(35.5, 235.3, [("085 401 16 47", 700)], 9.56, NAVY, "phone-number", weight=700)
    cut_path(st.d, 0, 0, st.w, st.h, (7.47, 7.47, 8.58, 8.58))
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes="Navy header with 'Storing?' (white, Ubuntu Medium 7.06 mm) above a white body with the service agent icon and the phone number (navy, Ubuntu Bold 9.56 mm). " + SHEET_NOTE)


@application("py-app-sticker-terminal-storing-nummer", "Terminalsticker storing telefoonnummer (pil)", "sticker", trim_mm=(91.22, 17.7),
             variants=("headset", "telefoon"), source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(8.85))
def _(ctx):
    dies = {"headset": (14.2, 246.5, 105.4, 264.2), "telefoon": (14.2, 269.1, 105.4, 286.8)}
    icons = {"headset": "py-atom-badge-icon-headset-navy", "telefoon": "py-atom-badge-icon-phone-navy"}
    ref, tpl = {}, {}
    for v, die in dies.items():
        st = Sticker(ctx, "py-app-sticker-terminal-storing-nummer", f"Terminalsticker storing telefoonnummer, {v}", die, ("py-tok-type-ubuntu-bold",))
        with st.d.group(icons[v], data_variable="icon"):
            st.place(icons[v], 16.3, die[1] + 1.4)
        st.d.variables["icon"] = v
        st.text(37.3, die[1] + 12.5, [("085 401 16 47", 700)], 9.56, NAVY, "phone-number", weight=700)
        st.d.cut_contour(0, 0, st.w, st.h, rx=8.85)
        st.d.guides(st.w, st.h)
        ref[v] = ctx.reference(KEY, 1, variant=v, region=st.region(), trim_box=die)
        tpl[v] = st.d
    return dict(reference=ref, template=tpl, omitted=[], copy_corrections=[],
                notes="Pill sticker (full radius) with a navy round icon badge (headset or phone) and the phone number in navy Ubuntu Bold 9.56 mm. Two variants on the sheet, same size. " + SHEET_NOTE)


@application("py-app-sticker-terminal-automaat-storing", "Terminalsticker automaat storing met automaatnummer", "sticker", trim_mm=(81.1, 86.1),
             variants=("leeg", "bsg-i1"), source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt",
             cut_contour=_cut(4.63, "Proposal: the source has no die line. The sticker is drawn with all four corners rounded at the header radius (4.63 mm). To be confirmed by the printer."))
def _(ctx):
    dies = {"leeg": (14.4, 296.5, 95.5, 382.6), "bsg-i1": (111.5, 295.1, 192.6, 381.2)}
    ref, tpl = {}, {}
    for v, die in dies.items():
        st = Sticker(ctx, "py-app-sticker-terminal-automaat-storing", f"Terminalsticker automaat storing, {v}", die,
                     ("py-tok-type-ubuntu-medium", "py-atom-logo-horizontal-reverse"))
        dx, dy = die[0], die[1]
        st.d.rect(-BLEED, -BLEED, st.w + BLEED, 26.8, fill=NAVY, gid="header-bar", variable="header-colour", example=NAVY)
        with st.d.group("py-atom-logo-horizontal-reverse"):
            st.place("py-atom-logo-horizontal-reverse", dx + 6.7 + (0.0 if v == "leeg" else 0.2), dy + 5.1 + (0.4 if v == "leeg" else 0.0), w=63.3)
        st.text(dx + 8.0, dy + 37.5, [("Storing?", 400)], 7.76, BLACK, "text-storing")
        st.text(dx + 8.0, dy + 48.1, [("085 - 401 16 47", 500)], 7.76, BLACK, "phone-number", weight=500)
        st.text(dx + 8.0, dy + 65.1, [("Automaatnummer", 400)], 7.76, BLACK, "text-automaatnummer")
        if v == "leeg":
            with st.d.group("placeholder-sticker"):
                st.d.rect(8.1, 67.7, 73.4, 80.8, fill=NAVY, rx=1.91, opacity=0.12, stroke=NAVY, sw=0.25, dash="1.2 0.9")
            st.text(dx + 20.2, dy + 76.3, [("plaats sticker hier", 300)], 5.29, WHITE, "placeholder-text", weight=300)
        else:
            with st.d.group("automaatnummer-bar"):
                st.d.rect(8.2, 67.8, 73.5, 80.85, fill=NAVY, rx=1.91, gid="bar")
            st.text(dx + 30.1, dy + 77.0, [("BSG-i1", 500)], 7.06, WHITE, "automaatnummer", weight=500)
        cut_path(st.d, 0, 0, st.w, st.h, (4.63, 4.63, 4.63, 4.63))
        st.d.guides(st.w, st.h)
        ref[v] = ctx.reference(KEY, 1, variant=v, region=st.region(), trim_box=die, outline_fonts=("ArialMT",))
        tpl[v] = st.d
    return dict(reference=ref, template=tpl, omitted=[], copy_corrections=[],
                notes=("Terminal fault sticker: navy header with the reverse logo, 'Storing?' and the phone number in black (Ubuntu), then 'Automaatnummer' with either a dashed "
                       "'plaats sticker hier' field (variant leeg) or a navy bar with the machine number (variant bsg-i1). The text colour in the source is pure black, the template uses PY-Zwart. "
                       + SHEET_NOTE))


@application("py-app-sticker-terminal-automaatnummer", "Terminalsticker automaatnummer", "sticker", trim_mm=(58.91, 13.05),
             source=[("terminal", [1])], bleed_mm=BLEED, region_references=True, status="rebuilt", cut_contour=_cut(1.82))
def _(ctx):
    st = Sticker(ctx, "py-app-sticker-terminal-automaatnummer", "Terminalsticker automaatnummer", (208.6, 295.9, 267.5, 308.95), ("py-tok-type-ubuntu-medium",))
    st.bg(NAVY)
    st.text(227.3, 305.1, [("BSG-i1", 500)], 7.06, WHITE, "automaatnummer", weight=500)
    st.d.cut_contour(0, 0, st.w, st.h, rx=1.82)
    st.d.guides(st.w, st.h)
    return dict(reference={"": make_ref(ctx, KEY, st)}, template={"": st.d}, omitted=[], copy_corrections=[],
                notes="Navy bar with the machine number in white Ubuntu Medium 7.06 mm (example BSG-i1). The sheet holds the sticker twice, identical. " + SHEET_NOTE)
