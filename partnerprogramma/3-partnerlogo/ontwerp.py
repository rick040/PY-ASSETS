#!/usr/bin/env python3
"""Badge "Parkeerpartner van ParkingYou": liggend en staand, licht en donker. Schrijft de vier bron-SVG's naar export/.

licht = voor lichte achtergronden (blauwe omlijning, logo in kleur). donker = voor donkere achtergronden (witte omlijning, logo omgekeerd).
Tekst staat als lijnwerk in de SVG, zodat partners Ubuntu niet hoeven te installeren. Achtergrond is transparant.
Alle maten in mm in de viewBox; de SVG heeft ook pixelmaten (4 px per mm) voor gebruik op een website.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from ppkit import brand as b          # noqa: E402

LABEL = "Parkeerpartner van"
LABEL_MM = 3.6           # lettergrootte van het label
STROKE = 0.6
RADIUS_RATIO = 0.22      # hoekradius op hoogte, zoals de partnerbadge in print (docs/print-rules.md, regel 10)
PAD = 5.0
VARIANTEN = {
    "licht": dict(lijn=b.BLAUW, tekst=b.BLAUW, logo="color"),
    "donker": dict(lijn=b.WIT, tekst=b.WIT, logo="reverse"),
}


def liggend(v):
    s = VARIANTEN[v]
    logo = f"py-atom-logo-horizontal-{s['logo']}"
    _, lw, lh = b.atom_info(logo)
    h_logo = 8.0
    sc = h_logo / lh
    label_w = b.text_width(LABEL, "medium", LABEL_MM)
    H = 16.0
    W = PAD + label_w + PAD + STROKE + PAD + lw * sc + PAD
    parts = [f'<rect x="{STROKE / 2}" y="{STROKE / 2}" width="{W - STROKE:.3f}" height="{H - STROKE}" rx="{H * RADIUS_RATIO:.3f}" fill="none" stroke="{s["lijn"]}" stroke-width="{STROKE}"/>']
    path, _ = b.text_outline(LABEL, "medium", LABEL_MM, PAD, H / 2 + LABEL_MM * 0.35, s["tekst"])
    parts.append(path)
    dx = PAD + label_w + PAD
    parts.append(f'<rect x="{dx:.3f}" y="{H * 0.28:.3f}" width="{STROKE / 2}" height="{H * 0.44:.3f}" fill="{s["lijn"]}" fill-opacity="0.5"/>')
    g, _, _ = b.atom(logo, dx + STROKE + PAD, (H - lh * sc) / 2, scale=sc)
    parts.append(g)
    return W, H, "".join(parts)


def staand(v):
    s = VARIANTEN[v]
    logo = f"py-atom-logo-stacked-{s['logo']}"
    _, lw, lh = b.atom_info(logo)
    label_w = b.text_width(LABEL, "medium", LABEL_MM)
    w_logo = 29.0
    sc = w_logo / lw
    W = max(label_w, w_logo) + 2 * PAD + 2
    H = PAD + LABEL_MM + 5.0 + lh * sc + PAD
    parts = [f'<rect x="{STROKE / 2}" y="{STROKE / 2}" width="{W - STROKE:.3f}" height="{H - STROKE:.3f}" rx="{min(W, H) * RADIUS_RATIO * 0.55:.3f}" fill="none" stroke="{s["lijn"]}" stroke-width="{STROKE}"/>']
    path, _ = b.text_outline(LABEL, "medium", LABEL_MM, W / 2, PAD + LABEL_MM * 0.8, s["tekst"], anchor="middle")
    parts.append(path)
    g, _, _ = b.atom(logo, (W - w_logo) / 2, PAD + LABEL_MM + 5.0, scale=sc)
    parts.append(g)
    return W, H, "".join(parts)


def svg(W, H, inner, title):
    px = 4
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W * px:.0f}" height="{H * px:.0f}" viewBox="0 0 {W:.3f} {H:.3f}" role="img" aria-label="Parkeerpartner van ParkingYou">'
            f'<title>{title}</title>{inner}</svg>\n')


def alle():
    for vorm, fn in (("liggend", liggend), ("staand", staand)):
        for v in VARIANTEN:
            W, H, inner = fn(v)
            yield vorm, v, W, H, svg(W, H, inner, f"Parkeerpartner van ParkingYou, {vorm}, {v}")


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "export"), exist_ok=True)
    for vorm, v, W, H, s in alle():
        p = os.path.join(HERE, "export", f"parkingyou-partnerlogo-{vorm}-{v}.svg")
        open(p, "w", encoding="utf-8").write(s)
        print(os.path.relpath(p, HERE), f"{W:.1f} x {H:.1f} mm")
