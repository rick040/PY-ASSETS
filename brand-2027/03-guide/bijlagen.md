## 14. Bijlagen

### 14.1 Tokens

Alle waarden in deze gids komen uit één bron: `brand-2027/tokens/tokens.json`, in het W3C-formaat voor design tokens (DTCG). Daaruit worden `tokens.css` voor schermen en `contrast.md` met alle doorgerekende kleurparen gemaakt. Een waarde die daar niet in staat, gebruiken we niet. Wil je een nieuwe waarde, vraag het dan aan de merkbeheerder.

De tokens hebben drie lagen:

| Laag | Wat het is | Voorbeeld |
|---|---|---|
| Basis | De ruwe waarden: kleuren, maten, tijden | `color.blue.700` = #1A3580 |
| Betekenis | Waar een waarde voor dient, licht en donker | `action.primary-bg`, `text.brand`, `task.pay-bg` |
| Onderdeel | Vaste waarden per onderdeel | `button.primary.bg`, `card.title`, `ticket.code-bg` |

**Merkkleuren**

| Naam | HEX | RGB | CMYK | RAL | Token |
|---|---|---|---|---|---|
| PY-Blauw | #1A3580 | 26 53 128 | 100 83 0 17 | 5002 | `color.blue.700` |
| PY-Aqua | #32B9CD | 50 185 205 | 69 0 21 0 | RAL Design 220 70 35 | `color.aqua.500` |
| PY-Oranje | #F08300 | 240 131 0 | 0 57 100 0 | 2003 | `color.orange.500` |
| PY-Diep | #0D142E | 13 20 46 | 100 83 0 80 | 5004 | `color.blue.900` |
| PY-Grijs | #AEAEAE | 174 174 174 | 0 0 0 42 | 9006 | `color.neutral.400` |
| PY-Zwart | #1D1D1B | 29 29 27 | 0 0 0 100 | 9005 | `color.neutral.900` |
| Wit | #FFFFFF | 255 255 255 | 0 0 0 0 | 9016 | `color.neutral.0` |

Pantone en folie per kleur staan in hoofdstuk 3, Kleur, onder Productie. Hoe die keuzes gemeten zijn, staat in 14.4.

**Maten en tijd**

| Groep | Waarden |
|---|---|
| Ruimte op scherm | 0, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 px (`space.0` tot `space.10`) |
| Hoeken | 0, 4, 8, 16, 24 px en pil (`radius.none` tot `radius.pill`) |
| Beweging | 120, 200, 320 en 600 ms (`duration.fast` tot `duration.expressive`) |
| Formaat | eenheid u = korte zijde gedeeld door 20; marge 2u, tussenruimte 1u |
| Letter | Ubuntu Sans (variabel), terugval Ubuntu, daarna de systeemletter. Drukwerk in punten: groep `print-type` |

**Contrast.** Elk kleurpaar voor tekst haalt WCAG 2.2 AA, in licht en donker. De volledige lijst met berekende waarden staat in `brand-2027/tokens/contrast.md`. Een paar voorbeelden: PY-Blauw op wit 11,26:1, wit op PY-Diep 18,16:1, PY-Diep op PY-Aqua 7,74:1, PY-Diep op PY-Oranje 6,87:1.

### 14.2 Bestanden

| Wat | Waar |
|---|---|
| Deze gids (bron) | `brand-2027/03-guide/volledig/ParkingYou-huisstijl-2027.md` |
| Korte gids als pdf | `brand-2027/03-guide/kort/ParkingYou-huisstijl-2027-kort.pdf` |
| Basisregels (core spec), met alle besluiten | `brand-2027/02-build/core-spec.md` |
| Tokens | `brand-2027/tokens/tokens.json`, `tokens.css`, `contrast.md` |
| Logo's | `brand-2027/02-build/kit/assets/logo-*.svg`: liggend, staand, beeldmerk, woordmerk; kleur, navy, wit, zwart en reverse |
| De parkeerders | `brand-2027/02-build/kit/assets/figure-*-navy.svg` en `-white.svg`, gespiegeld met `-flip` |
| Stem, bubbel en pijl | `arc.svg`, `bubble.svg`, `arrow-plain-*.svg`, `arrow-downleft-*.svg` in dezelfde map |
| Letter | `brand-2027/fonts/`: Ubuntu Sans, met de Ubuntu Font Licence. Gratis, ook voor drukwerk, borden en apps |
| Foto's | `brand-2027/02-build/kit/photos/`: eigen locatiefoto's. Kentekens zijn onleesbaar gemaakt |
| Figuren in deze gids | `brand-2027/02-build/<hoofdstuk>/figures/`, elk als HTML en PNG |

Alles van deze vernieuwing staat in de map `brand-2027` van PY-ASSETS. Oudere bestanden daarbuiten zijn niet aangepast en blijven bestaan.

### 14.3 Contact

Vragen over de huisstijl, een nieuwe waarde nodig, of twijfel over een toepassing? Neem contact op met de merkbeheerder.

| | |
|---|---|
| Merkbeheerder | [naam] |
| E-mail | [e-mailadres] |
| Website | parkingyou.nl |

Leg een nieuwe uiting voor je hem drukt of plaatst even voor aan de merkbeheerder. Bij borden in de garage altijd eerst een proefbord.
