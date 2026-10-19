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

NAVY, AQUA, WHITE = "#1A3580", "#32B9CD", "#FFFFFF"
LED_ON, LED_OFF = WHITE, AQUA  # lit dots white, unlit dots PY-Aqua at 22 percent: brand colours only

W = 400.0            # column width, as the pyloon panel
HEADER_H = 420.0
BAND_H = 110.0       # blauw to aqua band at the foot of the header
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
    """Free-spaces counter: PY-Blauw bezel with an aqua hairline and a dot matrix, lit dots white, unlit dots PY-Aqua at 22 percent."""
    n = len(digits)
    cols = n * 5 + (n - 1)
    pitch = min((w - 36) / cols, (h - 36) / 7)
    r = pitch * 0.355
    gx = x0 + (w - (cols - 1) * pitch) / 2
    gy = y0 + (h - 6 * pitch) / 2
    with d.group(gid or "counter"):
        d.rect(x0, y0, x0 + w, y0 + h, fill=NAVY, gid="bezel")
        d.rect(x0 + 0.6, y0 + 0.6, x0 + w - 0.6, y0 + h - 0.6, fill="none", stroke=AQUA, sw=1.2, gid="bezel-line")
        with d.group("dots-off"):
            for i, ch in enumerate(digits):
                for ry, row in enumerate(FONT[ch]):
                    for cx_, bit in enumerate(row):
                        if bit == "0":
                            d.circle(gx + (i * 6 + cx_) * pitch, gy + ry * pitch, r, fill=LED_OFF, opacity=0.22)
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
        '<linearGradient id="py-zuil-verloop" gradientUnits="userSpaceOnUse" x1="0" y1="%g" x2="0" y2="%g">'
        '<stop offset="0" stop-color="#1A3580"/><stop offset="0.18" stop-color="#1A3580"/>'
        '<stop offset="0.62" stop-color="#097BAE"/><stop offset="1" stop-color="#32B9CD"/></linearGradient>' % (HEADER_H, HEADER_H - BAND_H))
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit",
           "py-tok-gradient-verloop", "py-tok-type-ubuntu-bold", "py-tok-type-ubuntu-medium")

    with d.group("body"):
        d.rect(0, 0, W, H - PLINTH_H, fill=NAVY, gid="column")
    with d.group("header"):
        d.rect(0, 0, W, HEADER_H, fill=AQUA, gid="header-aqua")
        d.rect(0, HEADER_H - BAND_H, W, HEADER_H, fill="url(#py-zuil-verloop)", gid="header-verloop")
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
        d.rect(0, H - PLINTH_H, W, H, fill=AQUA, gid="plinth-plate")
    if H0 is None:
        return zuil(with_counter, digits, H=round(d.end_y))
    return d


# ---------------------------------------------------------------------------------------------- 2000 mm designs
H2 = 2000.0
V2_HEADER, V2_BAND = 580.0, 115.0          # blauw style: aqua header with the verloop band into the column
V2_PLINTH_TOP = 1935.0
MESSAGES = {
    "public": dict(slug="publiek-parkeren", name="Public parking 24/7",
                   lines=(("PUBLIC", "main"), ("PARKING", "main"), ("24/7", "aqua"))),
    "abonnee": dict(slug="abonnees", name="Alleen voor abonnees",
                    lines=(("Alleen voor", "main"), ("abonnees!", "main"))),
}


def _subscriber_text(d, main, wit):
    """Subscribers copy (NL and EN, as on the existing banner) with the warning triangle on top, readable sub lines and the fault number."""
    nl = ("Alleen voor", "abonnees!")
    en = ("Subscribers", "only!")
    subs = (("Geen abonnement =", "Geen toegang."), ("No subscription =", "No access."))
    size = 350.0 / max(text_width(t, 1.0, 700) for t in nl + en)
    ssz = min(size * 0.62, 340.0 / max(text_width(t, 1.0, 500) for pair in subs for t in pair))
    tri = NAVY if wit else AQUA
    with d.group("warning"):
        d.place("py-atom-icon-warning-triangle", CX, 630, w=124, anchor="tc", gid="warning-triangle", recolor={"#71CBDF": tri})
    y = 630 + 124 * 302.706 / 346.786 + 20 + size * 0.75
    with d.group("headline", data_variable="headline"):
        for t in nl:
            d.text(CX - text_width(t, size, 700) / 2, y, t, size=size, fill=main, weight=700, gid=f"headline-nl-{len(t)}")
            y += size * 1.2
    y += ssz * 0.35
    with d.group("subline-nl", data_variable="subline-nl"):
        for t in subs[0]:
            d.text(CX - text_width(t, ssz, 500) / 2, y, t, size=ssz, fill=main, weight=500)
            y += ssz * 1.3
    y += size * 0.45
    d.rect(150, y, 250, y + 3, fill=AQUA, gid="language-divider")
    y += 3 + size * 0.45 + size * 0.75
    with d.group("headline-en"):
        for t in en:
            d.text(CX - text_width(t, size, 700) / 2, y, t, size=size, fill=main, weight=700)
            y += size * 1.2
    y += ssz * 0.35
    with d.group("subline-en", data_variable="subline-en"):
        for t in subs[1]:
            d.text(CX - text_width(t, ssz, 500) / 2, y, t, size=ssz, fill=main, weight=500)
            y += ssz * 1.3
    d.variables["headline"] = "Alleen voor abonnees! / Subscribers only!"
    d.variables["subline-nl"] = "Geen abonnement = Geen toegang."
    d.variables["subline-en"] = "No subscription = No access."
    num = "085 21 30 422"
    nsz = 330.0 / text_width(num, 1.0, 700)
    base = 1500.0
    assert y < base - nsz, (y, base)
    d.text(CX - text_width(num, nsz, 700) / 2, base, num, size=nsz, fill=main, weight=700, gid="phone-number", variable="phone-number")


