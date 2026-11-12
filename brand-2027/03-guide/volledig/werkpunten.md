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
| De stem als scheiding op borden | Afstand 0,3x de hoogte aan beide kanten van de boog; hoogte gelijk aan het tekstblok naast de boog. | De core spec geeft de lijn voor borden, maar geen afstand en hoogte. |
| Paginakop per scherm | Desktop display-xl, tablet display-l, telefoon heading-xl. Boven de paginakop `space.9` (96 px) op desktop, `space.7` (48 px) op telefoon. | Maakt "grotere, rustigere koppen" toetsbaar, met bestaande tokens. |
| Regelafstand van u-koppen | Korps x 50/48, zoals print-display. | De core spec geeft voor posters en social alleen de kapitaalhoogte; de hoogte van de stem hangt van de regelafstand af. |
| Gewicht van het sleutelwoord | ExtraBold 800 in display-koppen, Bold 700 in heading-koppen; de rest altijd Regular 400. | Volgt de schaal; voorkomt een kop die helemaal vet is. |

## Patronen en designelementen: Voorgestelde waarden


Nieuw voorstel:

| Waarde | Voorstel | Reden |
|---|---|---|
| Lengte van de korte lijn in print en op u-formaten | over de volle kolommen die de parkeerder raakt | Besluit D45 geeft de schermlengte (16 px aan beide kanten). Voor u-formaten ontbreekt een lengte; op de kolommen ligt de lijn op het grid en blijft hij kort. |

Al goedgekeurd (besluit D43 in de core spec):

| Waarde | Voorstel | Reden |
|---|---|---|
| Gastheer en wijzer: afstand | 0,5u tussen hand en tekst of pijl; hand op de hoogte van de eerste regel | Dichterbij lijkt het of hij de tekst vastpakt; verder weg valt het verband weg. |
| Gespiegelde parkeerder | alleen het lijf spiegelen, het hoofd niet; als kitbestanden `figure-*-navy-flip.svg` en `figure-*-white-flip.svg` | De core spec staat spiegelen toe, maar het hoofd heeft de vorm van de bubbel en die spiegelt nooit. In de figuren is het hoofd terug op zijn plek gezet. |

## Patronen en designelementen: Open vragen


- De korte lijn in print en op u-formaten (zie Voorgestelde waarden): akkoord met "over de kolommen die hij raakt"? In de figuren voor pas, visitekaartje en post is het zo getekend.
- Prijzen in de figuren zijn € 12,50 (Parking Philips Stadion, dagtarief met reservering) of [prijs], geen verzonnen tarieven.

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

## Fotografie en beeld: Voorgestelde waarden


Goedgekeurd: zie besluiten D26 en D27 in de core spec. Waar de core spec iets anders zegt, geldt de core spec.


| Waarde | Voorstel | Reden |
|---|---|---|
| Brandpunt plekken | 24 tot 35 mm (kleinbeeld) | breed genoeg voor een ingang, zonder vervorming |
| Brandpunt mensen en details | 50 mm | natuurlijk perspectief, geen vertekening van gezichten |
| Diafragma | plekken f/8, mensen f/2.8 tot f/4 | plekken scherp; mensen los van de achtergrond |
| Camerahoogte rijbaan | 1,2 m | ooghoogte van een bestuurder |
| Witbalans | daglicht 5200 tot 5600 K, in nabewerking hooguit 200 K koeler | neutraal en iets koel, zonder blauwe zweem |
| Beeldverhoudingen | 3:2, 16:9 en 1:1 naast 4:5 en 9:16 | dekt website, drukwerk en social |
| Rustig vlak bij tekst op foto | minstens een derde van het beeld | ruimte voor kop en logo binnen 2u |
| Export | JPEG sRGB, lange zijde 3000 px voor scherm; print minimaal 300 ppi op eindformaat | één master voor web en social, scherp genoeg voor drukwerk |
| Fotobubbel op desktop | 240 px breed in een header | 104 px is op desktop te klein om een detail te herkennen |
| Alt-tekst | richtlijn onder 125 tekens | kort genoeg voor schermlezers |

## UI/UX: Open punten


- Adres van Parking Philips Stadion, live beschikbaarheid, servicekosten en het algemene telefoonnummer zijn nog onbekend en staan als [placeholder].
- `status.full` is oranje.700, dezelfde waarde als `feedback.warning`. Wij houden het als tekst en icoon, zoals een waarschuwing. Als oranje op het scherm helemaal weg moet, kan Vol `text.default` met het streep-icoon worden (16,88:1); dat is een keuze voor de core spec.
- Welke schermen van Aeroparker kunnen we stylen, en ondersteunt de PWA een ticket zonder bereik?
- Het ticket heeft geen bubbel meer: de kop draagt de stem en de springer, "geldig" staat als woord. Daarmee heeft de bubbel van 40 geen vast scherm. Voorstel: houden voor het niveau van je plek, als de PWA dat later toont. Graag een besluit.
- Opgelost: de pop-in van de bubbel hoort nu bij het openen van de app. Dat klopt met het hoofdstuk Beweging, waar het opstartscherm een merkmoment is.
- De terugpijl op hoofdletterhoogte van de titel is 11 px. Dat volgt de regel, maar is klein naast iconen van 24. Testen met gebruikers; zie Voorgestelde waarden.

