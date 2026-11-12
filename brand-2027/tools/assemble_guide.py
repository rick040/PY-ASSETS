#!/usr/bin/env python3
"""Assemble the full brand guideline from the chapter files (Phase 3).

Reads 02-build/<NN>/chapter.md in the fixed chapter order and writes:
  03-guide/volledig/ParkingYou-huisstijl-2027.md   the guideline (Dutch), 14 chapters
  03-guide/volledig/werkpunten.md                  proposed values and open questions taken out of the chapters
  03-guide/volledig/figures.json                   figure list in order: [{"chapter", "src", "alt"}]

Rules:
- "Voorgestelde waarden", "Open vragen" and "Open punten" sections leave the guide (they go to werkpunten.md).
- Each chapter's "Do's en don'ts" moves to chapter 13 "Do's en don'ts", grouped per chapter.
- Figure paths are rewritten relative to the output folder.
Run: python3 -I brand-2027/tools/assemble_guide.py
"""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BUILD = os.path.join(ROOT, "02-build")
OUT = os.path.join(ROOT, "03-guide", "volledig")

CHAPTERS = [
    ("00-intro", "Introductie en merkprincipes"),
    ("01-logo", "Logo"),
    ("02-kleur", "Kleur"),
    ("03-typografie", "Typografie"),
    ("04-grid", "Grid en layout"),
    ("05-patronen", "Patronen en designelementen"),
    ("06-iconografie", "Iconografie"),
    ("07-beweging", "Beweging"),
    ("08-fotografie", "Fotografie en beeld"),
    ("09-ui", "UI/UX"),
    ("10-stationery", "Stationery"),
    ("11-toepassingen", "Toepassingen"),
]
OUT_SECTIONS = ("voorgestelde waarden", "open vragen", "open punten")
DOS = "do's en don'ts"


def split_sections(text):
    """Return (intro, [(heading, body)]) split on level-2 headings."""
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    intro = parts[0]
    secs = [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]
    return intro, secs


def main():
    os.makedirs(OUT, exist_ok=True)
    guide, work, dos, figs = [], [], [], []
    guide.append("# ParkingYou huisstijl 2027\n\nVersie 1.0 · november 2026 · bron: `brand-2027/02-build/core-spec.md` en `brand-2027/tokens/tokens.json`\n")
    for n, (folder, title) in enumerate(CHAPTERS, start=1):
        text = open(os.path.join(BUILD, folder, "chapter.md"), encoding="utf-8").read()
        text = re.sub(r"^# .*\n", "", text, count=1)
        intro, secs = split_sections(text)
        body = [intro.strip()]
        for head, sec in secs:
            low = head.lower()
            if low.startswith(OUT_SECTIONS):
                work.append("## %s: %s\n%s" % (title, head, sec.rstrip()))
            elif low.startswith(DOS):
                dos.append("## %s\n%s" % (title, sec.strip()))
            else:
                body.append("## %s\n%s" % (head, sec.strip()))
        chapter = "\n\n".join(b for b in body if b)

        def fix(m):
            alt, rel = m.group(1), m.group(2)
            src = "02-build/%s/%s" % (folder, rel)
            figs.append({"chapter": n, "src": src, "alt": alt})
            return "![%s](../../%s)" % (alt, src)

        chapter = re.sub(r"!\[([^\]]*)\]\((figures/[^)]+)\)", fix, chapter)
        # demote headings one level so the guide has one H1
        chapter = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", chapter, flags=re.M)
        guide.append("## %d. %s\n\n%s\n" % (n, title, chapter))
    guide.append("## 13. Do's en don'ts\n\nPer onderwerp de belangrijkste regels. Twijfel je, dan geldt het hoofdstuk zelf, en daarna de core spec.\n\n"
                 + "\n\n".join(re.sub(r"^## ", "### ", d) for d in dos) + "\n")
    guide.append(open(os.path.join(ROOT, "03-guide", "bijlagen.md"), encoding="utf-8").read())
    open(os.path.join(OUT, "ParkingYou-huisstijl-2027.md"), "w", encoding="utf-8").write("\n".join(guide))
    open(os.path.join(OUT, "werkpunten.md"), "w", encoding="utf-8").write(
        "# Werkpunten uit de hoofdstukken\n\nVoorstellen en open vragen die de bouwers in hun hoofdstuk zetten. Ze staan niet in de gids. Wat is goedgekeurd, staat als besluit in de core spec.\n\n" + "\n\n".join(work) + "\n")
    json.dump(figs, open(os.path.join(OUT, "figures.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    words = sum(len(g.split()) for g in guide)
    print("chapters %d, figures %d, words %d, werkpunten %d" % (len(CHAPTERS) + 2, len(figs), words, len(work)))


if __name__ == "__main__":
    main()
