"""Stickers: instructie laadkabel (LaadKabel.pdf) and waarschuwing diefstal (StickerDiefstalARtisDruk.pdf).

New atoms: plug in open ring, car with padlock, divider line. New comps: bilingual NL/EN text stack, footer callout bar.
"""
from pyassets import printsrc
from pyassets.apps import application
from pyassets.registry import crop, element

NAVY = "#1A3580"   # py-tok-color-blauw
WHITE = "#FFFFFF"  # py-tok-color-wit
AQUA_LIGHT = "#68CBDB"  # sampled light aqua (CMYK 54/0/14/0), no token

# ---------------------------------------------------------------- source geometry (page mm, origin top left of the MediaBox)
LK_TRIM = 3.0  # LaadKabel: trim offset inside the 256 x 306 page
LK_PLUG = (76.157, 12.854)  # plug icon ink box, top left
LK_LOGO = (107.956, 282.822, 117.132, 293.889)  # beeldmerk of the small logo (9.2 x 11.1 mm)
DF_ICON = (48.533, 13.649)  # padlock plus car ink box, top left
BAR_Y0, BAR_Y1, BAR_R = 256.582, 284.324, 4.23


def run_line(d, cx, base, runs, size, fill, variable):
    """Centred line of mixed weights. Written start anchored at the computed x: text-anchor middle with tspans of another
    font is laid out wrongly by some renderers (cairosvg), so the centring is done here from the Ubuntu advance widths."""
    from pyassets.compose import text_width

    w = sum(text_width(t, size, wt) for t, wt in runs)
    d.text(cx - w / 2, base, "", size=size, fill=fill, weight=400, variable=variable, runs=runs)


# ---------------------------------------------------------------- atoms
@element("py-atom-icon-plug-ring", "Stekker in open ring", "atom", "icon", 1, src="laadkabel",
         variables=("colour",),
         notes="Plug in an open ring, three paths in light aqua (CMYK 54/0/14/0, viewer #68CBDB). Colour kept as sampled: light aqua has no token. "
               "Drawn for navy; the sticker uses it at 103.8 x 97.4 mm. Not the green EV sign.")
def _(src):
    return crop(src, 1, printsrc.box_mm(76, 12, 181, 111), texts=False)


@element("py-atom-icon-car-lock", "Auto met slot", "atom", "icon", 1, src="diefstal",
         variables=("colour car", "colour lock"),
         notes="Car part (navy, normalised to the token #1A3580) plus padlock (light aqua CMYK 54/0/14/0, viewer #68CBDA as sampled, no token). "
               "The white gaps in the car are holes in a compound path, not white shapes: it works on any background where navy is visible. 46.2 x 32.0 mm on the sticker.")
def _(src):
    return crop(src, 1, printsrc.box_mm(48, 13, 95.5, 46), texts=False)


@element("py-atom-line-divider", "Scheidingslijn", "atom", "line", 1, src="laadkabel",
         variables=("colour", "stroke width", "length"),
         notes="Stroked hairline as printed on the laadkabel sticker: white, 2 pt (0.706 mm), 170.6 mm long, flat caps. "
               "The diefstal sticker repeats the pattern in navy at 1 pt (0.353 mm), 127.5 mm: templates recolour and rescale it. "
               "White on transparent: view on a dark background.")
def _(src):
    return crop(src, 1, printsrc.box_mm(42, 201.5, 214, 203), texts=False)


# ---------------------------------------------------------------- comps
@element("py-comp-text-bilingual-nl-en", "Tweetalig tekstblok NL EN", "comp", "text", 1, src="laadkabel",
         variables=("nl text", "en text"),
         notes="Live text and divider of the laadkabel sticker as one block, white, cropped without icon and logo. Ubuntu 21.47 mm (60.9 pt), leading 1.2, centred. "
               "NL: 'Kabel terughangen' bold, 'na gebruik' regular. Divider. EN: 'Return cable' bold plus ' to' regular, 'hook after use.' regular. "
               "Same weight pattern in both languages (key phrase bold, supporting words regular). Text is start anchored at the printed positions; "
               "templates re-centre it. White on transparent: view on a dark background.")
def _(src):
    return crop(src, 1, printsrc.box_mm(20, 130, 236, 270), texts=True)


