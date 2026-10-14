"""Lichtbakken: 2.1 aanrijroute (p12), 3.1 entree (p14), 5.1 liggend (p37), 5.2 staand (p38).

Products are the front elevation (face with lichtbakprofiel frame plus the visible spacer and pole parts).
Left out: 3D renders (raster), top views and side views, dimension lines, callout lines and dots, wall
boxes, "TOEGEPASTE KLEUR" boxes, footer and the All Jobs logo.

All four drawings are 1:10 (1 pt in the PDF = 10 x 0.352778 mm), measured on the face width or height.
"""
import copy
import math

from pyassets import Gradient, Path, Text, gradient_shape, rect_item
from pyassets.filters import callout_dot
from pyassets.registry import crop, element

FRAME = "#1A3580"  # RAL 5002 lichtbakprofiel, brand-normalised (the source draws it #082E7A or #182F72)
GREY = "#AEAEAE"  # RAL 9006 / PY-Grijs
LINE = "#1D1D1B"


def _scale(width_pt, mm):
    return mm / width_pt


# measured scales (face outer size in points versus the stated size in mm)
S12 = _scale(481.802 - 198.337, 1000)  # p12 face 1000 mm wide
S14 = _scale(482.366 - 198.901, 1000)  # p14 face 1000 mm wide
S37 = _scale(867.401 - 158.740, 2500)  # p37 face 2500 mm wide
S38 = _scale(599.787 - 316.323, 1000)  # p38 face 1000 mm high (800 mm wide is 226.5 pt, consistent)


def _rect_segs(x0, y0, x1, y1):
    return [("M", x0, y0), ("L", x1, y0), ("L", x1, y1), ("L", x0, y1), ("Z",)]


def ring(outer, inner, fill=FRAME, tag="rebuilt-frame"):
    """Frame as one even-odd path (outer rectangle with the inner rectangle cut out)."""
    segs = _rect_segs(*outer) + _rect_segs(*inner)
    return Path(segs, fill=fill, evenodd=True, box=tuple(outer), tag=tag)


def _arc(cx, cy, r, a0, a1):
    """One cubic for the arc a0..a1 (radians, source coordinates, y down). Returns segs without the M."""
    k = 4 / 3 * math.tan((a1 - a0) / 4)
    p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
    p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
    c1 = (p0[0] - k * r * math.sin(a0), p0[1] + k * r * math.cos(a0))
    c2 = (p1[0] + k * r * math.sin(a1), p1[1] - k * r * math.cos(a1))
    return p0, [("C", *c1, *c2, *p1)]


def _crop_gradient(shape, box):
    """Copy of a gradient shape reduced to a rectangle (the gradient axis is kept, so it is a true crop)."""
    p = copy.copy(shape)
    x0, y0, x1, y1 = box
    p.segs = _rect_segs(x0, y0, x1, y1)
    p.box = (x0, y0, x1, y1)
    return p


def _spacer(box):
    x0, y0, x1, y1 = box
    return Path(_rect_segs(x0, y0, x1, y1), fill=GREY, stroke=LINE, width=0.5, box=box, tag="rebuilt-spacer")


def _pole(x0, x1, y0, y1):
    """Pole koker 100x200 as flat PY-Grijs bar. The source shows a raster fade to white at the bottom; the
    bar stops at y1 (where the fade is half way) and is open at the bottom."""
    fill = Path(_rect_segs(x0, y0, x1, y1), fill=GREY, box=(x0, y0, x1, y1), tag="rebuilt-pole")
    side = Path([("M", x0, y1), ("L", x0, y0), ("L", x1, y0), ("L", x1, y1)], stroke=LINE, width=0.5,
                box=(x0, y0, x1, y1), tag="rebuilt-pole-outline")
    mid = Path([("M", x1, y0), ("L", x1, y1)], stroke=LINE, width=0.5, box=(x1, y0, x1, y1), tag="rebuilt-pole-outline")
    return [fill, side, mid]


# ================================================================ p12 aanrijroute
P12_OUT = (198.337, 245.294, 481.802, 599.625)
P12_IN = (205.285, 252.243, 474.852, 592.676)
P12_CUT = 245.294 + (481.802 - 198.337)  # 1000 x 1000 face: the dashed line "geen display" at 1000 mm
P12_RING = 205.285 - 198.337
P12_NOTE = ("Gradient rebuilt from the clip path of the source raster shading, re-measured as a real SVG gradient. "
            "The #182F72 frame fill of the source is a soft-masked shadow effect drawn as outer plus inner rectangle; "
            "it is skipped and the lichtbakprofiel frame is rebuilt as an even-odd ring in RAL 5002 (PY-Blauw). ")