def zuil2(style, message):
    """Column at 400 x 2000 mm. style 'blauw' = PY-Blauw column with aqua header, 'wit' = white column with PY-Blauw header (curved edge as on the
    info pylon). message 'public' = PUBLIC PARKING 24/7, 'abonnee' = ALLEEN VOOR ABONNEMENTSHOUDERS. Positions measured from the approved layout."""
    wit = style == "wit"
    msg = MESSAGES[message]
    pid = f"py-prod-zuil-{msg['slug']}-{style}"
    d = Doc(pid, f"Informatiezuil {msg['name']}, {'wit' if wit else 'blauw'}", tight=True)
    main = NAVY if wit else WHITE
    d.uses("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-wit", "py-tok-gradient-verloop", "py-tok-type-ubuntu-bold")
    if wit:
        d.defs["py-zuil-edge"] = (
            '<linearGradient id="py-zuil-edge" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="830" y2="0">'
            '<stop offset="0" stop-color="#1A3580"/><stop offset="1" stop-color="#32B9CD"/></linearGradient>')
    else:
        d.defs["py-zuil-verloop"] = (
            '<linearGradient id="py-zuil-verloop" gradientUnits="userSpaceOnUse" x1="0" y1="%g" x2="0" y2="%g">'
            '<stop offset="0" stop-color="#1A3580"/><stop offset="0.18" stop-color="#1A3580"/>'
            '<stop offset="0.62" stop-color="#097BAE"/><stop offset="1" stop-color="#32B9CD"/></linearGradient>' % (V2_HEADER, V2_HEADER - V2_BAND))

    with d.group("body"):
        d.rect(0, 0, W, V2_PLINTH_TOP, fill=WHITE if wit else NAVY, gid="column")
    with d.group("header"):
        if wit:
            d.path("M0 0H400V519C340 529 220 534 140 533S30 532 0 531Z", (0, 0, 400, 534), fill="url(#py-zuil-edge)", gid="header-edge")
            d.path("M0 0H400V491C340 501 220 506 140 505S30 502 0 501Z", (0, 0, 400, 506), fill=NAVY, gid="header-navy")
        else:
            d.rect(0, 0, W, V2_HEADER, fill=AQUA, gid="header-aqua")
            d.rect(0, V2_HEADER - V2_BAND, W, V2_HEADER, fill="url(#py-zuil-verloop)", gid="header-verloop")
        d.place("py-atom-symbol-p-roof", CX, 76, w=276, anchor="tc")

    if message == "abonnee":
        _subscriber_text(d, main, wit)
    else:
        size = 350.0 / max(text_width(t, 1.0, 700) for t, _ in msg["lines"])
        base0, pitch = 760.0, (size * 1.2, size * 1.55)
        ys = [base0, base0 + pitch[0], base0 + pitch[0] + pitch[1]]
        sizes = [size, size, size * 1.45]
        with d.group("headline", data_variable="headline"):
            for i, ((t, col), y, sz) in enumerate(zip(msg["lines"], ys, sizes)):
                d.text(CX - text_width(t, sz, 700) / 2, y, t, size=sz, fill=AQUA if col == "aqua" else main, weight=700, gid=f"headline-{i + 1}")
        d.variables["headline"] = " ".join(t for t, _ in msg["lines"])
        arrow_top = 1106.0

    if message == "public":
        with d.group("direction"):
            d.place("py-atom-arrow-up-circle", CX, arrow_top, w=134, anchor="tc", gid="arrow", recolor={"#FFFFFF": NAVY} if wit else None)
        d.variables["arrow direction"] = "up"
    d.rect(0, 1574.2, W, 1578.2, fill=AQUA, gid="divider")
    with d.group("lockup"):
        d.place("py-atom-logo-stacked-color" if wit else "py-atom-logo-stacked-white", CX, 1661, w=238, anchor="tc")
        ls = 208.0 / text_width("Locatienaam", 1.0, 700)
        d.text(CX - 104.0, 1878, "Locatienaam", size=ls, fill=main, weight=700, gid="location-name", variable="location name")
    with d.group("plinth"):
        d.rect(0, V2_PLINTH_TOP, W, H2, fill=AQUA, gid="plinth-plate")
    return d