@element("py-comp-bar-footer-callout", "Voetbalk melding", "comp", "bar", 1, src="diefstal",
         variables=("callout text", "phone number"),
         notes="Navy bar 140 x 27.7 mm, top corners radius 4.23 mm, bottom corners square. In print the bar runs 4.3 mm over the page bottom, so the bar is taller "
               "than its visible part (23.4 mm above the trim). Live text white 7.76 mm: 'Verdachte situatie? Bel' Ubuntu Regular, '0900-8844' Ubuntu Bold.")
def _(src):
    return crop(src, 1, printsrc.box_mm(0, 256, 141, 285), texts=True)


# ---------------------------------------------------------------- application: instructie laadkabel
LK_NL = [[("Kabel terughangen", 700)], [("na gebruik", 400)]]
LK_EN = [[("Return cable", 700), (" to", 400)], [("hook after use.", 400)]]
LK_BASE = [157.31, 183.072, 234.595, 260.357]  # baselines in page mm
LK_SIZE = 21.468
LK_DIV_Y = 202.167


@application("py-app-sticker-instructie-laadkabel", "Instructiesticker laadkabel", "sticker", trim_mm=(250, 300),
             source=[("laadkabel", [1])], bleed_mm=3.0, status="rebuilt",
             cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": 4.2,
                          "note": "Proposal: the source has no cut contour. Corner radius 4.2 mm is borrowed from the diefstal footer bar (4.23 mm); to be confirmed by the owner."})
def _(ctx):
    d = ctx.Doc("py-app-sticker-instructie-laadkabel", "Instructiesticker laadkabel (NL/EN)", trim=(250, 300), bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-regular", "py-tok-type-ubuntu-bold",
           "py-comp-text-bilingual-nl-en", "py-atom-line-divider")
    d.rect(-3, -3, 253, 303, fill=NAVY, gid="background", variable="background-colour", example=NAVY)
    with d.group("py-atom-icon-plug-ring"):
        d.place("py-atom-icon-plug-ring", LK_PLUG[0] - LK_TRIM, LK_PLUG[1] - LK_TRIM, scale=1.0)
    with d.group("py-comp-text-bilingual-nl-en"):
        d.line(42.683 - LK_TRIM, LK_DIV_Y - LK_TRIM, 213.316 - LK_TRIM, LK_DIV_Y - LK_TRIM, WHITE, 0.706, gid="divider")
    with d.group("variables"):
        for i, (runs, base) in enumerate(zip(LK_NL + LK_EN, LK_BASE)):
            name = ("nl-text-%d" if i < 2 else "en-text-%d") % (i % 2 + 1)
            run_line(d, 125.0, base - LK_TRIM, runs, LK_SIZE, WHITE, name)
    with d.group("py-atom-logo-horizontal-white"):
        d.place("py-atom-logo-horizontal-white", 125.0, LK_LOGO[1] - LK_TRIM, h=LK_LOGO[3] - LK_LOGO[1], anchor="tc")
    d.cut_contour(0, 0, 250, 300, rx=4.2)
    d.guides(250, 300)
    return dict(
        reference={"": ctx.reference("laadkabel", 1, omit=lambda p: p.fill == "#BDBFBF" and p.box[2] - p.box[0] > 700)},
        template={"": d},
        omitted=["Hidden full-page grey underlay (CMYK 25/18/20/2, viewer #BDBFBF, 256 x 306 mm) under the blue background; not PY-Grijs, a leftover."],
        copy_corrections=[],
        notes=("Layout measured on LaadKabel.pdf: navy background into the 3 mm bleed, plug icon (light aqua, kept as sampled #68CBDB, no token), NL/EN text "
               "Ubuntu 21.47 mm white leading 1.2 centred, white divider 0.706 mm x 170.6 mm, library logo py-atom-logo-horizontal-white scaled by height "
               "(beeldmerk 11.1 mm, logo about 40 mm wide) centred at the bottom. The source blue is CMYK 100/85.9/6.6/0 (drift); the template uses the token blue. "
               "Variables: NL text lines and EN text lines as live text (the bold phrases are runs). The cut contour is a proposal: no contour in the source, "
               "radius 4.2 mm taken from the diefstal footer."))


# ---------------------------------------------------------------- application: waarschuwing diefstal
DF_CX = 70.0
DF_SIZE_H, DF_SIZE_B, DF_SIZE_F = 21.167, 14.111, 7.761
DF_NL = [[("Auto ", 400), ("op slot", 700), (" en", 400)], [("geen waardevolle", 700)], [("spullen", 700), (" achterlaten", 400)]]
DF_EN = [[("Lock", 700), (" your car and", 400)], [("remove", 700), (" all of your", 400)], [("valuables", 400)]]


