# PM-137 Phase 1: print applications inventory

Status: Phase 1 (approved). Correction found during Phase 2: the card back watermark is aqua at 5 percent, not 10 percent. Decisions taken after review are in `docs/print-rules.md` and `docs/print-build-notes.md`.
Sources: 10 PDF files in `source/print/` (11 pages). All were rendered to PNG and looked at. Measurements come from the PDF content (PyMuPDF), the QR code was decoded from a render.
Library state at the start: 204 elements (23 tok, 91 atom, 45 comp, 45 prod), `tokens.json`, `elements.json`.
Rule labels: every rule below is "observed in print". None of them is an official handbook rule.

## 1. Technical findings per file

| # | File | Pages | Trim (mm) | Bleed | Colour | Fonts | Vector or raster | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | `15728501-1.pdf` (title "UitritBord copy") | 1 | 800 x 250 | 10 mm all round, BleedBox set | CMYK, PDF/X-4, output intent FOGRA39 | none, all text outlined | vector, 0 images | Spot colour `ThruCut` (alternate 0/85/0/0) on a 1 pt cut contour 799.6 x 249.6 mm, inset 0.2 mm. Pill has elliptical ends (rx 133.3, ry 125 mm). Enfocus preflight metadata present. |
| 2 | `EvoluonPasjes.pdf` | 2 (front, back) | 85 x 55 | none set (TrimBox = BleedBox = MediaBox), art overshoots 3 to 20 mm | CMYK | Ubuntu, Ubuntu Bold (subset, embedded); wordmark outlined | vector, 0 images | Transparency used for tints: aqua at 10 percent (input fields), aqua at 5 percent (back watermark). |
| 3 | `InfoPylonBordGoed.pdf` | 1 | 600 x 840 | none set, blue overshoots 3 mm | CMYK | Ubuntu BoldItalic, MediumItalic (price only); all other text outlined | vector, 0 images | Blue panel is 714 mm high, the lower 126 mm is white paper. Art box 600 x 821.9. |
| 4 | `LaadKabel.pdf` | 1 | 250 x 300 | 3 mm, BleedBox set | CMYK | Ubuntu, Ubuntu Bold (live) | vector, 0 images | A full-page grey rectangle (25/18/20/2) sits under the blue one, hidden but present. No cut contour. |
| 5 | `StickerDiefstalARtisDruk.pdf` | 2 | 140 x 280 | none set, footer overshoots 4.3 mm at the bottom only | CMYK | Ubuntu, Bold, Medium (live) | vector, 0 images | Page 2 is empty (tiny 1 mm art box in a corner). No cut contour in the file. |
| 6 | `Maashaven.pdf` | 1 | 400 x 1000 | 3 mm, BleedBox set | CMYK | Ubuntu, Medium, Bold (live); ArialMT (the word MOBIAN inside a partner badge) | vector, 0 images, 1 axial shading (header edge) | QR is vector. Rows are aligned with runs of spaces, not tab stops. A white 115 mm square sits unused at y 881 (white on white). |
| 7 | `Tekengebied_1.pdf` | 1 | 297 x 420 (A3) | none | CMYK | Ubuntu Bold (live: P, Parkeren, destination names); GLOW outlined | vector | One off-page copy of the beeldmerk shape at x 256 to 653 (blue on blue, outside the trim). |
| 8 | `Tekengebied_4_kopie_4.pdf` | 1 | 297 x 420 (A3) | none | CMYK | Ubuntu Bold (live); GLOW outlined | vector | Four more off-page copies of the beeldmerk shape. Inactive pills sit in form XObjects at 25 percent opacity. |
| 9 | `Naamloos-7.pdf` | 1 | 148 x 105 (A6 landscape) | none | RGB (ICC, sRGB-like), no CMYK | Ubuntu Regular (tagline, live); logo outlined | vector | The only RGB file. Blue is #1A3680, the old vector blue that 1.3 replaced by #1A3580. |
| 10 | `Inleveren_Abbonementborg_A5.pdf` | 1 | 148 x 105 (A6 landscape, not A5) | none | CMYK | Ubuntu, Medium, Bold (live) | vector, 0 images | Signature box is blue at 5 percent opacity. Date field is 3 outlined segments with chamfered corners. |

