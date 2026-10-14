# Stream D: elements to build

Rows copied from docs/phase1-inventory.md (columns: ID, name, description, page, src, method, variables, built_from; product rows: ID, name, page, src, method, specification, variables, built_from).

| py-prod-pyloon-laag-front | 3.6 Informatiepyloon, voorzijde | 23 | V+R | crop + rebuild-grad | panel 1000 x 400 aluminium sandwich, total height 1400, width 480 over posts. Posts RVS koker 40x40x2, ligger 20x20x2, foot plate 100x100x5, plan 540 x 100. M: RVS pyloon powder coated RAL 9006. Double sided | location name, opening hours, tariffs, phone, URL, which signs | pyloon-header-band, section-bar-*, location-name-slot, opening-hours, price-strip, payment-row, emergency, terms |
| py-prod-pyloon-laag-back | achterzijde "Tot ziens" | 23 | V+R | same | 400 x 1000 | goodbye text | pyloon-back-tot-ziens |
| py-prod-pyloon-hoog-vuilnisbak-front | 3.7 Informatiepyloon hoog met vuilnisbak, voorzijde | 24 | V+R | same | total height 2000: panel 1000 plus bin zone 1000. Bin Dulce 50L powder coat RAL 5002, sticker "200x16,6" in text. RAL 9006 for pyloon | as 3.6 | as 3.6 plus sticker-trash |
| py-prod-pyloon-hoog-vuilnisbak-back | achterzijde | 24 | V | crop | 400 x 1000, logo in print foil | none | pyloon-back-logo |
| py-prod-display-volvrij | 3.8 Digitale display | 25 | V | crop | 414 with bracket, body 400 x 200 x 93, holes O10 at 264. States vol, vrij, gesloten via PMS. Standalone or in lichtbak | state | atom-display-volvrij-vrij |
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
| py-comp-rvv-cluster-pyloon | RVV icon cluster pyloon | five signs in a row (5, 2,1m, truck, bicycle, camera) | 23, 24 | V | crop | speed, height | rvv-a01, rvv-max-height, rvv-c07, rvv-no-bicycles, sign-camera |
| py-comp-pyloon-back-tot-ziens | achterzijde "Tot ziens" | header band, "Tot ziens", logo at bottom | 23 | V+R | rebuild-grad | goodbye text, optional image | header-band, logo-stacked-color |
| py-comp-pyloon-back-logo | achterzijde alleen logo | white panel with logo | 24 | V | crop | none | logo-stacked-color |
| py-atom-rvv-no-bicycles | fietsen verboden (not in 9.2) | bicycles prohibited, pylon row | 23, 24 | V | crop | none | none |
| py-atom-sign-camera | cameratoezicht (not in 9.2, not RVV) | black ring with camera, pylon row | 23, 24 | V | crop | none | none |
| py-atom-payment-contactless | contactloos betalen | contactless symbol with hand and card | 23, 24 | V | crop | none | none |
| py-atom-payment-mastercard | Mastercard | brand logo | 23, 24 | V | ref | none | none |
| py-atom-payment-maestro | Maestro | brand logo | 23, 24 | V | ref | none | none |
| py-atom-payment-pin-hand | (unnamed) hand met pas | hand inserting a card | 23, 24 | V | crop | none | none |
| py-atom-display-volvrij-vrij | VOL/VRIJ display | dark panel, LED dot matrix "VRIJ". Drawn in green only; 240 dots per instance | 12, 15, 25 | V | crop | state (VOL, VRIJ, gesloten) | none |
