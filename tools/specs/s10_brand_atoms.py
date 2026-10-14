"""Stream A: reverse logos (p1, p12, p14, p38), pictograms (p10), people figures and welcome banner (p40),
RVV signs (p51)."""
from pyassets import affine, items_box, ellipse_item
from pyassets.registry import crop, element

THIRD = ("third-party",)


def _pad(b, p=1.0):
    return (b[0] - p, b[1] - p, b[2] + p, b[3] + p)


# ------------------------------------------------------------------ reverse logos
# p14 carries the horizontal logo on a lichtbak face as pure vectors: white shape with hole, explicit
# navy ring disc, aqua dot, white wordmark outlines. The cover (p1) has the same logo, but its navy ring is the
# gradient background showing through the hole (no ring path), so p14 is the cleaner source.
@element("py-atom-logo-horizontal-reverse", "Logo liggend op blauw (candidate)", "atom", "logo", (14, 1, 38))
def _(src):
    return crop(src, 14, (212.5, 330, 441, 394), texts=False), {
        "notes": "Source page 14 (also on p1 and p38). White shape, navy ring #1A3580, aqua dot, white wordmark. "
                 "On p1 the ring is the background showing through the hole, so p14 was used. Not defined in 1.1.",
    }


@element("py-atom-logo-beeldmerk-reverse", "Beeldmerk op blauw (candidate)", "atom", "logo", (12, 1))
def _(src):
    return crop(src, 12, (411.5, 273, 454, 324), texts=False), {
        "notes": "Source page 12 (top right of the aanrijroute lichtbak). White bubble, navy ring, aqua dot. Not defined in 1.4.",
    }


@element("py-atom-logo-stacked-reverse", "Logo staand op blauw (candidate)", "atom", "logo", (6, 1),
         built_from=("py-atom-logo-stacked-white", "py-atom-logo-beeldmerk-reverse"))
def _(src):
    # A stacked logo on blue exists nowhere in the handbook with a drawn navy ring (p1 stacked is the colour version).
    # Take the white diapositief logo of p6 (white shape with hole, white wordmark) and put the navy ring disc and
    # aqua dot of the p12 beeldmerk behind/over it at the same proportions.
    mark_src = crop(src, 12, (411.5, 273, 454, 324), texts=False)       # white bubble, navy disc, aqua dot
    white_mark = mark_src[0]
    disc, dot = mark_src[1], mark_src[2]
    target = (194, 545, 267, 632)                                       # p6 stacked-white beeldmerk
    p6 = crop(src, 6, (194, 545, 267, 632), texts=False)
    word = crop(src, 6, (122, 637, 338, 684), texts=False)
    tb = items_box(p6)
    sb = items_box([white_mark])
    s = (tb[2] - tb[0]) / (sb[2] - sb[0])
    tx = tb[0] - sb[0] * s
    ty = tb[1] - sb[1] * s
    ring = affine([disc, dot], s, s, tx, ty)
    for r in ring:
        r.tag = "rebuilt-ring"
    return ring[:1] + p6 + ring[1:] + word, {
        "status": "rebuilt",
        "notes": "No stacked reverse logo with a drawn ring exists in the handbook (p1 stacked is the colour version, "
                 "and the white diapositief logo on p6 is a hole on a raster background). Built from the p6 white stacked logo "
                 "plus the navy ring disc and aqua dot of the p12 beeldmerk, scaled to the p6 mark.",
    }


# ------------------------------------------------------------------ 1.5 pictograms (p10)
PICTO = [
    ("car", "Route voor autoverkeer", (160.8, 244.3, 240.2, 302.4)),
    ("accessible", "Route naar parkeervakken voor mindervaliden", (166.9, 314.5, 234.5, 393.7)),
    ("ev", "Route naar parkeervakken voor electrische voertuigen", (162.2, 405.7, 238.1, 485.0)),
    ("motorcycle", "Route naar parkeervakken voor motorfietsen", (160.8, 499.0, 240.2, 563.2)),
    ("family", "Route naar parkeervakken voor gezinnen met kinderen", (158.3, 578.0, 242.6, 646.2)),
    ("pedestrian", "Route voor voetgangers", (638.8, 244.3, 672.6, 309.4)),
    ("lift", "Geeft route naar de lift aan", (628.3, 318.2, 689.9, 387.0)),
    ("escalator", "Geeft route naar de troltrap (tapis roulant) aan", (628.3, 396.9, 689.9, 443.1)),
    ("stairs", "Geeft route naar de trap aan", (630.9, 451.1, 689.9, 486.9)),
    ("payment-machine", "Geeft route naar de betaalautomaat aan", (633.4, 499.1, 688.5, 554.1)),
    ("toilet", "Geeft route naar de toiletten aan", (632.3, 563.6, 688.4, 619.7)),
    ("info", "Geeft route naar de beheerder/infobali aan", (629.9, 628.1, 689.9, 700.5)),
]
for _k, _n, _b in PICTO:
    def _mk(b=_b):
        return lambda src: (crop(src, 10, _pad(b), texts=False, outline_fonts=("Ubuntu",)), {"notes": "Any lettering (euro sign, WC) is outlined so the symbol does not depend on a font."})

    element(f"py-atom-picto-{_k}", _n, "atom", "picto", 10, variables=("colour",))(_mk())


