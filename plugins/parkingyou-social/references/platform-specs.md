# Platform specs

Channels in scope (decision S5): Instagram and Facebook (posted together), LinkedIn for pillar P6 only.
Platform limits change; re-check this file every quarter against the platforms' help pages. Last checked: 2026-11-23.

## 1. Canvas sizes

All renders are made at the listed size and exported at 2x for review (2160 px wide); the upload file is the 1x size unless the platform accepts more.

| ID | Use | Size (px) | Ratio | Channels |
|---|---|---|---|---|
| `feed` | Feed post, carousel slide | 1080 x 1350 | 4:5 | Instagram, Facebook, LinkedIn |
| `story` | Story frame, reel | 1080 x 1920 | 9:16 | Instagram, Facebook |
| `square` | LinkedIn post | 1200 x 1200 | 1:1 | LinkedIn (P6) |
| `landscape` | LinkedIn link or document cover | 1200 x 627 | 1.91:1 | LinkedIn (P6) |

## 2. Safe zones

| Format | Keep free of text, logo and key content | Source |
|---|---|---|
| `story` (and reel) | Top 250 px, bottom 340 px; also 60 px on the right for the reel buttons column | `remotion/README.md`, 2027 AP Social |
| `story` cover of a reel | Everything important inside the centre 1080 x 1350 (the 4:5 feed crop) and readable in the 3:4 profile grid crop (centre 1080 x 1440) | `strategy.md` §8 |
| `feed` | The profile grid shows a 3:4 crop (centre 1012 x 1350): keep the headline and logo inside it | Instagram grid |
| `feed` carousel | Same as `feed`; slide 1 must work alone | |
| `square`, `landscape` | 60 px on every side | |

## 3. Captions and text

| Channel | Limit | Visible before "meer" | Rule |
|---|---|---|---|
| Instagram | 2,200 characters, max 30 hashtags | About 125 characters | Hook in the first line, 3 to 5 hashtags at the end, "link in bio" (no clickable links) |
| Facebook | Long text allowed | About 125 to 150 characters | Same caption as Instagram; a link may be written out (`parkingyou.nl`) |
| LinkedIn | 3,000 characters | About 210 characters | Business tone, still "je"; no emoji markers; 1 to 3 hashtags; link in the post or first comment |
| Alt text | Instagram and LinkedIn take custom alt text (keep under about 250 characters) | | See `brand-voice.md` §5 |

## 4. Carousels

| Rule | Value |
|---|---|
| Slides | 2 to 10 (Instagram allows up to 20; we stay at 10 or fewer) |
| Size | All slides `feed` 1080 x 1350 |
| Arc | Slide 1 hook, slides 2 to n-1 one point each, last slide summary and CTA |
| Continuity | A swipe cue on slide 1 only; alternate navy and white grounds per slide (both themes) |

## 5. Video (reels, via the Remotion kit)

| Rule | Value | Source |
|---|---|---|
| Length | 6 to 15 s, hook within 2 s, frame 0 never empty | `strategy.md` §8, `social/remotion/README.md` |
| Encoding | H.264, yuv420p, BT.709 (keeps PY-Blauw on brand), 30 fps | `social/remotion/README.md` |
| Sound | Everything readable without sound | `brand-parkingyou.md` |
| End card | Logo and URL, at least 1.5 s | 2027 CS 8 |

## 6. Links and tracking

- The bio link goes straight to the booking page of the location in the latest post (`strategy.md` §7).
- UTM on the bio link: `utm_source=instagram&utm_medium=social&utm_campaign=<item id>` (`strategy.md` §10). Facebook: `utm_source=facebook`. LinkedIn: `utm_source=linkedin`.
- Visuals show `parkingyou.nl` only, never a long URL (D S1).
