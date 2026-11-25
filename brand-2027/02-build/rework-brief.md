# Rework brief: core spec v2 (variant 1 "Rustig" with own identity)

Read this first, then the files below. You are revising existing chapters, not starting over.

## What happened

At Gate 2 Rick (ParkingYou) reviewed all chapters and said:
"Oke ik vind dat we het moeten aanpassen en modernisering doorvoeren. Ik wil iets minder Oranje. En behoudt de elementen zoals de hoekige pijl in de repo als main pijl. Draai het logo niet. De halve boog moet terug, ook de stick figures."
He then chose variant 1 "Rustig" and added: "Ik mis wel wat eigen identiteit. Wees wat meer creatief."

The creative director answered with core spec v2. Everything marked **(v2)** in `core-spec.md` is new or changed; decisions D31 to D34 in its log supersede older ones.

## The change in one list

- **Orange**: only for paying in the garage (payment machines, tariff panels, fault and storing notices). No orange on screens, in marketing, in print, in social. The main button is PY-Blauw with white text (on dark surfaces PY-Aqua with PY-Diep text). Tokens already changed: `action.primary-*` is navy now.
- **Arrow**: the angular handbook arrow (`kit/assets/arrow-plain-*.svg`, `arrow-downleft-*.svg`) everywhere an arrow appears: signs, buttons, links, social. Never in a circle or bubble. Never a Tabler arrow or chevron.
- **Logo and bubble never rotate.** The bubble's tail always points down as in the beeldmerk. No arrows inside bubbles. No large background bubble any more.
- **De parkeerders**: the handbook stick figures are back, with the beeldmerk bubble as head in PY-Aqua (`kit/assets/figure-*-duo.svg`, `-duo-white.svg`, `-navy.svg`). One per surface, always standing on a line. This is the heart of the own identity: the logo becomes a person.
- **De stem**: the handbook half arc (`kit/assets/arc.svg`) opens a message, left of a headline; on signs it separates modules.
- **Het vak**: a parking deck from above, one bay is "jouw vak" (holds one figure or one bubble). Background for social, cards, newsletter, posters, screen headers, empty states. Never on wayfinding.
- **Per surface: the logo plus at most two of the five elements** (parkeerders, stem, vak, bubbel, pijl).
- **Verloop retired**: no gradients anywhere.
- **Layout**: more white (white and paper 47, navy 38, aqua 13 percent), larger type, one accent per surface. Still flat, still Ubuntu Sans, still the bold key phrase pattern.
- Task colours in the garage stay: navy is rijden, aqua is lopen, orange is betalen.

## Ambition

Rick wants more own identity and creativity. Do not just remove orange: make the five elements do real work in your chapter. Look for the moment where a parkeerder makes a layout feel like ParkingYou (a gastheer pointing at contact details, the loper on a pedestrian sign, the juicher in a confirmation, the zwaaier on a welcome banner), where the stem gives a headline its voice, where het vak says "jouw plek". Stay disciplined: the rules in section 4b are hard rules.

## Files to read

1. `brand-2027/00-intake/brief.md` (company, constraints)
2. `brand-2027/02-build/core-spec.md` (v2: sections 0, 1, 4, 4b, 5.2, 7, 8 and decisions D31 to D34)
3. `brand-2027/02-build/00-core/figures/identity-elements.png` (look at it) and `bubble-anatomy.png`
4. `brand-2027/02-build/kit/README.md` (figure kit, new assets at the end)
5. `brand-2027/02-build/gate2-feedback.md`
6. `brand-2027/tokens/tokens.json` and `contrast.md` (regenerated; do not edit, do not edit the generator)
7. Your chapter folder(s): the current `chapter.md` and `figures/*.html`

## How to work

- Keep what is still right. Rewrite what conflicts with v2. Add what v2 needs (the new elements in your chapter's context).
- Remove every trace of: orange buttons or prices outside the garage, the verloop, rotated bubble tails, arrows in bubbles or circles, the background bubble, "poppetjes vervallen", old decision numbers that are superseded (D14, D19 tail settle, D21 retire list).
- Figures: edit the HTML, render with `node brand-2027/tools/render.mjs <figures folder>`, look at every PNG (Read tool) and fix what is wrong. Delete a figure only if it no longer has a place; then also remove its HTML and PNG and its reference in the chapter. You may add figures.
- Chapter text: Dutch, plain and spoken, no fluff, no em dashes, no workstream jargon (no "B3", "creative director", "core spec v2"); say "de core spec" if needed. End with "## Do's en don'ts". A "## Voorgestelde waarden" section only for genuinely new values, with reason.
- Only values from the core spec and tokens. Real data from the repo, otherwise [placeholders].
- Never modify files outside your own chapter folders. Do not commit or push.
- Final reply: what changed per chapter, figures added, changed or removed, any proposed values, open questions.
