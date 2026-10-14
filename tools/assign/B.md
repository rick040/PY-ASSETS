# Stream B: elements to build

Rows copied from docs/phase1-inventory.md (columns: ID, name, description, page, src, method, variables, built_from; product rows: ID, name, page, src, method, specification, variables, built_from).

| py-prod-lichtbak-aanrijroute-display | 2.1 Uitsteeklichtbak in aanrijroute, met display | 12 | V+R | crop + rebuild-grad | 1000 x 1250 face, 200 deep. Display 200x400 (zicht 170x370). Spacer aluminium koker 40x150. Pole aluminium koker 100x200. Min 2500 above ground. M: aluminium profile powder coat, blockout foil so only white signing and beeldmerk light. Mt: pole. L: internal LED. RAL 5002, 9006 | arrow direction, display state | face-aanrijroute, display-volvrij |
| py-prod-lichtbak-aanrijroute-nodisplay | same without display | 12 | V+R | same | 1000 x 1000 | arrow direction | face-aanrijroute |
| py-prod-lichtbak-entree | 3.1 Uitsteeklichtbak bij entree | 14 | V+R | same | 1000 x 1000, 100 deep. Spacer koker 40x70. Min 2500 above ground. M: opal image plate with blockout foil, profile RAL 5002. Mt: wall, perpendicular. L: internal LED. RAL 5002, 9006 | location name, arrow direction | face-entree |
| py-prod-lichtbak-voetganger-liggend | 5.1 Voetgangersentree lichtbak (liggend) | 37 | V+R | crop + rebuild-grad | 2500 x 300 x 100. Aluminium profile RAL 5002, clear plate with blockout foil, LED. Tech info in 3.3.3 | location name | face-voetganger-liggend |
| py-prod-lichtbak-voetganger-staand | 5.2 Voetgangersentree lichtbak (staand) | 38 | V+R | crop + rebuild-grad | 800 x 1000, 100 deep, spacer koker 40x70, mounted above the pedestrian entrance, RAL 5002, 9006 | location name | face-voetganger-staand |
| py-comp-face-aanrijroute | lichtbakfront aanrijroute | gradient face, P-roof, arrow, beeldmerk, display zone | 12 | V+R | rebuild-grad | arrow direction, display fitted | symbol-p-roof, arrow-right-plain, logo-beeldmerk-reverse, display-volvrij-vrij |
| py-comp-face-entree | lichtbakfront entree | logo, P-roof, arrow, location name | 14 | V+R | rebuild-grad | location name, arrow direction | logo-horizontal-reverse, symbol-p-roof, arrow-downleft-plain |
| py-comp-face-voetganger-staand | lichtbakfront voetgangersentree | logo, P-roof, pedestrian figure, location name | 38 | V+R | rebuild-grad | location name | logo-horizontal-reverse, symbol-p-roof, picto-pedestrian |
| py-comp-face-voetganger-liggend | lichtbakfront liggend | P block, beeldmerk, name, white tab with pedestrian | 37 | V+R | rebuild-grad | location name | portal-p-block, logo-beeldmerk-reverse, picto-pedestrian |
| py-comp-location-name-slot | locatienaam slot | generic name field, Ubuntu Bold, white or aqua | 14, 37, 38, 40 | V | crop | location name | none |
| py-atom-symbol-p-roof | P met dak | white P with chevron roof, on every lichtbak, pylon and portal. Not captioned in 1.x | 12, 14, 15, 23, 37, 38 | V | crop | colour | none |
| py-atom-arrow-downleft-plain | pijl linksonder | white arrow on lichtbak entree | 14 | V | crop | colour | none |
| py-atom-arrow-right-plain | pijl rechts | solid arrow. Lichtbak arrow (p12) has a thinner shaft than the route arrow (p28); to be verified | 12, 28 | V | crop | colour | none |
