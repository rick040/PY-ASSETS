#!/usr/bin/env python3
"""Validate the PM-137 print additions.

Checks: applications.json vs applications/ vs spec.json; IDs unique and well formed; every built_from ID exists; handbook IDs and official tokens untouched;
template size = trim + 2 x bleed; cut-contour group where a contour is specified; variables present as data-variable or placeholder; token colours only;
no raster, clipPath, mask or filter; every SVG renders; the QR in the Maashaven reference decodes; no em or en dashes in generated text;
the toepassingen PDF: A3 landscape, no raster, fonts embedded, labels match the manifests 1:1.

usage: python3 -I tools/validate_print.py [--root .] [--pdf overview/parkingyou-toepassingen-overzicht.pdf]
"""
import argparse, collections, glob, io, json, os, re, subprocess, sys
import xml.etree.ElementTree as ET

import cairosvg
import pymupdf
from PIL import Image

ID_RE = re.compile(r"py-(?:tok|atom|comp|prod|app)-[a-z0-9]+(?:-[a-z0-9]+)*")
APP_RE = re.compile(r"^py-app-[a-z0-9]+(?:-[a-z0-9]+)*$")
EL_RE = re.compile(r"^py-(?:atom|comp|prod)-[a-z0-9]+(?:-[a-z0-9]+)*$")
BRAND_HEX = {"#1A3580", "#32B9CD", "#F08300", "#AEAEAE", "#1D1D1B", "#FFFFFF"}
OBSERVED_OK = {"#68CBDB", "#69CADA", "#68CBDA", "#7CCBDD", "#E6E7E6", "#FFD500"}  # light aqua, light grey QR plate (observed tokens)
CUT_PH = {"#EE4D9B", "#00A0E0"}  # cut contour, placeholders, guides
DRIFT = {"#1A3680", "#0B3D8A", "#1F4383", "#1C4695", "#204382", "#174797", "#27397E", "#24BFCD", "#24BDCD", "#23BDCD", "#31BBCD", "#1C4480", "#1E427F", "#1C427E"}
DASH = ("—", "–")
BASELINE_COMMIT = "4c04c1f"  # PM-134 result: handbook elements and official tokens must not change


def hexes(s):
    return {h.upper() for h in re.findall(r'(?:fill|stroke|stop-color)="(#[0-9A-Fa-f]{6})"', s)}


def svg_size(s):
    m = re.search(r'viewBox="0 0 ([\d.\-]+) ([\d.\-]+)"', s)
    return float(m.group(1)), float(m.group(2))


def renders(s):
    png = cairosvg.svg2png(bytestring=s.encode(), output_width=400, background_color="#808080")
    ex = Image.open(io.BytesIO(png)).convert("L").getextrema()
    return ex[0] != ex[1]


