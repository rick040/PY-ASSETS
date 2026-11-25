# ParkingYou brand refresh 2027: project brief

Version 1, 2026-11-07. Owner: Rick (rick@parkingyou.nl is the client contact; do not contact anyone).
Every subagent receives this file. It is the shared starting point. Read it fully before you start.

## 1. The company

ParkingYou B.V. (parkingyou.nl) runs parking garages and lots in the Netherlands: 40+ garages and terrains in 25+ cities
(Eindhoven, Amsterdam, Rotterdam, Den Haag, Utrecht, Tilburg and others), 500.000+ parkers a year (source: existing
ParkingYou Design System README, which takes it from the website copy). Entry by licence plate recognition.
Products: Direct parkeren (day tickets), Abonnementen (min. 3 months), ParkingPass (10 or 25 parking actions),
Waardekaarten (prepaid business cards), Evenementen parking (GLOW Eindhoven, PSV/Philips Stadion, Markthal),
and a B2B offer for garage owners (Zakelijk). Partners shown on terminals: EasyPark, ParkBee, MyWay, Mobian.
Tagline in use: "The other way of parking". Campaign line in use: "Voordelig parkeren zonder gedoe?".
Tone today: no-nonsense challenger, "digitaal waar het kan, menselijk wanneer het moet", short Dutch sentences, je/jij on marketing.

## 2. Where customers meet the brand

Website and booking flow (Aeroparker), PWA, social ads and reels (9:16, 4:5), monthly newsletter, campaigns (GLOW Eindhoven),
payment terminals (stickers on the machines), subscription cards, stickers, price signs (deelfolie), posters (A3, A2),
info pylons, entrance lightboxes, portals over the entry lane, height bars, route boards, level and section markers on columns,
wall banners, escape plans. Most physical signage hangs in dark, low, concrete garages with mixed LED and older lighting.

## 3. The current system (facts from the PY-ASSETS repo)

Source of truth today: "parkingyou Huisstijlhandboek, Wayfinding & inrichting parkeervoorziening" v1.0, 09-2025, made by
All Jobs Wayfinding & Parking Solutions. It is a signage handbook (51 pages), not a full brand guideline: it has no
digital, social, photography, tone of voice or motion chapter.

**Logo.** Beeldmerk: a speech-bubble / location-pin shape with a ring and an aqua dot. Wordmark "parkingyou" lowercase,
"parking" in Ubuntu Regular (handbook says Medium; outlines measure Regular), "you" in Ubuntu Bold. Stacked and horizontal
lockups in colour, black and white. An undocumented "reverse" logo (white bubble, navy ring, aqua dot) is used on every lightbox face.
Files: `svg/atom/py-atom-logo-*.svg`.

**Colour (handbook 1.3).** PY-Blauw #1A3580 (CMYK 100/83/0/17, RAL 5002 best match), PY-Aqua #32B9CD (69/0/21/0, RAL 6027 best match,
which is green-leaning), PY-Oranje #F08300 (0/57/100/0, RAL 2003), PY-Grijs #AEAEAE (RAL 9006), PY-Zwart #1D1D1B.
The "verloop" gradient blue to aqua is used everywhere but never defined; measured stops #1A3580 0-18%, #097BAE 62%, #32B9CD 100%.

**Computed WCAG contrast of today's pairs** (relative luminance, WCAG 2.x formula):
- PY-Blauw on white 11.26:1 (pass)
- PY-Aqua on white 2.34:1 (fails for any text; white text on aqua also 2.34:1)
- PY-Oranje on white 2.64:1 (fails; the booking CTA is white on orange)
- PY-Aqua on PY-Blauw 4.80:1 (passes AA normal text, narrowly)
- PY-Oranje on PY-Blauw 4.26:1 (AA large text only)
- PY-Grijs on white 2.22:1 (fails)
- White on the gradient mid stop #097BAE 4.71:1; white on the aqua end 2.34:1 (level markers and "Mindervaliden" boards put white text there)

