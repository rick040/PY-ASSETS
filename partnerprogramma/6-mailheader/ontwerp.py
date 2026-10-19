#!/usr/bin/env python3
"""Mailheader 600 px breed voor de welkomstmail en het maandoverzicht: verloop met de partnerbadge (donker, liggend).
Geen variabelen; één bestand. Schrijft template.svg."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PP = os.path.dirname(HERE)
sys.path.insert(0, PP)
from ppkit import brand as b, load            # noqa: E402
from ppkit.doc import Doc                      # noqa: E402

badge = load(os.path.join(PP, "3-partnerlogo", "ontwerp.py"), "ontwerp_partnerlogo")
W, H = 600, 140
d = Doc(W, H, "ParkingYou mailheader partner", bleed=0, unit="px", defs=b.verloop_defs("verloop", "horiz"))
d.rect(0, 0, W, H, "url(#verloop)", extra='id="achtergrond"')
d.atom("py-atom-logo-beeldmerk-watermark", W - 190, -40, h=250)
bw, bh, inner = badge.liggend("donker")
sc = 300 / bw
d.add(f'<g id="partnerlogo" transform="translate(32 {(H - bh * sc) / 2:.2f}) scale({sc:.5f})">{inner}</g>')
open(os.path.join(HERE, "template.svg"), "w", encoding="utf-8").write(d.svg())
print("template.svg geschreven")
