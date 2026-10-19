"""GLOW 2026 social posts for ParkingYou.

Builds every feed post, carrousel slide, story frame and reel card described in the
Notion page "GLOW 2026" (Social Posts database) from the elements in this repo.

    python3 -I social/glow-2026/build.py

Writes one SVG (editable source, live Ubuntu text) and one PNG per frame to
social/glow-2026/out/. Needs Python 3 with playwright (Chromium) and the Ubuntu
fonts from fonts/ installed.
"""
import pathlib
import random
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent / "out"

# Brand tokens (tokens.json, handbook 1.3)
BLAUW, AQUA, ORANJE, GRIJS, WIT = "#1A3580", "#32B9CD", "#F08300", "#AEAEAE", "#FFFFFF"
# Campaign night tones, darkened from PY-Blauw. Not brand colours, only for the Glow backgrounds.
NACHT, NACHT_DIEP = "#0E1E4D", "#060D24"

LOCATIES = ["TD-gebouw", "DLL", "Bedrijfsschoolgebouw", "Evoluon", "Philips Stadion"]

_uid = [0]


def element(eid, x, y, w=None, h=None, cls="", extra=""):
    """Place a repo SVG element at x, y scaled to width w or height h (px)."""
    level = eid.split("-")[1]
    src = (ROOT / "svg" / level / f"{eid}.svg").read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    _, _, vw, vh = [float(v) for v in vb.split()]
    if w is None:
        w = h * vw / vh
    if h is None:
        h = w * vh / vw
    inner = src.split(">", 2)[2] if src.startswith("<?xml") else src.split(">", 1)[1]
    inner = inner.rsplit("</svg>", 1)[0]
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    _uid[0] += 1
    p = f"e{_uid[0]}-"
    inner = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', inner)
    inner = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{p}{m.group(1)})", inner)
    inner = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{p}{m.group(1)}"', inner)
    return (f'<svg x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" viewBox="{vb}" '
            f'class="{cls}" overflow="visible" {extra}>{inner}</svg>')


STYLE = """<style>
.wit path,.wit circle,.wit rect,.wit polygon,.wit ellipse{fill:#FFFFFF}
.aqua path,.aqua circle,.aqua rect,.aqua polygon{fill:#32B9CD}
.oranje path,.oranje circle,.oranje rect,.oranje polygon{fill:#F08300}
text{font-family:Ubuntu}
.l{font-family:'Ubuntu Light'}
.m{font-family:'Ubuntu Medium'}
.b{font-weight:700}
</style>"""

DEFS = f"""<defs>
<filter id="blur-s" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="blur-m" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>
<filter id="blur-l" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="70"/></filter>
<filter id="blur-xl" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="140"/></filter>
<radialGradient id="nacht" cx="50%" cy="38%" r="75%">
  <stop offset="0" stop-color="{NACHT}"/><stop offset="1" stop-color="{NACHT_DIEP}"/></radialGradient>
<linearGradient id="verloop" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{BLAUW}"/><stop offset="0.18" stop-color="{BLAUW}"/>
  <stop offset="0.62" stop-color="#097BAE"/><stop offset="1" stop-color="{AQUA}"/></linearGradient>
<linearGradient id="bundel" x1="0" y1="1" x2="0" y2="0">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.55"/>
  <stop offset="1" stop-color="{AQUA}" stop-opacity="0"/></linearGradient>
<linearGradient id="fade-up" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{NACHT_DIEP}" stop-opacity="0"/>
  <stop offset="1" stop-color="{NACHT_DIEP}" stop-opacity="0.9"/></linearGradient>
</defs>"""


def background(w, h, seed=1, glows=None):
    """Night sky with soft light glows and light specks."""
    rnd = random.Random(seed)
    parts = [f'<rect width="{w}" height="{h}" fill="url(#nacht)"/>']
    for gx, gy, r, col, op in glows or []:
        parts.append(f'<circle cx="{gx}" cy="{gy}" r="{r}" fill="{col}" opacity="{op}" filter="url(#blur-xl)"/>')
    for _ in range(int(w * h / 9000)):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.choice([1.2, 1.6, 2.2, 3])
        col = rnd.choice([WIT, WIT, AQUA, ORANJE])
        parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}" opacity="{rnd.uniform(0.15, 0.6):.2f}"/>')
    return "".join(parts)


