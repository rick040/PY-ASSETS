# Print rules and drift report (PM-137)

Everything in this file is **observed in print**. None of it is an official handbook rule. The official brand values stay in `tokens.json`
(section `colors`, `gradients`, `typography`); sampled print colours that differ are in the separate `observed` section and never replace the official tokens.
Sources: the eleven print files in `source/print/`. Measurements come from the PDF content (PyMuPDF), not from screenshots.

## Decisions taken for the print library

| # | Decision |
|---|---|
| 1 | The eleven source PDFs are committed in `source/print/` (needed to rebuild; the handbook PDF stays out of the repo). |
| 2 | Master blue for print templates is the official token PY-Blauw, CMYK 100/83/0/17 (`#1A3580`). The other six print blues are drift and only listed under `observed`. |
| 3 | The two GLOW files are one application `py-app-event-sign-glow` with two variants (`-route`, `-bestemming`). |
| 4 | The Hofplein sign is typed `panel`, name `campagne` (not an info pyloon). |
| 5 | The Maashaven pyloon is a new product variant `py-prod-pyloon-laag-front-qr` (pyloon with reservation QR). The handbook product `py-prod-pyloon-laag-front` is untouched. |
| 6 | A generic `py-comp-section-bar` (title as variable) is added; the five title-bound bars stay. |
| 7 | Every template has 3 mm bleed (10 mm for the uitrit sign, as in its source). |
| 8 | The "e" badge in the payment row is EasyPark (`py-atom-partner-easypark`). |
| 9 | Stickers and the uitrit sign get a `cut-contour` group (spot ThruCut, 1 pt, 0.2 mm inside the trim). The sticker corner radius (4.2 mm) is a proposal. |
| 10 | `Naamloos-7` (RGB) is rebuilt in the token blue (CMYK); the RGB original is kept as reference. |
| 11 | `reference.svg` keeps the original copy including typos; `template.svg` has the corrected copy (`copy_corrections` in `spec.json`). |
| 12 | The terminal sticker sheet (September 2026) is split into 15 applications `py-app-sticker-terminal-*`, one per sticker design. Identical copies on the sheet (druk 3 seconden, pijl links, automaatnummer) are one application. Their `reference.svg` is the one sticker cut out of the sheet with 1.5 mm margin (`source.region_references` in `spec.json`), not the whole page. |
| 13 | The hairline die lines of the sheet (0.25 to 0.74 pt black) become the ThruCut `cut-contour` of each template, 0.2 mm inside the trim, plus 3 mm bleed. Radii are measured on the die lines; where the source has no die line (info bubble, automaat storing) the contour is a proposal. |

## 1. Colour drift

Native print values are CMYK. A viewer shows 100/83/0/17 as about `#0B3D8A`, the handbook hex is `#1A3580`: two sRGB renderings of the same brand blue.
That is why the comparison is on CMYK. "Viewer sRGB" is what PyMuPDF shows, "FOGRA39 sRGB" is the conversion with the output-intent profile of the uitrit file.

