#!/usr/bin/env python3
"""Landingspagina parkingyou.nl/partners: template.html + teksten.json + data/ -> export/index.html.

usage: python3 -I partnerprogramma/5-landingspagina/vul.py

Alle tekst komt uit teksten.json. Waarden tussen [haken] zijn placeholders en krijgen in beeld een oranje omlijning.
Locaties, percentages en slidergrenzen komen uit partnerprogramma/data/ en rekenhulp-logica.js (inline, geen fetch).
"""
import html
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "partnerprogramma", "data")
OUT = os.path.join(HERE, "export")


def lees(pad):
    with open(pad, encoding="utf-8") as f:
        return json.load(f)


TEKSTEN = lees(os.path.join(HERE, "teksten.json"))
LOCATIES = lees(os.path.join(DATA, "locaties.json"))
PROGRAMMA = lees(os.path.join(DATA, "partnerprogramma.json"))
LIMIETEN = {"bezoekers": dict(min=10, max=5000, stap=10, standaard=200), "deel": dict(min=5, max=60, stap=1, standaard=20)}


def esc(s):
    return html.escape(str(s), quote=True)


def t(s):
    """Tekst naar HTML; een geheel-tussen-haken waarde wordt een zichtbare placeholder."""
    s = str(s)
    if s.startswith("[") and s.endswith("]"):
        return '<span class="placeholder">%s</span>' % esc(s)
    return esc(s)


def zoek(pad):
    w = TEKSTEN
    for stuk in pad.split("."):
        w = w[stuk]
    return w


# ---------- fragmenten ----------

def stappen():
    regels = []
    for i, tekst in enumerate(TEKSTEN["zo_werkt_het"]["stappen"], 1):
        regels.append('      <li><span class="nr" aria-hidden="true">%d</span><div><h3>%s</h3><p>%s</p></div></li>'
                      % (i, t(tekst["kop"]), t(tekst["tekst"])))
    return "\n".join(regels)


def voor_wie():
    return "\n".join('      <li class="kaart"><h3>%s</h3></li>' % t(i) for i in TEKSTEN["voor_wie"]["items"])


def tabel():
    c = TEKSTEN["commissietabel"]
    rijen = []
    for n in PROGRAMMA["niveaus"]:
        aanbevolen = n.get("aanbevolen")
        label = '<span class="aanbevolen">%s</span>' % t(c["aanbevolen"]) if aanbevolen else ""
        rijen.append(
            '        <tr%s><th scope="row"><span class="niveau">%s</span>%s</th><td>%s</td><td class="pct">%d%%</td></tr>'
            % (' class="aanbevolen-rij"' if aanbevolen else "", esc(n["naam"]), label, t(c["niveaus"][n["id"]]), n["percentage"]))
    return "\n".join(rijen)


def rh_garage():
    r = TEKSTEN["rekenhulp"]
    regels = []
    for i, (code, loc) in enumerate(LOCATIES.items()):
        boeking = loc["gemiddelde_boeking_eur"]
        regels.append(
            '        <label class="optie"><input type="radio" name="garage" value="%s" data-boeking="%s"%s><span>%s</span></label>'
            % (esc(code), "" if boeking is None else esc(boeking), " checked" if i == 0 else "", esc(loc["locatie"])))
    return "\n".join(regels)


def rh_niveau():
    regels = []
    tpl = TEKSTEN["rekenhulp"]["waarde_percentage"]
    for n in PROGRAMMA["niveaus"]:
        regels.append(
            '        <label class="optie"><input type="radio" name="niveau" value="%s" data-percentage="%d" data-tekst="%s"%s><span>%s <small>%d%%</small></span></label>'
            % (esc(n["id"]), n["percentage"], esc(tpl.replace("{n}", str(n["percentage"]))),
               " checked" if n["id"] == "actief" else "", esc(n["naam"]), n["percentage"]))
    return "\n".join(regels)


def faq():
    return "\n".join('    <details class="faq"><summary>%s</summary><div class="antwoord"><p>%s</p></div></details>'
                     % (t(i["vraag"]), t(i["antwoord"])) for i in TEKSTEN["faq"]["items"])


def veld(sleutel, label, soort="text", verplicht=True, extra="", opties=None):
    id_ = "f-" + sleutel
    lab = esc(label) + ("" if verplicht else ' <span class="optioneel">%s</span>' % esc(TEKSTEN["formulier"]["optioneel"]))
    req = ' required aria-required="true"' if verplicht else ""
    desc = ' aria-describedby="%s-fout"' % id_
    if soort == "select":
        opts = '<option value="">%s</option>' % esc(TEKSTEN["formulier"]["keuze_leeg"])
        opts += "".join('<option value="%s">%s</option>' % (esc(v), esc(w)) for v, w in opties)
        ctl = '<select id="%s" name="%s"%s%s%s>%s</select>' % (id_, sleutel, req, desc, extra, opts)
    elif soort == "textarea":
        ctl = '<textarea id="%s" name="%s" rows="4"%s%s%s></textarea>' % (id_, sleutel, req, desc, extra)
    else:
        ctl = '<input id="%s" name="%s" type="%s"%s%s%s>' % (id_, sleutel, soort, req, desc, extra)
    return ('      <div class="veld" data-veld="%s"><label for="%s">%s</label>%s<p class="fout" id="%s-fout" hidden></p></div>'
            % (sleutel, id_, lab, ctl, id_))


