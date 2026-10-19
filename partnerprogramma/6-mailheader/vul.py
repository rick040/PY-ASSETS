#!/usr/bin/env python3
"""Mailheader: PNG op 600 px (1x) en 1200 px (2x, retina). Gebruik width="600" in de mail.

    python3 -I partnerprogramma/6-mailheader/vul.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from ppkit import render   # noqa: E402

svg = open(os.path.join(HERE, "template.svg"), encoding="utf-8").read()
for px, suffix in ((600, ""), (1200, "@2x")):
    render.png(svg, os.path.join(HERE, "export", f"parkingyou-mailheader-partner{suffix}.png"), px)
open(os.path.join(HERE, "export", "parkingyou-mailheader-partner.svg"), "w", encoding="utf-8").write(svg)
print("mailheader 600 en 1200 px")