| File | Fill | Native | Viewer sRGB | FOGRA39 sRGB | Versus token |
|---|---|---|---|---|---|
| Evoluon, Inleveren, Hofplein | blue | CMYK 100/83/0/17 | #0B3D8A | #293E82 | equal to token CMYK |
| Maashaven (header, bars, logo, text) | blue | CMYK 100/86/21.2/3.7 | #1F4383 | #2F417D | M +3, Y +21.2, K -13.3 |
| Maashaven (payment badges, QR plate) | blue | CMYK 100/83/0/17 | #0B3D8A | #293E82 | equal to token; two blues on one panel |
| LaadKabel | blue | CMYK 100/85.9/6.6/0 | #1C4695 | #2F428B | M +2.9, Y +6.6, K -17 |
| Sticker diefstal | blue | CMYK 100/86.3/21.5/3.5 | #204382 | #2F417C | M +3.3, Y +21.5, K -13.5 |
| GLOW (both files) | blue | CMYK 100/84.4/5.5/0.4 | #174797 | #2D438D | M +1.4, Y +5.5, K -16.6 |
| Uitrit | blue | CMYK 100/92.5/19.2/5.9 | #27397E | #343A78 | M +9.5, Y +19.2, K -11.1 |
| Naamloos-7 | blue | RGB (ICC) #1A3680 | #1A3680 | n.a. | the old vector blue; RGB only |
| Evoluon, Hofplein | aqua | CMYK 69/0/21/0 | #24BFCD | #3ABACD | equal to token |
| Uitrit | aqua arrow, arc | CMYK 67.8/3.1/19.2/0 | #31BBCD | #44B8CE | C -1.2, M +3.1, Y -1.8 |
| LaadKabel, diefstal, Hofplein chevron | light aqua | CMYK 54/0/14/0 | #68CBDB | #7CCBDD | no token (about 78 percent of aqua in cyan); observed, kept as sampled |
| Maashaven text | black | CMYK 91.2/78.7/62/97.4 | #000000 | #1D1D1D | rich black on small text; template uses PY-Zwart |
| LaadKabel | grey | CMYK 25.1/18.4/19.5/1.5 | #BDBFBF | #C8C8C8 | hidden leftover under the blue |

Seven different blues in ten files; four files match the token. PY-Oranje and PY-Grijs are not used in any of these prints.
In the library the print blues are normalised to `#1A3580`, aquas to `#32B9CD`, black to `#1D1D1B` (the element notes say so); `reference.svg` files keep the sampled colours.

## 2. Layout and content drift versus the handbook (pyloon, handbook 3.6)

| Item | Handbook | Print (Maashaven) |
|---|---|---|
| Format | 480 x 1400 (stated) | 400 x 1000 |
| Header | P with roof, 225 mm band | plain P, 116 mm band, gradient edge kept |
| Section bars | gradient blue to aqua | solid navy |
| Location name | aqua, next to the logo | navy bold, under the wordmark (wordmark to beeldmerk 2.10 instead of 2.55) |
| Opening hours | one row plus "Alleen toegankelijk voor abonnementhouders" | three rows, no note |
| Tariffs | per 30 minutes, dagtarief, reservering, vroegboekkorting | per 60 minutes, dagtarief, **verloren kaart (new)**, reservering |
| Payment | contactless, Mastercard, Maestro, pin hand | Maestro, Mastercard, VISA, V PAY, then EasyPark, ParkBee, MyWay, Mobian |
| New block | none | "Reserveer je parkeerplaats voordelig online" with QR |
| RVV icon cluster | five signs | not present |
| Terms URL | www.parkingyou.nl/nl/algemene-voorwaarden | www.parkingyou.nl/algemene-voorwaarden (no `/nl/`) |

Other drift: the card front uses the wordmark without the beeldmerk; the tagline lockup has an aqua dot on the card back and a white dot on the A6 background (two reverse logos);
the uitrit pill has elliptical ends, the GLOW pills are full round.

## 3. Typos and copy issues

| Where | Original | Template |
|---|---|---|
| Maashaven | "zijn na de lezen op" | "na te lezen op" |
| Maashaven | "uit de wegverkeerswet" | "wegenverkeerswet" |
| Form | "toegangs-" / "middel" (manual hyphen) | whole word, reflowed |
| Form | "Naam klant: ______" (typed underscores), "Datum " (trailing space) | drawn rule, no trailing space |

Open, not changed in the templates: the asterisk after "per dag" on the Hofplein panel has no footnote anywhere; the terms URL differs between handbook and print;
the brand is spelled "ParkingYou" in the form body and "parkingyou" in the logo; two phone formats (085 4011647 and 0900-8844);
the form file name says A5 but the page is 148 x 105 mm (A6 landscape); Maashaven rows were aligned with runs of spaces (the template uses real columns);
default artboard names in file names ("Tekengebied_1", "Naamloos-7").

