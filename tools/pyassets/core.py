"""Core of the ParkingYou asset extractor.

Reads vector drawings and live text out of the source handbook PDF with PyMuPDF
and turns them into tight SVG elements. Coordinates inside the source are PDF
points (1 pt = 0.352778 mm); elements are written in millimetres.
"""
from __future__ import annotations

import io
import math
import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Callable, Iterable, Optional, Sequence, Union

import pymupdf

PT_MM = 25.4 / 72.0

# ---------------------------------------------------------------- brand tokens
BRAND = {
    "blauw": "#1A3580",
    "aqua": "#32B9CD",
    "oranje": "#F08300",
    "grijs": "#AEAEAE",
    "zwart": "#1D1D1B",
    "wit": "#FFFFFF",
}
# colours that are brand values drawn slightly off in the handbook. Section 1.3 wins.
COLOR_NORMALISE = {
    "#1A3680": "#1A3580",  # vector blue is one unit off the 1.3 value
    "#010101": "#1D1D1B",  # logo black versus PY-Zwart
    "#030304": "#1D1D1B",
    "#082E7A": "#1A3580",  # RAL 5002 swatch drawn in hardware
    "#A0A1A0": "#AEAEAE",  # RAL 9006 swatch drawn in hardware
}
NORMALISE_LOG: dict[str, int] = {}

# measured blauw to aqua verloop (see docs/phase1-inventory.md)
GRADIENT_STOPS = [(0.0, "#1A3580"), (0.18, "#1A3580"), (0.62, "#097BAE"), (1.0, "#32B9CD")]


def hex_of(rgb) -> str:
    return "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in rgb[:3])


def norm_color(h: Optional[str]) -> Optional[str]:
    if h is None:
        return None
    h = h.upper()
    n = COLOR_NORMALISE.get(h)
    if n:
        NORMALISE_LOG[h] = NORMALISE_LOG.get(h, 0) + 1
        return n
    return h


