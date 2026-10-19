"""QR-codes: tekenen als vectorpad en na export terug lezen.

Foutcorrectie Q (25 procent), boven de gevraagde M. Rustzone 4 modules (de QR-norm) rondom, op een witte plaat.
Donkere modules op een lichte plaat, niet omgekeerd: omgekeerde codes (zoals op de Maashaven-pyloon) falen op oudere scanners.
"""
import io
import segno
from . import brand

QUIET = 4          # modules rustzone
ERROR = "q"        # l < m < q < h


def matrix(url, error=ERROR):
    q = segno.make(url, error=error, boost_error=False, micro=False)
    rows = [list(r) for r in q.matrix]
    return rows, q.version, q.error


def draw(url, x, y, code_mm, fill=brand.BLAUW, plate=brand.WIT, radius_ratio=0.10, error=ERROR):
    """QR met plaat. x, y, code_mm = de code zelf (zonder rustzone). Geeft (svg, info)."""
    rows, version, err = matrix(url, error)
    n = len(rows)
    mod = code_mm / n
    pad = QUIET * mod
    side = code_mm + 2 * pad
    d = []
    for r, row in enumerate(rows):
        c = 0
        while c < n:
            if row[c]:
                c0 = c
                while c < n and row[c]:
                    c += 1
                # 0.02 module overlap tegen haarlijnen tussen rijen
                d.append(f"M{x + c0 * mod:.4f} {y + r * mod - 0.01 * mod:.4f}h{(c - c0) * mod:.4f}v{mod * 1.02:.4f}h-{(c - c0) * mod:.4f}z")
            else:
                c += 1
    rr = side * radius_ratio
    svg = (f'<g data-qr="{brand.esc(url)}">'
           f'<rect x="{x - pad:.4f}" y="{y - pad:.4f}" width="{side:.4f}" height="{side:.4f}" rx="{rr:.3f}" fill="{plate}"/>'
           f'<path d="{"".join(d)}" fill="{fill}"/></g>')
    info = dict(url=url, version=version, error=err, modules=n, module_mm=mod, code_mm=code_mm, plate_mm=side, quiet_mm=pad)
    return svg, info


def decode_image(img):
    """img: PIL.Image. Geeft lijst gelezen teksten (zxing-cpp)."""
    import numpy as np
    import zxingcpp
    res = zxingcpp.read_barcodes(np.array(img.convert("RGB")))
    return [r.text for r in res if r.format.name == "QRCode"]


def decode_pdf(path, dpi=300):
    import pymupdf as fitz
    from PIL import Image
    out = []
    with fitz.open(path) as doc:
        for page in doc:
            pm = page.get_pixmap(dpi=dpi)
            img = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
            out.append(decode_image(img))
    return out
