"""PM-137 second batch, module p60: slagboom sign (BordSlagboomEVO.pdf), letterhead (Briefpapier_nieuw.pdf) and envelope 220 x 156
(ParkingYou_Envelop_220x156.pdf) with the registered mark atom, the address block and the envelope address line.

All numbers were measured from the source PDFs (page mm, origin top left of the MediaBox; 1 pt = 25.4/72 mm).
"""
from pyassets import printsrc
from pyassets.apps import application
from pyassets.compose import Doc, text_width
from pyassets.core import PT_MM, fmt, _esc
from pyassets.registry import crop, element

NAVY = "#1A3580"
AQUA = "#32B9CD"
LIGHT_AQUA = "#68CBDA"  # sampled (viewer), CMYK 54/0/14/0, no token
WHITE = "#FFFFFF"
MAGENTA = "#ED308A"
LOGO_H = 28.949          # height of the library logo atoms and of the lockup comp at scale 1


def _mm(pt):
    return pt * PT_MM


def _rich(d, x, y, size, runs, anchor="start", gid=None):
    """One live text line with several runs (weight, fill and variable per run). runs = [(text, weight, fill, variable_or_None)].
    Doc.text() takes one fill per element, so the line is written as one <text> with <tspan> per run (reflows with the content)."""
    fam = {300: "Ubuntu Light", 400: "Ubuntu", 700: "Ubuntu"}
    ax, ay = d._p(x, y)
    first = runs[0]
    a = f'x="{fmt(ax)}" y="{fmt(ay)}" font-family="{fam[first[1]]}" font-size="{fmt(size)}"'
    if first[1] == 700:
        a += ' font-weight="bold"'
    if anchor != "start":
        a += f' text-anchor="{anchor}"'
    a += f' fill="{first[2]}"'
    if gid:
        a += f' id="{gid}"'
    parts, wd = [], 0.0
    for text, w, fill, var in runs:
        at = f' font-family="{fam[w]}" font-weight="{"bold" if w == 700 else "normal"}" fill="{fill}"'
        if var:
            at += f' data-variable="{var}"'
            d.variables[var] = text
        parts.append(f"<tspan{at}>{_esc(text)}</tspan>")
        wd += text_width(text, size, w)
    x0 = ax if anchor == "start" else (ax - wd / 2 if anchor == "middle" else ax - wd)
    d._emit(f'<text {a} xml:space="preserve">{"".join(parts)}</text>', (x0, ay - size * 0.96, x0 + wd, ay + size * 0.19))


# ================================================================================================ atoms and comps
@element("py-atom-mark-registered", "Gedeponeerd merk", "atom", "mark", 1, src="briefpapier", variables=("colour",),
         notes="Small registered mark (R in a circle) next to the wordmark on the letterhead, 1.15 x 1.22 mm (about 1.2 mm), 57 path segments, taken as it is "
               "from Briefpapier_nieuw p1 (drawing 13). Source colour (viewer #1FBECC) normalised to PY-Aqua #32B9CD. In print it sits 0.75 mm right of the "
               "wordmark, level with its top (x 75.05, y 14.93 on the page). Not part of py-comp-lockup-logo-tagline-color. Aqua on transparent: view on a light ground.")
def _(src):
    return crop(src, 1, printsrc.box_mm(74.9, 14.8, 76.35, 16.3), texts=False)


# right edge of the address text: end of the advance of the live text in the source (530.82 pt = 187.26 mm; the brief says 187.3)
ADDR_RIGHT = _mm(530.8247)
ADDR_SIZE = _mm(9.0)  # 3.175 mm
ADDR_BASE = tuple(_mm(v) for v in (53.2596, 63.2587, 73.2577, 93.2557, 103.2547))  # 18.79, 22.32, 25.84, 32.90, 36.43
ADDR_EXAMPLE = {"company": "ParkingYou BV", "street": "Victoriapark 4", "postcode-city": "5611 BM Eindhoven",
                "email": "info@parkingyou.nl", "website": "www.parkingyou.nl"}


def _address(d, dx=0.0, dy=0.0, right=ADDR_RIGHT, values=ADDR_EXAMPLE):
    """Right aligned address block, origin of the coordinates = page (comp) or trim (template) corner shifted by (dx, dy)."""
    keys = ("company", "street", "postcode-city", "email", "website")
    for n, (k, base) in enumerate(zip(keys, ADDR_BASE)):
        d.text(right + dx, base + dy, values[k], size=ADDR_SIZE, fill=NAVY, weight=700 if n == 0 else 400, anchor="end", variable=k)


