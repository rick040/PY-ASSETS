# Parkeerpas Bedrijfsschoolgebouw

Pas in de stijl van de Philips Stadion-pas, met de barcode van het parkeerabonnement.

* Formaat: ISO CR80, 85,6 x 54 mm, 3 mm afloop rondom (afgeronde hoek 3,18 mm staat als verborgen hulplijn in `guides`).
* Voorkant (liggend): gebouwd uit `py-atom-illustration-card-pas` (verloop, voetbal- en sterrenpatroon, P onder dak, Operated by parkingyou, Philips Stadion-logo), opgeschaald, P-icoon op 85 procent, plus de locatienaam als live Ubuntu-tekst.
* Achterkant (staand): zelfde opbouw als de fysieke abonnementskaart. Barcode ITF `995840000972914286` op dezelfde plek en maat als op de echte kaart (ongeveer 39,7 x 16,7 mm, smalle streep 0,26 mm), nummer `972914286` eronder.

| Bestand | Wat |
|---|---|
| `pas-bedrijfsschoolgebouw-voorkant.svg` / `.pdf` | Voorkant, 91,6 x 60 mm incl. afloop |
| `pas-bedrijfsschoolgebouw-achterkant.svg` / `.pdf` | Achterkant, 60 x 91,6 mm incl. afloop |
| `build.py` | Generator, gebruikt de barcode uit `../psv-parkeerabonnement/build.py` |

Let op:
* Het Philips Stadion-logo komt uit de terminalsticker (third-party, reference only). Gebruik voor de definitieve druk het officiële logobestand.
* Voorkant is liggend, achterkant staand. Bij dubbelzijdig drukken de achterkant 90 graden draaien.
* Barcode niet verkleinen; de maat is gelijk aan de bestaande kaart zodat de lezer hem pakt.