# ------------------------------------------------------------------ 6.1 figures (p40)
# Each figure is a run of paint-order sequence numbers in the page drawing list (several figures overlap in x).
FIGS = [
    ("walk", "figuur 1", (158, 160, 236, 308), [(60, 63)]),
    ("dance", "figuur 2", (237, 164, 337, 308), [(64, 71)]),
    ("wave", "figuur 3", (339, 158, 424, 312), [(72, 79)]),
    ("jump", "figuur 4", (420, 157, 528, 312), [(100, 107)]),
    ("point", "figuur 5", (555, 154, 645, 308), [(86, 93)]),
    ("bags-walk", "figuur 6", (642, 153, 776, 301), [(187, 192)]),
    ("bags-cheer", "figuur 7", (766, 156, 941, 311), [(193, 202)]),
    ("cap-point", "figuur 8", (956, 152, 1046, 311), [(173, 178), (203, 209)]),
    ("cap-wave", "figuur 9", (1053, 149, 1138, 307), [(159, 164), (210, 216)]),
]
for _k, _n, _b, _seq in FIGS:
    def _mk(b=_b, seq=_seq):
        def build(src):
            return crop(src, 40, b, texts=False,
                        skip=lambda p: not any(lo <= p.seq <= hi for lo, hi in seq)), {
                "notes": "Navy figure. The white paths are the separation gaps of the source (limb outlines painted white), "
                         "not a second colour of the figure.",
            }
        return build

    element(f"py-atom-figure-{_k}", _n, "atom", "figure", 40)(_mk())


# ------------------------------------------------------------------ arrow circle and welcome banner (p40)
@element("py-atom-arrow-right-circle", "pijl rechts in witte cirkel", "atom", "arrow", 40, variables=("direction", "colour"))
def _(src):
    return crop(src, 40, (709.5, 460.5, 837.5, 588.5), texts=False)


@element("py-comp-welcome-wall-banner", "welkom muurbanner", "comp", "banner", 40, variables=("location name",),
         built_from=("py-atom-logo-horizontal-reverse", "py-atom-arrow-right-circle", "py-atom-figure-wave"))
def _(src):
    # drop the white page-size backing rectangle (seq 217) and the thin black frame around the artboard (seq 244)
    return crop(src, 40, (158, 358, 1156, 693), skip=lambda p: p.seq in (217, 244)), {
        "notes": "Extracted straight from p40: navy half-pill, live text 'Welkom bij' and the location name, white logo, "
                 "arrow circle and the large waving figure (white separation outlines kept). Frame and white backing removed.",
    }


# ------------------------------------------------------------------ 9.2 RVV signs (p51)
RVV = [
    ("a01", "A01 Maximumsnelheid", (164.3, 247.2, 255.4, 338.3), ("speed value",)),
    ("b06", "B06 Verleen voorrang", (265.3, 249.9, 385.9, 353.2), ()),
    ("c02", "C02 Eenrichtingweg, in deze richting gesloten", (396.4, 247.2, 487.5, 338.3), ()),
    ("c03", "C03 Eenrichtingsweg", (511.2, 247.0, 602.2, 338.1), ()),
    ("c07", "C07 Gesloten voor vrachtauto's", (634.1, 247.0, 725.2, 338.1), ()),
    ("c10", "C10 Gesloten voor motorvoertuigen met aanhangwagen", (749.8, 247.0, 840.9, 338.1), ()),
    ("c11", "C11 Gesloten voor motorfietsen", (160.8, 459.8, 251.9, 550.9), ()),
    ("c16", "C16 Gesloten voor voetgangers", (276.4, 459.8, 367.5, 550.9), ()),
    ("d2", "D2 Gebod voor alle bestuurders het bord voorbij te gaan", (391.9, 454.4, 491.9, 554.4), ("direction",)),
    ("e06", "E06 Gehandicaptenparkeerplaats", (512.1, 459.3, 603.2, 595.9), ()),
    ("e08c", "E08c Laadplaats voor elektrische voertuigen", (624.6, 459.3, 715.2, 595.9), ()),
    ("e10", "E10 Parkeerschijfzone", (732.9, 459.8, 849.7, 614.8), ("zone text", "duration")),
]
for _k, _n, _b, _v in RVV:
    def _mk(b=_b):
        return lambda src: crop(src, 51, _pad(b, 0.8), outline_fonts=("RWSTTDdx", "Anwb", "Ubuntu"))

    element(f"py-atom-rvv-{_k}", _n, "atom", "rvv", 51 if _k != "c02" else (51, 27), variables=_v, tags=THIRD)(_mk())
