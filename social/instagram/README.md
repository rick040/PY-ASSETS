# Instagram strategy and content library

| File | What |
|---|---|
| `strategy.md` | Where we are (reach per format), goal, audience, the 7 content pillars, format mix, weekly rhythm, backlog rules, copy and visual rules, Remotion build plan, open checks |
| `content-library.json` | Single source: pillars, 12 templates (7 Remotion reel templates, 5 static) and 66 items with hook, scenes or slides, Dutch caption, PY-ASSETS IDs, price-check flag and notes |
| `content-library.md` | The same library, readable. Generated, do not edit by hand |
| `build_library_md.py` | `python3 -I social/instagram/build_library_md.py` rewrites `content-library.md` from the JSON |
| `brand-parkingyou.md` | Brand reference for building reels and posts: tokens, which asset to use for what, layout, product facts |

The working backlog (status, posted date, reach) lives in the Notion database "ParkingYou Instagram contentbibliotheek". The JSON is the source for the texts and template props; Notion is where you track what has been made and posted.

Prices come from the kennisbank (Supabase `parkingyou-platform`, schema `kennisbank`) as of 5 November 2026. Every item with `price_check: true` must be checked against `kennisbank.tarief` before it is posted, and again after the February price change.

The reels are built with Remotion in `../remotion/` (template R1 Locatiekaart is built; IG-002 is rendered in `../remotion/renders/`).
