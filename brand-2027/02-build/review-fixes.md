# Review fixes, Phase 3

An independent reviewer checked the assembled guideline (`brand-2027/03-guide/volledig/ParkingYou-huisstijl-2027.md`, generated from `02-build/<NN>/chapter.md` by `tools/assemble_guide.py`). The creative director decided on every point; the decisions are D47 and D48 in `02-build/core-spec.md`. Read those two rows first.

## Rules for every fixer

- Only touch the files in your own scope (listed per group). Never touch core-spec.md, tokens, kit.css or another group's folder. Do not commit or push.
- Chapter text is plain, spoken Dutch: short sentences, je/jij, no marketing words, no em or en dashes as dashes, no English where Dutch works ("format unit" → "formaateenheid u", "lightbox" → "lichtbak", "full colour folie" → "folie in vierkleurendruk").
- **No process language in chapter text:** no D-numbers, no "Rick", no "repository"/"repo", no "voorstel", no "goedgekeurd", no "zie Voorgestelde waarden", no "(aanname)". The "Voorgestelde waarden" and "Open vragen/Open punten" sections are dropped by the assembler; a value that is decided must be stated in the body text.
- **Do's en don'ts, one format.** Keep the heading `## Do's en don'ts`. Below it one bullet list; every item starts with `**Wel:**` or `**Niet:**` (all Wel items first). No tables, no sub-headings, no English "Do/Don't".
- **Cross-references:** "hoofdstuk N, Naam" with the final numbers: 1 Introductie en merkprincipes, 2 Logo, 3 Kleur, 4 Typografie, 5 Grid en layout, 6 Patronen en designelementen, 7 Iconografie, 8 Beweging, 9 Fotografie en beeld, 10 UI/UX, 11 Stationery, 12 Toepassingen, 13 Do's en don'ts, 14 Bijlagen.
- Figure eyebrows are now sentence case (kit.css changed). Write eyebrow text in sentence case in the HTML.
- Phone: `[storingsnummer]` for the service number everywhere (not 085 401 16 47 or 085 21 30 422); `[telefoonnummer]` for a person's phone. Prices: only € 12,50 (Philips Stadion, dagtarief met reservering) is sourced; any other price in a figure becomes `[prijs]`. Price format "€ 12,50" with comma and two decimals.
- The bubble holds the amount only ("€ 12,50"); "per dag" stands next to the bubble. Levels with a real minus sign: "−1".
- The parkeerder bags-cheer is called **juicher** everywhere.
- Render changed figures: `node brand-2027/tools/render.mjs <folder>/figures/`, then look at each changed PNG (Read tool) and fix what is wrong.
- Final reply: per point what you did (point id), files changed, and anything you could not fix.

## Group A: 01-logo, 03-typografie, 04-grid

