#!/bin/sh
# Rebuild the whole bundle in order. Run from the repo root with the source PDF in source/handbook.pdf.
set -e
python3 -I tools/build_all.py --src source/handbook.pdf
python3 -I tools/build_overview.py --src source/handbook.pdf --svg-dir overview/pages-svg
python3 -I tools/build_notes.py
python3 -I tools/validate.py
python3 -I - <<'PY'
import os, zipfile
os.makedirs("dist", exist_ok=True)
with zipfile.ZipFile("dist/parkingyou-brand-assets.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk("svg"):
        for f in sorted(files):
            p = os.path.join(root, f); z.write(p, p)
    for f in ("tokens.json", "elements.json", "README.md"):
        z.write(f, f)
PY
