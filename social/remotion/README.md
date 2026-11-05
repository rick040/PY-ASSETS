# ParkingYou reels (Remotion)

Animated Instagram reels built from the PY-ASSETS brand library. Each reel is a **template** (a Remotion composition with a zod schema) plus an **item** (a JSON file with the texts, prices and colours of one post from `../instagram/content-library.json`).

| Template | Status | Items in the library |
|---|---|---|
| R1 Locatiekaart | built | IG-001, 002, 003, 005 to 010, 012, 016, 066 (IG-002 rendered) |
| R2 Prijsrol | built | IG-017, 018, 025, 054 (IG-017 and IG-018 rendered) |
| R4 Drie stappen | built | IG-028, 029, 035, 059 (IG-028 rendered) |
| R5 Figuursketch | built | IG-023, 031, 042, 050, 053, 057, 060, 064 (IG-064 rendered) |
| R7 Kinetische tekst | built | IG-021, 032, 033, 045, 048, 051, 062 (IG-021 rendered) |
| R3, R6 | not built yet | see `../instagram/strategy.md`, section 9 |

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
npm run render:ig-017         # and :feed, still:  R2, Hofplein €30 / €25 / €20
npm run render:ig-018         # and :feed, still:  R2, Rijswijk €12 / €9 / €7
npm run render:ig-028         # and :feed, still:  R4, "Je plek geregeld in 3 stappen."
npm run render:ig-021         # and :feed, still:  R7, "Rondjes rijden is ook betalen."
npm run render:ig-064         # and :feed, still:  R5, "Welk parkeertype ben jij?"
```

In a cloud session without internet access to the Remotion browser download, add the preinstalled browser, for example
`-- --browser-executable=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`.

Output is h264, yuv420p, BT.709 (set in `remotion.config.ts`, keeps PY-Blauw on brand).

## Add a new location reel (R1)

1. Copy `src/items/IG-002.json` to `src/items/IG-0NN.json` and fill it from the library item: hook (`*word*` = key phrase in aqua bold, `\n` = new line), location, three facts (icon = a PY-ASSETS element ID), price, CTA.
2. Check every price in `kennisbank.tarief` first.
3. Add the item to the `items` list in `src/Root.tsx` and add render scripts to `package.json`.
4. Render 15 or so stills across the timeline and look at them before rendering the MP4 (headline on two lines, nothing under the safe zones, frame 0 not empty).

## Feed style (v2, November 2026)

All templates follow the look of the current Instagram feed. The shared kit is in `src/v2/`:

| Part | What it does |
|---|---|
| `Backdrop` | `navy` (flat PY-Blauw with slowly drifting light, noise driven), `glow` (the cyan-to-blue GLOW gradient), `light` (pale blue, as the Easter post), `photo` (photo or video with a slow Ken Burns move and a dark gradient for legible text). Fine film grain and a vignette on top |
| `Title` | Big white headline, key words in **Bold** (weight contrast, same colour). Size is fitted to the widest line. Each line rises out of a mask with an expo-out curve, staggered; lines leave upwards before the scene ends |
| `CtaPill`, `UrlLine` | The "Reserveer online" button (aqua pill, white arrow circle) that grows out of its circle, gets a light sweep and a nudging arrow; the "voordelig**parkeren.nl**" line with the aqua chevron |
| `PriceBadge`, `PlacePill`, `TopLogo` | Round price badge (white/navy or aqua/white, small raised cents, one soft overshoot, then floats); white place pill with navy pin; small logo on top |
| `Card` | White pill card with a navy icon disc for facts, price rows and lines; text auto-fits |
| `Fx` | `Sunburst` (rays drawn with `@remotion/paths`, turning slowly), `Confetti` (orange, aqua, white; physics with drag and gravity), `Skyline` (white silhouettes of cars and people) |
| `transitions` | `slideBlur` (vertical push with speed-based blur), `bubbleReveal` (the next scene opens through the ParkingYou speech bubble), `zoomThrough` (zoom and blur) |
| `withMotionBlur` | Real camera motion blur from `@remotion/motion-blur` (6 sub-frames per frame, shutter 180 degrees) around every composition |
| `EndCardV2` | GLOW gradient, logo, headline, button, url line, tagline |

Motion rules: entrances use `cubic-bezier(0.16, 1, 0.3, 1)` (expo out), exits `cubic-bezier(0.7, 0, 0.84, 0)`; text never bounces, only badges get one soft overshoot; everything leaves before the cut so transitions feel choreographed; only transforms, opacity and filters are animated.

Render time with motion blur is about 3 minutes per 12-second reel at `--concurrency=4`. Turn it off for quick checks with the prop `motionBlur: false`. `npm run render:all` (`scripts/render-all.sh [browser]`) renders every item.

The url on the end card is `voordeligparkeren.nl`, as on the current posts; change `cta.url` per item if a post should point elsewhere.

## Photos

The hook of R1 switches to a full-bleed photo or video as soon as an item has `"media": { "type": "image" | "video", "src": "media/<file>" }` with the file in `public/media/`. The Ken Burns move and the text gradient are automatic. Good sources are the photos already used in the feed (Hofplein skyline, Bos en Lommer entrance, GLOW at night).

## Logo rule

Logos on blue, gradient or photo backgrounds are white with the aqua dot only. The `py-atom-logo-*-reverse` files have a navy ring fill; `scripts/sync-assets.mjs` writes `-open` versions without it to `public/py/derived/`. Always use `py-atom-logo-horizontal-reverse-open` (or the stacked or beeldmerk `-open` variant); the shared `EndCard` already does.

## Line icons

`Glyph` takes a PY-ASSETS ID or one of the built-in glyphs `clock`, `fuel`, `mood`, `pin`, `check`, `cross` (rounded stroke style), for ideas the library has no pictogram for yet. Note that several PY-ASSETS icons are white (for use on blue): on a light background use a glyph or a navy element.

## Real footage

`media.type: "none"` shows a branded stand-in (verloop, P with roof, a car parking under it). For the real thing, put a photo or a short clip of the location in `public/media/` and set for example `"media": { "type": "video", "src": "media/hofplein.mp4" }`. It is masked into the speech bubble of `py-atom-shape-bubble-image-mask`. A 5 to 7 second vertical clip of the entrance works best.

## Structure

```
src/theme.ts                  brand colours and verloop from tokens.json, Ubuntu from fonts/
src/lib/                      layout (Stage inside the safe zones, scales for 4:5), springs, shape paths, *key phrase* parsing
src/components/               EndCard, Slagboom (animated barrier), Glyph, LabelPill, Headline, BubbleMedia, LocationPill, FactRow, PriceBubble, UrlCta, Rain, SafeZones, AssetImg (any PY-ASSETS ID)
src/locatiekaart/             R1: schema.ts, LocatiekaartAd.tsx, scenes/ (Main, Price, Cta)
src/prijsrol/                 R2: price tags hook, rows that count up and get struck through, saving badge (calculated), price bubble
src/driestappen/              R4: barrier opens (outcome first), one scene per step with progress dots, outcome, end card
src/figuursketch/             R5: hook line-up, one beat per figure, outro, end card
src/kinetisch/                R7: hook (optional orbit), lines with icons, end line (optional arrive), end card
src/components/EndCard.tsx    shared end card for every template
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

