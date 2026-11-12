### 14.4 Bronnen bij Kleur

Hier staat hoe de productiewaarden in hoofdstuk 3, Kleur, zijn gekozen en waar de gegevens vandaan komen. Een kleurverschil uit schermdata vervangt nooit een fysiek staal: elke keuze wordt gecontroleerd met de Pantone-waaiers, de RAL K7-waaier en de foliestalen.

**Kleurverschil.** Het kleurverschil ΔE is berekend met de formule CIEDE2000.

- RAL en folie: de merkkleur is van sRGB omgerekend naar CIELab (D65) en vergeleken met de gepubliceerde Lab- of sRGB-waarde van de referentie.
- Pantone: de merkkleur is omgerekend naar CIELab D50 (chromatische aanpassing volgens Bradford) en vergeleken met de Lab-waarden uit de kleurboeken PANTONE+ Solid Coated en Solid Uncoated V3 (X-Rite, 2014). Waar ook nieuwere Pantone-waarden te vinden waren (colorxs.com), is een tweede ΔE berekend. De tabel hieronder geeft beide.

**CMYK.** Omgerekend met het ICC-profiel Coated FOGRA39 (ISO 12647-2:2004), uit de output intent van `source/print/15728501-1.pdf`, via LittleCMS (Pillow ImageCms), relatief colorimetrisch met zwartpuntcompensatie. De ΔE is de terugrekening via hetzelfde profiel.

- PY-Diep 100 83 0 80 is PY-Blauw plus 80 K, samen 263 procent inkt. De kleur valt buiten FOGRA39; het best haalbare verschil is 4,5. Een directe ICC-omrekening geeft 100 93 47 66 (ΔE 7,7).
- De handboekwaarden van PY-Blauw (ΔE 2,9), PY-Aqua (0,5) en PY-Oranje (1,3) rekenen goed terug en blijven staan.
- Het profiel voor ongestreken papier (FOGRA52) was niet te downloaden. De drukker rekent dat om vanuit de sRGB- of Lab-waarden.

**Pantone, beide datasets.** Eerste waarde: PANTONE+ V3 (2014). Tweede waarde: nieuwere gegevens via colorxs.com, waar beschikbaar.

| Kleur | Coated | Uncoated |
|---|---|---|
| PY-Blauw | 3597 C (2,1; 5,4). Alternatief 287 C (5,8; 4,8) | 280 U (6,7) |
| PY-Aqua | 3115 C (3,6; 2,1). Alternatief 2227 C (2,4; 4,2) | 3115 U (2,4) |
| PY-Oranje | 144 C (2,8; 4,4). Alternatief 716 C (2,9; 3,9) | 144 U (5,6) |
| PY-Diep | 5255 C (4,3; 6,9) | geen bruikbare match (beste: 282 U, 16,6) |
| PY-Grijs | Cool Gray 5 C (2,1) | Cool Gray 5 U (2,4) |
| PY-Zwart | 419 C (3,1) | K 100 |

**Folie.** De hexwaarde van 3M Scotchcal 100-717 Light Orange is niet officieel; hij komt uit de open kleurenlijst Colorly. De ΔE van ongeveer 3 is dus een schatting. Vraag een staal aan.

**Contrast.** Alle contrastverhoudingen in hoofdstuk 3 zijn berekend met de WCAG 2.x-formule (relatieve luminantie, sRGB) en vergeleken met `brand-2027/tokens/contrast.md`: 33 paren in licht en donker, grootste afwijking 0,005.

**Bronnen.**

- Pantone Lab: PANTONE+ Solid Coated en Uncoated V3, via [jacobbubu/color-books](https://github.com/jacobbubu/color-books); controle via [colorxs.com](https://www.colorxs.com/color/pantone-3115-c) en de [Pantone color finder 3597 C](https://www.pantone.com/color-finder/3597-c).
- RAL Classic Lab: [List of RAL colours, Wikipedia](https://en.wikipedia.org/wiki/List_of_RAL_colours). RAL Design: [RAL 220 70 35](https://ralcolorchart.com/ral-design/ral-220-70-35).
- Oracal sRGB-waarden: [Orafol 751C](https://www.orafol.com/en/europe/products/oracal-751c-high-performance-cast), [Orafol 8500](https://orafol.com/en/europe/products/oracal-8500-translucent-cal).
- 3M: [productbulletin 3630/3730](https://www.wensco.com/customer/docs/skudocs/3M_3630_3730_productbulletin.pdf) (namen en Pantone-simulaties), [productkaart 3630](https://www.sirvisual.com/Attachment/100/Product%20Card%203630.pdf) (maatkleuren, IJ3630-20), [kleurkaart 100](https://multimedia.3m.com/mws/media/653312O/color-card-100.pdf). Hexwaarde van 100-717: [Colorly](https://github.com/jpederson/Colorly) (MIT-licentie), niet officieel.
- Garagelicht (NEN 2443, natriumlicht): `brand-2027/01-research/R4-physical-environment.md`. Drukdrift: `docs/print-rules.md`, punt 1 en 7.1.
