"""Build the PSV parkeerabonnement barcode (ITF) as vector SVG plus an A5 print layout.

The barcode was decoded from a photo of the physical card: ITF (Interleaved 2 of 5),
data 995840000972914286 (18 digits, no extra check digit). The card prints only the
last nine digits (972914286) as human readable text.

    python3 -I print-jobs/psv-parkeerabonnement/build.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

DATA = "995840000972914286"
HUMAN = "972914286"

BLUE = "#1A3580"   # PY-Blauw (tokens.json)
AQUA = "#32B9CD"   # PY-Aqua
BAR = "#000000"    # barcodes always in pure black (K100) for scanner contrast

# ITF digit patterns: 1 = wide, 0 = narrow (5 elements per digit)
ITF = {
    "0": "00110", "1": "10001", "2": "01001", "3": "11000", "4": "00101",
    "5": "10100", "6": "01100", "7": "00011", "8": "10010", "9": "01010",
}


def itf_runs(data, ratio):
    """Return list of (is_bar, width_in_narrow_modules) for the full symbol."""
    assert len(data) % 2 == 0 and data.isdigit()
    runs = [(True, 1), (False, 1), (True, 1), (False, 1)]          # start
    for a, b in zip(data[0::2], data[1::2]):
        for wa, wb in zip(ITF[a], ITF[b]):                          # bars from a, spaces from b
            runs.append((True, ratio if wa == "1" else 1))
            runs.append((False, ratio if wb == "1" else 1))
    runs += [(True, ratio), (False, 1), (True, 1)]                  # stop
    return runs


def bars_path(x0, y0, narrow, height, ratio=2.5):
    """SVG path data with one rectangle per bar, coordinates in mm."""
    x, parts = x0, []
    for is_bar, w in itf_runs(DATA, ratio):
        w_mm = w * narrow
        if is_bar:
            parts.append(f"M{x:.4f} {y0:.4f}h{w_mm:.4f}v{height:.4f}h{-w_mm:.4f}z")
        x += w_mm
    return "".join(parts), x - x0


def symbol_width(narrow, ratio=2.5):
    return sum(w for _, w in itf_runs(DATA, ratio)) * narrow


def svg_barcode(narrow=0.5, height=25.0, quiet=10):
    """Bars only, white background including the ITF quiet zone (10x narrow each side)."""
    qz = quiet * narrow
    w = symbol_width(narrow) + 2 * qz
    d, _ = bars_path(qz, 0, narrow, height)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w:.3f}mm" height="{height:.3f}mm" viewBox="0 0 {w:.3f} {height:.3f}">
<title>ITF {DATA}</title>
<desc>Interleaved 2 of 5, data {DATA}, narrow bar {narrow} mm, wide:narrow 2.5:1, quiet zone {qz} mm each side included.</desc>
<rect id="quiet-zone" x="0" y="0" width="{w:.3f}" height="{height:.3f}" fill="#FFFFFF"/>
<path id="bars" d="{d}" fill="{BAR}"/>
</svg>
"""


def svg_barcode_with_number(narrow=0.5, height=25.0, quiet=10, text_size=4.2, gap=2.5):
    qz = quiet * narrow
    w = symbol_width(narrow) + 2 * qz
    total_h = height + gap + text_size * 1.1
    d, _ = bars_path(qz, 0, narrow, height)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w:.3f}mm" height="{total_h:.3f}mm" viewBox="0 0 {w:.3f} {total_h:.3f}">
