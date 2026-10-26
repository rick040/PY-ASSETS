"""The eleven print source PDFs (source/print/) with their production data, plus the reference reproduction builder.

Coordinates in the source are PDF points from the top left of the MediaBox (PyMuPDF convention); 1 pt = 25.4/72 mm.
`trim_off` is where the trim corner sits inside the page (mm); `bleed_set` says whether the PDF defines a BleedBox.
"""
from __future__ import annotations

import os

from .core import (PT_MM, Defs, Element, Path, Source, TF, Text, clip_to_rect, fmt, regroup, _esc)
from .registry import crop

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DIR = os.path.join(ROOT, "source", "print")

# key -> production data (all measured from the PDFs, see docs/print-phase1-inventory.md)
SOURCES = {
    "uitrit": dict(file="15728501-1.pdf", pages=1, page_mm=(820, 270), trim_mm=(800, 250), trim_off=(10, 10), bleed_set=True, cs="CMYK (PDF/X-4, FOGRA39), spot ThruCut"),
    "evoluon": dict(file="EvoluonPasjes.pdf", pages=2, page_mm=(85, 55), trim_mm=(85, 55), trim_off=(0, 0), bleed_set=False, cs="CMYK"),
    "hofplein": dict(file="InfoPylonBordGoed.pdf", pages=1, page_mm=(600, 840), trim_mm=(600, 840), trim_off=(0, 0), bleed_set=False, cs="CMYK"),
    "laadkabel": dict(file="LaadKabel.pdf", pages=1, page_mm=(256, 306), trim_mm=(250, 300), trim_off=(3, 3), bleed_set=True, cs="CMYK"),
    "diefstal": dict(file="StickerDiefstalARtisDruk.pdf", pages=2, page_mm=(140, 280), trim_mm=(140, 280), trim_off=(0, 0), bleed_set=False, cs="CMYK"),
    "maashaven": dict(file="Maashaven.pdf", pages=1, page_mm=(406, 1006), trim_mm=(400, 1000), trim_off=(3, 3), bleed_set=True, cs="CMYK"),
    "glow1": dict(file="Tekengebied_1.pdf", pages=1, page_mm=(297, 420), trim_mm=(297, 420), trim_off=(0, 0), bleed_set=False, cs="CMYK"),
    "glow4": dict(file="Tekengebied_4_kopie_4.pdf", pages=1, page_mm=(297, 420), trim_mm=(297, 420), trim_off=(0, 0), bleed_set=False, cs="CMYK"),
    "tagline": dict(file="Naamloos-7.pdf", pages=1, page_mm=(148, 105), trim_mm=(148, 105), trim_off=(0, 0), bleed_set=False, cs="RGB (ICC, sRGB)"),
    "terminal": dict(file="TerminalStickers_September2026.pdf", pages=1, page_mm=(271.0, 391.0), trim_mm=(271.0, 391.0), trim_off=(0, 0), bleed_set=False, cs="CMYK"),
    "inleveren": dict(file="Inleveren_Abbonementborg_A5.pdf", pages=1, page_mm=(148, 105), trim_mm=(148, 105), trim_off=(0, 0), bleed_set=False, cs="CMYK"),
    # second batch (PM-137 follow-up)
    "slagboom": dict(file="BordSlagboomEVO.pdf", pages=1, page_mm=(480, 240), trim_mm=(480, 240), trim_off=(0, 0), bleed_set=False, cs="CMYK"),
    "briefpapier": dict(file="Briefpapier_nieuw.pdf", pages=1, page_mm=(210, 297), trim_mm=(210, 297), trim_off=(0, 0), bleed_set=False, cs="CMYK"),
    "pr": dict(file="PR_RoadSignage.pdf", pages=1, page_mm=(210, 297), trim_mm=(210, 297), trim_off=(0, 0), bleed_set=False, cs="RGB (ICC)"),
    "envelop": dict(file="ParkingYou_Envelop_220x156.pdf", pages=1, page_mm=(249.28, 185.28), trim_mm=(220, 156), trim_off=(14.64, 14.64), bleed_set=False, cs="RGB (ICC), file claims PDF/X-1a"),
    "tarief": dict(file="TariefConcerten.pdf", pages=1, page_mm=(700, 1000), trim_mm=(700, 1000), trim_off=(0, 0), bleed_set=False, cs="RGB (ICC)"),
    # third batch
    "dranghek": dict(file="dranghekspandoek-dubbelzijdig_01.pdf", pages=1, page_mm=(2440, 1570), trim_mm=(2420, 1550), trim_off=(10, 10), bleed_set=True, cs="CMYK"),
    "wtcsticker": dict(file="PR_WTC_Sticker.pdf", pages=1, page_mm=(700, 700), trim_mm=(700, 700), trim_off=(0, 0), bleed_set=False, cs="RGB (ICC)"),
    "wtcposter": dict(file="PR_WTC_Poster.pdf", pages=1, page_mm=(700, 1000), trim_mm=(700, 1000), trim_off=(0, 0), bleed_set=False, cs="RGB (ICC)"),
    "posterA3": dict(file="posters_297x420_3_1.pdf", pages=1, page_mm=(303, 426), trim_mm=(297, 420), trim_off=(3, 3), bleed_set=True, cs="RGB (ICC sRGB)"),
    # fourth batch: one A4 landscape slide with mock-ups of the partner package (poster, flyers, stickers); pieces are at about 0.358 scale
    "marketing": dict(file="MarketingCampagne_ParkingYouPartner.pdf", pages=1, page_mm=(297, 210), trim_mm=(297, 210), trim_off=(0, 0), bleed_set=False, cs="RGB (ICC), mock-up slide"),
    "posterA2": dict(file="posters_420x594_3_1.pdf", pages=1, page_mm=(426, 600), trim_mm=(420, 594), trim_off=(3, 3), bleed_set=True, cs="RGB (ICC sRGB)"),
}
_CACHE: dict = {}


