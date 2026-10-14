# ParkingYou brand assets: Phase 1 inventory

Source: "parkingyou Huisstijlhandboek, Wayfinding & inrichting parkeervoorziening", v1.0, 09-2025, All Jobs Wayfinding & Parking Solutions. 51 pages, A3 landscape (1190.55 x 841.89 pt), InDesign 19.5 export (Adobe PDF Library 17.0), PDF 1.5, not tagged.

Status: Phase 1 only. Nothing has been built. Waiting for approval.

Legend used in the tables:

- **Src** (what the source PDF contains): `V` = real vector, `R` = raster, `V+R` = vector with a raster part.
- **Method**: `crop` = pdftocairo -svg of the page, clip by bounding box, strip stray paths, dimension lines, callouts. `rebuild-grad` = geometry extracted, the raster gradient replaced by a real vector gradient (marked "rebuilt"). `rebuild` = redrawn (marked "rebuilt"). `ref` = reference only, not an editable element.
- **third-party**: tagged as reference, official files to be sourced.
- Page numbers are PDF page numbers (they equal the printed numbers).

## 1. Technical findings (Step 2)

| Topic | Finding |
|---|---|
| Fonts embedded | Ubuntu (Light, Light Italic, Regular, Italic, Medium, Medium Italic, Bold, Bold Italic). Also Myriad Pro (cover text and page footer only), Wingdings and Unbounded (one stray glyph each on p7), RWSTTDdx (RVV numerals on portals, p15 to p21), AnwbEeVL and AnwbEexVL (RVV numerals on pylons, p23, p24), Campton Book (CAD dimension numbers, p25). |
| Live text vs outlines | Live: body text, location names, prices, level digits and section letters (Ubuntu Bold), RVV numerals. Outlined: the logo wordmark (p6, p7, cover), the hoogtebalk lettering "maximale doorrijhoogte 2,1m" (p22), some legend text on p35. |
| Gradients | Correction after the build: every blauw to aqua fill is written by InDesign as a clip path plus either a PDF shading (p9, p31, p33 and others) or a 72 ppi image inside the clip (p12, p14, p23 and others). PyMuPDF `get_drawings()` does not return either, so the earlier "all gradients are 72 ppi rasters" was too broad. The clip outline is the exact shape of the fill and is kept; the fill is rebuilt as a real vector gradient whose axis is measured from the rendered page. Footer and cover use real shadings too. |
| Pure raster content | Cover background polygons and the chapter divider banner (3000x860 px), the three third-party photos (p9 woman 175 px, p41 one-way-vision foil, p43 to p45 product photos), all 3D renders (p12, p14, p17, p23, p27, p28, p29, p30, p32, p37, p38, p47, p48, p50), brick wall backgrounds (p21, p30, p38), the car silhouette (p15, p16, p18, p19, 333x239 px at 200 ppi), the hoogtebalk red bands and chain/pendulum parts (p15 to p22, up to 105 small images per page), p35 two small legend icons. |
| Pure vector content | Logos (p6, 363 paths), colour swatches (p8), shapes (p9 except two gradient fills), pictograms (p10, 48 paths), figures and welcome banner (p40, 183 paths), RVV signs (p51, 80 paths), CAD line drawings (p20, p25, p43 to p45 dimension views, p47, p48), portal elevations (p15, p16, p18, p19: about 870 to 920 paths each, including 240 LED dots per display). |
| Colour spaces | RGB (ICC) throughout. Brand blue is stored as RGB 0.103/0.210/0.501 which is #1A3680, not the #1A3580 stated in 1.3. CMYK values exist only as text. |
| Clipping | No clipping masks around vector artwork in the source. |
| Brand gradient (measured) | Sampled from the rasters: three stops. #1A3580 held until about 25 percent, a mid blue of about #097EAF at 50 percent, #32B9CD from about 70 percent. Direction: diagonal top-left to bottom-right on bubbles, panels and lichtbak faces; vertical on the column strip (p31); horizontal on the pylon section bars (p23, p24). |

## 2. Tokens

| ID | Dutch name | Description | Page | Src | Method | Variables | built_from |
|---|---|---|---|---|---|---|---|
| py-tok-color-blauw | PY-Blauw | #1A3580, RGB 26/53/128, CMYK 100/83/0/17, RAL 5002 (best match) | 8 | V | spec value from 1.3 | none | none |
| py-tok-color-aqua | PY-Aqua | #32B9CD, RGB 50/185/205, CMYK 69/0/21/0, RAL 6027 (best match only) | 8 | V | spec value | none | none |
| py-tok-color-oranje | PY-Oranje | #F08300, RGB 240/131/0, CMYK 0/57/100/0, RAL 2003 | 8 | V | spec value | none | none |
| py-tok-color-grijs | PY-Grijs | #AEAEAE, RGB 174/174/174, CMYK 0/0/0/42, RAL 9006 | 8 | V | spec value | none | none |
| py-tok-color-zwart | PY-Zwart | #1D1D1B, RGB 29/29/27, CMYK 0/0/0/100, RAL 9005 | 8 | V | spec value | none | none |
| py-tok-color-wit | Wit (not in 1.3) | #FFFFFF, used for diapositief logo and all white signing | 6, 12 and others | V | observed | none | none |
| py-tok-color-ral-9010 | RAL 9010 (not in 1.3) | Hoogtebalk base colour, only mentioned in text on p22 | 22 | text | observed | none | none |
| py-tok-color-reflective-red | Rode reflecterende band (not brand) | #C20016, post bands p43, p44 | 43, 44 | V | observed | none | none |
| py-tok-color-led-green | LED groen (not brand) | #3AAA35 and #53A043, display dots | 12 to 25 | V | observed | none | none |
| py-tok-color-safety-green | Veiligheidsgroen (not brand) | #008A3B and #00913E, escape plan legend | 35 | V | observed | none | none |
| py-tok-color-rvv-red | RVV rood (third-party) | #E30613, RVV sign rings | 51 | V | observed | none | none |
| py-tok-gradient-verloop | Verloop (diagonal) | blauw to aqua with measured mid stop, 45 degrees | 9, 12, 14, 30, 32, 33 | R | rebuild-grad | none | blauw, aqua |
| py-tok-gradient-verloop-vertical | Verloop (vertical) | same stops, top to bottom (column strip, p31) | 31 | R | rebuild-grad | none | blauw, aqua |
| py-tok-gradient-verloop-horizontal | Verloop (horizontal) | same stops, left to right (pylon section bars) | 23, 24 | R | rebuild-grad | none | blauw, aqua |
| py-tok-type-ubuntu-light | Ubuntu Light | weight 300 | 7 | text | font via @fontsource/ubuntu | none | none |
| py-tok-type-ubuntu-light-italic | Ubuntu Light Italic | 300 italic | 7 | text | same | none | none |
| py-tok-type-ubuntu-regular | Ubuntu Regular | 400. Measured stem width of the logo "parking" matches this weight | 7 | text | same | none | none |
| py-tok-type-ubuntu-italic | Ubuntu Italic | 400 italic | 7 | text | same | none | none |
| py-tok-type-ubuntu-medium | Ubuntu Medium | 500. Handbook says this is the logo weight (see inconsistency 1) | 7 | text | same | none | none |
| py-tok-type-ubuntu-medium-italic | Ubuntu Medium Italic | 500 italic | 7 | text | same | none | none |
| py-tok-type-ubuntu-bold | Ubuntu Bold | 700 | 7 | text | same | none | none |
| py-tok-type-ubuntu-bold-italic | Ubuntu Bold Italic | 700 italic (slogan, "SMS PARKING") | 7 | text | same | none | none |
| py-tok-type-hoogtebalk-lettering | Snijletters hoogtebalk | wide geometric sans, outlined in the PDF, typeface unidentified | 22 | V (outlines) | crop | none | none |