## 4. Production findings

* Bleed: a BleedBox is set in only 3 of 10 files (uitrit, LaadKabel, Maashaven). In the others the artwork overshoots but the boxes say trim. Templates all carry 3 mm bleed (uitrit 10 mm).
* Cut contour: only the uitrit file has one (spot `ThruCut`, 1 pt, 799.6 x 249.6 mm, 0.2 mm inside the trim). The two stickers had none; templates add it.
* Hidden leftovers: grey rectangle under LaadKabel, unused white square in Maashaven, off-page beeldmerk copies in both GLOW files, empty page 2 in the diefstal sticker. They are left out of the references and listed under `omitted` in `spec.json`.
* The QR in Maashaven is drawn as a clip path (white modules on navy, inverted). It decodes, but some older scanners fail on inverted codes.
* `Naamloos-7` is RGB only.

## 5. Third-party marks

Maestro, Mastercard (white badge versions), VISA, V PAY, EasyPark, ParkBee, MyWay, Mobian and GLOW appear as reference only, tagged `third-party`. Source the official files before use; none are redrawn.
Venue and destination names (Evoluon, Philips stadion, TD-gebouw, DLL, Parking Hofplein, Maashaven) are example values for variables, not fixed content.

## 6. Observed rules

1. **Typeface.** Ubuntu only. Regular, Medium and Bold in use. Italic only for the price numerals on the campaign panel. Light appears once, in the second URL line ("parkeren.nl") of the campaign panel.
2. **Weight pattern.** A key phrase is bold, the supporting words regular, inside one line ("Kabel terughangen" bold, "na gebruik" regular). Titles stack a regular and a bold line ("Abonnement" / "Evoluon").
3. **Leading.** 1.2 x the font size for body and headings (stickers, Maashaven). Stacked card titles are tighter: 0.94 (card) and 1.03 (form).
4. **Type scale.** Stickers: heading 60 pt, body 40 pt (ratio 1.5). Maashaven: bars 60 pt, rows 50 pt, terms 35 pt. LaadKabel: both languages 60.9 pt.
5. **Bilingual pattern.** NL first, divider, EN below. Same size and same bold pattern in both languages. Divider: white 0.7 mm at 68 percent of the width (LaadKabel), navy 0.35 mm at 91 percent (diefstal).
6. **Tagline.** "The other way of parking" in Ubuntu Regular, tracking about +60/1000 em, size 0.158 x beeldmerk height, left edge aligned with the left of the wordmark, white. The lockup is centred on both axes of the format (card back and A6 background, both measured). Wordmark width is 2.55 x the beeldmerk height in every horizontal lockup except the Maashaven location lockup (2.10).
7. **Beeldmerk as image.** Cropped: the card front uses the beeldmerk at 1.51x, bleeding off left, top and bottom. Watermark: same shape and size in aqua at 5 percent on navy, centred on the card back.
8. **Tints are transparency.** Aqua at 10 percent for input fields, aqua at 5 percent for the watermark, navy at 5 percent for the signature box. Not flat spot tints.
9. **Light aqua on navy.** CMYK 54/0/14/0 for icons on navy (plug, padlock, chevron). Not a token.
10. **Corner radii.** QR plate 11.95 mm on 118.6 (10 percent), partner badge 7.94 on 36 (22 percent), input field 1.29 on 8.3 (15.5 percent), sticker footer bar 4.23 mm on all four corners (the bottom ones lie below the trim in the source), GLOW pill full round, uitrit pill elliptical ends (rx 133.3, ry 125).
11. **Margins.** Maashaven: text starts 11.8 mm from the trim edge (2.95 percent of the width; 14.8 mm in page coordinates with the 3 mm bleed), bars run edge to edge and through the bleed. GLOW: pills 28.3 mm from both sides (9.5 percent), bottom margin 20.6 mm, pill pitch 51.4 to 51.6 mm for a 43.1 mm pill (gap about 8.4 mm; the template uses 51.5). Card front: right margin 3.5 mm, wordmark 8.6 mm from the left.
12. **GLOW pill anatomy.** Disc diameter 87.7 percent of the pill height, ring inset 4.2 mm, label 26.46 mm bold, centred in the space right of the disc. Inactive pill: the whole group at 25 percent opacity.
13. **Date field.** Three segments 9.7 + 9.7 + 19.5 mm wide, 7.1 mm high, 0.26 mm stroke, label "Datum" right aligned under it.
14. **Header curve.** The pyloon header ends in a convex curve with a thin blue to aqua gradient edge.
15. **Headline on the campaign panel.** Font size about 106 mm (cap height of the M 73.6 mm; the 78.1 mm first measured is the i with its dot), line pitch 90.4 mm, left margin 8.2 percent of the width, keywords aqua bold. "per dag" is upright Ubuntu Regular, not italic.
16. **Cut contour.** Uitrit contour 0.2 mm inside the trim, 1 pt, spot ThruCut. Used as the model for the sticker contours (corner radius proposed, not observed).

