"""Abonnementskaart Evoluon (EvoluonPasjes.pdf) and Bewijs van inlevering (Inleveren_Abbonementborg_A5.pdf):
form fields (input field, date segments, signature box, line label) and the two applications."""
from pyassets import printsrc
from pyassets.apps import application
from pyassets.compose import Doc, text_width
from pyassets.core import PT_MM, regroup
from pyassets.registry import crop, element

NAVY = "#1A3580"
WHITE = "#FFFFFF"

# ---- EvoluonPasjes.pdf (mm, page = trim, 85 x 55), measured with print_probe / PyMuPDF
EV_LABEL_SIZE = 2.822
EV_LABEL_X = 36.722
EV_FIELD1 = (36.773, 24.424, 81.499, 32.681)   # ink box of the first input field
EV_FIELD_W, EV_FIELD_H = 81.499 - 36.773, 32.681 - 24.424
EV_BASE1, EV_BASE2 = 22.715, 36.988             # label baselines
EV_FIELD2_Y = 38.696
BEELD_FRONT = (-20.727, -10.011, 33.589, 55.505)   # navy beeldmerk on the front (cropped by the trim)
WORD_FRONT = (8.62, 46.832, 30.912, 51.354)        # wordmark ink box on the front
WATER_BACK = (18.063, -6.607, 72.379, 58.909)      # watermark on the back
LOCKUP_BACK = (15.722, 20.145, 27.98, 34.931)      # white beeldmerk of the back lockup (12.3 x 14.8)
LOCKUP_SCALE = 0.511
TAG_BACK = (31.395, 33.718, 2.342)                 # tagline origin x, baseline y, size

# ---- label block geometry (comp coordinates, origin = label text origin on its baseline)
FIELD_DX = EV_FIELD1[0] - EV_LABEL_X
FIELD_DY = EV_FIELD1[1] - EV_BASE1


@element("py-atom-field-input-rounded", "Invulveld afgerond", "atom", "field", 1, src="evoluon",
         variables=("colour",),
         notes="Aqua input field, 44.7 x 8.3 mm, corner radius 1.29 mm (15.5 percent of the height), aqua at 10 percent opacity (a transparency group in the source, "
               "kept as a group with opacity 0.1). Observed in print, not an official rule. Aqua on white looks pale; place on white paper.")
def _(src):
    items = crop(src, 1, printsrc.box_mm(36.5, 24.2, 81.7, 32.9), texts=False)
    return regroup(src, 1, items)


@element("py-comp-field-block-label-input", "Veldblok label met invulveld", "comp", "field", 1, src="evoluon", status="rebuilt",
         variables=("label",),
         notes="Label in live Ubuntu Regular 2.82 mm (navy) above the input field atom (py-atom-field-input-rounded). Distances as on the card front: "
               "label baseline 1.7 mm above the field top, field left edge 0.05 mm right of the text origin. Rebuilt: composed from the atom plus live text.")
def _(src):
    d = Doc("py-comp-field-block-label-input", "Veldblok label met invulveld", tight=True)
    _block(d, 0.0, 0.0, "Abonnementsnummer:")
    return d


def _block(d, x, y_base, label, variable="label"):
    """Label (baseline y_base, text origin x) and the field below it."""
    d.text(x, y_base, label, size=EV_LABEL_SIZE, fill=NAVY, variable=variable)
    d.place("py-atom-field-input-rounded", x + FIELD_DX, y_base + FIELD_DY)


@element("py-atom-logo-beeldmerk-watermark", "Beeldmerk watermerk (aqua 5 procent)", "atom", "logo", 2, src="evoluon",
         variables=("colour", "opacity"),
         notes="Beeldmerk shape in aqua at 5 percent opacity (group opacity 0.05, measured on the card back; the Phase 1 document said 10 percent by mistake), 54.3 x 65.5 mm. "
               "Same outline as py-atom-logo-beeldmerk-color (scale 1.508) but as a closed silhouette without the ring cut out, extracted as its own variant because it carries the tint. "
               "Place on PY-Blauw. Aqua on transparent: nearly invisible on white.")