def fmt(v: float) -> str:
    s = ("%.3f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ---------------------------------------------------------------- transform
@dataclass
class TF:
    """Uniform scale plus translation: x' = (x - x0) * s + ox."""

    x0: float = 0.0
    y0: float = 0.0
    s: float = 1.0
    ox: float = 0.0
    oy: float = 0.0

    def pt(self, x, y):
        return ((x - self.x0) * self.s + self.ox, (y - self.y0) * self.s + self.oy)

    def len(self, v):
        return v * self.s


# ---------------------------------------------------------------- gradient
@dataclass
class Gradient:
    """A real vector linear gradient defined in source coordinates."""

    x1: float
    y1: float
    x2: float
    y2: float
    stops: Sequence = tuple(GRADIENT_STOPS)
    key: str = ""

    @staticmethod
    def for_box(box, kind="diag", stops=None):
        x0, y0, x1, y1 = box
        stops = stops or GRADIENT_STOPS
        if kind == "vert":
            return Gradient((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, stops)
        if kind == "horiz":
            return Gradient(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, stops)
        # 45 degree axis, extents from the top-left to the bottom-right corner
        w, h = x1 - x0, y1 - y0
        e = (w + h) / 2
        return Gradient(x0, y0, x0 + e, y0 + e, stops)


    @staticmethod
    def for_items(items, kind="diag", stops=None, end=1.0):
        """Gradient whose axis spans exactly the extent of the shape (not its bbox corners)."""
        stops = stops or GRADIENT_STOPS
        pts = []
        for it in items:
            if isinstance(it, Path):
                for sg in it.segs:
                    v = sg[1:]
                    pts += [(v[i], v[i + 1]) for i in range(0, len(v), 2)]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        if kind == "vert":
            return Gradient(cx, min(ys), cx, min(ys) + (max(ys) - min(ys)) * end, stops)
        if kind == "horiz":
            return Gradient(min(xs), cy, min(xs) + (max(xs) - min(xs)) * end, cy, stops)
        r2 = math.sqrt(2)
        s = [(x + y) / r2 for x, y in pts]
        sc = (cx + cy) / r2
        a = min(s) - sc
        b = a + (max(s) - min(s)) * end
        return Gradient(cx + a / r2, cy + a / r2, cx + b / r2, cy + b / r2, stops)


Paint = Union[str, Gradient, None]

# ---------------------------------------------------------------- items
class Item:
    bbox = (0, 0, 0, 0)
    tag = ""

    def svg(self, tf: TF, defs: "Defs") -> str:  # pragma: no cover
        raise NotImplementedError


class Defs:
    def __init__(self, prefix=""):
        self.prefix = prefix
        self.items: list[str] = []
        self.n = 0

    def gradient(self, g: Gradient, tf: TF) -> str:
        self.n += 1
        gid = f"{self.prefix}grad{self.n}"
        x1, y1 = tf.pt(g.x1, g.y1)
        x2, y2 = tf.pt(g.x2, g.y2)
        stops = "".join(f'<stop offset="{fmt(o)}" stop-color="{c}"/>' for o, c in g.stops)
        self.items.append(
            f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
            f'x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}">{stops}</linearGradient>'
        )
        return f"url(#{gid})"


def _paint(p: Paint, tf: TF, defs: Defs) -> str:
    if p is None:
        return "none"
    if isinstance(p, Gradient):
        return defs.gradient(p, tf)
    return p


@dataclass
class Path(Item):
    segs: list
    fill: Paint = None
    stroke: Paint = None
    width: float = 0.0
    fill_opacity: float = 1.0
    stroke_opacity: float = 1.0
    evenodd: bool = False
    cap: int = 0
    join: int = 0
    dashes: Optional[Sequence] = None
    box: tuple = (0, 0, 0, 0)
    tag: str = ""

    @property
    def bbox(self):  # type: ignore[override]
        x0, y0, x1, y1 = self.box
        pad = (self.width or 0) / 2 if self.stroke else 0
        return (x0 - pad, y0 - pad, x1 + pad, y1 + pad)

    def d(self, tf: TF) -> str:
        out = []
        for sg in self.segs:
            c = sg[0]
            if c == "Z":
                out.append("Z")
            elif c in ("M", "L"):
                x, y = tf.pt(sg[1], sg[2])
                out.append(f"{c}{fmt(x)} {fmt(y)}")
            else:
                pts = []
                for i in (1, 3, 5):
                    x, y = tf.pt(sg[i], sg[i + 1])
                    pts.append(f"{fmt(x)} {fmt(y)}")
                out.append("C" + " ".join(pts))
        return "".join(out)

    def svg(self, tf, defs):
        a = [f'd="{self.d(tf)}"']
        a.append(f'fill="{_paint(self.fill, tf, defs)}"')
        if self.fill is not None and self.evenodd:
            a.append('fill-rule="evenodd"')
        if self.fill is not None and self.fill_opacity < 0.999:
            a.append(f'fill-opacity="{fmt(self.fill_opacity)}"')
        if self.stroke is not None:
            a.append(f'stroke="{_paint(self.stroke, tf, defs)}"')
            a.append(f'stroke-width="{fmt(max(tf.len(self.width), 0.01))}"')
            if self.cap == 1:
                a.append('stroke-linecap="round"')
            elif self.cap == 2:
                a.append('stroke-linecap="square"')
            if self.join == 1:
                a.append('stroke-linejoin="round"')
            elif self.join == 2:
                a.append('stroke-linejoin="bevel"')
            if self.stroke_opacity < 0.999:
                a.append(f'stroke-opacity="{fmt(self.stroke_opacity)}"')
            if self.dashes:
                a.append('stroke-dasharray="' + " ".join(fmt(tf.len(v)) for v in self.dashes) + '"')
        return "<path " + " ".join(a) + "/>"


def rect_item(x0, y0, x1, y1, fill: Paint = None, stroke: Paint = None, width=0.0, rx=0.0, tag=""):
    """Rebuilt rectangle (optionally rounded) as a Path."""
    segs = rounded_rect_segs(x0, y0, x1, y1, rx)
    return Path(segs, fill=fill, stroke=stroke, width=width, box=(x0, y0, x1, y1), tag=tag)


def rounded_rect_segs(x0, y0, x1, y1, rx=0.0):
    if rx <= 0:
        return [("M", x0, y0), ("L", x1, y0), ("L", x1, y1), ("L", x0, y1), ("Z",)]
    rx = min(rx, (x1 - x0) / 2, (y1 - y0) / 2)
    k = 0.5522847498 * rx
    return [
        ("M", x0 + rx, y0),
        ("L", x1 - rx, y0),
        ("C", x1 - rx + k, y0, x1, y0 + rx - k, x1, y0 + rx),
        ("L", x1, y1 - rx),
        ("C", x1, y1 - rx + k, x1 - rx + k, y1, x1 - rx, y1),
        ("L", x0 + rx, y1),
        ("C", x0 + rx - k, y1, x0, y1 - rx + k, x0, y1 - rx),
        ("L", x0, y0 + rx),
        ("C", x0, y0 + rx - k, x0 + rx - k, y0, x0 + rx, y0),
        ("Z",),
    ]


def ellipse_item(cx, cy, rx, ry, fill: Paint = None, stroke: Paint = None, width=0.0, tag=""):
    k = 0.5522847498
    segs = [
        ("M", cx + rx, cy),
        ("C", cx + rx, cy + k * ry, cx + k * rx, cy + ry, cx, cy + ry),
        ("C", cx - k * rx, cy + ry, cx - rx, cy + k * ry, cx - rx, cy),
        ("C", cx - rx, cy - k * ry, cx - k * rx, cy - ry, cx, cy - ry),
        ("C", cx + k * rx, cy - ry, cx + rx, cy - k * ry, cx + rx, cy),
        ("Z",),
    ]
    return Path(segs, fill=fill, stroke=stroke, width=width, box=(cx - rx, cy - ry, cx + rx, cy + ry), tag=tag)


# font naming -> SVG family, weight, style
def font_css(name: str):
    n = name.split("+")[-1]
    italic = "Italic" in n
    if n.startswith("Ubuntu"):
        if "Light" in n:
            return "Ubuntu Light", 300, italic
        if "Medium" in n:
            return "Ubuntu Medium", 500, italic
        if "Bold" in n:
            return "Ubuntu", 700, italic
        return "Ubuntu", 400, italic
    return None


@dataclass
class Text(Item):
    x: float
    y: float
    text: str
    family: str
    weight: int
    italic: bool
    size: float
    fill: str
    spacing: float = 0.0
    anchor: str = "start"
    box: tuple = (0, 0, 0, 0)
    tag: str = ""

    @property
    def bbox(self):  # type: ignore[override]
        return self.box

    def svg(self, tf, defs):
        x, y = tf.pt(self.x, self.y)
        a = [
            f'x="{fmt(x)}" y="{fmt(y)}"',
            f'font-family="{self.family}"',
            f'font-size="{fmt(tf.len(self.size))}"',
        ]
        if self.weight == 700:
            a.append('font-weight="bold"')
        if self.italic:
            a.append('font-style="italic"')
        if abs(self.spacing) > 1e-3:
            a.append(f'letter-spacing="{fmt(tf.len(self.spacing))}"')
        if self.anchor != "start":
            a.append(f'text-anchor="{self.anchor}"')
        a.append(f'fill="{self.fill}"')
        t = (self.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        return f'<text {" ".join(a)} xml:space="preserve">{t}</text>'


@dataclass
class Raw(Item):
    """Hand written SVG fragment in *output* units, positioned by caller. Rarely used."""

    xml: str
    box: tuple = (0, 0, 0, 0)

    @property
    def bbox(self):  # type: ignore[override]
        return self.box

    def svg(self, tf, defs):
        return self.xml


@dataclass
class Group(Item):
    """Transparency group (opacity applies to the group as a whole, like in the source PDF)."""

    items: list = field(default_factory=list)
    opacity: float = 1.0
    gid: str = ""
    tag: str = ""

    @property
    def bbox(self):  # type: ignore[override]
        bs = [it.bbox for it in self.items if it.bbox != (0, 0, 0, 0)]
        if not bs:
            return (0, 0, 0, 0)
        return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))

    def svg(self, tf, defs):
        a = f' id="{self.gid}"' if self.gid else ""
        if self.opacity < 0.999:
            a += f' opacity="{fmt(self.opacity)}"'
        return f"<g{a}>" + "".join(it.svg(tf, defs) for it in self.items) + "</g>"


# ---------------------------------------------------------------- source
class Source:
    def __init__(self, path: str):
        self.path = path
        self.doc = pymupdf.open(path)
        self._dr: dict[int, list] = {}
        self._clips: dict[int, list] = {}
        self._grects: dict[int, list] = {}
        self._tx: dict[int, list] = {}
        self._fonts: dict = {}

    def page(self, pno: int):
        return self.doc[pno - 1]

    def drawings(self, pno: int):
        """Drawings in paint order, with invisible (fully clipped) paths removed.

        Each returned dict gets `seq` (paint order) and `clipped` (True when the path
        is partly outside its clip scissor, which QA must look at)."""
        if pno not in self._dr:
            out = []
            clips = []
            stack: list = []  # (level, scissor)
            gstack: list = []  # (level, gid, opacity, rect) of transparency groups with opacity < 1
            grects: list = []
            for i, d in enumerate(self.page(pno).get_drawings(extended=True)):
                lvl = d.get("level", 0)
                while stack and stack[-1][0] >= lvl:
                    stack.pop()
                while gstack and gstack[-1][0] >= lvl:
                    gstack.pop()
                if d["type"] == "group":
                    op = d.get("opacity")
                    if op is not None and op < 0.999:
                        gid = f"g{pno}-{i}"
                        gstack.append((lvl, gid, float(op), d["rect"]))
                        grects.append((gid, float(op), d["rect"]))
                    continue
                if d["type"] == "clip":
                    stack.append((lvl, d["scissor"]))
                    d["seq"] = i
                    clips.append(d)
                    continue
                if d["type"] == "group":
                    continue
                d["seq"] = i
                d["clipped"] = False
                d["gop"] = tuple((g[1], g[2]) for g in gstack)
                if stack:
                    sc = pymupdf.Rect(stack[0][1])
                    for _, r in stack[1:]:
                        sc &= pymupdf.Rect(r)
                    r = d["rect"]
                    if sc.is_empty or (r.x1 < sc.x0 or r.x0 > sc.x1 or r.y1 < sc.y0 or r.y0 > sc.y1):
                        if not (r.width == 0 or r.height == 0) or sc.is_empty:
                            continue  # invisible
                    if r.x0 < sc.x0 - 0.5 or r.y0 < sc.y0 - 0.5 or r.x1 > sc.x1 + 0.5 or r.y1 > sc.y1 + 0.5:
                        d["clipped"] = True
                        d["scissor"] = tuple(sc)
                out.append(d)
            self._dr[pno] = out
            self._clips[pno] = clips
            self._grects[pno] = grects
        return self._dr[pno]

    def group_rects(self, pno: int):
        """Transparency groups with opacity below 1 as (gid, opacity, rect)."""
        self.drawings(pno)
        return self._grects[pno]

    def clips(self, pno: int, bbox, min_size=6.0, tol=1.5):
        """Clip paths inside bbox as Path items. InDesign exports every gradient fill as
        `clip path + shading`, so these are the exact outlines of the gradient shapes.
        seq is set just after the clip so a rebuilt fill lands at the right paint order."""
        self.drawings(pno)
        x0, y0, x1, y1 = bbox
        res = []
        for d in self._clips[pno]:
            sc = d["scissor"]
            if not (sc.x0 >= x0 - tol and sc.y0 >= y0 - tol and sc.x1 <= x1 + tol and sc.y1 <= y1 + tol):
                continue
            if sc.width < min_size or sc.height < min_size:
                continue
            p = Path(segs=self._segs({"items": d["items"], "closePath": True}), fill="#FFFFFF",
                     evenodd=bool(d.get("even_odd")), box=(sc.x0, sc.y0, sc.x1, sc.y1), tag="clip-shape")
            p.seq = d["seq"] + 0.5  # type: ignore[attr-defined]
            p.clipped = False  # type: ignore[attr-defined]
            res.append(p)
        return res

    def render_array(self, pno: int, box, s=3.0):
        import numpy as np

        pix = self.page(pno).get_pixmap(matrix=pymupdf.Matrix(s, s), clip=pymupdf.Rect(*box), alpha=False)
        return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3).astype(float)

    # --- paths
    @staticmethod
    def _segs(d) -> list:
        segs = []
        cur = None
        for it in d["items"]:
            k = it[0]
            if k == "l":
                p1, p2 = it[1], it[2]
                if cur is None or abs(cur.x - p1.x) > 1e-3 or abs(cur.y - p1.y) > 1e-3:
                    segs.append(("M", p1.x, p1.y))
                segs.append(("L", p2.x, p2.y))
                cur = p2
            elif k == "c":
                p1, c1, c2, p2 = it[1], it[2], it[3], it[4]
                if cur is None or abs(cur.x - p1.x) > 1e-3 or abs(cur.y - p1.y) > 1e-3:
                    segs.append(("M", p1.x, p1.y))
                segs.append(("C", c1.x, c1.y, c2.x, c2.y, p2.x, p2.y))
                cur = p2
            elif k == "re":
                r = it[1]
                ori = it[2] if len(it) > 2 else 1
                if ori is not None and ori < 0:  # keep the winding of the source (outer + inner rectangle rings)
                    segs += [("M", r.x0, r.y0), ("L", r.x0, r.y1), ("L", r.x1, r.y1), ("L", r.x1, r.y0), ("Z",)]
                else:
                    segs += [("M", r.x0, r.y0), ("L", r.x1, r.y0), ("L", r.x1, r.y1), ("L", r.x0, r.y1), ("Z",)]
                cur = None
            elif k == "qu":
                q = it[1]
                segs += [("M", q.ul.x, q.ul.y), ("L", q.ur.x, q.ur.y), ("L", q.lr.x, q.lr.y), ("L", q.ll.x, q.ll.y), ("Z",)]
                cur = None
        if d.get("closePath") and segs and segs[-1][0] != "Z":
            segs.append(("Z",))
        return segs

    def paths(self, pno: int, bbox, partial=False, tol=0.6, skip: Optional[Callable] = None):
        x0, y0, x1, y1 = bbox
        out = []
        for d in self.drawings(pno):
            r = d["rect"]
            if partial:
                inside = not (r.x1 < x0 or r.x0 > x1 or r.y1 < y0 or r.y0 > y1)
            else:
                inside = r.x0 >= x0 - tol and r.y0 >= y0 - tol and r.x1 <= x1 + tol and r.y1 <= y1 + tol
            if not inside:
                continue
            fill = d.get("fill")
            stroke = d.get("color") if d["type"] in ("s", "fs") else None
            if d["type"] == "s":
                fill = None
            if fill is None and stroke is None:
                continue
            p = Path(
                segs=self._segs(d),
                fill=norm_color(hex_of(fill)) if fill is not None else None,
                stroke=norm_color(hex_of(stroke)) if stroke is not None else None,
                width=d.get("width") or 0.0,
                fill_opacity=d.get("fill_opacity") if d.get("fill_opacity") is not None else 1.0,
                stroke_opacity=d.get("stroke_opacity") if d.get("stroke_opacity") is not None else 1.0,
                evenodd=bool(d.get("even_odd")),
                cap=(d.get("lineCap") or (0,))[0] if isinstance(d.get("lineCap"), (tuple, list)) else 0,
                join=int(d.get("lineJoin") or 0),
                dashes=_dash(d.get("dashes")),
                box=(r.x0, r.y0, r.x1, r.y1),
            )
            p.seq = d.get("seq", 0)  # type: ignore[attr-defined]
            p.clipped = d.get("clipped", False)  # type: ignore[attr-defined]
            p.gop = d.get("gop", ())  # type: ignore[attr-defined]
            if skip and skip(p):
                continue
            out.append(p)
        return out

    # --- live text
    def spans(self, pno: int):
        if pno not in self._tx:
            res = []
            for b in self.page(pno).get_text("dict")["blocks"]:
                if b["type"] != 0:
                    continue
                for l in b["lines"]:
                    for s in l["spans"]:
                        res.append(s)
            self._tx[pno] = res
        return self._tx[pno]

    def texts(self, pno: int, bbox, skip_text: Optional[Callable[[str], bool]] = None, recolor=None):
        x0, y0, x1, y1 = bbox
        out = []
        for s in self.spans(pno):
            bx = s["bbox"]
            cx, cy = (bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2
            if not (x0 <= cx <= x1 and y0 <= cy <= y1):
                continue
            t = s["text"]
            if not t.strip():
                continue
            if skip_text and skip_text(t):
                continue
            css = font_css(s["font"])
            if css is None:
                continue  # outlined elsewhere (see glyph_paths)
            fam, w, it = css
            col = norm_color("#%06X" % s["color"])
            if recolor and col in recolor:
                col = recolor[col]
            org = s["origin"]
            # letter spacing: measured advance versus nominal advance
            spacing = _tracking(s, fam, w, it)
            tt = t.rstrip("\t") if t.strip() else t
            tx = Text(org[0], org[1], tt, fam, w, it, s["size"], col, spacing,
                      box=ink_box(tt, fam, w, it, s["size"], org[0], org[1], spacing))
            out.append(tx)
        return out

    # --- glyph outlines for fonts we do not own (RVV numerals etc.)
    def glyph_paths(self, pno: int, bbox, fonts: Iterable[str]):
        from fontTools.ttLib import TTFont
        from fontTools.pens.svgPathPen import SVGPathPen  # noqa: F401
        from fontTools.pens.recordingPen import RecordingPen

        want = tuple(fonts)
        x0, y0, x1, y1 = bbox
        res = []
        page = self.page(pno)
        for sp in page.get_texttrace():
            fname = sp["font"].split("+")[-1]
            if not any(fname.startswith(w) for w in want):
                continue
            key = (pno, sp["font"])
            if key not in self._fonts:
                xref = None
                for f in page.get_fonts(full=True):
                    if f[3].split("+")[-1] == fname or f[3] == sp["font"]:
                        xref = f[0]
                        break
                buf = self.doc.extract_font(xref)[3] if xref else None
                self._fonts[key] = TTFont(io.BytesIO(buf)) if buf else None
            tt = self._fonts[key]
            if tt is None:
                continue
            gs = tt.getGlyphSet()
            order = tt.getGlyphOrder()
            upm = tt["head"].unitsPerEm
            size = sp["size"]
            col = norm_color(hex_of(sp["color"]))
            for ch in sp["chars"]:
                uni, gid, org, bb = ch[0], ch[1], ch[2], ch[3]
                if not (x0 <= org[0] <= x1 and y0 <= org[1] <= y1):
                    continue
                if gid >= len(order):
                    continue
                pen = RecordingPen()
                gs[order[gid]].draw(pen)
                segs = []
                k = size / upm
                cur = None
                for op, pts in pen.value:
                    P = [(org[0] + px * k, org[1] - py * k) for px, py in pts]
                    if op == "moveTo":
                        segs.append(("M", *P[0])); cur = P[0]
                    elif op == "lineTo":
                        segs.append(("L", *P[0])); cur = P[0]
                    elif op == "qCurveTo":
                        # expand quadratic spline into cubic segments
                        pts_ = [cur] + P
                        offs = P[:-1]
                        end = P[-1]
                        if end is None:
                            continue
                        cps = []
                        for i, o in enumerate(offs):
                            nxt = offs[i + 1] if i + 1 < len(offs) else end
                            on = ((o[0] + nxt[0]) / 2, (o[1] + nxt[1]) / 2) if i + 1 < len(offs) else end
                            cps.append((o, on))
                        p0 = cur
                        for o, on in cps:
                            c1 = (p0[0] + 2 / 3 * (o[0] - p0[0]), p0[1] + 2 / 3 * (o[1] - p0[1]))
                            c2 = (on[0] + 2 / 3 * (o[0] - on[0]), on[1] + 2 / 3 * (o[1] - on[1]))
                            segs.append(("C", c1[0], c1[1], c2[0], c2[1], on[0], on[1]))
                            p0 = on
                        cur = p0
                    elif op == "curveTo":
                        segs.append(("C", *P[0], *P[1], *P[2])); cur = P[2]
                    elif op in ("closePath", "endPath"):
                        segs.append(("Z",))
                if not segs:
                    continue
                xs = [s_[i] for s_ in segs for i in range(1, len(s_), 2) if s_[0] != "Z"]
                ys = [s_[i] for s_ in segs for i in range(2, len(s_), 2) if s_[0] != "Z"]
                res.append(Path(segs, fill=col, box=(min(xs), min(ys), max(xs), max(ys)), evenodd=False))
        return res

    # --- raster boxes (to find the gradient rasters that need rebuilding)
    def images(self, pno: int, bbox=None):
        out = []
        for im in self.page(pno).get_image_info(xrefs=True):
            b = im["bbox"]
            if bbox and not (b[0] >= bbox[0] - 1 and b[1] >= bbox[1] - 1 and b[2] <= bbox[2] + 1 and b[3] <= bbox[3] + 1):
                continue
            out.append({"bbox": tuple(b), "w": im["width"], "h": im["height"], "xref": im.get("xref", 0)})
        return out


def _dash(s):
    if not s:
        return None
    m = re.match(r"\[([^\]]*)\]\s*([\d.]+)", s)
    if not m or not m.group(1).strip():
        return None
    return [float(v) for v in m.group(1).split()]


_FONT_CACHE: dict = {}


def _font_adv(fam, w, it):
    from fontTools.ttLib import TTFont

    key = (fam, w, it)
    if key not in _FONT_CACHE:
        wname = {300: "Light", 400: "Regular", 500: "Medium", 700: "Bold"}[w]
        base = f"Ubuntu-{wname}" + ("Italic" if it and w != 400 else "")
        if it and w == 400:
            base = "Ubuntu-Italic"
        import os

        p = os.path.join(os.path.dirname(__file__), "..", "..", "fonts", base + ".ttf")
        f = TTFont(p)
        _FONT_CACHE[key] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _FONT_CACHE[key]


_BOUNDS: dict = {}


def ink_box(s, fam, w, it, size, x, y, spacing=0.0, anchor="start"):
    """Ink bounding box of a text run (from glyph outlines), not the font line box."""
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.ttLib import TTFont
    import os

    key = (fam, w, it)
    if key not in _BOUNDS:
        wname = {300: "Light", 400: "Regular", 500: "Medium", 700: "Bold"}[w]
        base = ("Ubuntu-Italic" if (it and w == 400) else f"Ubuntu-{wname}" + ("Italic" if it else ""))
        f = TTFont(os.path.join(os.path.dirname(__file__), "..", "..", "fonts", base + ".ttf"))
        _BOUNDS[key] = (f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    gs, cmap, hm, upm = _BOUNDS[key]
    k = size / upm
    cx = 0.0
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    for c in s:
        g = cmap.get(ord(c))
        if g is None:
            continue
        bp = BoundsPen(gs)
        gs[g].draw(bp)
        if bp.bounds:
            b = bp.bounds
            x0 = min(x0, cx + b[0] * k); x1 = max(x1, cx + b[2] * k)
            y0 = min(y0, -b[3] * k); y1 = max(y1, -b[1] * k)
        cx += hm[g][0] * k + spacing
    if x0 > x1:
        return (x, y, x, y)
    adv = cx - spacing
    ox = x if anchor == "start" else (x - adv / 2 if anchor == "middle" else x - adv)
    return (ox + x0, y + y0, ox + x1, y + y1)


def _tracking(span, fam, w, it) -> float:
    try:
        cmap, hmtx, upm = _font_adv(fam, w, it)
        t = span["text"].rstrip("\t")
        nat = sum(hmtx[cmap[ord(c)]][0] for c in t if ord(c) in cmap) * span["size"] / upm
        bw = span["bbox"][2] - span["bbox"][0]
        if len(t) > 1 and bw > 0:
            sp = (bw - nat) / (len(t) - 1)
            if abs(sp) > span["size"] * 0.004 and abs(sp) < span["size"] * 0.5:
                return sp
    except Exception:
        pass
    return 0.0


# ---------------------------------------------------------------- element
@dataclass
class Element:
    id: str
    name_nl: str
    level: str  # tok, atom, comp, prod
    category: str
    page: Union[int, Sequence[int]]
    items: list = field(default_factory=list)
    status: str = "extracted"  # extracted or rebuilt
    mm_per_pt: float = PT_MM  # millimetres per source point
    dims_mm: Optional[Sequence] = None  # stated overall dimensions (w, h, [d]) from the handbook
    variables: Sequence = ()
    built_from: Sequence = ()
    notes: str = ""
    tags: Sequence = ()  # e.g. third-party
    true_scale: bool = False  # True when mm_per_pt was derived from a handbook dimension
    background: Optional[str] = None

    def bbox(self):
        bs = [it.bbox for it in self.items if it.bbox != (0, 0, 0, 0)]
        if not bs:
            return (0, 0, 1, 1)
        return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))

    def size_mm(self):
        x0, y0, x1, y1 = self.bbox()
        return ((x1 - x0) * self.mm_per_pt, (y1 - y0) * self.mm_per_pt)

    def tf(self, scale=1.0, ox=0.0, oy=0.0):
        x0, y0, _, _ = self.bbox()
        return TF(x0, y0, self.mm_per_pt * scale, ox, oy)

    def body(self, tf: TF, defs: Defs) -> str:
        return "".join(it.svg(tf, defs) for it in self.items)

    def colors(self):
        cs = set()

        def flat(items):
            for it in items:
                if isinstance(it, Group):
                    yield from flat(it.items)
                else:
                    yield it

        for it in flat(self.items):
            if isinstance(it, Path):
                for c in (it.fill, it.stroke):
                    if isinstance(c, str):
                        cs.add(c)
                    elif isinstance(c, Gradient):
                        cs.add("gradient-verloop")
            elif isinstance(it, Text):
                cs.add(it.fill)
        return sorted(cs)

    def svg(self) -> str:
        w, h = self.size_mm()
        tf = self.tf()
        defs = Defs(prefix=self.id + "-")
        body = self.body(tf, defs)
        d = "<defs>" + "".join(defs.items) + "</defs>" if defs.items else ""
        title = f"{self.id}: {self.name_nl}"
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(w)}mm" height="{fmt(h)}mm" '
            f'viewBox="0 0 {fmt(w)} {fmt(h)}">\n<title>{_esc(title)}</title>\n{d}'
            f'<g id="{self.id}">{body}</g>\n</svg>\n'
        )


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- composition helpers
def affine(items, sx=1.0, sy=None, tx=0.0, ty=0.0):
    """Return copies of items mapped by x' = x*sx + tx, y' = y*sy + ty (source coordinates)."""
    import copy

    sy = sx if sy is None else sy
    out = []
    for it in items:
        c = copy.copy(it)
        if isinstance(c, Path):
            segs = []
            for sg in c.segs:
                if sg[0] == "Z":
                    segs.append(sg)
                else:
                    v = list(sg[1:])
                    nv = []
                    for i in range(0, len(v), 2):
                        nv += [v[i] * sx + tx, v[i + 1] * sy + ty]
                    segs.append((sg[0], *nv))
            c.segs = segs
            b = c.box
            c.box = (b[0] * sx + tx, b[1] * sy + ty, b[2] * sx + tx, b[3] * sy + ty)
            c.width = c.width * (abs(sx) + abs(sy)) / 2
            if isinstance(c.fill, Gradient):
                g = c.fill
                c.fill = Gradient(g.x1 * sx + tx, g.y1 * sy + ty, g.x2 * sx + tx, g.y2 * sy + ty, g.stops)
        elif isinstance(c, Group):
            c.items = affine(c.items, sx, sy, tx, ty)
        elif isinstance(c, Text):
            c.x, c.y = c.x * sx + tx, c.y * sy + ty
            c.size *= (abs(sx) + abs(sy)) / 2
            c.spacing *= abs(sx)
            b = c.box
            c.box = (b[0] * sx + tx, b[1] * sy + ty, b[2] * sx + tx, b[3] * sy + ty)
        out.append(c)
    return out


