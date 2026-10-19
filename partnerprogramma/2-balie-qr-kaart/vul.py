#!/usr/bin/env python3
"""Maakt per partner uit partners.csv een A6-kaart en een tafelstandaard (PDF, 3 mm afloop) en leest de QR-codes terug.

    python3 -I partnerprogramma/2-balie-qr-kaart/vul.py [CODE ...]     zonder code: alle partners
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from ppkit import data, render, template, qr   # noqa: E402

BLEED = 3
FORMATEN = {"a6": ((105, 148), "kaart-a6"), "tafelstandaard": ((105, 296), "tafelstandaard-a6")}
MIN_CODE_MM = 25


def bouw(partner, uit=None):
    """Geeft per bestand: (pdf, verwachte url, aantal verwachte codes, qr-info)."""
    uit = uit or os.path.join(HERE, "export", partner["code"])
    vals = data.partner_values(partner)
    res = []
    for sleutel, ((w, h), naam) in FORMATEN.items():
        svg = open(os.path.join(HERE, f"template-{sleutel}.svg"), encoding="utf-8").read()
        gevuld, info = template.process(svg, vals)
        for f in info["flow"]:
            if f["height"] > f["box_h"] + 1e-6:
                raise ValueError(f"{partner['code']}: tekstblok {f['id']} past niet")
        for q in info["qr"]:
            if q["code_mm"] < MIN_CODE_MM or q["quiet_mm"] < 4 * q["module_mm"] - 1e-9:
                raise ValueError(f"{partner['code']}: QR te klein of zonder rustzone: {q}")
        pdf = os.path.join(uit, f"parkingyou-{naam}-{partner['code']}.pdf")
        render.pdf(gevuld, pdf, (w + 2 * BLEED, h + 2 * BLEED), bleed_mm=BLEED,
                   title=f"ParkingYou {naam} {partner['bedrijf']}")
        res.append((pdf, "https://" + partner["link"], len(info["qr"]), info["qr"]))
    return res


def test(res):
    """Rasterizeer de gemaakte PDF en lees de code(s). Geeft lijst (pdf, dpi, ok, gelezen)."""
    out = []
    for pdf, url, n, info in res:
        for dpi in (300, 150, 100):
            pagina = qr.decode_pdf(pdf, dpi)[0]
            out.append((pdf, dpi, len(pagina) == n and all(t == url for t in pagina), pagina))
    return out


if __name__ == "__main__":
    alle = data.partners()
    codes = sys.argv[1:]
    gekozen = [p for p in alle if not codes or p["code"] in codes]
    fout = 0
    for p in gekozen:
        res = bouw(p)
        for pdf, dpi, ok, gelezen in test(res):
            fout += not ok
            print("OK  " if ok else "FOUT", os.path.relpath(pdf, HERE), f"{dpi} dpi", gelezen)
    sys.exit(1 if fout else 0)