def mm2pt(v):
    return v / PT_MM


def source(key: str) -> Source:
    if key not in _CACHE:
        _CACHE[key] = Source(os.path.join(DIR, SOURCES[key]["file"]))
    return _CACHE[key]


def page_pt(key):
    w, h = SOURCES[key]["page_mm"]
    return mm2pt(w), mm2pt(h)


def box_mm(x0, y0, x1, y1):
    """Rectangle in mm (page coordinates, origin top left of the MediaBox) to source points, for crop()."""
    return (mm2pt(x0), mm2pt(y0), mm2pt(x1), mm2pt(y1))


def reference_items(key, pno=1, omit=None, outline_fonts=(), extra=(), skip_text=None, region=None, under=()):
    """All visible vectors and live text of one page, in paint order, source colours (no normalisation).
    Paths that lie completely outside the page are dropped. `omit(path)` drops more (hidden underlays, leftovers).
    `region` = (x0, y0, x1, y1) in page mm: only what lies completely inside it (one sticker of a sheet)."""
    src = source(key)
    W, H = page_pt(key)

    def skip(p):
        b = p.box
        if b[2] < 0 or b[0] > W or b[3] < 0 or b[1] > H:
            return True
        return bool(omit and omit(p))

    if region:
        items = crop(src, pno, box_mm(*region), partial=False, skip=skip, outline_fonts=outline_fonts, skip_text=skip_text)
        items = regroup(src, pno, items)
        items = items[:1] + list(under) + items[1:]  # `under`: shapes missing in the vector export (shadings) go right above the first item, the die line fill
        return items + list(extra)
    items = crop(src, pno, (-W, -H, 2 * W, 2 * H), partial=True, skip=skip, outline_fonts=outline_fonts, skip_text=skip_text)
    items = regroup(src, pno, items)
    items = items[:1] + list(under) + items[1:] + list(extra)
    pad = mm2pt(12.0)  # a little room around the page; anything farther out is cut (boolean intersection, no clipping mask)
    return clip_to_rect(items, (-pad, -pad, W + pad, H + pad), slack=0.0)


