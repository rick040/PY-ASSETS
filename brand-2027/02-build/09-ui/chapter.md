# 09 UI/UX

Dit hoofdstuk zegt hoe ParkingYou eruitziet en werkt op een scherm: de website, de boekflow en de PWA met je ticket. Alles komt uit de core spec en `tokens.json`. De componentmaten staan in de core spec (besluiten D4 tot en met D14) en in het tokenbestand.

## Principes voor schermen

1. **Eén hoofdknop per scherm.** Er is altijd één ding dat je hier het liefst doet. Dat is de hoofdknop. De rest is tweede keus of een link.
2. **Oranje is boeken en betalen.** De hoofdknop in de boek- en betaalroute is oranje met PY-Diep tekst: zoeken, reserveren, betalen. Staat er op een scherm niets te boeken of te betalen, dan is navy de hoofdknop (ticket bekijken, route plannen). Oranje zie je verder alleen bij een prijs.
3. **Navy is de tweede keus.** Navy met witte tekst is de secundaire knop. De link (onderstreept, `text.link`) is voor alles wat minder belangrijk is.
4. **De bubbel alleen op een moment dat telt.** Een prijs, een niveau, beschikbaarheid of een bevestiging. Eén bubbel per scherm. Nooit als knop, avatar of in elke kaart van een lijst. Op een kaart is de kleine navy bubbel van 24 px wel de pin, met een witte P of prijs erin; daar telt de regel van één bubbel niet.
5. **Kleur nooit alleen.** Vrij, Vol en Gesloten staan altijd als woord, met kleur en een icoon erbij. Een fout staat in woorden onder het veld.
6. **Rustig en vlak.** Wit en `surface.subtle` als ondergrond, kaarten met radius 16, schaduw alleen op kaarten en vaste balken, nooit op de bubbel of het logo.

## Tokenarchitectuur

![Tokenarchitectuur: primitief, semantisch, component, licht en donker](figures/token-architecture.png)

We werken in drie lagen.

| Laag | Wat | Voorbeeld | Wie gebruikt het |
|---|---|---|---|
| Primitief | De kleurwaarde zelf | `color.orange.500` #F08300 | Alleen de semantische laag |
| Semantisch | De betekenis, met een waarde voor licht en donker | `action.primary-bg` | Componenten |
| Component | Waar het zit | `button.primary.bg` | Code en Figma |

Een component leest alleen semantische tokens, nooit een primitief. Daardoor werkt donkere modus vanzelf: dezelfde naam krijgt in `[data-theme="dark"]` een andere waarde. Spacing, radius, type, schaduw en motion zijn al tokens in `tokens.json` en worden direct gebruikt.

De negen semantische groepen en hoe componenten ze lezen:

| Groep | Tokens | Gelezen door |
|---|---|---|
| `surface` | default, subtle, raised, brand, inverse | pagina, kaart, veld, navy kop, toast |
| `text` | default, muted, brand, on-brand, link, aqua | alle tekst, hulptekst, links |
| `border` | subtle, strong | kaartrand (decoratief), veldrand |
| `focus` | ring, ring-on-brand | focusring op licht en op navy |
| `action` | primary-bg/-hover/-pressed/-fg, secondary-bg/-hover/-fg | knoppen, gekozen chip, vinkje |
| `task` | drive, walk, pay (bg en fg) | inhoud van de bubbel, taakvlakken |
| `bubble` | navy, aqua, orange, white | de bubbel |
| `status` | free, full, closed | beschikbaarheid |
| `feedback` | error, error-bg, success, warning, info | meldingen en foutteksten |

In donkere modus is de pagina PY-Diep (`blue.900`), zijn vlakken `blue.800`, wordt `text.brand` en `text.link` aqua.300 en wordt de secundaire knop aqua met PY-Diep tekst. Navy is op donker nooit tekst of rand (1,61:1).

## Componenten

Alle componenten zijn gebouwd met echte `<button>`, `<input>`, `<label>` en `<select>`. Iconen zijn outline, 24-raster, 2 px lijn (Tabler Icons, zie het hoofdstuk Iconografie).

### Knoppen

![Knoppen: primair, secundair en link in zes staten](figures/buttons.png)

