"""3.6 to 3.8 Informatiepyloon laag (p23), pyloon hoog met vuilnisbak (p24), digitale display (p25).

Scales (derived from stated dimensions, measured in source points):
  p23  panel 1000 mm = 231.5 .. 585.8 pt  -> 1000 / 354.3 mm per pt (drawing is 1:8)
  p23 back panel (right side of the page) is drawn at 1:10, 1000 mm = 217.3 .. 500.8 pt -> MM24
  p24  panel 1000 mm = 155.3 .. 438.8 pt  -> 1000 / 283.5 mm per pt (drawing is 1:10)
  p25  body 400 mm   = 805.9 .. 1090.3 pt -> 400 / 284.4 mm per pt
Gradients (header swoosh, section bars) are raster in the source and are rebuilt as vector gradients from
the clip outlines (src.clips + gradient_shape). Dimension lines, callout lines and dots, dimension texts
and the plan view are left out. RVV numerals (AnwbEe fonts) are outlined.
"""
import re

from pyassets import gradient_shape
from pyassets.registry import crop, element

MM23 = 1000.0 / 354.3
MM24 = 1000.0 / 283.5
MM25 = 400.0 / 284.4

THIRD = ("third-party",)
ANWB = ("Anwb",)

DIM_TEXT = re.compile(r"^\s*\d+(,\d+)?\s*mm\s*$")


def _dimline(p):
    """Zero-thickness hairline stroke in annotation black (dimension line or tick)."""
    w = p.box[2] - p.box[0]
    h = p.box[3] - p.box[1]
    return p.fill is None and p.stroke == "#1D1D1B" and (w < 0.01 or h < 0.01)


def _callout_dot(p):
    """3 x 3 pt filled round dot at the end of a callout line (annotation black)."""
    w = p.box[2] - p.box[0]
    h = p.box[3] - p.box[1]
    return p.fill == "#1D1D1B" and p.stroke is None and 2.5 < w < 3.5 and 2.5 < h < 3.5


def _annot(p):
    return _dimline(p) or _callout_dot(p)


def _dimtext(t):
    return bool(DIM_TEXT.match(t))


def _grads(src, pno, bbox, panel_h):
    """Gradient shapes (swoosh and section bars): every clip in bbox that is not the full panel clip."""
    out = []
    for c in src.clips(pno, bbox):
        if c.box[3] - c.box[1] < 0.5 * panel_h:
            out.append(gradient_shape(src, pno, c))
    return out


def _build(src, pno, bbox, mm, panel_h=None, outline=ANWB, skip=_annot, dims=None, notes="", tags=(), gradient=True,
           extra_grads=None):
    """Crop paths and live text, add rebuilt gradient shapes at their paint position."""
    paths = crop(src, pno, bbox, texts=False, skip=skip, outline_fonts=outline)
    grads = list(extra_grads or [])
    if gradient and panel_h:
        grads += _grads(src, pno, bbox, panel_h)
    allp = paths + grads
    allp.sort(key=lambda p: getattr(p, "seq", 1e9))
    items = allp + src.texts(pno, bbox, skip_text=_dimtext)
    extra = {"mm_per_pt": mm, "true_scale": True}
    if dims:
        extra["dims_mm"] = dims
    if tags:
        extra["tags"] = tags
    if grads:
        extra["status"] = "rebuilt"
        extra["notes"] = (notes + " " if notes else "") + (
            "Blauw to aqua gradient fills are raster in the source; rebuilt as real vector gradients on the exact "
            "clip outlines. Everything else is taken straight from source paths and live text.")
    elif notes:
        extra["notes"] = notes
    return items, extra


# ---------------------------------------------------------------- p23 geometry (points)
P23_PANEL = (149.5, 231.5, 291.3, 585.8)
P23_FRONT = (124.0, 230.5, 317.0, 728.0)  # posts, panel and feet; excludes dimension ticks beyond x 317
P23_BACK = (738.5, 216.5, 854.0, 502.0)
P24_FRONT = (144.0, 154.5, 298.5, 722.5)
P24_BACK = (798.5, 344.0, 914.0, 629.5)
P24_PANEL_H = 438.8 - 155.3
P23_PANEL_H = 585.8 - 231.5

BARS = {  # label -> y range of the gradient bar (points)
    "openingstijden": ((149.0, 344.2, 292.0, 357.8), "Openingstijden"),
    "tarieven": ((149.0, 379.7, 292.0, 393.3), "Tarieven"),
    "betalingsmogelijkheden": ((149.0, 431.1, 292.0, 444.7), "Betalingsmogelijkheden"),
    "calamiteiten": ((149.0, 470.0, 292.0, 483.6), "Calamiteiten"),
    "algemene-voorwaarden": ((149.0, 501.9, 292.0, 515.5), "Algemene voorwaarden"),
}


