# ParkingYou brand reference for social animation (Remotion)

Read this before building a reel or static post. Everything here comes from this repo (`tokens.json`, `elements.json`, `applications.json`, `docs/print-rules.md`) and from the kennisbank. When the two disagree on a price, the kennisbank wins.

## Tokens

| Token | Value | Use in social |
|---|---|---|
| PY-Blauw | `#1A3580` | Main background, logo, figures on white |
| PY-Aqua | `#32B9CD` | Keywords in headlines, price bubbles, lines, the dot in the beeldmerk |
| PY-Oranje | `#F08300` | Rare accent: "Nieuw", carnaval |
| PY-Grijs | `#AEAEAE` | Struck-through prices, inactive pills |
| PY-Zwart | `#1D1D1B` | Body text on white only |
| Verloop | `#1A3580` 0 to 18%, `#097BAE` 62%, `#32B9CD` 100% | Backgrounds of R7 and S4 (`py-tok-gradient-verloop*`) |
| Light aqua (observed) | CMYK 54/0/14/0, about `#68CBDB` | Icons on blue, optional |

Type: Ubuntu (`fonts/`), Regular 400, Medium 500, Bold 700. Load the TTFs with `@remotion/fonts` or `loadFont`. Headline pattern: key phrase Bold, rest Regular, one line; stacked headlines alternate Regular and Bold lines. Italic only for price numerals (as on the campaign panel: `€7,50`).

Logo rule (Rick, 5 November 2026): on blue, gradient or photo backgrounds the logo is white with the aqua dot and nothing else. The `py-atom-logo-*-reverse` files contain a PY-Blauw ring disc; leave that fill out.

Tagline: "The other way of parking", Ubuntu Regular, tracking +60/1000 em, white, left aligned with the wordmark (`py-comp-tagline-lockup-reverse`).

## Feed style (what the current posts look like)

Use this for every new reel or post; the Remotion kit in `social/remotion/src/v2/` implements it.

* Headlines: very large, white, sentence case, short lines; key words **Bold** in the same colour (weight contrast, not colour). On light backgrounds navy.
* Backgrounds: photo with a dark gradient, flat PY-Blauw, the cyan-to-blue GLOW gradient, or pale blue. Never flat white.
* Small logo on top. On navy or a photo: white with the aqua dot. On light blue (the GLOW gradient): all white with a white dot. On the pale blue background: the colour logo. Never the navy ring fill.
* Button "Reserveer online": aqua pill with the arrow circle from the library (`py-atom-arrow-right-circle`) on the left. Second style: navy pill "Bekijk locaties" with the arrow circle on the right.
* Url line "**voordelig**parkeren.nl" with the aqua chevron.
* Price: round badge, white with navy italic numerals (cents small and raised) or aqua with white; slightly rotated.
* Location: white pill, navy pin, navy name.
* Big numbers get a sunburst of short white rays. Celebrations get orange and aqua confetti and white silhouettes of cars and people.

## Building blocks per template

| Need | Asset ID | Notes |
|---|---|---|
| Logo end card | `py-atom-logo-horizontal-reverse-open` (Remotion), `py-atom-logo-horizontal-white` | **White and aqua only.** Never use the navy ring fill of the `-reverse` logos: the ring stays open so the background shows through. In Remotion use the `-open` IDs (made by `scripts/sync-assets.mjs`) |
| Watermark | `py-atom-logo-beeldmerk-watermark` | Aqua at 5% on blue, centred |
| Photo or video frame | `py-atom-shape-bubble-image-mask` | Use as a CSS `clip-path` or SVG mask over `<OffthreadVideo>` |
| Price label | `py-comp-price-bubble-speech`, `py-comp-price-badge-circle` | Price as live text, not outlines |
| Destination list | `py-comp-pill-list-destinations`, `py-comp-pill-destination` | Arrow circle + name; inactive pill at 25% opacity |
| Location name | `py-comp-pill-location`, `py-comp-lockup-location-garage` | |
| URL call to action | `py-comp-url-chevron`, `py-comp-url-tag-chevron` | "parkingyou.nl" with aqua chevron |
| People | `py-atom-figure-walk`, `-point`, `-wave`, `-dance`, `-jump`, `-bags-walk`, `-bags-cheer`, `-cap-point`, `-cap-wave` | Swap poses on a beat for simple character animation; `cap` = ParkingHost |
| How it works | `py-atom-illustration-phone-qr`, `-reader-qr`, `-contactless-hand`, `-card-pas`, `-card-barcode` | |
| Facts | `py-atom-picto-ev`, `-family`, `-pedestrian`, `-car`, `-lift`, `-accessible`; `py-atom-icon-calendar`, `-car-lock`, `-location-pin`, `-plug-ring`; `py-atom-symbol-p-roof`, `-p-garage-outline`; `py-atom-sign-camera` | One picto per fact |
| Date | `py-comp-calendar-date` | Day and month as live text |
| Levels | `py-atom-tag-level-*`, `py-atom-tag-section-*` | For "waar staat mijn auto" |
| Terminal stickers | `py-app-sticker-terminal-*` (applications) | Show exactly what people see on the pay station |

SVG viewBoxes are in millimetres and tight to the artwork; scale them with a wrapper. Every element is one SVG file in `svg/{atom,comp,prod}/<id>.svg`; applications have `template.svg` in `applications/<id>/`.

## Layout

* Reel 1080 x 1920: safe zone top 250 px, bottom 330 px. Headline from y 250, two lines max. Stage area roughly y 514 to 1414.
* Feed 1080 x 1350: scale the stage to 0.78, margins 80 px. Check the feed version separately.
* Frame 0 is never empty: headline and visual are already on screen (negative delays).
* One beat per 0.5 to 1 s. The hook lands within 2 s. 3 to 5 scenes, 6 to 15 s.
* Everything must work without sound. A short music bed is optional (`music` prop).
* Render h264, yuv420p, BT.709 (set the colour space, otherwise PY-Blauw shifts).

## Product facts (kennisbank, 5 November 2026)

Online booking is possible at 14 locations: Bos en Lommerplantsoen, Cruquius, Plantage (Artis), Zeeburgerkade (Amsterdam); DLL garage, DLL parkeerdek, Evoluon, Philips Bedrijfsschool, Philips Stadion, TD Gebouw (Eindhoven); Parking At the Park (Rijswijk); Europoint, Hofplein, Shopping Center (Rotterdam).

Three price levels at most booking locations: ter plaatse (drive-up), reservering online, vroegboek online. Examples: Hofplein €30 / €25 / €20 on weekdays; Parking At the Park €12 / €9 / €7; Plantage €45 / €42 / €30.

Other products: strippenkaart (10 or 25 days), subscriptions (24/7, Office, Avond/weekend, Bewoners, Bedrijf), doelgroeptarieven (Artis, Pathé), P+R Schiedam (€3,64 per day, Mon to Fri, with train travel), night rates (Hofplein €15, Plantage €22).

Prices change every February. Query `kennisbank.tarief` (filter `geldig_tot is null or geldig_tot > now()`) before rendering a reel with a price.

## Copy rules

See section 7 of `strategy.md`. In short: Dutch, "je", hook first, prices with location, no long dashes, "reserveer" only for booking locations, 3 to 5 hashtags.
