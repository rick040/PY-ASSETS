# Geurhanger (Aroman), drukbestand

Print file for the custom-shape car air freshener printed by Aroman. It replaces the Aroman proof, which used an
unofficial logo: wrong blue and aqua, and a darker "fold" on the tail that the beeldmerk does not have.

| File | What |
|---|---|
| `parkingyou-geurhanger-standaard.pdf` | Standard format (Aroman max 56 cm²): cut contour 68.5 x 80.9 mm (55.4 cm²), beeldmerk 61.5 mm wide. |
| `parkingyou-geurhanger-groot.pdf` | Large format option (Aroman max 64 cm², +€0.03 each): cut contour 73.5 x 86.9 mm (63.8 cm²), beeldmerk 66.5 mm wide. |
| `*-preview.png` | Front and back side by side (RGB approximation of the CMYK file). |

## Build

* Shape and logo: `svg/atom/py-atom-logo-beeldmerk-color.svg`, used unchanged and scaled. White paper border of 3.5 mm
  between the logo and the cut line, 2 mm radius in the inner corner where the tail meets the bubble.
* Page 1 is the front, page 2 the back. The back is the mirror image of the front so that both sides line up after die-cutting
  (seen from behind, the tail points the other way; this cannot be avoided with a cut in the shape of the logo).
* Colours: DeviceCMYK, PY-Blauw 100/83/0/17 and PY-Aqua 69/0/21/0 (`tokens.json`). No white objects: the white is
  paper, and the URL is knocked out of the ring.
* Front: `www.parkingyou.nl` in Ubuntu Medium 9 pt (x-height 1.7 mm), outlined, on the lower right of the ring, as on the proof.
* Cut contour and hanger hole (Ø 3 mm, centre on the top edge of the logo, 2 mm material above it): 0.25 pt stroke in the spot
  colour `CutContour` (overprint, does not print). TrimBox = cut contour bounds, 3 mm white bleed. No fonts, no images.
* The "56 cm²" is read as the bounding box of the cut (7 x 8 cm); the real shape area is about 40 cm².

Rebuild: `python3 -I tools/build_geurhanger.py --size standaard` (or `--size groot`).
Needs `skia-pathops`, `fonttools`, `reportlab` and `pymupdf`.

Check with Aroman: the cut colour name (`CutContour`) and the hole size and position, which Aroman may set themselves.
