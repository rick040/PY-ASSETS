#!/usr/bin/env python3
"""Build the Gate 2 review page: every chapter with its figures on one HTML page.

Usage: python3 -I brand-2027/tools/build_review.py <out_dir> [gate2_notes.md]
Writes <out_dir>/index.html and <out_dir>/figures/<chapter>/<name>.jpg (figures downscaled to 1600 px JPEG).
"""
import html
import os
import re
import sys

import markdown
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BUILD = os.path.join(ROOT, "02-build")
CHAPTERS = [
    ("00-intro", "Introductie en merkprincipes"), ("01-logo", "Logo"), ("02-kleur", "Kleur"),
    ("03-typografie", "Typografie"), ("04-grid", "Grid en layout"), ("05-patronen", "Patronen en designelementen"),
    ("06-iconografie", "Iconografie"), ("07-beweging", "Beweging"), ("08-fotografie", "Fotografie en beeld"),
    ("09-ui", "UI/UX"), ("10-stationery", "Stationery"), ("11-toepassingen", "Toepassingen"),
]


def convert_figure(chapter, name, out_dir):
    src = os.path.join(BUILD, chapter, "figures", name)
    if not os.path.exists(src):
        return None
    rel = "figures/%s/%s.jpg" % (chapter, os.path.splitext(name)[0])
    dst = os.path.join(out_dir, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im = Image.open(src).convert("RGB")
    im.thumbnail((1600, 1600))
    im.save(dst, quality=82, optimize=True, progressive=True)
    return rel, im.size


def chapter_html(chapter, title, out_dir):
    path = os.path.join(BUILD, chapter, "chapter.md")
    if not os.path.exists(path):
        return '<p class="missing">Dit hoofdstuk is nog niet klaar.</p>', 0
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"^# .*\n", "", text, count=1)  # the page sets its own chapter heading
    figs = 0

    def img(m):
        nonlocal figs
        alt, src = m.group(1), m.group(2)
        name = os.path.basename(src)
        res = convert_figure(chapter, name, out_dir)
        if not res:
            return "*[figuur ontbreekt: %s]*" % name
        figs += 1
        rel, (w, h) = res
        return '<figure><img src="%s" alt="%s" width="%d" height="%d" loading="lazy"><figcaption>%s</figcaption></figure>' % (
            rel, html.escape(alt, quote=True), w, h, html.escape(alt))
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", img, text)
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    body = body.replace("<table>", '<div class="table"><table>').replace("</table>", "</table></div>")
    body = re.sub(r"<p>(<figure>.*?</figure>)</p>", r"\1", body, flags=re.S)
    return body, figs


def main():
    out_dir = sys.argv[1]
    notes = open(sys.argv[2], encoding="utf-8").read() if len(sys.argv) > 2 else ""
    os.makedirs(out_dir, exist_ok=True)
    nav, sections, total = [], [], 0
    for i, (chapter, title) in enumerate(CHAPTERS):
        body, figs = chapter_html(chapter, title, out_dir)
        total += figs
        anchor = chapter.split("-", 1)[1]
        nav.append('<li><a href="#%s"><span class="n tnum">%d</span>%s</a></li>' % (anchor, i, html.escape(title)))
        sections.append('<section class="chapter" id="%s"><p class="eyebrow">Hoofdstuk %d · %d figuren</p><h2>%s</h2>%s</section>' % (
            anchor, i, figs, html.escape(title), body))
    notes_html = markdown.markdown(notes, extensions=["tables", "sane_lists"]) if notes else ""
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "review_template.html"), encoding="utf-8").read()
    page = tpl.replace("{{NAV}}", "\n".join(nav)).replace("{{SECTIONS}}", "\n".join(sections)) \
              .replace("{{NOTES}}", notes_html).replace("{{FIGS}}", str(total)).replace("{{CHAPTERS}}", str(len(CHAPTERS)))
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(page)
    print("review built:", len(CHAPTERS), "chapters,", total, "figures")


if __name__ == "__main__":
    main()
