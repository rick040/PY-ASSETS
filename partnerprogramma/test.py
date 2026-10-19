#!/usr/bin/env python3
"""Controleert de exports. Schrijft 2-balie-qr-kaart/qr-test-rapport.md. Exitcode 1 bij een fout.

    python3 -I partnerprogramma/test.py
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np                       # noqa: E402
import cv2                               # noqa: E402
import pymupdf                           # noqa: E402
import zxingcpp                          # noqa: E402
from PIL import Image                    # noqa: E402
from ppkit import data, qr               # noqa: E402

fouten, ok = [], 0


def check(cond, msg):
    global ok
    if cond:
        ok += 1
    else:
        fouten.append(msg)
        print("FOUT", msg)


def mm(v):
    return round(v / 72 * 25.4, 1)


def raster(pdf, dpi):
    pm = pymupdf.open(pdf)[0].get_pixmap(dpi=dpi)
    return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)


def lees_zxing(img):
    return [r.text for r in zxingcpp.read_barcodes(np.array(img)) if r.format.name == "QRCode"]


def lees_cv(img):
    """OpenCV leest twee codes in een beeld onbetrouwbaar; een tafelstandaard lezen we daarom per kant (zoals een telefoon)."""
    delen = [img] if img.height < 1.5 * img.width else [img.crop((0, 0, img.width, img.height // 2)), img.crop((0, img.height // 2, img.width, img.height))]
    out = []
    for d in delen:
        t, _, _ = cv2.QRCodeDetector().detectAndDecode(cv2.cvtColor(np.array(d), cv2.COLOR_RGB2BGR))
        if t:
            out.append(t)
    return out


# --- afstand ------------------------------------------------------------------------------------------------------------
for m, verwacht in ((1, "1 minuut"), (80, "1 minuut"), (81, "2 minuten"), (160, "2 minuten"), (220, "3 minuten"), (241, "4 minuten")):
    check(data.afstand_tekst(m).replace(" ", " ") == verwacht, f"afstand {m} m -> {data.afstand_tekst(m)!r}, verwacht {verwacht!r}")

# --- kaarten: QR terug lezen met twee decoders op drie resoluties ----------------------------------------------------------
rapport = ["# QR-test", "", "Na elke export worden de PDF's gerasterd (300, 150 en 100 dpi) en de codes teruggelezen met twee onafhankelijke decoders (zxing-cpp en OpenCV).",
           "Een kaart slaagt als op elke resolutie het verwachte aantal codes gelezen wordt en elke code precies de verwachte URL is.", "",
           "| PDF | Verwacht | Codes | Module | Code | Rustzone | Resultaat |", "|---|---|---|---|---|---|---|"]
for p in data.partners():
    verwacht = "https://" + p["link"]
    for naam, n in (("kaart-a6", 1), ("tafelstandaard-a6", 2)):
        pdf = os.path.join(HERE, "2-balie-qr-kaart", "export", p["code"], f"parkingyou-{naam}-{p['code']}.pdf")
        if not os.path.exists(pdf):
            check(False, f"ontbreekt: {pdf}")
            continue
        slaagt = True
        for dpi in (300, 150, 100):
            img = raster(pdf, dpi)
            for decoder, fn in (("zxing", lees_zxing), ("opencv", lees_cv)):
                gelezen = fn(img)
                goed = len(gelezen) == n and all(t == verwacht for t in gelezen)
                if not goed:
                    slaagt = False
                    fouten.append(f"QR {os.path.basename(pdf)} {decoder} {dpi} dpi: {gelezen}")
                    print("FOUT QR", os.path.basename(pdf), decoder, dpi, gelezen)
        from ppkit.qr import matrix
        rows, v, e = matrix(verwacht)
        nmod = len(rows)
        code_mm = 30.0
        rapport.append(f"| {os.path.relpath(pdf, HERE)} | {verwacht} | {n} | {nmod}x{nmod} (v{v}, {e}) | {code_mm:.0f} mm | {4 * code_mm / nmod:.1f} mm | {'gelezen' if slaagt else 'MISLUKT'} |")
        ok += slaagt
open(os.path.join(HERE, "2-balie-qr-kaart", "qr-test-rapport.md"), "w", encoding="utf-8").write("\n".join(rapport) + "\n")

# --- PDF's: formaat, trim, bleed, fonts ingebed ---------------------------------------------------------------------------
verwacht = {"onepager": (216, 303, 210, 297), "kaart-a6": (111, 154, 105, 148), "tafelstandaard-a6": (111, 302, 105, 296)}
for pdf in glob.glob(os.path.join(HERE, "*", "export", "**", "*.pdf"), recursive=True):
    sleutel = next((k for k in verwacht if k in os.path.basename(pdf)), None)
    if not sleutel:
        continue
    pg = pymupdf.open(pdf)[0]
    W, H, tw, th = verwacht[sleutel]
    got = (mm(pg.mediabox.width), mm(pg.mediabox.height), mm(pg.trimbox.width), mm(pg.trimbox.height))
    check(tuple(round(v) for v in got) == (W, H, tw, th), f"{os.path.basename(pdf)}: formaat {got}, verwacht {(W, H, tw, th)}")
    check(mm(pg.trimbox.x0) == 3.0 and mm(pg.trimbox.y0) == 3.0, f"{os.path.basename(pdf)}: trim niet op 3 mm afloop")
    fonts = {f[3].split("+")[-1] for f in pg.get_fonts()}
    check(fonts and all(f.startswith("Ubuntu") for f in fonts), f"{os.path.basename(pdf)}: fonts {fonts}")

# --- one-pager: placeholders zichtbaar zolang de bron leeg is ----------------------------------------------------------------
loc = data.locaties()
for code, l in loc.items():
    svg = open(os.path.join(HERE, "1-onepager", "export", code, f"parkingyou-partnerprogramma-onepager-{code}.svg"), encoding="utf-8").read()
    tekst = re.sub(r"<[^>]+>", "", svg)
    check(l["locatie"] in tekst, f"onepager {code}: locatienaam ontbreekt")
    if l["gemiddelde_boeking_eur"] is None:
        check("[bedrag]" in tekst and "[uitkomst]" in tekst, f"onepager {code}: placeholders [bedrag]/[uitkomst] niet zichtbaar")
    check(not re.search(r"\{[a-z_]+\}", tekst), f"onepager {code}: onvervuld veld")
    check(os.path.exists(os.path.join(HERE, "1-onepager", "export", code, f"parkingyou-partnerprogramma-onepager-{code}-mail.png")), f"onepager {code}: png ontbreekt")

# --- badge: transparant, drie hoeken doorzichtig ----------------------------------------------------------------------------
for png in glob.glob(os.path.join(HERE, "3-partnerlogo", "export", "*.png")):
    im = Image.open(png)
    check(im.mode == "RGBA" and im.getpixel((0, 0))[3] == 0 and im.getpixel((im.width - 1, im.height - 1))[3] == 0, f"{os.path.basename(png)}: niet transparant")

# --- social en mailheader: exacte pixelmaten ------------------------------------------------------------------------------------
for png in glob.glob(os.path.join(HERE, "4-social", "export", "*", "*.png")):
    m = re.search(r"(\d+)x(\d+)", os.path.basename(png))
    check(Image.open(png).size == (int(m[1]), int(m[2])), f"{os.path.basename(png)}: formaat {Image.open(png).size}")
for n, w in (("parkingyou-mailheader-partner.png", 600), ("parkingyou-mailheader-partner@2x.png", 1200)):
    p = os.path.join(HERE, "6-mailheader", "export", n)
    check(os.path.exists(p) and Image.open(p).width == w, f"{n}: breedte")

# --- geen em- of en-streepjes in tekst die wij schrijven -----------------------------------------------------------------------
for pad in glob.glob(os.path.join(HERE, "**", "*"), recursive=True):
    if os.path.isfile(pad) and pad.endswith((".svg", ".md", ".json", ".csv", ".html", ".js", ".css")) and "/export/assets/" not in pad:
        t = open(pad, encoding="utf-8").read()
        tekst = re.sub(r"<[^>]+>", "", t) if pad.endswith(".svg") else t
        if pad.endswith("vul.py") or pad.endswith("test.py"):
            continue
        check("—" not in tekst and "–" not in tekst, f"gedachtestreepje in {os.path.relpath(pad, HERE)}")

print(f"\n{ok} controles geslaagd, {len(fouten)} fouten")
sys.exit(1 if fouten else 0)