def _(src):
    items = crop(src, 2, printsrc.box_mm(17.9, -6.8, 72.5, 59.1), texts=False, skip=lambda p: (p.box[2] - p.box[0]) < 100)
    return regroup(src, 2, items)


@element("py-atom-field-date-segmented", "Datumveld in segmenten", "atom", "field", 1, src="inleveren",
         variables=("colour",),
         notes="Three outlined date segments for dd, mm and jjjj (2, 2 and 4 digits), 39.2 x 7.3 mm, chamfered corners with notches between the digit cells, navy stroke 0.75 pt, no fill. "
               "Three stroked paths taken from the source as they are.")
def _(src):
    return crop(src, 1, printsrc.box_mm(101.0, 8.4, 140.8, 16.2), texts=False)


@element("py-comp-field-signature-box", "Handtekeningvak", "comp", "field", 1, src="inleveren", status="rebuilt",
         variables=("label",),
         notes="Box 109.5 x 32 mm, navy at 5 percent opacity (transparency in the source), label 'Handtekening klant' as live Ubuntu Regular 3.53 mm navy "
               "at the bottom left (2.43 mm from the left edge, baseline 3.1 mm above the bottom). Rebuilt: rect plus live text.")
def _(src):
    d = Doc("py-comp-field-signature-box", "Handtekeningvak", tight=True)
    _sigbox(d, 0.0, 0.0)
    return d


SIG_W, SIG_H = 117.563 - 8.112, 100.699 - 68.724
SIG_LABEL = (10.543 - 8.112, 97.581 - 68.724)


def _sigbox(d, x, y, variable="label"):
    d.rect(x, y, x + SIG_W, y + SIG_H, fill=NAVY, opacity=0.05, gid="box")
    d.text(x + SIG_LABEL[0], y + SIG_LABEL[1], "Handtekening klant", size=3.528, fill=NAVY, variable=variable)


# label "Naam klant:" 4.586 mm, rule from 1.06 mm after the label to the same right end as the typed underscores in the source
LL_SIZE = 4.586
LL_RULE_X0 = 33.95 - 8.111           # start of the first underscore
LL_RULE_LEN = 117.44 - 33.95         # to the end of the last underscore
LL_RULE_DY = 0.667                   # underscore centre below the baseline (Ubuntu glyph: -0.185 to -0.106 em)
LL_RULE_W = 0.362                    # underscore thickness


@element("py-comp-field-line-label", "Label met lijn", "comp", "field", 1, src="inleveren", status="rebuilt",
         variables=("label", "line length"),
         notes="Label as live Ubuntu Regular 4.59 mm plus a drawn navy rule (0.36 mm, the thickness of the underscore glyph) in place of the typed underscores of the source "
               "('Naam klant: ____'). Rule starts 1.06 mm after the label and is 83.5 mm long, ending where the underscores ended (117.4 mm on the form). "
               "Set the rule length per use (line length).")
def _(src):
    d = Doc("py-comp-field-line-label", "Label met lijn", tight=True)
    _linelabel(d, 0.0, 0.0, "Naam klant:", LL_RULE_LEN)
    return d


def _linelabel(d, x, y_base, label, rule_len, variable="label"):
    d.text(x, y_base, label, size=LL_SIZE, fill=NAVY, variable=variable)
    with d.group("rule", data_variable="line-length"):
        d.line(x + LL_RULE_X0, y_base + LL_RULE_DY, x + LL_RULE_X0 + rule_len, y_base + LL_RULE_DY, NAVY, LL_RULE_W)
    d.variables["line-length"] = f"{rule_len:.1f} mm"


