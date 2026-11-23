"""Render content-library.json to content-library.md.

Usage: python3 -I social/instagram/build_library_md.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "content-library.json").read_text(encoding="utf-8"))
pillars = {p["id"]: p for p in data["pillars"]}
templates = {t["id"]: t for t in data["templates"]}

out = ["# ParkingYou Instagram content library", "",
       f"Generated from `content-library.json` (version {data['version']}, {data['updated']}). Edit the JSON, then run `python3 -I social/instagram/build_library_md.py`.", "",
       "## Overview", "", "| ID | Title | Pillar | Format | Template | Timing | Price check |", "|---|---|---|---|---|---|---|"]
for i in data["items"]:
    t = templates[i["template"]]
    out.append(f"| {i['id']} | {i['title']} | {i['pillar']} {pillars[i['pillar']]['name']} | {i['format']} | {i['template']} {t['name']} | {i['timing']} | {'yes' if i['price_check'] else ''} |")

out += ["", "## Templates", ""]
for t in data["templates"]:
    out += [f"### {t['id']} {t['name']} ({t['kind']}{', ' + t['length_s'] + ' s' if t['length_s'] else ''})", ""]
    out += [f"{n}. {s}" for n, s in enumerate(t["scenes"], 1)]
    out += ["", f"Props: `{', '.join(t['props'])}`", "", f"Assets: {', '.join('`' + a + '`' for a in t['assets'])}", ""]

for p in data["pillars"]:
    out += [f"## {p['id']} {p['name']} ({p['en']}, {p['share']}%)", "", p["goal"], ""]
    for i in [x for x in data["items"] if x["pillar"] == p["id"]]:
        t = templates[i["template"]]
        out += [f"### {i['id']} {i['title']}", "",
                f"**{i['format']}** · template {i['template']} {t['name']} · locations: {', '.join(i['locations'])} · {i['timing']}", "",
                f"**Hook:** {i['hook']}", "", "**Scenes / slides:**", ""]
        out += [f"{n}. {s}" for n, s in enumerate(i["body"], 1)]
        out += ["", "**Caption:**", "", "```", i["caption"], "```", ""]
        if i["assets"]:
            out += [f"**Assets:** {', '.join('`' + a + '`' for a in i['assets'])}", ""]
        if i["price_check"]:
            out += ["**Prijs check:** check the price in `kennisbank.tarief` before posting.", ""]
        if i["notes"]:
            out += [f"**Notes:** {i['notes']}", ""]

(HERE / "content-library.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote", HERE / "content-library.md")
