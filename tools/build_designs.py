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
KW, KH = 160, 240  # board size asked for this garage (Rick, 20-11-2026): 16 cm wide, 24 cm high (whole cm for Drukwerkdeal)
KK = 110 / 300  # bubble 110 mm wide; scale of the 4.7 layout (bubble 300 mm on the 400 mm board)


@design("py-app-sign-kolom-looproute", "Kolombord looproute uitgang", "sign", (KW, KH), variants=("rechtdoor", "links", "rechts"),
        cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": 10,
                     "note": "Proposal only (the 25 mm corners of handbook 4.7 scaled down). The print PDF has no cut line: choose straight or "
                             "rounded corners at the printer; the background runs into the bleed, so either works."},
        production={"format": "160 x 240 mm (width x height), 3 mm bleed; PDF 166 x 246 mm",
                    "material": "Sign board (for example dibond or forex) or self adhesive foil for the columns",
                    "colour": "Solid PY-Blauw (no verloop, at Rick's request), white bubble and caption, aqua time window. "
                              "Print PDF in DeviceCMYK with the token values: PY-Blauw 100/83/0/17 (200 percent ink), PY-Aqua 69/0/21/0, white 0/0/0/0"},
        notes="New design for the walking route to the exit, laid out like the column boards of handbook 4.7 and 4.8 (bubble on top, caption "
              "below, caption left aligned to the bubble) at 160 x 240 mm, with a solid PY-Blauw face instead of the verloop (requested): white "
              "bubble (py-atom-shape-bubble-solid), navy walking figure and navy route arrow, caption 'Uitgang Voetgangers' and the time window "
              "in aqua (as on the door sticker). The figure always walks towards the arrow (mirrored for links). "
              "Wayfinding only: it does not replace the green escape route signs (NEN-EN-ISO 7010, NEN 6088).")
def _(variant):
    vid = f"py-app-sign-kolom-looproute-{variant}"
    d = Doc(vid, "Kolombord looproute uitgang", trim=(KW, KH), bleed=3)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", TOKENS_TYPE[0], TOKENS_TYPE[1],
           "py-comp-bord-picto-bubble-face", "py-prod-bord-mindervaliden")
    # solid PY-Blauw face: the handbook 4.7 and 4.8 boards use the verloop, these looproute boards are solid on request
    d.rect(-3, -3, KW + 3, KH + 3, fill=BLAUW, gid="bleed-background", variable="background-colour", example=BLAUW)
    bx, by, bw = (KW - 300 * KK) / 2, 13, 300 * KK
    with d.group("py-atom-shape-bubble-solid"):
        d.place("py-atom-shape-bubble-solid", bx, by, w=bw, recolor={"#F08300": WIT})
    # pictograms at the 4.7 position inside the bubble (centre 146 mm below the bubble top on the 400 board)
    figure_and_arrow(d, KW / 2, by + 146 * KK, fig_h=176 * KK, arrow_w=112 * KK, gap=26 * KK, direction=variant)
    x = bx + 7.778 * KK  # caption left edge as on 4.7 (7.8 mm right of the bubble)
    cap = 41.967 * KK
    with d.group("variables"):
        d.text(x, 168, "Uitgang", size=cap, fill=WIT, weight=700, variable="caption-1")
        d.text(x, 168 + 50.361 * KK, "Voetgangers", size=cap, fill=WIT, weight=700, variable="caption-2")
        # last line ends at y 218 and x 141: clear of corner drill holes up to 15 mm from the edges (dibond option)
        d.text(x, 205, "Op werkdagen", size=11.2, fill=AQUA, weight=500, variable="when-1")
        d.text(x, 218, "van 7:00 tot 10:00 uur", size=11.2, fill=AQUA, weight=500, variable="when-2")
    d.cut_contour(0, 0, KW, KH, rx=10)
    d.guides(KW, KH)
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


# --------------------------------------------------------------------------------------------- ronde sticker looproute
RD = 100  # diameter in mm (Rick, 20-11-2026: a 10 cm sticker, not a floor sticker)
RS = RD / 400  # the layout was drawn at 400 mm


@design("py-app-sticker-looproute-rond", "Ronde sticker looproute uitgang", "sticker", (RD, RD),
        cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": RD / 2, "note": f"Round, diameter {RD} mm."},
        production={"format": f"Round, diameter {RD} mm (10 cm), 3 mm bleed; PDF {RD + 6} x {RD + 6} mm",
                    "material": "Self adhesive foil, laminated. One design for every direction: rotate the sticker so the arrow points along the route.",
                    "colour": "PY-Blauw CMYK 100/83/0/17, PY-Aqua CMYK 69/0/21/0"},
        notes="New design: round route marker along the walking route. PY-Blauw face (no aqua ring, removed at Rick's request), route arrow as "
              "in the route boards (py-atom-arrow-up-circle: aqua arrow in a white circle), white walking figure and caption. "
              "The background fills the whole page (square bleed), so a cut that shifts never shows white.")
