"""Toegangspas Bedrijfsschoolgebouw: Philips Stadion pass style on both sides, ITF barcode on the back.

Card: ISO CR80, 85.6 x 54 mm trim, 3 mm bleed.
  Toegangspas for stadium staff on match days (not a parking subscription).
  front  landscape, built from py-atom-illustration-card-pas (gradient, ball pattern, P without the roof,
         'Operated by parkingyou', Philips Stadion logo) scaled up, plus label and location name.
  back   landscape, same stadium background, footer line and logos as the front; ITF barcode on a white panel,
         usage line. Barcode reused from ../psv-parkeerabonnement/build.py.

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
LABEL = "Toegangspas"
USAGE = "Alleen voor stadionmedewerkers op wedstrijddagen"
BLUE, AQUA, WHITE = "#1A3580", "#32B9CD", "#FFFFFF"
CW, CH, BLEED = 85.6, 54.0, 3.0  # CR80

ATOM = ROOT / "svg/atom/py-atom-illustration-card-pas.svg"
AW, AH = 33.678, 21.791


def atom_parts():
    """Split the atom into the 10 percent pattern group, the P (path 0), the roof (path 1, not used) and the rest."""
    s = ATOM.read_text()
    tag = '<g id="py-atom-illustration-card-pas">'
    body = s[s.index(tag) + len(tag):s.rindex("</g>")]
    p0 = body.index('<g opacity="0.1">')
    p1 = body.index("</g>", p0) + 4
    paths = re.findall(r"<path [^>]*/>", body[p1:])
    return body[p0:p1], paths[0], "".join(paths[2:])


# P bounds in atom units (path 0): x 14.576 to 19.422, y 7.055 to 13.588
P_X0, P_X1, P_Y0, P_Y1 = 14.576, 19.422, 7.055, 13.588


def base(W, H, b):
    """Shared stadium background: gradient, ball and star pattern, footer line with both logos (same place on both sides)."""
    pattern, p_path, rest = atom_parts()
    s = W / AW
    dy = (H - AH * s) / 2
    sp = max((W + 2 * b) / AW, (H + 2 * b) / AH)
    px, py = (W - AW * sp) / 2, (H - AH * sp) / 2
    bg = (
        f'<defs><linearGradient id="grad" gradientUnits="userSpaceOnUse" x1="{-b}" y1="{-b}" x2="{(27.735 * s) - b:.3f}" y2="{(27.735 * s) - b:.3f}">'
        f'<stop offset="0" stop-color="#0A699F"/><stop offset="0.5" stop-color="#073D63"/><stop offset="1" stop-color="#030B13"/></linearGradient></defs>'
        f'<rect id="bleed-background" x="{-b}" y="{-b}" width="{W + 2 * b}" height="{H + 2 * b}" fill="url(#grad)"/>'
        f'<g id="pattern-ball-stars" transform="translate({px:.3f} {py:.3f}) scale({sp:.5f})">{pattern}</g>'
    )
    footer = f'<g id="footer-logos-line" transform="translate(0 {dy:.3f}) scale({s:.5f})">{rest}</g>'
    return bg, footer, p_path


def p_icon(p_path, cx, top, height, gid="icon-p"):
    k = height / (P_Y1 - P_Y0)
    x = cx - k * (P_X1 - P_X0) / 2
    return f'<g id="{gid}" transform="translate({x:.3f} {top:.3f}) scale({k:.5f}) translate({-P_X0} {-P_Y0})">{p_path}</g>'


def guides(W, H):
    return f'<g id="guides" display="none"><rect x="0" y="0" width="{W}" height="{H}" rx="3.18" fill="none" stroke="#FF00FF" stroke-width="0.1"/></g>'


def front():
    W, H, b = CW, CH, BLEED
    bg, footer, p_path = base(W, H, b)
    out = [
        bg,
        p_icon(p_path, W / 2, 4.6, 19.0),
        f'<text id="label" x="{W / 2}" y="29.4" font-family="Ubuntu" font-weight="500" font-size="3.2" letter-spacing="0.25" '
        f'text-anchor="middle" fill="{AQUA}">{LABEL}</text>',
        f'<text id="location-name" data-variable="location-name" x="{W / 2}" y="36.4" font-family="Ubuntu" font-weight="700" '
        f'font-size="5.2" text-anchor="middle" fill="{WHITE}">{LOCATION}</text>',
        footer,
        guides(W, H),
    ]
    return wrap("front", W, H, b, "".join(out))


def back():
    """Landscape like the front: same background, footer line and logos; barcode on a white panel."""
    W, H, b = CW, CH, BLEED
    bg, footer, p_path = base(W, H, b)
    x0, x1 = 5.134, 80.466                      # ends of the footer line (atom 2.02 and 31.658)
    out = [
        bg,
        f'<text id="label" x="{x0}" y="9.0" font-family="Ubuntu" font-weight="700" font-size="5.6" fill="{WHITE}">{LABEL}</text>',
        f'<text id="location-name" data-variable="location-name" x="{x0}" y="13.6" font-family="Ubuntu" font-weight="500" '
        f'font-size="3.2" fill="{AQUA}">{LOCATION}</text>',
        p_icon(p_path, x1 - 3.0, 4.2, 9.4, "icon-p-small"),
    ]
    # white panel with the barcode (quiet zone included) and the number
    py0, py1 = 16.6, 34.4
    out.append(f'<rect id="barcode-panel" x="{x0}" y="{py0}" width="{x1 - x0:.3f}" height="{py1 - py0:.3f}" rx="1.6" fill="{WHITE}"/>')
    narrow, bh, by = 0.36, 12.0, py0 + 1.8
    sw = bc.symbol_width(narrow)
    bx = (W - sw) / 2
    d, _ = bc.bars_path(bx, by, narrow, bh)
    out.append(f'<path id="barcode-itf" data-value="{bc.DATA}" d="{d}" fill="#000000"/>')
    out.append(f'<text id="number" data-variable="card-number" x="{W / 2}" y="{py1 - 1.5:.3f}" font-family="Ubuntu" font-weight="500" '
               f'font-size="2.3" letter-spacing="0.3" text-anchor="middle" fill="#1D1D1B">{bc.HUMAN}</text>')
    out.append(f'<text id="usage" x="{x0}" y="38.4" font-family="Ubuntu" font-weight="400" font-size="2.35" fill="{WHITE}">'
               f'{USAGE}</text>')
    out += [footer, guides(W, H)]
    return wrap("back", W, H, b, "".join(out))


def inner(path):
    s = Path(path).read_text()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    body = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
    return float(vb.group(1)), float(vb.group(2)), re.sub(r"<title>.*?</title>", "", body, flags=re.S)


def wrap(side, W, H, b, content):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2 * b}mm" height="{H + 2 * b}mm" viewBox="{-b} {-b} {W + 2 * b} {H + 2 * b}">
<title>Toegangspas {LOCATION} {side}</title>
<g id="pas-bedrijfsschoolgebouw-{side}">{content}</g>
</svg>
"""


if __name__ == "__main__":
    (HERE / "pas-bedrijfsschoolgebouw-voorkant.svg").write_text(front())
    (HERE / "pas-bedrijfsschoolgebouw-achterkant.svg").write_text(back())
    print("written to", HERE)
