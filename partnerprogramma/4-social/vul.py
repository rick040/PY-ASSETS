#!/usr/bin/env python3
"""Maakt per partner uit partners.csv zes posts (twee templates, drie formaten) als PNG.

    python3 -I partnerprogramma/4-social/vul.py [CODE ...]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from ppkit import data, render, template   # noqa: E402

FORMATEN = {"1080x1350": 1080, "1080x1080": 1080, "1200x627": 1200}   # instagram feed staand, vierkant, linkedin
TEMPLATES = ("partner", "parkingyou")


def bouw(partner, uit=None):
    uit = uit or os.path.join(HERE, "export", partner["code"])
    vals = data.partner_values(partner)
    out = []
    for naam in TEMPLATES:
        for k, px in FORMATEN.items():
            svg = open(os.path.join(HERE, f"template-{naam}-{k}.svg"), encoding="utf-8").read()
            gevuld, info = template.process(svg, vals)
            for f in info["flow"]:
                if f["height"] > f["box_h"] + 1e-6:
                    raise ValueError(f"{partner['code']} {naam} {k}: tekstblok {f['id']} past niet")
            p = os.path.join(uit, f"parkingyou-social-{naam}-{k}-{partner['code']}.png")
            render.png(gevuld, p, px)
            out.append(p)
    return out


if __name__ == "__main__":
    codes = sys.argv[1:]
    for p in data.partners():
        if not codes or p["code"] in codes:
            files = bouw(p)
            print(p["code"], len(files), "posts")
