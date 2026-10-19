"""Tokens, fonts en atoms uit de repo. Niets wordt hier opnieuw gedefinieerd; alles komt uit tokens.json, fonts/ en svg/."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PP = os.path.dirname(HERE)
ROOT = os.path.dirname(PP)
DATA = os.path.join(PP, "data")

with open(os.path.join(ROOT, "tokens.json"), encoding="utf-8") as f:
    TOKENS = json.load(f)

_c = TOKENS["colors"]
BLAUW = _c["py-tok-color-blauw"]["hex"]
AQUA = _c["py-tok-color-aqua"]["hex"]
ORANJE = _c["py-tok-color-oranje"]["hex"]
GRIJS = _c["py-tok-color-grijs"]["hex"]
ZWART = _c["py-tok-color-zwart"]["hex"]
WIT = _c["py-tok-color-wit"]["hex"]
# Aqua op 10 procent voor invoervelden en vlakken (docs/print-rules.md, regel 8): transparantie, geen vaste tint.
AQUA_TINT_OPACITY = 0.10

PT = 25.4 / 72  # mm per punt

# face -> (font-family, font-weight, bestand); dezelfde familienamen als in de bestaande templates
FACES = {
    "regular": ("Ubuntu", None, "Ubuntu-Regular.ttf"),
    "bold": ("Ubuntu", "bold", "Ubuntu-Bold.ttf"),
    "medium": ("Ubuntu Medium", None, "Ubuntu-Medium.ttf"),
    "light": ("Ubuntu Light", None, "Ubuntu-Light.ttf"),
}

_fonts = {}


def font(face):
    if face not in _fonts:
        from fontTools.ttLib import TTFont
        tt = TTFont(os.path.join(ROOT, "fonts", FACES[face][2]))
        _fonts[face] = (tt, tt.getBestCmap(), tt["hmtx"], tt["head"].unitsPerEm)
    return _fonts[face]


def text_width(text, face, size, letter_spacing=0.0):
    """Breedte in dezelfde eenheid als size. Geen kerning: zo rendert cairo (cairosvg) ook."""
    tt, cmap, hmtx, upm = font(face)
    w = 0.0
    for ch in text.replace("\u00a0", " "):
        g = cmap.get(ord(ch))
        if g is None:
            g = ".notdef"
        w += hmtx[g][0]
    return w * size / upm + letter_spacing * len(text)


def face_attrs(face):
    fam, weight, _ = FACES[face]
    s = f'font-family="{fam}"'
    if weight:
        s += f' font-weight="{weight}"'
    return s


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ---------- atoms -----------------------------------------------------------

def _atom_file(id_):
    for sub in ("atom", "comp", "prod"):
        p = os.path.join(ROOT, "svg", sub, id_ + ".svg")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(id_)


_atoms = {}


def atom_info(id_):
    """(inner svg, breedte mm, hoogte mm) van een element uit svg/."""
    if id_ not in _atoms:
        raw = open(_atom_file(id_), encoding="utf-8").read()
        m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', raw)
        w, h = float(m.group(1)), float(m.group(2))
        inner = raw[raw.index("</title>") + len("</title>"):raw.rindex("</svg>")].strip()
        inner = re.sub(r'\sid="[^"]*"', "", inner)  # geen dubbele id's als een atom twee keer voorkomt
        _atoms[id_] = (inner, w, h)
    return _atoms[id_]


def atom(id_, x, y, w=None, h=None, scale=None, recolor=None, opacity=None):
    """Zet een atom of component uit de repo. Geef breedte, hoogte of schaal; x, y is linksboven (mm)."""
    inner, aw, ah = atom_info(id_)
    if scale is None:
        scale = (w / aw) if w else (h / ah)
    if recolor:
        for a, b in recolor.items():
            inner = inner.replace(f'fill="{a}"', f'fill="{b}"')
    g = f'<g data-element="{id_}" transform="translate({x:.3f} {y:.3f}) scale({scale:.5f})"'
    if opacity is not None:
        g += f' opacity="{opacity}"'
    return g + f">{inner}</g>", aw * scale, ah * scale


def verloop_defs(id_="verloop", direction="diag"):
    """Het blauw-aqua verloop uit tokens.json (stops gemeten in de bron)."""
    stops = TOKENS["gradients"]["py-tok-gradient-verloop"]["stops"]
    x2, y2 = {"diag": ("1", "1"), "vert": ("0", "1"), "horiz": ("1", "0")}[direction]
    s = "".join(f'<stop offset="{st["offset"]}" stop-color="{st["hex"]}"/>' for st in stops)
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


# ---------- tekst als lijnwerk (voor SVG's die buiten de repo gaan) ----------

def text_outline(text, face, size, x, y, fill, anchor="start", letter_spacing=0.0):
    """Tekst als pad. Voor badges die partners op hun eigen site zetten, zonder dat Ubuntu geinstalleerd hoeft te zijn."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    tt, cmap, hmtx, upm = font(face)
    gs = tt.getGlyphSet()
    k = size / upm
    total = text_width(text, face, size, letter_spacing)
    cx = x - (total if anchor == "end" else total / 2 if anchor == "middle" else 0)
    parts = []
    for ch in text:
        g = cmap.get(ord(ch), ".notdef")
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.3f}".rstrip("0").rstrip("."))
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, y)))
        d = pen.getCommands()
        if d:
            parts.append(d)
        cx += hmtx[g][0] * k + letter_spacing
    return f'<path d="{" ".join(parts)}" fill="{fill}"/>', total
