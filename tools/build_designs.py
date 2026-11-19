#!/usr/bin/env python3
"""Build new designs (not extracted from an existing print file) from the library: designs/<id>/ and designs.json.

A design is an application (level `app`) composed from library atoms and components plus variables, with the same
template rules as applications/ (token colours, trim plus bleed, live Ubuntu text with data-variable, cut-contour group,
hidden guides). There is no reference.svg because there is no earlier print file.

Per design folder:
  template[-<variant>].svg   master file (open in Illustrator; the cut-contour group is the ThruCut line)
  print[-<variant>].pdf      vector print PDF at 1:1 with bleed, artwork only (no cut contour, no guides)
  spec.json                  trim, bleed, production notes, variables, built_from

usage: python3 -I tools/build_designs.py [--only REGEX] [--png DIR]
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

from pyassets.compose import Doc, text_width  # noqa: E402

BLAUW, AQUA, WIT = "#1A3580", "#32B9CD", "#FFFFFF"
TOKENS_TYPE = ("py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-medium", "py-tok-type-ubuntu-regular")
DESIGNS = {}


def design(id, name_nl, type, trim_mm, variants=("",), bleed_mm=3.0, cut_contour=None, production=None, notes=""):
    def deco(fn):
        DESIGNS[id] = dict(fn=fn, id=id, name_nl=name_nl, type=type, trim_mm=list(trim_mm), variants=list(variants),
                           bleed_mm=bleed_mm, cut_contour=cut_contour, production=production or {}, notes=notes)
        return fn
    return deco


def verloop(d, gid, x1, y1, x2, y2):
    """Brand verloop (py-tok-gradient-verloop) as a userSpaceOnUse gradient; coordinates are trim relative."""
    o = d.bleed
    d.defs[gid] = (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1 + o:.3f}" y1="{y1 + o:.3f}" '
                   f'x2="{x2 + o:.3f}" y2="{y2 + o:.3f}"><stop offset="0" stop-color="#1A3580"/><stop offset="0.18" stop-color="#1A3580"/>'
                   f'<stop offset="0.62" stop-color="#097BAE"/><stop offset="1" stop-color="#32B9CD"/></linearGradient>')
    d.uses("py-tok-gradient-verloop")
    return f"url(#{gid})"


ARROW_ROT = {"rechtdoor": 0, "rechts": 90, "links": -90}
ARROW_EXAMPLE = {"rechtdoor": "omhoog (rechtdoor)", "rechts": "rechts", "links": "links"}


def figure_and_arrow(d, cx, cy, fig_h, arrow_w, gap, direction, recolor=None):
    """Walking figure plus route arrow as one centred row. The figure always walks towards the arrow:
    for `links` the arrow comes first and the figure is mirrored."""
    fw = 26.518 / 51.038 * fig_h
    total = fw + gap + arrow_w
    x0 = cx - total / 2
    rc = recolor or {}
    left_first = direction == "links"
    fig_x = x0 + arrow_w + gap if left_first else x0
    arr_cx = x0 + arrow_w / 2 if left_first else x0 + fw + gap + arrow_w / 2
    with d.group("py-atom-figure-walk"):
        d.place("py-atom-figure-walk", fig_x, cy, h=fig_h, anchor="cl", flip_x=left_first, recolor=rc)
    with d.group("py-atom-arrow-up-plain", data_variable="arrow-direction"):
        d.place("py-atom-arrow-up-plain", arr_cx, cy, w=arrow_w, anchor="cc", rotate=ARROW_ROT[direction], recolor=rc)
    d.variables["arrow-direction"] = ARROW_EXAMPLE[direction]


# --------------------------------------------------------------------------------------------- kolombord looproute
@design("py-app-sign-kolom-looproute", "Kolombord looproute uitgang", "sign", (400, 600), variants=("rechtdoor", "links", "rechts"),
        cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": 25,
                     "note": "Board outline with the 25 mm corners of handbook 4.7 and 4.8. As a sticker the same line is the kiss cut."},
        production={"format": "400 x 600 mm, as handbook 4.7 and 4.8 (rijstvlies bord)",
                    "material": "Rijstvlies board 8 mm (wall or column) or 16 mm (pole), full colour foil plus laminate (handbook 4.7). "
                                "Alternative: the same file as a column sticker (wall foil plus laminate) to cover the existing plates.",
                    "colour": "PY-Blauw CMYK 100/83/0/17, PY-Aqua CMYK 69/0/21/0; verloop as py-tok-gradient-verloop"},
        notes="New design for the walking route to the exit, in the 400 x 600 column format of handbook 4.7 and 4.8: gradient face, white bubble "
              "(py-atom-shape-bubble-solid at the bubble position of py-comp-bord-picto-bubble-face), navy walking figure and navy route arrow, "
              "caption in two lines at the caption position and size of 4.7. The figure always walks towards the arrow (mirrored for links). "
              "Wayfinding only: it does not replace the green escape route signs (NEN-EN-ISO 7010, NEN 6088).")
def _(variant):
    vid = f"py-app-sign-kolom-looproute-{variant}"
    d = Doc(vid, "Kolombord looproute uitgang", trim=(400, 600), bleed=3)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", *TOKENS_TYPE[:1], "py-comp-bord-picto-bubble-face",
           "py-prod-bord-mindervaliden")
    # same gradient axis as the measured face of py-comp-bord-picto-bubble-face
    fill = verloop(d, f"{vid}-verloop", 16.366, -17.755, 325.005, 516.307)
    d.rect(-3, -3, 403, 603, fill=fill, gid="bleed-background")
    with d.group("py-atom-shape-bubble-solid"):
        d.place("py-atom-shape-bubble-solid", 50, 50, w=300, recolor={"#F08300": WIT})
    figure_and_arrow(d, 200, 196, fig_h=176, arrow_w=112, gap=26, direction=variant)
    with d.group("variables"):
        d.text(57.778, 488.504, "Uitgang", size=41.967, fill=WIT, weight=700, variable="caption-1")
        d.text(57.778, 538.865, "Voetgangers", size=41.967, fill=WIT, weight=700, variable="caption-2")
    d.cut_contour(0, 0, 400, 600, rx=25)
    d.guides(400, 600)
    return d


# --------------------------------------------------------------------------------------------- deursticker gesloten
@design("py-app-sticker-deur-gesloten", "Deursticker deur gesloten, volg de looproute", "sticker", (297, 420), variants=("links", "rechts"),
        cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": 4.2,
                     "note": "Sticker corner radius is the library proposal (4.2 mm, as on the diefstal footer)."},
        production={"format": "A3 portrait 297 x 420 mm; scales 1:1.414 to A4 without changes (same A ratio)",
                    "material": "Self adhesive foil plus laminate, for the outside of the closed pedestrian doors",
                    "colour": "PY-Blauw CMYK 100/83/0/17, PY-Aqua CMYK 69/0/21/0"},
        notes="New design for the pedestrian doors that are closed on working days. PY-Blauw face, white logo, heading and time window, "
              "white panel with the walking figure and the route arrow (direction per door: links or rechts), English line at the bottom. "
              "Copy in the je form as on the terminal stickers. Time window and texts are variables.")
def _(variant):
    vid = f"py-app-sticker-deur-gesloten-{variant}"
    W, H, M = 297, 420, 24
    d = Doc(vid, "Deursticker deur gesloten", trim=(W, H), bleed=3)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", *TOKENS_TYPE)
    d.rect(-3, -3, W + 3, H + 3, fill=BLAUW, gid="bleed-background")
    with d.group("py-atom-logo-horizontal-white"):
        d.place("py-atom-logo-horizontal-white", M, M, w=96)
    with d.group("variables"):
        d.text(M, 118, "Deur gesloten", size=36, fill=WIT, weight=700, variable="heading")
        d.text(M, 150, "Op werkdagen", size=19, fill=AQUA, weight=500, variable="when-1")
        d.text(M, 174, "van 7:00 tot 10:00 uur", size=19, fill=AQUA, weight=500, variable="when-2")
        d.text(M, 196, "Voor je veiligheid is deze deur dan dicht.", size=10, fill=WIT, weight=400, variable="reason")
    with d.group("panel"):
        d.rect(M, 216, W - M, 356, fill=WIT, rx=16)
        figure_and_arrow(d, W / 2, 258, fig_h=66, arrow_w=50, gap=14, direction=variant)
        with d.group("variables-panel"):
            d.text(W / 2, 315, "Volg de looproute", size=15, fill=BLAUW, weight=700, anchor="middle", variable="instruction-1")
            d.text(W / 2, 336, "naar de uitgang", size=15, fill=BLAUW, weight=700, anchor="middle", variable="instruction-2")
    with d.group("variables-en"):
        d.text(M, 378, "Closed on working days from 7:00 to 10:00.", size=8.6, fill=WIT, weight=400, variable="en-1")
        d.text(M, 390.5, "Please follow the walking route to the exit.", size=8.6, fill=WIT, weight=400, variable="en-2")
    d.cut_contour(0, 0, W, H, rx=4.2)
    d.guides(W, H)
    return d


# --------------------------------------------------------------------------------------------- vloersticker looproute
@design("py-app-sticker-vloer-looproute", "Vloersticker looproute uitgang", "sticker", (400, 400),
        cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": 200, "note": "Round, diameter 400 mm."},
        production={"format": "Round, diameter 400 mm",
                    "material": "Floor graphic foil with anti-slip laminate (slip resistance R10 or better), suitable for car park floors. "
                                "One design for every direction: rotate the sticker so the arrow points along the route.",
                    "colour": "PY-Blauw CMYK 100/83/0/17, PY-Aqua CMYK 69/0/21/0"},
        notes="New design for floor markers along the walking route. PY-Blauw disc, thin aqua ring, route arrow as in the route boards "
              "(py-atom-arrow-up-circle: aqua arrow in a white circle), white walking figure and caption.")
def _(variant):
    vid = "py-app-sticker-vloer-looproute"
    d = Doc(vid, "Vloersticker looproute uitgang", trim=(400, 400), bleed=3)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", TOKENS_TYPE[0], "py-comp-route-module-arrow")
    d.circle(200, 200, 203, fill=BLAUW, gid="bleed-background")
    d.circle(200, 200, 184, fill=None, stroke=AQUA, sw=5, gid="ring")
    with d.group("py-atom-arrow-up-circle"):
        d.place("py-atom-arrow-up-circle", 200, 62, w=158, anchor="tc")
    cap, size, fig_h, gap = "Uitgang", 46, 96, 16
    fw = 26.518 / 51.038 * fig_h
    tw = text_width(cap, size, 700)
    x0 = 200 - (fw + gap + tw) / 2
    base = 324
    with d.group("py-atom-figure-walk"):
        d.place("py-atom-figure-walk", x0, base + 2, h=fig_h, anchor="bl", recolor={BLAUW: WIT})
    with d.group("variables"):
        d.text(x0 + fw + gap, base - 14, cap, size=size, fill=WIT, weight=700, variable="caption")
    d.cut_contour(0, 0, 400, 400, rx=200)
    d.guides(400, 400)
    return d


# --------------------------------------------------------------------------------------------- build
BAD = re.compile("[\\u2013\\u2014]|<image|clipPath|<mask|<filter")  # en and em dash written as escapes


def print_svg(svg):
    """Artwork only: drop the cut contour and the hidden guides."""
    svg = re.sub(r'<g id="cut-contour"[^>]*>.*?</g>', "", svg, flags=re.S)
    return re.sub(r'<g id="guides"[^>]*>.*?</g>', "", svg, flags=re.S)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=".*")
    ap.add_argument("--png", default=os.path.join(ROOT, "build", "designs"), help="preview PNG folder (not committed)")
    a = ap.parse_args()
    import cairosvg

    os.makedirs(a.png, exist_ok=True)
    rows, errs = [], []
    for id_, m in sorted(DESIGNS.items()):
        if not re.search(a.only, id_):
            continue
        out = os.path.join(ROOT, "designs", id_)
        os.makedirs(out, exist_ok=True)
        variants, built, variables = [], [], {}
        tw, th = m["trim_mm"]
        bl = m["bleed_mm"]
        for v in m["variants"]:
            d = m["fn"](v)
            sfx = f"-{v}" if v else ""
            vid = id_ + sfx
            svg = d.svg(group_id=f"{vid}-template")
            w, h = d.size()
            if abs(w - (tw + 2 * bl)) > 0.01 or abs(h - (th + 2 * bl)) > 0.01:
                errs.append(f"{vid}: size {w} x {h} is not trim plus bleed")
            if BAD.search(svg):
                errs.append(f"{vid}: dash, raster, clipPath, mask or filter found")
            if 'id="cut-contour"' not in svg and m["cut_contour"]:
                errs.append(f"{vid}: no cut-contour group")
            fn_t, fn_p = f"template{sfx}.svg", f"print{sfx}.pdf"
            open(os.path.join(out, fn_t), "w", encoding="utf8").write(svg)
            cairosvg.svg2pdf(bytestring=print_svg(svg).encode(), write_to=os.path.join(out, fn_p))
            cairosvg.svg2png(bytestring=svg.replace('visibility="hidden"', ""), write_to=os.path.join(a.png, f"{vid}.png"),
                             output_width=1200 if tw >= th else int(1200 * tw / th) + 1, background_color="#FFFFFF")
            variants.append({"id": vid, "variant": v or None, "template": fn_t, "print_pdf": fn_p, "built_from": list(d.built_from)})
            for b in d.built_from:
                if b not in built:
                    built.append(b)
            variables[v or "default"] = dict(d.variables)
        spec = {
            "id": id_, "name_nl": m["name_nl"], "type": m["type"], "origin": "new", "status": "proposal",
            "variants": variants,
            "template": {"trim_mm": [tw, th], "bleed_mm": bl, "size_with_bleed_mm": [tw + 2 * bl, th + 2 * bl],
                         "colour": "RGB hex from tokens.json (official tokens); print values (CMYK) are in tokens.json",
                         "cut_contour": m["cut_contour"]},
            "production": m["production"],
            "variables": variables,
            "built_from": built,
            "notes": m["notes"],
        }
        json.dump(spec, open(os.path.join(out, "spec.json"), "w", encoding="utf8"), indent=1, ensure_ascii=False)
        rows.append(spec)
        print(f"{id_:45s} {len(variants)} variant(s), {tw:g} x {th:g} mm, built_from {len(built)}")
    if a.only == ".*":
        json.dump({"source": "new designs composed from the library (tools/build_designs.py)", "count": len(rows), "designs": rows},
                  open(os.path.join(ROOT, "designs.json"), "w", encoding="utf8"), indent=1, ensure_ascii=False)
    for e in errs:
        print("PROBLEM", e)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
