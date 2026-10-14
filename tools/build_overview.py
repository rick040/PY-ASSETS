#!/usr/bin/env python3
"""Build parkingyou-elementen-overzicht.pdf (A3 landscape, vector, editable).

Every element is one top-level group (a transparency group in the PDF, no clipping mask), in its own
cell. The ID label under it is a separate group, 7 pt neutral grey. Products sit on one scale per page
with a spec block beside them.

usage: python3 -I tools/build_overview.py --src source/handbook.pdf [--spec REGEX] --out overview/parkingyou-elementen-overzicht.pdf
"""
import argparse, importlib, json, os, pkgutil, re, sys, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import cairosvg  # noqa: E402
import pymupdf  # noqa: E402

pymupdf.TOOLS.mupdf_display_errors(False)
pymupdf.TOOLS.mupdf_display_warnings(False)

from pyassets import BRAND, Defs, Source, registry  # noqa: E402
from pyassets.core import _font_adv, fmt  # noqa: E402
import build_all  # noqa: E402

PW, PH = 420.0, 297.0
MX, MY0, MY1 = 15.0, 36.0, 276.0  # content area
LAB = "#8C8C8C"
PT = 25.4 / 72.0
FS7 = 7 * PT  # 7 pt in mm

TOKEN_TILE = "#D9D9D9"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tw(s, size_mm, fam="Ubuntu", w=400):
    cmap, hm, upm = _font_adv(fam, w, False)
    return sum(hm[cmap[ord(c)]][0] for c in s if ord(c) in cmap) * size_mm / upm


def wrap(text, width, size_mm, fam="Ubuntu", w=400):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if tw(t, size_mm, fam, w) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wrap_id(id_, width, size_mm):
    parts = id_.split("-")
    lines, cur = [], ""
    for i, p in enumerate(parts):
        t = (cur + "-" + p) if cur else p
        if tw(t, size_mm) <= width or not cur:
            cur = t
        else:
            lines.append(cur + "-")
            cur = p
    lines.append(cur)
    return lines


def text(x, y, s, size=FS7, fill=LAB, fam="Ubuntu", weight=400, anchor="start", italic=False):
    a = f'x="{fmt(x)}" y="{fmt(y)}" font-family="{fam}" font-size="{fmt(size)}" fill="{fill}"'
    if weight == 700:
        a += ' font-weight="bold"'
    if italic:
        a += ' font-style="italic"'
    if anchor != "start":
        a += f' text-anchor="{anchor}"'
    return f'<text {a} xml:space="preserve">{esc(s)}</text>'


def group(inner, gid=None):
    # opacity just below 1 makes cairo write a transparency group (one Form XObject) that
    # Illustrator imports as a single group; it renders identically.
    i = f' id="{gid}"' if gid else ""
    return f'<g{i} opacity="0.9999">{inner}</g>'