@element("py-comp-address-block-brief", "Adresblok briefpapier", "comp", "address", 1, src="briefpapier", status="rebuilt",
         variables=("company", "street", "postcode and city", "email", "website"),
         notes="Right aligned address block of the letterhead as live text in Ubuntu 3.17 mm (9 pt), navy PY-Blauw: company in Bold, then street, postcode and city, "
               "a blank gap (7.05 mm baseline step instead of 3.53), email and website. Right edge at 187.26 mm in page coordinates (end of the text advance; the letterhead is "
               "22.7 mm from the right trim edge). REBUILT: all five lines are live text in the source too, but are recomposed in a tight Doc (right anchored) so the variables can change length. "
               "The source address blue is CMYK 100/85.5/22.3/4 (viewer #1E4382), drift: the token blue is used. "
               "COPY CORRECTION also in this comp: the source writes 5611BM, the comp (and the template) write 5611 BM, as on the envelope. "
               "Navy on transparent: view on a light background.")
def _(src):
    d = Doc("py-comp-address-block-brief", "Adresblok briefpapier", tight=True)
    _address(d)
    return d


# envelope address line: source origin (156.7026 pt, 164.6949 pt), Ubuntu Light 6.9898 pt = 2.466 mm
ENV_LINE_SIZE = _mm(6.989842891693115)
ENV_LINE_EXAMPLE = {"street": "Victoriapark 4", "postcode-city": "5611 BM Eindhoven"}


def _envelope_line(d, x, y, values=ENV_LINE_EXAMPLE):
    """One text element in three runs: Light navy street, Regular aqua bar, Light navy postcode and city (as in the source, the spaces belong to the Light runs)."""
    _rich(d, x, y, ENV_LINE_SIZE, [(values["street"] + " ", 300, NAVY, "street"), ("|", 400, AQUA, None),
                                   (" " + values["postcode-city"], 300, NAVY, "postcode-city")])


@element("py-comp-address-line-envelop", "Adresregel envelop", "comp", "address", 1, src="envelop", status="rebuilt",
         variables=("street", "postcode and city"),
         notes="One line 'Victoriapark 4 | 5611 BM Eindhoven' in live Ubuntu Light 2.47 mm navy PY-Blauw, the separator bar in Ubuntu Regular PY-Aqua (three runs in one text element, "
               "so the line reflows when street or city change; the spaces around the bar belong to the Light runs as in the source). REBUILT: live text in the source as well, "
               "recomposed with token colours (source RGB blue #223A7A and aqua #34BACE, the envelope file is RGB only). "
               "Light is used here and on the campaign panel URL only. Navy and aqua on transparent: view on a light background.")
def _(src):
    d = Doc("py-comp-address-line-envelop", "Adresregel envelop", tight=True)
    _envelope_line(d, 0.0, ENV_LINE_SIZE * 0.96)
    return d


# ================================================================================================ application: slagboom sign
SB_TRIM = (480, 240)
SB_SIZE = _mm(98.0)  # 34.572 mm
SB_BASE = tuple(_mm(v) for v in (324.4556, 444.4076, 564.3596))  # 114.47, 156.78, 199.10
SB_LOGO = (178.607, 25.546, 33.428)  # beeldmerk x, y, height (27.7 x 33.4 mm)
SB_HOLES = ((150.05, 126.70), (329.95, 126.70))  # centres of the two rings (source bboxes 148.18..151.93 and 328.07..331.82)
SB_HOLE_R = 3.745 / 2
SB_LINES = ("i.v.m. een evenement is de", "parking enkel toegankelijk")


