# Bord slagboom vergunninghouders (nieuw ontwerp)

Vervangt het generieke bord "P Private parking / Parking only for permit holders" op de handslagboom.

| Bestand | Wat |
|---|---|
| `template.svg` | Drukbestand: 1000 x 125 mm plus 3 mm afloop, live Ubuntu-tekst, snijcontour (ThruCut, hoekradius 8 mm) |
| `proof.pdf` | Zelfde ontwerp als PDF-proef |
| `preview.png` | Voorbeeld zoals het bord eruit komt te zien |
| `mockup.jpg` | Het nieuwe bord op de foto van de slagboom |
| `spec.json` | Maten, variabelen, gebruikte bouwstenen |
| `build.py` | Bouwt alles opnieuw: `python3 -I designs/py-app-sign-slagboom-vergunninghouders/build.py` |

Opbouw: PY-Blauw vlak, witte P met dak, aqua scheidingslijnen, "Alleen vergunninghouders" in Ubuntu Bold wit,
"Permit holders only" in Ubuntu Regular PY-Aqua, wit wegsleep-pictogram (nieuw getekend), wit liggend logo.

Open punten voor bestellen:
* Het formaat 1000 x 125 mm is geschat op de foto (verhouding ca. 8 : 1). Meet het oude bord en pas `TRIM` in `build.py` aan.
* Montagegaten staan er niet in (hangt af van de beugel).
* Enkel- of dubbelzijdig, en materiaal (voorstel: 3 mm aluminium dibond, bedrukt en gelamineerd).