- **H1** Business card: the Stationery version (chapter 11) is the only one. `04-grid/chapter.md` (around line 37) and figure `04-grid/figures/voorbeelden-print.html`: rewrite the card to match `10-stationery/chapter.md` and `10-stationery/figures/key-business-card.png` (front flat PY-Blauw with only the reverse logo; back white: stem opens name and function, contact block, gastheer wijst 4u on the contact line), or reduce the Grid example to the grid only (margins, columns, u) without a different design.
- **H2** `01-logo/figures/location-examples.html` (line ~50): the orange "Reserveer je plek" pill becomes PY-Blauw with white text (or aqua with PY-Diep on a navy header). The subscription card in that figure must follow `11-toepassingen/figures/key-subscription-card.png` (flat navy, stem with "Abonnement / Evoluon", zwaaier on a short line) or be cropped out.
- **H4** `03-typografie/chapter.md` lines ~57 and ~147: on signs the stem is as high as the arrow or pictogram next to it. Table row ~75 and figure `03-typografie/figures/signage-sizing.html`: replace the "Routebord 10 m" (1600 x 400 rectangle, bilingual, korps 144, stem 298) by the real route board of chapter 12: a pill 200 mm high, cap height 70 mm, read at 7 m, Dutch only, stem 140 mm (= arrow height). Check the numbers against `11-toepassingen/chapter.md` (route boards section) and core-spec D42.
- **M1** `03-typografie/chapter.md` ~55: add that on orange payment signs the stem is PY-Diep.
- **M4** `03-typografie/chapter.md` ~45: Arial only in Word, PowerPoint, Outlook and the e-mail signature. HTML newsletters use Ubuntu Sans as webfont with Arial as fallback.
- **M8** `03-typografie/chapter.md` ~147 and the caption in `signage-sizing`: "het hoofdstuk bewegwijzering" → "hoofdstuk 12, Toepassingen". Check all other cross-references in your three chapters.
- **M21** `01-logo/chapter.md` ~95 ("Wil Rick hem houden"): rewrite neutrally ("Of de tagline blijft, beslist de merkbeheerder."). `03-typografie` ~183 "(aanname)": state it plainly or drop it. Remove all other process language.
- **M22** `04-grid/chapter.md` ~41 and `voorbeelden-print`: the pedestrian lightbox must be the chapter 12 product (1000 x 1000, cap 100 at 10 m, full logo, loper 540 mm, "Ingang", Dutch only; see `11-toepassingen/chapter.md` Entreelichtbak and `key-entrance-sign.png`), or name it as a different product. Prefer matching chapter 12.
- **M18** A4 poster in `voorbeelden-print`: bubble with the amount only, "per dag" next to it.
- **L9** `04-grid/chapter.md` ~39 A4 poster headline: cap 1.5u (Typografie says calm headlines 1.5u to 2u).
- **L17** `04-grid/figures/layoutpatronen.html` pattern 2: the loper must face the headline (use the -flip file if needed).
- **L1** `04-grid/chapter.md` ~72: juicher.
- **L8** level digits with a real minus sign in Typografie (~165).
- **L29** `03-typografie/chapter.md` ~185: suppliers get the official static Ubuntu Sans files from Canonical/Google Fonts, not instances we make ourselves (UFL §2c).
- **L34** English words in your chapters → Dutch.

## Group B: 02-kleur, 06-iconografie, 07-beweging, 08-fotografie

- **Kleur tone:** the production section (~line 184 onward) reads like a research report. Keep the decision tables (HEX, RGB, CMYK, Pantone, RAL, folie, ΔE value per choice) and a two-sentence method summary in the chapter. Move the full method (ΔE CIEDE2000, Bradford/D50, data sources, links, ICC profile names) to a new file `02-kleur/bronnen.md` with heading `### 14.4 Bronnen bij Kleur` (the assembler will append it to the appendix). In the chapter, point to it as "zie hoofdstuk 14, Bijlagen".
- **M1** `02-kleur/chapter.md` ~79: add "PY-Diep op oranje" as a stem colour (payment signs only).
- **M8** `02-kleur/chapter.md` ~182 "het hoofdstuk digitaal" → "hoofdstuk 10, UI/UX". Check all cross-references in your four chapters.
- **M21** Remove D-numbers in body text (02-kleur ~63, ~112, ~186) and other process words. `06-iconografie` ~53 "Deze waarden zijn goedgekeurd" → just state them. ~59 "Als voorstel … `06-iconografie/voorstel/`": describe the four redrawn pictograms as the standard and give their file location neutrally.
- **M6** `08-fotografie/chapter.md`: move the decided craft values from "Voorgestelde waarden" (~256-272) into the body under "Stijl" as a short table "Vaste waarden" (focal length, aperture, colour temperature, calm area, file format and size, resolution) and the photo bubble size 240 px at "Foto in de bubbel" (~81).
- **M5** `08-fotografie/chapter.md` ~58: add that photo thumbnails inside screen cards take `radius.m` (8 px); everywhere else photos have square corners.
- **L2** `07-beweging/chapter.md` ~66: the pose pairs are examples ("bijvoorbeeld"), not fixed pairs; mention loper → springer for a booking confirmation.
- **L7** `07-beweging` ~5, ~37: the tail of the bubble points to the bottom left ("naar linksonder"), as in the beeldmerk.
- **L13** `08-fotografie` ~89: correct the count ("28 shots in acht soorten plekken, waarvan één eventavond" or whatever is true).
- **L20** `06-iconografie`: make sure the text explains that the pedestrian pictogram has a round head and the parkeerder has the bubble head; if the redrawn pedestrian pictogram in your figures has a bubble-shaped head, give it a round head.
- **L34** `08-fotografie`: "lightbox" → "lichtbak"; "kernspecificatie"/"core spec" → "de basisregels van deze gids". English IPTC field names may stay in a table column, with Dutch labels.
- **L1** juicher everywhere in your chapters.