None of the ten files contains a raster image. Every page can therefore be extracted as vector.

QR code (only in file 6): `https://parkingyou.nl/nl/locaties/rotterdam/parking-maashaven/id=129`. It is drawn as white modules on a navy plate (inverted). It decodes from the render, but some older scanners fail on inverted codes.

## 2. Applications

Ten files become nine applications: the two GLOW files are two states of one sign (see question 3).
Front and back are variants of one application. IDs follow the new level `app`: `py-app-{type}-{name}[-{variant}]`.

### py-app-card-abonnement-evoluon

| Field | Value |
|---|---|
| ID | `py-app-card-abonnement-evoluon` (variants `-front`, `-back`) |
| Dutch name | Abonnementskaart Evoluon |
| Type | card |
| Size and bleed | 85 x 55 mm, no bleed set; build template with 3 mm bleed |
| Source | `EvoluonPasjes.pdf` p1 (front), p2 (back) |
| Existing IDs used | front: `py-atom-logo-beeldmerk-color` (scaled 1.51x, cropped by the trim at left, top and bottom), `py-atom-logo-wordmark-color`, `py-tok-color-blauw`, `py-tok-color-aqua`, `py-tok-type-ubuntu-regular`, `py-tok-type-ubuntu-bold`. Back: `py-atom-logo-horizontal-reverse` (candidate, aqua dot), `py-tok-color-blauw` |
| New elements | `py-atom-field-input-rounded`, `py-comp-field-block-label-input`, `py-atom-logo-beeldmerk-watermark`, `py-atom-text-tagline`, `py-comp-tagline-lockup` |
| Variables | location name (Evoluon), field labels (Abonnementsnummer, Kenteken), card number and plate (blank fields) |

### py-app-form-bewijs-inlevering

| Field | Value |
|---|---|
| ID | `py-app-form-bewijs-inlevering` |
| Dutch name | Bewijs van inlevering toegangsmiddel |
| Type | form |
| Size and bleed | 148 x 105 mm (A6 landscape), no bleed; the file name says A5 |
| Source | `Inleveren_Abbonementborg_A5.pdf` p1 |
| Existing IDs used | `py-atom-logo-beeldmerk-color` (scaled about 0.35x, no wordmark), `py-tok-color-blauw`, `py-tok-color-aqua`, `py-tok-type-ubuntu-regular`, `py-tok-type-ubuntu-medium`, `py-tok-type-ubuntu-bold` |
| New elements | `py-atom-field-date-segmented`, `py-comp-field-signature-box`, `py-comp-field-line-label` |
| Variables | date (dd, mm, jjjj), customer name, signature, body copy |

### py-app-sticker-waarschuwing-diefstal

| Field | Value |
|---|---|
| ID | `py-app-sticker-waarschuwing-diefstal` |
| Dutch name | Waarschuwingssticker diefstal (NL/EN) |
| Type | sticker (warning) |
| Size and bleed | 140 x 280 mm, no bleed set, no cut contour; page 2 is empty |
| Source | `StickerDiefstalARtisDruk.pdf` p1 (p2 empty) |
| Existing IDs used | `py-tok-color-blauw` (but drifted, see section 4), `py-tok-type-ubuntu-regular`, `py-tok-type-ubuntu-bold` |
| New elements | `py-atom-icon-car-lock`, `py-comp-text-bilingual-nl-en`, `py-atom-line-divider`, `py-comp-bar-footer-callout` |
| Variables | NL heading and body (bold keywords), EN heading and body, phone number (0900-8844), icon |

### py-app-sticker-instructie-laadkabel

