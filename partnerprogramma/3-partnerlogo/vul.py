#!/usr/bin/env python3
"""Partnerlogo: bron-SVG's uit ontwerp.py, transparante PNG's, overzicht en formaatregel.

    python3 -I partnerprogramma/3-partnerlogo/vul.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import ontwerp                          # noqa: E402
from ppkit import brand as b, render   # noqa: E402
import cairosvg                         # noqa: E402

PNG_BREEDTE = {"liggend": (600, 1800), "staand": (400, 1200)}
MIN_LABEL_PT_PRINT = 5.0    # kleinste leesbare lettergrootte van het label in druk
MIN_LABEL_PX_SCHERM = 8.0   # en op scherm


def main():
    uit = os.path.join(HERE, "export")
    os.makedirs(uit, exist_ok=True)
    maten = {}
    for vorm, v, W, H, s in ontwerp.alle():
        base = f"parkingyou-partnerlogo-{vorm}-{v}"
        open(os.path.join(uit, base + ".svg"), "w", encoding="utf-8").write(s)
        for px in PNG_BREEDTE[vorm]:
            render.png(s, os.path.join(uit, f"{base}-{px}px.png"), px, transparent=True)
        maten[vorm] = (W, H)

    # formaatregel: het label (3,6 mm op een badge van H mm hoog) moet leesbaar blijven
    regels = []
    for vorm, (W, H) in maten.items():
        label_deel = ontwerp.LABEL_MM / W          # lettergrootte als deel van de breedte
        mm = MIN_LABEL_PT_PRINT * b.PT / label_deel
        px = MIN_LABEL_PX_SCHERM / label_deel
        regels.append((vorm, round(mm / 5) * 5 or 5, int(-(-px // 10) * 10), W, H))
    md = ["# Partnerlogo: formaatregel", "",
          "Twee varianten, twee achtergronden. `licht` is voor lichte achtergronden (blauwe omlijning, logo in kleur), `donker` voor donkere achtergronden, zoals PY-Blauw (witte omlijning, logo omgekeerd). Achtergrond van de bestanden is transparant.",
          "", "| | Kleinste breedte in druk | Kleinste breedte op scherm | Verhouding |", "|---|---|---|---|"]
    for vorm, mm, px, W, H in regels:
        md.append(f"| {vorm.capitalize()} | {mm} mm | {px} px | {W:.0f} : {H:.0f} |")
    md += ["", "Kleiner dan dit wordt het label \"Parkeerpartner van\" onleesbaar. Daaronder: gebruik het logo niet.", "",
           f"Vrije ruimte: rondom minimaal een kwart van de hoogte van de badge, geen tekst of beeld in die rand.", "",
           "Niet doen: uitrekken, kleuren veranderen, de omlijning weghalen, de badge op een drukke foto zetten, het label of het logo los gebruiken.", "",
           f"Bestanden in `export/`: SVG (schaalbaar, tekst als lijnwerk) en PNG met transparante achtergrond in {', '.join(f'{vorm} {px[0]} en {px[1]} px breed' for vorm, px in PNG_BREEDTE.items())}.",
           "De drempels zijn berekend uit het ontwerp (label 5 pt in druk, 8 px op scherm) en niet uit het huisstijlhandboek; het handboek heeft geen regel voor dit label."]
    open(os.path.join(HERE, "formaatregel.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")

    # overzicht: alle vier op wit en op navy (controle, geen deliverable voor partners)
    parts = []
    for r, (bg, vs) in enumerate(((b.WIT, "licht"), (b.BLAUW, "donker"))):
        x = 8
        for vorm in ("liggend", "staand"):
            W, H = maten[vorm]
            s = open(os.path.join(uit, f"parkingyou-partnerlogo-{vorm}-{vs}.svg"), encoding="utf-8").read()
            inner = s[s.index("</title>") + 8:s.rindex("</svg>")]
            parts.append(f'<g transform="translate({x} {r * 56 + (56 - H) / 2})">{inner}</g>')
            x += W + 12
    sheet = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="{1400 * 112 // 160}" viewBox="0 0 160 112">'
             f'<rect width="160" height="56" fill="{b.WIT}"/><rect y="56" width="160" height="56" fill="{b.BLAUW}"/>' + "".join(parts) + "</svg>")
    cairosvg.svg2png(bytestring=sheet.encode(), write_to=os.path.join(HERE, "overzicht.png"))
    print("klaar:", ", ".join(f"{v} {W:.0f}x{H:.0f} mm" for v, (W, H) in maten.items()))


if __name__ == "__main__":
    main()
