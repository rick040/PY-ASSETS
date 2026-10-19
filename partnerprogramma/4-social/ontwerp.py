#!/usr/bin/env python3
"""Schrijft zes templates: twee posts (voor de partner, voor ParkingYou) in drie formaten. Teksten letterlijk uit de brief.

Het partnerlogo in de partnerpost is de badge uit 3-partnerlogo (donker, liggend).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PP = os.path.dirname(HERE)
sys.path.insert(0, PP)
from ppkit import brand as b, load            # noqa: E402
from ppkit.doc import Doc                      # noqa: E402

badge = load(os.path.join(PP, "3-partnerlogo", "ontwerp.py"), "ontwerp_partnerlogo")
tb = lambda s, c=None: f'<tspan font-weight="bold"{f" fill=\"{c}\"" if c else ""}>{s}</tspan>'

# formaat: marge, kop-box (y, h, max, min), antwoord-box (y, h, max, min), breedte tekst, badge-breedte, logo-breedte
F = {
    "1080x1350": dict(W=1080, H=1350, m=90, tw=900, kop=(150, 520, 128, 70), tekst=(730, 300, 66, 42), badge=720, logo=400, wm=1180),
    "1080x1080": dict(W=1080, H=1080, m=80, tw=920, kop=(100, 400, 118, 64), tekst=(530, 260, 60, 40), badge=620, logo=360, wm=980),
    "1200x627": dict(W=1200, H=627, m=60, tw=760, kop=(40, 250, 70, 40), tekst=(320, 120, 34, 26), badge=430, logo=270, wm=640),
}


def badge_svg(x, y, w):
    W, H, inner = badge.liggend("donker")
    return f'<g data-element="partnerlogo-liggend-donker" transform="translate({x} {y}) scale({w / W:.5f})">{inner}</g>', H * w / W


def partnerpost(k, f):
    W, H, m = f["W"], f["H"], f["m"]
    d = Doc(W, H, f"ParkingYou social, voor de partner, {k}", bleed=0, unit="px")
    d.rect(0, 0, W, H, b.BLAUW, extra='id="achtergrond"')
    d.atom("py-atom-logo-beeldmerk-watermark", W - f["wm"] * 0.62, H - f["wm"] * 0.9, h=f["wm"])
    y, h, mx, mn = f["kop"]
    d.flow(m, y, f["tw"], h, mx, mn, 1.06, 'Met de auto naar ' + tb("{bedrijf}", b.AQUA) + '?', face="bold", fill=b.WIT,
           id="kop", valign="bottom", units=True)
    y, h, mx, mn = f["tekst"]
    d.flow(m, y, f["tw"], h, mx, mn, 1.22, 'Reserveer vooraf je plek bij ' + tb("ParkingYou {locatie}") + '.', fill=b.WIT,
           id="tekst", units=True)
    g, bh = badge_svg(m, H - m - 0.195 * f["badge"], f["badge"])
    d.add(f'<g id="partnerlogo-ruimte">{g}</g>')
    return d


def ypost(k, f):
    W, H, m = f["W"], f["H"], f["m"]
    d = Doc(W, H, f"ParkingYou social, voor ParkingYou, {k}", bleed=0, unit="px")
    d.rect(0, 0, W, H, b.WIT, extra='id="achtergrond"')
    d.atom("py-atom-logo-beeldmerk-watermark", W - f["wm"] * 0.62, H - f["wm"] * 0.9, h=f["wm"], recolor={b.AQUA: b.BLAUW})
    d.atom("py-atom-logo-horizontal-color", m, m, w=f["logo"])
    y, h, mx, mn = f["kop"]
    y += f["logo"] * 0.3 if k != "1200x627" else 70
    h -= f["logo"] * 0.3 if k != "1200x627" else 70
    d.flow(m, y, f["tw"], h, mx, mn, 1.06, 'Welkom, ' + '{bedrijf}!', face="bold", fill=b.BLAUW, id="kop", valign="bottom", units=True)
    y, h, mx, mn = f["tekst"]
    d.flow(m, y, f["tw"], h, mx, mn, 1.22, 'Gasten van ' + tb("{bedrijf}") + ' reserveren nu vooraf een plek in onze garage ' + tb("{locatie}") + '.',
           fill=b.BLAUW, id="tekst", units=True)
    fh = {"1080x1350": 420, "1080x1080": 330, "1200x627": 280}[k]
    fx = {"1080x1350": 700, "1080x1080": 720, "1200x627": 960}[k]
    fy = {"1080x1350": H - m - fh + 30, "1080x1080": H - m - fh + 20, "1200x627": H - m - fh + 10}[k]
    d.atom("py-atom-figure-wave", fx, fy, h=fh)
    return d


if __name__ == "__main__":
    for k, f in F.items():
        for naam, fn in (("partner", partnerpost), ("parkingyou", ypost)):
            p = os.path.join(HERE, f"template-{naam}-{k}.svg")
            open(p, "w", encoding="utf-8").write(fn(k, f).svg())
    print("6 templates geschreven")