def glow_text(x, y, txt, size, fill=WIT, cls="b", anchor="start", glow=None, strength="m", extra=""):
    glow = glow or fill
    attrs = f'x="{x}" y="{y}" font-size="{size}" class="{cls}" text-anchor="{anchor}" {extra}'
    return (f'<text {attrs} fill="{glow}" opacity="0.85" filter="url(#blur-{strength})">{txt}</text>'
            f'<text {attrs} fill="{fill}">{txt}</text>')


def text(x, y, txt, size, fill=WIT, cls="", anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}" fill="{fill}" text-anchor="{anchor}" {extra}>{txt}</text>'


def pill(x, y, label, size=34, bg=WIT, fg=BLAUW, cls="b", pad=34, h=None, anchor="start", icon=None, w=None):
    """Rounded pill, width estimated from the label (Ubuntu Bold ~0.56 em per glyph)."""
    h = h or size * 2
    est = len(label) * size * (0.56 if "b" in cls else 0.5)
    iw = h * 0.62 if icon else 0
    w = w or est + 2 * pad + (iw + 14 if icon else 0)
    if anchor == "middle":
        x = x - w / 2
    out = [f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{h / 2:.0f}" fill="{bg}"/>']
    tx = x + pad
    if icon:
        out.append(icon(x + pad * 0.7, y + (h - iw) / 2, iw))
        tx += iw + 14 - pad * 0.3
    out.append(text(tx, y + h / 2 + size * 0.36, label, size, fg, cls))
    return "".join(out), w


def url_tag(x, y, scale=1.0, anchor="start"):
    """parkingyou.nl tag in the style of py-comp-url-tag-chevron (white plate, blue text, aqua chevron)."""
    w, h = 400 * scale, 82 * scale
    if anchor == "middle":
        x -= w / 2
    s = 38 * scale
    return (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{10 * scale:.0f}" fill="{WIT}"/>'
            f'<text x="{x + 26 * scale:.0f}" y="{y + h / 2 + s * 0.36:.0f}" font-size="{s:.0f}" fill="{BLAUW}">'
            f'<tspan class="b">parking</tspan><tspan class="b">you</tspan><tspan class="l">.nl</tspan></text>'
            f'<path d="M{x + w - 62 * scale:.0f} {y + 20 * scale:.0f} l{20 * scale:.0f} {21 * scale:.0f} '
            f'l{-20 * scale:.0f} {21 * scale:.0f}" stroke="{AQUA}" stroke-width="{9 * scale:.0f}" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def footer(w, h, y=None, cta=True, logo_w=300):
    y = h - 135 if y is None else y
    out = element("py-atom-logo-horizontal-white", 80, y, w=logo_w)
    if cta:
        out += url_tag(w - 80 - 400 * 0.85, y + 4, 0.85)
    return out


def date_chip(x, y, label="Glow · 7 t/m 14 november", anchor="start", size=30):
    s, w = pill(x, y, label, size=size, bg="none", fg=WIT, cls="m", anchor=anchor)
    box_x = x - w / 2 if anchor == "middle" else x
    return (f'<rect x="{box_x:.0f}" y="{y}" width="{w:.0f}" height="{size * 2}" rx="{size}" fill="{WIT}" '
            f'fill-opacity="0.08" stroke="{AQUA}" stroke-width="2.5"/>') + s


def bubble(x, y, w, fill=AQUA, glow=True):
    """Brand speech bubble (py-atom-shape-bubble-solid), recoloured, with an optional glow."""
    cls = {AQUA: "aqua", ORANJE: "oranje", WIT: "wit"}[fill]
    out = ""
    if glow:
        out += f'<g filter="url(#blur-l)" opacity="0.8">{element("py-atom-shape-bubble-solid", x, y, w=w, cls=cls)}</g>'
    return out + element("py-atom-shape-bubble-solid", x, y, w=w, cls=cls)


def struck(x, y, txt, size, col=GRIJS, anchor="start", rot=-8):
    est = len(txt) * size * 0.58
    x0 = x - est / 2 if anchor == "middle" else x
    return (text(x, y, txt, size, col, "b", anchor, 'opacity="0.75"') +
            f'<line x1="{x0 - 12:.0f}" y1="{y - size * 0.3:.0f}" x2="{x0 + est + 12:.0f}" y2="{y - size * 0.36:.0f}" '
            f'stroke="{ORANJE}" stroke-width="{size * 0.09:.0f}" stroke-linecap="round" '
            f'transform="rotate({rot} {x0 + est / 2:.0f} {y - size * 0.33:.0f})"/>')


def route(points, col=ORANJE, width=8, dash="2 22", glow=True):
    d = "M" + " ".join(f"{px},{py}" for px, py in points[:1])
    for i in range(1, len(points) - 1, 2):
        (cx, cy), (ex, ey) = points[i], points[i + 1]
        d += f" Q{cx},{cy} {ex},{ey}"
    out = ""
    if glow:
        out += f'<path d="{d}" stroke="{col}" stroke-width="{width * 3}" fill="none" opacity="0.45" filter="url(#blur-m)"/>'
    return out + (f'<path d="{d}" stroke="{col}" stroke-width="{width}" fill="none" '
                  f'stroke-dasharray="{dash}" stroke-linecap="round"/>')


def canvas(w, h, body, transparent=False):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'{STYLE}{DEFS}{"" if transparent else ""}{body}</svg>')


# ---------------------------------------------------------------- feed posts 1080x1350

FW, FH = 1080, 1350


def post_a():
    b = background(FW, FH, 11, [(300, 420, 330, AQUA, 0.55), (860, 1000, 280, ORANJE, 0.35)])
    b += date_chip(80, 90)
    b += bubble(70, 210, 500)
    b += text(320, 545, "€15", 210, WIT, "b", "middle", 'transform="rotate(-6 320 480)"')
    b += text(320, 620, "vooraf", 44, WIT, "m", "middle", 'transform="rotate(-6 320 600)"')
    b += text(640, 470, "in plaats van", 50, WIT, "l")
    b += struck(640, 640, "€20", 190)
    b += text(80, 930, "Reserveer je", 88, WIT, "l")
    b += glow_text(80, 1035, "Glow-plek vooraf", 88, AQUA, "b", strength="s")
    b += footer(FW, FH)
    return canvas(FW, FH, b)


def facade(x, y, w, h, seed=3):
    rnd = random.Random(seed)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0A1638"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="6" fill="{AQUA}" opacity="0.35"/>']
    cols, rows = 9, 7
    cw, rh = w / cols, (h - 40) / rows
    for r in range(rows):
        for c in range(cols):
            lit = rnd.random() < 0.18
            col = "#F6C46A" if lit else "#13224F"
            out.append(f'<rect x="{x + c * cw + 14:.0f}" y="{y + 30 + r * rh:.0f}" width="{cw - 28:.0f}" '
                       f'height="{rh - 26:.0f}" fill="{col}" opacity="{0.7 if lit else 1}"/>')
    return "".join(out)


def walkers(y, xs, h=120, cls="wit", op=0.95):
    out = ""
    figs = ["py-atom-figure-walk", "py-atom-figure-bags-walk", "py-atom-figure-walk", "py-atom-figure-point"]
    for i, x in enumerate(xs):
        out += f'<g opacity="{op}">{element(figs[i % len(figs)], x, y, h=h, cls=cls)}</g>'
    return out


def post_b():
    b = background(FW, FH, 21, [(540, 760, 380, AQUA, 0.45), (180, 260, 220, ORANJE, 0.25)])
    b += facade(110, 520, 860, 600)
    # projector beam from the street onto the facade
    b += '<polygon points="500,1210 580,1210 930,560 150,560" fill="url(#bundel)" opacity="0.55"/>'
    b += f'<g filter="url(#blur-l)" opacity="0.9">{element("py-atom-logo-beeldmerk-white", 410, 560, w=260, cls="aqua")}</g>'
    b += f'<g opacity="0.92">{element("py-atom-logo-beeldmerk-white", 410, 560, w=260)}</g>'
    b += f'<rect x="0" y="1120" width="{FW}" height="230" fill="{NACHT_DIEP}"/>'
    b += route([(60, 1165), (540, 1120), (1020, 1150)], ORANJE, 6, "2 18")
    b += walkers(1040, [150, 290, 760, 880], 115)
    b += text(80, 220, "Hier begint", 104, WIT, "l")
    b += glow_text(80, 380, "Glow.", 190, AQUA, "b", strength="m")
    b += element("py-atom-logo-horizontal-white", 80, FH - 115, w=260)
    b += url_tag(FW - 80 - 400 * 0.75, FH - 112, 0.75)
    return canvas(FW, FH, b)


def location_pin(x, y, w, glow=True):
    out = ""
    if glow:
        out += f'<g filter="url(#blur-m)" opacity="0.9">{element("py-atom-icon-location-pin", x, y, w=w, cls="aqua")}</g>'
    return out + element("py-atom-icon-location-pin", x, y, w=w)


def post_c():
    b = background(FW, FH, 31, [(540, 820, 420, BLAUW, 0.9), (820, 700, 200, AQUA, 0.35)])
    b += text(80, 190, "Wist je dat", 92, WIT, "l")
    b += text(80, 295, "hier een", 92, WIT, "l")
    b += glow_text(80, 410, "garage zit?", 104, AQUA, "b", strength="s")
    # abstract centre: the Glow route as a dotted light line, five ParkingYou pins along it
    b += route([(-20, 720), (250, 560), (460, 760), (700, 960), (1100, 820)], ORANJE, 7, "2 20")
    pins = [(130, 610, "TD-gebouw"), (330, 690, "DLL"), (520, 830, "Bedrijfsschoolgebouw"),
            (640, 1010, "Evoluon"), (870, 870, "Philips Stadion")]
    for px, py, name in pins:
        b += location_pin(px - 26, py - 76, 52)
        s, w = pill(px, py + 8, name, 24, WIT, BLAUW, "b", 18, anchor="middle")
        b += s
    b += text(80, 1150, "5 ParkingYou-garages vlak bij de Glow-route", 34, WIT, "m")
    b += footer(FW, FH, FH - 125, logo_w=260)
    return canvas(FW, FH, b)


def light_trails(cx, cy, rmax, seed=4):
    rnd = random.Random(seed)
    out = []
    for i in range(16):
        r = rmax * (0.38 + 0.62 * i / 15)
        col = rnd.choice([WIT, WIT, ORANJE, AQUA, ORANJE])
        start = rnd.uniform(0, 360)
        sweep = rnd.uniform(200, 330)
        circ = 6.2832 * r
        on = circ * sweep / 360
        sw = rnd.choice([4, 5, 7, 9])
        rot = f'transform="rotate({start:.0f} {cx} {cy})"'
        dash = f'stroke-dasharray="{on:.0f} {circ:.0f}"'
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.0f}" fill="none" stroke="{col}" stroke-width="{sw * 4}" '
                   f'opacity="0.35" filter="url(#blur-m)" {dash} {rot} stroke-linecap="round"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.0f}" fill="none" stroke="{col}" stroke-width="{sw}" '
                   f'opacity="0.9" {dash} {rot} stroke-linecap="round"/>')
    return "".join(out)