## Group C: 05-patronen and the gastheer -flip assets

- **M16 (asset)** `02-build/kit/assets/figure-cap-point-navy-flip.svg`, `figure-cap-point-white-flip.svg`, `figure-cap-wave-navy-flip.svg`, `figure-cap-wave-white-flip.svg`: today the body is mirrored but the head (bubble) is not, and the cap stays with the head, so the cap brim points away. Change these four files so the body AND the cap (brim) are mirrored while the bubble-shaped head keeps the logo orientation (tail bottom left). Compare with the unmirrored `figure-cap-*-navy.svg` to find the cap paths. Keep file names, viewBox and size identical. Render a test (HTML with both versions side by side on white and navy) in your scratch folder and look at it. Do not edit any other kit file.
- **M1** `05-patronen/chapter.md` ~176: "Op oranje: stem en pijl in PY-Diep, geen parkeerder."
- **M3 + L3** `05-patronen/figures/vlakke-grond.html`: the Nieuwsbriefkop tile on flat PY-Blauw with logo (reverse), stem in aqua, white headline, white zwaaier 96 px on a white 2 px line, caption "600 x 180 px. PY-Blauw. …". The Lege staat tile must match `09-ui/chapter.md` (zwaaier, "Je hebt nog geen tickets", short help text, navy button "Zoek een plek").
- **M11** Placeholders in `05-patronen/figures/parkeerders-*.html`: `[telefoonnummer]` (not `[telefoon]`); service number `[storingsnummer]`.
- **L1** juicher (already used; check consistency, also the kit README is not yours, leave it).
- **L12** ~176 "Op aqua: PY-Blauw pijl, stem en loper": reword as a colour rule ("Op aqua zijn pijl, stem en parkeerder PY-Blauw").
- **L18** `combinaties.html`: the arrow comes after the link text, not before.
- **L7** tail "naar linksonder" (~65, ~112): keep, it is correct.
- Unify the Do's format (see rules) and remove process language.

## Group D: 09-ui

- **M2** ~39: back arrow 16 px in a 44 x 44 px target.
- **M18** ~136 and figures `screens-key`, `desktop-location`, `dark-mode`, `availability-price`: the bubble holds the amount only ("€ 12,50"), "per dag" next to it.
- **M20 accessibility:** (a) `form-fields`: the checkbox/radio error state gets a message under the control ("Vink dit aan om door te gaan") with error icon, and the text names `aria-invalid` and `aria-describedby`; (b) map pins (~140): require a list view of the same locations, keyboard access, a text alternative per pin and zoom buttons as single-pointer alternative to dragging (WCAG 2.1.1, 2.5.7, 1.1.1); (c) the toast on `surface.inverse`: state text colour and its contrast (white on PY-Diep 18,16:1 in light; in dark mode check what the tokens give and state it; do not invent a token, mention it as an open point in your reply if missing); (d) add rows to the accessibility table for `lang="nl"`, headings and landmarks, a skip link, text spacing (1.4.12) and `aria-current` on the active tab.
- **M21** Remove "Rick vroeg om meer eigen identiteit" (~18), all D-numbers in body text (~3, ~140, ~146, figure caption "(D13)" in `availability-price`), "(aanname)" (~195).
- **L4** Prices in figures (`screens-key.html` ~57, `desktop-location.html` ~49-50, `availability-price`, `dark-mode`): keep € 12,50 for Philips Stadion; "€ 15" and "€ 1,50 per 30 min" become `[prijs]` (with "per dag"/"per 30 min" next to it as text).
- **L10** `feedback-chips`: orange.700 only as text or icon; the warning alert border becomes a neutral or orange.100 border, and the caption says "icoon of tekst".
- **L14** ~195: the EAA applies from 10 employees or more than € 2 million turnover (the micro-enterprise exemption is fewer than 10 employees and at most € 2 million). Say it plainly.
- **Tone:** this is the longest chapter. Tighten: keep components, states, screens, accessibility and UX text; shorten the token-architecture prose (the table stays). Target about 2,800 words. Plain voice like chapters 1 and 2.
- Unify the Do's format (no table).

