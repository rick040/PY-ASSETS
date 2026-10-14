"""Composer: build print templates and library components from existing library SVGs plus new shapes and live text.

Coordinates are millimetres. For a template (`Doc(trim=(w, h), bleed=3)`) all coordinates you pass are relative to the
TRIM corner (0, 0 = top left of the trimmed format); the composer adds the bleed offset. For a tight component
(`Doc(tight=True)`) coordinates are free and the viewBox is the union of everything placed.

    d = Doc("py-app-demo", "Demo", trim=(148, 105), bleed=3)
    d.rect(-3, -3, 151, 108, fill="#1A3580", gid="bleed-background")
    d.place("py-atom-logo-horizontal-white", 21.7, 38.1, w=104.9)
    d.text(52.3, 65.5, "The other way of parking", size=4.58, fill="#FFFFFF", spacing=0.27, variable="tagline")
    open("template.svg", "w").write(d.svg())
    d.built_from -> ["py-atom-logo-horizontal-white"]
"""
from __future__ import annotations

import math
import os
import re
from contextlib import contextmanager
from typing import Optional

from .core import fmt, ink_box, _esc, _font_adv

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LEVEL_DIR = {"tok": "tok", "atom": "atom", "comp": "comp", "prod": "prod"}
CUT_COLOR = "#EE4D9B"  # screen colour of the ThruCut spot in the source (alternate 0/85/0/0)
CUT_WIDTH = 0.353  # 1 pt, as in the source
PH_COLOR = "#EE4D9B"  # placeholder outline

_LIB: dict = {}


def lib_svg(ref_id: str):
    """Parse a library SVG: (w, h, defs_dict, inner_xml)."""
    if ref_id in _LIB:
        return _LIB[ref_id]
    lvl = ref_id.split("-")[1]
    path = os.path.join(ROOT, "svg", lvl, ref_id + ".svg")
    s = open(path, encoding="utf8").read()
    m = re.search(r'viewBox="0 0 ([\d.\-]+) ([\d.\-]+)"', s)
    w, h = float(m.group(1)), float(m.group(2))
    defs = {}
    dm = re.search(r"<defs>(.*?)</defs>", s, re.S)
    if dm:
        for g in re.finditer(r'<(linearGradient|radialGradient) id="([^"]+)".*?</\1>', dm.group(1), re.S):
            defs[g.group(2)] = g.group(0)
    body = re.search(r"</title>\s*(?:<defs>.*?</defs>)?(.*)</svg>", s, re.S).group(1).strip()
    # drop the element's own top-level group wrapper but keep its content
    mm = re.match(r'<g id="%s">(.*)</g>$' % re.escape(ref_id), body, re.S)
    inner = mm.group(1) if mm else body
    _LIB[ref_id] = (w, h, defs, inner)
    return _LIB[ref_id]


def _recolor(xml: str, mp: dict) -> str:
    if not mp:
        return xml
    mp = {k.upper(): v for k, v in mp.items()}

    def rep(m):
        c = m.group(2).upper()
        return f'{m.group(1)}="{mp.get(c, m.group(2))}"'

    return re.sub(r'(fill|stroke|stop-color)="(#[0-9A-Fa-f]{6})"', rep, xml)


def _anchor_off(anchor: str, w: float, h: float):
    v, hz = anchor[0], anchor[1]
    ox = {"l": 0.0, "c": w / 2, "r": w}[hz]
    oy = {"t": 0.0, "c": h / 2, "b": h}[v]
    return ox, oy


def text_width(s, size, weight=400, italic=False, spacing=0.0):
    fam = {300: "Ubuntu Light", 400: "Ubuntu", 500: "Ubuntu Medium", 700: "Ubuntu"}[weight]
    cmap, hm, upm = _font_adv(fam, weight, italic)
    return sum(hm[cmap[ord(c)]][0] for c in s if ord(c) in cmap) * size / upm + spacing * max(len(s) - 1, 0)


