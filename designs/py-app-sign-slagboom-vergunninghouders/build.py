"""New design: slagboombord "Alleen vergunninghouders" (replaces the generic "Private parking / Parking only for permit holders" plate).

Built from library elements (no source print file exists, this is a new design):
  py-atom-symbol-p-plain (white plain P, no roof: this is an open air private parking, not a garage), py-atom-logo-horizontal-white, tokens blauw / aqua / wit, Ubuntu Bold and Regular.
The tow away pictogram is drawn here (new, white on navy).

Run from the repo root:
    python3 -I designs/py-app-sign-slagboom-vergunninghouders/build.py
Writes template.svg (trim plus 3 mm bleed, live text, cut contour), proof.pdf and preview.png next to this file.
Change TRIM below when the measured plate size differs; every position is derived from it.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from pyassets.compose import Doc, text_width  # noqa: E402
from pyassets.core import fmt  # noqa: E402

ID = "py-app-sign-slagboom-vergunninghouders"
NAME = "Bord slagboom vergunninghouders"
NAVY, AQUA, WHITE = "#1A3580", "#32B9CD", "#FFFFFF"

TRIM = (1000.0, 125.0)   # ASSUMPTION: estimated from the photo of the old plate (about 8 : 1); measure before ordering
BLEED = 3.0
RADIUS = 8.0             # corner radius of the plate (proposal)
MARGIN = 30.0            # left and right inner margin

COPY = {
    "line-nl": "Alleen vergunninghouders",
    "line-en": "Permit holders only",
}


def tow_pictogram(d, x, y, h, fill=WHITE, ground=NAVY):
    """Tow away pictogram (tow truck lifting a car), white on navy. Drawn in a 100 x 56 unit box, placed at (x, y) with height h.
    Returns the placed box. Gaps between the shapes are navy strokes so the pictogram stays flat two colour vector."""
    s = h / 56.0
    w = 100.0 * s
    parts = []
    # truck: cab (right) with window, chassis, bed and boom
    parts.append(f'<path d="M58 34 L80 34 L80 16 Q80 13 83 13 L92 13 Q95 13 96.5 16 L100 25 L100 46 L58 46 Z" fill="{fill}"/>')
    parts.append(f'<path d="M84 17 L91.5 17 L95 25 L84 25 Z" fill="{ground}"/>')
    # boom from the bed up and back over the car, with the hook line
    parts.append(f'<path d="M62 35 L40 14" stroke="{fill}" stroke-width="4.2" stroke-linecap="round" fill="none"/>')
    parts.append(f'<path d="M40 14 L40 25" stroke="{fill}" stroke-width="2.2" stroke-linecap="round" fill="none"/>')
    # truck wheels with a navy ring so they read on the white body
    for cx in (68.0, 91.0):
        parts.append(f'<circle cx="{cx}" cy="47" r="7.6" fill="{ground}"/>')
        parts.append(f'<circle cx="{cx}" cy="47" r="5.6" fill="{fill}"/>')
    # car (side view), front lifted towards the hook: drawn level, rotated about the rear wheel
    car = (f'<path d="M0 15 Q0 10 4 9.5 L11 8.5 L17.5 1.5 Q19 0 21 0 L32 0 Q34 0 35.5 1.5 L41 8 L45 9 Q47 9.5 47 12 L47 16 L0 16 Z" fill="{fill}"/>'
           f'<path d="M19.5 3 L26 3 L26 8.5 L14.5 8.5 Z M28.5 3 L32 3 Q33 3 34 4 L37.5 8.5 L28.5 8.5 Z" fill="{ground}"/>'
           f'<circle cx="10" cy="17" r="6.4" fill="{ground}"/><circle cx="10" cy="17" r="4.6" fill="{fill}"/>'
           f'<circle cx="37" cy="17" r="6.4" fill="{ground}"/><circle cx="37" cy="17" r="4.6" fill="{fill}"/>')
    parts.append(f'<g transform="translate(0 33.4) rotate(-17 10 17)">{car}</g>')
    # ground line
    parts.append(f'<path d="M0 55 L100 55" stroke="{fill}" stroke-width="1.6" fill="none"/>')
    ax, ay = d._p(x, y)
    d._emit(f'<g id="py-atom-picto-tow-away" data-element="new" transform="translate({fmt(ax)} {fmt(ay)}) scale({fmt(s)})">{"".join(parts)}</g>',
            (ax, ay, ax + w, ay + h))
    return (x, y, x + w, y + h)


def build():
    W, H = TRIM
    d = Doc(ID, NAME, trim=TRIM, bleed=BLEED)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-regular")
    d.rect(-BLEED, -BLEED, W + BLEED, H + BLEED, fill=NAVY, gid="bleed-background", variable="background-colour", example=NAVY)

    cy = H / 2
    # 1. plain P, white (no roof: the roof marks a garage, this is an open air terrain)
    with d.group("py-atom-symbol-p-plain"):
        p_box = d.place("py-atom-symbol-p-plain", MARGIN + 4, cy, h=H * 0.60, anchor="cl")
    # aqua divider
    div1 = p_box[2] + 26
    d.line(div1, H * 0.20, div1, H * 0.80, stroke=AQUA, sw=2.0, cap="round", gid="divider-left")

    # 4. logo, right aligned
    logo_w = 150.0
    with d.group("py-atom-logo-horizontal-white"):
        logo_box = d.place("py-atom-logo-horizontal-white", W - MARGIN, cy, w=logo_w, anchor="cr")
    div2 = logo_box[0] - 28
    d.line(div2, H * 0.20, div2, H * 0.80, stroke=AQUA, sw=2.0, cap="round", gid="divider-right")

    # 3. tow away pictogram, left of the right divider
    tow_h = H * 0.50
    tow_w = tow_h * 100 / 56
    tow_x = div2 - 28 - tow_w
    tow_pictogram(d, tow_x, cy - tow_h / 2 - 1.5, tow_h)

    # 2. text block between the dividers: NL bold white, EN regular aqua, left aligned
    tx = div1 + 26
    avail = tow_x - 30 - tx
    size_nl = min(40.0, avail / (text_width(COPY["line-nl"], 1, 700)))
    size_en = size_nl * 0.62
    block_h = size_nl * 0.74 + size_en * 1.45 + size_en * 0.20   # cap top of the NL line to the descenders of the EN line
    base_nl = cy - block_h / 2 + size_nl * 0.74
    base_en = base_nl + size_en * 1.45
    shift = 0.0
    with d.group("variables"):
        d.text(tx, base_nl + shift, COPY["line-nl"], size=size_nl, fill=WHITE, weight=700, variable="line-nl", gid="line-nl")
        d.text(tx, base_en + shift, COPY["line-en"], size=size_en, fill=AQUA, weight=400, variable="line-en", gid="line-en")

    d.cut_contour(0, 0, W, H, rx=RADIUS)
    d.guides(W, H)
    return d, dict(size_nl=size_nl, size_en=size_en, text_x=tx, avail=avail)


def main():
    d, info = build()
    svg = d.svg()
    out_svg = os.path.join(HERE, "template.svg")
    open(out_svg, "w", encoding="utf8").write(svg)

    import cairosvg
    # preview without the magenta cut line and with the rounded plate shape, as the sign will look
    W, H = TRIM
    prev = svg.replace('data-spot="ThruCut"', 'data-spot="ThruCut" visibility="hidden"')
    prev = prev.replace(f'<rect x="0" y="0" width="{fmt(W + 2 * BLEED)}" height="{fmt(H + 2 * BLEED)}" fill="{NAVY}"',
                        f'<rect x="{fmt(BLEED)}" y="{fmt(BLEED)}" width="{fmt(W)}" height="{fmt(H)}" rx="{fmt(RADIUS)}" fill="{NAVY}"')
    cairosvg.svg2png(bytestring=prev.encode(), write_to=os.path.join(HERE, "preview.png"), output_width=2400, background_color="white")
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=os.path.join(HERE, "proof.pdf"))

    spec = {
        "id": ID,
        "name_nl": NAME,
        "type": "sign",
        "origin": "new design",
        "replaces": "generic plate 'P Private parking / Parking only for permit holders' with tow away pictogram, on the manual barrier",
        "template": {"trim_mm": list(TRIM), "bleed_mm": BLEED, "size_with_bleed_mm": [TRIM[0] + 2 * BLEED, TRIM[1] + 2 * BLEED],
                     "colour": "RGB hex from tokens.json (official tokens); print values (CMYK) are in tokens.json",
                     "cut_contour": {"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": RADIUS, "note": "proposal"}},
        "variables": {"default": {"background-colour": NAVY, **COPY}},
        "built_from": d.built_from + ["py-atom-picto-tow-away (new, drawn in build.py)"],
        "status": "new",
        "layout_mm": {k: round(v, 2) for k, v in info.items()},
        "notes": ("New barrier plate in the ParkingYou house style: navy PY-Blauw field, white plain P (no roof, not a garage), aqua dividers, Dutch line in Ubuntu Bold white, "
                  "English line in Ubuntu Regular PY-Aqua, white tow away pictogram, white horizontal logo. ASSUMPTION: trim 1000 x 125 mm is estimated "
                  "from the photo (the old plate is about 8 : 1 next to the boom); measure the old plate and the mounting holes before ordering, then change "
                  "TRIM in build.py and rebuild. Mounting holes are not marked (position depends on the bracket). Material proposal: 3 mm aluminium dibond, "
                  "printed and laminated, double sided if the plate is seen from both approaches."),
    }
    json.dump(spec, open(os.path.join(HERE, "spec.json"), "w", encoding="utf8"), indent=1, ensure_ascii=False)
    print(json.dumps(info, indent=1), d.size())


if __name__ == "__main__":
    main()
