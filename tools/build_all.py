#!/usr/bin/env python3
"""Build the whole bundle: svg/<level>/<id>.svg, elements.json, tokens.json, reports.

usage: python3 -I tools/build_all.py --src source/handbook.pdf [--spec REGEX] [--only REGEX]
"""
import argparse, fnmatch, importlib, json, os, pkgutil, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

from pyassets import BRAND, Source, registry  # noqa: E402
from pyassets.core import NORMALISE_LOG  # noqa: E402

BRAND_TOKEN = {"#1A3580": "py-tok-color-blauw", "#32B9CD": "py-tok-color-aqua", "#F08300": "py-tok-color-oranje",
               "#AEAEAE": "py-tok-color-grijs", "#1D1D1B": "py-tok-color-zwart", "#FFFFFF": "py-tok-color-wit",
               "#C20016": "py-tok-color-reflective-red", "#3AAA35": "py-tok-color-led-green", "#53A043": "py-tok-color-led-green",
               "#008A3B": "py-tok-color-safety-green", "#E30613": "py-tok-color-rvv-red"}

CMYK = {"blauw": (100, 83, 0, 17), "aqua": (69, 0, 21, 0), "oranje": (0, 57, 100, 0), "grijs": (0, 0, 0, 42), "zwart": (0, 0, 0, 100)}
RAL = {"blauw": "5002", "aqua": "6027", "oranje": "2003", "grijs": "9006", "zwart": "9005"}


def load_specs(only=None):
    sd = os.path.join(HERE, "specs")
    sys.path.insert(0, sd)
    for m in sorted(pkgutil.iter_modules([sd]), key=lambda m: m.name):
        if only and not re.search(only, m.name):
            continue
        importlib.import_module(m.name)