def items_box(items):
    bs = [it.bbox for it in items if it.bbox != (0, 0, 0, 0)]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def fit_items(items, box_to, keep_aspect=True):
    """Scale and move items so their bbox matches box_to."""
    b = items_box(items)
    sx = (box_to[2] - box_to[0]) / max(b[2] - b[0], 1e-6)
    sy = (box_to[3] - box_to[1]) / max(b[3] - b[1], 1e-6)
    if keep_aspect:
        sx = sy = min(sx, sy)
    tx = box_to[0] - b[0] * sx + ((box_to[2] - box_to[0]) - (b[2] - b[0]) * sx) / 2
    ty = box_to[1] - b[1] * sy + ((box_to[3] - box_to[1]) - (b[3] - b[1]) * sy) / 2
    return affine(items, sx, sy, tx, ty)


def paint(items, fill: Paint):
    """Recolour every path of a list with one paint (flat colour or Gradient)."""
    import copy

    out = []
    for it in items:
        c = copy.copy(it)
        if isinstance(c, Path):
            c.fill = fill
            c.stroke = None
        elif isinstance(c, Group):
            c.items = paint(c.items, fill)
        out.append(c)
    return out


def grad_rect(box, kind="diag", rx=0.0, stops=None, tag="rebuilt-gradient"):
    """Rebuilt rectangle filled with the real vector blauw-aqua verloop."""
    return rect_item(*box, fill=Gradient.for_box(box, kind, stops), rx=rx, tag=tag)


