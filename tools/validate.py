#!/usr/bin/env python3
"""Validate the bundle: PDF labels, SVG filenames and manifest IDs match one to one; colours; every SVG opens.

usage: python3 -I tools/validate.py [--root .] [--pdf overview/parkingyou-elementen-overzicht.pdf]
"""
import argparse, collections, glob, io, json, os, re, sys
import xml.etree.ElementTree as ET

import cairosvg
import pymupdf
from PIL import Image

ID_RE = re.compile(r"py-(?:tok|atom|comp|prod)-[a-z0-9]+(?:-[a-z0-9]+)*")
BRAND_HEX = {"#1A3580", "#32B9CD", "#F08300", "#AEAEAE", "#1D1D1B", "#FFFFFF"}
FUNCTIONAL = {"#C20016", "#3AAA35", "#53A043", "#008A3B", "#00913E", "#E30613", "#097BAE"}
FORBIDDEN = {"#1A3680", "#010101", "#082E7A", "#A0A1A0"}  # normalised away on purpose


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    ap.add_argument("--pdf", default=None)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    pdf = a.pdf or os.path.join(root, "overview", "parkingyou-elementen-overzicht.pdf")
    errs, warns = [], []

    man = json.load(open(os.path.join(root, "elements.json"), encoding="utf8"))
    man_ids = {e["id"] for e in man["elements"]}
    pdf_ids = {e["id"] for e in man["elements"] if e.get("origin") not in ("print", "design")}  # print additions have their own overview and validator; new designs (tools/build_zuil.py) are not in the handbook overview
    svg_files = sorted(glob.glob(os.path.join(root, "svg", "*", "*.svg")))
    svg_ids = {os.path.basename(f)[:-4] for f in svg_files}

    # ---- manifest <-> svg
    for i in sorted(man_ids - svg_ids):
        errs.append(f"manifest id without svg: {i}")
    for i in sorted(svg_ids - man_ids):
        errs.append(f"svg without manifest row: {i}")
    for e in man["elements"]:
        lvl = e["id"].split("-")[1]
        if not os.path.exists(os.path.join(root, "svg", lvl, e["id"] + ".svg")):
            errs.append(f"svg path wrong for {e['id']}")
        if e["level"] != lvl:
            errs.append(f"level mismatch {e['id']}")
        for b in e["built_from"]:
            if b not in man_ids:
                errs.append(f"{e['id']} built_from unknown id {b}")

    # ---- svg content
    cols_by = collections.defaultdict(set)
    n_ok = 0
    for f in svg_files:
        id_ = os.path.basename(f)[:-4]
        s = open(f, encoding="utf8").read()
        try:
            tree = ET.fromstring(s)
        except ET.ParseError as ex:
            errs.append(f"{id_}: invalid XML {ex}")
            continue
        for bad in ("<image", "<clipPath", "<mask", "<filter", "data:image"):
            if bad in s:
                errs.append(f"{id_}: contains {bad}")
        ns = "{http://www.w3.org/2000/svg}"
        gids = [g.get("id") for g in tree.iter(ns + "g") if g.get("id")]
        if id_ not in gids:
            errs.append(f"{id_}: no top-level group with its ID")
        for h in re.findall(r'(?:fill|stroke|stop-color)="(#[0-9A-Fa-f]{6})"', s):
            cols_by[id_].add(h.upper())
        for h in cols_by[id_] & FORBIDDEN:
            errs.append(f"{id_}: forbidden colour {h}")
        # opens and is not empty
        try:
            png = cairosvg.svg2png(bytestring=s.encode(), output_width=300, background_color="#808080")
            im = Image.open(io.BytesIO(png)).convert("L")
            ex = im.getextrema()
            if ex[0] == ex[1]:
                errs.append(f"{id_}: renders empty")
            else:
                n_ok += 1
        except Exception as ex:
            errs.append(f"{id_}: does not render ({ex})")
        vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
        if not vb:
            errs.append(f"{id_}: no viewBox")

    other = collections.defaultdict(list)
    for i, cs in cols_by.items():
        for c in cs - BRAND_HEX - FUNCTIONAL:
            other[c].append(i)
    # ---- pdf
    if os.path.exists(pdf):
        d = pymupdf.open(pdf)
        labels = set()
        ids_pdf = collections.Counter()
        for p in d:
            t = p.get_text()
            t = re.sub(r"-\n", "-", t)
            for m in ID_RE.findall(t):
                ids_pdf[m] += 1
        # label count: every ID appears as a label on its own page (plus once in the index lists)
        missing = sorted(pdf_ids - set(ids_pdf))
        unknown = sorted(set(ids_pdf) - man_ids)
        for i in missing:
            errs.append(f"PDF has no label for {i}")
        for i in unknown:
            errs.append(f"PDF label {i} not in manifest")
        for i, c in ids_pdf.items():
            if i in pdf_ids and c < 2:
                warns.append(f"{i}: found {c}x in PDF (expected label plus index entry)")
        for p in d:
            if p.rect.width < 1190 or p.rect.width > 1191 or p.rect.height < 841 or p.rect.height > 842:
                errs.append(f"page {p.number + 1} is not A3 landscape: {p.rect}")
            if p.get_images():
                errs.append(f"page {p.number + 1} contains raster images")
        fonts = collections.Counter()
        for p in d:
            for f in p.get_fonts(full=True):
                fonts[f[3]] += 1
                if f[1] in ("", None):
                    pass
        notemb = [f for f in fonts if not f.split("+")[0] or "+" not in f]
        for f in notemb:
            errs.append(f"PDF font not embedded as subset: {f}")
        print("PDF pages:", len(d), "fonts:", sorted(fonts))
    else:
        warns.append(f"no PDF at {pdf}")

    print(f"manifest {len(man_ids)} ids, svg {len(svg_ids)} files, {n_ok} render ok")
    print("non-brand colours present (review):", {c: len(v) for c, v in sorted(other.items(), key=lambda kv: -len(kv[1]))[:25]})
    for w in warns[:20]:
        print("WARN", w)
    for e in errs:
        print("ERROR", e)
    print(f"{len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