## 3. Atoms

### 3.1 Logo family

| ID | Dutch name | Description | Page | Src | Method | Variables | built_from |
|---|---|---|---|---|---|---|---|
| py-atom-logo-stacked-color | Logo (staand, kleur) | beeldmerk above wordmark, blauw and aqua | 6 | V | crop | none | none |
| py-atom-logo-stacked-black | Logo (staand, zwart) | black version. Source black is #010101 | 6 | V | crop | none | none |
| py-atom-logo-stacked-white | Logo (staand, diapositief) | white, ring and dot transparent | 6 | V | crop | none | none |
| py-atom-logo-horizontal-color | Logo (liggend, kleur) | beeldmerk left of wordmark | 6 | V | crop | none | none |
| py-atom-logo-horizontal-black | Logo (liggend, zwart) | black | 6 | V | crop | none | none |
| py-atom-logo-horizontal-white | Logo (liggend, diapositief) | white | 6 | V | crop | none | none |
| py-atom-logo-beeldmerk-color | Beeldmerk | mark alone, also 1.4 "beeldmerk" | 6, 9 | V | crop | none | none |
| py-atom-logo-beeldmerk-black | Beeldmerk zwart | split out of black logo | 6 | V | crop | none | none |
| py-atom-logo-beeldmerk-white | Beeldmerk diapositief | split out of white logo | 6 | V | crop | none | none |
| py-atom-logo-wordmark-color | Woordmerk (kleur) | "parkingyou" outlines, blauw | 6 | V | crop | none | none |
| py-atom-logo-wordmark-black | Woordmerk (zwart) | outlines | 6 | V | crop | none | none |
| py-atom-logo-wordmark-white | Woordmerk (diapositief) | outlines | 6 | V | crop | none | none |
| py-atom-logo-horizontal-reverse | Logo liggend op blauw (candidate) | white shape, navy ring #1A3680, aqua dot. Used on all lichtbak faces and cover, not defined in 1.1 | 1, 14, 38 | V | crop | none | none |
| py-atom-logo-stacked-reverse | Logo staand op blauw (candidate) | same treatment, stacked | 1 | V | crop | none | none |
| py-atom-logo-beeldmerk-reverse | Beeldmerk op blauw (candidate) | white bubble, navy ring, aqua dot (p12 top right) | 1, 12 | V | crop | none | none |

### 3.2 Huisstijlvormen (1.4) and symbols

| ID | Dutch name | Description | Page | Src | Method | Variables | built_from |
|---|---|---|---|---|---|---|---|
| py-atom-shape-bubble-solid | volvlak | speech-bubble silhouette, flat fill (orange in the example) | 9 | V | crop | fill colour | none |
| py-atom-shape-bubble-image-mask | afbeeldingsmasker | bubble silhouette with photo. Photo is third-party raster (175 px). Becomes empty shape plus placeholder | 9 | R photo, V outline | rebuild (outline from bubble) | image | bubble-solid |
| py-atom-shape-circle | cirkel | solid circle, aqua in the example | 9 | V | crop | fill colour | none |
| py-atom-shape-bubble-gradient | verloop | bubble with blauw to aqua gradient. Source is a 103x124 px raster | 9 | R | rebuild-grad | none | bubble-solid, gradient-verloop |
| py-atom-shape-bracket-arc | (no label in handbook) beugelboog met slogan | thin arc with slogan "Voordelig parkeren zonder gedoe?" in Ubuntu Bold Italic | 9 | V | crop | slogan text | none |
| py-atom-shape-separator-arc | (no label) scheidingsboog | short arc plus dotted construction circle. Used between route modules | 9, 27, 28 | V | crop | stroke colour | none |
| py-atom-shape-pill-solid | (no label) pil, vol | solid pill, navy | 9 | V | crop | fill colour | none |
| py-atom-shape-pill-outline-gradient | (no label) pil op verloop | orange pill with white outline on gradient panel. Panel is a 304x122 px raster | 9 | V+R | rebuild-grad (panel) | pill colour | pill-solid, gradient-verloop |
| py-atom-symbol-p-roof | P met dak | white P with chevron roof, on every lichtbak, pylon and portal. Not captioned in 1.x | 12, 14, 15, 23, 37, 38 | V | crop | colour | none |

### 3.3 Arrows

The handbook shows these arrows only. Further directions are in the suggested additions list.

| ID | Dutch name | Description | Page | Src | Method | Variables | built_from |
|---|---|---|---|---|---|---|---|
| py-atom-arrow-up-circle | pijl omhoog in witte cirkel | aqua arrow in white circle | 27 | V | crop | direction, colour | none |
| py-atom-arrow-right-circle | pijl rechts in witte cirkel | aqua arrow in white circle (welcome banner) | 40 | V | crop | direction, colour | none |
| py-atom-arrow-up-plain | pijl omhoog | solid arrow, navy | 28 | V | crop | colour | none |
| py-atom-arrow-right-plain | pijl rechts | solid arrow. Lichtbak arrow (p12) has a thinner shaft than the route arrow (p28); to be verified | 12, 28 | V | crop | colour | none |
| py-atom-arrow-left-plain | pijl links | solid arrow, navy (back of voetgangersroutebord) | 28 | V | crop | colour | none |
| py-atom-arrow-downleft-plain | pijl linksonder | white arrow on lichtbak entree | 14 | V | crop | colour | none |
| py-atom-arrow-diagonal-pair-black | zwarte diagonale pijlen | pair of heavy black arrows, down-left and down-right, one group | 33, 34 | V | crop | none | none |