def _p12_clip(src):
    return [c for c in src.clips(12, (198, 245, 483, 600)) if abs(c.box[2] - c.box[0] - 283.46) < 1][0]


def _p12_art(src, bottom=None):
    def skip(p):
        return p.seq == 206 or callout_dot(p)

    box = (198, 245, 483, 600 if bottom is None else bottom)
    return crop(src, 12, box, skip=skip)


def _p12_face(src, display=True):
    g = gradient_shape(src, 12, _p12_clip(src))
    if display:
        return [g, ring(P12_OUT, P12_IN)] + _p12_art(src)
    g = _crop_gradient(g, (P12_OUT[0], P12_OUT[1], P12_OUT[2], P12_CUT))
    art = [p for p in _p12_art(src, P12_CUT) if p.fill != "#1D1D1B" or p.box[3] < P12_CUT]
    out = (P12_OUT[0], P12_OUT[1], P12_OUT[2], P12_CUT)
    inn = (P12_IN[0], P12_IN[1], P12_IN[2], P12_CUT - P12_RING)
    return [g, ring(out, inn)] + art


def _p12_pole():
    # pole box in the drawing: x 159.0 to 186.8 (100 mm), top level with the face top
    return _pole(158.99, 186.836, 245.544, 705.0)


@element("py-prod-lichtbak-aanrijroute-display", "2.1 Uitsteeklichtbak in aanrijroute, met display", "prod", "lichtbak", 12,
         variables=("arrow direction", "display state"), built_from=("py-comp-face-aanrijroute",))
def _(src):
    spacer = _spacer((186.793, 256.385, 198.631, 588.535))
    items = _p12_pole() + [spacer] + _p12_face(src, True)
    return items, dict(status="rebuilt", mm_per_pt=S12, true_scale=True, dims_mm=(1000, 1250, 200),
                       notes=P12_NOTE + "Front elevation only (no top view, no 3D render). Pole grey fade is a raster in the "
                       "source: rebuilt as a flat PY-Grijs bar (RAL 9006) of the visible length, open at the bottom; the pole "
                       "length is not specified (min 2500 mm above ground). Display VRIJ LED dots are extracted source paths.")


@element("py-prod-lichtbak-aanrijroute-nodisplay", "2.1 Uitsteeklichtbak in aanrijroute, zonder display", "prod", "lichtbak", 12,
         variables=("arrow direction",), built_from=("py-comp-face-aanrijroute",))
def _(src):
    sp_bot = P12_CUT - (599.625 - 588.535)
    spacer = _spacer((186.793, 256.385, 198.631, sp_bot))
    items = _p12_pole() + [spacer] + _p12_face(src, False)
    return items, dict(status="rebuilt", mm_per_pt=S12, true_scale=True, dims_mm=(1000, 1000, 200),
                       notes=P12_NOTE + "Variant without display: the 1000 x 1000 face of the handbook (dashed line 'indien geen "
                       "display geplaatst'). Face cropped at 1000 mm height with the same gradient axis, bottom frame edge rebuilt, "
                       "display left out, spacer shortened to keep the 40 mm margins. Pole as in the display variant (flat grey, raster fade replaced).")


@element("py-comp-face-aanrijroute", "lichtbakfront aanrijroute", "comp", "lichtbak", 12,
         variables=("arrow direction", "display fitted"),
         built_from=("py-atom-symbol-p-roof", "py-atom-arrow-right-plain", "py-atom-logo-beeldmerk-reverse"))
def _(src):
    return _p12_face(src, True), dict(status="rebuilt", mm_per_pt=S12, true_scale=True, dims_mm=(1000, 1250),
                                      notes=P12_NOTE + "Face with display zone (VRIJ state) as drawn.")


@element("py-atom-symbol-p-roof", "P met dak", "atom", "symbol", (12, 14, 15, 23, 37, 38), variables=("colour",))
def _(src):
    return crop(src, 12, (226, 276, 382.2, 475.5), texts=False), dict(
        mm_per_pt=S12, true_scale=True,
        notes="Taken from p12 (white P with chevron roof, lichtbak 1:10 scale).")


@element("py-atom-arrow-right-plain", "pijl rechts", "atom", "arrow", (12, 28), variables=("colour",))
def _(src):
    return crop(src, 12, (382, 429, 454, 501), texts=False), dict(
        mm_per_pt=S12, true_scale=True, notes="Lichtbak arrow of p12 (white). The route arrow of p28 is not extracted here.")


