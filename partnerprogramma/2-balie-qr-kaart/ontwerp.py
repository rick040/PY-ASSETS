#!/usr/bin/env python3
"""Schrijft template-a6.svg en template-tafelstandaard.svg. Teksten letterlijk uit de brief; {velden} per partner."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from ppkit import brand as b          # noqa: E402
from ppkit.doc import Doc             # noqa: E402

W, H = 105, 148      # A6 staand
M = 9
tb = lambda s, c=None: f'<tspan font-weight="bold"{f" fill=\"{c}\"" if c else ""}>{s}</tspan>'


def kaart(d, oy=0, id_pre="kaart"):
    """Eén A6-vlak met linksboven (0, oy). Zonder achtergrond."""
    d.atom("py-atom-logo-beeldmerk-watermark", 52, oy + 22, h=118)
    d.atom("py-atom-logo-horizontal-reverse", M, oy + 11, w=38)
    d.flow(M, oy + 31, W - 2 * M, 24, 26, 20, 1.08,
           'Met de auto?<br/>' + tb("Wij weten een plek.", b.AQUA), face="bold", fill=b.WIT, id=f"{id_pre}-kop")
    d.flow(M, oy + 58, W - 2 * M, 22, 12, 10, 1.3,
           'Reserveer vooraf in parkeergarage ' + tb("ParkingYou {locatie}") + ', op\u00a0' + tb("{afstand}") + '\u00a0lopen.',
           fill=b.WIT, id=f"{id_pre}-tekst")
    # QR: code 30 mm (minimaal 25), rustzone 4 modules, witte plaat; gecentreerd op x 52,5
    d.add(f'<rect x="0" y="0" width="30" height="30" fill="{b.BLAUW}" data-qr="https://{{link}}" data-qr-plate="{b.WIT}" '
          f'data-qr-center="{W / 2} {oy + 100}"/>')
    d.text(W / 2, oy + 128.5, "Scan en reserveer", "bold", 13, b.WIT, anchor="middle")
    d.text(W / 2, oy + 141, "parkingyou.nl · Parkeerpartner van ParkingYou", "regular", 7.5, b.AQUA, anchor="middle")


# --- A6 ------------------------------------------------------------------------------
d = Doc(W, H, "ParkingYou balie- en QR-kaart A6, {code}")
d.rect(-3, -3, W + 6, H + 6, b.BLAUW, extra='id="achtergrond"')
kaart(d)
open(os.path.join(HERE, "template-a6.svg"), "w", encoding="utf-8").write(d.svg())

# --- tafelstandaard: vel 105 x 296, vouw op 148; de bovenste helft staat op zijn kop zodat beide kanten rechtop staan ------
d = Doc(W, 2 * H, "ParkingYou tafelstandaard A6, {code}")
d.rect(-3, -3, W + 6, 2 * H + 6, b.BLAUW, extra='id="achtergrond"')
sub = Doc(W, H, "")
kaart(sub, 0, "voorkant")
d.add(f'<g id="voorkant" transform="translate(0 {H})">{"".join(sub.parts)}</g>')
sub = Doc(W, H, "")
kaart(sub, 0, "achterkant")
d.add(f'<g id="achterkant" transform="rotate(180 {W / 2} {H / 2})">{"".join(sub.parts)}</g>')
# vouwmerken in de afloop (valt weg bij het snijden)
for x1, x2 in ((-3, -0.8), (W + 0.8, W + 3)):
    d.line(x1, H, x2, H, b.GRIJS, 0.25)
d.add('<g id="vouwlijn" data-note="vouw op 148 mm; merken staan in de afloop"/>')
open(os.path.join(HERE, "template-tafelstandaard.svg"), "w", encoding="utf-8").write(d.svg())
print("templates geschreven")