| Field | Value |
|---|---|
| ID | `py-app-sticker-instructie-laadkabel` |
| Dutch name | Instructiesticker laadkabel terughangen (NL/EN) |
| Type | sticker (instruction) |
| Size and bleed | 250 x 300 mm trim, 3 mm bleed (256 x 306 media), no cut contour |
| Source | `LaadKabel.pdf` p1 |
| Existing IDs used | `py-atom-logo-horizontal-white` (small, centred at the bottom), `py-tok-color-wit`, `py-tok-type-ubuntu-regular`, `py-tok-type-ubuntu-bold` |
| New elements | `py-atom-icon-plug-ring`, `py-comp-text-bilingual-nl-en`, `py-atom-line-divider` |
| Variables | NL text, EN text, icon |

### py-app-panel-campagne-hofplein

| Field | Value |
|---|---|
| ID | `py-app-panel-campagne-hofplein` |
| Dutch name | Campagnebord Parking Hofplein (voordeligparkeren.nl) |
| Type | panel (campaign sign, not an info pyloon) |
| Size and bleed | 600 x 840 mm, no bleed set (blue overshoots 3 mm); the blue field is 600 x 714 mm and the footer is white paper |
| Source | `InfoPylonBordGoed.pdf` p1 (file name reads "Hofplein bord goed") |
| Existing IDs used | `py-tok-color-blauw`, `py-tok-color-aqua`, `py-tok-color-wit`, `py-tok-type-ubuntu-regular`, `py-tok-type-ubuntu-bold`, `py-tok-type-ubuntu-bold-italic`, `py-tok-type-ubuntu-medium-italic` |
| New elements | `py-comp-price-bubble-corner`, `py-comp-url-chevron`, `py-comp-headline-two-colour`, `py-atom-symbol-p-garage-outline`, `py-comp-lockup-location-garage` |
| Variables | price, unit ("per dag"), footnote mark, headline words and which are aqua, URL, location name |

### py-app-panel-pyloon-maashaven

| Field | Value |
|---|---|
| ID | `py-app-panel-pyloon-maashaven` |
| Dutch name | Informatiepaneel pyloon Maashaven |
| Type | panel (info pyloon print) |
| Size and bleed | 400 x 1000 mm trim, 3 mm bleed (406 x 1006 media) |
| Source | `Maashaven.pdf` p1 |
| Existing IDs used | `py-atom-logo-beeldmerk-color`, `py-comp-pyloon-header-band` (variant needed), `py-comp-pyloon-location-name-slot` (variant needed), `py-comp-pyloon-section-bar-openingstijden`, `-tarieven`, `-betalingsmogelijkheden`, `-calamiteiten`, `-algemene-voorwaarden` (solid in print, gradient in handbook), `py-comp-pyloon-opening-hours`, `py-comp-pyloon-payment-row`, `py-comp-pyloon-emergency`, `py-comp-pyloon-terms`, `py-atom-shape-bracket-arc` (mirrored), `py-tok-gradient-verloop` (header edge), `py-atom-symbol-p-roof` (not used in print, see drift) |
| New elements | `py-comp-section-bar`, `py-comp-pyloon-header-band-plain`, `py-comp-pyloon-opening-hours-multirow`, `py-comp-pyloon-tariff-rows`, `py-comp-pyloon-payment-row-badges`, `py-atom-badge-round-navy`, `py-atom-badge-square-navy`, `py-comp-qr-reserveer`, `py-atom-symbol-p-plain`, third-party references (section 3) |
| Variables | location name, opening hours rows, tariff rows and highlighted row, which payment and partner badges, phone number, QR target, terms URL |

### py-app-event-sign-glow

| Field | Value |
|---|---|
| ID | `py-app-event-sign-glow` (variants `-route`, `-bestemming`) |
| Dutch name | Evenementbord Parkeren GLOW |
| Type | event-sign |
| Size and bleed | A3 297 x 420 mm, no bleed; background is exactly the trim |
| Source | `Tekengebied_1.pdf` p1 (`-route`: three pills with arrows), `Tekengebied_4_kopie_4.pdf` p1 (`-bestemming`: Evoluon active with pin, the others at 25 percent) |
| Existing IDs used | `py-atom-shape-pill-solid`, `py-atom-arrow-left-plain`, `py-atom-arrow-up-plain`, `py-tok-color-wit`, `py-tok-type-ubuntu-bold` |
| New elements | `py-comp-pill-destination` (states active, inactive), `py-comp-pill-list-destinations`, `py-atom-icon-location-pin`, `py-atom-symbol-p-plain`, third-party `py-atom-mark-glow` |
| Variables | event name mark, destination names, arrow direction per row, which row is active |