<title>ITF {DATA} met nummer</title>
<rect id="background" x="0" y="0" width="{w:.3f}" height="{total_h:.3f}" fill="#FFFFFF"/>
<path id="bars" d="{d}" fill="{BAR}"/>
<text id="human-readable" x="{w / 2:.3f}" y="{height + gap + text_size * 0.8:.3f}" font-family="Ubuntu" font-weight="500" font-size="{text_size}" letter-spacing="0.4" text-anchor="middle" fill="#1D1D1B">{HUMAN}</text>
</svg>
"""


def inner(svg_file):
    """Return (viewBox w, h, inner markup) of a library SVG."""
    import re
    s = (ROOT / svg_file).read_text()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    body = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
    body = re.sub(r"<title>.*?</title>", "", body, flags=re.S)
    return float(vb.group(1)), float(vb.group(2)), body


def place(svg_file, x, y, w=None, h=None, recolor=None):
    vw, vh, body = inner(svg_file)
    s = w / vw if w else h / vh
    if recolor:
        for a, b in recolor.items():
            body = body.replace(a, b)
    return f'<g transform="translate({x:.3f} {y:.3f}) scale({s:.5f})">{body}</g>', vw * s, vh * s


def svg_a5(bleed=3.0):
    """A5 portrait (148 x 210 mm trim, 3 mm bleed), card design scaled up."""
    W, H = 148.0, 210.0
    b = bleed
    header_h = 62.0
    out = []
    out.append(f'<rect id="bleed-background" x="{-b}" y="{-b}" width="{W + 2 * b}" height="{H + 2 * b}" fill="#FFFFFF"/>')
    out.append(f'<rect id="header" x="{-b}" y="{-b}" width="{W + 2 * b}" height="{header_h + b}" fill="{BLUE}"/>')
    # title, two lines like the card
    out.append(f'<text id="title" font-family="Ubuntu" fill="#FFFFFF" font-size="15">'
               f'<tspan x="14" y="31" font-weight="700">Parkeer</tspan>'
               f'<tspan x="14" y="49" font-weight="400">Abonnement</tspan></text>')
    # logo (reverse) in the header, right side
    g, lw, lh = place("svg/atom/py-atom-logo-beeldmerk-white.svg", 0, 0, h=20)
    out.append(f'<g id="logo" transform="translate({W - 14 - lw:.3f} {header_h / 2 - lh / 2:.3f})">{g}</g>')
    # arrow up + boven/up (scan direction)
    g, aw, ah = place("svg/atom/py-atom-arrow-up-plain.svg", W / 2 - 6, 80, w=12)
    out.append(f'<g id="arrow-up">{g}</g>')
    out.append(f'<text id="boven-up" x="{W / 2}" y="{80 + ah + 8:.3f}" font-family="Ubuntu" font-weight="400" font-size="7" '
               f'text-anchor="middle" fill="{BLUE}">boven/up</text>')
    # barcode: narrow 0.55 mm -> symbol 83.9 mm, quiet zone 5.5 mm each side
    narrow, bh = 0.55, 34.0
    sw = symbol_width(narrow)
    bx, by = (W - sw) / 2, 130.0
    d, _ = bars_path(bx, by, narrow, bh)
    qz = 10 * narrow
    out.append(f'<rect id="quiet-zone" x="{bx - qz:.3f}" y="{by:.3f}" width="{sw + 2 * qz:.3f}" height="{bh}" fill="#FFFFFF"/>')
    out.append(f'<path id="barcode-itf" data-value="{DATA}" d="{d}" fill="{BAR}"/>')
    # number pill
    pw, ph, py = 46.0, 10.0, by + bh + 6
    out.append(f'<rect id="number-pill" x="{(W - pw) / 2:.3f}" y="{py:.3f}" width="{pw}" height="{ph}" rx="{ph / 2}" fill="{AQUA}" fill-opacity="0.1"/>')
    out.append(f'<text id="number" data-variable="card-number" x="{W / 2}" y="{py + ph / 2 + 1.75:.3f}" font-family="Ubuntu" '
               f'font-weight="500" font-size="5" letter-spacing="0.5" text-anchor="middle" fill="#1D1D1B">{HUMAN}</text>')
    # trim guides (hidden)
    out.append(f'<g id="guides" display="none"><rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#FF00FF" stroke-width="0.1"/></g>')
    vb = f"{-b} {-b} {W + 2 * b} {H + 2 * b}"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2 * b}mm" height="{H + 2 * b}mm" viewBox="{vb}">
<title>Parkeerabonnement A5 (PSV), ITF {DATA}</title>
<g id="parkeerabonnement-a5">{''.join(out)}</g>
</svg>
"""


if __name__ == "__main__":
    (HERE / f"barcode-itf-{DATA}.svg").write_text(svg_barcode())
    (HERE / f"barcode-itf-{DATA}-met-nummer.svg").write_text(svg_barcode_with_number())
    (HERE / "parkeerabonnement-a5.svg").write_text(svg_a5())
    print("written to", HERE)