| Soort | Tokens | Gebruik |
|---|---|---|
| Primair | `action.primary-bg`, `-hover`, `-pressed`, `-fg` | Eén per scherm: Zoek een plek, Reserveer je plek, Betaal |
| Secundair | `action.secondary-bg`, `-hover`, `-fg` | Tweede keus, of hoofdknop zonder boek- of betaalactie |
| Link | `text.link` | Wijzig, Bekijk alles, Buitenlands kenteken? |
| Icoonknop | `text.brand` of `text.on-brand` | Terug, Sluiten, Menu; altijd met `aria-label` |

Vorm: pil (`radius.pill`). Maten: 48 standaard, 56 voor de hoofdknop onderaan een telefoonscherm. Padding 24 of 32, icoon 20 met 8 ruimte. Een knop heeft geen foutstaat: de fout staat bij het veld.

### Staten

| Staat | Knop primair | Knop secundair | Veld | Vinkje en rondje |
|---|---|---|---|---|
| Standaard | `action.primary-bg` | `action.secondary-bg` | rand 1 px `border.strong` op `surface.raised` | rand 2 px `border.strong` |
| Hover | `-bg-hover` (orange.400) | `-bg-hover` (blue.600) | rand 2 px `border.strong` | idem |
| Focus | ring 3 px `focus.ring`, 2 px los | idem | rand 2 px `focus.ring` plus ring | ring |
| Ingedrukt | `-bg-pressed` (orange.600) | voorstel `-bg-pressed` | n.v.t. | n.v.t. |
| Uitgeschakeld | `surface.subtle`, `text.muted`, rand `border.subtle` | idem | idem | idem |
| Fout | geen | geen | rand 2 px `feedback.error`, tekst eronder | rand `feedback.error` |
| Bezig | label plus draaiend icoon, `aria-busy` | idem | n.v.t. | n.v.t. |

Op een navy vlak blijft de hoofdknop oranje en wordt de focusring aqua (`focus.ring-on-brand`, 4,80:1).

### Invoervelden

![Tekstveld, datum en tijd, keuzelijst, kentekenveld, vinkje en rondje met hun staten](figures/form-fields.png)

- **Tekstveld.** Label boven (`label-m`), veld 48 hoog, `radius.m`, tekst `body-m` 16 px. Hulptekst onder in `body-s`, `text.muted`. Een placeholder is een voorbeeld, nooit het label.
- **Datum en tijd.** Twee velden naast elkaar, tabular cijfers. Op een telefoon opent de eigen kiezer van het toestel. Notatie: "za 14 nov 2026" en "10:00".
- **Kentekenveld.** 56 hoog, `heading-m`, hoofdletters, spatiëring 0,08 em, een NL-band in `surface.brand`. Je mag typen met of zonder streepjes; we zetten ze zelf goed volgens de Nederlandse indeling (6 tekens, bijvoorbeeld XX-123-X). `autocomplete="off"`, `spellcheck="false"`. Een link "Buitenlands kenteken?" opent een vrij veld. We imiteren de gele plaat niet: geel is geen merkkleur.
- **Keuzelijst.** Zelfde veld met chevron rechts.
- **Vinkje en rondje.** Vak 24, rij minstens 44 hoog, het hele label is klikbaar. Gekozen in `action.secondary-bg`. Betaalmethodes staan als keuze op een kaart.

### Locatiekaart

![Locatiekaart: anatomie, drie staten en grote variant](figures/location-card.png)

De hele kaart is één link; de naam is de linktekst. Foto 96 x 96 (`radius.m`), naam `heading-s`, afstand of openingstijd in `body-s` `text.muted`, onderaan status en prijs. Kaart: `surface.raised`, `radius.l`, `shadow.1`, rand `border.subtle`. Op desktop een grote variant met foto 3:2 bovenaan. In een lijst staat de prijs als tekst, niet in een bubbel.

### Beschikbaarheid, prijs en de bubbel

![Beschikbaarheid, prijsweergave en de bubbel in vier maten](figures/availability-price.png)