### 3.4 Pictograms (1.5, reused in 4.1, 4.2, 4.6)

All navy #1A3680/#1A3580 in the source. White (on navy) and aqua (on white) uses are recolours.

| ID | Dutch name | Description | Page | Src | Method | Variables | built_from |
|---|---|---|---|---|---|---|---|
| py-atom-picto-car | Route voor autoverkeer | car, front view | 10, 27 | V | crop | colour | none |
| py-atom-picto-accessible | Route naar parkeervakken voor mindervaliden | wheelchair | 10, 27, 33 | V | crop | colour | none |
| py-atom-picto-ev | Route naar parkeervakken voor electrische voertuigen | car with plug in ring | 10, 27, 34 | V | crop | colour | none |
| py-atom-picto-motorcycle | Route naar parkeervakken voor motorfietsen | motorcycle with rider | 10, 27 | V | crop | colour | none |
| py-atom-picto-family | Route naar parkeervakken voor gezinnen met kinderen | two adults and a child (4.1 calls it "families") | 10, 27 | V | crop | colour | none |
| py-atom-picto-pedestrian | Route voor voetgangers | walking person | 10, 28 | V | crop | colour | none |
| py-atom-picto-lift | Geeft route naar de lift aan | lift with up/down triangles | 10, 28, 32 | V | crop | colour | none |
| py-atom-picto-escalator | Geeft route naar de troltrap (tapis roulant) aan | escalator | 10, 28, 32 | V | crop | colour | none |
| py-atom-picto-stairs | Geeft route naar de trap aan | stairs | 10, 28 | V | crop | colour | none |
| py-atom-picto-payment-machine | Geeft route naar de betaalautomaat aan | euro sign in ring | 10, 28, 32 | V | crop | colour | none |
| py-atom-picto-toilet | Geeft route naar de toiletten aan | "WC" in ring | 10, 28 | V | crop | colour | none |
| py-atom-picto-info | Geeft route naar de beheerder/infobali aan | "i" in bubble (typo "infobali" in 1.5) | 10, 28 | V | crop | colour | none |

### 3.5 Tags, level and section markers, display, stickers, hoogtebalk

| ID | Dutch name | Description | Page | Src | Method | Variables | built_from |
|---|---|---|---|---|---|---|---|
| py-atom-tag-level-bubble-gradient | niveauaanduiding bel | gradient bubble with white digit (live Ubuntu Bold). Bubble is raster | 30 | V+R | rebuild-grad | level digit | bubble-gradient |
| py-atom-tag-level-bubble-white | niveau bel wit | big white bubble with aqua digit (overzichtsbord header) | 32 | V+R | rebuild-grad | level digit | bubble-solid |
| py-atom-tag-level-bubble-small | niveau bel klein | small white bubble with navy digit, part of "1A" | 31 | V+R | crop | level digit | bubble-solid |
| py-atom-tag-section-circle | sectie cirkel | white circle with aqua letter | 31 | V+R | crop | section letter | circle |
| py-atom-tag-section-1a | sectieaanduiding "1A" | level bubble plus section circle | 31 | V+R | crop | level digit, section letter | tag-level-bubble-small, tag-section-circle |
| py-atom-tag-level-circle-navy | niveau cirkel navy | navy circle, white digit (row on white pill) | 32 | V+R | crop | level digit | circle |
| py-atom-tag-level-circle-white | niveau cirkel wit | white circle, navy digit (row on navy pill) | 32 | V+R | crop | level digit | circle |
| py-atom-display-volvrij-vrij | VOL/VRIJ display | dark panel, LED dot matrix "VRIJ". Drawn in green only; 240 dots per instance | 12, 15, 25 | V | crop | state (VOL, VRIJ, gesloten) | none |
| py-atom-sticker-trash | vuilnisbak sticker | white bubble with aqua bin pictogram, dotted cut ring | 24, 47, 48 | V | crop | none | bubble-solid |
| py-atom-pattern-hoogtebalk-bands | hoogtebalk rode banden | red/white band pattern, 250 mm bands. Bands are rasters in the source | 22 | R | rebuild | bar length | none |
| py-atom-text-hoogtebalk-lettering | snijletters | "maximale doorrijhoogte 2,1m", outlines, 1000 mm wide | 22 | V | crop | height value | none |

### 3.6 People figures (6.1)

| ID | Dutch name | Description | Page | Src | Method | Variables | built_from |
|---|---|---|---|---|---|---|---|
| py-atom-figure-walk | figuur 1 | walking | 40 | V | crop | none | none |
| py-atom-figure-dance | figuur 2 | one arm up, one out | 40 | V | crop | none | none |
| py-atom-figure-wave | figuur 3 | waving (also used large in welcome banner) | 40 | V | crop | none | none |
| py-atom-figure-jump | figuur 4 | jumping, both arms up | 40 | V | crop | none | none |
| py-atom-figure-point | figuur 5 | pointing | 40 | V | crop | none | none |
| py-atom-figure-bags-walk | figuur 6 | walking with two bags | 40 | V | crop | none | none |
| py-atom-figure-bags-cheer | figuur 7 | cheering with two bags | 40 | V | crop | none | none |
| py-atom-figure-cap-point | figuur 8 | attendant with cap, pointing | 40 | V | crop | none | none |
| py-atom-figure-cap-wave | figuur 9 | attendant with cap, waving | 40 | V | crop | none | none |

The handbook gives no names for the figures. Names above are proposals.

### 3.7 Third-party reference marks (tagged third-party)

