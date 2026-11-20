"""Parkeerpas Bedrijfsschoolgebouw: front in the Philips Stadion pass style, back with the ITF barcode.

Card: ISO CR80, 85.6 x 54 mm trim, 3 mm bleed.
  front  landscape, built from py-atom-illustration-card-pas (gradient, ball pattern, P under a roof,
         'Operated by parkingyou', Philips Stadion logo) scaled up, plus the location name.
  back   portrait, same layout as the physical subscription card (blue header, boven/up arrow,
         barcode at the same height, number pill). Barcode reused from ../psv-parkeerabonnement/build.py.

    python3 -I print-jobs/pas-bedrijfsschoolgebouw/build.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "psv-parkeerabonnement"))
import build as bc  # noqa: E402  barcode helpers (DATA, HUMAN, bars_path, symbol_width)

LOCATION = "Bedrijfsschoolgebouw"
BLUE, AQUA, WHITE = "#1A3580", "#32B9CD", "#FFFFFF"
CW, CH, BLEED = 85.6, 54.0, 3.0  # CR80

ATOM = ROOT / "svg/atom/py-atom-illustration-card-pas.svg"
AW, AH = 33.678, 21.791


def atom_parts():
    """Split the atom into background, 10 percent pattern group, P icon (2 paths) and the rest."""
    s = ATOM.read_text()
    body = s[s.index('<g id="py-atom-illustration-card-pas">') + len('<g id="py-atom-illustration-card-pas">'):s.rindex("</g>")]
    p0 = body.index('<g opacity="0.1">')
    p1 = body.index("</g>", p0) + 4
    pattern = body[p0:p1]
    paths = re.findall(r"<path [^>]*/>", body[p1:])
    return pattern, "".join(paths[:2]), "".join(paths[2:])


def front():
    pattern, p_icon, rest = atom_parts()
    W, H, b = CW, CH, BLEED
    s = W / AW                      # 2.5417, width fits the trim exactly
    dy = (H - AH * s) / 2           # -0.69, centre vertically (crop 0.7 mm top and bottom)
    sp = max((W + 2 * b) / AW, (H + 2 * b) / AH)  # pattern covers the bleed too
    px, py = (W - AW * sp) / 2, (H - AH * sp) / 2
    # P icon: 85 percent, anchored at its top centre (roof top at atom y 2.69, centre x 16.84)
    pk, pcx, ptop = 0.85, 16.84, 2.69
    out = [
        f'<defs><linearGradient id="grad" gradientUnits="userSpaceOnUse" x1="{-b}" y1="{-b}" x2="{(27.735 * s) - b:.3f}" y2="{(27.735 * s) - b:.3f}">'
        f'<stop offset="0" stop-color="#0A699F"/><stop offset="0.5" stop-color="#073D63"/><stop offset="1" stop-color="#030B13"/></linearGradient></defs>',
        f'<rect id="bleed-background" x="{-b}" y="{-b}" width="{W + 2 * b}" height="{H + 2 * b}" fill="url(#grad)"/>',
        f'<g id="pattern-ball-stars" transform="translate({px:.3f} {py:.3f}) scale({sp:.5f})">{pattern}</g>',
        f'<g id="icon-p-roof" transform="translate(0 {dy:.3f}) scale({s:.5f}) translate({pcx} {ptop}) scale({pk}) translate({-pcx} {-ptop})">{p_icon}</g>',
        f'<text id="location-name" data-variable="location-name" x="{W / 2}" y="36.6" font-family="Ubuntu" font-weight="700" '
        f'font-size="5.2" text-anchor="middle" fill="{WHITE}">{LOCATION}</text>',
        f'<g id="footer-logos-line" transform="translate(0 {dy:.3f}) scale({s:.5f})">{rest}</g>',
        f'<g id="guides" display="none"><rect x="0" y="0" width="{W}" height="{H}" rx="3.18" fill="none" stroke="#FF00FF" stroke-width="0.1"/></g>',
    ]
    return wrap("front", W, H, b, "".join(out))


def back():
    """Portrait 54 x 85.6. Positions measured on the photo of the physical card (as fractions of the card)."""
    W, H, b = CH, CW, BLEED
    header_h = 24.5
    out = [
        f'<rect id="bleed-background" x="{-b}" y="{-b}" width="{W + 2 * b}" height="{H + 2 * b}" fill="{WHITE}"/>',
        f'<rect id="header" x="{-b}" y="{-b}" width="{W + 2 * b}" height="{header_h + b}" fill="{BLUE}"/>',
        f'<text id="title" font-family="Ubuntu" fill="{WHITE}" font-size="6.3">'
        f'<tspan x="3.8" y="9.2" font-weight="700">Parkeer</tspan><tspan x="3.8" y="15.6" font-weight="400">Abonnement</tspan></text>',
        f'<text id="location-name" data-variable="location-name" x="3.8" y="21.2" font-family="Ubuntu" font-weight="500" '
        f'font-size="3.4" fill="{AQUA}">{LOCATION}</text>',
    ]
    vw, vh, arrow = inner(ROOT / "svg/atom/py-atom-arrow-up-plain.svg")
    aw = 4.2
    out.append(f'<g id="arrow-up" transform="translate({W / 2 - aw / 2:.3f} 31.5) scale({aw / vw:.5f})">{arrow}</g>')
    out.append(f'<text id="boven-up" x="{W / 2}" y="{31.5 + aw * vh / vw + 3.4:.3f}" font-family="Ubuntu" font-size="2.6" '
               f'text-anchor="middle" fill="{BLUE}">boven/up</text>')
    # barcode: same size and height as on the physical card (about 39.5 x 16.7 mm, top at 65 percent)
    narrow, bh, by = 0.26, 16.7, 55.7
    sw = bc.symbol_width(narrow)
    bx = (W - sw) / 2
    d, _ = bc.bars_path(bx, by, narrow, bh)
    out.append(f'<path id="barcode-itf" data-value="{bc.DATA}" d="{d}" fill="#000000"/>')
    pw, ph, pcy = 18.0, 4.0, 78.3
    out.append(f'<rect id="number-pill" x="{(W - pw) / 2:.3f}" y="{pcy - ph / 2:.3f}" width="{pw}" height="{ph}" rx="1" fill="{AQUA}" fill-opacity="0.1"/>')
    out.append(f'<text id="number" data-variable="card-number" x="{W / 2}" y="{pcy + 0.75:.3f}" font-family="Ubuntu" font-weight="500" '
               f'font-size="2.2" letter-spacing="0.2" text-anchor="middle" fill="#1D1D1B">{bc.HUMAN}</text>')
    out.append(f'<g id="guides" display="none"><rect x="0" y="0" width="{W}" height="{H}" rx="3.18" fill="none" stroke="#FF00FF" stroke-width="0.1"/></g>')
    return wrap("back", W, H, b, "".join(out))


def inner(path):
    s = Path(path).read_text()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    body = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
    return float(vb.group(1)), float(vb.group(2)), re.sub(r"<title>.*?</title>", "", body, flags=re.S)


def wrap(side, W, H, b, content):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2 * b}mm" height="{H + 2 * b}mm" viewBox="{-b} {-b} {W + 2 * b} {H + 2 * b}">
<title>Parkeerpas {LOCATION} {side}</title>
<g id="pas-bedrijfsschoolgebouw-{side}">{content}</g>
</svg>
"""


if __name__ == "__main__":
    (HERE / "pas-bedrijfsschoolgebouw-voorkant.svg").write_text(front())
    (HERE / "pas-bedrijfsschoolgebouw-achterkant.svg").write_text(back())
    print("written to", HERE)
