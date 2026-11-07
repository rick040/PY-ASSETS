# Kleur

Kleur betekent bij ParkingYou iets. Navy is rijden en het merk, aqua is lopen, oranje is betalen en let op. Zo herken je ons van ver, en zo weet je in de garage waar je heen moet. Dit hoofdstuk legt vast welke kleuren er zijn, wat ze doen, welke combinaties mogen en hoe je ze maakt in druk, folie en lak.

## Onze kleuren

De waarden van PY-Blauw, PY-Aqua en PY-Oranje veranderen niet. Nieuw is de naam PY-Diep voor de donkerste navy. De oude websitekleuren (#192AA2, #0AD3E6, #FF8400), de Canva-kleuren (#344F9E, #76C8DB) en de middenstop #097BAE vervallen.

![Merkkleuren en hun taak](figures/palette-roles.png)

| Naam | HEX | RGB | CMYK | Token | Rol |
|---|---|---|---|---|---|
| PY-Blauw | #1A3580 | 26 53 128 | 100 83 0 17 | `color.blue.700` | rijden, merk, hoofdvlak |
| PY-Aqua | #32B9CD | 50 185 205 | 69 0 21 0 | `color.aqua.500` | lopen; buiten de garage het accent |
| PY-Oranje | #F08300 | 240 131 0 | 0 57 100 0 | `color.orange.500` | betalen, prijs, let op, hoofdknop |
| PY-Diep | #0D142E | 13 20 46 | zie Voorgestelde waarden | `color.blue.900` | tekst op oranje, donkerste vlak |
| PY-Grijs | #AEAEAE | 174 174 174 | 0 0 0 42 | `color.neutral.400` | hardware, lijnen; geen tekstkleur |
| PY-Zwart | #1D1D1B | 29 29 27 | 0 0 0 100 | `color.neutral.900` | lopende tekst |
| Wit | #FFFFFF | 255 255 255 | 0 0 0 0 | `color.neutral.0` | ruimte, tekst op blauw |

## Kleur draagt een taak

In de garage, op terminals en in de app heeft elke kleur één taak. We gebruiken kleur niet als versiering.

| Taak | Ondergrond | Inhoud | Waar |
|---|---|---|---|
| Rijden | PY-Blauw | wit | portalen, in- en uitrit, lichtbakken, routeborden voor auto's, niveaus |
| Lopen | PY-Aqua | PY-Blauw | voetgangersroutes, lift, trap, uitgang naar de straat |
| Betalen en let op | PY-Oranje | PY-Diep | betaalautomaten, tariefborden, storingen, de hoofdknop op het scherm |

- Lichtbakken en portalen blijven navy. Op een verlicht vlak zit de taakkleur in de bubbel, nooit in een volledig aqua of oranje vlak.
- Geprinte borden (Dibond, wandfolie) mogen de taakkleur als hele ondergrond hebben.
- Hoogtebalken houden rood en wit. Vluchtwegborden (ISO 7010, NEN 3011) en verkeersborden (RVV) krijgen nooit merkkleur, en merkkleur staat er ook niet als versiering naast.

![Taakkleuren op borden, en dezelfde borden met alleen lichtheid](figures/task-signs.png)

## Kleur in marketing

Op posters, social en de website is de verhouding ongeveer: PY-Blauw 60, wit 30, aqua 6 en oranje 4 procent. Aqua is daar het accent: een bubbel of een klein detail. Oranje staat er alleen bij een prijs, een deal of de actie. Binnen de garage betekent aqua altijd lopen.

![Verhouding van de kleuren in marketing](figures/proportions.png)

## Het verloop

Het verloop (`gradient.verloop`) heeft twee stops: PY-Blauw van 0 tot 45 procent, PY-Aqua op 100 procent, onder 135 graden. Het is alleen voor marketing: schermheaders, geprinte posters en panelen. Tekst staat alleen op het navy deel. Geen verloop in bewegwijzering, snijfolie, poedercoat of lichtbakfolie; daar wordt het vlak PY-Blauw. Het oude verloop met de middenstop #097BAE vervalt.

![Verloop: zo wel en zo niet](figures/verloop.png)

## Status en meldingen

Status heeft altijd een woord naast de kleur: Vrij, Vol, Gesloten. Kleur alleen draagt nooit betekenis, ook niet voor kleurenblinden of onder slecht licht.

| Token | Licht | Donker | Contrast op wit |
|---|---|---|---|
| `status.free` (Vrij) | aqua.700 #127C8C | aqua.300 | 4,90:1 |
| `status.full` (Vol) | orange.700 #B35A00 | orange.300 | 4,80:1 |
| `status.closed` (Gesloten) | neutral.600 #5E6470 | neutral.300 | 5,94:1 |
| `feedback.error` op `error-bg` | red.600 op red.100 | red.100 op red.700 | 5,01:1 |

## De volledige schalen

Blauw, aqua, oranje en neutraal lopen van 50 tot 900, rood heeft 100, 600 en 700. Schermen gebruiken de hele schaal via de semantische tokens; componenten lezen nooit direct een schaalwaarde.

![Volledige schalen](figures/scales.png)

## Welke combinaties mogen

Tekst heeft 4,5:1 nodig. Grote tekst (24 px, of 19 px vet; in druk 18 pt, of 14 pt vet) en UI-grafiek hebben 3:1 nodig. Alle verhoudingen zijn opnieuw berekend met de WCAG 2.x-formule (relatieve luminantie, sRGB) en vergeleken met `tokens/contrast.md`: 29 paren in licht en donker, grootste afwijking 0,005. Alles komt overeen.

| Paar | Verhouding | Gebruik |
|---|---|---|
| wit op PY-Blauw | 11,26:1 | alle tekst op navy, ook op borden |
| PY-Blauw op PY-Aqua | 4,80:1 | loopborden, aqua bubbel |
| PY-Diep op PY-Oranje | 6,87:1 | betaalborden, hoofdknop |
| PY-Blauw op wit | 11,26:1 | koppen en tekst in druk en op scherm |
| aqua.700 op wit | 4,90:1 | aqua als tekstkleur |
| orange.700 op wit | 4,80:1 | oranje als tekstkleur |

Op borden gebruiken we alleen de eerste drie paren, altijd mat.

![Contrastmatrix](figures/contrast-matrix.png)

## Niet toegestaan

- Wit op aqua (2,34:1) en wit op oranje (2,64:1).
- Aqua of oranje als tekstkleur op wit (2,34 en 2,64:1). Gebruik aqua.700 of orange.700.
- PY-Blauw op oranje onder grote tekst (4,26:1).
- PY-Blauw op PY-Diep (1,61:1), bijvoorbeeld in donkere modus.
- PY-Grijs als tekst op wit (2,22:1).
- Kleur zonder woord, en een volledig aqua of oranje lichtbakvlak.

![Niet toegestaan](figures/not-allowed.png)

## Kleur onder garagelicht

Uit het onderzoek naar de garage (R4): NEN 2443 vraagt gemiddeld 75 lux, oudere garages zijn op 40 lux of minder gebouwd. Op een navy bord is dat zo weinig licht dat het oog kleuren slecht scheidt. Natriumlicht maakt het erger: navy en aqua worden allebei donker, oranje bijna wit. Alleen het verschil in lichtheid tussen tekst en vlak blijft over. Daarom:

- Op borden alleen de drie paren hierboven; elk heeft een groot lichtheidsverschil.
- Een woord of pictogram draagt de betekenis, de kleur helpt alleen.
- Elke bordface krijgt mat laminaat, tegen spiegelingen van lampen.
- Geprinte lichtbakfolie wordt vaak dubbel geprint en oogt overdag donkerder.
- Voor de kleuren definitief zijn, testen we één set proefborden in een echte garage, onder het eigen licht (LED, TL en waar het nog hangt natrium).

## Donkere modus

In donkere modus is PY-Diep de ondergrond en is tekst wit (18,16:1). Navy werkt daar niet als tekst of rand (1,61:1); merktekst en links worden aqua.300 (11,01:1). De oranje hoofdknop blijft oranje met PY-Diep. De tweede knop wordt aqua met PY-Diep. Alle waarden staan in `tokens.json` onder `modes.dark`; de schermen zelf komen uit het hoofdstuk digitaal.

## Productie

Druk in CMYK (FOGRA39 gestreken of FOGRA52 ongestreken) met 3 mm afloop. Drukwerk gebruikt alleen de merkkleuren en hun lichte tinten; zo voorkomen we de 15 blauwen en 5 aqua's die nu in omloop zijn. Borden gaan via de RIP van de leverancier met de RAL- en foliereferenties hieronder. Alles in de tabel met een stippellijn is een voorstel.

![Productietabel per kleur](figures/production-table.png)

## Do's en don'ts

| Doen | Niet doen |
|---|---|
| Kleur kiezen op taak: rijden navy, lopen aqua, betalen oranje | Aqua of oranje gebruiken omdat het vrolijk staat |
| Op aqua altijd PY-Blauw, op oranje altijd PY-Diep | Wit op aqua of oranje |
| Status met een woord | Alleen een gekleurde stip |
| Verloop alleen in marketing, tekst op het navy deel | Verloop op borden, in folie, in de bubbel |
| PY-Blauw als vaste drukkleur 100 83 0 17 | Een blauw uit een oud bestand pipetten |
| Mat laminaat en een proefbord in de garage | Kleur goedkeuren op een scherm |

## Voorgestelde waarden

Goedgekeurd: zie besluiten D23 tot en met D25 in de core spec. Waar de core spec iets anders zegt, geldt de core spec.

**Methode.** ΔE is CIEDE2000, zelf berekend. Voor RAL en folie: merkkleur van sRGB naar CIELab D65 en vergeleken met de gepubliceerde Lab- of sRGB-waarde. Voor Pantone: merkkleur naar CIELab D50 (Bradford) en vergeleken met de Lab-waarden uit de PANTONE+ Solid Coated en Uncoated V3 kleurboeken (X-Rite 2014). Waar de nieuwere Pantone-waarden ook te vinden waren (colorxs.com) staat de tweede ΔE erbij. Een ΔE uit schermdata vervangt nooit een fysiek staal: elke keuze wordt gecontroleerd met de Pantone-waaiers, de RAL K7 en de folie-stalen.

**CMYK.** Omgerekend met het ICC-profiel Coated FOGRA39 (ISO 12647-2:2004), uit de output intent van `source/print/15728501-1.pdf`, via LittleCMS (Pillow ImageCms), relatief colorimetrisch met zwartpuntcompensatie. De ΔE is de terugrekening via hetzelfde profiel.

| Kleur | Voorstel CMYK | ΔE | Toelichting |
|---|---|---|---|
| PY-Diep | 100 83 0 80 | 4,8 | PY-Blauw plus 80 K, totaal 263 procent inkt. Valt buiten FOGRA39; het beste haalbare is 4,5. Directe ICC-omrekening geeft 100 93 47 66 (ΔE 7,7). |
| PY-Diep, tekst kleiner dan 12 pt op oranje | K 100 | n.v.t. | Drie platen op kleine tekst geven pasproblemen. PY-Zwart op oranje haalt 6,39:1. |
| blue.50 / 100 / 200 / 300 | 5 3 2 0 / 10 6 2 0 / 24 15 2 0 / 44 30 2 0 | 1,0 / 1,0 / 0,5 / 1,0 | ICC-omrekening |
| aqua.50 / 100 / 200 / 300 | 8 0 3 0 / 16 0 5 0 / 30 0 9 0 / 50 0 15 0 | 0,4 / 1,2 / 2,0 / 2,1 | raster van PY-Aqua (12, 23, 44, 72 procent); aqua.300 vervangt de vijf losse lichte aqua's in oud drukwerk |
| orange.50 / 100 / 200 | 0 5 11 0 / 0 13 25 0 / 0 25 49 0 | 0,0 / 0,7 / 0,8 | ICC-omrekening |

Ter controle: de handboekwaarden rekenen goed terug. PY-Blauw 100 83 0 17 geeft ΔE 2,9, PY-Aqua 69 0 21 0 geeft 0,5, PY-Oranje 0 57 100 0 geeft 1,3. Die blijven staan. Voorstel: drukwerk gebruikt alleen tinten 50 tot 300. FOGRA52 (ongestreken) is nog niet omgerekend, omdat het profiel niet te downloaden was; de drukker rekent dat om vanuit de sRGB- of Lab-waarden.

**Pantone.**

| Kleur | Coated | Uncoated |
|---|---|---|
| PY-Blauw | 3597 C (ΔE 2,1; nieuwere data 5,4). Alternatief 287 C (5,8; 4,8) | 280 U (6,7); ongestreken haalt dit blauw niet |
| PY-Aqua | 3115 C (3,6; nieuwere data 2,1). Alternatief 2227 C (2,4; 4,2) | 3115 U (2,4) |
| PY-Oranje | 144 C (2,8; 4,4). Alternatief 716 C (2,9; 3,9) | 144 U (5,6) |
| PY-Diep | 5255 C (4,3; 6,9) | geen bruikbare match (282 U 16,6) |
| PY-Grijs | Cool Gray 5 C (2,1) | Cool Gray 5 U (2,4) |
| PY-Zwart | 419 C (3,1); in de praktijk K 100 | K 100 |

**RAL.**

| Kleur | Nu | Voorstel |
|---|---|---|
| PY-Aqua | RAL 6027 Lichtgrün, ΔE 10,2, te groen | RAL Design 220 70 35 Ferienblau, ΔE 1,7. Geen RAL Classic komt binnen ΔE 9. Voor borden met aqua liever geprinte folie met mat laminaat op Dibond; poedercoat in aqua alleen waar het echt moet, in RAL Design. |
| PY-Oranje | RAL 2003, ΔE 7,5 | RAL 2003 houden, maar RAL 1037 Sonnengelb (ΔE 5,4) meenemen in de proefborden |
| PY-Diep | geen | RAL 5004 Schwarzblau, ΔE 9,1; alleen als het echt gelakt moet worden |
| Wit | geen | RAL 9016 Verkehrsweiß, ΔE 4,5, hoogste lichtreflectie (LRV 87) van de witten |
| PY-Blauw | RAL 5002, ΔE 4,5 | houden; nog steeds de beste RAL Classic |

**Folie.** Oracal 751C is glanzend, behalve wit en zwart, die ook mat bestaan (010M, 070M). Voor matte borden is printen met mat laminaat de standaard; snijfolie alleen voor één kleur op een vlak.

| Kleur | Opaak | Translucent (lichtbak) |
|---|---|---|
| PY-Blauw | Oracal 751C-049 King blue (ΔE 1,9) | Oracal 8500-006 Intensive blue (2,9) of 3M 3630-157 Sultan Blue |
| PY-Aqua | geen standaardkleur (beste: 751C-599 Pastel turquoise, 8,6). Printen, of maatkleur aanvragen | geen standaardkleur in 8500 of 3630. Printen op translucente printfolie (3M IJ3630-20), of maatkleur (3M levert 3630 op kleur) |
| PY-Oranje | 751C heeft niets binnen ΔE 9. 3M Scotchcal 100-717 Light Orange (ongeveer 3, hexwaarde niet officieel) | 3M 3630-74 Kumquat Orange (simuleert Pantone 151 C, ΔE 4,2) |
| PY-Diep | Oracal 751C-590 Blueberry (2,3) | geen; geen lichtbakkleur |
| PY-Grijs | Oracal 751C-724 Ice grey (3,2) | Oracal 8500-076 Telegrey (5,5) |
| PY-Zwart | Oracal 751C-070M Black mat (4,6) | Oracal 8500-070 Black (3,7) |
| Wit | Oracal 751C-010M White mat (3,1) | Oracal 8500-010 White (5,2) |

Translucente folie oogt doorgelicht anders dan op het staal. Kies lichtbakkleur altijd op een proefvlak in de lichtbak, bij dag en bij nacht.

**Bronnen.**
- Pantone Lab: PANTONE+ Solid Coated en Uncoated V3, via [jacobbubu/color-books](https://github.com/jacobbubu/color-books); controle via [colorxs.com](https://www.colorxs.com/color/pantone-3115-c) en [Pantone color finder 3597 C](https://www.pantone.com/color-finder/3597-c).
- RAL Classic Lab: [List of RAL colours, Wikipedia](https://en.wikipedia.org/wiki/List_of_RAL_colours). RAL Design: [RAL 220 70 35](https://ralcolorchart.com/ral-design/ral-220-70-35).
- Oracal sRGB-waarden: [Orafol 751C](https://www.orafol.com/en/europe/products/oracal-751c-high-performance-cast), [Orafol 8500](https://orafol.com/en/europe/products/oracal-8500-translucent-cal).
- 3M: [productbulletin 3630/3730](https://www.wensco.com/customer/docs/skudocs/3M_3630_3730_productbulletin.pdf) (namen en Pantone-simulaties), [productkaart 3630](https://www.sirvisual.com/Attachment/100/Product%20Card%203630.pdf) (maatkleuren, IJ3630-20), [kleurkaart 100](https://multimedia.3m.com/mws/media/653312O/color-card-100.pdf). De hexwaarde van 100-717 komt uit [Colorly](https://github.com/jpederson/Colorly) (MIT) en is niet officieel.
- Garagelicht: `01-research/R4-physical-environment.md`. Drukdrift: `docs/print-rules.md` 1 en 7.1.
