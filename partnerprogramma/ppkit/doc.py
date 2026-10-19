"""Kleine SVG-bouwer voor templates. Ontwerp in trim-coordinaten (mm); afloop zit eromheen."""
from . import brand
from .brand import esc, face_attrs, PT


class Doc:
    def __init__(self, w, h, title, bleed=3.0, defs="", unit="mm"):
        self.w, self.h, self.bleed, self.title, self.defs, self.unit = w, h, bleed, title, defs, unit
        self.parts = []

    def add(self, s):
        self.parts.append(s)
        return self

    def rect(self, x, y, w, h, fill, rx=0, opacity=None, stroke=None, sw=0.3, extra=""):
        s = f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}"'
        if rx:
            s += f' rx="{rx:.3f}"'
        s += f' fill="{fill}"' if fill else ' fill="none"'
        if opacity is not None:
            s += f' fill-opacity="{opacity}"'
        if stroke:
            s += f' stroke="{stroke}" stroke-width="{sw}"'
        return self.add(s + f" {extra}/>")

    def circle(self, cx, cy, r, fill, opacity=None):
        o = f' fill-opacity="{opacity}"' if opacity is not None else ""
        return self.add(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}" fill="{fill}"{o}/>')

    def line(self, x1, y1, x2, y2, stroke, sw=0.25, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, face, pt, fill, anchor="start", ls=0.0, id=None, size=None):
        """Een regel op basislijn y. {velden} blijven staan tot het vullen. pt in punten, of size in eenheden van het vel."""
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        l = f' letter-spacing="{ls}"' if ls else ""
        i = f' id="{id}"' if id else ""
        return self.add(f'<text{i} x="{x:.3f}" y="{y:.3f}" {face_attrs(face)} font-size="{(size if size else pt * PT):.4f}" fill="{fill}"{a}{l} xml:space="preserve">{s}</text>')

    def flow(self, x, y, w, h, max_pt, min_pt, lh, inner, face="regular", fill=brand.ZWART, align="start", ls=0.0, id=None, valign=None, units=False):
        """Tekstblok dat bij het vullen wordt afgebroken. y is de bovenkant. inner mag <tspan> en <br/> bevatten.
        max_pt en min_pt zijn punten; met units=True zijn het eenheden van het vel (px bij social)."""
        if units:
            max_pt, min_pt = f"{max_pt}u", f"{min_pt}u"
        i = f' id="{id}"' if id else ""
        a = f' data-align="{align}"' if align != "start" else ""
        l = f' letter-spacing="{ls}"' if ls else ""
        a += f' data-valign="{valign}"' if valign else ""
        return self.add(f'<text{i} x="{x:.3f}" y="{y:.3f}" data-flow="{w} {h} {max_pt} {min_pt} {lh}" {face_attrs(face)} '
                        f'fill="{fill}"{a}{l}>{inner}</text>')

    def atom(self, id_, x, y, **kw):
        s, w, h = brand.atom(id_, x, y, **kw)
        self.add(s)
        return w, h

    def svg(self, group_id="art"):
        B = self.bleed
        W, H = self.w + 2 * B, self.h + 2 * B
        defs = f"<defs>{self.defs}</defs>" if self.defs else ""
        return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:g}{self.unit}" height="{H:g}{self.unit}" viewBox="0 0 {W:g} {H:g}">\n'
                f'<title>{esc(self.title)}</title>{defs}\n'
                f'<g id="{group_id}" transform="translate({B:g} {B:g})">{"".join(self.parts)}</g>\n</svg>\n')
