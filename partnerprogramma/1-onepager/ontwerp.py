#!/usr/bin/env python3
"""Schrijft template.svg (A4 staand, trim 210 x 297 mm, 3 mm afloop). Alleen nodig om het ontwerp aan te passen;
het vullen doet vul.py. Teksten staan letterlijk uit de brief, met {velden} voor de variabelen."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from ppkit import brand as b          # noqa: E402
from ppkit.doc import Doc             # noqa: E402

W, H = 210, 297
M = 14                  # marge links en rechts
CW = W - 2 * M          # tekstbreedte
HEAD = 90               # hoogte navy kop
FOOT = 256              # begin navy voet

d = Doc(W, H, "ParkingYou partnerprogramma, one-pager {locatie}", defs=b.verloop_defs("verloop", "diag"))
B = "font-weight=\"bold\""
tb = lambda s, c=None: f'<tspan font-weight="bold"{f" fill=\"{c}\"" if c else ""}>{s}</tspan>'

# --- kop ---------------------------------------------------------------------
d.rect(-3, -3, W + 6, HEAD + 3, b.BLAUW, extra='id="kop-achtergrond"')
d.atom("py-atom-logo-beeldmerk-watermark", W - M - 80, 6, h=HEAD - 10, opacity=1)
d.atom("py-atom-logo-horizontal-reverse", M, 14, w=46)
d.flow(M, 36, CW, 30, 30, 22, 1.08,
       'Uw gasten parkeren zonder zoeken.<br/>' + tb("U verdient eraan.", b.AQUA), face="bold", fill=b.WIT, id="kop")
d.flow(M, 70, 150, 20, 13, 10.5, 1.3,
       'Word parkeerpartner van ParkingYou {locatie} en ontvang ' + tb("4\u00a0tot\u00a09%") + ' van elke reservering die via u binnenkomt.',
       fill=b.WIT, id="subkop")

# --- zo werkt het ------------------------------------------------------------
y = HEAD + 9
d.text(M, y + 5, "Zo werkt het", "bold", 15, b.BLAUW)
steps = ["U krijgt een eigen link, code en QR-kaart.",
         "Uw gasten reserveren daarmee vooraf een plek in onze garage, vlak bij u.",
         "Elk kwartaal krijgt u uw commissie uitbetaald. Wij regelen de factuur."]
gap = 8
cw = (CW - 2 * gap) / 3
for i, s in enumerate(steps):
    x = M + i * (cw + gap)
    d.circle(x + 4.5, y + 16.5, 4.5, b.BLAUW)
    d.text(x + 4.5, y + 16.5 + 1.75, str(i + 1), "bold", 13, b.WIT, anchor="middle")
    d.flow(x + 12, y + 14.1, cw - 12, 20, 10.5, 9, 1.28, s, fill=b.ZWART, id=f"stap-{i + 1}")

# --- wat u krijgt ------------------------------------------------------------
y = HEAD + 45
d.text(M, y + 5, "Wat u krijgt", "bold", 15, b.BLAUW)
rows = [("Basis", "Link delen als gasten vragen naar parkeren", "4%", False),
        ("Actief", "Parkeerinfo standaard in uw mails, op uw site en bij de balie", "6%", True),
        ("Top", "Actief, plus een vaste afspraak", "9%", False)]
d.text(M + 5, y + 11.2, "Niveau", "medium", 8.5, b.GRIJS)
d.text(M + 36, y + 11.2, "Wat u doet", "medium", 8.5, b.GRIJS)
d.text(M + CW - 5, y + 11.2, "Commissie", "medium", 8.5, b.GRIJS, anchor="end")
ry, rh, rg = y + 14, 15.5, 2.2
for i, (naam, tekst, pct, rec) in enumerate(rows):
    t = ry + i * (rh + rg)
    if rec:
        d.rect(M - 2, t - 1.2, CW + 4, rh + 2.4, b.BLAUW, rx=3.2, extra='id="actief-aanbevolen"')
    else:
        d.rect(M, t, CW, rh, b.AQUA, rx=3.0, opacity=b.AQUA_TINT_OPACITY)
    fg = b.WIT if rec else b.BLAUW
    d.text(M + 5, t + rh / 2 + 1.6, naam, "bold", 13, fg)
    d.flow(M + 36, t, 88, rh, 10.5, 9, 1.22, tekst, fill=b.WIT if rec else b.ZWART, id=f"niveau-{naam.lower()}", valign="middle")
    d.text(M + CW - 5, t + rh / 2 + 3.2, pct, "bold", 24, b.AQUA if rec else b.BLAUW, anchor="end")
    if rec:
        px = M + 128
        d.rect(px, t + rh / 2 - 3.1, 26, 6.2, b.AQUA, rx=3.1, extra='id="label-aanbevolen"')
        d.text(px + 13, t + rh / 2 + 1.1, "Aanbevolen", "bold", 8.5, b.BLAUW, anchor="middle")
y = ry + 3 * rh + 2 * rg + 4
d.flow(M, y, CW, 6, 10.5, 9, 1.3, tb("Plus:") + ' een kant-en-klare partnerkit, een maandoverzicht van uw reserveringen en een vast aanspreekpunt.',
       fill=b.ZWART, id="plus")

# --- kosten en rekenvoorbeeld ---------------------------------------------------
y = y + 14
bw = 78
d.text(M, y + 4.5, "Wat het u kost", "bold", 13, b.BLAUW)
d.flow(M, y + 8, bw, 20, 11, 9.5, 1.3, tb("Niets.") + ' Geen abonnement, geen minimum, opzeggen per maand.', fill=b.ZWART, id="kosten")
x2 = M + bw + 8
d.rect(x2, y - 3, CW - bw - 8, 31, b.AQUA, rx=3.0, opacity=b.AQUA_TINT_OPACITY)
d.text(x2 + 5, y + 4.5, "Rekenvoorbeeld", "bold", 13, b.BLAUW)
d.flow(x2 + 5, y + 8, CW - bw - 18, 20, 10, 8.5, 1.3,
       '{gasten} gasten per maand reserveren via uw link, gemiddeld €{bedrag} per reservering. Bij {percentage}% is dat ' + tb("€{uitkomst}") + ' per maand.',
       fill=b.ZWART, id="rekenvoorbeeld")

# --- voet ----------------------------------------------------------------------
d.rect(-3, FOOT, W + 6, H - FOOT + 3, b.BLAUW, extra='id="voet-achtergrond"')
fw = 88
d.text(M, FOOT + 10, "Over ParkingYou", "bold", 10.5, b.AQUA)
d.flow(M, FOOT + 13.5, fw, 24, 9.5, 8.5, 1.3, 'ParkingYou beheert {aantal_locaties} parkeerlocaties in Nederland, waaronder {locatie}.', fill=b.WIT, id="over")
cx = M + fw + 14
d.text(cx, FOOT + 10, "Contact", "bold", 10.5, b.AQUA)
d.flow(cx, FOOT + 13.5, CW - fw - 14, 26, 9.5, 8.5, 1.4,
       '{naam}, {functie}<br/>{telefoon}<br/>{email}<br/>' + tb("{url}"), fill=b.WIT, id="contact")

open(os.path.join(HERE, "template.svg"), "w", encoding="utf-8").write(d.svg())
print("template.svg geschreven")