## IG-021 timeline (R7, 342 frames, 11.4 s)

| Time | What happens |
|---|---|
| 0.0 s | "Rondjes rijden is ook betalen." with a car circling the P, lap counter |
| 2.8 s | "Je betaalt met": Benzine, Tijd, Je goede humeur (lines at +0.5, +1.1, +1.7 s) |
| 5.8 s | "Reserveer vooraf. Rijd direct naar je plek.": car drives straight in, check mark |
| 8.4 s | End card |

## IG-064 timeline (R5, 420 frames, 14.0 s)

| Time | What happens |
|---|---|
| 0.0 s | "Welk parkeertype ben jij?" with the four figures |
| 2.0 s, 3.8 s, 5.5 s, 7.2 s | 1/4 De rondjesrijder, 2/4 De last-minute boeker, 3/4 De vroegboeker, 4/4 De zoeker |
| 9.0 s | "Tag een rondjesrijder." with the walker highlighted |
| 11.0 s | End card "Word een vroegboeker" |

## IG-017 timeline (R2, 366 frames, 12.2 s)

| Time | What happens |
|---|---|
| 0.0 s | "Zelfde plek. Drie prijzen." with three swinging price tags (€30, €25, €20), then the Hofplein pill |
| 2.2 s | "Een dag parkeren": Ter plaatse €30, Online reserveren €25, Vroegboeken €20 count up one by one |
| 4.6 s | €30 and €25 are struck through, Vroegboeken turns aqua, "Je bespaart €10 per dag" (calculated from the rows) |
| 6.8 s | "Zelfde garage. Alleen eerder geboekt." with the €20 per dag bubble, "Doordeweeks, vroegboeken online" |
| 9.2 s | End card "Boek vroeg, betaal minder" |

The saving in the badge is always calculated from the row amounts (highest minus highlighted), so it cannot drift from the prices.

## IG-028 timeline (R4, 401 frames, 13.4 s)

| Time | What happens |
|---|---|
| 0.0 s | "Je plek geregeld in 3 stappen." The barrier opens (0.5 s) and a car drives through |
| 2.2 s | Step 1: phone with QR, "Kies je locatie en tijd" |
| 4.1 s | Step 2: contactless hand, "Betaal online" |
| 6.0 s | Step 3: QR reader, "Rijd in met je code" |
| 7.8 s | "Slagboom open. Je plek staat klaar.": barrier opens, the car drives out, a figure with shopping bags cheers |
| 10.4 s | End card |