# ---------------------------------------------------------------- products
@element("py-prod-pyloon-laag-front", "3.6 Informatiepyloon, voorzijde", "prod", "pyloon", 23,
         variables=("location name", "opening hours", "tariffs", "phone", "URL", "which signs"),
         built_from=("py-comp-pyloon-header-band", "py-comp-pyloon-section-bar-openingstijden",
                     "py-comp-pyloon-section-bar-tarieven", "py-comp-pyloon-section-bar-betalingsmogelijkheden",
                     "py-comp-pyloon-section-bar-calamiteiten", "py-comp-pyloon-section-bar-algemene-voorwaarden",
                     "py-comp-pyloon-location-name-slot", "py-comp-pyloon-opening-hours", "py-comp-price-strip-110x400",
                     "py-comp-pyloon-payment-row", "py-comp-pyloon-emergency", "py-comp-pyloon-terms"))
def _(src):
    return _build(src, 23, P23_FRONT, MM23, P23_PANEL_H, dims=(480, 1400),
                  notes="2D elevation with posts and 1000 x 400 panel (width 480 over the posts, total height 1400; the SVG is 540 wide because the foot plates are drawn). "
                        "Plan view with foot plates, dimension lines and callouts left out.")


@element("py-prod-pyloon-laag-back", "3.6 Informatiepyloon, achterzijde", "prod", "pyloon", 23,
         variables=("goodbye text",), built_from=("py-comp-pyloon-back-tot-ziens",))
def _(src):
    return _build(src, 23, P23_BACK, MM24, P23_PANEL_H, dims=(400, 1000),
                  notes="Back side 'Tot ziens' panel 400 x 1000 (drawn at 1:10 on the page, unlike the 1:8 front).")


@element("py-prod-pyloon-hoog-vuilnisbak-front", "3.7 Informatiepyloon hoog met vuilnisbak, voorzijde", "prod", "pyloon", 24,
         variables=("location name", "opening hours", "tariffs", "phone", "URL", "which signs"),
         built_from=("py-prod-pyloon-laag-front",))
def _(src):
    return _build(src, 24, P24_FRONT, MM24, P24_PANEL_H, dims=(480, 2000),
                  notes="Panel 1000 plus bin zone 1000 (Dulce 50L bin with trash sticker), total height 2000. "
                        "Callout line and dot on the bin and the 400mm dimension are left out.")


@element("py-prod-pyloon-hoog-vuilnisbak-back", "3.7 Informatiepyloon hoog, achterzijde", "prod", "pyloon", 24,
         built_from=("py-comp-pyloon-back-logo",))
def _(src):
    return _build(src, 24, P24_BACK, MM24, None, dims=(400, 1000), notes="Back side 400 x 1000 with the logo in print foil.")


@element("py-prod-display-volvrij", "3.8 Digitale display", "prod", "display", 25, variables=("state",),
         built_from=("py-atom-display-volvrij-vrij",))
def _(src):
    return _build(src, 25, (796.0, 305.5, 1100.0, 450.5), MM25, None, skip=lambda p: p.stroke == "#808080",
                  outline=(), dims=(400, 200, 93),
                  notes="Front view of the CAD drawing including the bracket bolts (414 mm over the bolts). The 'VRIJ' "
                        "dots are the only state drawn in the handbook. Dimension lines and numbers left out.")


# ---------------------------------------------------------------- components
@element("py-comp-pyloon-header-band", "pyloon kopband", "comp", "pyloon", (23, 24),
         built_from=("py-atom-symbol-p-roof", "py-tok-gradient-verloop"))
def _(src):
    return _build(src, 23, (149.0, 231.0, 292.0, 312.0), MM23, P23_PANEL_H)


def _bar(key):
    box, label = BARS[key]

    @element(f"py-comp-pyloon-section-bar-{key}", f"balk {label}", "comp", "pyloon", (23, 24),
             built_from=("py-tok-gradient-verloop-horizontal",))
    def _(src):
        return _build(src, 23, box, MM23, P23_PANEL_H)


for _k in BARS:
    _bar(_k)


@element("py-comp-pyloon-location-name-slot", "locatienaam pyloon", "comp", "pyloon", (23, 24),
         variables=("location name",), built_from=("py-atom-logo-horizontal-color",))
def _(src):
    return _build(src, 23, (155.5, 312.0, 283.0, 332.5), MM23, None, outline=())


@element("py-comp-pyloon-opening-hours", "openingstijden blok", "comp", "pyloon", (23, 24),
         variables=("days", "hours", "note"))
def _(src):
    return _build(src, 23, (149.0, 358.2, 292.0, 378.0), MM23, None, outline=())


@element("py-comp-price-strip-110x400", "deelfolie 110x400", "comp", "pyloon", (23, 24),
         variables=("tariff names", "prices"))
