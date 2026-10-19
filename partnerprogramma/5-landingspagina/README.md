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
| `vul.py` | Vult de template uit `teksten.json` en `../data/locaties.json` en `../data/partnerprogramma.json`. |
| `stijl.css` | Kleuren als custom properties uit `tokens.json` (PY-Blauw, PY-Aqua, PY-Oranje, PY-Grijs, PY-Zwart), Ubuntu. |
| `rekenhulp-logica.js` | De formule als pure functie, zonder DOM (werkt in browser en node). |
| `pagina.js` | DOM voor de rekenhulp en validatie van het formulier. |
| `test-rekenhulp.js` | Test van de formule, afronding, opmaak en de grenzen. |
| `assets/` | Ubuntu (Regular, Medium, Bold, Latin-subset als woff, licentie erbij), logo en beeldmerk uit `svg/atom/`. |

## Wat uit teksten-landingspagina.md moet komen

`teksten-landingspagina.md` was niet beschikbaar. Dit zijn de sleutels in `teksten.json` die nog placeholders zijn.
Vervang de waarde door de tekst uit het md-bestand (zonder haken) en draai `vul.py`. De rest staat letterlijk in de brief.

| Sleutel | Waar |
|---|---|
| `meta.titel`, `meta.beschrijving` | titel en beschrijving van de pagina |
| `hero.kop`, `hero.tekst` | hero |
| `voor_wie.kop`, `voor_wie.intro`, `voor_wie.items[].tekst` | voor wie (de vier kopjes Hotels, Theaters, Zalen, Restaurants komen uit de brief) |
| `rekenhulp.kop`, `rekenhulp.intro` | rekenhulp |
| `faq.kop`, `faq.items[].vraag`, `faq.items[].antwoord` | veelgestelde vragen (aantal items is vrij) |
| `formulier.kop`, `formulier.intro` | aanmeldformulier |
| `formulier.knop_verzenden`, `formulier.bevestiging` | verzendknop en bevestiging na verzenden |
| `formulier.keuze_leeg` | eerste regel in de keuzelijsten |
| `formulier.url_voorwaarden`, `formulier.url_privacy` | links in het vinkje |
| `formulier.endpoint` | waar het formulier naartoe post |

Eigen UI-teksten (niet uit de brief, graag nalopen): kolomkoppen van de tabel (`kolom_*`), "Aanbevolen", "Garage", `rekenhulp.waarde_*` (voorleestekst van de schuiven), de optie "Anders" bij soort bedrijf, "(optioneel)" en alle `meldingen.*`.
De placeholders in de rekenhulp-uitkomst ("[gemiddelde boeking per locatie]") verdwijnen vanzelf zodra `gemiddelde_boeking_eur` in `data/locaties.json` is ingevuld.

## Rekenhulp

Commissie per maand = bezoekers met auto x deel dat reserveert x gemiddelde boeking x percentage.

* Schuif bezoekers: 10 tot 5.000, stap 10, standaard 200. Schuif deel: 5 tot 60%, stap 1, standaard 20%. Niveau: Basis 4%, Actief 6% (standaard), Top 9%.
* De gemiddelde boeking staat per locatie vast (`data/locaties.json`). Omdat die per locatie verschilt heeft de rekenhulp een keuze voor de garage; dat is een invoer die niet in de brief staat.
* Uitkomst: "Indicatie: €x per maand, €y per jaar." met daaronder "Dit is een rekenvoorbeeld, geen garantie." Hele euro's, nl-NL opmaak. Het jaarbedrag is de afgeronde maand keer 12, zodat de twee getallen op de pagina bij elkaar passen.
* Zolang `gemiddelde_boeking_eur` `null` is staat op de plek van het bedrag de placeholder.
* Toegankelijk: echte labels, `aria-valuetext` op de schuiven, pijltjes, Home en End werken, de uitkomst wordt na een korte pauze voorgelezen via een `aria-live` regio.
* De grenzen staan zowel in `rekenhulp-logica.js` (`LIMIETEN`) als in `vul.py` (`LIMIETEN`); pas ze op beide plekken aan.

## Aanmeldformulier

Velden: bedrijfsnaam, KvK-nummer (8 cijfers), soort bedrijf, bij welke garage, naam, functie, e-mail, telefoon, bezoekers met de auto per maand, opmerking (optioneel), vinkje akkoord met voorwaarden en privacyverklaring.
Validatie in de browser met Nederlandse meldingen per veld, een samenvatting, focus naar het eerste foutieve veld en `aria-invalid`/`aria-describedby`.
Het prototype verstuurt niets: bij een geldig formulier komt de bevestiging en gaat er een `partner-aanmelding` event af met `detail.endpoint` en `detail.gegevens`. `data-endpoint` toont de placeholder `[endpoint]`.

## Mapping naar Payload (payload-website-starter)

Die repo stond niet in scope; er is niets naartoe geschreven. Voorstel per `data-block`:

| `data-block` | Payload-blok | Velden |
|---|---|---|
| `hero` | Hero | kop, tekst, knop (label "Word partner", link `#aanmelden`) |
| `zo-werkt-het` | Stappen | kop, `stappen[]` (tekst, volgnummer automatisch) |
| `voor-wie` | Kaarten | kop, intro, `items[]` (kop, tekst) |
| `commissietabel` | Tabel | kop, `rijen[]` (niveau, omschrijving, percentage, aanbevolen ja/nee), twee tekstregels (Plus, Wat het u kost) |
| `rekenhulp` | Rekenhulp | kop, intro, labels; locaties (naam, gemiddelde boeking) uit een collectie `Locaties`; niveaus en percentages uit globals |
| `veelgestelde-vragen` | FAQ | kop, `items[]` (vraag, antwoord) |
| `aanmeldformulier` | Formulier (form-builder plugin) | de elf velden hierboven, bevestigingstekst, redirect optioneel |

De rekenlogica (`rekenhulp-logica.js`) is framework-vrij en kan ongewijzigd in een client component of als losse module.

## Controle

Gecontroleerd in Chromium op 390 en 1280 breed: geen console-fouten, geen externe requests, geen horizontale scroll, Ubuntu laadt.
Contrast: navy op wit en navy op aqua (knop) ruim boven AA; aqua staat alleen op navy of als vlak, niet als tekst op wit.
Nog niet getest met een echte schermlezer.