- **Status.** Vrij (`status.free`, vinkje), Vol (`status.full`, streep), Gesloten (`status.closed`, slot). Altijd woord, kleur en icoon. Alleen op `surface.default` of `surface.raised`.
- **Prijs.** "€ 12,50" met spatie, komma en tabular cijfers, altijd met eenheid ("per dag", "per 30 min"). Groot in `numeric-xl`, in een kaart `numeric-m`. Nooit oranje tekst op wit.
- **Bubbel als UI-element.**

| Maat | Inhoud | Voorbeeld |
|---|---|---|
| 24 | één cijfer (niveau) | niveau "0" in een regel |
| 40 | icoon 24 | bevestiging op het ticket |
| 64 | woord tot 6 tekens of niveau | Vrij, Vol |
| 104 | prijs met eenheid, of icoon 32 | "per dag € 12,50", bevestiging na betalen |

Kleur volgt de taak: navy rijden en niveau, aqua lopen en bevestiging, oranje alleen geld. Gesloten past niet in een bubbel. Vrije ruimte 8 px (24, 40) of 16 px (64, 104). De pop-in (0,9 naar 1, `easing.bubble`, `duration.expressive`) alleen bij een bevestiging.

### Meldingen, lege staat, chips

![Meldingen, toast, lege staat, filterchips en labels](figures/feedback-chips.png)

Meldingen: tekst in `text.default`, kleur in het icoon en een rand van 1 px rondom. Fout krijgt `feedback.error-bg`. Een fout die je zelf oplost staat bij het veld. Een toast (`surface.inverse`) is voor een bevestiging, nooit voor een fout. Een lege staat zegt wat hier komt, wat je kunt doen, en heeft één knop. Filterchips zijn knoppen met `aria-pressed`; labels zijn geen knoppen.

### Navigatie

![Bovenbalk, onderbalk voor de PWA en desktopbalk](figures/navigation.png)

Telefoon: bovenbalk 56 met logo (beeldmerk minstens 24 hoog) en menu; in de boekflow terug, titel, sluiten en een voortgangsbalk met "Stap 2 van 3". De PWA heeft een onderbalk met drie tabs: Zoeken, Tickets, Account, altijd icoon plus woord. Desktop: balk 72, inhoud maximaal 1200 breed. Geen oranje in de navigatie.

## Hoofdschermen

![Home, locatiepagina en ticket op de telefoon](figures/screens-key.png)

![Boekflow: wanneer, kenteken en gegevens, betalen, bevestiging](figures/screens-booking.png)

![Locatiepagina Parking Philips Stadion op desktop](figures/desktop-location.png)

![Locatiepagina en ticket in donkere modus](figures/dark-mode.png)

- **Home.** Navy kop met de stemregel "**Parkeren** zonder gedoe.", zoekkaart met waar en wanneer, oranje "Zoek een plek", daaronder locatiekaarten.
- **Locatiepagina.** Foto, status, naam, adres, prijsbubbel (dagtarief met reservering € 12,50), feiten (700 plekken, doorrijhoogte 2,00 m, 9 min naar centrum, 24 uur open), vaste knop "Reserveer je plek". Op desktop staat de boekkaart rechts in 5 van de 12 kolommen.
- **Boekflow.** Drie stappen: wanneer, kenteken en gegevens, betalen. Totaal en hoofdknop staan vast onderaan. De bevestiging heeft de aqua bubbel en een navy knop "Bekijk je ticket".
- **Ticket (PWA).** Locatie en datum, kenteken groot, geldig van 10:00 tot 18:00, hoe je binnenkomt, een QR-code als reserve, adres en doorrijhoogte, navy knop "Plan je route". Het ticket moet zonder bereik werken: in de garage is vaak geen signaal.
- **Donkere modus.** Dezelfde schermen, alleen de semantische waarden wisselen. De QR-code blijft donker op wit.

## Toegankelijkheid

Doel: WCAG 2.2 AA op elk scherm.

