# Rework brief D44: het vak is retired

Rick (ParkingYou) reviewed three replacements for "het vak" (the parking-deck pattern with "jouw vak") and chose option A: **remove it, replace it with nothing**. Decision D44 in `brand-2027/02-build/core-spec.md`.

## The system now

- **Four own elements**: de parkeerders (one colour, always standing on a line), de stem (half arc), de bubbel (always upright), de hoekige pijl. Per surface: the logo plus at most two of them.
- **Backgrounds are flat** PY-Blauw or white (paper `blue.50` for quiet sections). No pattern, no deck, no bays, no stop line, no lane line, no "jouw vak", no decorative shape.
- Where het vak was used (social, subscription card, newsletter header, PWA ticket header, empty states, card backs, posters), the stem and one parkeerder standing on a short line carry the identity on a flat ground. A bubble may hold a price or level where it did before.
- The `vak.*` tokens are gone from `tokens.json`/`tokens.css`. Do not reference them.
- Everything else in core spec v2 stands (orange only for paying in the garage, navy main button, angular arrow, upright bubble, one-colour figures, no verloop).

## What to do

1. Read `brand-2027/02-build/core-spec.md` (sections 4, 4b, 5.2 and decision D44), `brand-2027/02-build/kit/README.md`, and your chapter folders (`chapter.md` and `figures/`).
2. Remove every trace of het vak from your chapters and figures: text, tables, rules, do's and don'ts, figure captions, helper scripts (`*.js`), and the drawings. "Vier elementen", never "vijf".
3. Redraw the affected figures on a flat ground with the remaining elements. Keep layouts calm (variant 1: much white, large type). A figure stands on a short 2 px line (screen) or 0.1u rule (print).
4. Delete figures that only existed for het vak (HTML and PNG) and remove their references in the chapter.
5. Render with `node brand-2027/tools/render.mjs <figures folder>`, look at every PNG (Read tool), fix what is wrong.
6. Dutch, plain and spoken, no em dashes, no workstream jargon. Only values from the core spec and tokens. Never touch files outside your folders. Do not commit or push.
7. Final reply: per chapter what changed, figures changed or deleted, open questions.
