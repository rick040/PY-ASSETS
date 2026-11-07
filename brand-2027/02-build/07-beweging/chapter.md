# Beweging

Beweging helpt je zien wat er verandert. Meer hoeft het niet te doen. We hebben twee soorten: productief voor alles in de interface, en expressief voor de bubbel op een paar merkmomenten. Alle waarden komen uit de tokens.

## Twee soorten beweging

**Productief.** Alle UI-beweging: een knop die je indrukt, een sheet die opent, een pagina die wisselt. Kort en rustig, 120 tot 320 ms, met `easing.standard`, `easing.enter` of `easing.exit`. Geen stuiter, geen overshoot.

**Expressief.** Alleen de bubbel, en alleen op merkmomenten: de opening en het einde van een reel, het opstartscherm van de app en een bevestiging (betaald, gereserveerd). 600 ms met `easing.bubble`, die een kleine overshoot heeft. Expressief is zeldzaam; daardoor valt het op.

## De tokens

| Token | Waarde | Gebruik |
|---|---|---|
| `duration.fast` | 120 ms | hover, druk, kleine statuswissel |
| `duration.moderate` | 200 ms | uitklappen, sheet in |
| `duration.slow` | 320 ms | paginawissel |
| `duration.expressive` | 600 ms | alleen de bubbel |
| `easing.standard` | cubic-bezier(0.2, 0, 0, 1) | standaard voor UI |
| `easing.enter` | cubic-bezier(0, 0, 0, 1) | iets komt binnen |
| `easing.exit` | cubic-bezier(0.3, 0, 1, 1) | iets gaat weg |
| `easing.bubble` | cubic-bezier(0.34, 1.3, 0.64, 1) | de bubbelpop |

![Principes, duur en easing](figures/tokens.png)

## De bubbelpop

De bubbel popt in: hij schaalt van 0,9 naar 1 in 600 ms met `easing.bubble`. De punt komt als laatste tot rust.

Zo bouw je hem:

1. **Schaal** van 0,9 naar 1, vanuit het midden van de cirkel, 600 ms, `easing.bubble`.
2. **Punt.** De bubbel start 45 graden gedraaid (één wegwijsstap) en draait in dezelfde 600 ms terug naar 0, ook met `easing.bubble`, rond het midden van de cirkel. Omdat de cirkel rond is, beweegt dan alleen de punt. Door de overshoot zwaait de punt ongeveer 1,3 graden door en valt dan terug. Dat is het "tot rust komen".
3. **Dekking** van 0 naar 1 in 120 ms (`duration.fast`, `easing.enter`), aan het begin.
4. **Inhoud** (cijfer, prijs, pictogram) schaalt mee maar draait niet mee. Inhoud blijft altijd rechtop.

Bij 300 ms is de bubbel praktisch op maat, bij 400 ms schiet hij 0,3 procent door, bij 600 ms staat hij stil. Je ziet de pop vooral aan de punt.

![De bubbelpop als storyboard](figures/bubbel-pop.png)

## Reduced motion

Als iemand in zijn systeem minder beweging heeft gekozen (`prefers-reduced-motion`), dan:

- **UI**: alle duurtokens worden 0 ms. Een sheet staat er meteen. Dat regelt `tokens.css` al. Laadindicatoren mogen blijven draaien; dat is informatie.
- **Bubbel**: geen schaal en geen draaiende punt. Alleen dekking van 0 naar 1 in 120 ms.
- **Video en carrousels** spelen niet vanzelf.

Let op: `tokens.css` zet onder reduced motion ook `duration.fast` op 0. De fade van 120 ms kan dus niet uit dat token komen. Zie Voorgestelde waarden.

Los van reduced motion geldt: alles wat langer dan 5 seconden vanzelf beweegt (video, carrousel, geanimeerde banner) krijgt een zichtbare pauzeknop van minstens 44 x 44 px.

![Reduced motion: fade in plaats van pop](figures/reduced-motion.png)

## Reels