| Criterium | Wat wij doen |
|---|---|
| 1.4.3 Contrast tekst | Alle semantische tekstparen halen 4,5:1 (`tokens/contrast.md`). Status alleen op `surface.default` of `raised`: `status.full` op `surface.subtle` is 4,44:1 en faalt. |
| 1.4.11 Contrast UI | Veldrand `border.strong` 4,24:1 (licht) en 5,12:1 (donker). `border.subtle` (1,31:1) is alleen decoratie, nooit de enige rand van een veld. Een oranje knop zonder tekst bestaat niet: oranje op wit is 2,64:1. |
| 2.4.7 Focus zichtbaar | Ring 3 px `focus.ring`, 2 px los; op navy aqua. Nooit `outline: none` zonder vervanging. |
| 2.4.11 Focus niet bedekt | De vaste balk onderaan en een cookiebalk bedekken nooit het veld met focus: `scroll-padding-bottom` gelijk aan de balkhoogte. |
| 2.5.8 Doelgrootte | Wij gebruiken 44 x 44, ook voor icoonknoppen, tabs en chips (chip 36 zichtbaar, raakvlak 44). Alleen een link in lopende tekst is uitgezonderd. |
| 3.3.7 Dubbele invoer | Kenteken en e-mail typ je één keer. Stap 3, de bevestiging en het ticket nemen ze over. Met jouw akkoord bewaren we ze voor de volgende keer. |
| 3.3.8 Toegankelijk inloggen | Geen puzzel of overtypen van tekens. Inloggen met een link in je mail of een passkey. Plakken en wachtwoordmanagers werken; `autocomplete="email"` en `one-time-code`. |

Verder: een fout heeft `aria-invalid` en `aria-describedby`, de toast `role="status"`, de pagina werkt bij 320 px breed en 200 procent tekst, en motion volgt `prefers-reduced-motion`.

