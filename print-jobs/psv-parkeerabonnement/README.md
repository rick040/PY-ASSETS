# Parkeerabonnement PSV: barcode en A5

Barcode gedecodeerd uit een foto van de fysieke abonnementskaart.

* Symbologie: ITF (Interleaved 2 of 5), geen extra controlecijfer
* Waarde in de barcode: `995840000972914286` (18 cijfers)
* Op de kaart gedrukt: alleen de laatste 9 cijfers, `972914286`

| Bestand | Wat |
|---|---|
| `barcode-itf-995840000972914286.svg` | Alleen de streepjes, mm-eenheden, smalle streep 0,5 mm, breed:smal 2,5:1, witte quiet zone (10x smal) aan beide kanten zit erin. Schaal proportioneel. |
| `barcode-itf-995840000972914286-met-nummer.svg` | Idem met het nummer eronder (Ubuntu Medium). |
| `parkeerabonnement-a5.svg` | A5 staand (148 x 210 mm) met 3 mm afloop, kaartontwerp opgeschaald. Barcode 84 mm breed. Live Ubuntu-tekst. |
| `parkeerabonnement-a5.pdf` | Printklare PDF van de A5 (154 x 216 mm incl. afloop, fonts ingesloten). |
| `build.py` | Generator. `python3 -I print-jobs/psv-parkeerabonnement/build.py` |

Controle: beide renders zijn teruggelezen met zxing-cpp en geven `995840000972914286`.

Printtips: streepjes altijd 100 procent zwart (K100), niet verkleinen onder ongeveer 80 procent van de kaartmaat, quiet zone wit laten, niet uitrekken in één richting.
