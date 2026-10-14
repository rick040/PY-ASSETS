"""Tokens: colour swatches, gradients and type specimens (generated, not cropped)."""
from pyassets import Gradient, Path, ellipse_item, make_text, rect_item, BRAND
from pyassets.registry import crop, element

R = 34.0  # swatch radius in source points (matches the 1.3 swatches)

COLORS = [
    ("blauw", "PY-Blauw", "#1A3580", "brand"),
    ("aqua", "PY-Aqua", "#32B9CD", "brand"),
    ("oranje", "PY-Oranje", "#F08300", "brand"),
    ("grijs", "PY-Grijs", "#AEAEAE", "brand"),
    ("zwart", "PY-Zwart", "#1D1D1B", "brand"),
    ("wit", "Wit (niet in 1.3)", "#FFFFFF", "observed"),
    ("ral-9010", "RAL 9010 hoogtebalk (niet in 1.3)", "#FFFFFF", "observed"),
    ("reflective-red", "Rode reflecterende band (geen merk)", "#C20016", "observed"),
    ("led-green", "LED groen (geen merk)", "#3AAA35", "observed"),
    ("safety-green", "Veiligheidsgroen (geen merk)", "#008A3B", "observed"),
    ("rvv-red", "RVV rood (third-party)", "#E30613", "observed"),
]
for key, name, hexv, kind in COLORS:
    def mk(hexv=hexv, key=key):
        def f(src):
            stroke = "#AEAEAE" if hexv == "#FFFFFF" else None
            c = ellipse_item(R, R, R, R, fill=hexv, stroke=stroke, width=0.6 if stroke else 0.0)
            return [c]
        return f
    element(f"py-tok-color-{key}", name, "tok", "color", 8 if kind == "brand" else None,
            notes=("Value from handbook 1.3." if kind == "brand" else "Observed in the drawings, not defined in 1.3."),
            tags=(("third-party",) if key == "rvv-red" else ()))(mk())

GRAD = [("verloop", "Verloop (diagonaal)", "diag", "9, 12, 14, 30, 32, 33"),
        ("verloop-vertical", "Verloop (verticaal)", "vert", "31"),
        ("verloop-horizontal", "Verloop (horizontaal)", "horiz", "23, 24")]
for key, name, kind, pg in GRAD:
    def mk(kind=kind):
        def f(src):
            box = (0, 0, 120, 60)
            return [rect_item(*box, fill=Gradient.for_box(box, kind), tag="rebuilt-gradient")], {
                "status": "rebuilt", "notes": "Source gradients are PDF shadings; stops were measured (#1A3580 to 18%, #097BAE at 62%, #32B9CD at 100%)."}
        return f
    element(f"py-tok-gradient-{key}", name, "tok", "gradient", None)(mk())

TYPE = [("light", "Ubuntu Light", "Ubuntu Light", 300, False), ("light-italic", "Ubuntu Light Italic", "Ubuntu Light", 300, True),
        ("regular", "Ubuntu Regular", "Ubuntu", 400, False), ("italic", "Ubuntu Italic", "Ubuntu", 400, True),
        ("medium", "Ubuntu Medium", "Ubuntu Medium", 500, False), ("medium-italic", "Ubuntu Medium Italic", "Ubuntu Medium", 500, True),
        ("bold", "Ubuntu Bold", "Ubuntu", 700, False), ("bold-italic", "Ubuntu Bold Italic", "Ubuntu", 700, True)]
for key, name, fam, w, it in TYPE:
    def mk(name=name, fam=fam, w=w, it=it):
        def f(src):
            return [make_text(0, 34, "Aa Bb 123", fam, w, it, 34, BRAND["blauw"]),
                    make_text(0, 52, name, fam, w, it, 13, BRAND["zwart"])]
        return f
    element(f"py-tok-type-ubuntu-{key}", name, "tok", "typography", 7)(mk())


@element("py-tok-type-hoogtebalk-lettering", "Snijletters hoogtebalk", "tok", "typography", 22,
         notes="Typeface unidentified, outlined in the PDF. Extracted from the clean sample on p22.")
def _(src):
    from pyassets.filters import thin_line
    items = crop(src, 22, (150, 645, 595, 681), texts=False, skip=thin_line)
    from pyassets import items_box
    b = items_box(items)
    return items, {"mm_per_pt": 1000.0 / (b[2] - b[0]), "true_scale": True, "dims_mm": (1000, round((b[3] - b[1]) * 1000.0 / (b[2] - b[0]), 1))}
