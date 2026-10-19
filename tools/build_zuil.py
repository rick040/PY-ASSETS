#!/usr/bin/env python3
"""Info column 'Public parking 24/7' (zuil), modelled on a dark street pylon with a P header, a free-spaces counter and a headline.

Builds from library elements only: py-atom-symbol-p-roof, py-atom-logo-stacked-white, py-atom-arrow-up-circle, token colours and live Ubuntu text.
Writes svg/comp/py-comp-led-counter.svg, svg/prod/py-prod-zuil-publiek-parkeren{,-zonder-teller}.svg and their rows in elements.json.

    python3 -I tools/build_zuil.py            # build the SVGs and update elements.json
    python3 -I tools/build_zuil.py --no-json  # SVGs only
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pyassets.compose import ROOT, Doc, text_width  # noqa: E402

NAVY, AQUA, BLACK, WHITE = "#1A3580", "#32B9CD", "#1D1D1B", "#FFFFFF"
LED_ON, LED_OFF = AQUA, NAVY  # lit dots PY-Aqua, unlit dots PY-Blauw outline: brand colours only

W = 400.0            # column width, as the pyloon panel
HEADER_H = 420.0
PLINTH_H = 60.0
FOOT_PAD = 40.0
CX = W / 2

# 5 x 7 dot matrix, rows top to bottom
FONT = {
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000",) * 7,
}


def counter(d, x0, y0, w=340.0, h=160.0, digits="071", gid=None):
    """Free-spaces counter: black bezel with an aqua hairline (as py-comp-portal-display-slot) and a dot matrix, lit dots in PY-Aqua."""
    n = len(digits)
    cols = n * 5 + (n - 1)
    pitch = min((w - 36) / cols, (h - 36) / 7)
    r = pitch * 0.355
    gx = x0 + (w - (cols - 1) * pitch) / 2
    gy = y0 + (h - 6 * pitch) / 2
    with d.group(gid or "counter"):
        d.rect(x0, y0, x0 + w, y0 + h, fill=BLACK, gid="bezel")
        d.rect(x0 + 0.157, y0 + 0.157, x0 + w - 0.157, y0 + h - 0.157, fill="none", stroke=AQUA, sw=0.314, gid="bezel-line")
        with d.group("dots-off"):
            for i, ch in enumerate(digits):
                for ry, row in enumerate(FONT[ch]):
                    for cx_, bit in enumerate(row):
                        if bit == "0":
                            d.circle(gx + (i * 6 + cx_) * pitch, gy + ry * pitch, r, fill="none", stroke=LED_OFF, sw=0.7)
        with d.group("dots-on", data_variable="free-spaces"):
            for i, ch in enumerate(digits):
                for ry, row in enumerate(FONT[ch]):
                    for cx_, bit in enumerate(row):
                        if bit == "1":
                            d.circle(gx + (i * 6 + cx_) * pitch, gy + ry * pitch, r, fill=LED_ON)
    d.variables["free-spaces"] = digits


def comp_counter():
    d = Doc("py-comp-led-counter", "LED teller vrije plaatsen", tight=True)
    counter(d, 0, 0, gid="py-comp-led-counter-art")
    return d


def zuil(with_counter=True, digits="071", H=None):
    pid = "py-prod-zuil-publiek-parkeren" + ("" if with_counter else "-zonder-teller")
    H0 = H
    H = H or 2400.0   # first pass with a long column; the second pass trims it to the content
    d = Doc(pid, "Informatiezuil Public parking 24/7" + ("" if with_counter else ", zonder teller"), tight=True)
    d.defs["py-zuil-verloop"] = (
        '<linearGradient id="py-zuil-verloop" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="%g" y2="0">'
        '<stop offset="0" stop-color="#1A3580"/><stop offset="0.18" stop-color="#1A3580"/>'
        '<stop offset="0.62" stop-color="#097BAE"/><stop offset="1" stop-color="#32B9CD"/></linearGradient>' % W)
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-zwart", "py-tok-color-wit",
           "py-tok-gradient-verloop", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-medium")

    with d.group("body"):
        d.rect(0, 0, W, H - PLINTH_H, fill=BLACK, gid="column")
    with d.group("header"):
        d.rect(0, 0, W, HEADER_H, fill=NAVY, gid="header-navy")
        d.rect(0, HEADER_H - 26, W, HEADER_H, fill="url(#py-zuil-verloop)", gid="header-verloop")
        d.place("py-atom-symbol-p-roof", CX, 62, w=236, anchor="tc")      # white P with roof, 236 x 303
    y = HEADER_H + 40

    if with_counter:
        counter(d, 20, y, w=360, h=170, digits=digits)
        d.text(CX, y + 170 + 52, "VRIJE PLAATSEN", size=27, fill=WHITE, weight=500, anchor="middle", spacing=1.2, gid="counter-label-nl",
               variable="counter-label-nl")
        d.text(CX, y + 170 + 90, "FREE SPACES", size=27, fill=AQUA, weight=500, anchor="middle", spacing=1.2, gid="counter-label-en",
               variable="counter-label-en")
        y += 285

    # headline: PUBLIC / PARKING in white, 24/7 in aqua; start anchored from the computed width (as in the print apps)
    size = 350.0 / text_width("PARKING", 1.0, 700)
    base = y + 40 + size * 0.72
    lines = (("PUBLIC", WHITE, size, "headline-1", base), ("PARKING", WHITE, size, "headline-2", base + size * 1.2),
             ("24/7", AQUA, size * 1.45, "headline-3", base + size * 1.2 + size * 1.55))
    with d.group("headline", data_variable="headline"):
        for s, col, sz, gid, b in lines:
            d.text(CX - text_width(s, sz, 700) / 2, b, s, size=sz, fill=col, weight=700, gid=gid)
    d.variables["headline"] = "PUBLIC PARKING 24/7"
    y = lines[-1][4] + 55

    d.rect(30, y, W - 30, y + 3, fill=AQUA, gid="divider")
    y += 3 + 70
    with d.group("lockup"):
        box = d.place("py-atom-logo-stacked-white", CX, y, w=230, anchor="tc")
        by = box[3] + 62
        d.text(CX - text_width("Locatienaam", 34, 700) / 2, by, "Locatienaam", size=34, fill=WHITE, weight=700, gid="location-name",
               variable="location name")
    ay = by + 70
    with d.group("direction"):
        d.place("py-atom-arrow-up-circle", CX, ay, w=130, anchor="tc", gid="arrow", recolor={})
    d.variables["arrow direction"] = "up"
    d.end_y = ay + 130 + FOOT_PAD + PLINTH_H

    with d.group("plinth"):
        d.rect(0, H - PLINTH_H, W, H, fill=NAVY, gid="plinth-plate")
    if H0 is None:
        return zuil(with_counter, digits, H=round(d.end_y))
    return d


def main():
    no_json = "--no-json" in sys.argv
    built = {}
    jobs = [("comp", comp_counter()), ("prod", zuil(True)), ("prod", zuil(False))]
    for lvl, d in jobs:
        p = os.path.join(ROOT, "svg", lvl, d.id + ".svg")
        open(p, "w", encoding="utf8").write(d.svg())
        built[d.id] = (lvl, d)
        print("wrote", os.path.relpath(p, ROOT), "%.1f x %.1f mm" % d.size())
    if no_json:
        return
    mp = os.path.join(ROOT, "elements.json")
    man = json.load(open(mp, encoding="utf8"))
    tokens = json.load(open(os.path.join(ROOT, "tokens.json"), encoding="utf8"))
    hex2tok = {v["hex"].upper(): k for k, v in tokens["colors"].items() if v["kind"] in ("brand", "observed")}
    hex2tok.pop("#FFFFFF", None)
    hex2tok["#FFFFFF"] = "py-tok-color-wit"
    meta = {
        "py-comp-led-counter": dict(
            name_nl="LED teller vrije plaatsen", category="display", variables=["free-spaces"],
            notes="Dot matrix counter (5 x 7 dots per digit, three digits shown: 071) in a black bezel with an aqua hairline, same bezel as "
                  "py-comp-portal-display-slot. REBUILT: new construction (no source drawing); lit dots PY-Aqua, unlit dots as PY-Blauw outline "
                  "(brand colours only; the portal displays in the handbook use LED green and red). Variable free-spaces is the digit string."),
        "py-prod-zuil-publiek-parkeren": dict(
            name_nl="Informatiezuil Public parking 24/7, met teller", category="zuil",
            variables=["free-spaces", "headline", "location name", "arrow direction", "counter labels"],
            notes="NEW DESIGN (not in the handbook), modelled on a street pylon with a P header, a free-spaces counter and the line PUBLIC PARKING 24/7. "
                  "Front elevation, 400 x 1750 mm (width as the info pylon panel), black column (PY-Zwart), navy header with white P-roof symbol and a "
                  "blauw to aqua band, counter, headline in Ubuntu Bold (24/7 in PY-Aqua), aqua divider, white stacked logo with location name, "
                  "direction arrow, PY-Blauw plinth of 60 mm. Dimensions and the plinth are a proposal; no material, post or foundation drawing. "
                  "Text is live Ubuntu; the counter digits are dots (variable free-spaces)."),
        "py-prod-zuil-publiek-parkeren-zonder-teller": dict(
            name_nl="Informatiezuil Public parking 24/7, zonder teller", category="zuil",
            variables=["headline", "location name", "arrow direction"],
            notes="Same design without the counter block, 400 x 1470 mm. NEW DESIGN (not in the handbook), proposal."),
    }
    rows = {e["id"]: i for i, e in enumerate(man["elements"])}
    for eid, (lvl, d) in built.items():
        svg = open(os.path.join(ROOT, "svg", lvl, eid + ".svg"), encoding="utf8").read()
        hexes = []
        for h in re.findall(r'(?:fill|stroke|stop-color)="(#[0-9A-Fa-f]{6})"', svg):
            h = h.upper()
            if h not in hexes:
                hexes.append(h)
        cols = [{"token": hex2tok.get(h), "hex": h} for h in hexes]
        if "url(#py-zuil-verloop)" in svg:
            cols.append({"token": "py-tok-gradient-verloop", "hex": None})
        w, h = d.size()
        m = meta[eid]
        row = {
            "id": eid, "name_nl": m["name_nl"], "level": lvl, "category": m["category"], "source_page": None, "status": "rebuilt",
            "dimensions_mm": {"width": round(w, 1), "height": round(h, 1), "stated": None, "basis": "proposal"},
            "colors": cols, "variables": m["variables"],
            "built_from": [b for b in d.built_from if b.startswith(("py-atom", "py-comp"))],
            "tags": ["new-design"], "notes": m["notes"], "svg": f"svg/{lvl}/{eid}.svg", "origin": "design",
        }
        if lvl == "prod" and "zonder" not in eid:
            row["built_from"].append("py-comp-led-counter")
        if eid in rows:
            man["elements"][rows[eid]] = row
        else:
            man["elements"].append(row)
    if "count" in man:
        man["count"] = len(man["elements"])
    json.dump(man, open(mp, "w", encoding="utf8"), indent=1, ensure_ascii=False)
    open(mp, "a").write("\n")
    print("elements.json updated:", len(man["elements"]), "rows")


if __name__ == "__main__":
    main()