# ---------------------------------------------------------------- gradient fitting
def _curve(stops, n=401):
    import numpy as np

    ts = np.linspace(0, 1, n)
    cols = np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for _, h in stops], float)
    offs = np.array([o for o, _ in stops])
    k = np.stack([np.interp(ts, offs, cols[:, c]) for c in range(3)], axis=1)
    return ts, k


def fit_gradient(src: Source, pno: int, shape, stops=None, s=3.0, tol=11.0):
    """Measure the real gradient axis of a shape in the source by regression.

    Renders the page region, keeps the pixels that lie on the blauw-aqua colour curve
    (this drops art drawn on top), maps each to its position t along the curve and fits
    t = a*x + b*y + c. Returns a Gradient that starts at t=0 and ends at t=1 in source
    coordinates. Falls back to the 45 degree corner-to-corner axis if there are too few pixels."""
    import numpy as np

    stops = stops or GRADIENT_STOPS
    box = shape.box if isinstance(shape, Path) else shape
    img = src.render_array(pno, box, s)
    H, W, _ = img.shape
    ys, xs = np.mgrid[0:H:2, 0:W:2]
    col = img[ys, xs].reshape(-1, 3)
    X = xs.reshape(-1) / s + box[0]
    Y = ys.reshape(-1) / s + box[1]
    ts, k = _curve(stops)
    # nearest curve point, chunked
    best_t = np.zeros(len(col)); best_d = np.zeros(len(col))
    for i in range(0, len(col), 4000):
        c = col[i:i + 4000]
        d = ((c[:, None, :] - k[None, :, :]) ** 2).sum(-1)
        j = d.argmin(1)
        best_t[i:i + 4000] = ts[j]
        best_d[i:i + 4000] = np.sqrt(d[np.arange(len(c)), j])
    keep = (best_d < tol) & (best_t > 0.05) & (best_t < 0.95)
    if keep.sum() < 80:
        return Gradient.for_box(box, "diag", stops)
    A = np.stack([X[keep], Y[keep], np.ones(keep.sum())], 1)
    t_ = best_t[keep]
    sol = np.linalg.lstsq(A, t_, rcond=None)[0]
    for _ in range(3):
        res = np.abs(A @ sol - t_)
        m = res < max(0.06, np.percentile(res, 80))
        if m.sum() < 60:
            break
        sol = np.linalg.lstsq(A[m], t_[m], rcond=None)[0]
    a, b, c = sol
    g2 = a * a + b * b
    if g2 < 1e-12:
        return Gradient.for_box(box, "diag", stops)
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    tc = a * cx + b * cy + c
    return Gradient(cx + a * (0 - tc) / g2, cy + b * (0 - tc) / g2, cx + a * (1 - tc) / g2, cy + b * (1 - tc) / g2, stops)


