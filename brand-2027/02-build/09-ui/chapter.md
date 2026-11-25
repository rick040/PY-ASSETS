# 09 UI/UX

Dit hoofdstuk zegt hoe ParkingYou eruitziet en werkt op een scherm: de website, de boekflow en de PWA met je ticket. Alle maten en kleuren komen uit `tokens.json`. Een component leest alleen tokens, nooit een losse waarde.

## Principes voor schermen

1. **Eén hoofdknop per scherm.** Er is altijd één ding dat je hier het liefst doet. Dat is de hoofdknop: PY-Blauw met witte tekst, of het nu zoeken, reserveren, betalen of je ticket bekijken is. De tweede keus is een omlijnde knop of een link.
2. **Geen oranje op het scherm.** Oranje betekent betalen in de garage. Op de website en in de app komt het niet voor. Alleen een waarschuwing (`feedback.warning`) en de status Vol (`status.full`) zijn oranje.700, en dan als tekst of icoon, nooit als vlak of rand.
3. **Het merk helpt je verder.** Onze eigen elementen staan alleen waar ze iets doen. Per scherm het logo plus hooguit twee van de vier.
4. **De bubbel op een moment dat telt.** Eén bubbel per scherm, altijd rechtop, nooit als knop of avatar. De kaartpin is de uitzondering.
5. **Kleur nooit alleen.** Vrij, Vol en Gesloten staan altijd als woord, met kleur en icoon. Een fout staat in woorden bij het veld.
6. **Rustig en vlak.** Veel wit, grote koppen, kaarten met radius 16. Een kop is vlak PY-Blauw of wit. Schaduw alleen op kaarten en vaste balken. Geen verloop.

## Eigen elementen op het scherm

![Hoofdschermen: de stem en de zwaaier op home, bubbel en pijl op de locatiepagina, de stem en de springer op het ticket](figures/screens-key.png)

Het product moet voelen als ParkingYou op de momenten die ertoe doen. Verder blijft het rustig. Deze tabel zegt welk element waar staat.

| Scherm | Logo | Elementen | Waarom |
|---|---|---|---|
| Home | ja | stem, zwaaier | De stem opent de kop, de zwaaier heet je welkom op de zoekkaart. |
| Locatiepagina | nee | bubbel, pijl | De prijs in de bubbel, de pijl naar de volgende stap. |
| Boekflow stap 1 tot 3 | nee | pijl | Hier wil je door, niet kijken. |
| Bevestiging | nee | stem, springer | De springer viert dat het geregeld is. |
| Ticket (PWA) | nee | stem, springer | Vlakke PY-Blauw kop, de springer op een korte witte lijn. |
| Lege staat | nee | zwaaier | Een leeg scherm voelt minder leeg. |
| Foutscherm | ja | gastheer wijst | Hij wijst naar het contact. |
| Desktop locatiepagina | ja | bubbel, pijl | Zoals op de telefoon. |

**De stem.** De halve boog (`kit/assets/arc.svg`) staat links van een kop van één tot drie regels. Hoogte = het tekstblok, lijn = 1/25 van die hoogte (minstens 1,5 px), afstand tot de tekst = 0,3 x de hoogte. Bij `heading-l` over twee regels: 76 px hoog, 3 px lijn, 23 px afstand. Kleur `voice.arc` (aqua.500). Alleen op home, de bevestiging en het ticket.

**De parkeerders.** Eén per scherm, 48 tot 160 px hoog, altijd staand op een lijn: de rand van een kaart, de bovenrand van de knoppenbalk of een korte lijn van 2 px. Een korte lijn loopt aan beide kanten 16 px (`space.4`) voorbij de figuur. Figuur en lijn hebben één kleur (`figure.body`): navy op wit, wit op navy. Een parkeerder is decoratie: `alt=""`. Nooit bij een betaalfout of een veldfout: daar is iemand geld of tijd kwijt.

**Vlakke koppen.** Een kop met merk is een vlakke band in `surface.brand` of wit, zonder patroon, vorm of grote bubbel erachter. De ticketkop is in licht en donker dezelfde PY-Blauw band.

**De hoekige pijl.** De pijl uit het handboek (`kit/assets/arrow-plain-navy.svg`), in stappen van 45 graden. In knoppen en links staat hij achter het label, op de basislijn, zo hoog als een hoofdletter (11 px bij een label van 16 px), 8 px na het label, in de tekstkleur van de knop. In de terugknop zonder label is de pijl 16 px, in een raakvlak van 44 x 44 px. Alleen bij een richting of een volgende stap. Nooit een chevron, een pijl uit de iconenset of een pijl in een cirkel.

