# Iconografie

We hebben twee sets met één tekenlogica. **Pictogrammen** zijn gevulde vormen voor borden en grote UI. **UI-iconen** zijn lijniconen voor schermen. Allebei zijn ze simpel, rond van karakter en volgen ze de kleur van de tekst ernaast.

## Pictogrammen

- **Raster** 48 eenheden in het vierkant.
- **Veilige zone** 4 eenheden rondom. Het tekenvlak is dus 40 x 40.
- **Vorm**: gevuld en vlak. Geen lijnen, geen verloop, geen schaduw.
- **Kleur**: de tekstkleur van de grond. Wit op navy, PY-Blauw op aqua, PY-Diep op oranje. In een bubbel de inhoudskleur van die bubbel.
- **In een bubbel**: het pictogram past in het inhoudsvierkant van 60 procent van de bubbelbreedte.

Voor de constructie gebruiken we hulplijnen, zodat pictogrammen even zwaar ogen: een cirkel van 40, een vierkant van 36, staand 32 x 40 en liggend 40 x 32. Een auto vult het liggende vlak, een voetganger het staande.

![Raster en constructie van pictogram en UI-icoon](figures/raster.png)

## Hertekening: vier voorbeelden

De twaalf handboekpictogrammen zijn op verschillende formaten getekend, met wisselende lijndiktes en soms een eigen rand. We hertekenen ze op het 48-raster. Als voorstel staan er vier klaar: auto, voetganger, lift en betalen. De originelen in `kit/assets/` blijven ongewijzigd; de voorstellen staan in `06-iconografie/voorstel/`.

- **Auto.** Vooraanzicht blijft. Ruit, lampen en grille als uitsparing.
- **Voetganger.** Het hoofd blijft de bubbel, uniform geschaald. Dat is een mooi stukje merk dat al in het origineel zat.
- **Lift.** Kader 3 eenheden dik, pijlen erboven, figuren met lucht eromheen.
- **Betalen.** De ring om het euroteken vervalt. In een bubbel of op een bordvlak is de ring dubbel: de bubbel of het bord is al de rand.

De voetganger en de lift zijn nu nog opgebouwd uit ronde lijnen; voor productie zetten we ze om naar gesloten contouren.

![Vier hertekeningen naast het origineel](figures/hertekening.png)

### Plan voor de andere acht

| Pictogram | Actie |
|---|---|
| Trap | Op raster zetten, treden 4 eenheden. |
| Roltrap | Vereenvoudigen: figuren weg of groter, nu te fijn op 24 px. |
| Mindervaliden | Hertekenen; de witte scheidingslijn wordt een echte uitsparing. |
| Elektrisch laden | Ring weg, auto plus stekker. |
| Gezin | Hertekenen met dezelfde lijfmaten als de voetganger. |
| Info | Wordt een losse "i". Het huidige pictogram is zelf een bubbel; in een bubbel wordt dat een bubbel in een bubbel. Op borden kan ook het woord "Info". |
| Motor | Op raster, wielen als uitsparing. |
| Toilet | Ring weg. |

Volgorde: eerst de pictogrammen die op lichtbakken en betaalautomaten staan (voetganger, lift, trap, betalen, auto, info), daarna de rest.

## Pictogrammen in de bubbel en op taakgronden

Op een lichtbak of portaal blijft het vlak navy en draagt de bubbel de taak. Op een geprint bord mag de taakkleur de hele grond zijn. Het voorbeeld hieronder gebruikt nog de handboekbestanden, ingekleurd. Je ziet daar ook waarom de ring van betalen en de bubbelvorm van info weg moeten.

![Pictogrammen in bubbels en op taakgronden](figures/toepassing.png)

## UI-iconen

- **Raster** 24 px, **veilige zone** 2 px, tekenvlak 20 x 20.
- **Lijn** 2 px, ronde uiteinden, ronde hoeken. Geen vulling.
- **Maten** 16, 20, 24 en 32 px. 24 is de standaard.
- **Kleur** volgt de tekst: wit op navy, PY-Diep op de oranje knop, `text.muted` voor een chevron.
- Een icoon staat nooit alleen voor een actie zonder label, behalve in vaste patronen (sluiten, terug, zoeken) met een toegankelijke naam.