def _slagboom_template(ctx):
    d = ctx.Doc("py-app-sign-slagboom-evenement", "Bord slagboom evenement", trim=SB_TRIM, bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-regular", "py-tok-type-ubuntu-bold")
    d.rect(-3, -3, 483, 243, fill=NAVY, gid="bleed-background", variable="background-colour", example=NAVY)
    with d.group("py-atom-logo-horizontal-white"):
        d.place("py-atom-logo-horizontal-white", SB_LOGO[0], SB_LOGO[1], h=SB_LOGO[2])
    with d.group("variables"):
        d.text(240.0, SB_BASE[0], SB_LINES[0], size=SB_SIZE, fill=WHITE, anchor="middle", variable="line-1", gid="line-1")
        d.text(240.0, SB_BASE[1], SB_LINES[1], size=SB_SIZE, fill=WHITE, anchor="middle", variable="line-2", gid="line-2")
        runs3 = [("voor ", 400, WHITE, "line-3-lead"), ("abonnementhouders", 700, LIGHT_AQUA, "keyword"), (".", 400, WHITE, "line-3-end")]
        w3 = sum(text_width(t, SB_SIZE, w) for t, w, _, _ in runs3)
        _rich(d, 240.0 - w3 / 2, SB_BASE[2], SB_SIZE, runs3, gid="line-3")  # start anchored from the centred example (text-anchor middle fails in cairosvg)
    with d.group("mounting-holes", data_purpose="assumed mounting hole marks", stroke_colour=MAGENTA):
        for cx, cy in SB_HOLES:
            d.circle(cx, cy, SB_HOLE_R, fill=None, stroke=MAGENTA, sw=PT_MM)
    d.guides(*SB_TRIM)
    return d


@application("py-app-sign-slagboom-evenement", "Bord slagboom evenement", "sign", trim_mm=SB_TRIM, source=[("slagboom", [1])], bleed_mm=3.0,
             status="rebuilt")
def _(ctx):
    # the empty 10 percent group (whole page) would wrap all live text in regroup() and fade it to 10 percent: texts are skipped there and added back plain
    src = printsrc.source("slagboom")
    ref = ctx.reference("slagboom", 1, skip_text=lambda t: True, extra=src.texts(1, printsrc.box_mm(-10, -10, 490, 250)))
    return dict(
        reference={"": ref}, template={"": _slagboom_template(ctx)},
        omitted=["10 percent opacity group (form XObject Fm0, graphics state GS1 at 10 percent, bbox x -514 to 481 mm, y -81 to 245 mm, mostly off the page): "
                 "the form content stream is empty (length 0), it draws nothing, so there is nothing to reproduce (the reference has no ink from it). Probably a leftover "
                 "of a deleted watermark or beeldmerk copy."],
        copy_corrections=[{"original": "i.v.m een evenement is de", "corrected": "i.v.m. een evenement is de (full stop after the m)"},
                          {"original": "abonnementshouders", "corrected": "abonnementhouders (the handbook writes abonnementhouders, see svg/comp/py-comp-pyloon-opening-hours.svg)"}],
        notes=("480 x 240 mm sign, no bleed and no BleedBox in the source (page = trim, art is the full navy field only); the template adds 3 mm bleed (viewBox 486 x 246). "
               "Navy: the source is CMYK 100/86.3/21.5/3.5 (viewer #204382, the same drifted blue as the diefstal sticker), the template uses the token #1A3580. "
               "Logo: py-atom-logo-horizontal-white at scale 1.155 (beeldmerk 27.7 x 33.4 mm at x 178.6, y 25.5), the logo block is centred on the sign (beeldmerk and wordmark together, x 178.6 to 299.7 mm). "
               "Text: three lines of live Ubuntu Regular 98 pt = 34.57 mm white, baselines 114.47, 156.78 and 199.10 mm (pitch 42.3 mm = 1.22 x the size), centred on x 240 (the source "
               "centres the lines 0.2 to 1.2 mm right of 240 because the typed trailing spaces are counted; the template centres the ink). The keyword in Ubuntu Bold in the sampled "
               "light aqua #68CBDA (CMYK 54/0/14/0, no token, kept as sampled, same colour as the icons on the laadkabel and diefstal stickers). "
               "Variables: line-1, line-2, line-3-lead, keyword, line-3-end (line 3 is one text element with three runs, start anchored at the x that centres the example; recentre it when the keyword changes). "
               "Mounting holes: two 1 pt magenta rings (#ED308A, CMYK 0/93.4/7.2/0, an ordinary process colour and NOT a spot like ThruCut), diameter 3.7 mm, centres x 150.05 and 329.95 mm, "
               "y 126.70 mm (each 90 mm left and right of the centre line). They are kept in the reference. In the template they are the named group mounting-holes (stroke #ED308A, 1 pt, no fill). "
               "ASSUMPTION: their purpose (mounting hole marks for the barrier sign) is not stated in the file; the owner must confirm whether they print, cut or are only guides. "
               "No cut contour (none in the source, the sign is not a die cut shape)."),
    )


# ================================================================================================ application: letterhead
LH_LOGO = (20.230, 12.182, 14.918)  # beeldmerk x, y, height (12.4 x 14.9 mm)
LH_REG = (75.047, 14.933)           # registered mark atom top left


@application("py-app-letterhead-briefpapier", "Briefpapier A4", "letterhead", trim_mm=(210, 297), source=[("briefpapier", [1])], bleed_mm=3.0,
             status="rebuilt")
def _(ctx):
    d = ctx.Doc("py-app-letterhead-briefpapier", "Briefpapier A4", trim=(210, 297), bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", "py-tok-type-ubuntu-regular", "py-tok-type-ubuntu-bold", "py-comp-address-block-brief")
    d.rect(-3, -3, 213, 300, fill=WHITE, gid="bleed-background")
    with d.group("py-comp-lockup-logo-tagline-color"):
        d.place("py-comp-lockup-logo-tagline-color", LH_LOGO[0], LH_LOGO[1], scale=LH_LOGO[2] / LOGO_H)
    with d.group("py-atom-mark-registered"):
        d.place("py-atom-mark-registered", LH_REG[0], LH_REG[1], scale=1.0)
    with d.group("py-comp-address-block-brief"):
        with d.group("variables"):
            _address(d, values={**ADDR_EXAMPLE})
    d.guides(210, 297)
    return dict(
        reference={"": ctx.reference("briefpapier", 1)}, template={"": d},
        omitted=[],
        copy_corrections=[{"original": "5611BM Eindhoven", "corrected": "5611 BM Eindhoven (space in the postcode, as on the envelope)"}],
        notes=("A4 portrait, no bleed and no BleedBox in the source (page = trim, everything else is white paper); the template adds 3 mm bleed (white). Blank page below the header block. "
               "Lockup: py-comp-lockup-logo-tagline-color at scale 0.515 (beeldmerk 12.4 x 14.9 mm at x 20.2, y 12.2; the tagline is live text inside the comp, aqua), "
               "the registered mark py-atom-mark-registered 0.75 mm right of the wordmark, level with its top. "
               "Address block: recomposed from py-comp-address-block-brief (right edge 187.26 mm, 3.17 mm Ubuntu, Bold company line) as five live text lines with data-variable "
               "(company, street, postcode-city, email, website). The source address text is CMYK 100/85.5/22.3/4 (viewer #1E4382, a drifted blue, listed in observed); the logo is "
               "CMYK 100/83/0/17 (viewer #0B3D8A, equal to the token); the template uses #1A3580 for both. "
               "Open point (layout): the address block is not aligned with the logo, its top line sits 3.5 mm above the wordmark baseline and its left start is ragged by design (right aligned). "
               "No margins, folding marks or a window position are drawn in the source; the owner may want to add them (DIN 5008 starts the address window at 45 mm)."),
    )


# ================================================================================================ application: envelope
EN_TRIM = (220, 156)
EN_OFF = (249.283 - 220) / 2  # 14.6415 mm: trim corner inside the page
EN_LOGO = (35.035 - EN_OFF, 32.871 - EN_OFF, 18.871)  # beeldmerk x, y (relative to trim), height (15.6 x 18.9 mm)
EN_LINE = (_mm(156.7026) - EN_OFF, _mm(164.6949) - EN_OFF)  # text origin (baseline) of the address line, relative to trim


@application("py-app-envelope-220x156", "Envelop 220 x 156", "envelope", trim_mm=EN_TRIM, source=[("envelop", [1])], bleed_mm=3.0, status="rebuilt")
def _(ctx):
    d = ctx.Doc("py-app-envelope-220x156", "Envelop 220 x 156", trim=EN_TRIM, bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", "py-tok-type-ubuntu-light", "py-tok-type-ubuntu-regular", "py-comp-address-line-envelop")
    d.rect(-3, -3, 223, 159, fill=WHITE, gid="bleed-background")
    with d.group("py-comp-lockup-logo-tagline-color"):
        d.place("py-comp-lockup-logo-tagline-color", EN_LOGO[0], EN_LOGO[1], scale=EN_LOGO[2] / LOGO_H)
    with d.group("py-comp-address-line-envelop"):
        with d.group("variables"):
            _envelope_line(d, EN_LINE[0], EN_LINE[1])
    d.guides(*EN_TRIM)
    return dict(
        reference={"": ctx.reference("envelop", 1)}, template={"": d},
        omitted=[],
        copy_corrections=[],
        notes=("Source page 249.28 x 185.28 mm, trim 220 x 156 mm centred (offset 14.64 mm), no BleedBox. The reference is faithful and keeps the crop marks: two stroked paths, "
               "white 1.25 pt under black 0.25 pt (registration spot All in the source). OPEN POINT: the marks sit at 11.64 and 237.64 mm, i.e. 3 mm OUTSIDE the trim, at the bleed edge of a "
               "226 x 162 mm area, and not at the trim edge; marks that are normally set to the trim would be at 14.64 and 234.64 mm. Confirm with the printer whether the 3 mm is meant as the bleed "
               "and which edge the marks refer to. "
               "The template has no crop marks (the printer's system adds them), 3 mm bleed (white, the envelope has no bleed content), coordinates relative to the trim. "
               "Lockup: py-comp-lockup-logo-tagline-color at scale 0.652 (beeldmerk 15.6 x 18.9 mm at x 20.39, y 18.23 relative to the trim, page 35.0, 32.9), then the address line comp below it "
               "(Ubuntu Light 2.47 mm, text origin x 40.64, baseline 58.1 minus 14.64 = 43.46 mm from the trim top, aligned with the wordmark left edge). "
               "The file claims PDF/X-1a but is RGB (ICC): colours are #223A7A (blue) and #34BACE (aqua), both listed under observed; the template uses #1A3580 and #32B9CD. "
               "PDF/X-1a requires CMYK, so the print file as supplied does not conform to the standard it claims. "
               "The envelope has no window, flap line or return address field in the source."),
    )