# =====================================================================  Application: card
@application("py-app-card-abonnement-evoluon", "Abonnementskaart Evoluon", "card", trim_mm=(85, 55), bleed_mm=3.0,
             variants=("front", "back"), source=[("evoluon", [1, 2])], status="rebuilt",
             notes="Source has no bleed box (art overshoots the page by 3 to 20 mm); templates are built with 3 mm bleed. Front: the beeldmerk at 1.508x (54.3 x 65.5 mm) "
                   "runs 20.7 mm off the left, 10.0 mm off the top and 0.5 mm off the bottom; the part beyond the 3 mm bleed lies outside the template viewBox. "
                   "Back: the source background overshoots the trim only 0.2 mm at the bottom and 3.3 mm at the top; the template runs the navy into 3 mm all round. "
                   "The watermark is 5 percent (the Phase 1 document said 10 percent). The back lockup is the reverse lockup (white bubble, aqua dot) at 0.511x of the A6 lockup, "
                   "centred on the card; the tagline is live text so it can be a variable. Card number and plate fields are blank in print (input fields only).")
def _(ctx):
    return dict(
        reference={"front": ctx.reference("evoluon", 1, variant="front"),
                   # regroup() would put the white tagline into the 5 percent watermark group (its centre lies inside); add it on top instead
                   "back": ctx.reference("evoluon", 2, variant="back", skip_text=lambda t: t.startswith("The other"),
                                         extra=printsrc.source("evoluon").texts(2, printsrc.box_mm(30, 30, 63, 35.5)))},
        template={"front": _card_front(ctx), "back": _card_back(ctx)},
        omitted=[],
        copy_corrections=[],
    )