## Group E: 10-stationery, 11-toepassingen

- **M7** `11-toepassingen/chapter.md` ~36, ~69 "(voorstel, zie hieronder)", ~150 "(was 272 px, zie Voorgestelde waarden)", figure `sign-route-boards` "stem PY-Diep (voorstel)": remove the pointers and the word voorstel; the values are decided.
- **M11** Service number `[storingsnummer]` in `key-subscription-card.html`, `newsletter.html`, `sign-terminal-stickers.html`, `sign-pylon-tariff.html`, `posters-stickers.html`, `vehicle-workwear.html` (and anywhere else in your folders). Person phone `[telefoonnummer]`.
- **M12** Entrance lightbox (`11-toepassingen/figures/py-signs.js` ~51-63, chapter ~48, ~50): the logo clear space is 0.5x the beeldmerk height (01-logo). Make it fit: reduce the beeldmerk (for example 150 mm, still at least 1.5 x the cap height) or the P module, and check the vertical sum (margins + logo + clear space + module + name) on the 1000 x 1000 face, for both faces. Update the chapter numbers.
- **M15** `py-social.js` ~9, ~31: the eyebrow on PY-Blauw becomes white, not aqua.
- **M4** Newsletter: Ubuntu Sans as webfont, Arial fallback (keep), consistent with the decision.
- **L5** `newsletter.html` ~32 "Voordelig parkeren zonder gedoe?" → no "voordelig" (for example "Parkeren zonder gedoe in [stad]").
- **L6** `newsletter.html` ~64: preheader is label-s 12 px (or body-s 14 px; pick the true token and name it right).
- **L15** `10-stationery` ~53: the contact line on the card back runs full width as a floor line ("vloerlijn"); say so.
- **L16** `sign-route-boards`: use the pictograms without the ring (see `06-iconografie` redraws) for euro and EV, or drop them.
- **L19** `sign-route-boards` "Centrum" board: at least 0.3x the module height of air between the loper's hand and the text.
- **L24** Column band "1A" (~35): korps 90 (or what fits the 60 % content square of the 195 mm bubble; measure with the real font if you can).
- **L25** Long names: add a rule for the subscription card (~118) and the business card (~50): names longer than 18 characters go to print-h3 or wrap over two lines; show nothing cut off.
- **L26** Portal plate (~29): the P with roof must fit inside the 2u margins of the plate; fix the size.
- **L27** Height bar (~30): black cut vinyl letters on the white retroreflective band (black cannot be retroreflective).
- **L28** (~37): "RVS staanders" or "gepoedercoate stalen staanders in RAL 9006", not both.
- **L30** Thin white lines knocked out of navy on cards: at least 0.3 mm.
- **L31** Embroidery (~170): ask the supplier for a stitch-out sample before production.
- **L34** "format unit" → "formaateenheid u"; "full colour folie" → "folie in vierkleurendruk"; "key phrase" in figures → Dutch.
- **L2** Pose cuts (~142): say "bijvoorbeeld".
- Chapter 11 title: the H1 may stay "Drukwerk en kantoor"; the guide calls the chapter "Stationery".
- M21: remove process language (D-numbers ~40, ~99, ~160 in 11; ~56 "repository", ~128 in 10). Unify the Do's format.
- Note: Group C changes the gastheer -flip SVG files (cap brim mirrored). You do not need to do anything for that; your figures pick it up when rendered.
