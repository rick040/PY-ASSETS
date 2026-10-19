"""Tekstomslag en passend maken voor SVG-templates (cairosvg breekt zelf geen regels af).

In een template markeert u een <text> met data-flow="breedte hoogte [max-pt] [min-pt] [regelhoogte]" (mm en punten).
Binnen het element mogen <tspan font-weight=... fill=...> en <br/> staan. {velden} worden eerst ingevuld.
Tekst tussen [haken] krijgt automatisch een oranje markering: placeholders blijven zichtbaar tot ze zijn ingevuld.
"""
import re
from . import brand
from .brand import esc, face_attrs, text_width, PT

PLACEHOLDER_HL = brand.ORANJE


def _style_face(attrs, base_face):
    """Bepaal het face van een run uit font-family / font-weight attributen."""
    fam = attrs.get("font-family")
    wt = attrs.get("font-weight")
    if fam is None and wt is None:
        return base_face
    if fam == "Ubuntu Medium":
        return "medium"
    if fam == "Ubuntu Light":
        return "light"
    if wt == "bold":
        return "bold"
    if wt in ("normal", "400") or fam == "Ubuntu":
        return "regular"
    return base_face


def tokenize(runs):
    """runs: lijst (tekst, {face, fill}); geeft woorden (tekst, style, spatie_erachter, placeholder) en harde breaks (None)."""
    out = []
    in_br = False
    for text, st in runs:
        if text is None:
            out.append(None)
            continue
        for part in re.split(r"(\n)", text):
            if part == "\n":
                out.append(None)
                continue
            if out and out[-1] is not None and part[:1] in " \t" and not out[-1][2]:
                w0, s0, _, p0 = out[-1]
                out[-1] = (w0, s0, True, p0)
            for m in re.finditer(r"([^ \t\n]+)([ \t]*)", part):
                word, sp = m.group(1), m.group(2)
                ph = in_br
                if "[" in word:
                    in_br = True
                    ph = True
                if "]" in word and in_br and word.rfind("]") >= word.rfind("["):
                    in_br = False
                    ph = True
                out.append((word, st, bool(sp), ph))
    return out


def layout(runs, width, size, ls=0.0):
    """Verdeel over regels. size in mm. Geeft lijst regels; regel = lijst segmenten (tekst, style, x, breedte, ph)."""
    toks = tokenize(runs)
    lines, cur, x = [], [], 0.0

    def flush():
        nonlocal cur, x
        lines.append(cur)
        cur, x = [], 0.0

    def push(tok_text, st, ph):
        nonlocal x
        w = text_width(tok_text, st["face"], size, ls)
        if cur and cur[-1][1] is st and cur[-1][4] == ph:
            t, s0, x0, w0, p0 = cur[-1]
            cur[-1] = (t + tok_text, s0, x0, w0 + w, p0)
        else:
            cur.append((tok_text, st, x, w, ph))
        x += w

    units = []
    for t in toks:
        if t is None:
            units.append(None)
        elif units and units[-1] is not None and not units[-1][-1][2]:
            units[-1].append(t)          # geen spatie ertussen (bv. vet woord plus komma): niet los van elkaar afbreken
        else:
            units.append([t])
    for u in units:
        if u is None:
            flush()
            continue
        ww = sum(text_width(w, st["face"], size, ls) for w, st, _, _ in u)
        if cur and x + ww > width + 1e-6:
            last = cur[-1]
            if last[0].endswith(" "):
                cur[-1] = (last[0][:-1], last[1], last[2], last[3] - text_width(" ", last[1]["face"], size, ls), last[4])
            flush()
        for word, st, sp, ph in u:
            push(word + (" " if sp else ""), st, ph)
        if ww > width + 1e-6:
            raise ValueError(f"woord past niet in de breedte: {''.join(w for w, *_ in u)!r} ({ww:.1f} > {width:.1f} mm)")
    if cur:
        last = cur[-1]
        if last[0].endswith(" "):
            cur[-1] = (last[0][:-1], last[1], last[2], last[3] - text_width(" ", last[1]["face"], size, ls), last[4])
        flush()
    return lines


def fit(runs, width, height, max_pt, min_pt, lh, ls=0.0):
    pt = max_pt
    while pt >= min_pt - 1e-9:
        size = pt * PT
        try:
            lines = layout(runs, width, size, ls)
        except ValueError:
            lines = None
        if lines is not None and len(lines) * size * lh <= height + 1e-6:
            return pt, lines
        pt -= 0.25
    raise ValueError(f"tekst past niet in {width} x {height} mm op {min_pt} pt: {''.join(t or ' ' for t, _ in runs)[:60]!r}")


def render(lines, x, y, size, lh, fill, align="start", width=0.0, ls=0.0, hl_pad=0.4):
    """SVG voor de regels. y is de bovenkant van het blok; de basislijn van regel 1 ligt op y + 0.8 * size."""
    out = []
    for i, line in enumerate(lines):
        total = sum(s[3] for s in line)
        off = 0.0 if align == "start" else (width - total) / (2 if align == "middle" else 1)
        base = y + i * size * lh + size * (0.5 + 0.5 * lh) * 0.8 + (lh - 1) * 0  # basislijn
        base = y + i * size * lh + size * ((lh - 1) / 2 + 0.80)
        for t, st, sx, sw, ph in line:
            if ph:
                out.append(f'<rect x="{x + off + sx - hl_pad:.3f}" y="{base - size * 0.82:.3f}" width="{sw + 2 * hl_pad:.3f}" '
                           f'height="{size * 1.1:.3f}" rx="{size * 0.2:.3f}" fill="{PLACEHOLDER_HL}" fill-opacity="0.32" stroke="{PLACEHOLDER_HL}" stroke-width="0.2" stroke-dasharray="0.8 0.5" data-placeholder="1"/>')
        segs = ""
        for t, st, sx, sw, ph in line:
            col = st["fill"] or fill
            if ph:
                col = st.get("ph_fill") or col
            segs += (f'<tspan {face_attrs(st["face"])} fill="{col}">{esc(t).replace(chr(160), " ")}</tspan>')
        ls_attr = f' letter-spacing="{ls}"' if ls else ""
        out.append(f'<text x="{x + off:.3f}" y="{base:.3f}" font-size="{size:.4f}"{ls_attr} xml:space="preserve">{segs}</text>')
    return "".join(out)