## UI/UX: Voorgestelde waarden


Goedgekeurd: zie besluiten D4 tot en met D14, D35 en D44 in de core spec. De tabel blijft als uitleg.

| Waarde | Voorstel | Reden |
|---|---|---|
| Lijn onder een parkeerder op scherm | 2 px (`size.border-width-strong`) in `figure.body`; een korte lijn loopt aan beide kanten `space.4` (16 px) voorbij de figuur | "Een lijn van 0,1u" geeft op scherm 4,8 px; dat wordt een balk. 2 px past bij de randen van de UI en volgt de kleur van het lijf, licht en donker. De lengte volgt uit een bestaand spacing-token, dus geen nieuwe waarde. |
| `action.secondary-border` | Nieuw semantisch token, gelijk aan `action.secondary-fg` (licht blue.700, donker aqua.300) | De tweede knop is nu een omlijning. Een eigen naam voorkomt dat code de tekstkleur als rand leest en houdt de rand los aanpasbaar. |
| Terugpijl in een icoonknop | 16 px (icoonmaat uit de core spec) in plaats van 11 px | Een pijl zonder label heeft geen hoofdletter naast zich. 16 px weegt even zwaar als de iconen van 24 met hun veilige zone. |

## Stationery: Open vragen


- KvK-nummer, btw-nummer, IBAN en een algemeen telefoonnummer staan niet in de repository. Nu staan ze als [placeholder].
- De bedrijfsnaam staat als "ParkingYou BV" op het oude briefpapier en als "ParkingYou B.V." elders. Wij gebruiken ParkingYou B.V.; graag bevestigen.
- CMYK van PY-Blauw voor ongestreken papier (FOGRA52): de drukker converteert; tot die tijd 100 83 0 17 en beoordelen op een proef.
- Willen we de gastheer standaard in de voet van het briefpapier, of alleen op brieven aan klanten?
- Gaat de brief ooit in een vensterenvelop? Dan maken we een tweede envelop, het adresveld staat al goed.

## Toepassingen: Voorgestelde waarden


De eerste drie zijn goedgekeurd in besluit D42. De lagere nieuwsbriefkop (na besluit D44) is een voorstel en staat zo in de figuur. Valt het af, dan blijft de kop 272 px met dezelfde opbouw en meer lucht boven het logo.

| Waarde | Voorstel | Reden |
|---|---|---|
| Hoogte van de stem op borden | zo hoog als de pijl of het pictogram ernaast (op routeborden 140 mm, op de lichtbak 200 mm); op het portaal zo hoog als het beeldmerk (250 mm) | De core spec zegt hoe dik en hoe ver, niet hoe hoog de stem als scheiding is. Even hoog als de kleinste module houdt de rij rustig en past binnen de marge. |
| Stem op PY-Oranje | PY-Diep, de inhoudskleur van oranje | De core spec noemt alleen navy en aqua. Op het betaalbord moet de familie doorlopen; PY-Diep haalt 6,87:1. |
| Welkomstwand | 3000 x 1000 mm, u = 50, kap 100 mm, stem 300 mm, zwaaier 600 mm op een lijn van 0,1u | Wandbanners staan in de brief, maar zonder maat. Dit formaat past op een standaard wandvlak bij lift of ingang. |
| Kop van de nieuwsbrief | 180 px hoog (was 272 px in besluit D42): 32 marge, logo 32, 24 lucht, stem en tekst 60, 32 marge; zwaaier 96 px op een lijn van 2 px | De 272 px was nodig voor het oude patroon met een parkeerder erin. Een vlakke kop met de stem en de zwaaier heeft 180 px genoeg; zo staat de hero-foto 92 px hoger, ook op een telefoon boven de vouw. |

## Toepassingen: Open vragen


- Er zijn twee storingsnummers: 085 401 16 47 (automaat, pyloon, posters) en 085 21 30 422 (spandoek). Wij gebruiken het eerste. Welk nummer is juist?
- Is er een algemeen telefoonnummer voor de bus, naast het storingsnummer?
- Heeft de abonnementspas een scancode, en zo ja welk type?
- Welke Vol/Vrij-display komt in het portaal, en in welke ledkleur?
- Welk busmodel rijdt er; daarna maken we de wrap op ware maat (5000 x 2300 is een aanname).
- Fluor oranje of fluor geel voor de jassen? Geel botst niet met PY-Oranje als het naast elkaar komt.
- GLOW-logo en campagnekleur moeten van de organisatie komen.
- Bij welke garages komt een welkomstwand, en is een voetgangersingang met de loper overal toegestaan, of eist de gemeente of de eigenaar ergens een pictogram?
- PY-Diep is CMYK 100 83 0 80 en RAL 5004 (besluit D23). Kleine tekst onder 12 pt op oranje drukwerk zet je in K 100 (besluit D24).
