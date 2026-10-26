#!/usr/bin/env python3
"""Build the PM-137 print additions: new atoms/components/products in svg/, applications/<id>/, applications.json,
the additions to elements.json and the `observed` section of tokens.json.

Sources are the eleven PDFs in source/print/. Specs live in tools/specs_print/ (one module registers its elements and applications).

usage: python3 -I tools/build_print.py [--spec REGEX] [--only REGEX]
"""
import argparse, importlib, json, os, pkgutil, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

from pyassets import registry  # noqa: E402
from pyassets import apps as apps_mod  # noqa: E402
from pyassets import printsrc  # noqa: E402
from pyassets.core import PRINT_NORMALISE, normalised, COLOR_NORMALISE  # noqa: E402
from pyassets.compose import Doc  # noqa: E402
import build_all  # noqa: E402

LEVELS = ["tok", "atom", "comp", "prod"]
PRINT_SOURCE_NOTE = "eleven print sources in source/print/ (PM-137)"

# sampled print colours that are not brand values (observed, never official). CMYK from the PDF content streams.
OBSERVED = [
    # id, name, CMYK %, files, used for
    ("py-obs-blauw-uitrit", "Blauw uitritbord", (100, 92.5, 19.2, 5.9), "15728501-1.pdf", "pill background"),
    ("py-obs-blauw-maashaven", "Blauw Maashaven", (100, 86, 21.2, 3.7), "Maashaven.pdf", "header, bars, logo, text"),
    ("py-obs-blauw-laadkabel", "Blauw laadkabel", (100, 85.9, 6.6, 0), "LaadKabel.pdf", "background"),
    ("py-obs-blauw-diefstal", "Blauw diefstalsticker en slagboombord", (100, 86.3, 21.5, 3.5), "StickerDiefstalARtisDruk.pdf, BordSlagboomEVO.pdf", "text, icon, footer, background"),
    ("py-obs-blauw-glow", "Blauw GLOW", (100, 84.4, 5.5, 0.4), "Tekengebied_1.pdf, Tekengebied_4_kopie_4.pdf", "background, text"),
    ("py-obs-blauw-rgb-1a3680", "Blauw RGB achtergrond", None, "Naamloos-7.pdf", "RGB only, #1A3680 (the vector blue replaced by #1A3580 in 1.3)"),
    ("py-obs-aqua-uitrit", "Aqua uitritbord", (67.8, 3.1, 19.2, 0), "15728501-1.pdf", "arrow and arc"),
    ("py-obs-aqua-licht", "Lichtaqua", (54, 0, 14, 0), "LaadKabel.pdf, StickerDiefstalARtisDruk.pdf, InfoPylonBordGoed.pdf", "icons on navy (plug, padlock), chevron"),
    ("py-obs-blauw-terminal", "Blauw terminalstickers", (99.5, 85, 21.4, 6.8), "TerminalStickers_September2026.pdf", "text, icons, badges, bars (also 99.6/84/21.3/6.6 and 100/86.4/21.4/3.7 on single stickers)"),
    ("py-obs-grijs-qrplaat", "Lichtgrijs QR plaat", (8.4, 5.8, 6.9, 0), "TerminalStickers_September2026.pdf", "QR plates of the phone, reader and subscription card illustrations (at 90 percent opacity)"),
    ("py-obs-zwart-rijk", "Rijk zwart", (91.2, 78.7, 62, 97.4), "Maashaven.pdf", "small text"),
    # second batch
    ("py-obs-blauw-briefpapier-tekst", "Blauw adresblok briefpapier", (100, 85.5, 22.3, 4), "Briefpapier_nieuw.pdf", "address text"),
    ("py-obs-magenta-gaten", "Magenta montagegaten", (0, 93.4, 7.2, 0), "BordSlagboomEVO.pdf", "two 1 pt rings (mounting holes), not a spot colour"),
    ("py-obs-blauw-rgb-pr", "Blauw RGB P+R bord", None, "PR_RoadSignage.pdf", "background and text, RGB (ICC) only", "#273A7C"),
    ("py-obs-blauw-rgb-pr-logo", "Blauw RGB P+R bord logo", None, "PR_RoadSignage.pdf", "logo and partner text, RGB (ICC) only", "#213A8F"),
    ("py-obs-blauw-rgb-envelop", "Blauw RGB envelop", None, "ParkingYou_Envelop_220x156.pdf", "logo and address, RGB (ICC) only (file claims PDF/X-1a)", "#223A7A"),
    ("py-obs-blauw-rgb-tarief", "Blauw RGB tariefbord", None, "TariefConcerten.pdf", "background and text, RGB (ICC) only", "#23398E"),
    ("py-obs-aqua-rgb-envelop", "Aqua RGB envelop", None, "ParkingYou_Envelop_220x156.pdf, PR_RoadSignage.pdf", "tagline, dot; RGB (ICC)", "#34BACE"),
    ("py-obs-aqua-licht-rgb", "Lichtaqua RGB", None, "TariefConcerten.pdf, PR_WTC_Sticker.pdf, PR_WTC_Poster.pdf", "price bubble, RGB (ICC) only", "#78C9DC"),
    # third batch
    ("py-obs-blauw-dranghek", "Blauw dranghekspandoek", (100, 85, 10, 1), "dranghekspandoek-dubbelzijdig_01.pdf", "background, figure text"),
    ("py-obs-aqua-licht-dranghek", "Lichtaqua dranghekspandoek", (51, 1, 11, 0), "dranghekspandoek-dubbelzijdig_01.pdf", "pill, triangle, divider, keyword"),
    ("py-obs-blauw-rgb-wtc", "Blauw RGB P+R sticker en poster", None, "PR_WTC_Sticker.pdf, PR_WTC_Poster.pdf", "background and text, RGB (ICC) only", "#233A89"),
    ("py-obs-blauw-rgb-poster-a3", "Blauw RGB poster A3", None, "posters_297x420_3_1.pdf", "text and icons, RGB (ICC sRGB) only", "#2B3D91"),
    ("py-obs-blauw-rgb-poster-a2", "Blauw RGB poster A2", None, "posters_420x594_3_1.pdf", "text and QR plate, RGB (ICC sRGB) only", "#2A3282"),
    # fourth batch (partner package slide)
    ("py-obs-blauw-rgb-partner", "Blauw RGB partnerpakket", None, "MarketingCampagne_ParkingYouPartner.pdf", "poster, flyers, stickers, RGB (ICC) only, vivid royal blue", "#192AA2"),
    ("py-obs-cyaan-rgb-partner", "Cyaan RGB partnerpakket", None, "MarketingCampagne_ParkingYouPartner.pdf", "beeldmerk dot, flyer panel, bright cyan, not PY-Aqua", "#0AD3E6"),
    ("py-obs-oranje-rgb-partner", "Oranje RGB partnerpakket", None, "MarketingCampagne_ParkingYouPartner.pdf", "price and keyword; close to PY-Oranje (#F08300)", "#FF8401"),
    ("py-obs-grijs-licht-sticker", "Lichtgrijs stickerbasis", None, "MarketingCampagne_ParkingYouPartner.pdf", "window sticker body, flat grey in the mock-up (raster in source), template placeholder", "#F0F0F0"),
    ("py-obs-grijs-nfc-schijf", "Grijs NFC schijf", None, "MarketingCampagne_ParkingYouPartner.pdf", "NFC sticker disc, flat grey in the mock-up (raster in source), template placeholder", "#E1E1E1"),
]
TOKEN_CMYK = {"blauw": (100, 83, 0, 17), "aqua": (69, 0, 21, 0)}
OBS_HEX = {"#78C9DC": "py-obs-aqua-licht-rgb", "#79C9DC": "py-obs-aqua-licht-rgb", "#71CBDF": "py-obs-aqua-licht-dranghek", "#83CBE1": "py-obs-aqua-licht-rgb", "#8CCDDF": "py-obs-aqua-licht-rgb", "#68CBDB": "py-obs-aqua-licht", "#69CADA": "py-obs-aqua-licht", "#68CBDA": "py-obs-aqua-licht", "#7CCBDD": "py-obs-aqua-licht", "#E6E7E6": "py-obs-grijs-qrplaat"}