# ================================================================ p14 entree
P14_OUT = (198.901, 316.323, 482.366, 599.787)


def _p14_face(src):
    clip = [c for c in src.clips(14, (198, 316, 483, 600)) if len(c.segs) == 5][0]
    g = gradient_shape(src, 14, clip)
    # seq 63..81 are white soft-mask rectangles and hairlines over the whole face; the frame is the 7.09 pt stroke
    art = crop(src, 14, (198, 316, 483, 600), skip=lambda p: 62 < p.seq < 82 or callout_dot(p))
    return [g] + art


@element("py-prod-lichtbak-entree", "3.1 Uitsteeklichtbak bij entree", "prod", "lichtbak", 14,
         variables=("location name", "arrow direction"), built_from=("py-comp-face-entree",))
def _(src):
    spacer = crop(src, 14, (187, 327, 199.5, 589), texts=False)
    return spacer + _p14_face(src), dict(
        status="rebuilt", mm_per_pt=S14, true_scale=True, dims_mm=(1000, 1000, 100),
        notes="Front elevation only (no top view, no wall boxes, no 3D render). Face gradient rebuilt from the clip path of the "
              "source raster shading and re-measured as a real SVG gradient; all other paths, the spacer (aluminium koker 40x70, "
              "RAL 9006) and live text 'Fellenoord' are extracted. The white soft-mask rectangles of the source are skipped. "
              "Frame is the source 7.09 pt stroke, brand-normalised RAL 5002.")


@element("py-comp-face-entree", "lichtbakfront entree", "comp", "lichtbak", 14,
         variables=("location name", "arrow direction"),
         built_from=("py-atom-logo-horizontal-reverse", "py-atom-symbol-p-roof", "py-atom-arrow-downleft-plain"))
def _(src):
    return _p14_face(src), dict(status="rebuilt", mm_per_pt=S14, true_scale=True, dims_mm=(1000, 1000),
                                notes="Gradient rebuilt from the clip path of the source raster shading (real SVG gradient). "
                                      "Paths and the live text 'Fellenoord' are extracted.")


@element("py-atom-arrow-downleft-plain", "pijl linksonder", "atom", "arrow", 14, variables=("colour",))
def _(src):
    return crop(src, 14, (234, 479, 293, 538), texts=False), dict(
        mm_per_pt=S14, true_scale=True, notes="White arrow of the lichtbak entree (p14, 1:10 scale).")


@element("py-comp-location-name-slot", "locatienaam slot", "comp", "lichtbak", (14, 37, 38, 40), variables=("location name",))
def _(src):
    items = crop(src, 14, (270, 548, 412, 585), skip=lambda p: True)
    return items, dict(mm_per_pt=S14, true_scale=True,
                       notes="Generic name field: live text in Ubuntu Bold, white (here 'Fellenoord' from p14, 25 pt at 1:10). "
                             "Replace the text with the location name. Aqua variant is the same slot with fill #32B9CD.")


# ================================================================ p37 voetganger liggend
P37_OUT = (158.740, 208.819, 867.401, 293.858)
P37_IN = (165.827, 215.906, 860.315, 286.772)
P37_ARC = (670.35, 250.05, 103.95)  # navy circle that cuts the white tab


