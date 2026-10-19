"""Gegevens inlezen: locaties.json, partnerprogramma.json, partners.csv."""
import csv
import json
import math
import os
from .brand import DATA


def _json(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def locaties():
    return _json("locaties.json")


def algemeen():
    return _json("partnerprogramma.json")


def partners():
    with open(os.path.join(DATA, "partners.csv"), encoding="utf-8-sig", newline="") as f:
        head = f.readline()
        f.seek(0)
        rows = list(csv.DictReader(f, delimiter=";" if head.count(";") > head.count(",") else ","))
    loc, alg = locaties(), algemeen()
    out = []
    for r in rows:
        r = {k.strip(): (v or "").strip() for k, v in r.items()}
        if not r.get("code"):
            continue
        if r["locatie"] not in loc:
            raise ValueError(f"{r['code']}: onbekende locatie {r['locatie']!r}; kies uit {list(loc)}")
        if not r["code"].startswith(r["locatie"] + "-"):
            raise ValueError(f"{r['code']}: code moet beginnen met {r['locatie']}-")
        r["afstand_m"] = float(r["afstand_m"])
        if r["afstand_m"] <= 0:
            raise ValueError(f"{r['code']}: afstand_m moet groter dan 0 zijn")
        r["link"] = r["link"] or alg["link_prefix"] + r["code"]
        out.append(r)
    codes = [r["code"] for r in out]
    if len(set(codes)) != len(codes):
        raise ValueError("dubbele code in partners.csv")
    return out


def afstand_tekst(afstand_m, per_minuut=80):
    """80 meter per minuut, naar boven afgerond. Geeft '3 minuten' of '1 minuut'."""
    n = max(1, math.ceil(afstand_m / per_minuut - 1e-9))
    return f"{n}\u00a0minuut" if n == 1 else f"{n}\u00a0minuten"   # vaste spatie: getal en eenheid blijven bij elkaar


def partner_values(p):
    loc, alg = locaties()[p["locatie"]], algemeen()
    return dict(locatie=loc["locatie"], afstand=afstand_tekst(p["afstand_m"], alg["loopsnelheid_m_per_minuut"]),
                bedrijf=p["bedrijf"], link=p["link"], code=p["code"])


def euro(x):
    s = f"{x:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return s[:-3] if s.endswith(",00") else s


def onepager_values(code):
    loc, alg = locaties()[code], algemeen()
    niv = next(n for n in alg["niveaus"] if n["id"] == alg["rekenvoorbeeld"]["niveau"])
    bedrag = loc.get("gemiddelde_boeking_eur")
    gasten = alg["rekenvoorbeeld"]["gasten_per_maand"]
    c = alg["contact"]
    ph = lambda v, name: v if v else f"[{name}]"
    return dict(
        locatie=loc["locatie"], aantal_locaties=alg["aantal_locaties"], gasten=gasten, percentage=niv["percentage"],
        bedrag=euro(bedrag) if bedrag is not None else "[bedrag]",
        uitkomst=euro(gasten * bedrag * niv["percentage"] / 100) if bedrag is not None else "[uitkomst]",
        naam=ph(c["naam"], "naam"), functie=ph(c["functie"], "functie"), telefoon=ph(c["telefoon"], "telefoon"),
        email=ph(c["email"], "e-mail"), url=c["url"],
    )
