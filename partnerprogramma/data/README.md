# Data

Een bron per soort gegeven. Alle visuals lezen hieruit; niets staat in een template.

| Bestand | Wat | Leeg betekent |
|---|---|---|
| `locaties.json` | per locatie: code, naam zoals in de tekst (`locatie`), `gemiddelde_boeking_eur` | `null`: in de one-pager staat `[bedrag]` en `[uitkomst]` in beeld |
| `partnerprogramma.json` | aantal locaties, loopsnelheid, niveaus en percentages, rekenvoorbeeld, contactgegevens | `null` bij contact: `[naam]`, `[functie]`, `[telefoon]`, `[e-mail]` blijven zichtbaar |
| `partners.csv` | per partner: `code`, `bedrijf`, `locatie` (HOF of PLA), `afstand_m`, `link` | n.v.t. |

De twee regels in `partners.csv` zijn voorbeeldpartners (Hotel Voorbeeld, Theater Voorbeeld) om de kaarten en posts te kunnen testen.
Vervang ze door de echte partners; de afstanden zijn verzonnen.

`{afstand}` wordt berekend uit `afstand_m`: 80 meter per minuut, naar boven afgerond, "1 minuut" of "N minuten".
De QR-code wijst naar `https://` plus de waarde in `link`.
