# Brand visual rules for social

Two themes share one post spec (decision S3): **`feed`** is the current Instagram look (default) and **`2027`** is the approved refresh.
Each rule names its source: `T` = `tokens.json`, `PR` = `docs/print-rules.md` (observed in print), `BP` = `social/instagram/brand-parkingyou.md`,
`RR` = `social/remotion/README.md`, `ST` = `social/instagram/strategy.md`, `CS` = `brand-2027/02-build/core-spec.md` (branch `claude/parkingyou-brand-refresh-hz67bb`),
`AP` = `brand-2027/02-build/11-toepassingen/chapter.md`, `D` = `decisions.md`.

Values are never copied into templates: the `feed` theme reads `tokens.json`, the `2027` theme reads `brand-2027/tokens/tokens.json`.

## 1. Shared by both themes

| Rule | Source |
|---|---|
| Brand colours: PY-Blauw `#1A3580`, PY-Aqua `#32B9CD`, PY-Oranje `#F08300`, PY-Grijs `#AEAEAE`, PY-Zwart `#1D1D1B`, white. | T, CS 5.1 |
| "Observed" tokens (reflective red, LED green, safety green, RVV red, terminal blue, light aqua `#68CBDB`) are never fills or text colours in a post. | T `observed`, README |
| Logo geometry is never changed, recoloured outside its versions, rotated, stretched, outlined or placed inside a bubble. | CS 2, PR 6 |
| Logo clear space 0.5 x the beeldmerk width on all sides. Minimum on a 1080 px canvas: beeldmerk height 24 px for the horizontal lockup. | CS 2 |
| The wordmark is never retyped; use the logo files. | README "Text and fonts", CS 6 |
| Ubuntu family only (Ubuntu in `feed`, Ubuntu Sans in `2027`). Sentence case. | T `typography`, CS 6 |
| Headline voice: key phrase bold, rest regular, in one line or stacked ("**Parkeer** ernaast."). | PR 2, BP, CS 6 |
| Figures (`py-atom-figure-*`) are never redrawn, never rotated, never cut off by the canvas edge. | CS 4b |
| Third-party marks (payment brands, partner badges, RVV signs, GLOW, EasyPark, Pathé) only from official files and after approval. | README, ST 7, D S10 |
| No AI images of real locations presented as real. Photos are own locations, natural colour. | CS 9 |
| URL is `parkingyou.nl`. | D S1 |
| No emoji anywhere in a visual. | D S8 |

## 2. Contrast (WCAG 2.x, computed)

Text needs 4.5:1; large text (24 px regular or 19 px bold and up at 1080 px wide) and graphics 3:1.

| Text on ground | Ratio | Use |
|---|---|---|
| white on PY-Blauw | 11.26 | Default for both themes |
| PY-Aqua on PY-Blauw | 4.80 | `feed` only, for key words and badges. `2027`: never (AP Social) |
| PY-Blauw on PY-Aqua | 4.80 | Both |
| PY-Blauw on white | 11.26 | Both |
| PY-Grijs on PY-Blauw | 5.08 | Struck-through prices (`feed`) |
| white on the verloop mid stop `#097BAE` | 4.71 | Just passes; keep text in the navy part of the verloop |
| PY-Blauw on PY-Aqua (button, badge) | 4.80 | Both (D S16) |
| white on PY-Aqua | 2.34 | **Never** |
| white on PY-Oranje | 2.64 | **Never** |
| PY-Aqua or PY-Grijs on white | 2.34 / 2.22 | **Never** as text |
| PY-Blauw on PY-Oranje | 4.26 | Large text only |

Contrast is measured on the rendered pixels behind the glyphs, not on the nominal colour (QA `check_brand.py`).

## 3. Theme `feed` (current look)

Source of truth for the look: the 15 posts in `social/remotion/renders/posts/` and the kit in `social/remotion/src/v2/` (RR "Feed style").

### 3.1 Colour roles

Only exact token colours (decision S13). No lighting effects, glows, grain, vignettes, shadows or extra gradients.

