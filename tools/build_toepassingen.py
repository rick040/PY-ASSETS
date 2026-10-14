#!/usr/bin/env python3
"""Build overview/parkingyou-toepassingen-overzicht.pdf (A3 landscape, vector).

Per application (and variant): the original (reference), the template at the same scale, and an exploded view that lists
the IDs it is built from. Then the new atoms, components and products. Same rules as the element overview: one top-level group
per element (transparency group, no clipping mask), ID labels as separate grey groups (7 pt), nothing rasterised.

usage: python3 -I tools/build_toepassingen.py [--out overview/parkingyou-toepassingen-overzicht.pdf] [--svg-dir overview/toepassingen-pages-svg]
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import cairosvg  # noqa: E402
import pymupdf  # noqa: E402

pymupdf.TOOLS.mupdf_display_errors(False)
pymupdf.TOOLS.mupdf_display_warnings(False)

from pyassets.core import BRAND, fmt  # noqa: E402
from build_overview import FS7, LAB, MX, PH, PW, group, text, tw, wrap, wrap_id  # noqa: E402

TILE = "#D9D9D9"
FRAME = "#D0D0D0"


def read_svg(path):
    s = open(path, encoding="utf8").read()
    m = re.search(r'viewBox="0 0 ([\d.\-]+) ([\d.\-]+)"', s)
    w, h = float(m.group(1)), float(m.group(2))
    defs = re.findall(r'<(?:linearGradient|radialGradient) id=.*?</(?:linearGradient|radialGradient)>', s, re.S)
    body = re.search(r"</title>\s*(?:<defs>.*?</defs>)?(.*)</svg>", s, re.S).group(1).strip()
    body = re.sub(r'<g id="(?:trim-guide|guides)" visibility="hidden">.*?</g>', "", body, flags=re.S)
    return w, h, defs, body, s


def colors_of(s):
    return {c.upper() for c in re.findall(r'(?:fill|stroke|stop-color)="(#[0-9A-Fa-f]{6})"', s)}


class Pg:
    def __init__(self, section, title, sub=""):
        self.section, self.title, self.sub = section, title, sub
        self.body, self.defs, self.ids = [], {}, []

    def embed(self, path, x, y, k, gid, tile=False, frame=True):
        w, h, defs, body, raw = read_svg(path)
        for d in defs:
            self.defs.setdefault(re.search(r'id="([^"]+)"', d).group(1), d)
        if x < -0.01 or y < -0.01 or x + w * k > PW + 0.01 or y + h * k > PH + 0.01:
            raise SystemExit(f"{gid} placed outside the page ({x:.1f},{y:.1f},{w * k:.1f}x{h * k:.1f})")
        if tile:
            self.body.append(group(f'<rect x="{fmt(x - 1.5)}" y="{fmt(y - 1.5)}" width="{fmt(w * k + 3)}" height="{fmt(h * k + 3)}" fill="{TILE}"/>', f"tile-{gid}"))
        elif frame:
            self.body.append(group(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w * k)}" height="{fmt(h * k)}" fill="none" stroke="{FRAME}" stroke-width="0.2"/>', f"frame-{gid}"))
        self.body.append(group(f'<g transform="translate({fmt(x)} {fmt(y)}) scale({fmt(k)})">{body}</g>', gid))
        return w, h

    def label(self, cx, y, ident, name, width, anchor="middle"):
        lines = wrap_id(ident, width, FS7) + wrap(name, width, FS7)
        out, yy = [], y + FS7
        for l in lines:
            out.append(text(cx, yy, l, anchor=anchor))
            yy += FS7 * 1.28
        self.body.append(group("".join(out), f"label-{ident}-{len(self.body)}"))
        return yy - y

    def block(self, x, y, width, lines, gid):
        out, yy = [], y + FS7
        for kind, s in lines:
            if kind == "h":
                out.append(text(x, yy, s, FS7, BRAND["blauw"], weight=700))
                yy += FS7 * 1.4
            else:
                for l in wrap(s, width, FS7):
                    out.append(text(x, yy, l, FS7, "#3C3C3B"))
                    yy += FS7 * 1.28
                yy += FS7 * 0.2
        self.body.append(group("".join(out), gid))
        return yy - y

    def svg(self, num):
        h = [text(MX, 14, self.section.upper(), 3.2, BRAND["aqua"], weight=700),
             text(MX, 24, self.title, 8.5, BRAND["blauw"], weight=700)]
        if self.sub:
            h.append(text(MX, 30, self.sub, 3.2, LAB))
        h.append(text(PW - MX, 14, "parkingyou toepassingen-overzicht", 3.2, LAB, anchor="end"))
        h.append(text(MX, PH - 8, "Bron: tien printbestanden (source/print). Referentie = getrouwe vectorweergave; template = officiele tokenkleuren, 3 mm bleed, variabelen als live tekst. Labels staan in aparte groepen.", FS7, LAB))
        h.append(text(PW - MX, PH - 8, str(num), 4, BRAND["blauw"], weight=700, anchor="end"))
        d = "<defs>" + "".join(self.defs.values()) + "</defs>" if self.defs else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(PW)}mm" height="{fmt(PH)}mm" viewBox="0 0 {fmt(PW)} {fmt(PH)}">'
                f'<rect width="{fmt(PW)}" height="{fmt(PH)}" fill="#FFFFFF"/>{d}{group("".join(h), "page-chrome")}{"".join(self.body)}</svg>')


def fit(w, h, bw, bh):
    return min(bw / w, bh / h)


def app_pages(apps, els, root):
    pages = []
    for spec in apps:
        for v in spec["variants"]:
            vid = v["id"]
            ref = os.path.join(root, "applications", spec["id"], v["reference"])
            tpl = os.path.join(root, "applications", spec["id"], v["template"])
            rw, rh = read_svg(ref)[:2]
            tw_, th_ = read_svg(tpl)[:2]
            vname = f" ({v['variant']})" if v["variant"] else ""
            pg = Pg("Toepassing", f"{spec['name_nl']}{vname}", f"{vid}   |   type {spec['type']}   |   trim {spec['template']['trim_mm'][0]:g} x {spec['template']['trim_mm'][1]:g} mm, bleed {spec['template']['bleed_mm']:g} mm   |   status {spec['status']}")
            top, bot = 36.0, 244.0  # artwork band
            ex_x0, ex_x1 = 302.0, PW - MX  # exploded column
            gap = 8.0
            wide = max(rw, tw_) > 1.25 * max(rh, th_)
            if wide:
                aw, ah = ex_x0 - MX - 6, (bot - top - 16) / 2
                k = fit(max(rw, tw_), max(rh, th_), aw, ah - 8)
                y1 = top + 4
                pg.embed(ref, MX, y1, k, f"{vid}-reference")
                lh = pg.label(MX + rw * k / 2, y1 + rh * k + 1.5, vid, "Origineel (referentie)", 150)
                y2 = y1 + rh * k + lh + 10
                pg.embed(tpl, MX, y2, k, f"{vid}-template")
                pg.label(MX + tw_ * k / 2, y2 + th_ * k + 1.5, vid, "Template (tokenkleuren, met bleed)", 150)
            else:
                aw = (ex_x0 - MX - gap - 6) / 2
                k = fit(max(rw, tw_), max(rh, th_), aw, bot - top - 20)
                pg.embed(ref, MX, top + 4, k, f"{vid}-reference")
                pg.label(MX + rw * k / 2, top + 4 + rh * k + 1.5, vid, "Origineel (referentie)", max(aw, 60))
                x2 = MX + aw + gap
                pg.embed(tpl, x2, top + 4, k, f"{vid}-template")
                pg.label(x2 + tw_ * k / 2, top + 4 + th_ * k + 1.5, vid, "Template (tokenkleuren, met bleed)", max(aw, 60))
            # exploded column
            pg.body.append(group(text(ex_x0, top + 3, "Opgebouwd uit", FS7, BRAND["blauw"], weight=700), "head-exploded"))
            bf = [b for b in spec["built_from"] if b in els]
            n = max(len(bf), 1)
            cols = 3 if n > 6 else 2
            rows_ = -(-n // cols)
            cw = (ex_x1 - ex_x0) / cols
            ch = min(30.0, (bot - top - 8) / rows_)
            for i, b in enumerate(bf):
                r, c = divmod(i, cols)
                bx, by = ex_x0 + c * cw, top + 8 + r * ch
                p = os.path.join(root, els[b]["svg"])
                w, h = read_svg(p)[:2]
                kk = min((cw - 8) / w, (ch - 14) / h, 1.0)
                white = colors_of(open(p, encoding="utf8").read()) <= {"#FFFFFF"}
                pg.embed(p, bx + (cw - 8 - w * kk) / 2, by, kk, f"{vid}-built-{b}", tile=white, frame=False)
                pg.label(bx + (cw - 8) / 2, by + h * kk + 1.2, b, "", cw - 6)
            # spec block
            src = spec["source"]["files"]
            lines = [("h", "Specificatie")]
            lines.append(("t", f"Bron: {', '.join(f['file'].split('/')[-1] + ' p' + ','.join(map(str, f['pages'])) for f in src)}  ({src[0]['colour_space']}; bleed box in bron {'ja' if src[0]['bleed_box_set'] else 'nee'}). "
                               f"Template: trim {spec['template']['trim_mm'][0]:g} x {spec['template']['trim_mm'][1]:g} mm, bleed {spec['template']['bleed_mm']:g} mm, totaal {spec['template']['size_with_bleed_mm'][0]:g} x {spec['template']['size_with_bleed_mm'][1]:g} mm."))
            vv = spec["variables"].get(v["variant"] or "default", {})
            if vv:
                lines.append(("t", "Variabelen: " + "; ".join(f"{k} = {str(x)[:48]}" for k, x in list(vv.items())[:14])))
            cc = spec.get("template", {}).get("cut_contour")
            if cc:
                lines.append(("t", f"Snijcontour: groep cut-contour, spot {cc.get('spot', 'ThruCut')}, {cc.get('stroke_pt', 1)} pt, {cc.get('inset_mm', 0.2)} mm binnen de trim." + (f" {cc['note']}" if cc.get("note") else "")))
            for c in spec.get("copy_corrections", []):
                lines.append(("t", f"Tekstcorrectie in template: \"{c['original']}\" wordt \"{c['corrected']}\" (referentie houdt het origineel)."))
            if spec.get("notes"):
                lines.append(("t", str(spec["notes"])[:420]))
            pg.block(MX, bot + 6, PW - 2 * MX, lines, f"spec-{vid}")
            pages.append((pg, f"{vid}"))
            pg.ids += [vid] + bf
    return pages


def element_pages(new_els, root):
    pages = []
    groups = [("Nieuwe atomen", [e for e in new_els if e["level"] == "atom"]),
              ("Nieuwe componenten", [e for e in new_els if e["level"] == "comp"]),
              ("Nieuwe producten", [e for e in new_els if e["level"] == "prod"])]
    for title, items in groups:
        if not items:
            continue
        per = 12 if title != "Nieuwe producten" else 3
        for pi in range(0, len(items), per):
            chunk = items[pi:pi + per]
            n_pages = -(-len(items) // per)
            sub = "Elk element op eigen schaal (past in zijn cel); echte maat staat in het label. [third-party] = alleen referentie, officieel bestand ophalen."
            pg = Pg("Print-elementen", title + (f" ({pi // per + 1}/{n_pages})" if n_pages > 1 else ""), sub)
            cols = 4 if title != "Nieuwe producten" else 3
            rows_ = -(-len(chunk) // cols)
            cw, ch = (PW - 2 * MX) / cols, (276 - 40) / rows_
            for i, e in enumerate(chunk):
                r, c = divmod(i, cols)
                x0, y0 = MX + c * cw, 40 + r * ch
                p = os.path.join(root, e["svg"])
                w, h = read_svg(p)[:2]
                lab_h = 4 * FS7 * 1.28 + FS7
                kk = min((cw - 10) / w, (ch - lab_h - 8) / h)
                white = colors_of(open(p, encoding="utf8").read()) <= {"#FFFFFF"}
                pg.embed(p, x0 + (cw - 10 - w * kk) / 2, y0, kk, e["id"], tile=white, frame=False)
                name = e["name_nl"] + (" [third-party]" if "third-party" in e["tags"] else "") + (" [rebuilt]" if e["status"] == "rebuilt" else "") + f"  {e['dimensions_mm']['width']:g} x {e['dimensions_mm']['height']:g} mm"
                pg.label(x0 + (cw - 10) / 2, y0 + h * kk + 3, e["id"], name, cw - 12)
                pg.ids.append(e["id"])
            pages.append((pg, title))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "overview", "parkingyou-toepassingen-overzicht.pdf"))
    ap.add_argument("--svg-dir", default=None)
    a = ap.parse_args()
    man = json.load(open(os.path.join(ROOT, "elements.json"), encoding="utf8"))
    els = {e["id"]: e for e in man["elements"]}
    new_els = [e for e in man["elements"] if e.get("origin") == "print"]
    apps = json.load(open(os.path.join(ROOT, "applications.json"), encoding="utf8"))["applications"]
    apages = app_pages(apps, els, ROOT)
    epages = element_pages(new_els, ROOT)

    # index
    idx = Pg("Index", "Toepassingen en nieuwe elementen", "Elke toepassing: origineel, template en opbouw uit bestaande en nieuwe elementen")
    y = 40.0
    idx.body.append(group(text(MX, y, "Toepassingen", 4, BRAND["blauw"], weight=700), "idx-h1"))
    y += 6
    rows = [text(MX, y, "ID", FS7, BRAND["blauw"], weight=700), text(MX + 118, y, "Naam", FS7, BRAND["blauw"], weight=700),
            text(MX + 205, y, "Type", FS7, BRAND["blauw"], weight=700), text(MX + 235, y, "Trim (mm)", FS7, BRAND["blauw"], weight=700),
            text(MX + 275, y, "Pagina", FS7, BRAND["blauw"], weight=700)]
    y += 4
    pno = 3
    for s in apps:
        for v in s["variants"]:
            rows.append(text(MX, y, v["id"], FS7, "#3C3C3B"))
            rows.append(text(MX + 118, y, s["name_nl"] + (f" ({v['variant']})" if v["variant"] else ""), FS7, "#3C3C3B"))
            rows.append(text(MX + 205, y, s["type"], FS7, "#3C3C3B"))
            rows.append(text(MX + 235, y, f"{s['template']['trim_mm'][0]:g} x {s['template']['trim_mm'][1]:g}", FS7, "#3C3C3B"))
            rows.append(text(MX + 275, y, str(pno), FS7, "#3C3C3B"))
            y += 3.6
            pno += 1
    idx.body.append(group("".join(rows), "idx-apps"))
    y += 6
    idx.body.append(group(text(MX, y, "Nieuwe elementen", 4, BRAND["blauw"], weight=700), "idx-h2"))
    y += 6
    cols = 3
    cw = (PW - 2 * MX) / cols
    per_col = -(-len(new_els) // cols)
    out = []
    for i, e in enumerate(new_els):
        c, r = divmod(i, per_col)
        out.append(text(MX + c * cw, y + r * 3.3, e["id"], 2.2, "#3C3C3B"))
    idx.body.append(group("".join(out), "idx-elements"))
    # fit check: index must stay inside the page
    if y + per_col * 3.3 > PH - 12:
        raise SystemExit("index too long for one page")

    # cover
    cov = []
    cov.append(text(MX, 60, "parkingyou", 14, BRAND["blauw"], weight=700))
    cov.append(text(MX, 80, "Toepassingen-overzicht", 11, BRAND["aqua"], weight=700))
    cov.append(text(MX, 98, "Printtoepassingen opgebouwd uit de bibliotheek van atomen en componenten. Per toepassing: origineel, template en opbouw.", 3.6, "#3C3C3B"))
    cov.append(text(MX, 108, f"{len(apps)} toepassingen, {sum(len(s['variants']) for s in apps)} versies, {len(new_els)} nieuwe elementen (atomen, componenten, producten).", 3.6, "#3C3C3B"))
    cov.append(text(MX, 124, "Lees dit zo", 4, BRAND["blauw"], weight=700))
    for i, l in enumerate([
        "Origineel (referentie): getrouwe vector van het printbestand, inclusief bronkleuren en originele tekst. Alleen om mee te vergelijken.",
        "Template: officiele merkkleuren uit tokens.json, juiste trim en 3 mm bleed (10 mm bij het uitritbord), variabelen als live Ubuntu-tekst of als gemarkeerde placeholder.",
        "Snijcontour van stickers en bord staat in een eigen groep cut-contour (spotkleur ThruCut, 1 pt, 0,2 mm binnen de trim).",
        "Opgebouwd uit: de ID's van bestaande en nieuwe elementen; elk element is een eigen groep, het label staat in een aparte grijze groep.",
        "Derde-partij merken (betaal, partner, GLOW) staan er alleen als referentie in. Haal de officiele bestanden op.",
        "Waargenomen regels en afwijkingen: docs/print-rules.md. Dit zijn regels uit de praktijk, geen officiele handboekregels.",
    ]):
        cov.append(text(MX, 133 + i * 6, l, 3.2, "#3C3C3B"))
    cover = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(PW)}mm" height="{fmt(PH)}mm" viewBox="0 0 {fmt(PW)} {fmt(PH)}">'
             f'<rect width="{fmt(PW)}" height="{fmt(PH)}" fill="#FFFFFF"/>{group("".join(cov), "cover")}</svg>')

    docs = pymupdf.open()
    svgs, toc = [], []

    def add(s, title=None, num=None):
        svgs.append(s)
        with pymupdf.open(stream=cairosvg.svg2pdf(bytestring=s.encode())) as d:
            docs.insert_pdf(d)
        if title:
            toc.append([1, title, num or len(docs)])

    add(cover, "Cover", 1)
    add(idx.svg(2), "Index", 2)
    num = 3
    for pg, t in apages + epages:
        add(pg.svg(num), t, num)
        num += 1
    docs.set_toc(toc)
    docs.set_metadata({"title": "parkingyou toepassingen-overzicht", "author": "ParkingYou", "subject": "Print applications built from the brand asset library", "keywords": "parkingyou, huisstijl, print, vector"})
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    docs.save(a.out, garbage=3, deflate=True)
    print("pages:", len(docs), "apps:", len(apps), "new elements:", len(new_els), "->", a.out)
    if a.svg_dir:
        os.makedirs(a.svg_dir, exist_ok=True)
        for i, s in enumerate(svgs, 1):
            open(os.path.join(a.svg_dir, f"page-{i:02d}.svg"), "w", encoding="utf8").write(s)


if __name__ == "__main__":
    main()