def velden():
    v = TEKSTEN["formulier"]["velden"]
    f = TEKSTEN["formulier"]
    soorten = [(o, o) for o in f["soort_opties"]]
    garages = [(code, loc["locatie"]) for code, loc in LOCATIES.items()]
    uit = [
        veld("bedrijfsnaam", v["bedrijfsnaam"], extra=' autocomplete="organization"'),
        veld("kvk", v["kvk"], extra=' inputmode="numeric" autocomplete="off" maxlength="12"'),
        veld("soort_bedrijf", v["soort_bedrijf"], "select", opties=soorten),
        veld("garage", v["garage"], "select", opties=garages),
        veld("naam", v["naam"], extra=' autocomplete="name"'),
        veld("functie", v["functie"], verplicht=False, extra=' autocomplete="organization-title"'),
        veld("email", v["email"], "email", extra=' autocomplete="email" inputmode="email"'),
        veld("telefoon", v["telefoon"], "tel", extra=' autocomplete="tel" inputmode="tel"'),
        veld("bezoekers", v["bezoekers"], "select", verplicht=False, opties=[(o, o) for o in f["bezoekers_opties"]]),
        veld("opmerking", v["opmerking"], "textarea", verplicht=False),
        ('      <div class="veld akkoord" data-veld="akkoord"><label class="vink"><input id="f-akkoord" name="akkoord" type="checkbox" required aria-required="true" aria-describedby="f-akkoord-fout"><span>%s<a href="%s">%s</a>%s<a href="%s">%s</a></span></label><p class="fout" id="f-akkoord-fout" hidden></p></div>'
         % (esc(f["akkoord_voor"]), esc(f["url_voorwaarden"]), t(f["akkoord_voorwaarden"]), esc(f["akkoord_en"]),
            esc(f["url_privacy"]), t(f["akkoord_privacy"]))),
    ]
    return "\n".join(uit)


def beeldmerk_pad():
    with open(os.path.join(ROOT, "svg", "atom", "py-atom-logo-beeldmerk-watermark.svg"), encoding="utf-8") as f:
        return re.search(r'<path d="([^"]*)"', f.read()).group(1)


FRAGMENTEN = {
    "stappen": stappen, "voor_wie": voor_wie, "tabel": tabel, "rh_garage": rh_garage, "rh_niveau": rh_niveau,
    "faq": faq, "velden": velden, "beeldmerk_pad": beeldmerk_pad,
    "meldingen_json": lambda: json.dumps(TEKSTEN["meldingen"], ensure_ascii=False).replace("</", "<\\/"),
    "bez_min": lambda: LIMIETEN["bezoekers"]["min"], "bez_max": lambda: LIMIETEN["bezoekers"]["max"],
    "bez_stap": lambda: LIMIETEN["bezoekers"]["stap"], "bez_std": lambda: LIMIETEN["bezoekers"]["standaard"],
    "deel_min": lambda: LIMIETEN["deel"]["min"], "deel_max": lambda: LIMIETEN["deel"]["max"],
    "deel_stap": lambda: LIMIETEN["deel"]["stap"], "deel_std": lambda: LIMIETEN["deel"]["standaard"],
}


def vervang(m):
    sleutel = m.group(1)
    if sleutel.startswith("@"):
        return str(FRAGMENTEN[sleutel[1:]]())
    pad, _, modus = sleutel.partition("|")
    waarde = zoek(pad)
    if modus == "attr":
        return esc(waarde)
    if pad == "meta.titel":
        return esc(waarde)
    return t(waarde)


def bouw():
    with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
        pagina = f.read()
    pagina = re.sub(r"\{\{([^}]+)\}\}", vervang, pagina)
    # em en en dashes horen nergens in de uitvoer thuis
    assert "\u2014" not in pagina and "\u2013" not in pagina, "gedachtestreepje in uitvoer"
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina)
    shutil.copytree(os.path.join(HERE, "assets"), os.path.join(OUT, "assets"), dirs_exist_ok=True)
    for bron in ("stijl.css", "pagina.js", "rekenhulp-logica.js"):
        shutil.copy(os.path.join(HERE, bron), os.path.join(OUT, "assets", bron))
    print("geschreven:", os.path.relpath(os.path.join(OUT, "index.html"), ROOT))


if __name__ == "__main__":
    bouw()