# ---------------------------------------------------------------- inventory (variables, built_from, product specs)
def parse_inventory():
    txt = open(os.path.join(ROOT, "docs", "phase1-inventory.md"), encoding="utf8").read()
    rows = {}
    for line in txt.splitlines():
        m = re.match(r"\| (py-(?:tok|atom|comp|prod)-[a-z0-9-]+) \|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        id_ = cells[0]
        level = id_.split("-")[1]
        if level == "prod":
            rows[id_] = dict(name=cells[1], page=cells[2], spec=cells[5], variables=cells[6], built_from=cells[7])
        else:
            rows[id_] = dict(name=cells[1], desc=cells[2], page=cells[3], variables=cells[6], built_from=cells[7])
    return rows


def resolve(tokens, ids, level_of):
    """Turn short names from the inventory (e.g. 'picto-*', 'bubble-solid') into registered IDs."""
    out, unresolved = [], []
    for raw in re.split(r",", tokens):
        t = raw.strip().lower()
        t = re.sub(r"^(as .*|same.*|none.*|geen.*)$", "", t)
        t = re.sub(r"\(.*?\)", "", t).strip()
        if not t or t in ("none", "geen"):
            continue
        t = re.sub(r"^(atom|comp|prod|tok)-", "", t)
        found = []
        for i in ids:
            suf = i.split("-", 2)[2]
            if "*" in t:
                if fnmatch.fnmatch(suf, t) or fnmatch.fnmatch(suf, "*" + t):
                    found.append(i)
            elif suf == t or suf.endswith("-" + t) or i == t:
                found.append(i)
        if len(found) > 1:  # prefer the exact suffix
            ex = [i for i in found if i.split("-", 2)[2] == t]
            found = ex or found
        if found:
            out += [f for f in found if f not in out]
        else:
            unresolved.append(t)
    return out, unresolved


def hex_rgb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def write_tokens(out):
    from pyassets.core import GRADIENT_STOPS
    colors = {}
    names = {"blauw": "PY-Blauw", "aqua": "PY-Aqua", "oranje": "PY-Oranje", "grijs": "PY-Grijs", "zwart": "PY-Zwart"}
    for k, hx in (("blauw", "#1A3580"), ("aqua", "#32B9CD"), ("oranje", "#F08300"), ("grijs", "#AEAEAE"), ("zwart", "#1D1D1B")):
        colors[f"py-tok-color-{k}"] = {"name": names[k], "hex": hx, "rgb": hex_rgb(hx), "cmyk": list(CMYK[k]),
                                       "ral": RAL[k], "ral_note": "best match only, does NOT match the huisstijlkleur exactly (handbook p8)",
                                       "source_page": 8, "kind": "brand"}
    obs = {"wit": ("#FFFFFF", "Wit", "diapositief logo and white signing"),
           "ral-9010": ("#FFFFFF", "RAL 9010 (hoogtebalk)", "mentioned on p22 only; drawn white; no official sRGB"),
           "reflective-red": ("#C20016", "Rode reflecterende band", "post bands p43, p44; not a brand colour"),
           "led-green": ("#3AAA35", "LED groen", "display dots p12 to p25 (also #53A043); not a brand colour"),
           "safety-green": ("#008A3B", "Veiligheidsgroen", "escape plan p35 (also #00913E); not a brand colour"),
           "rvv-red": ("#E30613", "RVV rood", "third-party RVV signs p51")}
    for k, (hx, nm, note) in obs.items():
        colors[f"py-tok-color-{k}"] = {"name": nm, "hex": hx, "rgb": hex_rgb(hx), "cmyk": None, "ral": "9010" if k == "ral-9010" else None,
                                       "source_page": None, "kind": "observed", "note": note}
    grad = {}
    for k, kind, direction in (("verloop", "diag", "top-left to bottom-right (45 degrees)"), ("verloop-vertical", "vert", "top to bottom"), ("verloop-horizontal", "horiz", "left to right")):
        grad[f"py-tok-gradient-{k}"] = {"kind": "linear", "direction": direction,
                                        "stops": [{"offset": o, "hex": h} for o, h in GRADIENT_STOPS],
                                        "note": "Not defined in handbook 1.3. Measured from the source shadings (p9, p12, p23, p31). The mid stop #097BAE is not a brand colour."}
    styles = []
    for k, nm, w, it in (("light", "Ubuntu Light", 300, False), ("light-italic", "Ubuntu Light Italic", 300, True), ("regular", "Ubuntu Regular", 400, False),
                         ("italic", "Ubuntu Italic", 400, True), ("medium", "Ubuntu Medium", 500, False), ("medium-italic", "Ubuntu Medium Italic", 500, True),
                         ("bold", "Ubuntu Bold", 700, False), ("bold-italic", "Ubuntu Bold Italic", 700, True)):
        styles.append({"id": f"py-tok-type-ubuntu-{k}", "name": nm, "weight": w, "italic": it,
                       "file": f"fonts/{nm.replace(' ', '-')}.ttf".replace("Ubuntu-Regular", "Ubuntu-Regular")})
    typo = {"family": "Ubuntu", "licence": "Ubuntu Font Licence 1.0 (fonts/UBUNTU-FONT-LICENCE.txt)", "styles": styles,
            "logo": {"parking": "Ubuntu Regular (measured on the vector outlines; handbook p6 says Medium, p7 says Medium)", "you": "Ubuntu Bold"},
            "usage_observed": {"location names, captions": "Ubuntu Bold", "body text": "Ubuntu Regular", "pylon section bars": "Ubuntu Medium", "dimension labels": "Ubuntu Light"},
            "other": {"py-tok-type-hoogtebalk-lettering": "outlined in the PDF, typeface unidentified",
                      "RVV numerals": "RWSTTDdx on portals, AnwbEeVL on pylons (third-party, outlined in the SVGs)"}}
    with open(os.path.join(out, "tokens.json"), "w", encoding="utf8") as f:
        json.dump({"colors": colors, "gradients": grad, "typography": typo,
                   "deviations": [
                       {"found": "#1A3680 in vector artwork", "used": "#1A3580", "reason": "handbook 1.3 states #1A3580"},
                       {"found": "#010101 (logo black)", "used": "#1D1D1B", "reason": "PY-Zwart in 1.3"},
                       {"found": "#082E7A (RAL 5002 swatch in hardware)", "used": "#1A3580", "reason": "RAL values are best match only"},
                       {"found": "#A0A1A0 (RAL 9006 swatch in hardware)", "used": "#AEAEAE", "reason": "PY-Grijs in 1.3"}]}, f, indent=1, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--spec", default=None)
    ap.add_argument("--only", default=".*")
    ap.add_argument("--out", default=ROOT)
    a = ap.parse_args()
    load_specs(a.spec)
    src = Source(a.src)
    inv = parse_inventory()
    ids = sorted(registry.BUILDERS)
    pat = re.compile(a.only)
    elements, unresolved_all, problems = [], {}, []
    for id_ in ids:
        if not pat.search(id_):
            continue
        try:
            el = registry.build(src, id_)
        except Exception as e:  # keep going, report
            problems.append((id_, repr(e)))
            continue
        w, h = el.size_mm()
        os.makedirs(os.path.join(a.out, "svg", el.level), exist_ok=True)
        with open(os.path.join(a.out, "svg", el.level, id_ + ".svg"), "w", encoding="utf8") as f:
            f.write(el.svg())
        row = inv.get(id_, {})
        variables = list(el.variables) if el.variables else [v.strip() for v in re.split(r",", row.get("variables", "")) if v.strip() and not v.strip().lower().startswith(("none", "geen"))]
        bf_src = list(el.built_from) if el.built_from else None
        if bf_src is None:
            bf, un = resolve(row.get("built_from", ""), ids, None)
            bf = [b for b in bf if b != id_]
            if un:
                unresolved_all[id_] = un
        else:
            bf = bf_src
        cols = []
        for c in el.colors():
            if c == "gradient-verloop":
                cols.append({"token": "py-tok-gradient-verloop", "hex": None})
            else:
                cols.append({"token": BRAND_TOKEN.get(c), "hex": c})
        stated = list(el.dims_mm) if el.dims_mm else None
        notes = el.notes or ""
        if getattr(el, "normalised", None):
            n = "; ".join(f"{k} to {v}" for k, v in ((k, __import__('pyassets').core.COLOR_NORMALISE[k]) for k in el.normalised))
            notes = (notes + " " if notes else "") + f"Colour normalised to the 1.3 brand value ({n})."
        tags = list(el.tags)
        pg = el.page
        elements.append({
            "id": id_, "name_nl": el.name_nl, "level": el.level, "category": el.category,
            "source_page": pg, "status": el.status,
            "dimensions_mm": {"width": round(w, 1), "height": round(h, 1),
                              "stated": stated, "basis": "handbook scale" if el.true_scale else ("n/a (token swatch)" if el.level == "tok" else "illustrative (no dimension in handbook)")},
            "colors": cols, "variables": variables, "built_from": bf, "tags": tags, "notes": notes.strip(),
            "svg": f"svg/{el.level}/{id_}.svg",
        })
    elements.sort(key=lambda e: ("tok atom comp prod".split().index(e["level"]), e["id"]))
    with open(os.path.join(a.out, "elements.json"), "w", encoding="utf8") as f:
        json.dump({"source": "parkingyou Huisstijlhandboek, Wayfinding & inrichting parkeervoorziening, v1.0, 09-2025 (All Jobs)", "count": len(elements), "elements": elements}, f, indent=1, ensure_ascii=False)
    write_tokens(a.out)
    print(len(elements), "elements written")
    if problems:
        print("BUILD ERRORS:")
        for p in problems:
            print("  ", p)
    if unresolved_all:
        print("unresolved built_from names (add to builder metadata):")
        for k, v in unresolved_all.items():
            print("  ", k, v)
    print("colour normalisation counts:", NORMALISE_LOG)


if __name__ == "__main__":
    main()