class Page:
    def __init__(self, section, title, sub=""):
        self.section, self.title, self.sub = section, title, sub
        self.body = []
        self.defs = []
        self.ids = []
        self.n = 0

    def chrome(self, num, total):
        h = [text(MX, 14, self.section.upper(), 3.2, BRAND["aqua"], weight=700),
             text(MX, 24, self.title, 8.5, BRAND["blauw"], weight=700)]
        if self.sub:
            h.append(text(MX, 30, self.sub, 3.2, LAB))
        h.append(text(PW - MX, 14, "parkingyou elementen-overzicht", 3.2, LAB, anchor="end"))
        h.append(text(MX, PH - 8, "Bron: parkingyou Huisstijlhandboek v1.0, 09-2025. Elementen zijn bewerkbare vectoren; labels staan in aparte groepen.", FS7, LAB))
        h.append(text(PW - MX, PH - 8, f"{num}", 4, BRAND["blauw"], weight=700, anchor="end"))
        return group("".join(h), "page-chrome")

    def svg(self, num, total):
        d = "<defs>" + "".join(self.defs) + "</defs>" if self.defs else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(PW)}mm" height="{fmt(PH)}mm" viewBox="0 0 {fmt(PW)} {fmt(PH)}">'
                f'<rect width="{fmt(PW)}" height="{fmt(PH)}" fill="#FFFFFF"/>{d}{self.chrome(num, total)}{"".join(self.body)}</svg>')

    def add_element(self, el, x, y, k, tile=False):
        """Place element with its top-left corner at (x, y), scale k (mm per mm)."""
        defs = Defs(prefix=f"{el.id}-")
        tf = el.tf(scale=k, ox=x, oy=y)
        inner = el.body(tf, defs)
        self.defs += defs.items
        w, h = el.size_mm()
        if x < -0.01 or y < -0.01 or x + w * k > PW + 0.01 or y + h * k > PH + 0.01:
            raise SystemExit(f"{el.id} is placed outside the page ({x:.1f},{y:.1f},{w * k:.1f}x{h * k:.1f})")
        if tile:
            self.body.append(group(f'<rect x="{fmt(x - 2)}" y="{fmt(y - 2)}" width="{fmt(w * k + 4)}" height="{fmt(h * k + 4)}" fill="{TOKEN_TILE}"/>', f"tile-{el.id}"))
        self.body.append(group(inner, el.id))
        self.ids.append(el.id)

    def add_label(self, el, cx, y, width):
        ls = wrap_id(el.id, width, FS7)
        nm = wrap(el.name_nl + (" [third-party]" if "third-party" in el.tags else "") + (" [rebuilt]" if el.status == "rebuilt" else ""), width, FS7)
        out = []
        yy = y + FS7
        for l in ls + nm:
            out.append(text(cx, yy, l, anchor="middle"))
            yy += FS7 * 1.28
        self.body.append(group("".join(out), f"label-{el.id}"))
        return yy - y

    def add_spec(self, x, y, lines, gid, width):
        out = []
        yy = y + FS7
        for kind, s in lines:
            if kind == "h":
                out.append(text(x, yy, s, FS7, BRAND["blauw"], weight=700))
                yy += FS7 * 1.4
            else:
                for l in wrap(s, width, FS7):
                    out.append(text(x, yy, l, FS7, "#3C3C3B"))
                    yy += FS7 * 1.28
                yy += FS7 * 0.25
        self.body.append(group("".join(out), gid))


# ---------------------------------------------------------------- cell geometry
def label_dims(el, maxw):
    ls = wrap_id(el.id, maxw, FS7)
    nm = wrap(el.name_nl + (" [third-party]" if "third-party" in el.tags else "") + (" [rebuilt]" if el.status == "rebuilt" else ""), maxw, FS7)
    width = max(max(tw(l, FS7) for l in ls + nm), 1)
    return width, (len(ls) + len(nm)) * FS7 * 1.28 + FS7


def cell_size(el, k, maxlab=46.0):
    w, h = el.size_mm()
    lw, lh = label_dims(el, maxlab)
    return max(w * k, lw), h * k + 3 + lh, lw, lh


def shelf(cells, area=(MX, MY0, PW - MX, MY1), gx=9.0, gy=10.0):
    """cells: list of (w,h). Returns positions or None when they do not fit."""
    x0, y0, x1, y1 = area
    x, y, rowh = x0, y0, 0
    pos = []
    for w, h in cells:
        if w > x1 - x0 or h > y1 - y0:
            return None
        if x + w > x1 + 1e-6:
            x, y, rowh = x0, y + rowh + gy, 0
        if y + h > y1 + 1e-6:
            return None
        pos.append((x, y))
        x += w + gx
        rowh = max(rowh, h)
    return pos


