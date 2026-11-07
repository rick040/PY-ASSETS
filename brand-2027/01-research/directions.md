# ParkingYou 2027: research summary and three directions (Gate 1)

Version 1, 2026-11-07. Inputs: brief.md, R1 to R5 in this folder. Visual boards: Design artifact "ParkingYou 2027 richtingen" (https://claude.ai/artifact/6qzpbCHjaKxE8PrSUfM2Rd).
Mock-up data is real where it exists (Parking Philips Stadion: 700 places, 2,00 m, EUR 12,50 day rate with reservation, 9 min to centre, from parkingyou.nl); anything unknown is a [placeholder]. Photos are ParkingYou's own location photos from parkingyou.nl.
All contrast values are computed with the WCAG 2.x relative luminance formula.

## 1. What the research says, in ten lines

1. **The equity is real and narrow.** The beeldmerk (bubble/pin, ring, aqua dot), "parking" regular plus "you" bold, the flat navy field with big white type, and the P with roof are on every touchpoint and still look current (R1).
2. **Consistency is the biggest problem, not style.** Three palettes in daily use (handbook #1A3580/#32B9CD/#F08300, live site #192AA2/#0AD3E6/#FF8400, Canva #344F9E/#76C8DB) and at least 20 blues across print, web and Canva (R1). The fix is one token source with print and signage values attached (R5).
3. **The main conversion points fail WCAG.** Every primary CTA is white on orange (2.46 to 2.76:1). White on aqua is 2.34:1 and appears on level markers, the Mindervaliden board and Canva pills (R1, brief). Since 28 June 2025 the EAA makes this a legal issue for booking and payment (R4, R5).
4. **Navy alone does not differentiate.** Interparking, APCOA, P1 and the regulatory P all live in dark blue. **No Dutch operator leads with aqua.** The category speaks in diagonals (Q-Park, P1, Interparking, APCOA); round geometry is free, except Indigo's pin-O (R2).
5. **Yellow is taken** (ParkBee, Yellowbrick, Interparking accent, NS). Orange sits close to APCOA's accent, which is leaving NL (R2).
6. **Systems that last fix one form and vary a few named parameters** (TfL roundel, Melbourne M). Fully generative marks dated within three years (MIT 2011) (R3).
7. **Ubuntu Sans** (Canonical with Dalton Maag, variable, wdth 75 to 100, wght 100 to 800, Ubuntu Font Licence, free) is the direct, cost-free evolution of today's Ubuntu (R3).
8. **In the garage only lightness contrast survives every lamp.** Under sodium, navy and aqua both go dark; mesopic light shifts hues. White on navy is the workhorse. Cap height about 10 mm per metre of reading distance; a 200 mm route board works up to about 10 m (R4).
9. **Gradients do not survive production** on cut vinyl, RAL powder coat or translucent lightbox film; each needs a flat fallback (R4).
10. **Dated, by taste:** the stick figures, heavy all-italic headings, colour-overlaid stock photos, emoji in headlines and wave dividers. Not dated: the flat navy signage faces (R1).

## 2. Baseline that all three directions share

These follow from the evidence. They hold whichever direction you choose.

- Logo, beeldmerk and wordmark stay. The undocumented reverse logo (white bubble, navy ring, aqua dot) becomes official.
- PY-Blauw #1A3580 stays the core blue. The live site blue #192AA2 and the Canva blue #344F9E are retired.
- One DTCG token file is the only source: sRGB plus CMYK, RAL, Pantone and vinyl codes in `$extensions`. Site CSS, the Canva brand kit, print templates and sign specs all read from it.
- Ubuntu Sans replaces Ubuntu (same family, same licence, free). Print and signage get fixed instances, outlined, with overlaps merged.
- No white text on aqua or on orange. The CTA becomes orange with deep navy text (#0D142E on #F08300, 6.87:1) or moves to navy.
- Text colours added for small text on white: aqua 700 #127C8C (4.90:1) and orange 700 #B35A00 (4.80:1).
- Every gradient gets a flat fallback. RVV and ISO 7010 safety signs stay unbranded.
- The nine stick figures are retired from new work; the 12 pictograms are redrawn on one grid with the new type.
- Minimum cap height per signage product, by reading distance (R4 table).

## 3. Direction A: Bubbel

**Idea.** The bubble in the beeldmerk becomes the one container for everything ParkingYou says: a level number, a price, an arrow, a photo, a location name. Like the TfL roundel: one fixed shape, a short list of variables. The bubble is a speech bubble first; it is the brand talking to you, plainly. The rest of the system stays quiet: flat navy, white, lots of space.

**Core system.**
- Logo: unchanged. Reverse logo official. On signage the beeldmerk sits top right as today.
- Colour roles: navy ground (about 60 percent), white (30), aqua only as a bubble fill with navy content (navy on aqua 4.80:1), orange only for prices and deals with deep navy text. The verloop stays as a defined two-stop gradient for printed panels and screen heroes, with text only on its navy half; flat navy everywhere else.
- Type: Ubuntu Sans. The bold key phrase plus regular line stays the voice. No italics.
- Signature device, "de bubbel": one silhouette (the beeldmerk outline, never redrawn). Variables: fill (navy, aqua, white, photo), content (number, price, arrow, pictogram, photo), tail direction in 45 degree steps (the tail points where you go on signage), size from the grid. Max one bubble per surface, two on large signs.
- Grid: 8 px on screen, 8 mm on print and signage modules; bubble widths 3, 5, 8 or 13 units.
- Imagery: ParkingYou's own garages and streets, daylight, no colour overlay; people shown inside the bubble mask.

**Why it fits.** It keeps nearly all recognition, uses shapes the handbook already defines (volvlak, afbeeldingsmasker, verloop bubble) and the cheapest rollout of the three: most signs only change colour discipline.

**Risks.** The bubble can turn into wallpaper; the pin reading sits close to Indigo's pin-O; it is the least "2027" of the three; the gradient keeps a production exception.

**Distance from today: 2 of 5.**

## 4. Direction B: Helder

**Idea.** Flip the colour weight. Aqua becomes the big brand field, navy becomes the ink. This takes the one colour position no Dutch operator holds and makes ParkingYou recognisable in a two second scroll. The ring and dot of the beeldmerk become a small kit: the dot is "jij, hier", the ring is "jouw plek", the arc is movement. Round geometry against the category's diagonals.

**Core system.**
- Logo: unchanged shapes, navy wordmark on aqua (4.80:1). New variant needed: on an aqua field the aqua dot disappears, so the dot turns white (proposal, needs your approval). On navy signage the reverse logo.
- Colour roles: aqua field (screens, social, print, card), navy for all text and icons, white for calm areas, orange as a small "nu" dot or deal marker only. In the garage the roles swap back: navy faces with white type (11.26:1) and aqua as a band, because aqua turns dark under sodium and mesopic light.
- Type: Ubuntu Sans with the width axis: condensed bold (wdth 75) for headlines and long street names, normal width for body.
- Signature device, "ring en stip": circles on one grid. The ring frames a place, the solid dot marks you or a free spot, the arc (from the existing scheidingsboog) links. Circles also crop photos. State logic: filled dot is vrij, open ring is vol.
- Grid: 12 columns, circle diameters in 4 sizes (1, 2, 4, 8 units of 24 px or 25 mm).
- Imagery: bright, warm daylight, people arriving; round crops; never dark garage interiors in marketing.

**Why it fits.** Strongest stand out in the category, friendly without being childish, fits the "digitaal waar het kan, menselijk wanneer het moet" tone, and the ring and dot come straight from the logo.

**Risks.** Aqua on translucent lightbox film is hard to match (RAL 6027 leans green); every text on aqua must be navy, which takes discipline; a bigger visible change for regulars; reprint cost on signage that turns aqua.

**Distance from today: 3.5 of 5.**

## 5. Direction C: Route

**Idea.** ParkingYou gets you from the street, to a spot, to where you were going. The signature is one continuous line, "de routelijn", that runs in from the edge of every format and ends at a destination: the dot of the beeldmerk, a price, a button, a level. In the garage it becomes a real wayfinding band on walls and columns. Colours are coded by task, like Schiphol: navy for driving, aqua for walking, orange for paying and attention.

**Core system.**
- Logo: unchanged; the aqua dot is where every line ends.
- Colour roles by task: navy = rijden (portals, route boards for cars), aqua = lopen (pedestrian routes, exits, lifts; with navy text), orange = betalen en let op (terminals, tariffs, storing; with deep navy text). White and paper grounds on screen, navy grounds in the garage.
- Type: Ubuntu Sans; tabular figures for prices, times and levels; very large numerals for levels.
- Signature device, "de routelijn": one stroke weight per format (equals the grid unit), only straight runs and quarter turns with one fixed radius (2 units), always starts at a format edge, always ends at a destination dot. On signage it is a 100 mm band at a fixed height; in motion it draws itself (under one second, static under reduced motion).
- Grid: unit = line weight; 8 px screen, 25 mm signage.
- Imagery: documentary, real routes and entrances, top down and eye level; fewer, bigger photos.

**Why it fits.** It is about what ParkingYou actually does, it is the most disciplined and wayfinding-led (the empty "friendly but as clear as TfL" quadrant from R2), and the task colours solve where orange and aqua belong.

**Risks.** The line can become decoration if the "starts at an edge, ends at a destination" rule slips; wall bands add installation work; task colours only work if every sign family follows them; the bubble shape plays a smaller role.

**Distance from today: 3 of 5.**

## 6. Side by side

| | A Bubbel | B Helder | C Route |
|---|---|---|---|
| Lead colour | navy | aqua (navy in garage) | white or navy, colour by task |
| Signature device | bubble container | ring, dot, arc | continuous route line |
| Type | Ubuntu Sans | Ubuntu Sans, condensed headlines | Ubuntu Sans, tabular figures |
| Gradient | kept, two stops, printed only | dropped | dropped |
| Stand out in category | medium | high | medium to high |
| Signage rework | low | medium to high | medium |
| Distance from today | 2/5 | 3.5/5 | 3/5 |

Combining is possible: for example, A's bubble as the content container with C's task colours in the garage, or B's aqua field for marketing with A's navy signage.

## 7. Decisions for Rick at Gate 1

1. Pick a direction, or name the elements to combine.
2. Orange CTA: orange with deep navy text, or a navy CTA with orange kept for prices only?
3. The nine stick figures: retire, or redraw in the new style for signage only?
4. Canva brand kit: may we update it in Phase 3 (write access), or deliver values only?
5. The live site palette (#192AA2, #0AD3E6, #FF8400) and voordeligparkeren.nl: in scope for the rollout plan?

## 8. Open questions from research (not blocking Gate 1)

- Which garages still have sodium or TL lighting? A sample board test in one real garage is advised before colour sign-off (R4).
- Who runs Instagram and Facebook; is TikTok @parkingyou yours (R1)?
- Which Aeroparker booking screens can be styled (R1)?
- Can All Jobs' cutters and RIP take variable fonts, or outlines only (R3)?
- Which storing number is current: 085 4011647 or 085 21 30 422 (R1)?