def _(src):
    return _build(src, 23, (373.5, 392.2, 516.5, 432.0), MM23, None, outline=(), dims=(400, 110),
                  notes="Deelfolie strip 110 x 400 with four tariff rows, rows 3 and 4 in blauw. Caption and dimensions left out.")


@element("py-comp-pyloon-payment-row", "betaalmogelijkheden rij", "comp", "pyloon", (23, 24),
         variables=("which marks",),
         built_from=("py-atom-payment-contactless", "py-atom-payment-mastercard", "py-atom-payment-maestro",
                     "py-atom-payment-pin-hand"))
def _(src):
    return _build(src, 23, (158.5, 448.5, 258.0, 462.0), MM23, None, outline=())


@element("py-comp-pyloon-emergency", "calamiteiten blok", "comp", "pyloon", (23, 24), variables=("phone number",))
def _(src):
    return _build(src, 23, (149.0, 483.8, 292.0, 501.0), MM23, None, outline=())


@element("py-comp-pyloon-terms", "algemene voorwaarden blok", "comp", "pyloon", (23, 24),
         variables=("URL", "signs"), built_from=("py-comp-rvv-cluster-pyloon",))
def _(src):
    return _build(src, 23, (149.0, 516.0, 292.0, 576.0), MM23, None)


@element("py-comp-rvv-cluster-pyloon", "RVV icon cluster pyloon", "comp", "pyloon", (23, 24), variables=("speed", "height"),
         built_from=("py-atom-rvv-a01", "py-atom-rvv-max-height", "py-atom-rvv-c07", "py-atom-rvv-no-bicycles",
                     "py-atom-sign-camera"))
def _(src):
    return _build(src, 23, (159.0, 551.0, 281.5, 575.0), MM23, None,
                  notes="Five round signs: speed 5, max height 2,1m, truck, bicycles prohibited, camera. Numerals outlined "
                        "(AnwbEe fonts). Bicycle and camera signs are third-party marks.")


@element("py-comp-pyloon-back-tot-ziens", "achterzijde Tot ziens", "comp", "pyloon", 23,
         variables=("goodbye text", "optional image"), built_from=("py-comp-pyloon-header-band", "py-atom-logo-stacked-color"))
def _(src):
    return _build(src, 23, P23_BACK, MM24, P23_PANEL_H, dims=(400, 1000),
                  notes="Drawn at 1:10 on the page, unlike the 1:8 front.")


@element("py-comp-pyloon-back-logo", "achterzijde alleen logo", "comp", "pyloon", 24, built_from=("py-atom-logo-stacked-color",))
def _(src):
    return _build(src, 24, P24_BACK, MM24, None, dims=(400, 1000))


# ---------------------------------------------------------------- atoms
@element("py-atom-rvv-no-bicycles", "fietsen verboden", "atom", "rvv", (23, 24))
def _(src):
    return _build(src, 23, (233.0, 551.0, 257.0, 575.0), MM23, None, tags=THIRD,
                  notes="Not in section 9.2. Taken from the pyloon sign row.")


@element("py-atom-sign-camera", "cameratoezicht", "atom", "rvv", (23, 24))
def _(src):
    return _build(src, 23, (257.4, 551.0, 281.5, 575.0), MM23, None, tags=THIRD,
                  notes="Not in section 9.2 and not an RVV sign. Black ring with camera, from the pyloon sign row.")


@element("py-atom-payment-contactless", "contactloos betalen", "atom", "payment", (23, 24))
def _(src):
    return _build(src, 23, (159.7, 450.0, 176.3, 460.3), MM23, None, tags=THIRD, outline=())


@element("py-atom-payment-mastercard", "Mastercard", "atom", "payment", (23, 24))
def _(src):
    return _build(src, 23, (185.0, 448.5, 202.0, 462.0), MM23, None, tags=THIRD, outline=())


@element("py-atom-payment-maestro", "Maestro", "atom", "payment", (23, 24))
def _(src):
    return _build(src, 23, (204.8, 448.5, 222.0, 462.0), MM23, None, tags=THIRD, outline=())


@element("py-atom-payment-pin-hand", "hand met pas", "atom", "payment", (23, 24))
def _(src):
    return _build(src, 23, (226.5, 448.5, 241.0, 462.0), MM23, None, tags=THIRD, outline=())


@element("py-atom-display-volvrij-vrij", "VOL/VRIJ display, VRIJ", "atom", "display", (25, 12, 15), variables=("state",))
def _(src):
    return _build(src, 25, (805.0, 306.0, 1091.0, 450.0), MM25, None, skip=lambda p: p.stroke == "#808080", outline=(),
                  notes="Front panel of the digital display: frame, black face and the green 'VRIJ' LED dots. Bracket "
                        "bolts and dimension lines left out.")
