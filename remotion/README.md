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
node scripts/stills.mjs /tmp/stills all 0 330 # stills for checking
```

* Data from the public location pages on parkingyou.nl (25-11-2026). Hourly prices are worked out from the published rate (for example €1,25 per 20 min = €3,75 per uur); "vanaf" only for the lowest of several rates.
* Only locations with a public visitor rate are in (34). Left out: B2 Amsterdam (subscription only) and the 14 locations without a rate on the site (Eindhoven The Beech, Mauritsstraat, BD7, Cornelis Paradise, City Tower, Lichttoren, Hoog Bergen, Hoog Stratum, Paradijslaan; Utrecht Vliegend Hert; Tilburg Pakhuis; Dordrecht De Holland).
* Photos: the location photo from the site, cropped to the right panel (`public/locaties/<id>.jpg`); Plantage uses the aerial from the Jitter file.
* Title: one size (88 px) for every location. When the name does not fit next to "Parking", "Parking" stays on line 1 and the name goes to line 2 (and wraps at a space to line 3 if needed; the check rows then move down a little).
* Colours from `tokens.json` (PY-Blauw background, PY-Aqua check circles); the Jitter file used slightly different values. Logo is the library beeldmerk plus wordmark.
* Entries with a `check` field have an open point from the Instagram strategy (IG-013, IG-014, IG-024) or data that is not on the site; confirm before posting. Overview: `out/locaties/OVERZICHT.md`.