### py-app-brand-background-tagline

| Field | Value |
|---|---|
| ID | `py-app-brand-background-tagline` |
| Dutch name | Merkachtergrond met tagline |
| Type | brand-background (tagline lockup) |
| Size and bleed | 148 x 105 mm (A6 landscape), no bleed, RGB |
| Source | `Naamloos-7.pdf` p1 |
| Existing IDs used | `py-atom-logo-horizontal-white` (white dot), `py-tok-color-blauw` |
| New elements | `py-atom-text-tagline`, `py-comp-tagline-lockup` |
| Variables | background colour, tagline text |

### py-app-sign-uitrit

| Field | Value |
|---|---|
| ID | `py-app-sign-uitrit` |
| Dutch name | Uitritbord (pilvorm, snijcontour) |
| Type | sign (contour-cut) |
| Size and bleed | 800 x 250 mm trim, 10 mm bleed, ThruCut contour 0.2 mm inside the trim |
| Source | `15728501-1.pdf` p1 |
| Existing IDs used | `py-comp-route-panel-pill` (new size 800 x 250, elliptical ends), `py-comp-route-module-picto` with `py-atom-picto-car`, `py-comp-route-module-separator` with `py-atom-shape-separator-arc`, `py-comp-route-module-text`, `py-comp-route-module-arrow` with `py-atom-arrow-up-circle` |
| New elements | `py-atom-contour-thrucut` (named group, spot `ThruCut`) |
| Variables | destination word (Uit), pictogram, arrow direction, size |

## 3. New atoms and components

Reuse first: an element is only new when no library element has the same shape. Variants of existing elements get a suffix.