class Doc:
    def __init__(self, id: str, title: str, trim: Optional[tuple] = None, bleed: float = 0.0, tight: bool = False):
        self.id, self.title = id, title
        self.trim, self.bleed, self.tight = trim, bleed, tight
        self.ox = self.oy = (0.0 if tight else bleed)
        self.frags: list = []  # xml strings (with nesting handled by _stack)
        self._stack: list = [[]]
        self.defs: dict = {}
        self.built_from: list = []
        self.variables: dict = {}
        self.boxes: list = []
        self.notes: list = []

    # ------------------------------------------------------------ plumbing
    def _emit(self, xml, box=None):
        self._stack[-1].append(xml)
        if box:
            self.boxes.append(box)

    def _p(self, x, y):
        return x + self.ox, y + self.oy

    @contextmanager
    def group(self, gid: str, **attrs):
        """Named group, e.g. variables, cut-contour, guides, or one element of the design."""
        self._stack.append([])
        yield self
        inner = "".join(self._stack.pop())
        a = f' id="{gid}"' if gid else ""
        for k, v in attrs.items():
            a += f' {k.replace("_", "-")}="{_esc(str(v))}"'
        self._stack[-1].append(f"<g{a}>{inner}</g>")

    def _ref(self, ref_id):
        if ref_id not in self.built_from:
            self.built_from.append(ref_id)

    # ------------------------------------------------------------ shapes
    def uses(self, *ids):
        """Record library elements or tokens that are used without being placed as SVG (e.g. tokens, pattern comps)."""
        for i in ids:
            self._ref(i)

    def rect(self, x0, y0, x1, y1, fill=None, rx=0.0, ry=None, stroke=None, sw=None, opacity=None, gid=None, dash=None,
             variable=None, example=None):
        ax, ay = self._p(x0, y0)
        a = f'x="{fmt(ax)}" y="{fmt(ay)}" width="{fmt(x1 - x0)}" height="{fmt(y1 - y0)}"'
        if rx:
            a += f' rx="{fmt(rx)}" ry="{fmt(ry if ry is not None else rx)}"'
        a += f' fill="{fill or "none"}"'
        if opacity is not None and opacity < 0.999:
            a += f' fill-opacity="{fmt(opacity)}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{fmt(sw or 0.25)}"'
            if dash:
                a += f' stroke-dasharray="{dash}"'
        if gid:
            a += f' id="{gid}"'
        if variable:
            a += f' data-variable="{variable}"'
            self.variables[variable] = example if example is not None else fill
        self._emit(f"<rect {a}/>", (ax, ay, ax + x1 - x0, ay + y1 - y0))

    def circle(self, cx, cy, r, fill=None, stroke=None, sw=None, opacity=None, gid=None):
        ax, ay = self._p(cx, cy)
        a = f'cx="{fmt(ax)}" cy="{fmt(ay)}" r="{fmt(r)}" fill="{fill or "none"}"'
        if opacity is not None and opacity < 0.999:
            a += f' fill-opacity="{fmt(opacity)}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{fmt(sw or 0.25)}"'
        if gid:
            a += f' id="{gid}"'
        self._emit(f"<circle {a}/>", (ax - r, ay - r, ax + r, ay + r))

    def line(self, x0, y0, x1, y1, stroke, sw, cap="butt", gid=None):
        ax, ay = self._p(x0, y0)
        bx, by = self._p(x1, y1)
        a = f'x1="{fmt(ax)}" y1="{fmt(ay)}" x2="{fmt(bx)}" y2="{fmt(by)}" stroke="{stroke}" stroke-width="{fmt(sw)}" stroke-linecap="{cap}"'
        if gid:
            a += f' id="{gid}"'
        self._emit(f"<line {a}/>", (min(ax, bx), min(ay, by) - sw / 2, max(ax, bx), max(ay, by) + sw / 2))

    def path(self, d, box, fill=None, stroke=None, sw=None, opacity=None, evenodd=False, gid=None, dx=0.0, dy=0.0):
        """Raw path data in doc coordinates (trim relative). `box` = (x0, y0, x1, y1) of the path in the same space.
        The bleed offset is applied through a translate, so d needs no manual shift."""
        a = f'd="{d}" fill="{fill or "none"}"'
        if evenodd:
            a += ' fill-rule="evenodd"'
        if opacity is not None and opacity < 0.999:
            a += f' fill-opacity="{fmt(opacity)}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{fmt(sw or 0.25)}"'
        if gid:
            a += f' id="{gid}"'
        ax, ay = self._p(0, 0)
        self._emit(f'<path transform="translate({fmt(ax)} {fmt(ay)})" {a}/>', (box[0] + ax, box[1] + ay, box[2] + ax, box[3] + ay))

    # ------------------------------------------------------------ text
    def text(self, x, y, s, size, fill, weight=400, italic=False, anchor="start", spacing=0.0, variable=None,
             rotate=0.0, gid=None, runs=None, example=None):
        """Live Ubuntu text. y is the baseline. `runs` = [(text, weight), ...] writes one line with mixed weights.
        `variable` marks it as a template variable (data-variable) and records the example value."""
        ax, ay = self._p(x, y)
        fam = {300: "Ubuntu Light", 400: "Ubuntu", 500: "Ubuntu Medium", 700: "Ubuntu"}[weight]
        a = f'x="{fmt(ax)}" y="{fmt(ay)}" font-family="{fam}" font-size="{fmt(size)}"'
        if weight == 700:
            a += ' font-weight="bold"'
        if italic:
            a += ' font-style="italic"'
        if abs(spacing) > 1e-4:
            a += f' letter-spacing="{fmt(spacing)}"'
        if anchor != "start":
            a += f' text-anchor="{anchor}"'
        a += f' fill="{fill}"'
        if variable:
            a += f' data-variable="{variable}"'
            self.variables[variable] = example if example is not None else (s if runs is None else "".join(t for t, _ in runs))
        if gid:
            a += f' id="{gid}"'
        if rotate:
            a += f' transform="rotate({fmt(rotate)} {fmt(ax)} {fmt(ay)})"'
        if runs:
            parts = []
            full = ""
            for t, w in runs:
                tt = _esc(t)
                if w == weight:
                    parts.append(tt)
                else:
                    f2 = {300: "Ubuntu Light", 400: "Ubuntu", 500: "Ubuntu Medium", 700: "Ubuntu"}[w]
                    extra = ' font-weight="bold"' if w == 700 else ' font-weight="normal"'
                    parts.append(f'<tspan font-family="{f2}"{extra}>{tt}</tspan>')
                full += t
            body = "".join(parts)
            wd = sum(text_width(t, size, w, italic, spacing) for t, w in runs)
            base = full
        else:
            body = _esc(s)
            wd = text_width(s, size, weight, italic, spacing)
            base = s
        x0 = ax if anchor == "start" else (ax - wd / 2 if anchor == "middle" else ax - wd)
        bx = ink_box(base, fam, weight if weight != 700 else 700, italic, size, ax, ay, spacing, anchor)
        self._emit(f'<text {a} xml:space="preserve">{body}</text>', bx if bx[2] > bx[0] else (x0, ay - size, x0 + wd, ay))
        return text_width

    # ------------------------------------------------------------ library elements
    def place(self, ref_id, x, y, w=None, h=None, scale=None, anchor="tl", recolor=None, opacity=None, rotate=0.0,
              flip_x=False, flip_y=False, gid=None):
        """Place a library SVG. Size by w (mm), h (mm) or scale; (x, y) is where `anchor` of the element lands.
        Returns the placed box (x0, y0, x1, y1) in trim-relative coordinates."""
        ew, eh, defs, inner = lib_svg(ref_id)
        if scale is None:
            if w is not None:
                scale = w / ew
            elif h is not None:
                scale = h / eh
            else:
                scale = 1.0
        sw_, sh_ = ew * scale, eh * scale
        ox, oy = _anchor_off(anchor, sw_, sh_)
        tx, ty = self._p(x - ox, y - oy)
        t = f"translate({fmt(tx)} {fmt(ty)})"
        if rotate:
            t += f" rotate({fmt(rotate)} {fmt(ox)} {fmt(oy)})"
        t += f" scale({fmt(-scale if flip_x else scale)} {fmt(-scale if flip_y else scale)})"
        if flip_x or flip_y:
            t = f"translate({fmt(tx + (sw_ if flip_x else 0))} {fmt(ty + (sh_ if flip_y else 0))})" + (
                f" rotate({fmt(rotate)})" if rotate else "") + f" scale({fmt(-scale if flip_x else scale)} {fmt(-scale if flip_y else scale)})"
        body = _recolor(inner, recolor)
        a = f' data-element="{ref_id}" transform="{t}"'
        if opacity is not None and opacity < 0.999:
            a += f' opacity="{fmt(opacity)}"'
        if gid:
            a += f' id="{gid}"'
        for k, v in defs.items():
            self.defs.setdefault(k, _recolor(v, recolor) if recolor else v)
        self._ref(ref_id)
        corners = [(0, 0), (ew, 0), (ew, eh), (0, eh)]
        ang = math.radians(rotate)
        pts = []
        for cx, cy in corners:
            px, py = cx * scale - ox, cy * scale - oy
            if rotate:
                px, py = px * math.cos(ang) - py * math.sin(ang), px * math.sin(ang) + py * math.cos(ang)
            pts.append((tx + ox + px, ty + oy + py))
        box = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
        self._emit(f"<g{a}>{body}</g>", box)
        return (box[0] - self.ox, box[1] - self.oy, box[2] - self.ox, box[3] - self.oy)

    # ------------------------------------------------------------ print production helpers
    def cut_contour(self, x0, y0, x1, y1, rx=0.0, ry=None, inset=0.2, gid="cut-contour"):
        """ThruCut contour as its own named group: 1 pt magenta stroke, no fill, inset from the trim (source: 0.2 mm)."""
        a, b, c, d = x0 + inset, y0 + inset, x1 - inset, y1 - inset
        ax, ay = self._p(a, b)
        attrs = (f'x="{fmt(ax)}" y="{fmt(ay)}" width="{fmt(c - a)}" height="{fmt(d - b)}" fill="none" '
                 f'stroke="{CUT_COLOR}" stroke-width="{fmt(CUT_WIDTH)}"')
        if rx:
            attrs += f' rx="{fmt(max(rx - inset, 0))}" ry="{fmt(max((ry if ry is not None else rx) - inset, 0))}"'
        self._stack[-1].append(f'<g id="{gid}" data-spot="ThruCut"><rect {attrs}/></g>')
        self.boxes.append((ax, ay, ax + c - a, ay + d - b))

    def placeholder(self, pid, x0, y0, x1, y1, label, variable=None, example=None):
        """Clearly marked placeholder group (dashed magenta outline plus label), e.g. for the QR code."""
        with self.group(f"placeholder-{pid}", data_placeholder=pid):
            self.rect(x0, y0, x1, y1, fill="none", stroke=PH_COLOR, sw=0.4, dash="2 1.5")
            self.text((x0 + x1) / 2, (y0 + y1) / 2 + 1.5, label, size=min(5.0, (y1 - y0) / 3), fill=PH_COLOR, weight=700, anchor="middle")
        if variable:
            self.variables[variable] = example if example is not None else label

    def guides(self, trim_w, trim_h):
        """Hidden trim guide (separate named group, visibility hidden)."""
        ax, ay = self._p(0, 0)
        self._stack[-1].append(
            f'<g id="guides" visibility="hidden"><rect x="{fmt(ax)}" y="{fmt(ay)}" width="{fmt(trim_w)}" height="{fmt(trim_h)}" '
            f'fill="none" stroke="#00A0E0" stroke-width="0.2"/></g>')

    # ------------------------------------------------------------ output
    def svg(self, group_id: Optional[str] = None) -> str:
        body = "".join(self._stack[0])
        gid = group_id or self.id
        if self.tight:
            bs = self.boxes
            x0 = min(b[0] for b in bs); y0 = min(b[1] for b in bs)
            x1 = max(b[2] for b in bs); y1 = max(b[3] for b in bs)
            w, h = x1 - x0, y1 - y0
            body = f'<g transform="translate({fmt(-x0)} {fmt(-y0)})">{body}</g>'
        else:
            tw, th = self.trim
            w, h = tw + 2 * self.bleed, th + 2 * self.bleed
        defs = "<defs>" + "".join(self.defs.values()) + "</defs>" if self.defs else ""
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(w)}mm" height="{fmt(h)}mm" viewBox="0 0 {fmt(w)} {fmt(h)}">\n'
            f"<title>{_esc(self.id + ': ' + self.title)}</title>\n{defs}"
            f'<g id="{gid}">{body}</g>\n</svg>\n'
        )

    def size(self):
        if self.tight:
            bs = self.boxes
            return (max(b[2] for b in bs) - min(b[0] for b in bs), max(b[3] for b in bs) - min(b[1] for b in bs))
        return (self.trim[0] + 2 * self.bleed, self.trim[1] + 2 * self.bleed)
