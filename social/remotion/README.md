# ParkingYou reels (Remotion)

Animated Instagram reels built from the PY-ASSETS brand library. Each reel is a **template** (a Remotion composition with a zod schema) plus an **item** (a JSON file with the texts, prices and colours of one post from `../instagram/content-library.json`).

| Template | Status | Items in the library |
|---|---|---|
| R1 Locatiekaart | built | IG-001 to IG-012, IG-016, IG-066 (IG-002 rendered) |
| R2 to R7 | not built yet | see `../instagram/strategy.md`, section 9 |

## Start

```bash
cd social/remotion
npm install
npm run studio        # copies svg/, fonts/ and tokens.json to public/py, then opens Remotion Studio
```

In Studio, folder `R1-Locatiekaart` has a `Template` and one entry per item, each in two sizes: `-Reel` (1080 x 1920) and `-Feed` (1080 x 1350). Every text, price, icon, colour and scene length is a prop in the right-hand panel. Turn on `showSafeZones` to see what Instagram covers.

## Render

```bash
npm run render:ig-002         # renders/IG-002-hofplein-reel.mp4
npm run render:ig-002:feed    # renders/IG-002-hofplein-feed.mp4
npm run still:ig-002          # renders/IG-002-hofplein-cover.png (frame 60)
```

In a cloud session without internet access to the Remotion browser download, add the preinstalled browser, for example
`-- --browser-executable=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`.

Output is h264, yuv420p, BT.709 (set in `remotion.config.ts`, keeps PY-Blauw on brand).

## Add a new location reel (R1)

1. Copy `src/items/IG-002.json` to `src/items/IG-0NN.json` and fill it from the library item: hook (`*word*` = key phrase in aqua bold, `\n` = new line), location, three facts (icon = a PY-ASSETS element ID), price, CTA.
2. Check every price in `kennisbank.tarief` first.
3. Add the item to the `items` list in `src/Root.tsx` and add render scripts to `package.json`.
4. Render 15 or so stills across the timeline and look at them before rendering the MP4 (headline on two lines, nothing under the safe zones, frame 0 not empty).

## Real footage

`media.type: "none"` shows a branded stand-in (verloop, P with roof, a car parking under it). For the real thing, put a photo or a short clip of the location in `public/media/` and set for example `"media": { "type": "video", "src": "media/hofplein.mp4" }`. It is masked into the speech bubble of `py-atom-shape-bubble-image-mask`. A 5 to 7 second vertical clip of the entrance works best.

## Structure

```
src/theme.ts                  brand colours and verloop from tokens.json, Ubuntu from fonts/
src/lib/                      layout (Stage inside the safe zones, scales for 4:5), springs, shape paths, *key phrase* parsing
src/components/               Headline, BubbleMedia, LocationPill, FactRow, PriceBubble, UrlCta, Rain, SafeZones, AssetImg (any PY-ASSETS ID)
src/locatiekaart/             R1: schema.ts, LocatiekaartAd.tsx, scenes/ (Main, Price, Cta)
src/items/                    one JSON per library item
renders/                      delivered MP4s and covers (in git)
public/py/                    synced copy of svg/, fonts/, tokens.json (git-ignored)
```

## IG-002 timeline (30 fps, 366 frames, 12.2 s)

| Time | Frame | What happens |
|---|---|---|
| 0.0 s | 0 | Hook on screen: "Midden in Rotterdam. Droog geparkeerd.", rain, bubble, car driving in under the roof |
| 0.6 s | 18 | Location pill "Hofplein Rotterdam" |
| 3.1 s | 92 | Bubble shrinks, pill moves up |
| 3.7 / 4.3 / 4.9 s | 112 / 130 / 148 | Facts: 300 overdekte plekken, Camerabewaking, Vroegboeken €20 per dag |
| 6.6 s | 198 | Slide up to the price scene |
| 7.0 s | 208 | Price bubble "€15 per dag", "En in het weekend?" |
| 9.2 s | 276 | Wipe to the end card |
| 9.7 s | 290 | parkingyou.nl, then logo and tagline |
