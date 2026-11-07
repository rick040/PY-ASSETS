# Logo

## Wat het logo is

Ons logo bestaat uit twee delen. Het beeldmerk: een bubbel met een ring en een aqua stip. En het woordmerk: "parking" in Ubuntu Regular en "you" in Ubuntu Bold, als tekening, niet als tekst.

Het logo blijft zoals het is. Mensen kennen het van de lichtbak bij de ingang, de pas en de site. Die herkenning bouw je niet opnieuw op. Wat verandert: de reverse versie wordt officieel en er komt een navy versie voor aqua en oranje.

We meten alles in **x**: de breedte van het beeldmerk in de lockup die je gebruikt.

## Lockups

![Lockups](figures/lockups.png)

- **Liggend** is de standaard. Gebruik deze als je niet zeker weet welke.
- **Staand** voor smalle, hoge vlakken: een pyloon, een story, een sticker.
- **Beeldmerk los** als het logo klein moet of als het merk al duidelijk is: app-icoon, avatar, favicon.
- **Woordmerk los** alleen als het beeldmerk al op hetzelfde vlak staat.

Je combineert de delen nooit zelf. Gebruik de bestanden `logo-horizontal-*`, `logo-stacked-*`, `logo-beeldmerk-*` en `logo-wordmark-*`.

## Vijf versies, elk op zijn eigen ondergrond

![Versies op ondergronden](figures/versions-grounds.png)

| Versie | Ondergrond | Bestand |
|---|---|---|
| Kleur (navy, aqua stip) | wit, blue.50, lichte foto met rustig vlak | `logo-*-color.svg` |
| Reverse (witte bubbel, navy ring, aqua stip) | PY-Blauw, PY-Diep, donkere foto | `logo-*-reverse.svg` |
| Wit, één kleur | alleen eenkleurige productie op donker: folie, gravure, laser | `logo-*-white.svg` |
| Navy, één kleur (nieuw) | PY-Aqua, PY-Oranje, eenkleurige navy druk | `logo-*-navy.svg` |
| Zwart, één kleur | alleen eenkleurige zwarte druk | `logo-*-black.svg` |

Op beeld werkt het zo. Zoek een rustig vlak: lucht, een egale muur, schaduw. Licht vlak: kleurversie. Donker vlak: reverse. Is de foto overal druk, zet het logo dan op een navy vlak naast of onder de foto, niet op een donkere laag over de foto. Op het verloop staat alleen de reverse versie, en alleen op het navy deel.

## Vrije ruimte

![Vrije ruimte](figures/clear-space.png)

Rond elke lockup blijft 0,5x vrij, aan alle kanten, ook onder de punt van het beeldmerk. In dat vlak staat niets: geen tekst, geen rand, geen bubbel, geen rand van het formaat. Staat het logo in een hoek van een poster of pas, dan is de marge 2u of 0,5x, wat het grootst is.

## Minimale maten

![Minimale maten](figures/minimum-sizes.png)

| Lockup | Scherm | Druk |
|---|---|---|
| Liggend (hoogte beeldmerk) | 24 px | 7 mm |
| Staand (hele hoogte) | 48 px | 14 mm |
| Beeldmerk los | 16 px | 5 mm |

Op borden geldt één regel: het beeldmerk is minstens 2 keer zo hoog als de kapitaalhoogte van de grootste tekst op dat bordvlak. Een bord met "P1" in 50 mm kapitaalhoogte vraagt dus een beeldmerk van minstens 100 mm hoog.

## Locatielockups

![Opbouw locatielockup](figures/location-construction.png)

Bij een garage of locatie zetten we de naam naast het logo. Het logo zelf blijft het originele bestand; alleen de naam is tekst.

**A, naam onder het woordmerk (standaard).**
- Liggend logo, ongewijzigd.
- Naam in Ubuntu Sans Bold, lettergrootte 0,4x, spatiëring 0,01 em. De kapitaalhoogte is dan 0,28x.
- Naam links gelijk met de stok van de p van "parking".
- Basislijn van de naam op de punt van het beeldmerk.
- Vrije ruimte 0,5x om het geheel.

**B, naam op één regel.** Voor brede, lage vlakken: portalen, gevelbanden, de kop van een webpagina. Zelfde lettergrootte 0,4x, op de basislijn van het woordmerk, 0,5x na "you".