| ID | Dutch name | Level | Found in | Why it is new | Third-party |
|---|---|---|---|---|---|
| `py-atom-text-tagline` | Tagline "The other way of parking" | atom | card back, background | Not in the library. Ubuntu Regular, tracking about +60/1000 em, size 0.158 x beeldmerk height | no |
| `py-atom-logo-beeldmerk-watermark` | Beeldmerk watermerk | atom (variant of beeldmerk) | card back | Same shape as `py-atom-logo-beeldmerk-color`, aqua at 5 percent on navy | no |
| `py-atom-field-input-rounded` | Invoerveld afgerond | atom | card front | 44.7 x 8.3 mm, radius 1.29 mm, aqua at 10 percent | no |
| `py-atom-field-date-segmented` | Datumveld in drie delen | atom | form | 3 outlined segments (2, 2, 4 digits), chamfered corners | no |
| `py-comp-field-signature-box` | Handtekeningvak | comp | form | Navy at 5 percent box with label bottom left | no |
| `py-comp-field-line-label` | Veld met lijn en label | comp | form | Label plus rule (print uses typed underscores) | no |
| `py-comp-field-block-label-input` | Abonnementsveld blok | comp | card front | Label above input field | no |
| `py-comp-tagline-lockup` | Taglinelockup | comp | card back, background | Horizontal logo plus tagline, centred | no |
| `py-atom-icon-location-pin` | Locatiepin | atom | GLOW | Map pin outline, not in the library | no |
| `py-atom-icon-plug-ring` | Stekker in open ring | atom | laadkabel | Not the green EV sign | no |
| `py-atom-icon-car-lock` | Auto met slot | atom | diefstal | Car part plus padlock in light aqua | no |
| `py-atom-symbol-p-plain` | P (plat) | atom | pyloon, GLOW | Plain bold P, live text in Ubuntu Bold; the library has only the P with roof | no |
| `py-atom-symbol-p-garage-outline` | P in garage-omtrek | atom | campagnebord | Outline house with P, differs from `py-atom-symbol-p-roof` | no |
| `py-atom-line-divider` | Scheidingslijn | atom | stickers | Hairline, white on navy (0.7 mm, 68 percent of width) or navy on white (0.35 mm, 91 percent) | no |
| `py-comp-text-bilingual-nl-en` | Tweetalig tekstblok NL/EN | comp | stickers | NL first, divider, EN with the same weight pattern | no |
| `py-comp-bar-footer-callout` | Voetbalk melding | comp | diefstal | Navy bar, r 4.2 mm (all four corners in the source; the bottom ones lie below the trim), text with bold phone number | no |
| `py-comp-pill-destination` | Bestemmingspil (actief, inactief) | comp | GLOW | White pill, navy disc with arrow or pin, bold label; inactive = whole group at 25 percent | no |
| `py-comp-pill-list-destinations` | Bestemmingslijst | comp | GLOW | Three pills, pitch 51.7 mm | no |
| `py-comp-price-bubble-corner` | Prijsbel in de hoek | comp | campagnebord | White circle cropped by the corner, rotated price in bold italic | no |
| `py-comp-url-chevron` | URL met chevron | comp | campagnebord | Two-line URL plus light aqua chevron | no |
| `py-comp-headline-two-colour` | Kop in twee kleuren | comp | campagnebord | White regular with aqua bold keywords | no |
| `py-comp-lockup-location-garage` | Garage-lockup | comp | campagnebord | Outline symbol plus two-line bold name | no |
| `py-comp-section-bar` | Sectiebalk (titel variabel) | comp | pyloon | One bar with title variable and fill solid or verloop. The five title-bound bars in the library stay as they are | no |
| `py-comp-pyloon-header-band-plain` | Kopband zonder dak | comp (variant) | pyloon | Header 116 mm instead of 225 mm, plain P, gradient edge | no |
| `py-comp-pyloon-opening-hours-multirow` | Openingstijden meerdere rijen | comp (variant) | pyloon | Three day rows, no subscriber note | no |
| `py-comp-pyloon-tariff-rows` | Tariefrijen | comp | pyloon | Label left, price right, optional blue row | no |
| `py-comp-pyloon-payment-row-badges` | Betaalrij met badges | comp (variant) | pyloon | 4 payment badges, divider, 4 partner badges | no |
| `py-atom-badge-round-navy` | Ronde badge navy | atom | pyloon | 36 mm disc, container only | no |
| `py-atom-badge-square-navy` | Vierkante badge navy | atom | pyloon | 36 mm square, radius 7.94 mm, container only | no |
| `py-comp-qr-reserveer` | Reserveer QR-blok | comp | pyloon | QR plate 118.6 mm (radius 11.95), modules white on navy, with mirrored bracket arc and slogan | no |
| `py-atom-contour-thrucut` | Snijcontour ThruCut | atom | uitrit | Named group on spot colour `ThruCut` | no |
| `py-atom-mark-glow` | GLOW merk | atom | GLOW | Event brand wordmark plus white square | **third-party** |
| `py-atom-payment-visa` | VISA | atom | pyloon | Reference only | **third-party** |
| `py-atom-payment-vpay` | V PAY | atom | pyloon | Reference only | **third-party** |
| `py-atom-payment-maestro-badge`, `py-atom-payment-mastercard-badge` | Maestro, Mastercard (witte badge-versie) | atom | pyloon | Older wordmark versions, differ from the library colour marks | **third-party** |
| `py-atom-partner-parkbee`, `py-atom-partner-myway`, `py-atom-partner-mobian`, `py-atom-partner-e-unknown` | ParkBee, MyWay, Mobian, "e" | atom | pyloon | Partner badges. The "e" mark is not identified. Mobian contains live ArialMT text | **third-party** |

Not new, recorded as placement of an existing element: the cropped beeldmerk on the card front is `py-atom-logo-beeldmerk-color` at 1.51x (54.3 x 65.5 mm), clipped by the trim.

Third-party marks stay reference only: official files must be sourced, none are redrawn.

