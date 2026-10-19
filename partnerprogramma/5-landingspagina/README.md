# 5. Landingspagina parkingyou.nl/partners

Mobiel-eerst prototype (HTML, CSS, vanilla JS, geen dependencies, geen externe requests) voor de nieuwe Payload-site.
Het is een ontwerp dat blok voor blok over te nemen is; het is zelf geen Payload-code.

```
python3 -I partnerprogramma/5-landingspagina/vul.py      # template.html + teksten.json + data/ -> export/index.html
node partnerprogramma/5-landingspagina/test-rekenhulp.js # test van de rekenformule
```

Open `export/index.html` direct in de browser (werkt via file://). Screenshots op 390 en 1280 breed staan in `export/screenshots/`.

## Bestanden

| Bestand | Wat |
|---|---|
| `template.html` | Pagina met `{{sleutel}}`-velden en `{{@fragment}}`-blokken. Elke sectie heeft `data-block="..."`. |
| `teksten.json` | **Enige tekstbron.** Alles tussen [haken] is een placeholder en krijgt in beeld een oranje omlijning. |
| `teksten-landingspagina.md` | Brontekst (vervanger van het ontbrekende bestand), letterlijk; `teksten.json` volgt dit bestand. |
| `vul.py` | Vult de template uit `teksten.json` en `../data/locaties.json` en `../data/partnerprogramma.json`. |
| `stijl.css` | Kleuren als custom properties uit `tokens.json` (PY-Blauw, PY-Aqua, PY-Oranje, PY-Grijs, PY-Zwart), Ubuntu. |
| `rekenhulp-logica.js` | De formule als pure functie, zonder DOM (werkt in browser en node). |
| `pagina.js` | DOM voor de rekenhulp en validatie van het formulier. |
| `test-rekenhulp.js` | Test van de formule, afronding, opmaak en de grenzen. |
| `assets/` | Ubuntu (Regular, Medium, Bold, Latin-subset als woff, licentie erbij), logo en beeldmerk uit `svg/atom/`. |

## Teksten

Alle tekst staat in `teksten.json`. Bijna alles komt letterlijk uit `teksten-landingspagina.md` (naast dit bestand).
Dat md-bestand is een **vervanger**: het stond al in het Claude Doc "Partnerprogramma ParkingYou: teksten en documenten" en is overgenomen omdat het losse bestand uit de brief niet beschikbaar was.
Komt het echte bestand er, vergelijk het dan met `teksten.json`, pas de waarden aan en draai `vul.py`.

Uit het md-bestand: paginatitel en metabeschrijving, hero (kop, tekst, knop), de drie stappen Aanmelden, Delen en Verdienen (de landingspagina heeft eigen stappen, niet die van de one-pager),
voor wie (de opsomming is in zes items gesplitst, de woorden zijn letterlijk, "in de buurt van een ParkingYou-garage." staat eronder), de commissietabel met Plus en Wat het u kost,
de labels en disclaimer van de rekenhulp, de zes veelgestelde vragen, de soorten bedrijf, de bezoekersklassen en de bevestiging "Bedankt! We bellen u binnen twee werkdagen."
De vier hoofdletters aan het begin van keuzes (Tot 50, Theater/bioscoop, enzovoort) zijn de enige aanpassing aan de bron.

Gewone UI-teksten die niet in de bron staan en dus uit `teksten.json` zelf komen: de sectiekoppen "Voor wie", "Commissie", "Rekenhulp", "Veelgestelde vragen" en "Aanmelden"; "Aanbevolen" bij Actief;
het label "Garage" in de rekenhulp (nodig omdat de gemiddelde boeking per locatie verschilt); de voorleesteksten `rekenhulp.waarde_*`; "Maak een keuze", "(optioneel)", de verzendknop "Versturen" en alle `meldingen.*`.

**Nog open (placeholder, oranje omlijnd in beeld):**

| Sleutel | Waarom |
|---|---|
| `formulier.url_voorwaarden`, `formulier.url_privacy` | links in het vinkje; de bron noemt ze niet |
| `formulier.endpoint` | waar het formulier naartoe post |
| `rekenhulp.intro` | een intro bij de rekenhulp staat niet in de bron; laat leeg of vul in |
| `rekenhulp.placeholder_boeking` | zichtbaar zolang `gemiddelde_boeking_eur` in `data/locaties.json` `null` is; verdwijnt vanzelf zodra die is ingevuld |

De bron noemt "een kop en intro per blok" als niet geleverd. Voor wie, voor wie-intro en formulier-intro zijn daarom vervallen (er is geen intro), de overige koppen zijn UI-labels zoals hierboven.

## Rekenhulp

Commissie per maand = bezoekers met auto x deel dat reserveert x gemiddelde boeking x percentage.

* Schuif bezoekers met de auto per maand: 10 tot 5.000, stap 10, standaard 200. Schuif deel dat via uw link reserveert: 5 tot 60%, stap 1, standaard 20%. Niveau: Basis 4%, Actief 6% (standaard), Top 9%.
* De gemiddelde boeking staat per locatie vast (`data/locaties.json`). Omdat die per locatie verschilt heeft de rekenhulp een keuze voor de garage; dat is een invoer die niet in de brief staat.
* Uitkomst: "Indicatie: €x per maand, €y per jaar." met daaronder "Dit is een rekenvoorbeeld, geen garantie." Hele euro's, nl-NL opmaak. Het jaarbedrag is de afgeronde maand keer 12, zodat de twee getallen op de pagina bij elkaar passen.
* Zolang `gemiddelde_boeking_eur` `null` is staat op de plek van het bedrag de placeholder.
* Toegankelijk: echte labels, `aria-valuetext` op de schuiven, pijltjes, Home en End werken, de uitkomst wordt na een korte pauze voorgelezen via een `aria-live` regio.
* De grenzen staan zowel in `rekenhulp-logica.js` (`LIMIETEN`) als in `vul.py` (`LIMIETEN`); pas ze op beide plekken aan.

## Aanmeldformulier

Velden volgens de bron: bedrijfsnaam, KvK-nummer (8 cijfers), soort bedrijf (acht keuzes), bij welke garage, naam contactpersoon, e-mail, telefoon en het vinkje akkoord met voorwaarden en privacyverklaring zijn verplicht;
functie, bezoekers met de auto per maand (keuzelijst met vier klassen) en opmerking zijn optioneel.
Validatie in de browser met Nederlandse meldingen per veld, een samenvatting, focus naar het eerste foutieve veld en `aria-invalid`/`aria-describedby`.
Het prototype verstuurt niets: bij een geldig formulier komt de bevestiging en gaat er een `partner-aanmelding` event af met `detail.endpoint` en `detail.gegevens`. `data-endpoint` toont de placeholder `[endpoint]`.

## Mapping naar Payload (payload-website-starter)

Die repo stond niet in scope; er is niets naartoe geschreven. Voorstel per `data-block`:

| `data-block` | Payload-blok | Velden |
|---|---|---|
| `hero` | Hero | kop, tekst, knop (label "Word partner", link `#aanmelden`) |
| `zo-werkt-het` | Stappen | kop, `stappen[]` (kop, tekst; volgnummer automatisch) |
| `voor-wie` | Kaarten | kop, `items[]` (kop), slotregel |
| `commissietabel` | Tabel | kop, `rijen[]` (niveau, omschrijving, percentage, aanbevolen ja/nee), twee tekstregels (Plus, Wat het u kost) |
| `rekenhulp` | Rekenhulp | kop, intro (optioneel), labels, disclaimer; locaties (naam, gemiddelde boeking) uit een collectie `Locaties`; niveaus en percentages uit globals |
| `veelgestelde-vragen` | FAQ | kop, `items[]` (vraag, antwoord) |
| `aanmeldformulier` | Formulier (form-builder plugin) | de tien velden en het vinkje hierboven, bevestigingstekst, redirect optioneel |

De rekenlogica (`rekenhulp-logica.js`) is framework-vrij en kan ongewijzigd in een client component of als losse module.

## Controle

Gecontroleerd in Chromium op 390 en 1280 breed (ook met de echte teksten): geen console-fouten, geen externe requests, geen horizontale scroll, Ubuntu laadt.
Contrast: navy op wit en navy op aqua (knop) ruim boven AA; aqua staat alleen op navy of als vlak, niet als tekst op wit.
Nog niet getest met een echte schermlezer.
