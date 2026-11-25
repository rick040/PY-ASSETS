#!/usr/bin/env python3
"""Facts check: every price, count and facility in a post must be backed by its kennisbank snapshot (facts.json).

Usage:  python3 check_facts.py <post-dir or spec.json> [...]      (facts.json next to the spec)
Exit 1 when a blocking finding is found.

facts.json is written by the skill from scripts/facts.sql (Supabase connector, read only):
  { "date": "YYYY-MM-DD", "codes": [...], "locaties": [...], "tarieven": [...], "abonnementen": [...], "openingstijden": [...] }

Checks (references/product-truth.md):
- a post that names a location or shows a price needs a snapshot; older than 7 days warns, older than 30 days blocks;
- every location code exists in the snapshot;
- reserve wording ("reserveer", "zeker van je plek", cta "reserve") only when every location in the post is reservable;
- facility words (laden, camera, overdekt/droog, doorrijhoogte, "N plekken") only when the snapshot says so;
- every euro amount matches a current tarief or abonnement of those locations (subscriptions with or without the
  service costs), and a post with a price has price_check: true.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import Finding, load_json, plain, texts_of  # noqa: E402

RESERVE = re.compile(r"reserveer|reserveren|zeker\s+van\s+je\s+plek", re.I)
FACILITIES = [
    (re.compile(r"laadpa(al|len)|opladen|\bladen\b|laadplek", re.I), "elektrisch_laden", "charging"),
    (re.compile(r"camera", re.I), "camerabewaking", "camera surveillance"),
    (re.compile(r"\boverdekt|droog\s+(geparkeerd|uitstappen|uit)|stapt\s+droog", re.I), "overdekt", "covered"),
]
EURO = re.compile(r"€\s?(\d{1,4}(?:[.,]\d{1,2})?)(?!\d)")
HEIGHT = re.compile(r"(\d)[,.](\d{2})\s*m(eter)?\b", re.I)
SPOTS = re.compile(r"(\d[\d.]*)\s*(?:overdekte\s+)?plekken", re.I)


def codes_of(spec: dict) -> list[str]:
    out = []

    def walk(v):
        if isinstance(v, dict):
            if isinstance(v.get("code"), str):
                out.append(v["code"])
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)

    walk(spec.get("slots", {}))
    return sorted(set(out))


def amounts_of(spec: dict) -> list[tuple[str, float]]:
    found = []
    for where, text in texts_of(spec):
        for m in EURO.finditer(plain(text)):
            found.append((where, float(m.group(1).replace(".", "").replace(",", ".") if "," in m.group(1) else m.group(1))))

    def walk(v, where):
        if isinstance(v, dict):
            if isinstance(v.get("amount"), (int, float)):
                found.append((where, float(v["amount"])))
            for k, x in v.items():
                walk(x, f"{where}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, f"{where}[{i}]")

    walk(spec.get("slots", {}), "slots")
    return found


def uses_reserve(spec: dict) -> bool:
    if any(RESERVE.search(t) for _, t in texts_of(spec)):
        return True

    def ctas(v):
        if isinstance(v, dict):
            return (v.get("cta") == "reserve") or any(ctas(x) for x in v.values())
        if isinstance(v, list):
            return any(ctas(x) for x in v)
        return False

    return ctas(spec.get("slots", {}))


def check(spec: dict, facts: dict | None, today: dt.date | None = None) -> list[Finding]:
    today = today or dt.date.today()
    out: list[Finding] = []
    codes = codes_of(spec)
    amounts = amounts_of(spec)
    texts = " \n".join(plain(t) for _, t in texts_of(spec))
    if not codes and not amounts and not uses_reserve(spec):
        return [Finding("facts", "info", "-", "no locations or prices in this post")]
    if amounts and not spec.get("price_check"):
        out.append(Finding("facts", "block", "price_check", "the post shows a price; set price_check: true and check it on the posting day", "product-truth.md §2"))
    if facts is None:
        out.append(Finding("facts", "block", "facts.json", "no facts snapshot; run scripts/facts.sql for the location codes and save facts.json next to the spec", "product-truth.md §1"))
        return out

    try:
        age = (today - dt.date.fromisoformat(facts["date"])).days
    except (KeyError, ValueError):
        age = 999
    if age > 30:
        out.append(Finding("facts", "block", "facts.json", f"snapshot is {age} days old; fetch the facts again", "product-truth.md §2"))
    elif age > 7:
        out.append(Finding("facts", "warn", "facts.json", f"snapshot is {age} days old", "product-truth.md §2"))

    loc = {r["code"]: r for r in facts.get("locaties", [])}
    for c in codes:
        if c not in loc:
            out.append(Finding("facts", "block", f"location {c}", "code not in the snapshot (or not in the kennisbank)", "product-truth.md §1"))
    known = [loc[c] for c in codes if c in loc]

    if not codes and (amounts or uses_reserve(spec)):
        out.append(Finding("facts", "warn", "slots", "price or reserve wording without a location code; nothing to check it against", "product-truth.md"))

    if uses_reserve(spec):
        for r in known:
            if not r.get("reserveren_mogelijk"):
                out.append(Finding("facts", "block", f"location {r['code']}", f"reserve wording, but {r['naam']} cannot be reserved online", "brand-voice.md §2"))

    for rx, field, label in FACILITIES:
        if rx.search(texts):
            vals = [r.get(field) for r in known]
            if not known or not all(v is True for v in vals):
                out.append(Finding("facts", "block", field, f"the post claims {label}, but the kennisbank does not confirm it for every location ({', '.join(f'{r['code']}={r.get(field)}' for r in known) or 'no location'})", "product-truth.md §1"))

    for m in HEIGHT.finditer(texts):
        h = float(f"{m.group(1)}.{m.group(2)}")
        if not any(r.get("doorrijhoogte_m") is not None and abs(float(r["doorrijhoogte_m"]) - h) < 0.011 for r in known):
            out.append(Finding("facts", "block", "doorrijhoogte", f"{h:.2f} m does not match doorrijhoogte_m in the kennisbank", "product-truth.md"))

    for m in SPOTS.finditer(texts):
        n = int(m.group(1).replace(".", ""))
        totals = [r.get("plekken_totaal") for r in known if r.get("plekken_totaal")]
        if not totals or not any(0.9 * t <= n <= t for t in totals) and n != sum(totals):
            out.append(Finding("facts", "block", "plekken", f"{n} plekken does not match plekken_totaal ({totals or 'unknown'})", "product-truth.md"))

    allowed = set()
    for t in facts.get("tarieven", []):
        if t.get("code") in codes and t.get("prijs") is not None:
            allowed.add(round(float(t["prijs"]), 2))
    for a in facts.get("abonnementen", []):
        if a.get("code") in codes and a.get("prijs_per_maand") is not None:
            p = float(a["prijs_per_maand"])
            allowed.add(round(p, 2))
            if a.get("servicekosten_per_maand"):
                allowed.add(round(p + float(a["servicekosten_per_maand"]), 2))
                allowed.add(round(float(a["servicekosten_per_maand"]), 2))
    for where, amount in amounts:
        if round(amount, 2) not in allowed:
            out.append(Finding("facts", "block", where, f"€{amount:.2f} is not a current tarief or abonnement of {', '.join(codes) or 'the post'}", "product-truth.md §1"))
    return out


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    blocked = False
    for arg in argv:
        p = Path(arg)
        spec_path = p / "spec.json" if p.is_dir() else p
        spec = load_json(spec_path)
        fp = spec_path.parent / "facts.json"
        for f in check(spec, load_json(fp) if fp.exists() else None):
            blocked |= f.severity == "block"
            print(f"{spec['id']}  {f.severity.upper():5}  {f.where}: {f.message}  [{f.rule}]")
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