def _p37_face(src):
    x0, y0, x1, y1 = P37_OUT
    cx, cy, r = P37_ARC
    dy = y1 - cy
    dx = math.sqrt(r * r - dy * dy)
    a = math.atan2(dy, dx)
    p0, arc = _arc(cx, cy, r, a, -a)  # from bottom to top, bulging to the right
    # white tab: top edge, right edge, bottom edge, then the arc of the navy circle back up to the top
    # (arc runs from angle +a to -a and bulges to the right, into the tab)
    segs = [("M", cx + dx, y0), ("L", x1, y0), ("L", x1, y1), ("L", cx + dx, y1)] + arc + [("Z",)]
    tab = Path(segs, fill="#FFFFFF", box=(cx + dx, y0, x1, y1), tag="rebuilt-tab")
    base = rect_item(x0, y0, x1, y1, fill="#1A3580", tag="rebuilt-face")
    # aqua P block: the source is an aqua disc (clipped to the block) over a thin raster sliver that fades from mid blue
    # to navy along the clip arc. The gradient fit does not work on this near flat raster, so it is set by hand
    # from sampled colours (aqua #32B9CD flat, sliver #097FB0 to navy).
    clip = [c for c in src.clips(37, (150, 200, 260, 300)) if len(c.segs) == 8][0]
    sliver = copy.copy(clip)
    sliver.fill = Gradient(243.0, 250.0, 247.5, 250.0, [(0.0, "#097FB0"), (0.6, "#097FB0"), (1.0, "#1A3580")])
    sliver.tag = "rebuilt-gradient"
    dcx, dcy, dr = 139.9, 250.05, 103.95
    at = math.atan2(y0 - dcy, math.sqrt(dr * dr - (y0 - dcy) ** 2))
    ab = math.atan2(y1 - dcy, math.sqrt(dr * dr - (y1 - dcy) ** 2))
    q0, darc = _arc(dcx, dcy, dr, at, ab)
    disc = Path([("M", x0, y0), ("L", q0[0], y0)] + [("L", q0[0], q0[1])] + darc + [("L", x0, y1), ("Z",)],
                fill="#32B9CD", box=(x0, y0, dcx + dr, y1), tag="rebuilt-aqua-block")
    aqua = [sliver, disc]

    def skip(p):
        if p.seq in (60, 61, 87) or callout_dot(p):
            return True
        return (p.box[2] - p.box[0]) > 150  # soft-mask circles

    art = crop(src, 37, (158, 208, 868, 294.5), skip=skip)
    return [base, tab] + aqua + art + [ring(P37_OUT, P37_IN)]


P37_NOTE = ("Face rebuilt: navy base, white tab cut by the navy circle (arc taken from the source clip circle), aqua P block as "
            "a real SVG gradient from the clip path of the source raster, ring frame (source draws it as outer plus inner "
            "rectangle) as an even-odd path in RAL 5002 (PY-Blauw). P roof, beeldmerk, pedestrian and live text 'City Tower' are extracted. ")


@element("py-prod-lichtbak-voetganger-liggend", "5.1 Voetgangersentree lichtbak (liggend)", "prod", "lichtbak", 37,
         variables=("location name",), built_from=("py-comp-face-voetganger-liggend",))
def _(src):
    return _p37_face(src), dict(status="rebuilt", mm_per_pt=S37, true_scale=True, dims_mm=(2500, 300, 100),
                                notes=P37_NOTE + "Front elevation only (no side view, no 3D render).")


@element("py-comp-face-voetganger-liggend", "lichtbakfront liggend", "comp", "lichtbak", 37,
         variables=("location name",),
         built_from=("py-atom-symbol-p-roof", "py-atom-logo-beeldmerk-reverse", "py-atom-picto-pedestrian"))
def _(src):
    return _p37_face(src), dict(status="rebuilt", mm_per_pt=S37, true_scale=True, dims_mm=(2500, 300), notes=P37_NOTE)


# ================================================================ p38 voetganger staand
def _p38_face(src):
    clip = [c for c in src.clips(38, (198, 316, 427, 600)) if len(c.segs) == 5][0]
    g = gradient_shape(src, 38, clip)
    art = crop(src, 38, (198, 316, 427, 600), skip=lambda p: callout_dot(p) or p.seq in (62,))
    return [g] + art


@element("py-prod-lichtbak-voetganger-staand", "5.2 Voetgangersentree lichtbak (staand)", "prod", "lichtbak", 38,
         variables=("location name",), built_from=("py-comp-face-voetganger-staand",))
def _(src):
    spacer = crop(src, 38, (187, 327, 199.5, 589), texts=False)
    return spacer + _p38_face(src), dict(
        status="rebuilt", mm_per_pt=S38, true_scale=True, dims_mm=(800, 1000, 100),
        notes="Front elevation only (no top view, no wall boxes, no side view, no 3D renders). Face gradient rebuilt from the clip "
              "path of the source raster shading (real SVG gradient); spacer (koker 40x70, RAL 9006), frame stroke, logo, P roof, "
              "pedestrian and live text 'City Tower' are extracted.")


@element("py-comp-face-voetganger-staand", "lichtbakfront voetgangersentree", "comp", "lichtbak", 38,
         variables=("location name",),
         built_from=("py-atom-logo-horizontal-reverse", "py-atom-symbol-p-roof", "py-atom-picto-pedestrian"))
def _(src):
    return _p38_face(src), dict(status="rebuilt", mm_per_pt=S38, true_scale=True, dims_mm=(800, 1000),
                                notes="Gradient rebuilt from the clip path of the source raster shading (real SVG gradient). "
                                      "All other paths and the live text 'City Tower' are extracted.")