## Tokenarchitectuur

![Tokenarchitectuur: primitief, semantisch, component, licht en donker](figures/token-architecture.png)

We werken in drie lagen.

| Laag | Wat | Voorbeeld | Wie gebruikt het |
|---|---|---|---|
| Primitief | De kleurwaarde zelf | `color.blue.700` #1A3580 | Alleen de semantische laag |
| Semantisch | De betekenis, met een waarde voor licht en donker | `action.primary-bg` | Componenten |
| Component | Waar het zit | `button.primary.bg` | Code en Figma |

Een component leest alleen semantische tokens. Daardoor werkt donkere modus vanzelf: dezelfde naam krijgt in `[data-theme="dark"]` een andere waarde.

| Groep | Tokens | Gelezen door |
|---|---|---|
| `surface` | default, subtle, raised, brand, inverse, code | pagina, kaart, veld, navy kop, toast, QR-code |
| `text` | default, muted, brand, on-brand, link, aqua, on-code, on-inverse | alle tekst, hulptekst, links, toast |
| `border` | subtle, strong | kaartrand (decoratief), veldrand |
| `focus` | ring, ring-on-brand | focusring op licht en op navy |
| `action` | primary-bg/-hover/-pressed/-fg, secondary-bg/-hover/-pressed/-fg/-border | knoppen, gekozen chip, vinkje, voortgangsbalk |
| `task` | drive, walk, pay (bg en fg) | inhoud van de bubbel |
| `voice` | arc | de stem |
| `figure` | body | de parkeerders en hun lijn |
| `bubble` | navy, aqua, orange, white | de bubbel; orange nooit op een scherm |
| `status` | free, full, closed | beschikbaarheid |
| `feedback` | error, error-bg, success, warning, info | meldingen en foutteksten |

Donker: pagina PY-Diep (`blue.900`), kaarten `blue.800`, vlakken `blue.850`. Navy is op donker nooit tekst, rand of bubbel (1,61:1).

## Componenten

Alle componenten zijn echte `<button>`, `<input>`, `<label>` en `<select>`. Iconen zijn outline, 24-raster, 2 px lijn (Tabler Icons, zie hoofdstuk 7, Iconografie). Pijlen zijn altijd de hoekige pijl.

### Knoppen

![Knoppen: primair, secundair en link in zes staten, de hoekige pijl, op navy en donker](figures/buttons.png)

| Soort | Tokens | Gebruik |
|---|---|---|
| Primair | `action.primary-bg`, `-hover`, `-pressed`, `-fg` | Eén per scherm: Zoek een plek, Betaal |
| Secundair (omlijnd) | `action.secondary-bg`, `-hover`, `-pressed`, `-fg`; rand 2 px in `action.secondary-border` | Tweede keus: Wijzig, Andere tijd |
| Link | `text.link` | Bekijk alles |
| Icoonknop | `text.brand` of `text.on-brand` | Terug, Sluiten, Menu; altijd met `aria-label` |

Pil (`radius.pill`), hoogte 48, of 56 onderaan een telefoonscherm. Padding 24 of 32, icoon 20 met 8 ruimte. Een knop heeft óf een icoon vooraan, óf een pijl achteraan, nooit allebei. Een knop heeft geen foutstaat: de fout staat bij het veld.

**Op een navy vlak** gelden de donkere waarden (`data-theme="dark"`): de hoofdknop wordt aqua met PY-Diep tekst.

### Staten

| Staat | Knop primair | Knop secundair | Veld | Vinkje en rondje |
|---|---|---|---|---|
| Standaard | `action.primary-bg` (blue.700) | wit, rand en tekst 2 px blue.700 | rand 1 px `border.strong` op `surface.raised` | rand 2 px `border.strong` |
| Hover | `-bg-hover` (blue.600) | `-bg-hover` (blue.50) | rand 2 px `border.strong` | idem |
| Focus | ring 3 px `focus.ring`, 2 px los | idem | rand 2 px `focus.ring` plus ring | ring |
| Ingedrukt | `-bg-pressed` (blue.800) | `-bg-pressed` (blue.100) | n.v.t. | n.v.t. |
| Gekozen | n.v.t. | n.v.t. | n.v.t. | vlak `action.primary-bg`, vinkje `action.primary-fg` |
| Uitgeschakeld | `surface.subtle`, `text.muted`, rand `border.subtle` | idem | idem | idem |
| Fout | geen | geen | rand 2 px `feedback.error`, melding eronder | rand `feedback.error`, melding eronder |
| Bezig | label plus draaiend icoon, `aria-busy` | idem | n.v.t. | n.v.t. |