def _(variant):
    vid = "py-app-sticker-looproute-rond"
    d = Doc(vid, "Ronde sticker looproute uitgang", trim=(RD, RD), bleed=3)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", TOKENS_TYPE[0], "py-comp-route-module-arrow")
    d.rect(-3, -3, RD + 3, RD + 3, fill=BLAUW, gid="bleed-background")
    with d.group("py-atom-arrow-up-circle"):
        d.place("py-atom-arrow-up-circle", RD / 2, 62 * RS, w=158 * RS, anchor="tc")
    cap, size, fig_h, gap = "Uitgang", 46 * RS, 96 * RS, 16 * RS
    fw = 26.518 / 51.038 * fig_h
    tw = text_width(cap, size, 700)
    x0 = RD / 2 - (fw + gap + tw) / 2
    base = 324 * RS
    with d.group("py-atom-figure-walk"):
        d.place("py-atom-figure-walk", x0, base + 2 * RS, h=fig_h, anchor="bl", recolor={BLAUW: WIT})
    with d.group("variables"):
        d.text(x0 + fw + gap, base - 14 * RS, cap, size=size, fill=WIT, weight=700, variable="caption")
    d.cut_contour(0, 0, RD, RD, rx=RD / 2)
    d.guides(RD, RD)
    return d


# --------------------------------------------------------------------------------------------- sticker druk op de knop
KD = 200  # diameter in mm (20-11-2026): round, larger than the current 'Push' sticker (estimated at about 15 cm); change here
KS = KD / 200  # the layout is drawn at 200 mm


def button_icon(d, cx, cy, u, fill=BLAUW):
    """Pictogram 'press the button': mushroom push button (side view) with a press arrow above it. Drawn for this sticker
    (the library has no button pictogram); u = 1/100 of the drawing scale, the icon is 88u wide and 124u high, centred on (cx, cy)."""
    cy += 4 * u  # optical centre: the icon runs from -66u (arrow tail) to +58u (base)
    with d.group("icon-button"):
        dome = (f"M{cx - 36 * u:.3f} {cy + 14 * u:.3f} A{36 * u:.3f} {32 * u:.3f} 0 0 1 {cx + 36 * u:.3f} {cy + 14 * u:.3f} Z")
        d.path(dome, (cx - 36 * u, cy - 18 * u, cx + 36 * u, cy + 14 * u), fill=fill)
        d.rect(cx - 14 * u, cy + 17 * u, cx + 14 * u, cy + 32 * u, fill=fill)
        d.rect(cx - 44 * u, cy + 35 * u, cx + 44 * u, cy + 58 * u, fill=fill, rx=5 * u)
    with d.group("py-atom-arrow-up-plain"):
        d.place("py-atom-arrow-up-plain", cx, cy - 45 * u, w=42 * u, anchor="cc", rotate=180, recolor={BLAUW: fill})


@design("py-app-sticker-druk-op-de-knop", "Ronde sticker druk op de knop (loopdeur)", "sticker", (KD, KD),
        cut_contour={"spot": "ThruCut", "stroke_pt": 1, "inset_mm": 0.2, "corner_radius_mm": KD / 2, "note": f"Round, diameter {KD} mm."},
        production={"format": f"Round, diameter {KD} mm, 3 mm bleed; PDF {KD + 6} x {KD + 6} mm",
                    "material": "Self adhesive foil, laminated (outdoor), on the door post directly above the exit button",
                    "colour": "PY-Blauw CMYK 100/83/0/17, PY-Aqua CMYK 69/0/21/0"},
        notes="New design asked by the parking host for a pedestrian door that opens with a push button: replaces a round third party "
              "'Push' sticker with a larger round one. PY-Blauw face over the whole page, white mushroom button pictogram with press arrow "
              "(drawn, the library has none), 'Druk op de knop', aqua line 'om de deur te openen', English in medium italic as on the "
              "terminal stickers ('Druk 3 seconden'), route arrow (py-atom-arrow-up-circle, turned down) pointing at the button below.")
