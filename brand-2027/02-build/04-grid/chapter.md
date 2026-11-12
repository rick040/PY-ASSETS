# Grid en layout

Eén maat voor alles: van visitekaartje tot lichtbak, van post tot reel. Die maat heet u. Op schermen werken we met een vast 4 px-raster. Dit hoofdstuk legt beide uit en geeft vijf standaardpatronen waar je bijna elke uiting mee bouwt.

De toon is rustig: veel wit, grote letters, één accent per vlak. Per vlak staat het logo plus hooguit twee van onze vier elementen (parkeerder, stem, bubbel, pijl). De grond is altijd vlak: PY-Blauw of wit, en `blue.50` voor rustige delen. Hoe die elementen zelf werken, staat in Patronen en designelementen.

## De formaateenheid u

u is de korte zijde van het formaat gedeeld door 20. Meer hoef je niet te onthouden. Een post van 1080 x 1350 px heeft een korte zijde van 1080, dus u = 54 px. Een A4 heeft een korte zijde van 210 mm, dus u = 10,5 mm.

Alles op het vlak meet je in u:

- **Marge** 2u aan alle kanten. Afloop (3 mm bij print) komt er buiten bij.
- **Goot** 1u tussen de kolommen.
- **Kolommen**: 6 op staande en vierkante formaten, 12 op liggende formaten.
- **Ritme**: elementen staan op veelvouden van 0,5u. Bovenkant van een kop, onderkant van een logo, een lijn onder een parkeerder: allemaal op dat ritme.
- **Kop op posters en social**: kapitaalhoogte 1u tot 2u. Regelafstand 50/48 van de lettergrootte. Het vette kernwoord in ExtraBold 800, de rest Regular.
- **Lopende tekst**: kapitaalhoogte 0,3u tot 0,5u.
- **Elementen**: bubbel 3u, 5u, 8u of 13u breed; parkeerder 3u tot 8u hoog, op een lijn van 0,1u; de stem zo hoog als het tekstblok dat hij opent.

Kolombreedte reken je zo uit: breedte min 4u, min (kolommen min 1) keer u, gedeeld door het aantal kolommen.

![De formaateenheid u en de tabel met de formaten](figures/formaat-eenheid.png)

## Vijf echte formaten

| Formaat | u | Marge | Kolommen | Kolom |
|---|---|---|---|---|
| Visitekaartje 85 x 55 mm | 2,75 mm | 5,5 mm | 12 | 3,65 mm |
| A4 poster | 10,5 mm | 21 mm | 6 | 19,25 mm |
| Lichtbak 1000 x 1000 mm | 50 mm | 100 mm | 6 | 91,7 mm |
| Post 1080 x 1350 px | 54 px | 108 px | 6 | 99 px |
| Reel 1080 x 1920 px | 54 px | 108 px | 6 | 99 px |

A2 volgt dezelfde regel: u = 21 mm.

**Visitekaartje.** Liggend, dus 12 kolommen. Het logo staat linksboven op de marge, 3u hoog; de beeldmerkhoogte is dan 8,25 mm en ligt boven het minimum van 7 mm. Op zo'n klein formaat zou de u-regel voor tekst te kleine letters geven, dus de tekst volgt de printschaal: print-h3 voor de naam, print-small voor de gegevens. Op de voorkant staat de gastheer, 5u hoog, op de basislijn van de laatste regel; zijn hand wijst naar je telefoonnummer. De achterkant is vlak PY-Blauw. De stem opent de kop "**Parkeren** zonder gedoe." linksboven op de marge, in print-h3. Rechtsonder zwaait de gastheer, 8u hoog, op een witte lijn van 0,1u op de ondermarge; de lijn loopt over de drie kolommen die hij raakt. Het logo staat linksonder op dezelfde marge. Logo plus twee elementen: stem en parkeerder. De hoeken volgen ID-1: 3,18 mm.

**A4 poster.** Wit. De stem opent de kop vanaf 4u, kapitaalhoogte 1,25u. Tekst 0,4u, 1u onder de kop. Een navy bubbel van 8u met de prijs staat rechtsonder op de kolommen, het logo linksonder op de marge. Twee elementen: stem en bubbel. Geen oranje: buiten de garage is een prijs navy.

**Lichtbak.** Het vlak blijft navy; de taakkleur zit in de bubbel. Tekst op borden rekent met de leesafstand uit de typografie (10 mm kapitaalhoogte per meter), niet met de u-regel. In het voorbeeld 75 mm voor 7,5 m, Nederlands en Engels even groot, met 0,5u tussen de regels. De hoekige pijl is 2 x de kapitaalhoogte (150 mm). Het beeldmerk staat rechtsboven, 3u hoog: minstens 2 keer de grootste kapitaalhoogte. Twee elementen: bubbel en pijl.

![Visitekaartje voor en achter, A4 poster en lichtbak op hun grid](figures/voorbeelden-print.png)