def is_white(el):
    """True when white artwork would vanish on the white page: white covers a good share of the element."""
    from pyassets.core import Path, Text

    cols = set(el.colors())
    if "#FFFFFF" not in cols:
        return False
    if cols <= {"#FFFFFF"}:
        return True
    b = el.bbox()
    area = max((b[2] - b[0]) * (b[3] - b[1]), 1e-6)
    wa = 0.0
    big_dark = 0.0
    for it in el.items:
        bb = it.bbox
        a = max(bb[2] - bb[0], 0) * max(bb[3] - bb[1], 0)
        if isinstance(it, Path) and it.fill == "#FFFFFF":
            wa += a
        elif isinstance(it, Text) and it.fill == "#FFFFFF":
            wa += a
        elif isinstance(it, Path) and it.fill is not None:
            big_dark += a
    # white that sits on a large dark/colour shape needs no tile; loose white parts do
    return wa / area >= 0.10 and big_dark / area < 0.9 and not (big_dark / area > 0.5 and wa < big_dark)


# ---------------------------------------------------------------- pagination
def paginate(els, scales, cellfn, area=(MX, MY0, PW - MX, MY1)):
    """Greedy: keep adding elements while a common scale from `scales` (large to small) still fits."""
    pages, cur = [], []
    best = None

    def fits(group):
        for k in scales:
            cells = [cellfn(e, k) for e in group]
            pos = shelf([(c[0], c[1]) for c in cells], area)
            if pos is not None:
                return k, cells, pos
        return None

    for e in els:
        trial = cur + [e]
        f = fits(trial)
        if f is None:
            if cur:
                pages.append(cur)
            cur = [e]
            if fits(cur) is None:
                raise SystemExit(f"{e.id} does not fit a page at any scale")
        else:
            cur = trial
    if cur:
        pages.append(cur)
    return [(g,) + fits(g) for g in pages]


def grid_page(title, section, group, k, cells, pos, sub=""):
    pg = Page(section, title, sub)
    for el, c, (x, y) in zip(group, cells, pos):
        cw, ch, lw, lh = c
        w, h = el.size_mm()
        ax = x + (cw - w * k) / 2
        pg.add_element(el, ax, y, k, tile=is_white(el))
        pg.add_label(el, x + cw / 2, y + h * k + 3, max(lw, 10))
    return pg


# ---------------------------------------------------------------- sections
ATOM_PAGES = [
    ("Logo", r"^py-atom-logo-"),
    ("Vormen en symbool", r"^py-atom-(shape|symbol)-"),
    ("Pijlen", r"^py-atom-arrow-"),
    ("Pictogrammen", r"^py-atom-picto-"),
    ("Labels, display, sticker en hoogtebalk", r"^py-atom-(tag|display|sticker|pattern|text)-"),
    ("Figuren", r"^py-atom-figure-"),
    ("Derde partij: RVV en overige borden (referentie)", r"^py-atom-(rvv|sign)-"),
    ("Derde partij: betaaltekens en vluchtwegsymbolen (referentie)", r"^py-atom-(payment|escape)-"),
]
COMP_PAGES = [
    ("Routebord-modules", r"^py-comp-(route|walk)-"),
    ("Portaal", r"^py-comp-(portal|rvv-cluster-portal)"),
    ("Lichtbakfronten en naamveld", r"^py-comp-(face|location)-"),
    ("Pyloon", r"^py-comp-(pyloon|price|rvv-cluster-pyloon)"),
    ("Niveau, sectie en overzicht", r"^py-comp-(section|overview)-"),
    ("Rijstvliesborden", r"^py-comp-bord-"),
    ("Hoogtebalk, welkom en vluchtweg", r"^py-comp-(hoogtebalk|welcome|escape)"),
]

TOKEN_SPECS = {}


def spec_lines_token(el):
    from pyassets.core import GRADIENT_STOPS
    id_ = el.id
    if "color" in id_:
        k = id_.split("-")[-1]
        d = {"blauw": ("#1A3580", "100/83/0/17", "5002"), "aqua": ("#32B9CD", "69/0/21/0", "6027"), "oranje": ("#F08300", "0/57/100/0", "2003"),
             "grijs": ("#AEAEAE", "0/0/0/42", "9006"), "zwart": ("#1D1D1B", "0/0/0/100", "9005")}
        if k in d:
            hx, cm, ral = d[k]
            rgb = build_all.hex_rgb(hx)
            return [("t", f"HEX {hx}"), ("t", f"RGB {rgb[0]}/{rgb[1]}/{rgb[2]}"), ("t", f"CMYK {cm}"), ("t", f"RAL {ral} (beste match)")]
        return [("t", el.notes or "")]
    if "gradient" in id_:
        return [("t", "0% #1A3580, 18% #1A3580, 62% #097BAE, 100% #32B9CD"), ("t", "Gemeten, niet gedefinieerd in 1.3")]
    return []


