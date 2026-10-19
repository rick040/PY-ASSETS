#!/usr/bin/env python3
"""Vult template.svg per locatie en exporteert PDF (drukklaar, 3 mm afloop) en PNG (mail).

    python3 -I partnerprogramma/1-onepager/vul.py [HOF PLA]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from ppkit import data, render, template   # noqa: E402

TRIM = (210, 297)
BLEED = 3


def bouw(code, uit=None):
    uit = uit or os.path.join(HERE, "export", code)
    svg = open(os.path.join(HERE, "template.svg"), encoding="utf-8").read()
    vals = data.onepager_values(code)
    gevuld, info = template.process(svg, vals)
    for f in info["flow"]:
        if f["height"] > f["box_h"] + 1e-6:
            raise ValueError(f"{code}: tekstblok {f['id']} past niet ({f['height']:.1f} > {f['box_h']:.1f} mm)")
    naam = f"parkingyou-partnerprogramma-onepager-{code}"
    render.pdf(gevuld, os.path.join(uit, naam + "-druk.pdf"), (TRIM[0] + 2 * BLEED, TRIM[1] + 2 * BLEED), bleed_mm=BLEED,
               title=f"ParkingYou partnerprogramma {vals['locatie']}")
    render.png(render.crop_svg(gevuld, BLEED, BLEED, *TRIM), os.path.join(uit, naam + "-mail.png"), 1240)
    open(os.path.join(uit, naam + ".svg"), "w", encoding="utf-8").write(gevuld)
    return uit, info


if __name__ == "__main__":
    codes = sys.argv[1:] or list(data.locaties())
    for c in codes:
        uit, info = bouw(c)
        print(c, "->", os.path.relpath(uit), [(f["id"], round(f["pt"], 2), f["lines"]) for f in info["flow"]])
