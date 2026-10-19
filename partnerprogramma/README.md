# Partnerprogramma: visuals

Visuals voor het ParkingYou-partnerprogramma (pilot Hofplein `HOF` en Artis (Plantage) `PLA`). Alles volgt de huisstijl uit de rest van de repo:
tokens uit `tokens.json`, Ubuntu uit `fonts/`, logo's en figuren uit `svg/`. Er is niets nieuws gedefinieerd waar al een token, atom of component voor was.

## Eén commando

```
python3 -I partnerprogramma/build.py                         # alles
python3 -I partnerprogramma/build.py --locatie HOF           # one-pager en alle partners van Hofplein
python3 -I partnerprogramma/build.py --partner HOF-HOTELVB   # kaarten en posts van één partner
python3 -I partnerprogramma/build.py --only kaart,social     # alleen deze visuals
python3 -I partnerprogramma/test.py                          # alleen de controles
```
Visuals: `onepager`, `kaart`, `partnerlogo`, `social`, `landingspagina`, `mailheader`. `build.py` draait daarna `test.py`.

Nodig: Python 3 met `pymupdf cairosvg fonttools segno zxing-cpp opencv-python-headless Pillow numpy`, en de Ubuntu-fonts uit `fonts/` geinstalleerd
(`cp fonts/*.ttf ~/.fonts && fc-cache -f`). Voor de landingspagina-test ook `node`.

## Opbouw

| Map | Visual | Bron | Export |
|---|---|---|---|
| `1-onepager/` | A4 staand, per locatie | `template.svg` | `export/<LOC>/`: `-druk.pdf` (216 x 303 mm met 3 mm afloop, TrimBox en BleedBox gezet), `-mail.png` (1240 px breed, zonder afloop), `.svg` |
| `2-balie-qr-kaart/` | A6 en tafelstandaard, per partner | `template-a6.svg`, `template-tafelstandaard.svg` | `export/<CODE>/`: PDF met 3 mm afloop; `qr-test-rapport.md` |
| `3-partnerlogo/` | badge liggend en staand, licht en donker | `ontwerp.py` (de SVG's zelf in `export/`) | SVG en transparante PNG; `formaatregel.md`; `overzicht.png` |
| `4-social/` | twee posts in drie formaten, per partner | `template-<post>-<formaat>.svg` | `export/<CODE>/`: 6 PNG's |
| `5-landingspagina/` | prototype voor parkingyou.nl/partners | `template.html`, `teksten.json` | `export/index.html`; zie de eigen README |
| `6-mailheader/` | 600 px banner | `template.svg` | `export/`: 600 en 1200 px (2x) |

Per visual met variabelen: `template.svg` (gewone SVG met `{velden}`) plus `vul.py` (leest `data/`, vult, exporteert).
`ontwerp.py` schrijft de template en is alleen nodig om het ontwerp aan te passen; `template.svg` is de bron. Een veld als `{bedrijf}` vult `vul.py`;
tekstblokken met `data-flow` worden bij het vullen afgebroken en passend gemaakt (cairosvg breekt zelf geen regels af); `data-qr` wordt een QR-code.
`ppkit/` is de gedeelde kit.

## Gegevens (`data/`)

`locaties.json`, `partnerprogramma.json` en `partners.csv`; zie `data/README.md`. `{afstand}` is berekend uit `afstand_m` (80 m per minuut, naar boven afgerond).
De QR-code wijst naar `https://` plus `link`.

## Wat nog moet worden aangeleverd (placeholders blijven zichtbaar)

* `[bedrag]` en `[uitkomst]` in het rekenvoorbeeld: `gemiddelde_boeking_eur` per locatie in `data/locaties.json`. In het brondocument staat €15 als voorbeeld; dat is bewust niet overgenomen.
* `[naam]`, `[functie]`, `[telefoon]`, `[e-mail]` bij Contact: `contact` in `data/partnerprogramma.json`.
* Echte partners in `data/partners.csv` (nu twee voorbeeldpartners met verzonnen afstanden).
* Landingspagina: links naar voorwaarden en privacyverklaring en het formulier-endpoint; zie `5-landingspagina/README.md`.

Placeholders in `[haken]` krijgen automatisch een oranje markering in de exports.

## Bron van de teksten

`teksten-landingspagina.md` uit de brief was niet beschikbaar. De teksten komen uit het Claude Doc "Partnerprogramma ParkingYou: teksten en documenten":
tab Werving (one-pager en landingspagina) en tab Partnerkit (balie- en QR-kaart, social posts en captions). `5-landingspagina/teksten-landingspagina.md` is daar een letterlijke kopie van en vervangt het ontbrekende bestand.

## Waar brief en brondocument verschillen

| Plek | Brief | Brondocument | Gekozen |
|---|---|---|---|
| One-pager, stap 2 | "in onze garage, vlak bij u" | "in onze garage, op {afstand} lopen" | brief; een one-pager is per locatie en kent geen afstand per partner |
| One-pager, niveau Top | "Actief plus een vaste afspraak" | "Actief, plus een vaste afspraak" | brondocument (alleen een komma) |
| One-pager, tabel | geen kolomkoppen | Niveau, Wat u doet, Commissie | brondocument |
| Rekenvoorbeeld | zichtbare placeholder | €15, €90, "ruim €1.000" als voorbeeld | placeholder |
| Rekenhulp, disclaimer | "Dit is een rekenvoorbeeld, geen garantie." | plus "De echte commissie hangt af van hoeveel gasten reserveren." | brondocument |

## Keuzes buiten de brief

* **Kleur:** exports zijn RGB met de tokenwaarden. Voor druk: PY-Blauw is CMYK 100/83/0/17 (zie `tokens.json`); laat de drukker of Acrobat converteren, of lever CMYK aan.
* **QR:** foutcorrectie Q (boven de gevraagde M), code 30 mm (minimaal 25), rustzone 4 modules op een witte plaat, donkere modules. Niet omgekeerd, anders dan de Maashaven-pyloon; omgekeerde codes falen op oudere scanners.
* **Tafelstandaard:** gelezen als tentkaart: een vel van 105 x 296 mm, vouw op 148 mm, twee A6-kanten (de bovenste staat op zijn kop zodat beide kanten rechtop staan). Vouwmerken staan in de afloop.
* **Partnerlogo in de posts en de mailheader:** de badge uit `3-partnerlogo` (donker, liggend). Het eigen logo van de partner is niet geplaatst.
* **"Licht" en "donker"** gaan over de achtergrond waarop de badge staat, niet over de badge zelf.
* **Eén woord toegevoegd:** het label "Aanbevolen" bij Actief. Verder zijn de teksten letterlijk; alleen hoofdletters aan het begin van tabelcellen en regels zijn gezet en de contactgegevens staan op aparte regels.
* **Artis (Plantage):** in `locaties.json` staat `locatie` als "Artis (Plantage)", dus de tekst luidt "ParkingYou Artis (Plantage)". Pas daar aan als dit "Artis" moet zijn.
* **Captions** bij de posts komen uit het brondocument (`4-social/captions.json`) en staan per partner als `.txt` naast de posts. De caption van de partnerpost eindigt op "Link in bio"; dat past niet bij LinkedIn.
* **Rekenhulp:** extra keuze voor de garage, omdat de gemiddelde boeking per locatie verschilt.
* **Drukcontrole:** exports hebben geen snijmerken; BleedBox en TrimBox zijn in de PDF gezet.
