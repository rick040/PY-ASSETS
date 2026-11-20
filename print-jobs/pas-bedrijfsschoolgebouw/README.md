# Toegangspas Bedrijfsschoolgebouw

Toegangspas voor stadionmedewerkers op wedstrijddagen, in de stijl van de Philips Stadion-pas. Geen parkeerabonnement.

* Formaat: ISO CR80, 85,6 x 54 mm, 3 mm afloop rondom (afgeronde hoek 3,18 mm staat als verborgen hulplijn in `guides`). Beide kanten liggend.
* Beide kanten: verloop, voetbal- en sterrenpatroon, witte lijn met Operated by parkingyou en het Philips Stadion-logo op dezelfde plek, uit `py-atom-illustration-card-pas`. Het dakje boven de P is weggelaten.
* Voorkant: grote P, "Toegangspas" (aqua), "Bedrijfsschoolgebouw" (wit, bold).
* Achterkant: "Toegangspas" en "Bedrijfsschoolgebouw" links boven, kleine P rechts boven, wit vlak met barcode ITF `995840000972914286` (smalle streep 0,36 mm, 54,9 x 12 mm) en nummer `972914286`, daaronder "Alleen voor stadionmedewerkers op wedstrijddagen".

| Bestand | Wat |
|---|---|
| `pas-bedrijfsschoolgebouw-voorkant.svg` / `.pdf` | Voorkant, 91,6 x 60 mm incl. afloop |
| `pas-bedrijfsschoolgebouw-achterkant.svg` / `.pdf` | Achterkant, 91,6 x 60 mm incl. afloop |
| `build.py` | Generator; teksten staan bovenin (`LABEL`, `LOCATION`, `USAGE`), barcode komt uit `../psv-parkeerabonnement/build.py` |

Let op:
* Het Philips Stadion-logo komt uit de terminalsticker (third-party, reference only). Gebruik voor de definitieve druk het officiële logobestand.
* De barcode zit op een andere plek en is groter dan op de oude staande kaart: eerst een proefdruk testen bij de lezer.
* Het witte vlak rond de barcode is de quiet zone; niet verkleinen of met kleur bedrukken.