def load_specs(only=None):
    sd = os.path.join(HERE, "specs_print")
    sys.path.insert(0, sd)
    for m in sorted(pkgutil.iter_modules([sd]), key=lambda m: m.name):
        if only and not re.search(only, m.name):
            continue
        importlib.import_module(m.name)


def fogra_hex(cmyk):
    """sRGB via the FOGRA39 output-intent profile embedded in 15728501-1.pdf."""
    try:
        import io
        from PIL import Image, ImageCms
        import pymupdf

        global _T
        if "_T" not in globals():
            d = pymupdf.open(os.path.join(printsrc.DIR, "15728501-1.pdf"))
            oi = d.xref_get_key(d.pdf_catalog(), "OutputIntents")
            xr = None
            for x in range(1, d.xref_length()):
                o = d.xref_object(x, compressed=True)
                if "/OutputConditionIdentifier" in o and "FOGRA39" in o:
                    m = re.search(r"/DestOutputProfile (\d+) 0 R", o)
                    xr = int(m.group(1))
            prof = ImageCms.ImageCmsProfile(io.BytesIO(d.xref_stream(xr)))
            _T = ImageCms.buildTransform(prof, ImageCms.createProfile("sRGB"), "CMYK", "RGB", renderingIntent=1)
        im = Image.new("CMYK", (1, 1), tuple(round(v * 2.55) for v in cmyk))
        return "#%02X%02X%02X" % ImageCms.applyTransform(im, _T).getpixel((0, 0))
    except Exception:
        return None


