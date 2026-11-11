# Bord slagboom vergunninghouders (nieuw ontwerp)

Vervangt het generieke bord "P Private parking / Parking only for permit holders" op de handslagboom.

| Bestand | Wat |
|---|---|
| `template.svg` | Drukbestand: 1000 x 200 mm plus 3 mm afloop, live Ubuntu-tekst, snijcontour (ThruCut, rechte hoeken), schroefposities als aparte laag `mounting-holes` (niet drukken) |
| `proof.pdf` | Zelfde ontwerp als PDF-proef |
| `preview.png` | Voorbeeld zoals het bord eruit komt te zien |
| `mockup.jpg` | Het nieuwe bord op de foto van de slagboom |
| `spec.json` | Maten, variabelen, gebruikte bouwstenen |
| `build.py` | Bouwt alles opnieuw: `python3 -I designs/py-app-sign-slagboom-vergunninghouders/build.py` |

Opbouw: PY-Blauw vlak, witte platte P (zonder dak, het is geen garage), aqua scheidingslijnen, "Alleen vergunninghouders" in Ubuntu Bold wit,
"Permit holders only" in Ubuntu Regular PY-Aqua, wit wegsleep-pictogram (nieuw getekend), wit liggend logo.
Het hele bord is PY-Blauw. Onderin (vanaf 146 mm) zit het bord met drie schroeven op de boom vast, dus daar staat geen tekst.

Open punten voor bestellen:
* Het formaat 1000 x 200 mm en de schroefposities (x 123, 555 en 917 mm, 164 mm vanaf boven) zijn geschat op de foto van de lege montageplaat. Meet ze op en pas `TRIM` en `HOLES` in `build.py` aan.
* Enkel- of dubbelzijdig, en materiaal (voorstel: 3 mm aluminium dibond, bedrukt en gelamineerd).