Donker: primair aqua.500, hover aqua.400, ingedrukt aqua.600, tekst blue.900; secundair blue.900, hover blue.800, ingedrukt blue.850, rand en tekst aqua.300.

### Invoervelden

![Tekstveld, datum en tijd, keuzelijst, kentekenveld, vinkje en rondje met hun staten](figures/form-fields.png)

- **Tekstveld.** Label boven (`label-m`), veld 48 hoog, `radius.m`, tekst 16 px. Hulptekst onder in `body-s`. Een placeholder is nooit het label.
- **Datum en tijd.** Twee velden naast elkaar, tabular cijfers, de kiezer van het toestel.
- **Kentekenveld.** 56 hoog, `heading-m`, hoofdletters, spatiëring 0,08 em, een NL-band in `surface.brand`. Typen mag met of zonder streepjes; wij zetten ze goed. "Buitenlands kenteken?" opent een vrij veld. Geen imitatie van de gele plaat.
- **Keuzelijst.** Zelfde veld, met de hoekige pijl omlaag rechts op hoofdletterhoogte.
- **Vinkje en rondje.** Kader 24, rij minstens 44 hoog, het hele label is klikbaar. Een betaalmethode is een keuze op een kaart; gekozen krijgt een rand van 2 px in `action.primary-bg`.
- **Fout.** Onder het veld, het vinkje of de groep rondjes staat een melding in woorden met het fouticoon, bijvoorbeeld "Vink dit aan om door te gaan." Het veld of vakje krijgt `aria-invalid="true"` en `aria-describedby` met de id van de melding. Bij een groep rondjes wijst de `fieldset` naar de melding.

### Locatiekaart

![Locatiekaart: anatomie, drie staten en grote variant](figures/location-card.png)

De hele kaart is één link; de naam is de linktekst. Foto 96 x 96 met `radius.m`, naam `heading-s`, onderaan status en prijs. Kaart: `surface.raised`, `radius.l`, `shadow.1`. Op desktop een grote variant met foto 3:2. In een lijst staat de prijs als tekst, niet in een bubbel.

### Beschikbaarheid, prijs en de bubbel

![Beschikbaarheid, prijsweergave, de kaartpin en de bubbel in vier maten](figures/availability-price.png)

- **Status.** Vrij (`status.free`, vinkje), Vol (`status.full`, streep), Gesloten (`status.closed`, slot). Altijd woord, kleur en icoon. Alleen op `surface.default` of `surface.raised`.
- **Prijs.** "€ 12,50": spatie, komma, tabular cijfers, en altijd de eenheid ernaast ("per dag", "per 30 min"). Groot in `numeric-xl`, in een kaart `numeric-m`. Nooit in oranje.
- **Bubbel als UI-element.**

| Maat | Inhoud | Voorbeeld |
|---|---|---|
| 24 | P of één cijfer | kaartpin (navy, witte P), niveau "0" in een regel |
| 40 | één cijfer of icoon 24 | niveau "−1" op een navy vlak (aqua, PY-Blauw cijfer) |
| 64 | woord tot 6 tekens of niveau | Vrij, Vol (navy, wit) |
| 104 | alleen het bedrag | "€ 12,50" op de locatiepagina, "per dag" ernaast |

Navy op wit, aqua op navy en in donkere modus. Vrije ruimte 8 px (24, 40) of 16 px (64, 104). De pop-in hoort alleen bij een merkmoment, zoals het openen van de app (zie hoofdstuk 8, Beweging).

**Kaart.** Elke locatie op de kaart is een navy bubbel van 24 px met een witte P, rechtop, de punt op de locatie. De regel van één bubbel per scherm geldt niet voor kaartdata. Een kaart is nooit de enige weg:

- Naast de kaart staat altijd een lijst met dezelfde locaties.
- Elke pin is met het toetsenbord te bereiken en opent met Enter.
- Elke pin heeft een tekstalternatief met naam, status en prijs, zoals "Parking Philips Stadion, vrij, € 12,50 per dag".
- Knoppen plus en min zoomen in en uit. Zo hoef je niet te knijpen of te slepen.

### Meldingen, toast, chips