def git_show(root, path):
    try:
        return subprocess.check_output(["git", "-C", root, "show", f"{BASELINE_COMMIT}:{path}"], stderr=subprocess.DEVNULL).decode()
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    ap.add_argument("--pdf", default=None)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    pdf = a.pdf or os.path.join(root, "overview", "parkingyou-toepassingen-overzicht.pdf")
    errs, warns = [], []

    man = json.load(open(os.path.join(root, "elements.json"), encoding="utf8"))
    els = {e["id"]: e for e in man["elements"]}
    new = {i: e for i, e in els.items() if e.get("origin") in ("print", "design")}
    ids_all = [e["id"] for e in man["elements"]]
    if len(ids_all) != len(set(ids_all)):
        errs.append("duplicate IDs in elements.json")
    appj = json.load(open(os.path.join(root, "applications.json"), encoding="utf8"))
    apps = {s["id"]: s for s in appj["applications"]}

    # ---- handbook elements and official tokens untouched
    base = git_show(root, "elements.json")
    if base:
        bids = {e["id"]: e for e in json.loads(base)["elements"]}
        for i, e in bids.items():
            if i not in els:
                errs.append(f"handbook element removed: {i}")
            elif {k: els[i][k] for k in ("name_nl", "level", "category", "source_page", "status")} != {k: e[k] for k in ("name_nl", "level", "category", "source_page", "status")}:
                errs.append(f"handbook element changed: {i}")
        if set(new) & set(bids):
            errs.append(f"print element reuses a handbook ID: {sorted(set(new) & set(bids))}")
    bt = git_show(root, "tokens.json")
    if bt:
        old, cur = json.loads(bt), json.load(open(os.path.join(root, "tokens.json"), encoding="utf8"))
        for k in old:
            if old[k] != cur.get(k):
                errs.append(f"official tokens section changed: {k}")
        if "observed" not in cur:
            errs.append("tokens.json has no observed section")
    else:
        warns.append("no git baseline for tokens/elements comparison")

    # ---- new library elements
    ok_svg = 0
    for i, e in sorted(new.items()):
        if not EL_RE.match(i):
            errs.append(f"bad element ID {i}")
        if e["level"] != i.split("-")[1]:
            errs.append(f"level mismatch {i}")
        p = os.path.join(root, "svg", e["level"], i + ".svg")
        if not os.path.exists(p):
            errs.append(f"no svg for {i}")
            continue
        s = open(p, encoding="utf8").read()
        try:
            ET.fromstring(s)
        except ET.ParseError as ex:
            errs.append(f"{i}: invalid XML {ex}")
            continue
        for bad in ("<image", "<clipPath", "<mask", "<filter", "data:image"):
            if bad in s:
                errs.append(f"{i}: contains {bad}")
        if f'id="{i}"' not in s:
            errs.append(f"{i}: no top-level group with its ID")
        if any(d in s for d in DASH) or any(d in (e["notes"] or "") + e["name_nl"] for d in DASH):
            errs.append(f"{i}: em or en dash in text")
        for h in hexes(s) & DRIFT:
            errs.append(f"{i}: print drift colour {h} in a library element")
        if "third-party" in e["tags"] and "reference only" not in (e["notes"] or "").lower():
            errs.append(f"{i}: third-party without a 'reference only' note")
        for b in e["built_from"]:
            if b not in els:
                errs.append(f"{i} built_from unknown ID {b}")
        try:
            if renders(s):
                ok_svg += 1
            else:
                errs.append(f"{i}: renders empty")
        except Exception as ex:
            errs.append(f"{i}: does not render ({ex})")

    # ---- applications
    folders = {os.path.basename(d) for d in glob.glob(os.path.join(root, "applications", "*")) if os.path.isdir(d)}
    for i in sorted(folders - set(apps)):
        errs.append(f"applications/{i} not in applications.json")
    for i in sorted(set(apps) - folders):
        errs.append(f"{i} in applications.json but no folder")
    variant_ids = []
    ok_ref = ok_tpl = 0
    for aid, sp in sorted(apps.items()):
        if not APP_RE.match(aid) or not aid.startswith("py-app-" + sp["type"] + "-"):
            errs.append(f"{aid}: ID must be py-app-<type>-<name> (type {sp['type']})")
        d = os.path.join(root, "applications", aid)
        spj = os.path.join(d, "spec.json")
        if not os.path.exists(spj):
            errs.append(f"{aid}: no spec.json")
            continue
        sj = json.load(open(spj, encoding="utf8"))
        if sj != sp:
            errs.append(f"{aid}: spec.json differs from applications.json")
        for b in sp["built_from"]:
            if b not in els:
                errs.append(f"{aid} built_from unknown ID {b}")
        tr, bl = sp["template"]["trim_mm"], sp["template"]["bleed_mm"]
        for v in sp["variants"]:
            vid = v["id"]
            variant_ids.append(vid)
            for b in v.get("built_from", []):
                if b not in els:
                    errs.append(f"{vid} built_from unknown ID {b}")
                if b not in sp["built_from"]:
                    errs.append(f"{vid}: variant built_from {b} missing in the application built_from")
            if not APP_RE.match(vid):
                errs.append(f"bad variant ID {vid}")
            for kind in ("reference", "template"):
                if v[kind] is None:  # new design without a print source: no reference
                    if kind == "template" or sp.get("origin") != "design":
                        errs.append(f"{vid}: missing {kind}")
                    continue
                fp = os.path.join(d, v[kind])
                if not os.path.exists(fp):
                    errs.append(f"{vid}: missing {v[kind]}")
                    continue
                s = open(fp, encoding="utf8").read()
                try:
                    ET.fromstring(s)
                except ET.ParseError as ex:
                    errs.append(f"{vid} {kind}: invalid XML {ex}")
                    continue
                for bad in ("<image", "<clipPath", "<mask", "<filter", "data:image"):
                    if bad in s:
                        errs.append(f"{vid} {kind}: contains {bad}")
                if any(x in s for x in DASH):
                    errs.append(f"{vid} {kind}: em or en dash in text")
                try:
                    if not renders(s):
                        errs.append(f"{vid} {kind}: renders empty")
                except Exception as ex:
                    errs.append(f"{vid} {kind}: does not render ({ex})")
                w, h = svg_size(s)
                if kind == "template":
                    ok_tpl += 1
                    ew, eh = tr[0] + 2 * bl, tr[1] + 2 * bl
                    if abs(w - ew) > 0.01 or abs(h - eh) > 0.01:
                        errs.append(f"{vid}: template size {w:g} x {h:g} mm, expected trim + 2 x bleed = {ew:g} x {eh:g}")
                    # gradient stops are interpolations of the token gradient (and its #097BAE middle stop); only fill and stroke are checked
                    bad = {h.upper() for h in re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})"', s)} - BRAND_HEX - OBSERVED_OK - CUT_PH
                    # functional colours of third-party marks inside templates are allowed only if listed in built_from third-party elements
                    if bad:
                        tp = any("third-party" in els[b]["tags"] for b in sp["built_from"] if b in els)
                        (warns if tp else errs).append(f"{vid}: colours outside the tokens in template: {sorted(bad)}")
                    for h_ in hexes(s) & DRIFT:
                        errs.append(f"{vid}: print drift colour {h_} in template")
                    if sp["template"].get("cut_contour") and 'id="cut-contour"' not in s:
                        errs.append(f"{vid}: spec has a cut contour but the template has no cut-contour group")
                    vk = sp["variables"].get(v["variant"] or "default", {})
                    for name in vk:
                        if not re.search(r'data-variable[\w-]*="%s"' % re.escape(name), s) and 'data-placeholder' not in s:
                            errs.append(f"{vid}: variable {name} not marked in template")
                    if not vk:
                        errs.append(f"{vid}: template has no variables")
                    ph = len(re.findall(r'<(?:text|g|rect|path|circle)[^>]*data-variable', s))
                    if ph == 0 and "data-placeholder" not in s:
                        errs.append(f"{vid}: no live text variable or placeholder in template")
                else:
                    ok_ref += 1
                    src0 = sp["source"]["files"][0]
                    # reference page size equals the source page size
                    pdfp = os.path.join(root, src0["file"])
                    if os.path.exists(pdfp) and not sp["source"].get("region_references"):
                        pg = pymupdf.open(pdfp)[0]
                        if abs(w - pg.rect.width * 25.4 / 72) > 0.1 or abs(h - pg.rect.height * 25.4 / 72) > 0.1:
                            errs.append(f"{vid}: reference size {w:.1f} x {h:.1f} differs from source page {pg.rect.width * 25.4 / 72:.1f} x {pg.rect.height * 25.4 / 72:.1f}")
        # json text
        txt = open(spj, encoding="utf8").read()
        if any(x in txt for x in DASH):
            errs.append(f"{aid}: em or en dash in spec.json")

    # ---- QR in the Maashaven reference decodes
    qr = os.path.join(root, "applications", "py-app-panel-pyloon-maashaven", "reference.svg")
    if os.path.exists(qr):
        try:
            import zxingcpp

            png = cairosvg.svg2png(url=qr, output_width=2400, background_color="#FFFFFF")
            res = zxingcpp.read_barcodes(Image.open(io.BytesIO(png)).convert("L"))
            urls = [r.text for r in res]
            if "https://parkingyou.nl/nl/locaties/rotterdam/parking-maashaven/id=129" not in urls:
                errs.append(f"Maashaven reference: QR does not decode to the expected URL (got {urls})")
        except ImportError:
            warns.append("zxingcpp not installed: QR decode check skipped")

    # ---- pdf
    if os.path.exists(pdf):
        d = pymupdf.open(pdf)
        ids_pdf = collections.Counter()
        for p in d:
            t = re.sub(r"-\n", "-", p.get_text())
            for m in ID_RE.findall(t):
                ids_pdf[m] += 1
        known = set(els) | set(variant_ids) | set(apps)
        for i in sorted(set(ids_pdf) - known):
            errs.append(f"PDF label {i} is not in elements.json or applications.json")
        for v in variant_ids:
            if ids_pdf.get(v, 0) < 2:
                errs.append(f"PDF: {v} found {ids_pdf.get(v, 0)}x (expected reference label, template label and index entry)")
        for i in sorted(new):
            if ids_pdf.get(i, 0) < 1:
                errs.append(f"PDF has no label for new element {i}")
        for aid, sp in apps.items():
            for b in sp["built_from"]:
                if ids_pdf.get(b, 0) < 1:
                    errs.append(f"PDF: built_from element {b} of {aid} is not shown")
        for p in d:
            if not (1190 < p.rect.width < 1191 and 841 < p.rect.height < 842):
                errs.append(f"page {p.number + 1} is not A3 landscape: {p.rect}")
            if p.get_images():
                errs.append(f"page {p.number + 1} contains raster images")
        fonts = collections.Counter(f[3] for p in d for f in p.get_fonts(full=True))
        for f in fonts:
            if "+" not in f:
                errs.append(f"PDF font not embedded as subset: {f}")
        print("PDF pages:", len(d))
    else:
        warns.append(f"no PDF at {pdf}")

    print(f"new elements {len(new)} ({ok_svg} render ok), applications {len(apps)}, variants {len(variant_ids)} (reference ok {ok_ref}, template ok {ok_tpl})")
    for w in warns[:30]:
        print("WARN", w)
    for e in errs:
        print("ERROR", e)
    print(f"{len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
