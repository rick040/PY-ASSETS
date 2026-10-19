"""SVG naar PDF (met trim- en bleedbox) en PNG (bijgesneden op de trim)."""
import io
import os
import re
import cairosvg
import pymupdf as fitz

MM = 72 / 25.4


def _root_attrs(svg, w_mm, h_mm, vb):
    svg = re.sub(r'(<svg\b[^>]*?)\swidth="[^"]*"', r"\1", svg, count=1)
    svg = re.sub(r'(<svg\b[^>]*?)\sheight="[^"]*"', r"\1", svg, count=1)
    svg = re.sub(r'(<svg\b[^>]*?)\sviewBox="[^"]*"', r"\1", svg, count=1)
    return svg.replace("<svg", f'<svg width="{w_mm}mm" height="{h_mm}mm" viewBox="{vb}"', 1)


def crop_svg(svg, x, y, w, h):
    """Zelfde tekening, zichtbaar gebied x,y,w,h in mm (voor PNG zonder afloop)."""
    return _root_attrs(svg, w, h, f"{x} {y} {w} {h}")


def pdf(svg, out, page_mm, trim_mm=None, bleed_mm=3.0, title=""):
    """PDF met MediaBox = formaat plus afloop; TrimBox en BleedBox gezet. Tekst blijft tekst (fonts ingebed)."""
    os.makedirs(os.path.dirname(out), exist_ok=True)
    buf = cairosvg.svg2pdf(bytestring=svg.encode("utf-8"))
    with fitz.open(stream=buf, filetype="pdf") as doc:
        pg = doc[0]
        r = pg.rect  # cairo schrijft MediaBox = tekenformaat (mm in punten, afgerond)
        b = bleed_mm * MM
        pg.set_bleedbox(r)
        pg.set_trimbox(fitz.Rect(r.x0 + b, r.y0 + b, r.x1 - b, r.y1 - b))
        doc.set_metadata({"title": title, "author": "ParkingYou", "producer": "py-assets partnerprogramma"})
        doc.save(out, garbage=3, deflate=True)


def png(svg, out, width_px, transparent=False, bg="#FFFFFF"):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out, output_width=width_px,
                     background_color=None if transparent else bg)


def pdf_fonts(path):
    with fitz.open(path) as doc:
        return sorted({f[3] for f in doc[0].get_fonts()})