| ID | Dutch name | Description | Page | Src | Method | Variables | built_from |
|---|---|---|---|---|---|---|---|
| py-atom-rvv-a01 | A01 Maximumsnelheid | speed limit | 51 | V | crop | speed value | none |
| py-atom-rvv-b06 | B06 Verleen voorrang | give way | 51 | V | crop | none | none |
| py-atom-rvv-c02 | C02 Eenrichtingweg, in deze richting gesloten | no entry (also back of autoroutebord) | 51, 27 | V | crop | none | none |
| py-atom-rvv-c03 | C03 Eenrichtingsweg | one-way, blue | 51 | V | crop | none | none |
| py-atom-rvv-c07 | C07 Gesloten voor vrachtauto's | trucks | 51 | V | crop | none | none |
| py-atom-rvv-c10 | C10 Gesloten voor motorvoertuigen met aanhangwagen | with trailer | 51 | V | crop | none | none |
| py-atom-rvv-c11 | C11 Gesloten voor motorfietsen | motorcycles | 51 | V | crop | none | none |
| py-atom-rvv-c16 | C16 Gesloten voor voetgangers | pedestrians | 51 | V | crop | none | none |
| py-atom-rvv-d2 | D2 Gebod voor alle bestuurders het bord voorbij te gaan | pass on this side (handbook writes "D2") | 51 | V | crop | direction | none |
| py-atom-rvv-e06 | E06 Gehandicaptenparkeerplaats | disabled parking | 51 | V | crop | none | none |
| py-atom-rvv-e08c | E08c Laadplaats voor elektrische voertuigen | EV charging | 51 | V | crop | none | none |
| py-atom-rvv-e10 | E10 Parkeerschijfzone | disc zone, "max 2h" | 51 | V | crop | zone text, duration | none |
| py-atom-rvv-max-height | maximale doorrijhoogte bord (not in 9.2) | height limit sign, numerals in RWS or ANWB font | 15, 16, 23 | V | crop | height value | none |
| py-atom-rvv-no-bicycles | fietsen verboden (not in 9.2) | bicycles prohibited, pylon row | 23, 24 | V | crop | none | none |
| py-atom-sign-camera | cameratoezicht (not in 9.2, not RVV) | black ring with camera, pylon row | 23, 24 | V | crop | none | none |
| py-atom-sign-ev-allowed-green | groene cirkel auto met stekker (not in 9.2) | green ring, car and plug, portal cluster | 15, 16 | V | crop | none | none |
| py-atom-payment-contactless | contactloos betalen | contactless symbol with hand and card | 23, 24 | V | crop | none | none |
| py-atom-payment-mastercard | Mastercard | brand logo | 23, 24 | V | ref | none | none |
| py-atom-payment-maestro | Maestro | brand logo | 23, 24 | V | ref | none | none |
| py-atom-payment-pin-hand | (unnamed) hand met pas | hand inserting a card | 23, 24 | V | crop | none | none |
| py-atom-escape-exit | uitgang | green exit sign | 35 | V | crop | none | none |
| py-atom-escape-emergency-exit | nooduitgang | green running man | 35 | V+R | crop | none | none |
| py-atom-escape-first-aid | EHBO middelen | green cross | 35 | V | crop | none | none |
| py-atom-escape-route | vluchtroute | green path with arrows | 35 | V | crop | none | none |
| py-atom-escape-door-release | noodontgrendeling deur | door release | 35 | V | crop | none | none |
| py-atom-escape-extinguisher | brandblusser | red extinguisher | 35 | V | crop | none | none |
| py-atom-escape-manager | beheerder | information symbol | 35 | V | crop | none | none |
| py-atom-escape-lift-no-use | bij brand lift niet gebruiken | prohibition symbol | 35 | V | crop | none | none |

Tagging note: payment marks and RVV signs are tagged third-party. The escape-plan symbols are standard safety pictograms and are also tagged third-party/standard pending your answer to question 5.

## 4. Components