@application("py-app-sticker-waarschuwing-diefstal", "Waarschuwingssticker diefstal", "sticker", trim_mm=(140, 280),
             source=[("diefstal", [1])], bleed_mm=3.0, status="rebuilt",
             cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": 4.2,
                          "note": "Proposal: the source has no cut contour. Corner radius 4.2 mm is the radius seen on the footer bar (4.23 mm); to be confirmed by the owner."})
def _(ctx):
    from pyassets.compose import text_width

    d = ctx.Doc("py-app-sticker-waarschuwing-diefstal", "Waarschuwingssticker diefstal (NL/EN)", trim=(140, 280), bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-regular", "py-tok-type-ubuntu-bold",
           "py-comp-text-bilingual-nl-en", "py-comp-bar-footer-callout")
    with d.group("py-atom-icon-car-lock"):
        d.place("py-atom-icon-car-lock", DF_ICON[0], DF_ICON[1], scale=1.0)
    with d.group("variables"):
        d.text(DF_CX, 70.092, "Let op!", size=DF_SIZE_H, fill=NAVY, weight=700, anchor="middle", variable="heading-nl")
        for i, (runs, base) in enumerate(zip(DF_NL, (94.081, 111.014, 127.948)), 1):
            run_line(d, DF_CX, base, runs, DF_SIZE_B, NAVY, f"body-nl-{i}")
    with d.group("py-atom-line-divider"):
        d.line(6.23, 151.649, 133.77, 151.649, NAVY, 0.353, gid="divider")
    with d.group("variables-en"):
        d.text(DF_CX, 181.42, "Please note!", size=DF_SIZE_H, fill=NAVY, weight=700, anchor="middle", variable="heading-en")
        for i, (runs, base) in enumerate(zip(DF_EN, (205.409, 222.342, 239.275)), 1):
            run_line(d, DF_CX, base, runs, DF_SIZE_B, NAVY, f"body-en-{i}")
    # footer bar: top corners r 4.23, bottom square; runs to the bleed edge (the source overshoots the page by 4.3 mm, the bleed is 3 mm)
    yb = 283.0
    with d.group("py-comp-bar-footer-callout"):
        d.path(f"M0 {yb}V{BAR_Y0 + BAR_R:.3f}A{BAR_R} {BAR_R} 0 0 1 {BAR_R} {BAR_Y0}H{140 - BAR_R:.3f}A{BAR_R} {BAR_R} 0 0 1 140 {BAR_Y0 + BAR_R:.3f}V{yb}Z",
               box=(0, BAR_Y0, 140, yb), fill=NAVY, gid="bar")
        gap = text_width(" ", DF_SIZE_F, 700)
        d.text(90.498, 271.287, "Verdachte situatie? Bel", size=DF_SIZE_F, fill=WHITE, anchor="end", variable="callout-text")
        d.text(90.498 + gap, 271.287, "0900-8844", size=DF_SIZE_F, fill=WHITE, weight=700, variable="phone-number")
    d.cut_contour(0, 0, 140, 280, rx=4.2)
    d.guides(140, 280)
    return dict(
        reference={"": ctx.reference("diefstal", 1)},
        template={"": d},
        omitted=["Page 2 of StickerDiefstalARtisDruk.pdf: empty (a 1 mm art box in a corner), not part of the reference.",
                 "The footer bar part that lies below the page (4.3 mm): the reference shows the page only, as a viewer does."],
        copy_corrections=[],
        notes=("White sticker, no background fill: only the footer bar runs into the bottom bleed (template: to the bleed edge, 3 mm; the source overshoots 4.3 mm). "
               "All text is navy token #1A3580 (source drifted blue CMYK 100/86.3/21.5/3.5), Ubuntu, centred, leading 1.2: headings Bold 21.17 mm, body Regular 14.11 mm "
               "with bold keywords 'op slot', 'geen waardevolle spullen', 'Lock', 'remove'. Divider navy 1 pt, 127.5 mm. Footer text white 7.76 mm: callout Regular, phone number Bold. "
               "The padlock stays light aqua (#68CBDA as sampled, no token). Original copy kept, no spelling errors found. Variables: headings, body lines (bold runs), callout text, phone number. "
               "The cut contour is a proposal (no contour in the source)."))
