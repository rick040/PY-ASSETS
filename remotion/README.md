# Remotion: stories and location spots

Three general ParkingYou social media stories (1080x1920, 30 fps, 8 s) built with [Remotion](https://www.remotion.dev) from this library.
Brand colours and the verloop come from `../tokens.json`; logos, figures and shapes come from `../svg/atom/`; type is Ubuntu from `../fonts/`.
`npm run sync-assets` copies `svg/` and `fonts/` into `public/` (generated, not committed), so the library stays the single source of truth.

| Composition | Story | Copy taken from | Atoms used |
|---|---|---|---|
| `Story1-App` | Makkelijk parkeren vanuit je broekzak, scanning phone, CTA | `py-app-poster-app-a2` | logo-horizontal-white, illustration-phone-qr |
| `Story2-Shoppen` | Jouw dagje shoppen start hier!, walking then cheering shopper in a verloop bubble (white figure) | `py-app-poster-partner-a4` | logo-horizontal-color, logo-beeldmerk-watermark, shape-bubble-gradient, figure-bags-walk, figure-bags-cheer |
| `Story3-Tagline` | Voordelig parkeren zonder gedoe?, circle wipe to the logo and tagline | `py-app-brand-background-tagline`, `py-app-panel-campagne-hofplein` | logo-stacked-white |

The top 250 px and bottom 340 px are kept free of key content (Instagram and TikTok UI). Rendered files are in `out/`.

## Use

```bash
cd remotion
npm install
npm run studio     # live preview
npm run render     # all three to out/*.mp4
node scripts/render-all.mjs Story2-Shoppen   # one story
```

`render-all.mjs` uses a pre-installed Chromium in `/opt/pw-browsers` if present, or set `BROWSER_EXECUTABLE`.

## Notes

* This is a test: the copy is reused from the print files, no new claims or prices.
* The phone and QR in story 1 is the library illustration, not a working QR code.
* The verloop is the measured three-stop gradient from `tokens.json` (not defined in handbook 1.3).
* Orange (PY-Oranje) is deliberately not used in the stories: accents are PY-Aqua, white and PY-Blauw.

## Location spots (LocatieSpot)

`src/LocatieSpot.tsx` rebuilds the Jitter animation "Plantage" (1920x1080, 60 fps, 395 frames, 6.6 s) as a template, with the Jitter keyframe times and easings:
hook screen, blue panel zooms out to the left, title, four check rows, logo, price bubble, check circles close at the end.
`src/locaties.ts` holds one entry per location (hook, four facts, price, photo, source and open check). Every location becomes a composition `Spot-<slug>`.

```bash
node scripts/render-locaties.mjs              # all locations to out/locaties/<slug>.mp4
node scripts/render-locaties.mjs plantage     # one or more slugs
node scripts/render-locaties.mjs --reels      # 9:16 reels to out/reels/<slug>.mp4
node scripts/stills.mjs /tmp/stills all 0 330 # stills for checking
```

* Data from the public location pages on parkingyou.nl (25-11-2026). Hourly prices are worked out from the published rate (for example €1,25 per 20 min = €3,75 per uur); "vanaf" only for the lowest of several rates.
* Only locations with a public visitor rate are in (34). Left out: B2 Amsterdam (subscription only) and the 14 locations without a rate on the site (Eindhoven The Beech, Mauritsstraat, BD7, Cornelis Paradise, City Tower, Lichttoren, Hoog Bergen, Hoog Stratum, Paradijslaan; Utrecht Vliegend Hert; Tilburg Pakhuis; Dordrecht De Holland).
* Photos: the location photo from the site, cropped to the right panel (`public/locaties/<id>.jpg`); Plantage uses the aerial from the Jitter file.
* Reels (`Reel-<slug>`, 1080x1920, 60 fps, 8.3 s): same timing, photo on top (760 px), blue panel below, key content inside the safe zones (top 250 px, bottom 330 px), and an end card with the stacked logo and parkingyou.nl from frame 372. Photos in `public/locaties/staand/`.
* Title: one size (88 px) for every location. When the name does not fit next to "Parking", "Parking" stays on line 1 and the name goes to line 2 (and wraps at a space to line 3 if needed; the check rows then move down a little).
* Colours from `tokens.json` (PY-Blauw background, PY-Aqua check circles); the Jitter file used slightly different values. Logo is the library beeldmerk plus wordmark.
* Entries with a `check` field have an open point from the Instagram strategy (IG-013, IG-014, IG-024) or data that is not on the site; confirm before posting. Overview: `out/locaties/OVERZICHT.md`.

## Search spots (ZoekSpot)

`src/ZoekSpot.tsx`, after the Jitter work in progress "IOS Stack": a question is typed in a search bar ("Avondje **PSV**?"),
the bar moves up, the matching locations come in as a photo-card carousel (name, price pill, walking-time pill, page dots),
and a CTA closes it. 60 fps, 7 to 15 s depending on the question and the number of cards; the first card is in view within 3 s (YouTube skip at 5 s).
`src/zoekopdrachten.ts` holds the questions; every location is in at least one. Compositions `Zoek-<slug>` (9:16) and `ZoekYT-<slug>` (16:9).

* CTA "Reserveer online, en sta zeker van je plek" only when every location in the question has online booking (`RESERVEERBAAR` in `locaties.ts`, the 15 locations with a "met reservering" rate); otherwise "Bekijk alle locaties".
* "Avondje PSV?" leaves out Philips Stadion and Philips Bedrijfsschool: the site says they are not available during matches and big events.

```bash
node scripts/render-locaties.mjs --zoek               # all, to out/zoek/ and out/zoek-youtube/
node scripts/render-locaties.mjs --zoek avondje-psv   # one question
```

## Chat spots (ChatSpot, "Het appje")

`src/ChatSpot.tsx`: a chat in the house style (plain bubbles, no messenger branding). A question comes in after typing dots
(the hook, from frame 0), the answer is a location card plus a short tip, a reply closes it, then the same end screen as the
search spots (`EindCta` in `ZoekSpot.tsx`). One location per chat, 11.4 s, 9:16 (`Chat-<slug>`) and 16:9 (`ChatYT-<slug>`).
`src/chatgesprekken.ts` holds the chats; every fact in a tip must be on the location page (`bron` field).
Older messages scroll up and fade out before they reach the logo.

```bash
node scripts/render-locaties.mjs --chat               # to out/chat/ and out/chat-youtube/
```

## Checklist spots (LijstSpot, "Het lijstje")

`src/LijstSpot.tsx`: a question (from frame 0), a white card with four points that get a tick one by one, then the card
opens to show the location photo, name and a price circle, then the shared end screen (`EindCta`). One location per video,
10.8 s, 9:16 (`Lijst-<slug>`, photo above the list) and 16:9 (`LijstYT-<slug>`, photo left of the list).
`src/lijstjes.ts` holds the question and the four points per location (text between [ ] is bold); every point must be on
the location page (`bron` field). Each point fits on one line at both sizes.

```bash
node scripts/render-locaties.mjs --lijst              # to out/lijstje/ and out/lijstje-youtube/
```

## Signpost spots (BordSpot, "Het bordje")

`src/BordSpot.tsx`: a question (from frame 0), then a street sign builds up on two posts: the parking on an aqua plank
(with a price circle), four nearby places on white planks with an arrow and the walking time, each plank flipping down
in turn, then the shared end screen (`EindCta`). One location per video, 10.7 s, 9:16 (`Bord-<slug>`) and 16:9 (`BordYT-<slug>`).
`src/borden.ts` holds three or four places per location (32 locations; Lentse plas and Pathé Ede are left out because only the cinema itself is within about 20 minutes' walk). Where the location page gives a walking time, that time is used. Walking times are foot routes from the parking address via OpenStreetMap
(routing.openstreetmap.de), rounded to whole minutes; the arrow is the compass direction (up = north, 8 directions), not the route.
Partner names as text only.

```bash
node scripts/render-locaties.mjs --bord               # to out/bordje/ and out/bordje-youtube/
```

## Map spots (KaartSpot, "Het kaartje")

`src/KaartSpot.tsx`: a question about a well-known place ("Naar het Muziekgebouw?"), a drawn map with an aqua pin on the
place, our nearest parkings drop in around it with a dotted line, name and walking time, then a row per parking with its
price (nearest marked) and the shared end screen. 10.6 s, 9:16 (`Kaart-<slug>`) and 16:9 (`KaartYT-<slug>`).
`src/kaartjes.ts` holds the places. Only places where none of our parkings is right next door. Walking times and the drawn
routes are foot routes via OpenStreetMap; the parkings sit at their real offset from the place (north up, same scale both ways).
The map is real: `scripts/kaartdata.py` fetches the routes (routing.openstreetmap.de) and the streets, water, parks, buildings
and railways around the place (Overpass), draws them in the house colours as SVG, and `scripts/raster-svg.cjs` turns that into
`public/kaarten/<slug>.jpg`. Map data © OpenStreetMap contributors (ODbL), credited on the map. The parking cards follow the
search-spot cards (photo, "Parking" + name, aqua price pill, white walking-time pill).

```bash
node scripts/render-locaties.mjs --kaart              # to out/kaartje/ and out/kaartje-youtube/
```

## Amsterdam Light campaign (Instagram ads, 9:16)

`src/AmsterdamLight.tsx`: six concepts for Parking Plantage during the light festival, 60 fps, 1080x1920, 8 to 11 s,
all with the shared end screen ("Reserveer online"). Shared kit: canal houses whose windows switch on, water with
reflections and ripples, light-art arches and rings, strings of bulbs, neon lines made of stacked strokes (no blur).

| Composition | Concept |
|---|---|
| `Light-1-lichten-aan` | A clock ticks to 16:30, the canal houses light up window by window, "Je plek staat al klaar." Usable every day. |
| `Light-2-een-lichtlijn` | One neon line from the barrier, out of the garage, along the water, ending as the logo mark; loops seamlessly (frame 480 = frame 0). Awareness. |
| `Light-3-kies-je-rondje` | Split screen: a car circles past full car parks while a stress meter rises, someone walks along lit canals. "Rondje zoeken of rondje kijken?" |
| `Light-4-light-night-<datum>` | Three dated versions (26 nov, 12 dec, 19 dec) with a countdown to that evening; run only in the days before. |
| `Light-5-reserveren-3-tikken` | A phone shows the booking: pick a date, spot confirmed, the ticket glows. |
| `Light-6-dagje-artis-avondje-licht` | Families: animals by day, the screen turns to light art at dusk. "Eén keer parkeren, de hele dag Amsterdam." |

```bash
node scripts/render-locaties.mjs --light              # to out/amsterdam-light/
```

* The phone in concept 5 is an illustration of the booking steps, not a screenshot of the real booking site.
* Partner names (Artis) as text only, no logos. The festival name itself is not used.

## Early-booking spots (VroegSpot, "Vroeg boeken loont")

`src/VroegSpot.tsx`: a question, three parking tickets with the day rates of the location (without booking, with booking,
booked early) drop in, the first two are struck through and the early one wins with the saving, then the shared end screen.
10.2 s, 9:16 (`Vroeg-<slug>`) and 16:9 (`VroegYT-<slug>`). `src/vroegboeken.ts` holds the rates of the 10 locations whose
page lists all three (DLL garage and deck are left out: closed on weekdays during office hours).

```bash
node scripts/render-locaties.mjs --vroeg              # to out/vroegboeken/ and out/vroegboeken-youtube/
```

## ParkingPass spots (StripSpot, "De strippenkaart")

`src/StripSpot.tsx`: a question ("Vaak in Rotterdam?"), a ParkingPass with 25 strips that get punched one by one while a
day counter runs, then the price per day of the 25-strip pass next to a loose day ticket (struck through) and the total
saving over 25 days; end screen "Bestel je ParkingPass". 10.4 s, 9:16 (`Strip-<slug>`) and 16:9 (`StripYT-<slug>`).
`src/strippenkaarten.ts` holds the 11 locations with a 10- and 25-strip pass (one strip is one day, as the pages say).
DLL garage and deck are left out (closed on weekdays during office hours).

```bash
node scripts/render-locaties.mjs --strip              # to out/strippenkaart/ and out/strippenkaart-youtube/
```

## Entrance-route spots (RijSpot, "Zo rijd je erin")

`src/RijSpot.tsx`: a question ("Waar is de inrit van het TD-gebouw?"), a real map (OpenStreetMap data in the house colours)
with the last stretch by car to the entrance. A car drives it, the route fills in behind it, each step (street, turn, entrance)
appears on the map and as a row under it, then the P at the entrance and the shared end screen. 10.6 s, 9:16 (`Rij-<slug>`)
and 16:9 (`RijYT-<slug>`). `src/rijroutes.ts` holds the routes; `scripts/rijdata.py` builds the route (OSRM car profile) and
the map. The stretch shown is the part that routes from several directions share, so it is right for most drivers.

```bash
node scripts/render-locaties.mjs --rij                # to out/rijroute/ and out/rijroute-youtube/
```

## Park-and-ride spots (OverstapSpot, "Parkeer en stap over")

`src/OverstapSpot.tsx`: a question ("Met de trein naar Den Haag?"), then a line map like a metro map: a car pulls into the
parking stop (with the price pill), a walker follows the line to the station with the walking time, a train pulls in and a
departure board fills with the places the location page names; the train leaves and the shared end screen follows.
10.7 s, 9:16 (vertical line, `Overstap-<slug>`) and 16:9 (horizontal line, `OverstapYT-<slug>`). `src/overstappen.ts` holds
the data; every fact (walking time, station, destinations, price, conditions such as a P+R rate) comes from the location page.

```bash
node scripts/render-locaties.mjs --overstap           # to out/overstap/ and out/overstap-youtube/
```