De naam heeft altijd de kleur van het woordmerk: navy op licht en op aqua of oranje, wit bij de reverse versie. Nooit aqua of oranje tekst. Schrijf alleen de plaatsnaam: "Philips Stadion", niet "Parking Philips Stadion". Past een naam op een bord niet, gebruik dan Ubuntu Sans Condensed Bold. Geen tweede regel en geen kleinere letter. De staande lockup krijgt geen naam.

Maat kiezen: begin bij de naam. x = 2,5 keer de lettergrootte van de naam.
- Scherm: naam 16 px geeft x = 40 px, het beeldmerk wordt 48 px hoog.
- Druk: naam in print-h2 (22 pt) geeft x = 55 pt, ongeveer 19 mm.
- Borden: de naam volgt de leesafstand uit de typografie. Op 5 meter is de letter 72 mm, dus x = 180 mm. Het beeldmerk is dan ruim 4 keer de kapitaalhoogte van de naam; de bordregel klopt vanzelf.

![Locatielockups in gebruik](figures/location-examples.png)

De huidige Maashaven-lockup heeft een kleiner woordmerk dan het echte logo. Bij de volgende druk vervangen we die door deze opbouw.

## Tagline "The other way of parking"

**Advies: stoppen met de tagline als lockup.** Vier redenen:
1. Hij is Engels. Al onze teksten zijn Nederlands, met je en jij.
2. De kleurversie zet aqua tekst op wit: 2,34:1. Dat haalt WCAG niet.
3. Hij staat op 0,158 keer de hoogte van het beeldmerk. Bij een logo van 24 px is dat minder dan 4 px: onleesbaar.
4. Hij belooft iets zonder het te laten zien. "**Parkeren** zonder gedoe." zegt meer, als kop in de layout.

Bestaand drukwerk mag op, nieuw werk krijgt hem niet meer. Wil Rick hem houden, dan als losse regel tekst in de layout, niet vast aan het logo.

## App-icoon en favicon

![App-icoon en favicon](figures/app-icon.png)

- Reverse beeldmerk op PY-Blauw.
- Het vlak is vierkant: 0,5x boven en 0,5x onder het beeldmerk, horizontaal gecentreerd. Het beeldmerk is dan 45 procent van de breedte en valt binnen de veilige zone van Android.
- iOS: lever 1024 x 1024 px aan, vierkant, zonder afronding. iOS rondt zelf af.
- Android: adaptief icoon met PY-Blauw als achterlaag en het beeldmerk als voorlaag.
- Favicon: SVG plus 32 px. Het beeldmerk is daarin 17,5 px hoog.

## Zo niet

![Zo niet](figures/misuse.png)

## Do's en don'ts

- Doe: gebruik altijd het originele bestand uit `kit/assets/` of `svg/atom/`.
- Doe: kies de versie bij de ondergrond, volgens de tabel.
- Doe: houd 0,5x vrij rondom en blijf boven de minimale maat.
- Doe: zet een locatienaam volgens opbouw A of B, in Ubuntu Sans Bold.
- Niet: uitrekken, indrukken of draaien.
- Niet: andere kleuren, omlijning, schaduw, gloed of verloop in het logo.
- Niet: het woordmerk opnieuw typen, ook niet in Ubuntu.
- Niet: beeldmerk en woordmerk los van elkaar schalen of verschuiven.
- Niet: het logo in een bubbel zetten, of het beeldmerk als bubbel gebruiken voor een prijs, niveau of foto.
- Niet: het kleurlogo op PY-Blauw, of wit op aqua of oranje.
- Niet: het logo op een druk deel van een foto.
- Niet: de tagline aan het logo vastzetten.

## Voorgestelde waarden

Niet gebruiken in definitief werk tot de creative director akkoord geeft. De figuren laten het voorstel zien.

| Waarde | Voorstel | Reden |
|---|---|---|
| Lettergrootte naam in locatielockup | 0,4x (kapitaalhoogte 0,28x) | Eerst 0,5x getest: de naam raakt dan bijna de staarten van p en g, en wordt groter dan het woordmerk. Met 0,4x blijft er lucht, past "Philips Stadion" binnen de breedte van het logo en blijft het beeldmerk ruim 4 keer de kapitaalhoogte van de naam. |
| Favicon 16 px | Geen eigen 16 px-tekening; de browser verkleint de SVG of 32 px-versie. Uitzondering op het minimum van 16 px voor het losse beeldmerk. | In een tabblad van 16 px is het beeldmerk met vrije ruimte maar 8,7 px hoog. Zonder vrije ruimte wordt het een andere tekening. Dit is de enige plek waar het minimum niet haalbaar is. |