def post_d():
    b = background(FW, FH, 41, [(540, 500, 300, ORANJE, 0.25)])
    b += light_trails(540, 500, 370)
    b += text(80, 990, "Rondjes rijden", 80, WIT, "l")
    b += text(80, 1080, "hoort niet bij", 80, WIT, "l")
    b += glow_text(80, 1175, "de lichtshow", 86, AQUA, "b", strength="s")
    b += element("py-atom-logo-horizontal-white", 80, FH - 100, w=230)
    b += url_tag(FW - 80 - 400 * 0.7, FH - 100, 0.7)
    return canvas(FW, FH, b)


def carrousel():
    W = FW * 5
    b = background(W, FH, 51, [(540, 500, 380, AQUA, 0.45), (1620, 800, 300, ORANJE, 0.3),
                               (2700, 700, 320, AQUA, 0.35), (3780, 900, 300, ORANJE, 0.3),
                               (4860, 600, 380, AQUA, 0.45)])
    # one route runs through all five slides
    b += route([(300, 1060), (1100, 940), (1620, 1010), (2200, 1080), (2700, 1000),
                (3200, 920), (3780, 1010), (4300, 1100), (4860, 1000)], ORANJE, 8, "2 22")
    # slide 1
    b += f'<g filter="url(#blur-l)">{element("py-atom-logo-beeldmerk-white", 380, 330, w=320, cls="aqua")}</g>'
    b += element("py-atom-logo-beeldmerk-white", 380, 330, w=320)
    b += text(80, 175, "Jouw Glow-avond.", 84, WIT, "l")
    b += glow_text(80, 820, "In 4 stappen.", 120, AQUA, "b", strength="s")
    b += date_chip(80, 880)
    b += text(1000, 1270, "Swipe", 34, WIT, "m", "end") + \
        f'<path d="M1012 1248 l18 12 l-18 12" stroke="{AQUA}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    b += element("py-atom-logo-horizontal-white", 80, 1225, w=230)

    def step(i, n, line1, line2, sub=None):
        ox = FW * i
        s = bubble(ox + 70, 120, 150)
        s += text(ox + 145, 228, str(n), 96, WIT, "b", "middle")
        s += text(ox + 80, 420, line1, 92, WIT, "l")
        s += glow_text(ox + 80, 530, line2, 104, AQUA, "b", strength="s")
        if sub:
            s += text(ox + 80, 610, sub, 36, WIT, "m")
        return s

    b += step(1, 1, "Reserveer", "online. €15.", "Plek kiezen, betalen, klaar.")
    b += element("py-atom-shape-bubble-solid", FW + 640, 690, w=280, cls="oranje")
    b += text(FW + 780, 880, "€15", 110, WIT, "b", "middle", 'transform="rotate(-6 1860 840)"')
    b += step(2, 2, "Rij naar binnen.", "Plek staat klaar.")
    b += f'<g filter="url(#blur-m)" opacity="0.8">{element("py-atom-symbol-p-garage-outline", 2*FW + 600, 650, w=320, cls="aqua")}</g>'
    b += element("py-atom-symbol-p-garage-outline", 2 * FW + 600, 650, w=320, cls="wit")
    b += step(3, 3, "Loop zo", "de route op.")
    b += walkers(830, [3 * FW + 560, 3 * FW + 720], 190)
    b += step(4, 4, "Terug naar je auto,", "warm naar huis.")
    b += element("py-atom-figure-wave", 4 * FW + 760, 720, h=230, cls="wit")
    s, _ = pill(4 * FW + 80, 700, "Reserveer nu", 44, ORANJE, WIT, "b", 46)
    b += s
    b += element("py-atom-logo-horizontal-white", 4 * FW + 80, 1225, w=230)
    b += url_tag(5 * FW - 80 - 400 * 0.7, 1225, 0.7)
    return canvas(W, FH, b)