def _card_front(ctx):
    d = ctx.Doc("py-app-card-abonnement-evoluon", "Abonnementskaart Evoluon voorzijde", trim=(85, 55), bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", "py-tok-type-ubuntu-regular", "py-tok-type-ubuntu-bold")
    d.rect(-3, -3, 88, 58, fill=WHITE, gid="bleed-background")
    bx0, by0, bx1, by1 = BEELD_FRONT
    with d.group("py-atom-logo-beeldmerk-color"):
        # cropped by the trim at left, top and bottom; content beyond the bleed lies outside the template viewBox
        d.place("py-atom-logo-beeldmerk-color", bx0, by0, h=by1 - by0)
    with d.group("py-atom-logo-wordmark-color"):
        d.place("py-atom-logo-wordmark-color", WORD_FRONT[0], WORD_FRONT[1], w=WORD_FRONT[2] - WORD_FRONT[0])
    with d.group("variables"):
        d.text(EV_LABEL_X, 9.416, "Abonnement", size=6.35, fill=NAVY, weight=400, gid="title-line-1")
        d.text(EV_LABEL_X, 15.41, "Evoluon", size=6.35, fill=NAVY, weight=700, variable="location-name", gid="title-line-2")
        for n, (base, label) in enumerate(((EV_BASE1, "Abonnementsnummer:"), (EV_BASE2, "Kenteken:")), 1):
            with d.group("py-comp-field-block-label-input"):
                _block(d, EV_LABEL_X, base, label, variable=f"field-label-{n}")
    d.uses("py-comp-field-block-label-input")
    d.guides(85, 55)
    return d


def _card_back(ctx):
    d = ctx.Doc("py-app-card-abonnement-evoluon", "Abonnementskaart Evoluon achterzijde", trim=(85, 55), bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-wit", "py-tok-type-ubuntu-regular", "py-comp-tagline-lockup-reverse")
    d.rect(-3, -3, 88, 58, fill=NAVY, gid="bleed-background")
    with d.group("py-atom-logo-beeldmerk-watermark"):
        d.place("py-atom-logo-beeldmerk-watermark", WATER_BACK[0], WATER_BACK[1])
    with d.group("py-comp-tagline-lockup-reverse"):
        d.place("py-atom-logo-horizontal-reverse", LOCKUP_BACK[0], LOCKUP_BACK[1], h=28.949 * LOCKUP_SCALE)
        d.text(TAG_BACK[0], TAG_BACK[1], "The other way of parking", size=TAG_BACK[2], fill=WHITE, spacing=0.272 * LOCKUP_SCALE,
               variable="tagline-text")
    d.guides(85, 55)
    return d


# =====================================================================  Application: form
@application("py-app-form-bewijs-inlevering", "Bewijs van inlevering toegangsmiddel", "form", trim_mm=(148, 105), bleed_mm=3.0,
             source=[("inleveren", [1])], status="rebuilt",
             notes="The file is named A5 but the page is 148 x 105 mm (A6 landscape). No bleed in the source; the template has 3 mm bleed (white). "
                   "Open question for the owner: the running text spells the brand 'ParkingYou' (capital P and Y) while the logo is set 'parkingyou'; kept as in the source, not changed. "
                   "Reflow: with the word 'toegangsmiddel' whole, line 2 no longer fits in the text width, so paragraph 1 is set in three lines (leading 1.2 x 4.59 mm = 5.5 mm, "
                   "as in the source) and the gap to paragraph 2 is 8.0 mm instead of 11.0 mm so the lower block (Naam klant, signature box) stays where it is in the source. "
                   "The beeldmerk bottom right is the beeldmerk without wordmark (py-atom-logo-beeldmerk-color at 0.348x, 12.6 x 15.1 mm).")
def _(ctx):
    d = ctx.Doc("py-app-form-bewijs-inlevering", "Bewijs van inlevering toegangsmiddel", trim=(148, 105), bleed=3.0)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", "py-tok-type-ubuntu-regular", "py-tok-type-ubuntu-medium", "py-tok-type-ubuntu-bold")
    d.rect(-3, -3, 151, 108, fill=WHITE, gid="bleed-background")
    X = 8.111
    with d.group("title", data_variable="title"):
        d.text(X, 14.212, "Bewijs van inlevering", size=7.056, fill=NAVY, weight=500)
        d.text(X, 21.267, "toegangsmiddel", size=7.056, fill=NAVY, weight=700)
    d.variables["title"] = "Bewijs van inlevering / toegangsmiddel"
    lead = 4.586 * 1.2
    p1 = ["ParkingYou bevestigt hierbij de ontvangst van het", "toegangsmiddel dat hoort bij het abonnement van", "onderstaande klant."]
    p2 = ["De bijbehorende borg wordt, na verwerking, teruggestort", "conform de geldende voorwaarden."]
    for line in p1 + p2:
        assert X + text_width(line, 4.586) <= 140.0, (line, X + text_width(line, 4.586))
    with d.group("variables"):
        for gid, lines, y0 in (("body-1", p1, 31.851), ("body-2", p2, 50.861)):
            with d.group(gid, data_variable=gid):
                for k, line in enumerate(lines):
                    d.text(X, y0 + k * lead, line, size=4.586, fill=NAVY)
            d.variables[gid] = " ".join(lines)
    with d.group("py-atom-field-date-segmented"):
        fb = d.place("py-atom-field-date-segmented", 101.44 - 0.375 * PT_MM, 8.737 - 0.375 * PT_MM)
    d.text(140.351, 20.859, "Datum", size=3.326, fill=NAVY, anchor="end")
    with d.group("py-comp-field-line-label"):
        _linelabel(d, X, 65.503, "Naam klant:", LL_RULE_LEN, variable="customer-name-label")
    d.uses("py-comp-field-line-label")
    with d.group("py-comp-field-signature-box"):
        _sigbox(d, 8.112, 68.724, variable="signature-label")
    d.uses("py-comp-field-signature-box")
    with d.group("py-atom-logo-beeldmerk-color"):
        d.place("py-atom-logo-beeldmerk-color", 127.468, 84.711, h=99.861 - 84.711)
    d.guides(148, 105)
    return dict(
        reference={"": ctx.reference("inleveren", 1)},
        template={"": d},
        omitted=[],
        copy_corrections=[
            {"original": "toegangs-/middel (manual hyphenation across two lines)", "corrected": "toegangsmiddel (word whole, paragraph reflowed to three lines)"},
            {"original": "Datum  (trailing space)", "corrected": "Datum (no trailing space, right aligned to the end of the date field)"},
            {"original": "Naam klant: ______ (typed underscores)", "corrected": "Naam klant: plus a drawn navy rule of the same length (py-comp-field-line-label)"},
        ],
    )