| Role | Value | Source |
|---|---|---|
| Main ground | Flat PY-Blauw (`navy`, the default) | T, D S15 |
| Second ground | The verloop from `tokens.json` (`verloop`, 135°): text stays in the navy part. Open point in `decisions.md` | T `py-tok-gradient-verloop` |
| Light ground | Flat white (`white`), navy text, colour logo | T, D S15 |
| Photo | Own photo with text on a PY-Blauw field next to or below it, never on the photo and never under a darkening overlay | CS 9, D S15 |
| Accent | PY-Aqua for badges, the CTA button, numbers and lines | BP, ST 8 |
| Orange | Rare accent only ("Nieuw", carnaval). Never a button, never a ground | BP, ST 8 |
| Never | Any colour that is not a token: the GLOW gradient, drifting light (`#9FF3FF`, `#4E7BFF`, `#3B5BD0`), pale blue `#E4EEF4`, darkened navy, shadows | D S13 |

### 3.2 Logo

| Ground | Logo | File |
|---|---|---|
| Navy, verloop, navy field next to a photo | White with the aqua dot. **Never the navy ring fill** of the `-reverse` files (Rick, 5 November 2026) | `py-atom-logo-horizontal-reverse-open` (derived by `sync-assets.mjs`) |
| White | Colour logo | `py-atom-logo-horizontal-color` |

Placement: small, centred at the top of a post. Tagline "The other way of parking" only in the lockup `py-comp-tagline-lockup-reverse` (Ubuntu Regular, tracking +60/1000 em, left aligned with the wordmark; PR 6).

### 3.3 Type

| Element | Rule | Source |
|---|---|---|
| Headline | Very large, white (navy on white), sentence case, short lines; key words Bold in the same colour, rest Regular. Fitted to the widest line | BP |
| Body | Ubuntu Regular, white, max about 2 lines | posts |
| Price numerals | Bold italic, cents small and raised; "per dag" upright Regular | BP, PR 15, PR 25 |
| Italic | Only for price numerals | PR 1 |

### 3.4 Elements

| Element | Use | ID / component |
|---|---|---|
| Price badge | Round, white or aqua with **navy** numerals (D S16), slightly rotated, optional sunburst of short white rays, no shadow. **Max one per post**, and not in two posts in a row (the current feed uses it in 6 of 15) | kit `PriceBadge`, `py-comp-price-badge-circle` |
| Fact pill | White pill with a navy icon disc; 2 or 3 per post. White library artwork (`py-atom-symbol-p-*`, location pins) never on a white disc | kit `Pill`, `ArtDisc` |
| Place pill | White pill, navy pin, navy name | kit `Pill`, `py-comp-pill-location` |
| CTA button | "Reserveer online": aqua pill with **navy** text (D S16) and the library arrow circle on the left. Only for the 14 reservable locations (`product-truth.md`) | kit `CtaButton`, `py-atom-arrow-right-circle` |
| URL | "parkingyou.nl" as plain text (D S1). **No chevron**: the chevron is part of the voordeligparkeren sub-brand logo (D S14) | kit `Url` |
| Figures | White on navy, navy on white | kit `Figure`, `py-atom-figure-*` |
| Bubble image mask | Photo or video inside the beeldmerk bubble shape | `py-atom-shape-bubble-image-mask`, PR 23 |

### 3.5 Layout

| Format | Rule | Source |
|---|---|---|
| Post 4:5 1080 x 1350 | Margins 80 px, logo top centre, headline below it, stage in the middle, URL line bottom left | BP "Layout", posts |
| Story and reel 9:16 1080 x 1920 | Nothing important in the top 250 px and bottom 340 px | `remotion/README.md` (main), CS/AP Social |
| Reel cover | Frame 0 is never empty; the 4:5 centre crop must read on its own | BP, ST 8 |

### 3.6 Do and don't (`feed`)

| Do | Don't | Why |
|---|---|---|
| Flat token colours | Glows, lights, grain, shadows, purple-blue tints | D S13 |
| "parkingyou.nl" as text | The chevron next to parkingyou.nl | D S14 |
| One price, one location, one reason per post | Two prices fighting for attention | Concrete and local posts perform best (ST 1) |
| Let the ground choose the logo | Use a `-reverse` file with its navy ring | Rick's rule |
| Keep white text in the navy part of the verloop | Put white text on the aqua corner | 2.34:1 |
| Vary the hero: photo, figure, number, badge | A price badge with rays on every post | The feed starts to look like one post |
| Orange as a spark (carnaval, "Nieuw") | Orange buttons or grounds | BP, ST 8 |

## 4. Theme `2027`

Source of truth: `brand-2027/02-build/core-spec.md` and the three social templates in `brand-2027/02-build/11-toepassingen/figures/social-templates.png`.
The 2027 theme is stricter: **per surface the logo plus at most two elements, and exactly one parkeerder** (CS 4b, AP Social).

