#!/usr/bin/env python3
"""Bouwt alle visuals van het partnerprogramma. Eén commando:

    python3 -I partnerprogramma/build.py                       alles, alle locaties en partners
    python3 -I partnerprogramma/build.py --locatie HOF         one-pager en alle partners van Hofplein
    python3 -I partnerprogramma/build.py --partner HOF-HOTELVB kaarten en posts van een partner
    python3 -I partnerprogramma/build.py --only kaart,social   alleen deze visuals (onepager, kaart, partnerlogo, social, landingspagina, mailheader)

Daarna draait test.py (QR-codes terug lezen, PDF-boxen, transparantie, streepjes, placeholders); uitzetten kan met --geen-test.
Vereist Python 3 met pymupdf, cairosvg, fonttools, segno, zxing-cpp, opencv-python-headless, Pillow, numpy en de Ubuntu-fonts uit fonts/ (zie README.md).
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ppkit import data   # noqa: E402

MAPPEN = {"onepager": "1-onepager", "kaart": "2-balie-qr-kaart", "partnerlogo": "3-partnerlogo",
          "social": "4-social", "landingspagina": "5-landingspagina", "mailheader": "6-mailheader"}
PER_LOCATIE = {"onepager"}
PER_PARTNER = {"kaart", "social"}


def run(naam, args):
    script = os.path.join(HERE, MAPPEN[naam], "vul.py")
    print(f"== {naam}", " ".join(args))
    r = subprocess.run([sys.executable, "-I", script, *args], cwd=HERE)
    if r.returncode:
        sys.exit(f"{naam} mislukt")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--locatie", action="append", help="HOF of PLA (mag vaker)")
    ap.add_argument("--partner", action="append", help="partnercode (mag vaker)")
    ap.add_argument("--only", help="komma-gescheiden lijst visuals")
    ap.add_argument("--geen-test", action="store_true")
    a = ap.parse_args()

    locs = a.locatie or list(data.locaties())
    partners = [p for p in data.partners() if (not a.partner or p["code"] in a.partner) and (not a.locatie or p["locatie"] in a.locatie)]
    if a.partner and len(partners) != len(set(a.partner)):
        sys.exit("onbekende partnercode: " + ", ".join(set(a.partner) - {p["code"] for p in partners}))
    keuze = a.only.split(",") if a.only else list(MAPPEN)
    for k in keuze:
        if k not in MAPPEN:
            sys.exit(f"onbekende visual {k!r}; kies uit {', '.join(MAPPEN)}")
    # met --partner alleen de visuals die per partner zijn, tenzij --only iets anders zegt
    if a.partner and not a.only:
        keuze = [k for k in keuze if k in PER_PARTNER]
    for k in keuze:
        if k in PER_LOCATIE:
            run(k, locs)
        elif k in PER_PARTNER:
            run(k, [p["code"] for p in partners])
        else:
            run(k, [])
    if not a.geen_test:
        r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "test.py")], cwd=HERE)
        sys.exit(r.returncode)


if __name__ == "__main__":
    main()