| ID | Dutch name | Description | Page | Src | Method | Variables | built_from |
|---|---|---|---|---|---|---|---|
| py-comp-route-panel-pill | routebord paneel | pill-shaped panel, 200 high, 600/800/1000 wide, radius 100 | 27, 28, 29 | V | crop | width, fill (navy front, white pedestrian front) | atom-shape-pill-solid |
| py-comp-route-module-picto | route module pictogram | one picto slot plus arc | 27 | V | crop | which picto | atom-picto-*, shape-separator-arc |
| py-comp-route-module-separator | route module scheiding | separator arc between modules | 27, 29 | V | crop | none | atom-shape-separator-arc |
| py-comp-route-module-text | route module tekst | label slot ("in" in the example), white Ubuntu | 27 | V | crop | label text | none |
| py-comp-route-module-arrow | route module pijl | arrow in white circle, end of panel | 27 | V | crop | direction | atom-arrow-up-circle |
| py-comp-route-back-noentry | achterzijde routebord | red no-entry sign on navy pill | 27 | V | crop | none | route-panel-pill, rvv-c02 |
| py-comp-walk-route-figure-block | voetgangersfiguur blok | pedestrian figure plus arc, mirrored on back | 28 | V | crop | direction | picto-pedestrian, separator-arc |
| py-comp-walk-route-row | voetgangersroute regel | picto strip, "Uitgang Naam", arrow, aqua rule. Two rows per board | 28 | V | crop | exit names, pictos, arrow directions | picto-lift, escalator, stairs, payment-machine, arrow-*-plain |
| py-comp-portal-p-block | portaal P blok links | aqua block with curved navy edge and P-roof | 15, 16, 18, 19, 37 | V+R | rebuild-grad | none | symbol-p-roof |
| py-comp-portal-name-block | portaal naamblok | horizontal reverse logo plus location name, Ubuntu Bold white | 15, 16 | V | crop | location name | logo-horizontal-reverse |
| py-comp-portal-display-slot | portaal displayvak | single VOL/VRIJ display position | 15, 16 | V | crop | state | display-volvrij-vrij |
| py-comp-portal-display-slot-dual | portaal displayvak dubbel | two displays labelled "Bezoekers" and "Vergunninghouders" | 15, 16, 18, 19 | V | crop | labels, states | display-volvrij-vrij |
| py-comp-rvv-cluster-portal | RVV icon cluster portaal | four signs in 2x2 on a white tab with curved edge (5, truck, max height, green EV) | 15, 16, 18, 19 | V | crop | speed, height, which signs | rvv-a01, rvv-c07, rvv-max-height, sign-ev-allowed-green |
| py-comp-rvv-cluster-pyloon | RVV icon cluster pyloon | five signs in a row (5, 2,1m, truck, bicycle, camera) | 23, 24 | V | crop | speed, height | rvv-a01, rvv-max-height, rvv-c07, rvv-no-bicycles, sign-camera |
| py-comp-portal-face-1baans | portaal beeldplaat 1-baans | P block, name block, display, RVV cluster. Width variable | 15, 18 | V+R | crop | location name, width, extra display | portal-p-block, name-block, display-slot, rvv-cluster-portal |
| py-comp-portal-face-2baans | portaal beeldplaat 2-baans | name centred, display and RVV 2x2 on the right | 16, 19 | V+R | crop | location name, width | same as 1-baans |
| py-comp-face-aanrijroute | lichtbakfront aanrijroute | gradient face, P-roof, arrow, beeldmerk, display zone | 12 | V+R | rebuild-grad | arrow direction, display fitted | symbol-p-roof, arrow-right-plain, logo-beeldmerk-reverse, display-volvrij-vrij |
| py-comp-face-entree | lichtbakfront entree | logo, P-roof, arrow, location name | 14 | V+R | rebuild-grad | location name, arrow direction | logo-horizontal-reverse, symbol-p-roof, arrow-downleft-plain |
| py-comp-face-voetganger-staand | lichtbakfront voetgangersentree | logo, P-roof, pedestrian figure, location name | 38 | V+R | rebuild-grad | location name | logo-horizontal-reverse, symbol-p-roof, picto-pedestrian |
| py-comp-face-voetganger-liggend | lichtbakfront liggend | P block, beeldmerk, name, white tab with pedestrian | 37 | V+R | rebuild-grad | location name | portal-p-block, logo-beeldmerk-reverse, picto-pedestrian |
| py-comp-hoogtebalk-bar | hoogtebalk | bar with bands plus lettering | 22 | V+R | rebuild | length, height text | pattern-hoogtebalk-bands, text-hoogtebalk-lettering |
| py-comp-pyloon-header-band | pyloon kopband | white P-roof on blauw/aqua curved band | 23, 24 | V+R | rebuild-grad | none | symbol-p-roof, gradient-verloop |
| py-comp-pyloon-section-bar-openingstijden | balk Openingstijden | gradient bar with live label | 23, 24 | V+R | rebuild-grad | none (label fixed) | gradient-verloop-horizontal |
| py-comp-pyloon-section-bar-tarieven | balk Tarieven | same | 23, 24 | V+R | rebuild-grad | none | same |
| py-comp-pyloon-section-bar-betalingsmogelijkheden | balk Betalingsmogelijkheden | same | 23, 24 | V+R | rebuild-grad | none | same |
| py-comp-pyloon-section-bar-calamiteiten | balk Calamiteiten | same | 23, 24 | V+R | rebuild-grad | none | same |
| py-comp-pyloon-section-bar-algemene-voorwaarden | balk Algemene voorwaarden | same | 23, 24 | V+R | rebuild-grad | none | same |
| py-comp-pyloon-location-name-slot | locatienaam pyloon | beeldmerk, "parkingyou", location name in aqua Ubuntu Bold | 23, 24 | V | crop | location name | logo-horizontal-color |
| py-comp-pyloon-opening-hours | openingstijden blok | days and hours, optional blue note line | 23, 24 | V | crop | days, hours, note | none |
| py-comp-price-strip-110x400 | deelfolie 110x400 | four tariff rows, rows 3 and 4 in blauw | 23, 24 | V | crop | tariff names, prices | none |
| py-comp-pyloon-payment-row | betaalmogelijkheden rij | contactless, Mastercard, Maestro, pin hand | 23, 24 | V | crop | which marks | payment-* |
| py-comp-pyloon-emergency | calamiteiten blok | text plus phone number | 23, 24 | V | crop | phone number | none |
| py-comp-pyloon-terms | algemene voorwaarden blok | text, URL, RVV cluster | 23, 24 | V | crop | URL, signs | rvv-cluster-pyloon |
| py-comp-pyloon-back-tot-ziens | achterzijde "Tot ziens" | header band, "Tot ziens", logo at bottom | 23 | V+R | rebuild-grad | goodbye text, optional image | header-band, logo-stacked-color |
| py-comp-pyloon-back-logo | achterzijde alleen logo | white panel with logo | 24 | V | crop | none | logo-stacked-color |
| py-comp-section-wrap-strip | kolomband sectie | 300 mm vertical gradient strip, "1A" repeated | 31 | V+R | rebuild-grad | level, section, repeats, width | tag-section-1a, gradient-verloop-vertical |
| py-comp-overview-level-header | overzichtsbord niveaukop | big white bubble with aqua digit | 32 | V+R | rebuild-grad | level digit | tag-level-bubble-white |
| py-comp-overview-level-row-filled | niveaurij gevuld | navy pill, white circle, white icons | 32 | V+R | crop | level, icons | pill-solid, tag-level-circle-white, picto-escalator, picto-lift, picto-payment-machine |
| py-comp-overview-level-row-outlined | niveaurij wit | white pill, navy circle, aqua icons | 32 | V+R | crop | level, icons | pill-solid, tag-level-circle-navy |
| py-comp-bord-picto-bubble-face | rijstvlies bord voorzijde | gradient panel, white bubble with pictogram, caption in Ubuntu Bold | 33, 34 | V+R | rebuild-grad | picto, caption | bubble-solid, picto-accessible or picto-ev |
| py-comp-bord-arrow-plate | pijlplaat | white plate, black diagonal arrows | 33, 34 | V | crop | none | arrow-diagonal-pair-black |
| py-comp-welcome-wall-banner | welkom muurbanner | navy half-pill, "Welkom bij", logo, location name, arrow circle, waving figure | 40 | V | crop | location name | logo-horizontal-white, arrow-right-circle, figure-wave |
| py-comp-location-name-slot | locatienaam slot | generic name field, Ubuntu Bold, white or aqua | 14, 37, 38, 40 | V | crop | location name | none |
| py-comp-escape-legend | legenda vluchtweg | eight symbols plus labels | 35 | V+R | crop | which symbols | atom-escape-* |
| py-comp-escape-safety-instructions | veiligheidsinstructies | text block (ongeval, ontruiming, brand) | 35 | V | crop | text | none |

## 5. Products

Specification columns condensed into one cell: dimensions in mm; M = materials and finish; Mt = mounting; L = lighting; RAL.

