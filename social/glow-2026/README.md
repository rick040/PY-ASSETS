# GLOW 2026 social posts

Feed posts, carrousel, stories and reel cards for the ParkingYou x Glow Eindhoven campaign (7 t/m 14 november 2026).
Copy and formats come from the Notion page "GLOW 2026" (Social Posts database). Built only from elements in this repo.

Rebuild: `python3 -I social/glow-2026/build.py` (needs playwright with Chromium and the Ubuntu fonts from `fonts/`).
Every frame is written as an editable SVG (live Ubuntu text) and a PNG in `out/`.

## Files and when they run

| Bestand | Brief | Formaat | Fase |
|---|---|---|---|
| `post-b-hier-begint-glow` | Post B | 1080x1350 | Bekendheid 13-24 okt |
| `post-c-garage-die-je-niet-kent` | Post C | 1080x1350 | Bekendheid 13-24 okt |
| `story3-frame1..3` | Story 3 | 1080x1920 | Bekendheid 13-24 okt |
| `post-a-vijf-euro` | Post A | 1080x1350 | Reserveren 25 okt-6 nov |
| `post-d-geen-rondjes` | Post D | 1080x1350 | Reserveren 25 okt-6 nov |
| `post-e-carrousel-slide-1..5` | Post E | 1080x1350, 5 slides | Reserveren 25 okt-6 nov |
| `post-f-aftellen-nog-7..1` | Post F | 1080x1350, 1 per dag | 31 okt (nog 7) t/m 6 nov (nog 1) |
| `story1-frame1..3` | Story 1 | 1080x1920 | Reserveren |
| `story2-frame1..3-overlay` | Story 2 | 1080x1920, transparant | Reserveren, over eigen beelden |
| `story4-frame1-nog-7..1`, `story4-frame2` | Story 4 | 1080x1920 | Reserveren, 1 per dag |
| `story5-frame1`, `story5-frame2-<locatie>` | Story 5 | 1080x1920 | Live 7-14 nov, 16:00-20:00 |
| `reel-hook-overlay`, `reel-eindkaart` | Reel Light Brigade | 1080x1920 | Live, na de eerste avond |
| `post-g-night-card` | Post G | 1080x1350 | Retargeting vanaf 15 nov |

## Captions (uit de briefs)

**Post A** · Kop: Glow-parkeren vanaf €15 · CTA: Nu reserveren
Naar Glow? Reserveer je plek vooraf en je betaalt €15 in plaats van €20. Je plek staat klaar, je loopt zo de route op. Kost je een minuutje.

**Post B** · Kop: Parkeer waar Glow begint · CTA: Nu reserveren
Je avond begint niet bij het eerste kunstwerk. Hij begint bij je parkeerplek. Parkeer bij ParkingYou, stap uit en je staat zo op de route.

**Post C** · Kop: 5 garages dichtbij de route · CTA: Meer informatie
Midden in het centrum, vlak bij de Glow-route. En toch rijden de meeste mensen er langs. Jammer voor hen, fijn voor jou: plek genoeg.

**Post D** · Kop: Vaste plek tijdens Glow · CTA: Nu reserveren
Om 19:00 staat half Brabant in de rij voor dezelfde garage. Jij niet. Reserveer vooraf en rij zo naar binnen.

**Post E** · Kop: Glow zonder parkeerstress
Zo makkelijk kan het zijn. Reserveer vooraf bij ParkingYou en je hoeft alleen nog te genieten.

**Post F** · Kop: Reserveer je Glow-avond · CTA: Nu reserveren
Glow loopt van 7 tot en met 14 november. Vrijdag en zaterdag gaan het snelst. Regel je plek nu voor €15.

**Post G** · Kop: Activeer je Night Card · CTA: Aanmelden · Doelgroep: gereserveerd, geparkeerd of Night Card-pagina bezocht
Bedankt dat je met Glow bij ons parkeerde. Met je Night Card parkeer je nog 3 avonden gratis bij elke ParkingYou-locatie in Nederland. Ook in het weekend.

## Notes

* Stories are delivered as separate frames (one PNG per frame); upload them in order as a story sequence.
* Story 2 and the reel hook are transparent overlays for your own footage (dashboard shot, gimbal at the exit, Light Brigade). Text sits on a PY-Blauw panel at 85 percent so it reads on any shot.
* Story 5: only post the location versions on evenings when that garage really has room.
* Post C and Story 3 use a stylised route with pins, not a real map. Swap in a map or photo if you want exact positions.
* Post B and Story 3 frame 1 draw the projection as an illustration; a real evening photo of the projection on TD or DLL can replace it once it exists.
* The Night Card on Post G and the reel end card is a placeholder card built from brand elements. Replace it with the final Night Card design when that is printed.
* Background night tones `#0E1E4D` and `#060D24` are darkened PY-Blauw for the campaign only, not brand colours. All other colours are tokens from `tokens.json`.
* The GLOW logo is not used (third-party mark, reference only in this repo); "Glow" appears as plain text.
* CTA tag shows `parkingyou.nl`. Change the tag in `url_tag()` if the campaign gets its own landing page URL.