def product_units(prods):
    """Group front/back and variant pairs into one unit that shares a row and a spec block."""
    units, seen = [], set()
    by = {p.id: p for p in prods}

    def stem(i):
        s = re.sub(r"-(front|back)$", "", i)
        s = re.sub(r"-(extradisplay|nodisplay)$", "", s)
        s = re.sub(r"-display$", "", s) if "aanrijroute" in s else s
        return s

    for p in prods:
        if p.id in seen:
            continue
        st = stem(p.id)
        members = [q for q in prods if stem(q.id) == st and q.id not in seen]
        for q in members:
            seen.add(q.id)
        members.sort(key=lambda q: (0 if q.id.endswith("-front") else 1 if q.id.endswith("-back") else 0,
                                    1 if re.search(r"-(extradisplay|nodisplay)$", q.id) else 0, q.id))
        units.append(members)
    return units


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--spec", default=None)
    ap.add_argument("--out", default=os.path.join(ROOT, "overview", "parkingyou-elementen-overzicht.pdf"))
    ap.add_argument("--svg-dir", default=None, help="also write the page SVGs here (fallback with real named groups)")
    a = ap.parse_args()
    build_all.load_specs(a.spec)
    src = Source(a.src)
    inv = build_all.parse_inventory()
    els = {i: registry.build(src, i) for i in sorted(registry.BUILDERS)}
    by_level = {l: [e for e in els.values() if e.level == l] for l in ("tok", "atom", "comp", "prod")}

    pages = []  # (Page, toc_title)

    # ---- tokens
    tok = by_level["tok"]
    colors = [e for e in tok if "-color-" in e.id]
    grads = [e for e in tok if "-gradient-" in e.id]
    types = [e for e in tok if "-type-" in e.id]
    for title, grp, per_row in (("Kleuren", colors, 6), ("Verlopen", grads, 3), ("Typografie", types, 3)):
        if not grp:
            continue
        pg = Page("Tokens", title, "Waarden uit handbook 1.3; niet-merkkleuren zijn waargenomen in de tekeningen")
        cw = (PW - 2 * MX) / per_row
        k = 1.6 if title != "Typografie" else 1.2
        for i, e in enumerate(grp):
            r, c = divmod(i, per_row)
            x = MX + c * cw
            y = MY0 + 6 + r * 82
            w, h = e.size_mm()
            kk = min(k, 58.0 / w, 40.0 / h)  # large true-scale tokens (hoogtebalk lettering) must stay inside the cell
            pg.add_element(e, x + 8, y, kk, tile=is_white(e))
            ly = y + h * kk + 3
            hh = pg.add_label(e, x + 8 + w * kk / 2, ly, 46)
            sp = spec_lines_token(e)
            if sp:
                pg.add_spec(x + 8, ly + hh + 1, sp, f"spec-{e.id}", 46)
        pages.append((pg, f"Tokens: {title}"))

    # ---- atoms and components
    def atoms_like(level, defs, scales, area=None):
        rest = list(by_level[level])
        out = []
        def emit(title, grp):
            grp.sort(key=lambda e: e.id)
            for sub, tag in ((False, ""), (True, " (ware schaal)")):
                g_ = [e for e in grp if bool(e.true_scale) == sub]
                if not g_:
                    continue
                for n, (g, k, cells, pos) in enumerate(paginate(g_, scales, lambda e, k: cell_size(e, k))):
                    t_ = title + tag + (f" ({n + 1})" if n else "")
                    pg = grid_page(t_, "Atomen" if level == "atom" else "Componenten", g, k, cells, pos,
                                   f"Weergave {k:.2f}x van de SVG-grootte (mm)" + (", gemeten aan een maat uit het handboek" if sub else ", grootte illustratief (geen maat in het handboek)"))
                    pages.append((pg, f"{'Atomen' if level == 'atom' else 'Componenten'}: {t_}"))

        for title, pat in defs:
            grp = [e for e in rest if re.search(pat, e.id)]
            rest = [e for e in rest if e not in grp]
            if grp:
                emit(title, grp)
        if rest:
            emit("Overig", rest)

    atoms_like("atom", ATOM_PAGES, [3.0, 2.5, 2.0, 1.6, 1.3, 1.0, 0.8, 0.6, 0.45, 0.3, 0.2, 0.15, 0.1, 0.07, 0.05])
    atoms_like("comp", COMP_PAGES, [1.0, 0.75, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.075, 0.05])

    # ---- products: one consistent scale per page, front and back side by side, spec block beside
    prods = by_level["prod"]
    prods.sort(key=lambda e: e.id)
    order = []
    # follow handbook order via source page of the first product of each unit
    units = product_units(prods)
    units.sort(key=lambda u: (min((p.page if isinstance(p.page, int) else (p.page[0] if p.page else 99)) for p in u), u[0].id))
    SPECW = 58.0

    def unit_spec(u):
        lines = []
        for p in u:
            row = inv.get(p.id, {})
            lines.append(("h", p.name_nl))
            st = p.dims_mm
            if st:
                lines.append(("t", "Maat " + " x ".join(str(round(v)) for v in st if v) + " mm"))
            if row.get("spec"):
                lines.append(("t", row["spec"]))
            lines.append(("t", f"Handboek p{p.page if isinstance(p.page, int) else ', '.join(map(str, p.page or []))}"))
        return lines

    def spec_height(lines, width):
        h = FS7
        for kind, s in lines:
            if kind == "h":
                h += FS7 * 1.4
            else:
                h += len(wrap(s, width, FS7)) * FS7 * 1.28 + FS7 * 0.25
        return h

    def kp(p, N):
        """Scale of one product: 1/N when the handbook gives a dimension, otherwise a fixed display size."""
        if p.true_scale:
            return 1.0 / N
        w, h = p.size_mm()
        return min(90.0 / w, 75.0 / h)

    def unit_cell(u, N):
        w = sum(p.size_mm()[0] * kp(p, N) for p in u) + 6 * (len(u) - 1)
        h = max(p.size_mm()[1] * kp(p, N) for p in u)
        lab_h = max(label_dims(p, max(p.size_mm()[0] * kp(p, N), 40))[1] for p in u)
        wlabs = sum(max(p.size_mm()[0] * kp(p, N), label_dims(p, 40)[0]) for p in u) + 6 * (len(u) - 1)
        return wlabs + 8 + SPECW, max(h + 3 + lab_h, spec_height(unit_spec(u), SPECW - 2))

    denoms = [5, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75, 100]
    pages_p, cur = [], []

    def fitsU(group):
        for N in denoms:
            cells = [unit_cell(u, N) for u in group]
            pos = shelf(cells, gx=8, gy=9)
            if pos is not None:
                # keep sizes comparable: no unit may be shown more than 2.5x smaller than it could be
                if len(group) > 1 and any(N > 2.5 * alone[id(u)] for u in group):
                    return None
                return N, cells, pos
        return None

    alone = {}
    for u in units:
        for N in denoms:
            if shelf([unit_cell(u, N)], gx=8, gy=9) is not None:
                alone[id(u)] = N
                break
        else:
            raise SystemExit(f"unit {u[0].id} does not fit a page")

    for u in units:
        f = fitsU(cur + [u])
        if f is None:
            if cur:
                pages_p.append(cur)
            cur = [u]
            if fitsU(cur) is None:
                raise SystemExit(f"unit {u[0].id} does not fit a page")
        else:
            cur = cur + [u]
    if cur:
        pages_p.append(cur)
    for n, g in enumerate(pages_p):
        N, cells, pos = fitsU(g)
        secs = sorted({(m.page if isinstance(m.page, int) else m.page[0]) for u in g for m in u if m.page})
        pg = Page("Producten", f"Producten, handboek p{secs[0]} tot p{secs[-1]}" if len(secs) > 1 else f"Producten, handboek p{secs[0]}",
                  f"Schaal 1:{N} voor alle producten op deze pagina. Voor- en achterzijde naast elkaar.")
        for u, (cw, ch), (x, y) in zip(g, cells, pos):
            xx = x
            for p in u:
                k = kp(p, N)
                w, h = p.size_mm()
                lw, lh = label_dims(p, max(w * k, 40))
                cwid = max(w * k, lw)
                pg.add_element(p, xx + (cwid - w * k) / 2, y, k, tile=is_white(p))
                pg.add_label(p, xx + cwid / 2, y + h * k + 3, max(lw, 10))
                xx += cwid + 6
            lines = unit_spec(u)
            pg.add_spec(xx - 6 + 8, y, lines, f"spec-{u[0].id}", SPECW - 2)
        pages.append((pg, f"Producten p{secs[0]}-{secs[-1]} (1:{N})" if len(secs) > 1 else f"Producten p{secs[0]} (1:{N})"))

    # ---- cover and index
    total = len(pages) + 3
    front = []
    cov = Page("", "")
    cov.body.append(f'<rect x="0" y="0" width="{fmt(PW)}" height="120" fill="{BRAND["blauw"]}"/>')
    cov.body.append(text(MX + 5, 62, "parkingyou", 22, "#FFFFFF", weight=700))
    cov.body.append(text(MX + 5, 85, "Elementen-overzicht", 12, BRAND["aqua"], weight=700))
    cov.body.append(text(MX + 5, 105, "Alle merk- en signing-elementen uit de huisstijlhandboek, als bewerkbare vectoren", 5, "#FFFFFF"))
    n_by = {l: len(by_level[l]) for l in by_level}
    lines = [f"Bron: parkingyou Huisstijlhandboek, Wayfinding & inrichting parkeervoorziening, versie 1.0, 09-2025 (All Jobs)",
             f"Tokens {n_by['tok']}, atomen {n_by['atom']}, componenten {n_by['comp']}, producten {n_by['prod']} (totaal {sum(n_by.values())})",
             "Elke element is een eigen groep; het ID-label (7 pt, grijs) staat in een aparte groep eronder en kan voor export worden verwijderd."]
    for i, l in enumerate(lines):
        cov.body.append(text(MX + 5, 150 + i * 9, l, 4.2, "#3C3C3B"))
    cov.body.append(text(MX + 5, 200, "Opmerkingen", 4.2, BRAND["blauw"], weight=700))
    notes = ["Verlopen zijn herbouwd als echte vectorverlopen (de bron slaat ze op als shading of rasterplaatje binnen een clip-pad).",
             "Elementen gemarkeerd met [rebuilt] zijn niet rechtstreeks uit de bronpaden gehaald; zie elements.json.",
             "Derde-partij tekens (RVV, betaalmerken, vluchtwegsymbolen) staan alleen als referentie; haal officiele bestanden op.",
             "Het All Jobs-logo en de handboekvoet zijn bewust niet opgenomen."]
    for i, l in enumerate(notes):
        cov.body.append(text(MX + 5, 208 + i * 6.5, l, FS7 * 1.15, "#3C3C3B"))

    # index: sections on the first index page, element IDs in columns; extra index pages when needed
    per = int((MY1 - MY0 - 12) / 3.2)
    first_cap = per * 2  # two columns right of the section table
    n_ids = sum(len(pg.ids) for pg, _ in pages)
    extra_n = 0
    while True:
        start = 3 + extra_n
        allids = sorted((i, num) for num, (pg, t) in enumerate(pages, start=start) for i in pg.ids)
        need = max(0, (len(allids) - first_cap + per * 3 - 1) // (per * 3))
        if need == extra_n:
            break
        extra_n = need
    start = 3 + extra_n
    pidx = Page("Index", "Inhoud", "Pagina's per sectie en elk element-ID met zijn pagina")
    y = MY0 + 4
    for xx, hd in ((MX, "Pagina"), (MX + 16, "Sectie"), (MX + 120, "Elementen")):
        pidx.body.append(text(xx, y, hd, 3, BRAND["blauw"], weight=700))
    y += 5
    for num, (pg, t) in enumerate(pages, start=start):
        pidx.body.append(text(MX, y, str(num), 3.2, "#3C3C3B"))
        pidx.body.append(text(MX + 16, y, t, 3.2, "#3C3C3B"))
        pidx.body.append(text(MX + 120, y, str(len(pg.ids)), 3.2, "#3C3C3B"))
        y += 4.3
    pidx.body.append(text(MX + 150, MY0 + 4, "Element-ID's en pagina", 3, BRAND["blauw"], weight=700))
    cols = [MX + 150, MX + 150 + 120]
    for q, (i_, n_) in enumerate(allids[:first_cap]):
        col, row = divmod(q, per)
        pidx.body.append(text(cols[col], MY0 + 9 + row * 3.2, f"{i_}  p{n_}", 2.3, "#3C3C3B"))
    extra = []
    rest = allids[first_cap:]
    for j in range(extra_n):
        pg = Page("Index", f"Element-ID's ({j + 2})")
        chunk = rest[j * per * 3:(j + 1) * per * 3]
        for q, (i_, n_) in enumerate(chunk):
            col, row = divmod(q, per)
            pg.body.append(text(MX + col * 130, MY0 + 4 + row * 3.2, f"{i_}  p{n_}", 2.3, "#3C3C3B"))
        extra.append(pg)
    total = len(pages) + 2 + extra_n

    # ---- render
    docs = pymupdf.open()
    toc = []
    svgs = []

    def add(pg, num, title=None, chrome=True):
        s = pg.svg(num, total) if chrome else pg.svg(num, total)
        svgs.append(s)
        pdf = cairosvg.svg2pdf(bytestring=s.encode())
        with pymupdf.open(stream=pdf) as d:
            docs.insert_pdf(d)
        if title:
            toc.append([1, title, num])

    # cover without chrome text
    cov_svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(PW)}mm" height="{fmt(PH)}mm" viewBox="0 0 {fmt(PW)} {fmt(PH)}">'
               f'<rect width="{fmt(PW)}" height="{fmt(PH)}" fill="#FFFFFF"/>{"".join(cov.body)}</svg>')
    svgs.append(cov_svg)
    with pymupdf.open(stream=cairosvg.svg2pdf(bytestring=cov_svg.encode())) as d:
        docs.insert_pdf(d)
    toc.append([1, "Cover", 1])
    add(pidx, 2, "Index")
    num = 3
    for e in extra:
        add(e, num)
        num += 1
    for pg, t in pages:
        add(pg, num, t)
        num += 1
    docs.set_toc(toc)
    docs.set_metadata({"title": "parkingyou elementen-overzicht", "author": "ParkingYou", "subject": "Brand and signage elements from the huisstijlhandboek v1.0 (09-2025)", "keywords": "parkingyou, huisstijl, signing, vector"})
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    docs.save(a.out, garbage=3, deflate=True)
    print("pages:", len(docs), "elements placed:", sum(len(p.ids) for p, _ in pages), "->", a.out)
    if a.svg_dir:
        os.makedirs(a.svg_dir, exist_ok=True)
        for i, s in enumerate(svgs, 1):
            open(os.path.join(a.svg_dir, f"page-{i:02d}.svg"), "w", encoding="utf8").write(s)
    json.dump({"pages": [{"page": i + 4, "title": t, "ids": pg.ids} for i, (pg, t) in enumerate(pages)]}, open(os.path.join(ROOT, "build", "overview_pages.json"), "w") if os.path.isdir(os.path.join(ROOT, "build")) else open(os.devnull, "w"), indent=1)


if __name__ == "__main__":
    main()