def gradient_shape(src: Source, pno: int, shape: Path, stops=None):
    """Return the clip shape filled with its fitted real vector gradient (a rebuilt element)."""
    import copy

    p = copy.copy(shape)
    p.fill = fit_gradient(src, pno, shape, stops)
    p.tag = "rebuilt-gradient"
    return p


def make_text(x, y, s, family="Ubuntu", weight=400, italic=False, size=10.0, fill="#1D1D1B", anchor="start", spacing=0.0):
    """Live text item with a bbox computed from the Ubuntu font metrics."""
    try:
        cmap, hmtx, upm = _font_adv(family, weight, italic)
        wd = sum(hmtx[cmap[ord(c)]][0] for c in s if ord(c) in cmap) * size / upm + spacing * max(len(s) - 1, 0)
    except Exception:
        wd = len(s) * size * 0.55
    return Text(x, y, s, family, weight, italic, size, fill, spacing, anchor, box=ink_box(s, family, weight, italic, size, x, y, spacing, anchor))


# ---------------------------------------------------------------- boolean cut-outs
def _to_pathops(p: "Path"):
    import pathops

    po = pathops.Path()
    po.fillType = pathops.FillType.EVEN_ODD if p.evenodd else pathops.FillType.WINDING
    pen = po.getPen()
    open_ = False
    for sg in p.segs:
        c = sg[0]
        if c == "M":
            if open_:
                pen.endPath()
            pen.moveTo((sg[1], sg[2])); open_ = True
        elif c == "L":
            pen.lineTo((sg[1], sg[2]))
        elif c == "C":
            pen.curveTo((sg[1], sg[2]), (sg[3], sg[4]), (sg[5], sg[6]))
        elif c == "Z":
            pen.closePath(); open_ = False
    if open_:
        pen.endPath()
    return po


