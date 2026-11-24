---
name: social-post
description: Maakt een on-brand statische social post voor ParkingYou (Instagram/Facebook 4:5, story 9:16, LinkedIn 1:1 of 1.91:1) uit een idee, een brief, een item uit de contentbibliotheek (IG-0NN) of "bedenk er een", met caption, alt-tekst en QA. Use for "maak een post over...", "werk IG-013 uit", "ParkingYou Instagram post", "social post for ParkingYou", "LinkedIn-post over abonnementen", "statische post", "feedpost".
---

# ParkingYou social post

Works only inside a checkout of py-assets. Paths below are relative to the repo root.

## Workflow

1. **Load the rules.** Read `plugins/parkingyou-social/references/README.md`, then `decisions.md`, `brand-voice.md` and the theme section of `brand-visual.md` (`feed` unless the user or `decisions.md` says `2027`).
2. **Pin the idea.** One location, one reason, one price at most. From an item ID: take hook, caption and assets from `social/instagram/content-library.json`. Without a brief: pick with the rules in `references/pillars-and-angles.md` §4 and check the Notion database "ParkingYou Instagram contentbibliotheek" for what was posted recently.
3. **Choose the archetype and formats.** `plugins/parkingyou-social/schema/archetypes.json` lists slots, limits, grounds and formats per archetype; use only archetypes with `"status": "built"`. Formats per channel: `references/platform-specs.md`.
4. **Fetch the facts.** For every location code in the post, run the queries in `plugins/parkingyou-social/scripts/facts.sql` with the Supabase connector (read only) and save `facts.json` next to the spec. Never take a price, count or facility from memory or from the library text; `references/product-truth.md` §4 lists what never to claim.
5. **Write the spec** as `spec.json` (schema: `plugins/parkingyou-social/schema/post-spec.schema.json`). Headline with `*key phrase*`, caption in the shape of `brand-voice.md` §5, alt text, 3 to 5 hashtags, `price_check: true` when a price is shown.
6. **Render and check:** `python3 plugins/parkingyou-social/scripts/render.py <spec.json>`. Output: `social/posts/<date>-<id>-<slug>/` with a PNG per format, `@2x` versions, `caption.md` and `qa.json`.
7. **Fix every blocking finding** in `qa.json` and render again. Read each warning and either fix it or say in the reply why it stands (for example a price that was checked today).
8. **Look at every PNG yourself** with the checklist in `skills/brand-check/SKILL.md` §2. When a flaw comes from the archetype, not from this post, report it instead of patching around it.
9. **Deliver:** send the PNGs, show the caption, and list open points (price to re-check on the posting day, partner approval, photo still missing). Reply in Dutch, short.

## Do not

- Invent a price, a facility, an opening time or a partner deal.
- Use an archetype or theme that is not built; say what is missing instead.
- Edit the brand library (`svg/`, `tokens.json`, `elements.json`, `applications/`) or `brand-2027/`.