def post_f(days):
    b = background(FW, FH, 60 + days, [(540, 520, 380, AQUA, 0.5), (900, 1050, 250, ORANJE, 0.3)])
    b += date_chip(80, 90, "Aftellen tot Glow", size=28)
    b += glow_text(540, 780, str(days), 660, AQUA, "b", "middle", strength="l")
    b += text(540, 780, str(days), 660, WIT, "b", "middle", 'opacity="0.18"')
    label = "dag." if days == 1 else "dagen."
    b += text(80, 960, f'Nog <tspan class="b">{days} {label}</tspan>', 64, WIT, "l")
    b += text(80, 1050, "Heb jij je plek al?", 80, AQUA, "b")
    b += date_chip(80, 1100, "7 t/m 14 november · vooraf €15", size=28)
    b += element("py-atom-logo-horizontal-white", 80, FH - 100, w=230)
    b += url_tag(FW - 80 - 400 * 0.7, FH - 100, 0.7)
    return canvas(FW, FH, b)


def night_card(x, y, w, rot=-8):
    h = w * 0.63
    g = (f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})">'
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w * 0.05}" fill="{AQUA}" opacity="0.7" filter="url(#blur-l)"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w * 0.05}" fill="url(#verloop)"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w * 0.05}" fill="none" stroke="{WIT}" stroke-opacity="0.35" stroke-width="2"/>')
    g += element("py-atom-logo-horizontal-white", x + w * 0.07, y + h * 0.1, w=w * 0.42)
    g += text(x + w * 0.07, y + h * 0.62, "Night Card", w * 0.11, WIT, "b")
    g += text(x + w * 0.07, y + h * 0.77, "3x gratis avondparkeren", w * 0.05, WIT, "m")
    g += text(x + w * 0.07, y + h * 0.88, "18:00 tot 24:00 · elke locatie in NL", w * 0.037, WIT, "l", extra='opacity="0.85"')
    for i in range(3):
        g += f'<circle cx="{x + w * (0.72 + i * 0.085):.0f}" cy="{y + h * 0.2:.0f}" r="{w * 0.03:.0f}" fill="{ORANJE}"/>'
    return g + "</g>"


def post_g():
    b = background(FW, FH, 71, [(540, 560, 380, AQUA, 0.45), (850, 300, 200, ORANJE, 0.3)])
    b += night_card(170, 300, 740)
    b += text(80, 950, "Nog 3 gratis", 92, WIT, "l")
    b += glow_text(80, 1055, "avonden te goed", 92, AQUA, "b", strength="s")
    b += text(80, 1125, "Bij elke ParkingYou-locatie in NL, ook in het weekend.", 32, WIT, "m")
    b += date_chip(80, 90, "Bedankt voor je Glow-avond", size=28)
    b += element("py-atom-logo-horizontal-white", 80, FH - 100, w=230)
    b += url_tag(FW - 80 - 400 * 0.7, FH - 100, 0.7)
    return canvas(FW, FH, b)


# ---------------------------------------------------------------- stories 1080x1920 (safe zone 250 px top and bottom)

SW, SH = 1080, 1920


def story_frame(body, seed, glows, logo=True, cta=False):
    b = background(SW, SH, seed, glows) + body
    if logo:
        b += element("py-atom-logo-horizontal-white", 340, SH - 380, w=400)
    if cta:
        b += url_tag(540, SH - 520, 1.0, "middle")
    return canvas(SW, SH, b)


def s1():
    f1 = story_frame(glow_text(540, 900, "Glow", 220, AQUA, "b", "middle", strength="l") +
                     text(540, 1060, "kijken?", 150, WIT, "l", "middle"), 101, [(540, 900, 300, AQUA, 0.45)], logo=False)
    f2 = story_frame(text(540, 760, "Ter plekke:", 96, WIT, "l", "middle") +
                     struck(540, 1060, "€20", 300, anchor="middle"), 102, [(540, 900, 300, ORANJE, 0.3)], logo=False)
    f3 = story_frame(text(540, 560, "Vooraf:", 96, WIT, "l", "middle") +
                     bubble(260, 620, 560) +
                     text(540, 980, "€15", 230, WIT, "b", "middle", 'transform="rotate(-6 540 900)"') +
                     text(540, 1470, "Swipe omhoog", 54, WIT, "m", "middle") +
                     f'<path d="M510 1405 l30 -30 l30 30" stroke="{AQUA}" stroke-width="8" fill="none" stroke-linecap="round"/>',
                     103, [(540, 850, 340, AQUA, 0.5)])
    return {"story1-frame1": f1, "story1-frame2": f2, "story1-frame3": f3}


def overlay_panel(y, lines, h=None):
    """Text over footage: navy panel at 85 percent so it reads on any shot."""
    h = h or 90 + 110 * len(lines)
    out = f'<rect x="80" y="{y}" width="920" height="{h}" rx="40" fill="{BLAUW}" fill-opacity="0.85"/>'
    for i, (t, col, cls, size) in enumerate(lines):
        out += text(540, y + 110 + i * 112, t, size, col, cls, "middle")
    return out


def s2():
    f1 = canvas(SW, SH, overlay_panel(300, [("POV:", WIT, "l", 76), ("je hebt je plek al", AQUA, "b", 76)]))
    f2 = canvas(SW, SH, overlay_panel(300, [("Parkeren.", WIT, "b", 84), ("Uitstappen.", WIT, "l", 84)]))
    f3 = canvas(SW, SH, glow_text(540, 760, "Licht.", 200, WIT, "b", "middle", glow=AQUA, strength="m") +
                f'<rect x="190" y="{SH - 640}" width="700" height="300" rx="40" fill="{BLAUW}" fill-opacity="0.85"/>' +
                element("py-atom-logo-horizontal-white", 340, SH - 610, w=400) +
                text(540, SH - 420, 'Reserveer vanaf <tspan class="b" fill="#32B9CD">€15</tspan>', 56, WIT, "l", "middle"))
    return {"story2-frame1-overlay": f1, "story2-frame2-overlay": f2, "story2-frame3-overlay": f3}


def s3():
    f1 = story_frame(facade(140, 980, 800, 560, 9) +
                     f'<rect x="420" y="1380" width="240" height="160" fill="{NACHT_DIEP}"/>' +
                     f'<g filter="url(#blur-m)">{element("py-atom-logo-beeldmerk-white", 490, 1180, w=100, cls="aqua")}</g>' +
                     element("py-atom-logo-beeldmerk-white", 490, 1180, w=100) +
                     text(540, 520, "Wist je dat", 96, WIT, "l", "middle") +
                     text(540, 630, "hier een", 96, WIT, "l", "middle") +
                     glow_text(540, 760, "garage zit?", 110, AQUA, "b", "middle", strength="s"),
                     111, [(540, 1200, 320, AQUA, 0.35)], logo=False)
    body = route([(240, 1300), (420, 1000), (560, 1050), (720, 1100), (860, 760)], ORANJE, 9, "2 26")
    body += location_pin(190, 1190, 100)
    body += pill(240, 1345, "ParkingYou", 34, WIT, BLAUW, "b", 26, anchor="middle")[0]
    body += f'<circle cx="860" cy="760" r="70" fill="{ORANJE}" opacity="0.8" filter="url(#blur-m)"/>'
    body += f'<circle cx="860" cy="760" r="26" fill="{WIT}"/>'
    body += pill(860, 830, "Glow-route", 34, ORANJE, WIT, "b", 26, anchor="middle")[0]
    body += text(540, 480, "Vlak bij de", 96, WIT, "l", "middle")
    body += glow_text(540, 600, "Glow-route", 116, AQUA, "b", "middle", strength="s")
    f2 = story_frame(body, 112, [(540, 1000, 340, BLAUW, 0.8)], logo=False)
    f3 = story_frame(text(540, 760, "Plek genoeg.", 110, WIT, "l", "middle") +
                     glow_text(540, 900, "Reserveer vooraf.", 104, AQUA, "b", "middle", strength="s"),
                     113, [(540, 850, 340, AQUA, 0.45)], cta=True)
    return {"story3-frame1": f1, "story3-frame2": f2, "story3-frame3": f3}


def s4():
    out = {}
    for d in range(7, 0, -1):
        label = "dag" if d == 1 else "dagen"
        body = (text(540, 470, "Nog", 100, WIT, "l", "middle") +
                glow_text(540, 1180, str(d), 780, AQUA, "b", "middle", strength="l") +
                text(540, 1360, f"{label} tot Glow", 96, WIT, "l", "middle"))
        out[f"story4-frame1-nog-{d}"] = story_frame(body, 120 + d, [(540, 900, 360, AQUA, 0.5)])
    body = (text(540, 520, "Jouw plek", 104, WIT, "l", "middle") +
            text(540, 640, "al geregeld?", 104, WIT, "l", "middle") +
            bubble(330, 760, 420) +
            text(540, 1030, "€15", 170, WIT, "b", "middle", 'transform="rotate(-6 540 970)"') +
            text(540, 1100, "vooraf", 44, WIT, "m", "middle", 'transform="rotate(-6 540 1090)"'))
    out["story4-frame2"] = story_frame(body, 128, [(540, 1050, 340, AQUA, 0.45)], cta=True)
    return out


def s5():
    out = {"story5-frame1": story_frame(text(540, 860, "Vanavond", 130, WIT, "l", "middle") +
                                        glow_text(540, 1040, "Glow.", 220, AQUA, "b", "middle", strength="l"),
                                        130, [(540, 950, 360, AQUA, 0.5), (800, 1300, 240, ORANJE, 0.3)])}
    for i, loc in enumerate(LOCATIES):
        size = 70 if len(loc) > 14 else 92
        body = (text(540, 640, "Nog plek bij", 96, WIT, "l", "middle") +
                location_pin(490, 700, 100) +
                glow_text(540, 960, loc, size, AQUA, "b", "middle", strength="s") +
                text(540, 1100, 'Reserveer in <tspan class="b">1 minuut.</tspan>', 64, WIT, "l", "middle"))
        slug = loc.lower().replace(" ", "-")
        out[f"story5-frame2-{slug}"] = story_frame(body, 131 + i, [(540, 900, 340, AQUA, 0.45)], cta=True)
    return out


def reel():
    hook = canvas(SW, SH, overlay_panel(300, [("Deze mensen geven", WIT, "l", 70),
                                              ("gratis parkeren weg.", AQUA, "b", 70)]))
    body = (text(540, 560, "Zie je ons lopen?", 92, WIT, "l", "middle") +
            glow_text(540, 690, "Vraag om je", 96, AQUA, "b", "middle", strength="s") +
            glow_text(540, 805, "Night Card.", 96, AQUA, "b", "middle", strength="s") +
            night_card(220, 900, 640, -6) +
            text(540, 1430, '<tspan class="b">3 avonden</tspan> gratis parkeren', 58, WIT, "l", "middle"))
    end = story_frame(body, 140, [(540, 1100, 360, AQUA, 0.45)])
    return {"reel-hook-overlay": hook, "reel-eindkaart": end}


# ---------------------------------------------------------------- render

def build():
    files = {
        "post-a-vijf-euro": (post_a(), FW, FH),
        "post-b-hier-begint-glow": (post_b(), FW, FH),
        "post-c-garage-die-je-niet-kent": (post_c(), FW, FH),
        "post-d-geen-rondjes": (post_d(), FW, FH),
        "post-g-night-card": (post_g(), FW, FH),
    }
    for d in range(7, 0, -1):
        files[f"post-f-aftellen-nog-{d}"] = (post_f(d), FW, FH)
    files["post-e-carrousel-panorama"] = (carrousel(), FW * 5, FH)
    for group in (s1(), s2(), s3(), s4(), s5(), reel()):
        for k, v in group.items():
            files[k] = (v, SW, SH)
    return files


def render(files):
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for name, (svg, w, h) in files.items():
            (OUT / f"{name}.svg").write_text(svg)
            page.set_viewport_size({"width": w, "height": h})
            transparent = "overlay" in name
            bg = "transparent" if transparent else "#060D24"
            page.set_content(f'<html><body style="margin:0;background:{bg}">{svg}</body></html>')
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(150)
            if name == "post-e-carrousel-panorama":
                for i in range(5):
                    page.screenshot(path=str(OUT / f"post-e-carrousel-slide-{i + 1}.png"),
                                    clip={"x": i * FW, "y": 0, "width": FW, "height": FH})
            else:
                page.screenshot(path=str(OUT / f"{name}.png"), omit_background=transparent)
        browser.close()


if __name__ == "__main__":
    fs = build()
    render(fs)
    print(len(fs), "designs written to", OUT)