## 4. Drift and issue report

### 4.1 Colour drift

Native print values are CMYK. The library token `py-tok-color-blauw` is CMYK 100/83/0/17 and sRGB #1A3580. A viewer converts 100/83/0/17 to about #0B3D8A, so the handbook hex and the rendered hex are two renderings of the same brand blue. That is why CMYK is the primary comparison. "Viewer sRGB" is what PyMuPDF shows, "FOGRA39 sRGB" is a conversion with the output-intent profile found in file 1.

| File | Fill | Native | Viewer sRGB | FOGRA39 sRGB | Versus token |
|---|---|---|---|---|---|
| Evoluon, Inleveren, Hofplein | blue | CMYK 100/83/0/17 | #0B3D8A | #293E82 | equal to token CMYK |
| Maashaven (header, bars, logo, text) | blue | CMYK 100/86/21.2/3.7 | #1F4383 | #2F417D | M +3, Y +21.2, K -13.3 |
| Maashaven (payment badges, QR plate) | blue | CMYK 100/83/0/17 | #0B3D8A | #293E82 | equal to token. Two blues on one panel |
| LaadKabel | blue | CMYK 100/85.9/6.6/0 | #1C4695 | #2F428B | M +2.9, Y +6.6, K -17 |
| Sticker diefstal | blue | CMYK 100/86.3/21.5/3.5 | #204382 | #2F417C | M +3.3, Y +21.5, K -13.5 |
| GLOW (both files) | blue | CMYK 100/84.4/5.5/0.4 | #174797 | #2D438D | M +1.4, Y +5.5, K -16.6 |
| Uitrit | blue | CMYK 100/92.5/19.2/5.9 | #27397E | #343A78 | M +9.5, Y +19.2, K -11.1 (darkest, most purple) |
| Naamloos-7 | blue | RGB (ICC) #1A3680 | #1A3680 | not applicable | the old vector blue that 1.3 replaced; RGB only |
| Evoluon, Hofplein | aqua | CMYK 69/0/21/0 | #24BFCD | #3ABACD | equal to token |
| Maashaven | aqua dot | CMYK 69.1/0.8/20.3/0 | #24BDCD | #3BBACE | about equal |
| Uitrit | aqua arrow, arc | CMYK 67.8/3.1/19.2/0 | #31BBCD | #44B8CE | C -1.2, M +3.1, Y -1.8 |
| LaadKabel, diefstal, Hofplein chevron | light aqua | CMYK 54/0/14/0 | #68CBDB | #7CCBDD | no token. About 78 percent of aqua in cyan. Used for icons on navy |
| Maashaven text | black | CMYK 91.2/78.7/62/97.4 (rich black) | #000000 | #1D1D1D | token zwart is CMYK 0/0/0/100. Rich black on small text risks registration problems |
| LaadKabel | grey | CMYK 25.1/18.4/19.5/1.5 | #BDBFBF | #C8C8C8 | hidden leftover under the blue, not PY-Grijs (0/0/0/42) |

Summary: seven different blues across ten files; only four files match the token CMYK. PY-Oranje and PY-Grijs are used nowhere in these prints.

### 4.2 Layout and content drift versus the handbook (pyloon, handbook 3.6)

| Item | Handbook | Print (Maashaven) |
|---|---|---|
| Format | 480 x 1400 (stated) | 400 x 1000 |
| Header | P with roof on a 225 mm band | plain P on a 116 mm band, gradient edge kept |
| Section bars | gradient blue to aqua | solid navy |
| Location name | aqua, next to the logo | navy bold, stacked under the wordmark; wordmark to beeldmerk ratio 2.10 instead of 2.55 |
| Opening hours | one row plus "Alleen toegankelijk voor abonnementhouders" | three rows (ma t/m vr, za, zo), no note |
| Tariffs | per 30 minutes, dagtarief, reservering, vroegboekkorting | per 60 minutes, dagtarief, **verloren kaart (new)**, reservering |
| Payment | contactless, Mastercard, Maestro, pin hand | Maestro, Mastercard, VISA, V PAY, then "e", ParkBee, MyWay, Mobian |
| New block | none | "Reserveer je parkeerplaats voordelig online" with QR |
| RVV icon cluster | five signs | not present |
| Terms URL | www.parkingyou.nl/nl/algemene-voorwaarden | www.parkingyou.nl/algemene-voorwaarden (no `/nl/`) |