def _from_pathops(po, like: "Path"):
    segs = []
    cur = None
    for verb, pts in po.segments:
        if verb == "moveTo":
            segs.append(("M", *pts[0])); cur = pts[0]
        elif verb == "lineTo":
            segs.append(("L", *pts[0])); cur = pts[0]
        elif verb == "curveTo":
            segs.append(("C", *pts[0], *pts[1], *pts[2])); cur = pts[2]
        elif verb == "qCurveTo":
            q = list(pts)
            p0 = cur
            offs, end = q[:-1], q[-1]
            for i, o in enumerate(offs):
                on = end if i == len(offs) - 1 else ((o[0] + offs[i + 1][0]) / 2, (o[1] + offs[i + 1][1]) / 2)
                segs.append(("C", p0[0] + 2 / 3 * (o[0] - p0[0]), p0[1] + 2 / 3 * (o[1] - p0[1]),
                             on[0] + 2 / 3 * (o[0] - on[0]), on[1] + 2 / 3 * (o[1] - on[1]), on[0], on[1]))
                p0 = on
            cur = p0
        elif verb == "closePath":
            segs.append(("Z",))
    import copy

    c = copy.copy(like)
    c.segs = segs
    c.evenodd = False
    xs = [s[i] for s in segs if s[0] != "Z" for i in range(1, len(s), 2)]
    ys = [s[i] for s in segs if s[0] != "Z" for i in range(2, len(s), 2)]
    if xs:
        c.box = (min(xs), min(ys), max(xs), max(ys))
    return c


