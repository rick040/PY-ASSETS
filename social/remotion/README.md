# ParkingYou reels (Remotion)

Animated Instagram reels built from the PY-ASSETS brand library. Each reel is a **template** (a Remotion composition with a zod schema) plus an **item** (a JSON file with the texts, prices and colours of one post from `../instagram/content-library.json`).

| Template | Status | Items in the library |
|---|---|---|
| R1 Locatiekaart | built | IG-001, 002, 003, 005 to 010, 012, 016, 066 (IG-002 rendered) |
| R2 Prijsrol | built | IG-017, 018, 025, 054 (IG-017 and IG-018 rendered) |
| R4 Drie stappen | built | IG-028, 029, 035, 059 (IG-028 rendered) |
| R5 Figuursketch | built | IG-023, 031, 042, 050, 053, 057, 060, 064 (IG-064 rendered) |
| R7 Kinetische tekst | built | IG-021, 032, 033, 045, 048, 051, 062 (IG-021 rendered) |
| R3 Looproute | built | IG-038, 039, 044 (IG-039 rendered) |
| R6 Aftelkalender | built | IG-037, 041, 047 (IG-041 rendered) |

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

## Logo and button rules

`TopLogo` picks the logo from the backdrop it sits on, so scenes never choose it by hand:

| Background | Logo | File |
|---|---|---|
| Navy, photo | white with the aqua dot, never the navy ring fill | `py-atom-logo-horizontal-reverse-open` (derived) |
| Light blue (GLOW gradient, end card) | all white with a white dot | `py-atom-logo-horizontal-reverse-whitedot` (derived; the library's white logo has a hole where the dot is) |
| Pale blue (`light`) | colour logo | `py-atom-logo-horizontal-color` (white would disappear) |

`scripts/sync-assets.mjs` writes the derived files to `public/py/derived/`. The "Reserveer online" button uses the arrow from the asset library, `py-atom-arrow-right-circle` (white circle, aqua arrow).

## Line icons

`Glyph` takes a PY-ASSETS ID or one of the built-in glyphs `clock`, `fuel`, `mood`, `pin`, `check`, `cross` (rounded stroke style), for ideas the library has no pictogram for yet. Note that several PY-ASSETS icons are white (for use on blue): on a light background use a glyph or a navy element.

## Structure

```
src/theme.ts                  brand colours and verloop from tokens.json, Ubuntu from fonts/
src/lib/                      layout (Stage inside the safe zones, scales for 4:5), springs, shape paths, *key phrase* parsing
src/components/               Slagboom (animated barrier), Glyph, BubbleMedia, Rain, SafeZones, AssetImg (any PY-ASSETS ID)
src/v2/                       feed-style kit: Backdrop, Title, CtaPill, UrlLine, PriceBadge, PlacePill, TopLogo, Card, Fx, transitions, withMotionBlur, EndCardV2
src/locatiekaart/             R1: hook (photo or stand-in), facts, price badge, end card
src/prijsrol/                 R2: price badges hook, rows that count up and get struck through, saving pill (calculated), answer badge
src/driestappen/              R4: barrier opens (outcome first), one scene per step with progress dots, outcome, end card
src/figuursketch/             R5: hook line-up, one beat per figure, outro, end card
src/looproute/                R3: walker on a drawing route, walking minutes per location, price badge
src/aftelkalender/            R6: flipping tear-off calendar to the event date, event card, price badge
src/kinetisch/                R7: hook (optional orbit), lines with icons, end line (optional arrive), end card
src/items/                    one JSON per library item
renders/                      delivered MP4s and covers (in git)
public/py/                    synced copy of svg/, fonts/, tokens.json (git-ignored)
```

## Rendered items (feed style, 30 fps, motion blur)

| Item | Template | Length | Scenes |
|---|---|---|---|
| IG-002 Hofplein | R1 | 12.3 s | hook with headline and place pill, facts on white cards, weekend price badge over rays, end card |
| IG-017 Hofplein drie prijzen | R2 | 12.3 s | price badges on the GLOW gradient, rows that count up and get struck through, saving pill, answer badge, end card |
| IG-018 Rijswijk drie prijzen | R2 | 12.3 s | same as IG-017 with €12 / €9 / €7 |
| IG-021 Rondjes rijden | R7 | 11.5 s | car circling the P with a lap counter, three cards, car drives straight in, end card |
| IG-028 Reserveren in 3 stappen | R4 | 13.8 s | barrier opens, three steps on pale blue with rays, outcome with confetti, end card |
| IG-039 GLOW looproute | R3 | 13.1 s | "Waar parkeer je tijdens GLOW?" with a walker on a drawing route, five locations with walking minutes, €15 per avond badge, end card |
| IG-041 Amsterdam Light Festival | R6 | 12.3 s | tear-off calendar flips from 6 to 26 November with sparkles, "Nog 20 dagen", event card with dates and locations, vanaf €17,50 badge, end card |
| IG-064 Parkeertypes | R5 | 14.4 s | line-up, four types, outro with confetti, end card |

Beat timings live as constants at the top of each scene file (for example `T_PILL`, `T_FACTS`, `T_STRIKE`), so a voice-over can be timed against them.