### 4.1 Colour roles

| Role | Value | Source |
|---|---|---|
| Ground | Flat PY-Blauw or white (paper `blue.50` for quiet areas). No gradient, no drifting light, no grain, no decorative bubble | CS 4, 4b, 5.2 |
| Accent | PY-Aqua for "de stem" and small accents. **Aqua is never a text colour on navy** | CS 5.2, AP Social |
| Orange | Never in social (only on payment signs in the garage) | CS 0 #2, CS 5.2 |
| Share of a layout | White and paper about 47 %, PY-Blauw 38 %, PY-Aqua 13 %, orange 0 % | CS 5.2 |

### 4.2 Logo

| Ground | Version | Source |
|---|---|---|
| White, `blue.50`, light photo | Colour (navy, aqua dot) | CS 2 |
| PY-Blauw, PY-Diep, dark photo | Reverse (white bubble, navy ring, aqua dot): official in 2027 | CS 2, CS 0 #6 |
| PY-Aqua | Navy one-colour (new) | CS 2 |

Placement: top left on the margin (in a reel at 5u). Clear space 0.5x.

### 4.3 Type

| Element | Rule | Source |
|---|---|---|
| Family | Ubuntu Sans variable, from `brand-2027/fonts/` | CS 6 |
| Headline | Key word ExtraBold 800, rest Regular 400; line height = size x 50/48; may break after the key word | CS 6, AP Social |
| Sizes on 1080 px (u = 54 px) | Offer headline 117 px (cap 1.5u); location 78 px; event 90 px; body 31 px (cap 0.4u) | AP Social |
| Price | Plain text "€ 12,50" ExtraBold with "per dag" beside it in Regular. No bubble, no italics, never orange | CS 6, AP Social, `brand-voice.md` |
| Eyebrow | White on PY-Blauw, all caps, at most 3 words, letter spacing 0.08 em | CS 6, AP Social |

### 4.4 Elements (choose at most two besides the logo)

| Element | Use | Source |
|---|---|---|
| De stem (half arc) | Left of the headline, as tall as the block it opens, gap 0.3x its height, stroke 1/25 of its height. Aqua on navy and white | CS 4b, kit `arc.svg` |
| De parkeerder | Exactly one, one colour (white on navy, navy on white), 3u to 8u high, always standing on a line of 0.1u, may be mirrored to face the text. Roles: gastheer for offers, loper for locations, danser for events only, juicher for deals | CS 4b, AP Social |
| De bubbel | Price, level or one word of at most 6 characters; never rotated, never with text longer than 6 characters, one per surface | CS 4 |
| De hoekige pijl | Direction only; never in a circle or bubble | CS 4b |

### 4.5 Layout

| Format | Rule | Source |
|---|---|---|
| Post 4:5 and reel 9:16 | u = 54 px, margin 2u = 108 px | AP Social |
| Reel | Top 250 px and bottom 340 px free of text and logo; key content between 5u and 29u | AP Social |
| Photo | Full bleed, plain rectangle or bubble mask. Text never on the photo; put text on a navy or white field instead of a darkening overlay | CS 9, AP Social |

### 4.6 Do and don't (`2027`)

| Do | Don't | Why |
|---|---|---|
| Leave the surface quiet | Fill empty space with pills, rays or confetti | "Rustig en vlak" (CS 1) |
| One parkeerder on a line, facing the text | Groups, skylines, floating or rotated figures | CS 4b |
| Price as text | Price badge or rotated bubble | AP Social |
| Navy field under text next to a photo | Text over a darkened photo | CS 9 |

## 5. Mapping between themes

A post spec names slots, not looks. Each archetype renders the same slots in both themes:

| Slot | `feed` | `2027` |
|---|---|---|
| headline | `Title`, weight contrast | stem + headline, ExtraBold key word |
| price | `PriceBadge` (optional rays) | plain text price line |
| location | `PlacePill` | eyebrow or stem + location name |
| facts | `Card` pills with icons | plain lines, at most 2 |
| figure | white figures, groups allowed | exactly one parkeerder on a line |
| cta | `CtaPill` + `UrlLine` | "Reserveer je plek op parkingyou.nl" text line |
| ground | navy, verloop, white, photo + field | navy, white, photo + field |

Where a slot has no 2027 equivalent (confetti, rays, second figure), the 2027 renderer drops it and QA reports it as info.