def write_observed(root):
    p = os.path.join(root, "tokens.json")
    t = json.load(open(p, encoding="utf8"))
    obs = {
        "note": ("Colours sampled from the eleven print files in source/print/. They are NOT brand values and never replace the official tokens. "
                 "Native print values are CMYK; hex_viewer is the sRGB a PDF viewer shows, hex_fogra39 the sRGB through the FOGRA39 profile. "
                 "Official blauw is CMYK 100/83/0/17 (#1A3580); four files use exactly that, the rest (the terminal sticker sheet included) drift as listed."),
        "colors": {},
    }
    for rec in OBSERVED:
        oid, name, cmyk, files, use = rec[:5]
        row = {"name": name, "files": files, "used_for": use, "kind": "observed"}
        if cmyk:
            row["cmyk"] = list(cmyk)
            row["hex_fogra39"] = fogra_hex(cmyk)
            ref = TOKEN_CMYK["blauw"] if "blauw" in oid else (TOKEN_CMYK["aqua"] if "aqua" in oid else None)
            if ref:
                row["delta_to_token_cmyk"] = [round(a - b, 1) for a, b in zip(cmyk, ref)]
        else:
            hx = rec[5] if len(rec) > 5 else "#1A3680"
            row["rgb"] = [int(hx[i:i + 2], 16) for i in (1, 3, 5)]
            row["hex_viewer"] = hx
        obs["colors"][oid] = row
    t["observed"] = obs
    json.dump(t, open(p, "w", encoding="utf8"), indent=1, ensure_ascii=False)


def level_order(id_):
    return LEVELS.index(id_.split("-")[1])


def build_elements(only):
    pat = re.compile(only)
    ids = sorted((i for i, m in registry.META.items() if m.get("src") and pat.search(i)), key=lambda i: (level_order(i), i))
    rows, pending, problems = {}, list(ids), []
    with normalised(PRINT_NORMALISE):
        for rnd in range(4):
            nxt = []
            for id_ in pending:
                meta = registry.META[id_]
                try:
                    el = registry.build(printsrc.source(meta["src"]), id_)
                except FileNotFoundError as e:
                    nxt.append(id_)
                    continue
                w, h = el.size_mm()
                os.makedirs(os.path.join(ROOT, "svg", el.level), exist_ok=True)
                with open(os.path.join(ROOT, "svg", el.level, id_ + ".svg"), "w", encoding="utf8") as f:
                    f.write(el.svg())
                rows[id_] = (el, w, h, meta)
            pending = nxt
            if not pending:
                break
        for id_ in pending:
            problems.append((id_, "dependency not built"))
    return rows, problems