| ID | Dutch name | Page | Src | Method | Specification | Variables | built_from |
|---|---|---|---|---|---|---|---|
| py-prod-lichtbak-aanrijroute-display | 2.1 Uitsteeklichtbak in aanrijroute, met display | 12 | V+R | crop + rebuild-grad | 1000 x 1250 face, 200 deep. Display 200x400 (zicht 170x370). Spacer aluminium koker 40x150. Pole aluminium koker 100x200. Min 2500 above ground. M: aluminium profile powder coat, blockout foil so only white signing and beeldmerk light. Mt: pole. L: internal LED. RAL 5002, 9006 | arrow direction, display state | face-aanrijroute, display-volvrij |
| py-prod-lichtbak-aanrijroute-nodisplay | same without display | 12 | V+R | same | 1000 x 1000 | arrow direction | face-aanrijroute |
| py-prod-lichtbak-entree | 3.1 Uitsteeklichtbak bij entree | 14 | V+R | same | 1000 x 1000, 100 deep. Spacer koker 40x70. Min 2500 above ground. M: opal image plate with blockout foil, profile RAL 5002. Mt: wall, perpendicular. L: internal LED. RAL 5002, 9006 | location name, arrow direction | face-entree |
| py-prod-portaal-1baans-luxe | 3.2.1 Portaal 1-baans luxe | 15 | V+R | crop + rebuild-grad | plate 520 high, frame 600 high, 200 deep. Width variable (3300 in illustration). Hoogtebalk 2500x90 on gaffelset 300. Posts aluminium or RVS koker 100x200. M: aluminium plate 2 mm with full colour foil and laminate, illuminated box letters. Mt: two posts. RAL 5002, 9006 | location name, width, max height, speed, post height | portal-face-1baans, hoogtebalk-bar |
| py-prod-portaal-1baans-luxe-extradisplay | with extra display for vergunninghouders | 15 | V+R | same | as above plus second display | same | portal-face-1baans, display-slot-dual |
| py-prod-portaal-2baans-luxe | 3.2.2 Portaal 2-baans luxe | 16 | V+R | same | width variable (6600 in illustration). Two hoogtebalken, two gaffelsets | same | portal-face-2baans |
| py-prod-portaal-2baans-luxe-extradisplay | with extra display | 16 | V+R | same | as above | same | portal-face-2baans, display-slot-dual |
| py-prod-portaal-luxe-spec | 3.2.3 Portaal technische specificaties (luxe) | 17 | R | ref | isometric: frame koker 50x200 RAL 5002, spacer 40x150x2 and 520 high, post 100x200 | none | none |
| py-prod-portaal-1baans-standaard | 3.3.1 Portaal 1-baans standaard | 18 | V+R | same | plate 500, frame 600. M: aluminium profile RAL 5002, clear plate with blockout foil. L: internal LED. RAL 5002, 9006 | same as luxe | portal-face-1baans |
| py-prod-portaal-1baans-standaard-extradisplay | with extra display | 18 | V+R | same | | same | portal-face-1baans, display-slot-dual |
| py-prod-portaal-2baans-standaard | 3.3.2 Portaal 2-baans standaard | 19 | V+R | same | Can also be wall mounted without posts | same | portal-face-2baans |
| py-prod-portaal-2baans-standaard-extradisplay | with extra display | 19 | V+R | same | | same | portal-face-2baans, display-slot-dual |
| py-prod-portaal-standaard-spec | 3.3.3 Portaal technische specificaties (standaard) | 20 | V | crop | CAD: profile 200 wide, R8.8, 31/126/31, 6 mm slots; frontplate polycarbonate 4 mm; double powder coat RAL 5002 | none | none |
| py-prod-wandbord | 3.4 Wandbord | 21 | V+R | crop | 300 high, width variable. M: aluminium sandwich panel with full colour foil. Mt: directly on wall; display on bracket. Optional two hoogtebalken | location name, width | portal-face-2baans, hoogtebalk-bar |
| py-prod-hoogtebalk-ketting | 3.5 Hoogtebalk met ketting | 22 | V+R | rebuild | 2000 x 90, hanger distance 1500, chain 500 inside or 150 outside max. Max bar length 6000. M: aluminium RAL 9010, red bands foil. Snijletters retro reflective black | length, height text | hoogtebalk-bar |
| py-prod-hoogtebalk-gaffel | Hoogtebalk met gaffelset | 22 | V+R | rebuild | 2500 x 90, hanger distance 1500, gaffelset max 1000. Foil 3M 580-72 | same | hoogtebalk-bar |
| py-prod-hoogtebalk-pendel | Hoogtebalk met starre pendel | 22 | V+R | rebuild | 3000 x 90, hanger distance 2000, pendel RVS koker 40x40 max 2000 plus chain | same | hoogtebalk-bar |
| py-prod-pyloon-laag-front | 3.6 Informatiepyloon, voorzijde | 23 | V+R | crop + rebuild-grad | panel 1000 x 400 aluminium sandwich, total height 1400, width 480 over posts. Posts RVS koker 40x40x2, ligger 20x20x2, foot plate 100x100x5, plan 540 x 100. M: RVS pyloon powder coated RAL 9006. Double sided | location name, opening hours, tariffs, phone, URL, which signs | pyloon-header-band, section-bar-*, location-name-slot, opening-hours, price-strip, payment-row, emergency, terms |
| py-prod-pyloon-laag-back | achterzijde "Tot ziens" | 23 | V+R | same | 400 x 1000 | goodbye text | pyloon-back-tot-ziens |
| py-prod-pyloon-hoog-vuilnisbak-front | 3.7 Informatiepyloon hoog met vuilnisbak, voorzijde | 24 | V+R | same | total height 2000: panel 1000 plus bin zone 1000. Bin Dulce 50L powder coat RAL 5002, sticker "200x16,6" in text. RAL 9006 for pyloon | as 3.6 | as 3.6 plus sticker-trash |
| py-prod-pyloon-hoog-vuilnisbak-back | achterzijde | 24 | V | crop | 400 x 1000, logo in print foil | none | pyloon-back-logo |
| py-prod-display-volvrij | 3.8 Digitale display | 25 | V | crop | 414 with bracket, body 400 x 200 x 93, holes O10 at 264. States vol, vrij, gesloten via PMS. Standalone or in lichtbak | state | atom-display-volvrij-vrij |
| py-prod-routebord-auto-600-front | 4.1 Autoroutebord 600 | 27 | V+R | crop | 200 x 600, radius 100. Aluminium sandwich panel, wire and eyelets. Max 5 modules, more than 5 means two boards. RAL 9006 (Verfkleur) | pictos, label, arrow | route-panel-pill, route-module-* |
| py-prod-routebord-auto-1000-front | Autoroutebord 1000 | 27 | V+R | crop | 200 x 1000, five modules (car, "in", accessible, EV, arrow). An 800 width is mentioned but not drawn | same | same |
| py-prod-routebord-auto-back | achterzijde | 27 | V | crop | no-entry sign | none | route-back-noentry |
| py-prod-routebord-voet-front | 4.2 Voetgangersroutebord voorzijde | 28 | V+R | crop | 200 x 1000 | exit names, pictos, arrows | route-panel-pill, walk-route-* |
| py-prod-routebord-voet-back | achterzijde (mirrored) | 28 | V+R | crop | figure direction follows first named exit | same | same |
| py-prod-routebord-spec | 4.3 Routeborden technische gegevens | 29 | V+R | crop | sandwich panel, wooden core painted RAL 9006 set back 10 mm all round, radius 100, side view 10/180/10 | none | none |
| py-prod-niveauaanduiding | 4.4 Niveauaanduiding | 30 | V+R | rebuild-grad | 420 x 350 sandwich panel on painted wooden core RAL 9006. Examples 0, 1, 2 | level digit | tag-level-bubble-gradient |
| py-prod-sectieaanduiding-kolomband | 4.5 Sectieaanduiding | 31 | V+R | rebuild-grad | 300 high, variable width. High quality wall foil, full colour plus laminate, glued on columns | level, section, width | section-wrap-strip |
| py-prod-overzichtsbord | 4.6 Overzichtsbord | 32 | V+R | rebuild-grad | 400 x 550, plus 90 per extra level. Aluminium sandwich panel | levels, icons per level | overview-level-header, level-row-* |
| py-prod-overzichtsbord-frame | houten frame | 32 | V | crop | multiplex 20 mm, 50 mm strips, 10 mm inset, RAL 9006 | none | none |
| py-prod-bord-mindervaliden | 4.7 Mindervaliden parkeerplek aanduiding | 33 | V+R | crop + rebuild-grad | 400 x 600. Rijstvlies board 8 mm (wall) or 16 mm (pole). Full colour foil plus laminate | caption | bord-picto-bubble-face |
| py-prod-bord-pijlplaat | pijlplaat (4.7, 4.8) | 33, 34 | V | crop | 400 x 200, same material | none | bord-arrow-plate |
| py-prod-buispaal | optionele buispaal | 33, 34 | V+R | crop | 1000 long, O48, round foot plate, powder coat RAL 9006 | none | none |
| py-prod-bord-ev | 4.8 EV-laad parkeerplek aanduiding | 34 | V+R | crop + rebuild-grad | 400 x 600, caption "Oplaadpunt" | caption | bord-picto-bubble-face |
| py-prod-vluchtwegplattegrond | 4.9 Vluchtwegplattegrond | 35 | V+R | crop + rebuild-grad | no dimensions given, aspect about 1.43:1. Aluminium sandwich panel with full colour foil | floor plan, symbols | escape-legend, escape-safety-instructions, logo-horizontal-color |
| py-prod-lichtbak-voetganger-liggend | 5.1 Voetgangersentree lichtbak (liggend) | 37 | V+R | crop + rebuild-grad | 2500 x 300 x 100. Aluminium profile RAL 5002, clear plate with blockout foil, LED. Tech info in 3.3.3 | location name | face-voetganger-liggend |
| py-prod-lichtbak-voetganger-staand | 5.2 Voetgangersentree lichtbak (staand) | 38 | V+R | crop + rebuild-grad | 800 x 1000, 100 deep, spacer koker 40x70, mounted above the pedestrian entrance, RAL 5002, 9006 | location name | face-voetganger-staand |
| py-prod-anti-rampaal | 7.1 RVS anti-rampaal | 43 | V+R | crop (CAD views) | O139,7, 850 above ground, 650 buried. RVS 304 brushed K320, concrete filled, two red reflective bands | none | none |
| py-prod-bolderpaal | RVS bolderpaal | 43 | V+R | crop | O139,7, 850, foot plate O220, 8 thick | none | none |
| py-prod-pms-beschermpaal | PMS beschermpaal | 44 | V+R | crop | 1000 high, plate 220x220, holes O14 at 180, bands 50 from top | none | none |
| py-prod-flexpost-klein | 7.2 Flexpost klein | 45 | V+R | crop | 750 high, O80, foot O210. Black plastic with white reflective bands | none | none |
| py-prod-flexpost-groot | Flexpost groot | 45 | V+R | crop | 1000 high, O160, foot 300 x 220 | none | none |
| py-prod-vuilnisbak-wand | 8.1 Vuilnisbak wandmontage | 47 | V | crop | model Dulce 50 L, 675 x 400 x 265, RAL 5002 powder coat, with trash sticker | none | atom-sticker-trash |
| py-prod-vuilnisbak-staanders | 8.2 Vuilnisbak op staanders | 48 | V+R | crop | total height 850, RVS koker 40x40 on plate 80x80, RAL 9006 | none | atom-sticker-trash |
| py-prod-rijstvliesbord-blank | 9.1 (Rijstvliesborden) | 50 | R | ref | blank board render, text on biobased rijstvlies material only | none | none |