def cutout(items, hole="#FFFFFF"):
    """Turn white 'gap' paths painted over solid paths into real holes (boolean difference).

    Single-colour pictograms and figures in the source separate limbs and glyph parts with white paths.
    Placed on a coloured or gradient background those would show up as white lines, so they are cut out."""
    import pathops

    out: list = []
    for it in items:
        if isinstance(it, Path) and isinstance(it.fill, str) and it.fill.upper() == hole and it.stroke is None:
            under = [o for o in out if isinstance(o, Path) and isinstance(o.fill, str) and o.fill.upper() != hole
                     and not (it.box[2] < o.box[0] or it.box[0] > o.box[2] or it.box[3] < o.box[1] or it.box[1] > o.box[3])]
            if under:
                w = _to_pathops(it)
                for o in under:
                    r = pathops.op(_to_pathops(o), w, pathops.PathOp.DIFFERENCE)
                    new = _from_pathops(r, o)
                    out[out.index(o)] = new
                continue
        out.append(it)
    return out


# ---------------------------------------------------------------- print support
# Blues, aquas and black that the print files draw slightly off the 1.3 values (see docs/print-phase1-inventory.md).
# Applied only when library elements are built from print files (library atoms and components);
# reference reproductions keep the source colours.
PRINT_NORMALISE = {
    "#0B3D8A": "#1A3580", "#1F4383": "#1A3580", "#1C4695": "#1A3580", "#204382": "#1A3580",
    "#174797": "#1A3580", "#27397E": "#1A3580",
    "#24BFCD": "#32B9CD", "#24BDCD": "#32B9CD", "#23BDCD": "#32B9CD", "#31BBCD": "#32B9CD",
    "#000000": "#1D1D1B",
}


