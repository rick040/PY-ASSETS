# Werkpunten uit de hoofdstukken

Voorstellen en open vragen die de bouwers in hun hoofdstuk zetten. Ze staan niet in de gids. Wat is goedgekeurd, staat als besluit in de core spec.

## Logo: Voorgestelde waarden


Goedgekeurd: zie besluiten D1 en D2 in de core spec. Waar de core spec iets anders zegt, geldt de core spec.

| Waarde | Voorstel | Reden |
|---|---|---|
| Lettergrootte naam in locatielockup | 0,4x (kapitaalhoogte 0,28x) | 0,5x getest: de naam raakt bijna de staarten van p en g en overheerst het woordmerk. Met 0,4x blijft er lucht en past "Philips Stadion" binnen de breedte van het logo. |
| Favicon 16 px | Geen eigen 16 px-versie; de browser verkleint SVG of 32 px. Uitzondering op het minimum van 16 px. | Op 16 px is het beeldmerk met vrije ruimte 8,7 px hoog. De enige plek waar het minimum niet haalbaar is. |

## Typografie: Voorgestelde waarden


Goedgekeurd en verwerkt: besluiten D25 en D39 in de core spec.

| Onderwerp | Voorstel | Waarom |
|---|---|---|
| Meten van de stem | Hoogte tekstblok = aantal regels x regelhoogte. Afstand 0,3x gemeten van de open kant van de boog (de punten) tot de eerste letter. | De core spec zegt "hoogte = tekstblok" en "afstand 0,3x", maar niet vanaf waar. Zo is het op elke maat meetbaar. De referentiefiguur bij de eigen elementen staat iets krapper (ongeveer 0,2x); die zou mee moeten. |
| De stem als scheiding op borden | Afstand 0,3x de hoogte aan beide kanten van de boog; hoogte gelijk aan de pijl of het pictogram ernaast (vervangen door D42 en D47). | De core spec geeft de lijn voor borden, maar geen afstand en hoogte. |
| Paginakop per scherm | Desktop display-xl, tablet display-l, telefoon heading-xl. Boven de paginakop `space.9` (96 px) op desktop, `space.7` (48 px) op telefoon. | Maakt "grotere, rustigere koppen" toetsbaar, met bestaande tokens. |
| Regelafstand van u-koppen | Korps x 50/48, zoals print-display. | De core spec geeft voor posters en social alleen de kapitaalhoogte; de hoogte van de stem hangt van de regelafstand af. |
| Gewicht van het sleutelwoord | ExtraBold 800 in display-koppen, Bold 700 in heading-koppen; de rest altijd Regular 400. | Volgt de schaal; voorkomt een kop die helemaal vet is. |

## Iconografie: Voorgestelde waarden


Goedgekeurd: zie besluit D37 in de core spec.

| Waarde | Voorstel | Reden |
|---|---|---|
| Pijl op borden | hoogte 2 x de kaphoogte van de naam (2k); tekenvlak van een pictogram op hetzelfde bord ook 2k | De core spec geeft de pijl alleen een maat in knoppen. 2k is dezelfde regel als het beeldmerk op borden, past binnen de marge van 2u op een routebord (kaphoogte 70 mm, pijl 140 mm, bord 200 mm) en houdt pijl en pictogram even zwaar. |
| Afstand pijl en label | 8 px (`space.2`) in een knop, 4 px (`space.1`) in een link | Bestaande tokens; zonder vaste afstand plakt de pijl in een link aan het woord of zweeft hij in een knop. |
| Schuine pijl | `arrow-downleft`, gedraaid per 90 graden, geschaald tot dezelfde pijllengte als de rechte pijl (tekenvlak 0,875 h) | Het handboekbestand is op 199 mm getekend tegen 250 mm voor de rechte pijl, waardoor hij op hetzelfde tekenvlak 9 procent kleiner oogt. Zo is elke richting even zwaar. |
| Pijl naar buiten | schuin rechtsomhoog (45 graden) na de linktekst | Geeft "opent een andere site of app" zonder extra icoon, binnen de stappen van 45 graden. |