**Two palettes in parallel.** The website (Next.js + Payload, captured in the ParkingYou Design System artifact) uses a
marketing palette #374E9D blue, #79CADC aqua, #EE7D2C orange, #0D142E deep navy. The booking UI and signage use the handbook palette.
So the brand already has two blues, two aquas and two oranges in daily use.

**Print drift (docs/print-rules.md).** Across 21 print files: 15 different blues and 5 aquas; light aqua exists in at least five
values with no token; 8 of 20 files are RGB only; bleed missing in 7 of 10; orange and grey are not used in any print file.
Two blues sometimes appear on one sheet.

**Type.** Ubuntu only (Ubuntu Font Licence 1.0, free), Light to Bold plus italics. Signature: bold key phrase plus regular
supporting words in one line; italic accent word in website headings. RVV sign numerals use third-party fonts.

**Shapes and graphic devices (handbook 1.4).** Speech-bubble silhouette (solid, gradient, image mask), circle, pill (solid and
on gradient), separator arc, bracket arc with slogan, "P with roof" symbol, 12 navy pictograms, 9 people figures
(stick-figure style, waving, shopping bags, attendant with cap), level bubble "0" and section tag "1A", column band with
repeated "1A" on gradient.

**Website (from the Design System README).** 8px radius cards, 999px pill buttons, blue-tinted soft shadows, pin-shaped photo crop,
circular "price blob", italic accent word in headings, Unsplash-style daylight photography, no patterns.

**Social.** Three test Remotion stories (9:16) exist in `remotion/`: navy, aqua, white; orange deliberately left out.

## 4. The ambition

Move to a 2027 design language that is dynamic, adjustable and modular. Clean, modern, simple, and recognisable from across a
garage floor or in a two-second scroll. One language from a 9:16 reel to a 3-metre entrance sign.
Default stance: **evolution, not revolution**. Keep the equity that works (recognition, logo, core blue) unless research gives a
strong, evidence-based reason to go further. Any such reason is presented to Rick, not decided by us.

## 5. Constraints that every workstream respects

- Every text colour pair meets WCAG 2.2 AA (4.5:1 normal, 3:1 large text and UI graphics). Signage colours must also work under poor garage light.
- Everything must be producible: standard print processes (CMYK offset and digital, large-format UV, cut vinyl, lightbox film),
  existing signage materials (aluminium sandwich panel, powder coat RAL, opal lightbox faces, wall foil), free or licensable fonts
  (flag any licence cost).
- Plain spoken Dutch for guideline copy; no marketing fluff; no em dashes (use commas, semicolons or periods).
- Token names, file names and code in English.
- Never delete or overwrite existing assets. New work lives in `brand-2027/`.
- Every research claim is sourced with a link. Anything not sourced is marked **(assumption)**.
- Third-party marks (RVV signs, payment brands, partner logos) are reference only.

## 6. Where to look

Repo root `/home/user/PY-ASSETS` (GitHub rick040/PY-ASSETS):
`README.md`, `tokens.json`, `elements.json`, `applications.json`, `docs/phase1-inventory.md` (handbook inventory and 27 inconsistencies),
`docs/print-rules.md` (print drift and observed rules), `svg/{tok,atom,comp,prod}/`, `applications/<id>/reference.svg`,
`overview/*.pdf` (A3 overviews of every element and application), `remotion/`.
Rendered overview pages (PNG) are in the session scratchpad if you need a quick look:
`/tmp/claude-0/-home-user-PY-ASSETS/1b5086e0-7801-51e7-a402-d5ed0b8f0d3d/scratchpad/renders/`.
Live: https://www.parkingyou.nl and ParkingYou's social channels.

## 7. Output rules for research briefs

Max about 800 words. Fixed structure:

```
## [Scope]
Key findings (5 to 8 bullets)
What this means for ParkingYou (3 to 5 bullets)
Open questions
Sources (linked)
```
Write in English (the guideline itself will be Dutch). Be specific: numbers, names, values. No filler.