def main():
    no_json = "--no-json" in sys.argv
    built = {}
    jobs = [("comp", comp_counter()), ("prod", zuil(True)), ("prod", zuil(False))]
    jobs += [("prod", zuil2(st, m)) for m in ("public", "abonnee") for st in ("blauw", "wit")]
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
            notes="Dot matrix counter (5 x 7 dots per digit, three digits shown: 071) in a PY-Blauw bezel with an aqua hairline. REBUILT: new construction (no source drawing); lit dots white, unlit dots PY-Aqua at 22 percent "
                  "(brand colours only; the portal displays in the handbook use LED green and red). Variable free-spaces is the digit string."),
        "py-prod-zuil-publiek-parkeren": dict(
            name_nl="Informatiezuil Public parking 24/7, met teller", category="zuil",
            variables=["free-spaces", "headline", "location name", "arrow direction", "counter labels"],
            notes="NEW DESIGN (not in the handbook), modelled on a street pylon with a P header, a free-spaces counter and the line PUBLIC PARKING 24/7. "
                  "Front elevation, 400 x 1750 mm (width as the info pylon panel), PY-Blauw column, aqua header with white P-roof symbol and a "
                  "aqua to blauw band, counter, headline in Ubuntu Bold (24/7 in PY-Aqua), aqua divider, white stacked logo with location name, "
                  "direction arrow, PY-Aqua plinth of 60 mm. Dimensions and the plinth are a proposal; no material, post or foundation drawing. "
                  "Text is live Ubuntu; the counter digits are dots (variable free-spaces)."),
        "py-prod-zuil-publiek-parkeren-zonder-teller": dict(
            name_nl="Informatiezuil Public parking 24/7, zonder teller", category="zuil",
            variables=["headline", "location name", "arrow direction"],
            notes="Same design without the counter block, 400 x 1470 mm. NEW DESIGN (not in the handbook), proposal."),
    }
    for m_ in ("public", "abonnee"):
        for st in ("blauw", "wit"):
            msg = MESSAGES[m_]
            meta[f"py-prod-zuil-{msg['slug']}-{st}"] = dict(
                name_nl=f"Informatiezuil {msg['name']}, {'wit met blauwe header' if st == 'wit' else 'PY-Blauw met aqua header'}",
                category="zuil", variables=(["headline", "location name", "arrow direction"] if m_ == "public" else ["headline", "subline-nl", "subline-en", "phone-number", "location name"]),
                notes=("NEW DESIGN (not in the handbook), 400 x 2000 mm front elevation, positions measured from the approved layout. "
                       + ("White column with PY-Blauw header (curved edge as on the info pylon), headline in PY-Blauw, arrow disc PY-Blauw, colour logo. "
                          if st == "wit" else
                          "PY-Blauw column with PY-Aqua header and the blauw to aqua band into the column, white headline, white arrow disc, white logo. ")
                       + ("Headline PUBLIC PARKING 24/7 (24/7 in PY-Aqua). " if m_ == "public" else
                          "Copy of the existing subscribers banner in this order: warning triangle (py-atom-icon-warning-triangle), Alleen voor abonnees!, Geen abonnement = Geen toegang., Subscribers only!, No subscription = No access., then the fault number 085 21 30 422 (number only, no pill, no arrow). Sub lines on two lines in Ubuntu Medium for legibility. ")
                       + "Plinth PY-Aqua from 1935 mm. Text is live Ubuntu Bold. Proposal, no material or foundation drawing."))
    rows = {e["id"]: i for i, e in enumerate(man["elements"])}
    for eid, (lvl, d) in built.items():
        svg = open(os.path.join(ROOT, "svg", lvl, eid + ".svg"), encoding="utf8").read()
        hexes = []
        for h in re.findall(r'(?:fill|stroke|stop-color)="(#[0-9A-Fa-f]{6})"', svg):
            h = h.upper()
            if h not in hexes:
                hexes.append(h)
        cols = [{"token": hex2tok.get(h), "hex": h} for h in hexes]
        if "url(#py-zuil-verloop)" in svg or "url(#py-zuil-edge)" in svg:
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
        if eid == "py-prod-zuil-publiek-parkeren":
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
