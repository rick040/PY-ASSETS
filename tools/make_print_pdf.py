#!/usr/bin/env python3
"""Print PDF from a print SVG of print/: text outlined with the Ubuntu fonts, page = trim + bleed at 1:1, TrimBox and BleedBox set,
fills written as CMYK from the brand values of tokens.json.

    python3 -I tools/make_print_pdf.py print/zuil-abonnees-790x1400-wit-druk.svg [more.svg ...]

Needs: pymupdf, fonttools, playwright (node) with Chromium.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

import pymupdf
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FONTS = {("Ubuntu", False): "Ubuntu-Regular.ttf", ("Ubuntu", True): "Ubuntu-Bold.ttf", ("Ubuntu Medium", False): "Ubuntu-Medium.ttf",
         ("Ubuntu Light", False): "Ubuntu-Light.ttf"}
_cache = {}


def font(name, bold):
    key = (name, bold)
    if key not in _cache:
        tt = TTFont(os.path.join(ROOT, "fonts", FONTS[key]))
        _cache[key] = (tt, tt.getGlyphSet(), tt.getBestCmap(), tt["head"].unitsPerEm, tt["hmtx"])
    return _cache[key]


def outline_text(svg):
    def rep(m):
        attrs, body = m.group(1), m.group(2)
        g = dict(re.findall(r'([\w:-]+)="([^"]*)"', attrs))
        tt, gs, cmap, upm, hmtx = font(g["font-family"], g.get("font-weight") == "bold")
        size = float(g["font-size"])
        x, y = float(g["x"]), float(g["y"])
        ls = float(g.get("letter-spacing", 0))
        txt = body.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        sc = size / upm
        d = []
        for ch in txt:
            gn = cmap.get(ord(ch))
            if gn is None:
                continue
            pen = SVGPathPen(gs)
            gs[gn].draw(TransformPen(pen, (sc, 0, 0, -sc, x, y)))
            if pen.getCommands():
                d.append(pen.getCommands())
            x += hmtx[gn][0] * sc + ls
        extra = f' id="{g["id"]}"' if "id" in g else ""
        return f'<path d="{" ".join(d)}" fill="{g["fill"]}"{extra}/>'
    return re.sub(r"<text\b([^>]*)>([^<]*)</text>", rep, svg)


def cmyk_map():
    t = json.load(open(os.path.join(ROOT, "tokens.json"), encoding="utf8"))["colors"]
    out = {"#FFFFFF": (0, 0, 0, 0)}
    for k in ("py-tok-color-blauw", "py-tok-color-aqua", "py-tok-color-oranje", "py-tok-color-grijs", "py-tok-color-zwart"):
        c = t[k]
        if c.get("cmyk"):
            out[c["hex"].upper()] = tuple(v / 100 for v in c["cmyk"])
    return out


def to_cmyk(pdf_path, out_path, bleed_mm, width_mm, height_mm):
    doc = pymupdf.open(pdf_path)
    cm = cmyk_map()
    rgb = {tuple(round(int(h[i:i + 2], 16) / 255, 4) for i in (1, 3, 5)): v for h, v in cm.items()}
    done = 0
    for page in doc:
        for xref in page.get_contents():
            s = doc.xref_stream(xref).decode("latin-1")

            def rep(m):
                nonlocal done
                key = tuple(round(float(m.group(i)), 4) for i in (1, 2, 3))
                best = min(rgb, key=lambda k: sum((a - b) ** 2 for a, b in zip(k, key)))
                if sum((a - b) ** 2 for a, b in zip(best, key)) > 1e-4:
                    raise SystemExit(f"colour not in brand table: {key}")
                c, mm, y, k = rgb[best]
                done += 1
                return f"{c:.3f} {mm:.3f} {y:.3f} {k:.3f} " + ("k" if m.group(4) == "rg" else "K")

            s = re.sub(r"(-?[\d.]+) (-?[\d.]+) (-?[\d.]+) (rg|RG)\b", rep, s)
            doc.update_stream(xref, s.encode("latin-1"))
        pt = 72 / 25.4
        page.set_trimbox(pymupdf.Rect(bleed_mm * pt, bleed_mm * pt, (width_mm - bleed_mm) * pt, (height_mm - bleed_mm) * pt))
        page.set_bleedbox(page.mediabox)
    doc.save(out_path, garbage=4, deflate=True)
    return done


def main():
    for svg_path in sys.argv[1:]:
        svg_path = os.path.abspath(svg_path)
        svg = open(svg_path, encoding="utf8").read()
        w, h = (float(v) for v in re.search(r'width="([\d.]+)mm" height="([\d.]+)mm"', svg).groups())
        out_svg = outline_text(svg)
        assert "<text" not in out_svg
        tmp = tempfile.mkdtemp()
        html = os.path.join(tmp, "p.html")
        body = re.sub(r"<\?xml[^>]*>", "", out_svg).replace("<svg ", '<svg style="display:block" ', 1)
        open(html, "w").write(f"<!doctype html><meta charset=utf-8><style>@page{{size:{w}mm {h}mm;margin:0}}html,body{{margin:0}}</style>{body}")
        raw = os.path.join(tmp, "raw.pdf")
        js = os.path.join(tmp, "pdf.js")
        open(js, "w").write("""const {chromium}=require('/opt/node-tools/node_modules/playwright');
(async()=>{const [html,out,w,h]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+html);await p.pdf({path:out,width:w+'mm',height:h+'mm',printBackground:true,preferCSSPageSize:true,margin:{top:'0',right:'0',bottom:'0',left:'0'}});await b.close();})();""")
        subprocess.run(["node", js, html, raw, str(w), str(h)], check=True)
        out_pdf = svg_path[:-4] + ".pdf"
        n = to_cmyk(raw, out_pdf, 3.0, w, h)
        print("wrote", os.path.relpath(out_pdf, ROOT), f"{w} x {h} mm, {n} colour operators set to CMYK")


if __name__ == "__main__":
    main()
