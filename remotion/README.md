# Remotion stories (test)

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