## 7. Terminal sticker sheet (TerminalStickers_September2026.pdf)

One page, 271 x 391 mm, no bleed, no trim marks, 21 white stickers with a hairline die line. Vector only (no raster), Ubuntu embedded.

* **Blue drift.** The sheet uses CMYK 99.5/85/21.4/6.8 for almost everything (also 99.6/84/21.3/6.6 and 100/86.4/21.4/3.7 on single stickers): viewer sRGB `#1C4480`, `#1E427F`, `#1C427E`, `#204382`. Not the token CMYK 100/83/0/17. Logged as `py-obs-blauw-terminal` under `observed`; templates and library elements use the token blue.
* **Black text** on the automaat stickers is pure K black (`#000000`); templates use PY-Zwart `#1D1D1B`. The QR and barcode illustrations use rich blacks (`#111617` to `#171B1D`), normalised to PY-Zwart in the library atoms.
* **Light grey QR plate** (CMYK 8.4/5.8/6.9/0, `#E6E7E6`, drawn at 90 percent) is logged as `py-obs-grijs-qrplaat`.
* **Outlined text.** "Druk 3 seconden / Press 3 seconds" and the header of the subscription pass are outlines in the source. The template sets the sticker text as live Ubuntu fitted to the glyphs (bold 5.96 mm with -0.085 mm tracking, medium italic 5.96 mm).
* **Hidden leftover.** A red bar (`#EB1E26`, 8.6 x 3.1 mm) lies under the navy header of the subscription pass illustration; it is left out of the atom.
* **Gradient.** The pass card background is a PDF shading, which the vector reader does not export. It is rebuilt as a three stop vector gradient sampled from the render; the star and hexagon pattern is a source path (10 percent white) clipped by the card in the source and cut to the card outline with a boolean intersection.
* **Pattern across stickers.** Cards and badges are scaled copies of one drawing: the phone with QR is 17.1 x 30.4 mm on the subscription sticker and about 0.88 times that on the QR sticker; payment badges are the Maashaven badges at 0.544 (round, 19.6 mm) and 0.572 (square, 20.6 mm).
* **Third party.** Payment and partner marks, the contactless line art and the pass card (Philips Stadion) are reference only, tagged `third-party`.
* **Corner radii** (mm): druk 4.78, scan pas and QR 4.65, scan code abonnement and bankpas voorhouden 4.7, bankpas invoeren 3.59, wacht 1.85, betaal and partner rows 6.93, storing balk 7.47 top and 8.58 bottom, storing pill 8.85 (full round), automaat storing 4.63, automaatnummer bar 1.82, round arrow 6.04 (circle).
