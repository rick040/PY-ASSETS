# Print rules and drift report (PM-137)

Everything in this file is **observed in print**. None of it is an official handbook rule. The official brand values stay in `tokens.json`
(section `colors`, `gradients`, `typography`); sampled print colours that differ are in the separate `observed` section and never replace the official tokens.
Sources: the 21 files in `source/print/` (first ten, then ten more, then one marketing slide with mock-ups). Measurements come from the PDF content (PyMuPDF), not from screenshots.

## Decisions taken for the print library

| # | Decision |
|---|---|
| 1 | The 21 source PDFs are committed in `source/print/` (needed to rebuild; the handbook PDF stays out of the repo). |
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

Seven different blues in the first ten files; four of them match the token (see section 7 for the other ten files). PY-Oranje and PY-Grijs are not used in any of these prints.
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

## 7. Second and third batch (ten more files)

Added: `BordSlagboomEVO`, `Briefpapier_nieuw`, `PR_RoadSignage`, `ParkingYou_Envelop_220x156`, `TariefConcerten`, `dranghekspandoek-dubbelzijdig_01`, `PR_WTC_Sticker`, `PR_WTC_Poster`, `posters_297x420_3_1`, `posters_420x594_3_1`.
Same decisions as in the table at the top (token blue as master, 3 mm bleed in templates, 10 mm for the banner, references keep the original copy, templates have the corrected copy, stickers get a cut-contour group).

### 7.1 Colour and file findings

