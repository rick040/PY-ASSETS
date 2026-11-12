#!/usr/bin/env python3
"""Build the short brand guideline PDF (brand-2027/03-guide/kort/).

1. Copies the figures the guide uses from 02-build into 03-guide/kort/img/ as 1800 px JPEG (not committed).
2. Renders guide.html to ParkingYou-huisstijl-2027-kort.pdf with Playwright (tools/render_pdf.mjs).
Run: python3 -I brand-2027/tools/build_short_guide.py
"""
import os
import subprocess

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
B = os.path.join(ROOT, "02-build")
OUT = os.path.join(ROOT, "03-guide", "kort")
FIGS = {
    "principles": "00-intro/figures/principles.png",
    "identity-elements": "00-core/figures/identity-elements.png",
    "bubble-anatomy": "00-core/figures/bubble-anatomy.png",
    "lockups": "01-logo/figures/lockups.png",
    "versions-grounds": "01-logo/figures/versions-grounds.png",
    "palette-roles": "02-kleur/figures/palette-roles.png",
    "de-stem": "03-typografie/figures/de-stem.png",
    "layoutpatronen": "04-grid/figures/layoutpatronen.png",
    "parkeerders-cast": "05-patronen/figures/parkeerders-cast.png",
    "stem": "05-patronen/figures/stem.png",
    "vak": "05-patronen/figures/vak.png",
    "pijl-constructie": "06-iconografie/figures/pijl-constructie.png",
    "style-board": "08-fotografie/figures/style-board.png",
    "screens-key": "09-ui/figures/screens-key.png",
    "key-entrance-sign": "11-toepassingen/figures/key-entrance-sign.png",
    "key-social-post": "11-toepassingen/figures/key-social-post.png",
    "key-subscription-card": "11-toepassingen/figures/key-subscription-card.png",
    "key-business-card": "10-stationery/figures/key-business-card.png",
}


def main():
    img = os.path.join(OUT, "img")
    os.makedirs(img, exist_ok=True)
    for name, rel in FIGS.items():
        im = Image.open(os.path.join(B, rel)).convert("RGB")
        im.thumbnail((1800, 1800))
        im.save(os.path.join(img, name + ".jpg"), quality=86, optimize=True)
    pdf = os.path.join(OUT, "ParkingYou-huisstijl-2027-kort.pdf")
    subprocess.run(["node", os.path.join(ROOT, "tools", "render_pdf.mjs"), os.path.join(OUT, "guide.html"), pdf], check=True)
    print("pdf:", pdf, os.path.getsize(pdf) // 1024, "kB")


if __name__ == "__main__":
    main()