- **Eén idee per reel.** Niet drie aanbiedingen achter elkaar.
- **Lengte** 6 tot 15 seconden.
- **Opbouw**: de bubbel popt in (0,6 s), dan de boodschap in beeld en tekst, dan de eindkaart.
- **Eindkaart** 1,5 seconde: logo gestapeld, stil, op PY-Blauw, met het webadres eronder.
- **Ondertitels** altijd aan. Kapitaalhoogte 0,4u (21,6 px op 1080 breed), wit op PY-Blauw of PY-Blauw op wit. Onderaan de kernzone, nooit over een drukke plek in de foto.
- **Vrije zones**: boven 250 px en onder 340 px geen belangrijke inhoud (zie Grid en layout).
- **Kleur**: oranje alleen bij een prijs of de actie. Geen verloop over een foto.

Bestaande Remotion-verhalen in `remotion/` lezen nog het oude tokenbestand, gebruiken het driestopsverloop en Ubuntu in plaats van Ubuntu Sans. Bij de volgende versie gaan ze over op `tokens.json` van 2027, deze opbouw en de eindkaart.

![Opbouw van een reel van 10 seconden](figures/reel-structuur.png)

## Overgangen in de interface

| Wat | Duur | Easing |
|---|---|---|
| Knop hover en druk | `duration.fast` | `easing.standard` |
| Chip, schakelaar, vinkje | `duration.fast` | `easing.standard` |
| Uitklappen en inklappen | `duration.moderate` | `easing.standard` |
| Sheet of dialoog in | `duration.moderate` | `easing.enter` |
| Sheet of dialoog uit | `duration.fast` | `easing.exit` |
| Paginawissel | `duration.slow` | `easing.standard` |
| Bevestiging (betaald) | `duration.expressive` | `easing.bubble` |

Beweeg alleen wat verandert, één ding tegelijk. Wat van onder komt, gaat naar onder weg. Een knop verandert van kleur bij hover en druk, niet van maat. Schaduw (`shadow.1` tot `shadow.3`) mag op schermlagen, nooit op de bubbel.

![Bottom sheet: storyboard en tabel](figures/ui-overgangen.png)

## Do's en don'ts

- **Do:** UI-beweging altijd uit de tokens, nooit een losse waarde in code.
- **Do:** de bubbelpop alleen op merkmomenten: reel open en dicht, splash, bevestiging.
- **Do:** test elke animatie met reduced motion aan.
- **Do:** ondertitels in elke reel, ook als er geen gesproken tekst is.
- **Don't:** overshoot of stuiter in de UI. Die hoort bij de bubbel.
- **Don't:** de bubbel laten draaien, knipperen of steeds opnieuw poppen.
- **Don't:** autoplay langer dan 5 s zonder pauzeknop.
- **Don't:** beweging in bewegwijzering of op schermen in de garage die de aandacht van bestuurders trekt.
- **Don't:** reels langer dan 15 s of met meer dan één boodschap.

## Voorgestelde waarden

Goedgekeurd door de creative director: zie besluiten D16 en D19 in de core spec. Waar de core spec iets anders zegt, geldt de core spec.

Niet gebruiken in finals tot de creative director ze goedkeurt.

| Waarde | Voorstel | Reden |
|---|---|---|
| Startstand punt | 45 graden gedraaid, terug naar 0 in 600 ms met `easing.bubble`, rond het midden van de cirkel | Core-spec zegt "de punt komt als laatste tot rust" maar niet hoe. Zo blijft de vorm heel (alleen draaien en schalen) en gebruikt het de bestaande stap van 45 graden. |
| Dekking tijdens de pop | 0 naar 1 in `duration.fast`, `easing.enter` | Anders staat de bubbel op 0 ms al zichtbaar op 0,9. |
| Fade onder reduced motion | nieuw token, bijvoorbeeld `duration.fade-reduced` = 120 ms, dat niet op 0 gaat | `tokens.css` zet `duration.fast` op 0 onder reduced motion; de 120 ms uit core-spec moet een eigen token krijgen. Generator aanpassen. |
| Ondertitelpositie reel | onderaan de kernzone, regel 26,5u tot 29u | Vaste plek in het template, boven de vrije zone van 340 px. |
| Eindkaart | gestapeld logo, 6u hoog, gecentreerd, webadres eronder in regular | Core-spec noemt de duur maar niet de inhoud. |
| Lengte opening | bubbelpop in de eerste 0,6 s van de reel | Volgt `duration.expressive`; zo is de opening altijd even lang. |
