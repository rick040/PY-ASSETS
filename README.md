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
| `applications/<id>/` | Print applications (level `app`, PM-137): `reference.svg` (faithful vector copy of the print file, or of one sticker cut out of a sheet, source colours, original copy), `template.svg` (official token colours, trim plus 3 mm bleed, variables as live Ubuntu text or placeholder groups, `cut-contour` group for stickers and signs) and `spec.json` (type, trim and bleed in mm, colour space, variables with example values, `built_from`, source file, status). Applications with variants have `reference-<variant>.svg` and `template-<variant>.svg`. |
| `applications.json` | Manifest of the applications: one row per application with its variants, source files, template size, variables, `built_from`, status and copy corrections. |
| `designs/<id>/` | New designs composed from the library for a location (no earlier print file, so no `reference.svg`): `template[-<variant>].svg` (master with `cut-contour` group), `print[-<variant>].pdf` (vector print file 1:1 with bleed, DeviceCMYK with the token values, TrimBox and BleedBox set, artwork only) and `spec.json` (trim, bleed, production notes, variables, `built_from`). |
| `designs.json` | Manifest of the new designs, same row format as `applications.json` plus `production`, `origin: "new"`. |
| `overview/parkingyou-toepassingen-overzicht.pdf` | A3 landscape vector overview of the applications: original, template and exploded view with the IDs it is built from, followed by the new atoms, components and products. Same group and label rules as the element overview. |
| `docs/print-rules.md` | Decisions, colour drift, layout and copy drift, production findings and the rules observed in print (observed in print, not official handbook rules). |
| `docs/print-phase1-inventory.md` | The PM-137 inventory the print build is based on. |
| `source/print/` | The 22 print source PDFs (20 print files, the partner package slide and `TerminalStickers_September2026.pdf`, one sheet with 21 terminal stickers). |
| `fonts/` | Ubuntu (8 styles) under the Ubuntu Font Licence 1.0. Install them to see live text correctly. |
| `tools/` | Extraction and build scripts (see `tools/README.md`). |
| `docs/phase1-inventory.md` | The inventory the build is based on: element tables, inconsistencies found in the handbook, suggested additions. |
| `docs/build-notes.md` | What was rebuilt and why, deviations and open points from the build. |

## ID scheme

`py-{level}-{category}-{name}[-{variant}]`, lowercase kebab-case.

* `app` (PM-137) print applications: `py-app-{type}-{name}[-{variant}]`, for example `py-app-sticker-instructie-laadkabel` or `py-app-card-abonnement-evoluon-front`. They are built from atoms and components plus variables.
* `tok` tokens (colours, gradients, type), `atom` single marks (logo, shapes, pictograms, arrows, figures), `comp` reusable blocks built from atoms
  (route modules, portal plate parts, pylon bars, level rows), `prod` the numbered products of handbook sections 2.1 to 8.2 with their variants.
* Product names keep the Dutch handbook nouns (`portaal`, `pyloon`, `lichtbak`, `hoogtebalk`) as in the original examples.
  Variants end in `-front`/`-back`, `-luxe`/`-standaard`, `-1baans`/`-2baans`, `-extradisplay`.
* `built_from` in `elements.json` lists the IDs a component or product is made of. `variables` lists what changes per location
  (location name, prices, opening hours, max doorrijhoogte, speed limit, phone number, level and section codes, exit names, which pictograms).

## Print applications

Cards, forms, stickers (including the 15 terminal stickers of `TerminalStickers_September2026.pdf`, `py-app-sticker-terminal-*`), panels, event signs and brand backgrounds are built by combining existing atoms and components and filling in variables (`applications/<id>/spec.json` lists them).
Library elements found in print (new atoms, components and the product `py-prod-pyloon-laag-front-qr`) are in `svg/` and in `elements.json` with `origin: "print"`, `source_file` and `source_page`.
Third-party marks (payment brands, partner badges, GLOW) are reference only (`third-party` tag): source the official files.
Rules seen in practice are written down in `docs/print-rules.md` and labelled "observed in print". Colours sampled from print that differ from the brand values are in the `observed` section of `tokens.json`; they never overwrite the official tokens.

## New designs

New signs and stickers that have no earlier print file are built with `tools/build_designs.py` from library atoms and tokens, with the same template rules as the applications (token colours, trim plus bleed, live Ubuntu text with `data-variable`, `cut-contour` group, hidden guides).
Status is `proposal` until approved.

| ID | What | Size | Variants |
|---|---|---|---|
| `py-app-sign-kolom-looproute` | Column sign for the walking route to the exit, laid out like the column boards of handbook 4.7 and 4.8 (solid PY-Blauw face, white bubble with walking figure and route arrow, caption "Uitgang Voetgangers", time window "Op werkdagen van 7:00 tot 10:00 uur" in aqua). Also usable as a column sticker. | 160 x 240 mm (w x h) | `rechtdoor`, `links`, `rechts` |
| `py-app-sticker-deur-gesloten` | Door sticker for pedestrian doors that are closed at set times ("Deur gesloten", time window, follow the walking route, English line). | A3 297 x 420 mm (scales to A4) | `links`, `rechts` |
| `py-app-sticker-looproute-rond` | Round route sticker (PY-Blauw, route arrow in a white circle, walking figure, "Uitgang"); rotate it so the arrow follows the route. The background fills the whole page, so a shifted cut never shows white. | diameter 100 mm | none |
| `py-app-sticker-druk-op-de-knop` | Round sticker for a pedestrian door that opens with an exit button (PDZ, dome 94 mm), placed directly above the button (replaces a round "Push" sticker of about 22 to 24 cm): white mushroom button pictogram with press arrow, "Druk op de knop", "om de deur te openen" in aqua, English in medium italic, route arrow pointing down at the button. 200 mm lies flat on the door post (about 21 to 22 cm wide); 250 mm is larger than the current sticker but wraps around the post edges. | diameter 200 or 250 mm | `200mm`, `250mm` |

These are wayfinding signs. They do not replace the green escape route signs (NEN-EN-ISO 7010, NEN 6088).
The print PDFs are vector files in DeviceCMYK: cairo writes them, `to_cmyk()` replaces every colour with the exact token CMYK (PY-Blauw 100/83/0/17, 200 percent ink; PY-Aqua 69/0/21/0; white no ink) and stops the build on any other colour. 3 mm bleed is in the file, no crop marks, fonts embedded (as Drukwerkdeal asks). They are not formally PDF/X. Set the `cut-contour` group of the SVG master to the ThruCut spot colour when the printer needs the cut line in the file.

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
python3 -I tools/build_print.py                                  # PM-137: new print elements, applications/, applications.json, observed tokens (needs source/print/*.pdf)
python3 -I tools/build_toepassingen.py                           # overview/parkingyou-toepassingen-overzicht.pdf
python3 -I tools/validate_print.py                               # print additions: IDs, trim plus bleed, cut contour, variables, colours, QR, PDF labels
python3 -I tools/build_designs.py                                # new designs: designs/, designs.json, preview PNGs in build/designs/
```
Requires Python 3 with `pymupdf`, `cairosvg`, `fonttools`, `numpy`, `Pillow`, `skia-pathops`, and the Ubuntu fonts from `fonts/` installed (copy to `~/.fonts` and run `fc-cache`).
The source PDF is not stored in the repo (copy it to `source/handbook.pdf`).