### Aanbevolen set: Tabler Icons

We raden **Tabler Icons** aan (tabler.io/icons, versie 3.50, MIT-licentie, meer dan 5.000 outline-iconen). Waarom:

- Zelfde tekenlogica als onze regel: raster 24, lijn 2, ronde uiteinden en hoeken.
- Tabler houdt 2 px vrij van de rand. Dat is precies onze veilige zone.
- Er zitten iconen in die wij echt nodig hebben: car, parking, elevator, stairs, walk, wheelchair, charging-pile, ticket, credit-card.
- MIT is gratis voor commercieel gebruik. Voorwaarde: de licentietekst meeleveren in de app en de website (bijvoorbeeld op de pagina met open-sourcelicenties).

Het alternatief is **Lucide** (ISC-licentie, sommige iconen MIT via Feather). Ook raster 24, lijn 2 en rond. Lucide tekent tot 1 px van de rand en is daardoor op hetzelfde formaat iets groter. Kies je toch Lucide, dan zet je het tekenvlak op 20 px.

Regels voor de set: gebruik alleen de outline-variant, niet de filled-variant. Gebruik nooit de merkiconen uit de set (de `brand-`-iconen); dat zijn merken van anderen. Ontbreekt een icoon, teken het dan zelf op het 24-raster met dezelfde lijn.

![UI-iconen: set, maten en gebruik](figures/ui-iconen.png)

## Merken van anderen

RVV-verkeerstekens, veiligheidsborden (ISO 7010, NEN 3011), betaalmerken en partnerlogo's gebruiken we zoals de eigenaar ze aanlevert. Nooit hertekend in onze stijl, nooit ingekleurd, nooit in een bubbel. Ze krijgen hun eigen vlak met vrije ruimte, en onze iconen staan er niet tegenaan.

Let op: de witte partner- en betaalmerken in `svg/atom/` zijn uit drukwerk gehaald. Voor nieuw werk vraag je het officiële bestand op bij de eigenaar.

![Merken van anderen: wel en niet](figures/derde-partijen.png)

## Do's en don'ts

- **Do:** pictogrammen gevuld, op het 48-raster, binnen het tekenvlak van 40.
- **Do:** UI-iconen uit Tabler, outline, lijn 2 px.
- **Do:** icoonkleur = tekstkleur van de grond.
- **Do:** merken van anderen uit het originele bestand, in hun eigen kleuren.
- **Don't:** lijniconen op borden, of gevulde pictogrammen in de UI-navigatie.
- **Don't:** twee sets door elkaar (Tabler en Lucide, of handboek en hertekend) op één vlak.
- **Don't:** een pictogram met een eigen rand of bubbelvorm in een bubbel zetten.
- **Don't:** RVV-tekens, betaalmerken of partnerlogo's natekenen, inkleuren of in een bubbel zetten.
- **Don't:** de stokfiguren als pictogram gebruiken.

## Voorgestelde waarden

Goedgekeurd door de creative director: zie besluiten D18 en D20 in de core spec. Waar de core spec iets anders zegt, geldt de core spec.

Niet gebruiken in finals tot de creative director ze goedkeurt.

| Waarde | Voorstel | Reden |
|---|---|---|
| Hulplijnen pictogram | cirkel 40, vierkant 36, staand 32 x 40, liggend 40 x 32 | Gelijk visueel gewicht tussen ronde, vierkante en langwerpige pictogrammen. |
| Kleinste detail pictogram | uitsparingen en tussenruimtes minstens 2 eenheden | Op 24 px is dat 1 px; kleiner dichtgelopen op borden en schermen. |
| Lijfmaten mensfiguren | armen 4,5, benen 5, romp 6,5 eenheden | Eén maat voor voetganger, gezin en mindervaliden. |
| Kaderdikte pictogram | 3 eenheden (lift, kaders) | Blijft zichtbaar op 24 px. |
| Lijndikte UI-icoon | 2 px op elke maat, ook bij 16 en 32 | Core-spec zegt "2 px lijn"; vaste lijn houdt iconen even zwaar als de tekst ernaast. In Tabler en Lucide is dat een instelling. |
| UI-iconenset | Tabler Icons 3.50, MIT | Zie boven. |