def reference_svg(app_id, key, pno=1, variant="", omit=None, outline_fonts=(), extra=(), skip_text=None, title=None, region=None, trim_box=None, under=()):
    """Faithful reproduction of one source page. viewBox = the whole page (MediaBox, bleed included), mm.
    A hidden group `trim-guide` carries the trim box. Colours are the source colours (sRGB as a viewer shows the CMYK)."""
    info = SOURCES[key]
    items = reference_items(key, pno, omit, outline_fonts, extra, skip_text, region, under)
    el = Element(id=app_id, name_nl="", level="app", category="reference", page=pno, items=items)
    rx0, ry0 = (region[0], region[1]) if region else (0.0, 0.0)
    tf = TF(rx0 / PT_MM, ry0 / PT_MM, PT_MM, 0.0, 0.0)
    defs = Defs(prefix=f"{app_id}{('-' + variant) if variant else ''}-ref-")
    body = el.body(tf, defs)
    W, H = info["page_mm"]
    tx, ty = info["trim_off"]
    tw, th = info["trim_mm"]
    if region:
        W, H = region[2] - region[0], region[3] - region[1]
        tb = trim_box or region
        tx, ty, tw, th = tb[0] - region[0], tb[1] - region[1], tb[2] - tb[0], tb[3] - tb[1]
    d = "<defs>" + "".join(defs.items) + "</defs>" if defs.items else ""
    gid = f"{app_id}-reference" + (f"-{variant}" if variant else "")
    t = title or f"{app_id}{(' ' + variant) if variant else ''}: reference reproduction of {info['file']} page {pno}"
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(W)}mm" height="{fmt(H)}mm" viewBox="0 0 {fmt(W)} {fmt(H)}">\n'
        f"<title>{_esc(t)}</title>\n{d}"
        f'<g id="{gid}" data-role="reference">{body}</g>\n'
        f'<g id="trim-guide" visibility="hidden"><rect x="{fmt(tx)}" y="{fmt(ty)}" width="{fmt(tw)}" height="{fmt(th)}" fill="none" stroke="#00A0E0" stroke-width="0.2"/></g>\n'
        "</svg>\n"
    )


def piece_reference_svg(app_id, key, seq_ranges, origin_mm, scale, trim_mm, pno=1, variant="", omit=None, extra=(), skip_text=None, title=None):
    """Reproduction of ONE mock-up piece taken from a presentation slide, scaled up to its real size.

    seq_ranges: paint order ranges (Source.drawings 'seq') that belong to the piece; origin_mm: top left of the real piece on the slide (mm);
    scale: slide scale (mm on the slide per mm real); trim_mm: real size. viewBox = trim size. Paths inside transparency groups (soft shadows)
    are dropped; list them under omitted. Live text whose centre lies on the piece is added."""
    from .core import affine

    src = source(key)
    ox, oy = origin_mm
    k = 1.0 / scale
    tw, th = trim_mm
    x0, y0 = mm2pt(ox), mm2pt(oy)
    x1, y1 = mm2pt(ox + tw * scale), mm2pt(oy + th * scale)
    inr = lambda q: any(a <= getattr(q, "seq", -1) <= b for a, b in seq_ranges)

    def skip(p_):
        if not inr(p_) or getattr(p_, "gop", ()):
            return True
        return bool(omit and omit(p_))

    items = crop(src, pno, (-1e5, -1e5, 1e5, 1e5), partial=True, skip=skip, texts=False)
    items = clip_to_rect(items, (x0 - mm2pt(2), y0 - mm2pt(2), x1 + mm2pt(2), y1 + mm2pt(2)))
    txt = [t for t in src.texts(pno, (x0, y0, x1, y1), skip_text=skip_text)]
    items = affine(items + txt + list(extra), k, k, -x0 * k, -y0 * k)
    el = Element(id=app_id, name_nl="", level="app", category="reference", page=pno, items=items)
    tf = TF(0.0, 0.0, PT_MM, 0.0, 0.0)
    defs = Defs(prefix=f"{app_id}{('-' + variant) if variant else ''}-ref-")
    body = el.body(tf, defs)
    d = "<defs>" + "".join(defs.items) + "</defs>" if defs.items else ""
    gid = f"{app_id}-reference" + (f"-{variant}" if variant else "")
    t = title or f"{app_id}{(' ' + variant) if variant else ''}: reference reproduction of a mock-up piece from {SOURCES[key]['file']}, scaled to real size (slide scale {scale})"
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(tw)}mm" height="{fmt(th)}mm" viewBox="0 0 {fmt(tw)} {fmt(th)}">\n'
        f"<title>{_esc(t)}</title>\n{d}"
        f'<g id="{gid}" data-role="reference">{body}</g>\n'
        "</svg>\n"
    )