![Meldingen, toast, filterchips en labels, licht en donker](figures/feedback-chips.png)

Een melding heeft tekst in `text.default`, de kleur in het icoon en een rand van 1 px rondom. Fout krijgt `feedback.error-bg`. Een waarschuwing heeft een oranje.700 icoon en een neutrale rand (`border.strong`): oranje alleen als icoon of tekst. Een fout die je zelf oplost staat bij het veld.

Een toast (`surface.inverse`) is voor een bevestiging, nooit voor een fout. Tekst en icoon zijn `text.on-inverse`: wit op PY-Diep in licht, PY-Diep op wit in donker, allebei 18,16:1. Een toast blijft minstens 6 seconden staan; een toast met een actie sluit nooit vanzelf.

Filterchips zijn knoppen met `aria-pressed`. Labels zijn geen knoppen.

### Lege staat en foutscherm

![Lege staat met de zwaaier en foutscherm met de gastheer](figures/empty-error.png)

- **Lege staat.** Wit scherm, de zwaaier op een korte navy lijn, dan "Je hebt nog geen tickets", wat je kunt doen en één navy knop "Zoek een plek".
- **Foutscherm.** Een pagina die niet bestaat, geen verbinding of onderhoud. De gastheer wijst naar het contact (info@parkingyou.nl, [telefoonnummer]). Daaronder één hoofdknop en een link naar home.
- **Geen figuur bij een fout in een formulier of bij betalen.** Daar staat alleen de melding, rustig en concreet.

### Navigatie

![Bovenbalk, onderbalk voor de PWA en desktopbalk](figures/navigation.png)

Telefoon: bovenbalk 56 met logo en menu; in de boekflow terug, titel, sluiten en een voortgangsbalk met "Stap 2 van 3". De PWA heeft een onderbalk met drie tabs: Zoeken, Tickets, Account, altijd icoon plus woord. De actieve tab heeft `aria-current="page"`. Desktop: balk 72, inhoud maximaal 1200 breed, de actieve link onderstreept, ook met `aria-current="page"`.

## Hoofdschermen

![Boekflow: wanneer, kenteken en gegevens, betalen, bevestiging met de springer](figures/screens-booking.png)

![Locatiepagina Parking Philips Stadion op desktop](figures/desktop-location.png)

![Locatiepagina en ticket in donkere modus](figures/dark-mode.png)

- **Home.** Navy kop met logo, stem en zwaaier. Zoekkaart met waar en wanneer, knop "Zoek een plek", daaronder locatiekaarten.
- **Locatiepagina.** Foto, status, naam, adres, de prijsbubbel met € 12,50 en "per dag" ernaast, feiten, vaste knop "Reserveer je plek". Op desktop staat de boekkaart rechts in 5 van de 12 kolommen.
- **Boekflow.** Drie stappen: wanneer, kenteken en gegevens, betalen. Totaal en hoofdknop staan vast onderaan. "Ga verder" heeft de pijl, "Betaal € 12,50" een slotje.
- **Bevestiging.** De stem voor "**Je plek** is gereserveerd.", een samenvatting, de springer op de knoppenbalk, knop "Bekijk je ticket".
- **Ticket (PWA).** Een tab, dus zonder terugknop. Onder de PY-Blauw kop de ticketkaart: locatie, datum, kenteken groot, geldig van 10:00 tot 18:00, hoe je binnenkomt, een QR-code als reserve, knop "Plan je route". Het ticket werkt zonder bereik: in de garage is vaak geen signaal.
- **Donkere modus.** Dezelfde schermen; de prijsbubbel en de hoofdknop worden aqua, de ticketkop blijft PY-Blauw, de QR-code blijft donker op wit.

## Toegankelijkheid

Doel: WCAG 2.2 AA op elk scherm. Alle contrasten zijn berekend op de waarden in `tokens.json`.