**Post en reel.** Zelfde u (54 px), zelfde 6 kolommen. In een reel liggen boven 250 px en onder 340 px knoppen en tekst van het platform. Daar komt niets belangrijks. Op het u-raster: de kern ligt tussen 5u (270 px) en 29u (1566 px). Ondertitels staan op 26,5u tot 29u, wit op PY-Blauw. Het logo staat op de eindkaart van 1,5 s.

In het voorbeeld is de post het patroon foto + navy veld met de stem voor de kop, en de reel het patroon parkeerder op de lijn: de loper loopt over een vloerlijn. Een volgende scène mag een andere pose hebben, met een harde knip.

![Post en reel met vrije zones](figures/voorbeelden-social.png)

## Schermen

Op schermen rekenen we niet in u maar in pixels, met een basis van 4 px. Ruimte komt uit de tokens `space.0` tot `space.10`: 0, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 px.

| Scherm | Breedte | Kolommen | Goot | Marge |
|---|---|---|---|---|
| Telefoon | tot 767 px | 4 | 16 px | 16 px |
| Tablet | 768 tot 1199 px | 8 | 24 px | 32 px |
| Desktop | 1200 px en breder | 12 | 24 px | minstens 32 px; inhoud max. 1200 px, gecentreerd |

Raakvlakken zijn minstens 44 x 44 px. Kaarten hebben `radius.l` (16), invoervelden `radius.m` (8), knoppen en chips `radius.pill`. Een parkeerder op scherm is 48 tot 160 px hoog en staat op een lijn van 2 px in `figure.body`, die aan beide kanten 16 px (`space.4`) uitsteekt.

![Telefoon, tablet en desktop met hun kolommen](figures/schermgrids.png)

## Vijf standaardpatronen

Bijna elke uiting past in een van deze vijf. Begin daar, en wijk alleen af met een reden. De maten gelden voor een post van 1080 x 1350 px; op andere formaten reken je dezelfde u om.

1. **Stem + kop.** Wit. De stem opent de kop vanaf 4u, kapitaalhoogte 1,5u; de kop mag breken na het vette kernwoord. Tekst 1u eronder, logo onderaan op de marge. Voor merk en campagne.
2. **Parkeerder op de rand.** Navy. De stem opent de kop vanaf 4u, kapitaalhoogte 1,5u; tekst 1u eronder. Rechtsonder staat een witte parkeerder van 8u op een lijn van 0,1u op de ondermarge, dezelfde lijn waar het logo links op staat. De lijn loopt over de kolommen die de parkeerder raakt. Laat hem naar de kop kijken. Voor "jouw plek", reserveren en abonnementen.
3. **Foto + navy veld.** Eigen foto 10u hoog bovenin, navy veld eronder. De stem en de kop staan op navy. Nooit tekst op de foto en geen donkere laag over een foto.
4. **Parkeerder op de lijn.** Licht vlak (`blue.50`) of wit. Kop bovenin, een lijn van 0,1u op 21u, een parkeerder van 8u op die lijn. Kies de parkeerder bij de boodschap: zwaaier of gastheer bij welkom, juicher bij een deal, loper bij een route.
5. **Info.** Wit. Een navy bubbel van 5u met één woord (Info). Kop, dan tijden en prijzen in tabelcijfers op regels van 1,5u. Prijzen zijn navy, nooit oranje.

De maten in de patronen (kop op 4u, lijn op 21u of op de ondermarge) zijn een startpunt, geen vaste regel. Vast is: marge, kolommen, het 0,5u-ritme, de maten van de elementen, hooguit twee elementen per vlak en de kleurverdeling. Over een reeks uitingen is dat ongeveer 47 procent wit en licht (`blue.50`), 38 procent PY-Blauw en 13 procent aqua. Oranje komt in deze patronen niet voor; dat hoort alleen bij betalen in de garage. De grond is vlak: geen patroon, geen verloop, geen grote achtergrondbubbel.

![Vijf standaardpatronen op een post](figures/layoutpatronen.png)

## Do's en don'ts

- **Do:** reken eerst u uit en zet marge, goot en kolommen neer voordat je iets plaatst.
- **Do:** zet alles op 0,5u. Twijfel je, schuif naar het dichtstbijzijnde halve u.
- **Do:** kies een van de vijf patronen en hooguit twee elementen.
- **Do:** laat wit staan. Grote kop, korte tekst, één accent.
- **Do:** houd in reels de bovenste 250 en onderste 340 px vrij van belangrijke inhoud.
- **Do:** gebruik op borden de leesafstand voor de letterhoogte, niet de u-regel.
- **Don't:** marges kleiner dan 2u, ook niet "omdat het net niet past". Maak de tekst korter.
- **Don't:** tekst op een foto of een donkere laag over een foto. Gebruik een navy veld.
- **Don't:** oranje voor prijzen of knoppen buiten de garage, en nergens een verloop.
- **Don't:** een patroon of decoratieve vorm als achtergrond, of een parkeerder die zweeft.
- **Don't:** losse pixelwaarden op schermen. Alleen `space`-tokens.