def _(variant):
    vid = "py-app-sticker-druk-op-de-knop"
    d = Doc(vid, "Ronde sticker druk op de knop", trim=(KD, KD), bleed=3)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", *TOKENS_TYPE, "py-app-sticker-terminal-druk-3-seconden")
    d.rect(-3, -3, KD + 3, KD + 3, fill=BLAUW, gid="bleed-background")
    c, k = KD / 2, KS
    button_icon(d, c, 47 * k, u=0.42 * k, fill=WIT)
    with d.group("variables"):
        d.text(c, 106 * k, "Druk op", size=25 * k, fill=WIT, weight=700, anchor="middle", variable="heading-1")
        d.text(c, 131 * k, "de knop", size=25 * k, fill=WIT, weight=700, anchor="middle", variable="heading-2")
        d.text(c, 148 * k, "om de deur te openen", size=10 * k, fill=AQUA, weight=500, anchor="middle", variable="sub")
        d.text(c, 160 * k, "Press the button to open the door", size=6.6 * k, fill=WIT, weight=500, italic=True, anchor="middle",
               variable="en")
    with d.group("py-atom-arrow-up-circle"):
        d.place("py-atom-arrow-up-circle", c, 177 * k, w=22 * k, anchor="cc", rotate=180)  # points down at the button
    d.cut_contour(0, 0, KD, KD, rx=KD / 2)
    d.guides(KD, KD)
    return d


# --------------------------------------------------------------------------------------------- build
BAD =re.compile("[\\u2013\\u2014]|<image|clipPath|<mask|<filter")  # en and em dash written as escapes


def print_svg(svg):
    """Artwork only: drop the cut contour and the hidden guides."""
    svg = re.sub(r'<g id="cut-contour"[^>]*>.*?</g>', "", svg, flags=re.S)
    return re.sub(r'<g id="guides"[^>]*>.*?</g>', "", svg, flags=re.S)


# token RGB (as cairo writes it, 6 decimals) to the official CMYK of tokens.json; white is no ink
CMYK = {"#1A3580": (1.00, 0.83, 0.00, 0.17), "#32B9CD": (0.69, 0.00, 0.21, 0.00), "#FFFFFF": (0, 0, 0, 0)}
_RGB_OP = re.compile(rb"(?<![\w.])([\d.]+) ([\d.]+) ([\d.]+) (rg|RG)\b")
_GRAY_OP = re.compile(rb"(?<![\w.])([\d.]+) (g|G)\b")


def to_cmyk(pdf_path, bleed_mm):
    """Rewrite the cairo PDF to DeviceCMYK with the exact token values (no ICC conversion, so PY-Blauw stays 100/83/0/17)
    and set TrimBox and BleedBox. Raises on any colour that is not a token: nothing may be converted by guesswork."""
    import pymupdf

    lut = {tuple(round(int(h[i:i + 2], 16) / 255, 3) for i in (1, 3, 5)): c for h, c in CMYK.items()}

    def rgb(m):
        key = tuple(round(float(m.group(i)), 3) for i in (1, 2, 3))
        if key not in lut:
            raise ValueError(f"{pdf_path}: colour {key} is not a token")
        c = " ".join(f"{v:g}" for v in lut[key]).encode()
        return c + (b" k" if m.group(4) == b"rg" else b" K")

    def gray(m):
        v = float(m.group(1))
        if v not in (0.0, 1.0):
            raise ValueError(f"{pdf_path}: grey {v} is not a token")
        return (b"0 0 0 1" if v == 0 else b"0 0 0 0") + (b" k" if m.group(2) == b"g" else b" K")

    doc = pymupdf.open(pdf_path)
    streams = set()
    for pg in doc:
        streams.update(pg.get_contents())
    for x in range(1, doc.xref_length()):
        if doc.xref_is_stream(x) and doc.xref_get_key(x, "Subtype")[1] == "/Form":
            streams.add(x)
    for x in streams:
        s = _GRAY_OP.sub(gray, _RGB_OP.sub(rgb, doc.xref_stream(x)))
        if re.search(rb"\b(rg|RG|scn|SCN|sc|SC)\b", s):
            raise ValueError(f"{pdf_path}: colour operator left after conversion")
        doc.update_stream(x, s)
    b = bleed_mm * 72 / 25.4
    for pg in doc:
        r = pg.mediabox
        pg.set_bleedbox(r)
        pg.set_trimbox(pymupdf.Rect(r.x0 + b, r.y0 + b, r.x1 - b, r.y1 - b))
    doc.set_metadata({"title": os.path.basename(os.path.dirname(pdf_path)), "producer": "PY-ASSETS tools/build_designs.py",
                      "creator": "cairosvg plus pymupdf", "creationDate": "", "modDate": ""})
    tmp = pdf_path + ".tmp"
    doc.save(tmp, garbage=4, deflate=True, no_new_id=True)
    doc.close()
    os.replace(tmp, pdf_path)


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
            try:
                to_cmyk(os.path.join(out, fn_p), bl)
            except ValueError as e:
                errs.append(str(e))
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