Other drift: the card front uses the wordmark without the beeldmerk; the tagline lockup uses an aqua dot on the card back and a white dot on the A6 background (two reverse logos); the pill ends of the Uitrit sign are elliptical, the GLOW pills are full round.

### 4.3 Typos and copy issues

1. Maashaven: "zijn **na de lezen** op" should be "na te lezen op" (the handbook says "na te lezen").
2. Maashaven: "uit de **wegverkeerswet**" should be "wegenverkeerswet" (the handbook has it right).
3. Hofplein: "per dag\*" has an asterisk but no footnote anywhere on the panel.
4. Hofplein: the URL is split inside the domain ("voordelig" / "parkeren.nl").
5. Form: "toegangs-" / "middel" is a manual hyphen at a line end; "Naam klant: ______" is typed underscores instead of a rule; "Datum " has a trailing space.
6. Form: file name says A5, the page is 148 x 105 mm (A6 landscape); file name also has the typos "Abbonemenetborg".
7. Spelling of the brand: "ParkingYou" (form body) versus "parkingyou" (logo, handbook).
8. Maashaven rows are aligned with runs of spaces, which breaks as soon as a text changes. The template needs real columns.
9. Two phone number formats: "085 4011647" (Maashaven) and "0900-8844" (sticker).
10. Default artboard names in file names ("Tekengebied_1", "Tekengebied_4_kopie_4", "Naamloos-7") and a file name "hOFGPLIENbORDGOED".

### 4.4 Production issues

* Bleed: BleedBox is set in only 3 of 10 files (Uitrit, LaadKabel, Maashaven). In the other files the artwork overshoots, but the boxes say trim.
* Cut contour: only Uitrit has one. The two stickers have none.
* Sticker diefstal has an empty page 2.
* The inverted QR code (white on navy) may fail on some readers.
* RGB: Naamloos-7 is RGB only.
* Hidden leftovers: grey rectangle under LaadKabel, white square in Maashaven, off-page beeldmerk shapes in both GLOW files.

### 4.5 Third-party marks used

Maestro, Mastercard, VISA, V PAY (payment), ParkBee, MyWay, Mobian and an unidentified "e" mark (partners), GLOW (event brand), venue and destination names (Evoluon, Philips stadion, TD-gebouw, DLL, Parking Hofplein, Maashaven). The printer name "Artis Druk" appears only in a file name.

## 5. Observed rules (observed in print, not official)