def element_row(id_, el, w, h, meta):
    cols = []
    for c in el.colors():
        if c == "gradient-verloop":
            cols.append({"token": "py-tok-gradient-verloop", "hex": None})
        else:
            cols.append({"token": build_all.BRAND_TOKEN.get(c) or OBS_HEX.get(c), "hex": c})
    notes = (el.notes or "").strip()
    srcinfo = printsrc.SOURCES[meta["src"]]
    return {
        "id": id_, "name_nl": el.name_nl, "level": el.level, "category": el.category,
        "source_page": el.page, "source_file": srcinfo["file"], "origin": "print", "status": el.status,
        "dimensions_mm": {"width": round(w, 1), "height": round(h, 1),
                          "stated": list(el.dims_mm) if el.dims_mm else None,
                          "basis": "print scale (1:1 from source)" if el.level != "tok" else "n/a"},
        "colors": cols, "variables": list(el.variables or []), "built_from": list(el.built_from or []),
        "tags": list(el.tags or []), "notes": notes, "svg": f"svg/{el.level}/{id_}.svg",
    }


class Ctx:
    """Passed to application builders."""

    def __init__(self, app_id):
        self.app_id = app_id
        self.Doc = Doc
        self.SOURCES = printsrc.SOURCES

    def reference(self, key, pno=1, variant="", **kw):
        return printsrc.reference_svg(self.app_id, key, pno, variant, **kw)

    def piece_reference(self, key, seq_ranges, origin_mm, scale, trim_mm, pno=1, variant="", **kw):
        """Mock-up piece from a presentation slide, scaled to real size (see printsrc.piece_reference_svg)."""
        return printsrc.piece_reference_svg(self.app_id, key, seq_ranges, origin_mm, scale, trim_mm, pno, variant, **kw)


