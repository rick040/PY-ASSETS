# py-assets: ParkingYou brand and signage elements

Single source of truth for every ParkingYou brand and signage element, extracted from
"parkingyou Huisstijlhandboek, Wayfinding & inrichting parkeervoorziening", v1.0, 09-2025 (All Jobs Wayfinding & Parking Solutions).
Elements can be combined into new signage, price stickers (deelfolie), info pylons and a full signage set for a new location.

## Contents

| Path | What |
|---|---|
| `overview/parkingyou-elementen-overzicht.pdf` | A3 landscape vector overview. Open it in Illustrator, marquee-select an element, export. Every element is its own group with a separate ID label group (7 pt grey) below it. |
| `svg/{tok,atom,comp,prod}/<id>.svg` | One SVG per element. File name equals the element ID. The viewBox is tight to the artwork, units are millimetres. |
| `elements.json` | Manifest: id, name_nl, level, category, source_page, status (extracted or rebuilt), dimensions_mm, colors, variables, built_from, tags, notes. |
| `tokens.json` | Colours (HEX, RGB, CMYK, RAL), gradients, typography, and the colour deviations that were normalised. |
| `fonts/` | Ubuntu (8 styles) under the Ubuntu Font Licence 1.0. Install them to see live text correctly. |
| `tools/` | Extraction and build scripts (see `tools/README.md`). |
| `docs/phase1-inventory.md` | The inventory the build is based on: element tables, inconsistencies found in the handbook, suggested additions. |
| `docs/build-notes.md` | What was rebuilt and why, deviations and open points from the build. |

## ID scheme

`py-{level}-{category}-{name}[-{variant}]`, lowercase kebab-case.

* `tok` tokens (colours, gradients, type), `atom` single marks (logo, shapes, pictograms, arrows, figures), `comp` reusable blocks built from atoms
  (route modules, portal plate parts, pylon bars, level rows), `prod` the numbered products of handbook sections 2.1 to 8.2 with their variants.
* Product names keep the Dutch handbook nouns (`portaal`, `pyloon`, `lichtbak`, `hoogtebalk`) as in the original examples.
  Variants end in `-front`/`-back`, `-luxe`/`-standaard`, `-1baans`/`-2baans`, `-extradisplay`.
* `built_from` in `elements.json` lists the IDs a component or product is made of. `variables` lists what changes per location
  (location name, prices, opening hours, max doorrijhoogte, speed limit, phone number, level and section codes, exit names, which pictograms).

## Colours

Exact brand values (handbook 1.3): PY-Blauw `#1A3580`, PY-Aqua `#32B9CD`, PY-Oranje `#F08300`, PY-Grijs `#AEAEAE`, PY-Zwart `#1D1D1B`.
Where the drawings deviate, 1.3 wins and the deviation is logged in `tokens.json` and in the element notes:
vector blue `#1A3680` to `#1A3580`, logo black `#010101` to `#1D1D1B`, RAL 5002 swatch `#082E7A` to `#1A3580`, RAL 9006 swatch `#A0A1A0` to `#AEAEAE`.
The verloop (blauw to aqua gradient) is not defined in 1.3. Its three stops were measured from the source (`#1A3580` to 18 percent, `#097BAE` at 62 percent, `#32B9CD` at 100 percent).
Functional colours that appear in the drawings but are not brand colours (reflective red, LED green, safety green, RVV red) are listed as `observed` tokens.

## Status values

* `extracted`: the artwork comes straight from the source paths (and live text).
* `rebuilt`: part of the element is not source vector. This covers gradients (the source stores them as shadings or 72 ppi images; the clip outline of the shading is kept and the fill is written as a real vector gradient),
  raster parts redrawn as vector (hoogtebalk bands, steel shading), placeholders (afbeeldingsmasker) and constructed elements. The notes field says what.

## Text and fonts

Editable content (location names, prices, labels, level digits) is live Ubuntu text (`font-family` Ubuntu, Ubuntu Light, Ubuntu Medium). The logo wordmark is outlines and also exists as separate wordmark atoms.
Third-party numerals (RVV signs) are outlined.

## Third-party marks

RVV signs, payment marks (contactless, Mastercard, Maestro) and escape-plan safety symbols are tagged `third-party` and are reference only. Source official files before use.
The All Jobs logo and the handbook page footer are not part of the element set.

## Rebuilding

```
python3 -I tools/build_all.py --src source/handbook.pdf          # svg/, elements.json, tokens.json
python3 -I tools/build_overview.py --src source/handbook.pdf     # overview/parkingyou-elementen-overzicht.pdf
python3 -I tools/validate.py                                     # PDF labels, SVG names and manifest IDs match; colours; every SVG opens
```
Requires Python 3 with `pymupdf`, `cairosvg`, `fonttools`, `numpy`, `Pillow`, `skia-pathops`, and the Ubuntu fonts from `fonts/` installed (copy to `~/.fonts` and run `fc-cache`).
The source PDF is not stored in the repo (copy it to `source/handbook.pdf`).