**EAA.** Sinds 28 juni 2025 houdt de ACM toezicht op de Europese toegankelijkheidsregels voor websites en apps waarmee je een dienst koopt of reserveert, bij bedrijven met meer dan 10 medewerkers of meer dan € 2 miljoen omzet ([ACM](https://www.acm.nl/en/publications/acm-calls-businesses-prepare-themselves-new-rules-regarding-accessibility-websites-and-apps)). Boeken en betalen van parkeren valt daaronder (aanname, juridisch te bevestigen). EN 301 549 v4.1.1 neemt WCAG 2.2 AA over ([Deque](https://www.deque.com/blog/en-301-549-v4-1-1-is-final-what-changed-what-it-means-and-what-you-should-do/)). Dit geldt ook voor de boekschermen van Aeroparker: wie dat deel bouwt, moet aan dezelfde lat voldoen. Publiceer een toegankelijkheidsverklaring.

## UX-tekst

Altijd je en jij, korte zinnen, geen uitroeptekens bij fouten, geen emoji.

| Soort | Regel | Wel | Niet |
|---|---|---|---|
| Knop | Werkwoord eerst, zeg wat er gebeurt | Reserveer je plek · Betaal € 12,50 · Plan je route | Verzenden · OK · Klik hier · Doorgaan naar betaalpagina |
| Fout | Wat is er mis, en hoe los je het op | Je vertrektijd ligt voor je aankomst. Kies een tijd na 10:00. | Ongeldige invoer! · Fout 422 |
| Fout kenteken | Concreet, met voorbeeld | Dit kenteken is te kort. Een Nederlands kenteken heeft 6 letters en cijfers. | Kenteken onjuist |
| Betaalfout | Geruststellen, dan de stap | Betalen is niet gelukt. Je bent niets kwijt. Probeer het opnieuw. | Transactie mislukt |
| Lege staat | Wat komt hier, wat kun je doen, één knop | Je hebt nog geen tickets. Reserveer een plek, dan staat je ticket hier. | Geen data gevonden |
| Geen resultaat | Geef een uitweg | Geen plek vrij op deze tijd. Kies een andere tijd of kijk in de buurt. | 0 resultaten |

Prijzen als "€ 12,50", tijden als "10:00 tot 18:00", datums als "za 14 nov 2026".

## Open punten

- Adres van Parking Philips Stadion, live beschikbaarheid en servicekosten zijn nog onbekend en staan als [placeholder].
- In donkere modus zijn `surface.subtle` en `surface.raised` allebei blue.800. Een gekozen staat in `subtle` op een kaart verdwijnt. Wij stappen dan terug naar `surface.default`; de generator kan dit beter oplossen met een eigen token.
- Welke schermen van Aeroparker kunnen we stylen, en ondersteunt de PWA een ticket zonder bereik?

## Do's en don'ts

| Do | Don't |
|---|---|
| Eén oranje hoofdknop per scherm, in de boek- en betaalroute | Twee oranje knoppen, of oranje voor "Inloggen" of navigatie |
| Navy als hoofdknop op een scherm zonder boeken of betalen | Een navy knop op een navy vlak |
| Status als woord, kleur en icoon | Een gekleurde stip zonder woord |
| Eén bubbel per scherm, voor prijs, niveau, beschikbaarheid of bevestiging | De bubbel als knop, avatar of in elke kaart (de kaartpin is de enige uitzondering) |
| Label boven het veld, fout eronder in woorden | Alleen een rode rand, of een placeholder als label |
| Componenten lezen semantische tokens | Hexwaarden of primitieven in een component |
| Raakvlak 44 x 44 | Icoonknoppen of chips kleiner dan 44 |
| De vaste knop onderaan houdt het veld met focus vrij | Een cookiebalk over de betaalknop |
| QR-code donker op wit, ook in donkere modus | QR-code in aqua of op navy |

## Voorgestelde waarden

Goedgekeurd in de core spec als besluiten D4 tot en met D14; de waarden staan nu in het tokenbestand. De tabel blijft als uitleg.

| Waarde | Voorstel | Reden |
|---|---|---|
| Hoogte knop en veld | 48 px | 44 is het minimum; 48 geeft ruimte voor tekst van 16 px en lijnt knoppen en velden in één rij uit. |
| Hoogte groot | 56 px | Hoofdknop onderaan een telefoonscherm en het kentekenveld: makkelijk te raken met de duim. |
| Type knoplabel `label-l` | 16/24, 600 | `label-m` (14) is te klein voor de hoofdactie; `body-m` is 400 en leest niet als knop. |
| Focusring | 3 px breed, 2 px los | Zichtbaar op wit, oranje en navy; ruimer dan de 2 px die 2.4.13 (AAA) noemt. |
| Randdikte | 1 px rust, 2 px hover, focus en fout | Verschil tussen staten zonder alleen op kleur te leunen. |
| Bovenbalk | 56 px telefoon, 72 px desktop | Ruimte voor icoonknop 44 en logo boven het minimum van 24. |
| Onderbalk PWA | 64 px plus veilige zone | Tab 44 hoog met icoon plus woord. |
| Chip | 36 px zichtbaar, raakvlak 44 | Rustiger in een rij; doelgrootte blijft 44. |
| Label (tag) | 28 px | Geen knop, dus kleiner mag. |
| Melding | rand 1 px rondom (besluit D10) | Kleur zonder gekleurde tekst. |
| Voortgangsbalk | 4 px, `radius.pill` | Dun, de tekst "Stap 2 van 3" draagt de informatie. |
| Kentekenveld | NL-band 36 px breed, spatiëring 0,08 em | Herkenbaar als kenteken zonder de gele plaat na te maken. |
| Foto-verhouding | 3:2, kaartfoto 96 x 96 | Onze eigen foto's zijn 3:2; één verhouding voor alle locaties. |
| Cijfer in bubbel 24 | 12 px, 800 | `label-s` is 600; de core spec vraagt 800 voor cijfers in de bubbel. |
| Prijs in bubbel 104 | 20/26, 800 | `numeric-m` is 700; zelfde reden. |
| Toastduur | minimaal 6 s; met een actie sluit hij niet vanzelf (besluit D12) | Lang genoeg om te lezen (WCAG 2.2.1). |
| `action.secondary-bg-pressed` | licht blue.800 (14,73:1 met wit), donker aqua.600 (5,43:1 met PY-Diep) | Ontbreekt in `tokens.json`; nodig voor de ingedrukte staat. |
| `surface.code`, `text.on-code` | neutral.0 en blue.900 in beide modi | De QR-code moet in elke modus donker op wit staan. |
| Componentlaag | `button.primary.bg` → `action.primary-bg`, `button.secondary.bg` → `action.secondary-bg`, `input.border` → `border.strong`, `input.bg` en `card.bg` → `surface.raised`, `status.free.fg` → `status.free`, `focus.ring.color` → `focus.ring` | Derde laag in de generator, zodat code en Figma dezelfde namen gebruiken. |