9.2 RVV signing is covered by the third-party atoms in 3.7.

### Spec-only items without artwork

6.2 Folies technische specificaties: muurfolie (high-tack adhesive, direct UV full colour print, laminate) and raamfolie one-way-vision (calendered white perforated foil, black reverse, full colour print). Page 41 shows a third-party photo only. These go in elements.json notes, not in the PDF.

## 6. Counts (proposed)

| Level | Count |
|---|---|
| Tokens | 23 |
| Atoms | 91 (of which 28 third-party or standard marks, 3 reverse-logo candidates) |
| Components | 45 |
| Products | 47 (of which 4 are spec or reference sheets) |

## 7. Inconsistencies and likely errors

Not fixed. Section 1.3 wins where drawings deviate (logged here).

| # | Pages | Finding |
|---|---|---|
| 1 | 6, 7 | Logo weight. p6 says "parking" is Ubuntu Medium and "you" Ubuntu Bold. p7 labels the logo face "Ubuntu Medium (logo)". Measured on the vector outlines: the "i" stem is 120 units (Ubuntu Regular 120, Medium 149, Bold 178), so "parking" is Regular. "you" matches Bold. Outlines win. |
| 2 | 6, 7, 8 | Black. The black logo is #010101, the p7 specimen is #1D1D1B (PY-Zwart). |
| 3 | 8, 10 | Blue. 1.3 says #1A3580, vector fills are #1A3680. p10 mixes both (34 paths #1A3680, 10 paths #1A3580). |
| 4 | 6, 8 | Naming. p6 "donkerblauw" and "lichtblauw (69/0/21/0)" versus 1.3 "PY-Blauw" and "PY-Aqua". |
| 5 | 8 | RAL are best match only (handbook says so). 6027 is green-leaning, drawn swatch #75B8B6 versus PY-Aqua #32B9CD. RAL 5002 swatch #082E7A is much darker than #1A3580. RAL 9010 (hoogtebalk) is missing from 1.3. |
| 6 | 9 and all faces | The verloop has no definition in 1.3. Source gradients are 72 ppi rasters. Three-stop gradient is measured, not specified. |
| 7 | 22 versus 15, 16, 18, 19, 21 | Hoogtebalk height labelled 900 mm on p22 (three times), 90 mm elsewhere. 90 is meant. |
| 8 | 15, 18 | Portal drawings show the RVV max-height sign as 2,4m while the hoogtebalk text on the same drawing reads 2,1m. p16, p19, p21, p23, p24 use 2,1m. |
| 9 | 3, 50, 51 | TOC lists 9.1 "Rijstvliesborden" (p50) and 9.2 "RVV signing" (p51). p50 header reads "9.1 RVV signing" while its content is rijstvliesborden. p51 reads "9.2 RVV signing". |
| 10 | 3 versus page headers | TOC "4. Signing in de parkeergarages" versus page headers "parkeergarage". TOC "6. Muur- en Raamfolies" versus "raamfolies". TOC "3.5 hoogtebalken" lowercase. p49 "Rijstvlies borden" versus TOC "Rijstvliesborden". |
| 11 | 10, 27 | "gezinnen met kinderen" (p10) versus "families" (p27). "electrische" (p10) versus "elektrische". "infobali" (p10) is a typo for infobalie. |
| 12 | 7 | "gewaarborchd" for gewaarborgd, unmatched opening quote before Ubuntu, and a stray Wingdings arrow and Unbounded space in the "MEETING ROOM 308" sample. |
| 13 | 24 | Bin sticker "200x16,6mm", most likely 200x166 mm. |
| 14 | 24 | Colour box on p24 lists only RAL 9006, but the bin is RAL 5002. |
| 15 | 14, 38 | Vertical dimensions 40 + 900 + 40 = 980, but the face is 1000 high. |
| 16 | 38 | Note text "haaks aan de wand bij de entree" is copied from 3.1. p38 itself says "boven de voetgangersingang". |
| 17 | 15, 16 vs 18, 19 | Plate height 520 (luxe) versus 500 (standaard) under the same 600 frame. Intentional? p15 top view labels frame "100mm" while p17 says frame koker 50x200. |
| 18 | 30 | Dimensions 420, 400 and 350. Text says 420x350. The 400 is unexplained. |
| 19 | 12, 15, 25 | Display. p12, p15, p16 show red and green dots, p25 shows green only. A "VOL" state is never drawn. |
| 20 | 1.1 versus products | The white logo on every lichtbak face (white shape, navy ring, aqua dot) differs from the diapositief in 1.1 (transparent ring and dot). |
| 21 | 15 to 24, 51 | RVV numerals are set in three different fonts (RWS, ANWB, outlined on p51). Signs used in drawings (max height, bicycles, camera, green EV) are not in 9.2. |
| 22 | 22 | Hoogtebalk lettering is outlined. The typeface is unidentified and no font name is in the PDF (Unbounded is embedded only as one stray space on p7). |
| 23 | 22 | "RAL 9010 wit conform NEN 2443" and 3M 580-72 foil are the only places RAL 9010 appears. |
| 24 | 3.6, 3.7 | "RVS pyloon gepoedercoat in RAL 9006": stainless steel with powder coat, confirm. Front width 480 vs plan 540 is the foot plate overhang. |
| 25 | 9 | The bottom row of 1.4 has four shapes without labels. Names here are proposals. |
| 26 | 35 | No dimensions. Annotation in non-brand pink. Escape symbols are standard safety signs and green is not a brand colour. |
| 27 | 23, 24 | "wegenverkeerswet" should be capitalised, and "reglement verkeersregels en verkeerstekens" is incomplete (RVV 1990). |