## Beweging: Voorgestelde waarden


Goedgekeurd: zie besluit D38 in de core spec.

| Waarde | Voorstel | Reden |
|---|---|---|
| Pijl schuift in knop en link | 4 px (`space.1`), `duration.moderate`, `easing.standard`, heen en terug | De core spec noemt de beweging en de duur, niet de afstand. 4 px is een bestaand token en blijft binnen de 8 px tussen label en pijl. |
| Pijl schuift in beeld | 0,5u achter de eindplek, `duration.moderate`, `easing.enter`, dekking 0 naar 1 in `duration.fast` | 0,5u is de kleinste stap van het verticale ritme; zichtbaar in een reel (27 px) zonder dat de pijl door het beeld vliegt. |
| Tekst na de stem | dekking 0 naar 1 in `duration.fast`, `easing.enter`, direct na de 320 ms van de boog; samen 440 ms | De stem opent de boodschap; de tekst moet dus na de boog komen, met een bestaand token. |
| Houding parkeerder | elke houding minstens 1 s in beeld; hooguit één knip per scène | Korter leest als een haperende animatie; meer knippen maakt van de parkeerder een tekenfilm. |
| Opening reel | de bubbelpop (0,6 s) of de stem met de kop (0,44 s); beide binnen de eerste 0,6 s | Uitbreiding van de bestaande regel "bubbelpop in de eerste 0,6 s", zodat een reel met stem en parkeerder geen derde element nodig heeft. |
| Reduced motion voor stem en pijl | stem en tekst samen in een fade van `duration.reduced`; de pijl schuift niet | Zelfde aanpak als de bubbel: het moment blijft, de beweging gaat weg. |

## UI/UX: Open punten


- Adres van Parking Philips Stadion, live beschikbaarheid, servicekosten, andere tarieven dan € 12,50 en het algemene telefoonnummer zijn nog onbekend en staan als placeholder.
- `status.full` is oranje.700, dezelfde waarde als `feedback.warning`. Als oranje op het scherm helemaal weg moet, kan Vol `text.default` met het streep-icoon worden (16,88:1).
- Welke schermen van Aeroparker kunnen we stylen, en ondersteunt de PWA een ticket zonder bereik?
- De bubbel van 40 heeft geen vast scherm meer, nu het ticket geen bubbel heeft. Houden voor het niveau van je plek, als de PWA dat later toont?

## Stationery: Open vragen


- KvK-nummer, btw-nummer, IBAN en een algemeen telefoonnummer zijn nog niet bekend. Nu staan ze als [nummer] en [telefoonnummer].
- De bedrijfsnaam staat als "ParkingYou BV" op het oude briefpapier en als "ParkingYou B.V." elders. Wij gebruiken ParkingYou B.V.; graag bevestigen.
- CMYK van PY-Blauw voor ongestreken papier (FOGRA52): de drukker converteert; tot die tijd 100 83 0 17 en beoordelen op een proef.
- Willen we de gastheer standaard in de voet van het briefpapier, of alleen op brieven aan klanten?
- Gaat de brief ooit in een vensterenvelop? Dan maken we een tweede envelop, het adresveld staat al goed.

## Toepassingen: Open vragen


- Er zijn twee storingsnummers in omloop. Welk nummer is juist? Tot die tijd staat in elke figuur [storingsnummer].
- Is er een algemeen telefoonnummer voor de bus, naast het storingsnummer?
- Heeft de abonnementspas een scancode, en zo ja welk type?
- Welke Vol/Vrij-display komt in het portaal, en in welke ledkleur?
- Welk busmodel rijdt er? Daarna maken we de wrap op ware maat; de figuur gaat uit van circa 5000 x 2300 mm.
- Fluor oranje of fluor geel voor de jassen? Geel botst niet met PY-Oranje als het naast elkaar komt.
- GLOW-logo en campagnekleur moeten van de organisatie komen.
- Bij welke garages komt een welkomstwand, en is een voetgangersingang met de loper overal toegestaan, of eist de gemeente of de eigenaar ergens een pictogram?