| Criterium | Wat wij doen |
|---|---|
| 1.4.3 Contrast tekst | Alle tekstparen halen 4,5:1, in licht en donker. Hoofdknop 11,26:1 (donker 7,74:1), prijsbubbel 11,26:1 (donker 4,80:1), toast 18,16:1, Vol en waarschuwing 4,80:1. Status nooit op `surface.subtle`: Vol haalt daar 4,44:1. |
| 1.4.11 Contrast UI | Veldrand 4,24:1 (donker 5,12:1), kaartpin 9,86:1 op een lichte kaartgrond. `border.subtle` (1,31:1) is nooit de enige rand van iets dat je moet zien. |
| 1.1.1 Niet-tekstuele inhoud | De stem en de parkeerders zijn decoratie: `alt=""` of `aria-hidden`. De bubbel met prijs of niveau heeft een label ("€ 12,50 per dag", "Niveau −1"). Elke kaartpin heeft een tekstalternatief. De pijl in een knop is `aria-hidden`; de terugknop heeft `aria-label="Terug"`. |
| 1.3.1 Info en relaties, 2.4.6 Koppen | Eén `h1` per pagina, koppen in volgorde. Landmarks: `header`, `nav` met een naam, `main`, `footer`. |
| 1.4.12 Tekstafstand | Niets valt weg of overlapt bij regelafstand 1,5, alinea-afstand 2 x de lettergrootte, letterafstand 0,12 em en woordafstand 0,16 em. Geen vaste hoogtes op tekstblokken. |
| 2.1.1 Toetsenbord | Alles werkt met het toetsenbord, ook de kaartpins. Naast de kaart staat altijd een lijst. |
| 2.4.1 Blokken omzeilen | Een skiplink "Naar de inhoud" is het eerste element dat focus krijgt en wordt zichtbaar bij focus. |
| 2.4.7 Focus zichtbaar | Ring 3 px `focus.ring`, 2 px los; op navy en donker aqua. Nooit `outline: none` zonder vervanging. |
| 2.4.11 Focus niet bedekt | De vaste balk onderaan en een cookiebalk bedekken nooit het veld met focus: `scroll-padding-bottom` gelijk aan de balkhoogte. |
| 2.5.7 Sleepbewegingen | Zoomknoppen plus en min op de kaart; de lijst vervangt schuiven over de kaart. |
| 2.5.8 Doelgrootte | Wij gebruiken 44 x 44, ook voor icoonknoppen, de terugpijl, tabs en chips (chip 36 zichtbaar, raakvlak 44). Alleen een link in lopende tekst is uitgezonderd. |
| 3.1.1 Taal van de pagina | `<html lang="nl">`. Een Engelse zin krijgt `lang="en"` op zijn eigen element. |
| 3.3.1 Foutidentificatie | Een fout staat in woorden onder het veld, met icoon. Het veld heeft `aria-invalid="true"` en `aria-describedby` naar de melding. |
| 3.3.7 Dubbele invoer | Kenteken en e-mail typ je één keer. Met jouw akkoord bewaren we ze voor de volgende keer. |
| 3.3.8 Toegankelijk inloggen | Geen puzzel of overtypen. Inloggen met een link in je mail of een passkey; plakken en wachtwoordmanagers werken. |
| 4.1.2 Naam, rol, waarde | De actieve tab en de actieve link in de menubalk hebben `aria-current="page"`. Filterchips hebben `aria-pressed`. |
| 4.1.3 Statusberichten | De toast heeft `role="status"`. |
| 2.3.3 Animatie (AAA) | Beweging volgt `prefers-reduced-motion`: dan een fade van 120 ms of niets. |

De pagina werkt bij 320 px breed en bij 200 procent tekst.