1. **Typeface.** Ubuntu only. Regular, Medium and Bold in use. Italic only for the price numerals on the campaign panel. Light is not used.
2. **Weight pattern.** A key phrase is bold and the supporting words are regular, inside one line ("Kabel terughangen" bold, "na gebruik" regular; "Return cable" bold, "to hook after use." regular). Titles stack a regular and a bold line ("Abonnement" / "Evoluon").
3. **Leading.** Body and headings 1.2 x the font size (stickers, Maashaven). Stacked card titles are tighter: 0.94 (card) and 1.03 (form).
4. **Type scale.** Stickers: heading 60 pt, body 40 pt (1.5 ratio). Maashaven: bars 60 pt, rows 50 pt, terms 35 pt. LaadKabel: both languages at 60.9 pt.
5. **Bilingual pattern.** NL first, divider, EN below. NL and EN use the same size and the same bold pattern. Divider: white 0.7 mm at 68 percent of the width (LaadKabel), navy 0.35 mm at 91 percent (diefstal).
6. **Tagline.** "The other way of parking" in Ubuntu Regular, tracking about +60/1000 em, size 0.158 x the height of the beeldmerk, left edge aligned with the left of the wordmark, white. The lockup is centred on both axes of the format (card back and A6 background, both measured). The wordmark width is 2.55 x the beeldmerk height in every horizontal lockup except the Maashaven location lockup (2.10).
7. **Beeldmerk as image.** Cropped: card front uses the beeldmerk at 1.51x, bleeding off left, top and bottom. Watermark: the same size and shape in aqua at 5 percent on navy, centred on the card back.
8. **Tints are transparency.** Aqua at 10 percent for input fields, aqua at 5 percent for the watermark, navy at 5 percent for the signature box. Not flat spot tints.
9. **Light aqua on navy.** CMYK 54/0/14/0 for icons on navy (plug, padlock, chevron).
10. **Corner radii.** QR plate 11.95 mm on 118.6 (10 percent), partner badge 7.94 on 36 (22 percent), input field 1.29 on 8.3 (15.5 percent), sticker footer 4.23 mm on the top corners only, GLOW pill full round (radius = half the height), Uitrit pill elliptical ends (rx 133.3, ry 125).
11. **Margins.** Maashaven: text starts at 14.8 mm (3.7 percent of the width), bars run edge to edge. GLOW: pills 28.3 mm from both sides (9.5 percent), bottom margin 20.6 mm, pill pitch 51.7 mm for a 43.1 mm pill (gap 8.6 mm). Card front: right margin 3.5 mm, wordmark 8.6 mm from the left.
12. **GLOW pill anatomy.** Disc diameter 87.7 percent of the pill height, ring inset 4.2 mm, label 26.46 mm bold, centred in the space right of the disc. Inactive pill: the whole group at 25 percent opacity.
13. **Date field.** Three segments 9.7 + 9.7 + 19.5 mm wide, 7.1 mm high, 0.26 mm stroke, label "Datum" right-aligned under it.
14. **Header curve.** Pyloon header ends in a convex curve with a thin blue-to-aqua gradient edge.
15. **Headline on the campaign panel.** Cap height 78.1 mm, line pitch 90.4 mm, left margin 8.2 percent of the width, keywords in aqua bold.

## 6. Proposed repo additions (for Phase 2)

* `/svg/atom`, `/svg/comp`: the new atoms and components above. New level `app` is not placed in `/svg`.
* `/applications/{id}/reference.svg`, `template.svg`, `spec.json` for the nine applications (the GLOW variants share one folder with two template files).
* `applications.json` plus additions to `elements.json`.
* `tokens.json`: an `observed` section for the sampled drift colours (the seven blues, light aqua, rich black). Official tokens untouched.
* `docs/print-rules.md` with sections 4 and 5.
* `overview/parkingyou-toepassingen-overzicht.pdf` (A3 landscape, original, template and exploded view per application).
* README update.

## 7. Questions

1. Should the ten source PDFs be committed to `source/print/`? They are in the working tree now. The handbook PDF was kept out of the repo.
2. Which blue is the master for print templates: the token CMYK 100/83/0/17 (four files use it) or one of the other six? I propose the token, and the drifted values go into `observed`.
3. Are the two GLOW files one application with two variants (`-route`, `-bestemming`), or two separate applications?
4. The campaign panel (Hofplein) is a campaign sign, not an info pyloon. OK to type it `panel` with the name `campagne`?
5. The Maashaven pyloon differs on many points from handbook 3.6 (section 4.2). Is the print the new standard (then a new `py-prod` variant is needed) or a one-off?
6. Section bars: add one generic `py-comp-section-bar` (title as variable) and keep the five title-bound bars, or replace them?
7. Which template format do you want for the 4 files with no bleed box: add 3 mm bleed to every template, or keep the original format?
8. Partner badges: is "e" in the payment row a known partner? I cannot identify it from the artwork.
9. The Uitrit sign is on the ThruCut spot. Should every sticker template get the same cut-contour group, even where the source has none (diefstal, laadkabel)?
10. Naamloos-7 is RGB. Build the template in CMYK (token blue) and keep the original as reference, or keep RGB?
11. Typos: keep the original copy in `reference.svg` and use the corrected copy only in the templates?

Waiting for approval.