class normalised:
    """Context manager: apply extra colour normalisation (e.g. PRINT_NORMALISE) while building elements."""

    def __init__(self, extra):
        self.extra = extra

    def __enter__(self):
        self._saved = dict(COLOR_NORMALISE)
        COLOR_NORMALISE.update(self.extra)
        return self

    def __exit__(self, *a):
        COLOR_NORMALISE.clear()
        COLOR_NORMALISE.update(self._saved)


def regroup(src: "Source", pno: int, items: list):
    """Wrap items that sat inside a transparency group (opacity < 1) of the source in Group items.

    Paths carry `gop` from Source.paths; live texts are assigned to a group when their centre lies in the
    group rectangle. Consecutive members of one group become one Group (z-order of the first member)."""
    rects = {g: (op, r) for g, op, r in src.group_rects(pno)}
    # live text carries no group information: it joins only a text-only group (a group without path members), the smallest one
    # whose rectangle holds its centre. A text over a tinted shape (watermark, field) therefore stays outside the tint.
    with_paths = {it.gop[-1][0] for it in items if isinstance(it, Path) and getattr(it, "gop", ())}
    text_groups = {g: v for g, v in rects.items() if g not in with_paths}
    out: list = []
    cur: dict = {}
    for it in items:
        gid = None
        if isinstance(it, Path) and getattr(it, "gop", ()):
            gid = it.gop[-1][0]
            op = 1.0
            for _, o in it.gop:
                op *= o
        elif isinstance(it, Text):
            cx, cy = (it.box[0] + it.box[2]) / 2, (it.box[1] + it.box[3]) / 2
            best = None
            for g, (o, r) in text_groups.items():
                if r.x0 <= cx <= r.x1 and r.y0 <= cy <= r.y1 and (best is None or r.width * r.height < best[2]):
                    best = (g, o, r.width * r.height)
            if best:
                gid, op = best[0], best[1]
        if gid is None:
            out.append(it)
            continue
        if gid not in cur:
            cur[gid] = Group(items=[], opacity=op, gid="")
            out.append(cur[gid])
        cur[gid].items.append(it)
    return out