**Europese toegankelijkheidswet.** Sinds 28 juni 2025 gelden Europese regels voor websites en apps waarmee je een dienst koopt of reserveert. De ACM houdt toezicht ([ACM](https://www.acm.nl/en/publications/acm-calls-businesses-prepare-themselves-new-rules-regarding-accessibility-websites-and-apps)). De regels gelden voor elk bedrijf met 10 of meer medewerkers of meer dan € 2 miljoen omzet. Alleen een micro-onderneming, met minder dan 10 medewerkers en hooguit € 2 miljoen omzet, valt erbuiten. Parkeren boeken en betalen valt eronder. De norm EN 301 549 v4.1.1 neemt WCAG 2.2 AA over ([Deque](https://www.deque.com/blog/en-301-549-v4-1-1-is-final-what-changed-what-it-means-and-what-you-should-do/)). Dat geldt ook voor de boekschermen van Aeroparker. Publiceer een toegankelijkheidsverklaring.

## UX-tekst

Altijd je en jij, korte zinnen, geen uitroeptekens bij fouten, geen emoji.

| Soort | Regel | Wel | Niet |
|---|---|---|---|
| Knop | Werkwoord eerst, zeg wat er gebeurt | Reserveer je plek · Betaal € 12,50 · Plan je route | Verzenden · OK · Klik hier · Doorgaan naar betaalpagina |
| Fout | Wat is er mis, en hoe los je het op | Je vertrektijd ligt voor je aankomst. Kies een tijd na 10:00. | Ongeldige invoer! · Fout 422 |
| Fout kenteken | Concreet, met voorbeeld | Dit kenteken is te kort. Een Nederlands kenteken heeft 6 letters en cijfers. | Kenteken onjuist |
| Fout vinkje | Zeg wat je moet doen | Vink dit aan om door te gaan. | Verplicht veld |
| Betaalfout | Geruststellen, dan de stap | Betalen is niet gelukt. Je bent niets kwijt. Probeer het opnieuw. | Transactie mislukt |
| Bevestiging | Zeg wat er nu geregeld is | Je plek is gereserveerd. Rij gewoon naar binnen: je kenteken is je ticket. | Gefeliciteerd! · Bestelling geplaatst |
| Lege staat | Wat komt hier, wat kun je doen, één knop | Je hebt nog geen tickets. Reserveer een plek, dan staat je ticket hier. | Geen data gevonden |
| Foutscherm | Wat is er, en waar kun je heen | Deze pagina is er niet. Zoek een plek, of vraag het ons. | 404 Not Found · Oeps! |
| Geen resultaat | Geef een uitweg | Geen plek vrij op deze tijd. Kies een andere tijd of kijk in de buurt. | 0 resultaten |

Prijzen als "€ 12,50", tijden als "10:00 tot 18:00", datums als "za 14 nov 2026".

## Open punten

- Adres van Parking Philips Stadion, live beschikbaarheid, servicekosten, andere tarieven dan € 12,50 en het algemene telefoonnummer zijn nog onbekend en staan als placeholder.
- `status.full` is oranje.700, dezelfde waarde als `feedback.warning`. Als oranje op het scherm helemaal weg moet, kan Vol `text.default` met het streep-icoon worden (16,88:1).
- Welke schermen van Aeroparker kunnen we stylen, en ondersteunt de PWA een ticket zonder bereik?
- De bubbel van 40 heeft geen vast scherm meer, nu het ticket geen bubbel heeft. Houden voor het niveau van je plek, als de PWA dat later toont?

## Do's en don'ts

- **Wel:** één navy hoofdknop per scherm, met witte tekst.
- **Wel:** de tweede knop omlijnd: wit, rand en tekst 2 px PY-Blauw.
- **Wel:** de hoekige pijl op hoofdletterhoogte bij een volgende stap of richting; in de terugknop 16 px in een raakvlak van 44 x 44.
- **Wel:** de stem voor de kop van home, de bevestiging en het ticket.
- **Wel:** één parkeerder per scherm, staand op een lijn, bij welkom, bevestiging of een foutscherm.
- **Wel:** een vlakke kop in PY-Blauw of wit, met de stem en één parkeerder.
- **Wel:** per scherm het logo plus hooguit twee eigen elementen.
- **Wel:** één bubbel per scherm, rechtop, met alleen het bedrag erin en "per dag" ernaast.
- **Wel:** status als woord, kleur en icoon.
- **Wel:** label boven het veld, fout eronder in woorden, met icoon, `aria-invalid` en `aria-describedby`.
- **Wel:** naast een kaart altijd een lijst, en pins die je met het toetsenbord bereikt.
- **Wel:** componenten die alleen semantische tokens lezen.
- **Wel:** raakvlak 44 x 44.
- **Wel:** de QR-code donker op wit, ook in donkere modus.
- **Niet:** twee hoofdknoppen, of een oranje knop, prijs, rand of bubbel op een scherm.
- **Niet:** een navy knop op een navy vlak; gebruik daar de donkere action-waarden.
- **Niet:** een chevron, een pijl uit de iconenset, of een pijl in een cirkel of bubbel.
- **Niet:** de stem voor elke kop, of rechts van de tekst.
- **Niet:** een parkeerder bij een betaalfout, zwevend, gedraaid of met een spreekballon.
- **Niet:** een patroon, vorm of grote bubbel achter een kop of lege staat.
- **Niet:** drie of vier eigen elementen op één scherm.
- **Niet:** de bubbel als knop, avatar of in elke kaart van een lijst.
- **Niet:** een gekleurde stip zonder woord.
- **Niet:** alleen een rode rand, of een placeholder als label.
- **Niet:** hexwaarden of primitieven in een component.
- **Niet:** icoonknoppen of chips kleiner dan 44.
- **Niet:** een QR-code in aqua of op navy.