def build_apps(only):
    pat = re.compile(only)
    out_rows, problems = [], []
    for id_ in sorted(apps_mod.APPS):
        if not pat.search(id_):
            continue
        meta = apps_mod.APP_META[id_]
        ctx = Ctx(id_)
        try:
            res = apps_mod.APPS[id_](ctx)
        except Exception as e:  # report, keep going
            import traceback

            traceback.print_exc()
            problems.append((id_, repr(e)))
            continue
        d = os.path.join(ROOT, "applications", id_)
        os.makedirs(d, exist_ok=True)
        variants = meta["variants"]
        files = {"reference": {}, "template": {}}
        built = []
        variables = {}
        vbf = {}
        for v in variants:
            sfx = f"-{v}" if v else ""
            ref = res["reference"][v]
            tpl = res["template"][v]
            fn_r, fn_t = f"reference{sfx}.svg", f"template{sfx}.svg"
            open(os.path.join(d, fn_r), "w", encoding="utf8").write(ref)
            vid = id_ + sfx
            tsvg = tpl.svg(group_id=f"{vid}-template") if hasattr(tpl, "svg") else tpl
            open(os.path.join(d, fn_t), "w", encoding="utf8").write(tsvg)
            files["reference"][v or "default"] = fn_r
            files["template"][v or "default"] = fn_t
            vbf[v or "default"] = list(getattr(tpl, "built_from", []))
            if hasattr(tpl, "built_from"):
                for b in tpl.built_from:
                    if b not in built:
                        built.append(b)
                variables[v or "default"] = dict(tpl.variables)
            else:
                variables[v or "default"] = res.get("variables", {}).get(v, {})
        for b in res.get("built_from", []):
            if b not in built:
                built.append(b)
        tw_, th_ = meta["trim_mm"]
        bl = meta["bleed_mm"]
        srcs = meta["source"]
        first = printsrc.SOURCES[srcs[0][0]] if srcs and srcs[0][0] in printsrc.SOURCES else {}
        spec = {
            "id": id_, "name_nl": meta["name_nl"], "type": meta["type"], "origin": "print",
            "variants": [{"id": id_ + (f"-{v}" if v else ""), "variant": v or None,
                          "reference": files["reference"][v or "default"], "template": files["template"][v or "default"],
                          "built_from": vbf.get(v or "default", [])} for v in variants],
            "source": dict({"files": [{"file": "source/print/" + printsrc.SOURCES[k]["file"], "pages": pg,
                                       "colour_space": printsrc.SOURCES[k]["cs"], "trim_mm": list(printsrc.SOURCES[k]["trim_mm"]),
                                       "bleed_box_set": printsrc.SOURCES[k]["bleed_set"]} for k, pg in srcs]},
                           **({"region_references": True} if meta.get("region_references") else {})),
            "template": {"trim_mm": [tw_, th_], "bleed_mm": bl, "size_with_bleed_mm": [tw_ + 2 * bl, th_ + 2 * bl],
                         "colour": "RGB hex from tokens.json (official tokens); print values (CMYK) are in tokens.json",
                         "cut_contour": meta["cut_contour"]},
            "reference_note": ("Faithful vector reproduction of one sticker of the source sheet, cut out with 1.5 mm margin (source colours as a viewer shows them, original copy including typos). Hidden leftovers are listed under omitted."
                               if meta.get("region_references") else
                               "Faithful vector reproduction of the source page (source colours as a viewer shows them, original copy including typos). Hidden leftovers are listed under omitted."),
            "variables": variables,
            "built_from": built,
            "status": meta["status"],
            "tags": meta["tags"],
            "reference_scope": meta.get("reference_scope", "page"),
            "omitted": res.get("omitted", []),
            "copy_corrections": res.get("copy_corrections", []),
            "notes": res.get("notes", meta.get("notes", "")),
        }
        json.dump(spec, open(os.path.join(d, "spec.json"), "w", encoding="utf8"), indent=1, ensure_ascii=False)
        out_rows.append(spec)
    return out_rows, problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default=None)
    ap.add_argument("--only", default=".*")
    ap.add_argument("--no-json", action="store_true", help="do not touch elements.json, tokens.json, applications.json")
    a = ap.parse_args()
    load_specs(a.spec)
    rows, p1 = build_elements(a.only)
    arows, p2 = build_apps(a.only)
    for id_, (el, w, h, meta) in sorted(rows.items(), key=lambda kv: (level_order(kv[0]), kv[0])):
        print(f"{id_:55s} {w:7.1f} x {h:6.1f} mm  {el.status:9s} {len(el.built_from or [])} built_from")
    for s in arows:
        print(f"{s['id']:55s} app, {len(s['variants'])} variant(s), built_from {len(s['built_from'])}")
    if not a.no_json and a.spec is None and a.only == ".*":
        mp = os.path.join(ROOT, "elements.json")
        m = json.load(open(mp, encoding="utf8"))
        keep = [e for e in m["elements"] if e.get("origin") != "print"]
        new = [element_row(i, *rows[i][:3], rows[i][3]) for i in rows]
        els = keep + new
        els.sort(key=lambda e: (LEVELS.index(e["level"]), e["id"]))
        m["elements"], m["count"] = els, len(els)
        m["print_sources"] = sorted({s["file"] for s in printsrc.SOURCES.values()})
        json.dump(m, open(mp, "w", encoding="utf8"), indent=1, ensure_ascii=False)
        write_observed(ROOT)
        arows.sort(key=lambda s: s["id"])
        json.dump({"source": PRINT_SOURCE_NOTE, "count": len(arows), "applications": arows},
                  open(os.path.join(ROOT, "applications.json"), "w", encoding="utf8"), indent=1, ensure_ascii=False)
        print(len(new), "new elements,", len(arows), "applications written")
    for pr in p1 + p2:
        print("PROBLEM", pr)
    sys.exit(1 if (p1 or p2) else 0)


if __name__ == "__main__":
    main()