* Across the 21 files the `observed` section of `tokens.json` lists 15 blues and 5 aquas that deviate from the brand values. Only `Evoluon`, `Inleveren`, `Hofplein`, `Briefpapier` (logo) and parts of `Maashaven` use the token blue exactly.
* RGB only (ICC), no CMYK: `Naamloos-7`, `PR_RoadSignage`, `ParkingYou_Envelop_220x156`, `TariefConcerten`, `PR_WTC_Sticker`, `PR_WTC_Poster` and both posters, 8 of 20 files. The envelope even claims PDF/X-1a, which requires CMYK.
* The address blue on the letterhead is CMYK 100/85.5/22.3/4 while its logo is the token (100/83/0/17): two blues on one sheet. The P+R sign has #273A7C (field) and #213A8F (logo) on one sheet.
* Light aqua exists in at least five values (CMYK 54/0/14/0, 51/1/11/0 and RGB #78C9DC, #83CBE1, #8CCDDF). None is a token.
* Raster content found: the barrier banner has a 15901 x 112 px grayscale image (fold shadow, omitted with the 20 percent rectangle it masks), the A3 poster has an indexed raster (the pale background bubble, rebuilt as a vector: it is the beeldmerk silhouette scaled 6.07x), the A2 poster has a JPEG photo of hands with a phone (never copied; the template has a placeholder group `placeholder-photo`).
* Crop marks: the envelope file has them at the BLEED edge of a 226 x 162 mm area (11.64 and 237.64 mm on a 249.28 x 185.28 mm page), not at the 220 x 156 mm trim. Confirm with the printer which edge they mean.
* Banner: both sides are in one file, the upper half rotated 180 degrees. The fold line is at y 775 mm, not at the trim middle (785 mm), so the back is 765 mm and the front 785 mm high. The source has no bottom bleed (the template adds it).
* `BordSlagboomEVO`: two magenta 1 pt rings (3.7 mm, x 150 and 330 mm, y 126.7 mm) are plain process magenta, not a spot. They look like mounting hole marks; their purpose is assumed. An empty full-page 10 percent form XObject is in the file (invisible).

### 7.2 Copy issues

| Where | Original | Template |
|---|---|---|
| Slagboombord | "i.v.m een evenement" | "i.v.m. een evenement" |
| Slagboombord | "abonnementshouders" | "abonnementhouders" (handbook spelling) |
| Briefpapier | "5611BM Eindhoven" | "5611 BM Eindhoven" (the envelope has the space) |

Open, not changed: the storing number is 085 4011647 on Maashaven and the A3 poster but 085 21 30 422 on the barrier banner; the P+R poster shows voordeligparkeren.nl, other pieces www.parkingyou.nl; lines in the slagboombord are centred 0.2 to 1.2 mm off because of typed trailing spaces; the brand is spelled "ParkingYou" in the letterhead address block.

### 7.3 Observed rules (added)

17. **Colour lockup.** The horizontal logo in colour with the tagline in PY-Aqua (0.158 x beeldmerk height, left aligned with the wordmark) is used on letterhead, envelope, P+R sign and A3 poster. A registered mark sits beside the wordmark on the letterhead only.
18. **P+R symbol.** Two white bars with rounded outer corners (radius 6.68 mm on an 88 mm wide A4 version) above and below a live bold "P+R"; used from A4 to 700 mm (scale 4.97 to 5.96).
19. **Price bubble.** The light aqua speech bubble (price in bold white, unit in regular white, both rotated about -6.7 to -6.9 degrees, pointer at the bottom) is one shape: the 700 mm sticker bubble equals the tariff panel bubble at scale 0.68.
20. **Storing contact.** Three patterns: a navy outline box with a small triangle and "Storing? Bel ..." (A3 poster), a light aqua pill with the number (banner), and a footer bar (diefstal sticker). The small triangle in the box is a thinner, rounder version of the large light aqua triangle.
21. **Bilingual on the banner.** NL line in Ubuntu Light with the key word bold, divider in light aqua (20 pt), EN line mirrors it (key word bold first). Same pattern as the laadkabel sticker, with Light instead of Regular.
22. **Calendar dates.** White calendar tiles with bold navy day number and regular month; three tiles in a row with equal gaps.
23. **Posters.** Headline outlined bold navy, QR on a navy plate with white modules (inverted), photo in the beeldmerk bubble shape (the bubble is the image mask).

## 8. Fourth batch (partner package slide)

Source: `MarktetingCampagne_ParkingYouPartner.pdf`, one A4 landscape slide (297 x 210 mm) with mock-ups (poster, two flyers, window sticker, NFC sticker). The pieces are separated by paint order and rebuilt at real size; shadows and rasters are not copied.

### 8.1 Findings

* Mock-up scale on the slide is 0.358 (the A4 poster measures 75.19 x 106.35 mm). Real sizes follow from that scale. The A5 flyer measures 148.5 mm wide in the mock-up (148 mm in the standard); the template uses 148 x 210 mm.
* The slide is RGB only (ICC). It uses a vivid blue #192AA2, a bright cyan #0AD3E6 and an orange #FF8401. They are rebuilt in the token blue (#1A3580), token aqua (#32B9CD) and the token orange (#F08300). This is the first print use of PY-Oranje. The three source colours are listed under `observed` in `tokens.json`.
* Two flat greys exist only in the mock-up (window sticker body #F0F0F0, NFC disc #E1E1E1). In the source the grey body is one image with a shadow; the template draws it as a flat vector. Both greys are observed placeholder colours, not tokens.
* The flyer back carries a real vector QR (decodes to https://parkingyou.nl/nl). The QR plate has a corner radius of about 12.6 percent, unlike `py-comp-qr-plate`.
* The price bubble on the poster is rotated 12 degrees; on the flyer it is straight. Both use the new `py-comp-price-badge-circle`.
* Sizes of the window sticker (136 x 46 mm) and the NFC sticker (70 mm round) are not in the source. They are proposals, as are the cut contours.

### 8.2 Copy issues

| Where | Original | Template |
|---|---|---|
| Flyer front | "Geldig vanaf 1 januari - niet op wedstrijddagen" | "Geldig vanaf 1 januari, niet op wedstrijddagen" |

### 8.3 Observed rules (added)

24. **Location pill.** A navy pill with a white pin icon and the location name in bold white (`py-comp-pill-location`), used on both the poster and the flyer front.
25. **Partner price badge.** A white circle with the price in bold navy italic (cents superscript) and "per dag" below (`py-comp-price-badge-circle`), overlapping the image bubble or the poster corner.
26. **Flyer split.** The front is a navy upper field with a bubble photo, the lower white strip holds the beeldmerk, claim and validity line; the back mirrors it with the app message and a QR on a navy plate.
27. **Stickers.** Partner stickers are cut around the beeldmerk bubble and the pills (contour shape), not a rectangle.