## 8. Suggested additions (not in the PDF)

1. VOL and gesloten states of the display.
2. Remaining arrow directions and styles as rotations of the existing paths.
3. Routebord width 800, mentioned on p27 but not drawn.
4. Level bubbles for every digit and section letters as live-text templates.
5. A white-on-gradient and a navy-on-white version of the P-roof symbol.
6. Official files for RVV, Mastercard, Maestro, contactless and safety symbols.

## 9. Proposed repo structure

```
py-assets/
  README.md                 naming, IDs, how to export
  tokens.json               colours (HEX, RGB, CMYK, RAL), gradients, typography
  elements.json             one row per element (id, name_nl, level, category, source_page, status, dimensions_mm, colors, variables, built_from, notes)
  svg/
    tok/  atom/  comp/  prod/    one SVG per element, filename = ID, viewBox tight to the artwork
  overview/
    parkingyou-elementen-overzicht.pdf
  fonts/                    Ubuntu (OFL) and licence
  source/                   handbook PDF (optional, see question 12)
  tools/                    extract.py, build_overview.py, validate.py
  docs/                     phase1-inventory.md, inconsistencies.md
```

## 10. Proposed PDF page layout

A3 landscape (420 x 297 mm), white background, 15 mm margins, 16 pt gutters.

1. Cover, then index (ID prefix, page, count).
2. Tokens: one page for colours (swatch, HEX, RGB, CMYK, RAL), one for gradients, one for type specimens (live Ubuntu text).
3. Atoms: pages by family (logos, shapes, arrows, pictograms, tags and display, figures, third-party). Grid of fixed cells, 6 columns, element centred, one scale per page.
4. Components: same grid, 4 columns.
5. Products: one consistent scale per page (1:10 proposed), front and back side by side, spec block on the right (dimensions, materials, RAL, handbook page). Page order follows the handbook numbering.
6. Every element is one top-level group with no clipping mask. Label group below each element: ID plus Dutch name, 7 pt neutral grey (#8A8A8A), separate group named "labels".
7. Gradients as real vector gradients, text live with Ubuntu embedded, wordmark also as outlines in the logo atoms.
