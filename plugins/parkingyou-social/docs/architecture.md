# Architecture

Status: approved 2026-11-24. Built in phase 2: plugin manifest, marketplace, schemas, skills, the PY-Post composition with QA measuring, render-spec.mjs, render.py, check_copy.py, facts.sql and the archetype `typografisch` (theme `feed`).

## 1. Principles

1. **One post spec, many outputs.** A post is a JSON spec with slots (headline, price, location, facts, figure, cta). The same spec renders in every format and in both themes.
2. **One engine.** The Remotion kit in `social/remotion/` renders statics (stills), carousels, stories and reels (decision S4). No second renderer.
3. **No value written twice.** Colours, gradients and fonts come from the theme's tokens file; SVGs by element ID; facts from the kennisbank; rules from `references/`.
4. **Checks are scripts, not promises.** Copy, facts and brand are checked by code on every render. A blocking finding stops delivery.
5. **Reuse what works.** The v2 kit, the 7 reel templates, the content library and the GLOW campaign structure stay; the 15 hand-built posts become test fixtures.

## 2. Folder layout

```
.claude-plugin/marketplace.json                 repo root: lists the plugin, so it installs from this repo
plugins/parkingyou-social/
  .claude-plugin/plugin.json
  README.md                                     install, usage, how to extend
  docs/architecture.md                          this file
  references/                                   phase 1 (rules, decisions, facts, voice, specs)
  schema/post-spec.schema.json                  JSON Schema of a post spec (validated before render)
  skills/
    social-post/SKILL.md                        idea, brief or IG-id to finished static post(s)
    carousel/SKILL.md                           2 to 10 slides with an arc
    story-and-reel/SKILL.md                     9:16 story frames, reel cover, reels via R1 to R7
    campaign/SKILL.md                           a coordinated set for one event or promotion
    content-plan/SKILL.md                       a week or month of posts from the library
    brand-check/SKILL.md                        QA on any spec, batch or delivered PNG
  scripts/                                      Python 3, stdlib + Pillow
    render.py                                   spec -> facts check -> Remotion render -> QA -> output folder
    check_copy.py                               references/copy-rules.txt on slots, caption, alt text
    check_facts.py                              spec against its facts snapshot (reservable, facilities, prices)
    check_brand.py                              PNG + layout.json: palette, contrast on real pixels, safe zones, logo, slot limits
    contact_sheet.py                            one overview image per batch, with QA status per tile
    selftest.py                                 every element ID exists, every archetype renders in every format and theme, every rule parses
    facts.sql                                   the kennisbank queries the skills run through the Supabase connector

social/remotion/src/
  themes/feed.ts, themes/t2027.ts               theme = tokens + fonts + logo picker + element rules
  archetypes/<name>/                            one folder per archetype: slots.ts (zod schema + limits), Feed.tsx, T2027.tsx
  archetypes/PostComposition.tsx                one composition "PY-Post": props = post spec, size from format
  qa/measure.tsx                                in QA mode, measures every data-qa box and logs layout.json
social/remotion/scripts/render-spec.mjs         renderStill for each format and slide at 2x; also the text-hidden pass for QA

social/posts/<YYYY-MM-DD>-<id>-<slug>/          delivered output, committed
  spec.json  facts.json  caption.md  qa.json
  <format>.png  (carousel: feed-01.png ...)  layout-<format>.json
```

## 3. The post spec

Compatible with `content-library.json` items: `item` links to the library, `caption` and `hashtags` are copied from it when present.

```json
{
  "id": "IG-013",
  "item": "IG-013",
  "archetype": "prijs",
  "theme": "feed",
  "formats": ["feed", "story"],
  "ground": "glow",
  "slots": {
    "headline": "Een hele dag parkeren in Almere voor *€6.*",
    "price": { "amount": "6", "unit": "per dag", "from": false },
    "location": { "code": "P2MAN", "label": "P2 Mandela WTC" },
    "facts": [{ "icon": "py-atom-symbol-p-roof", "text": "250 overdekte plekken" }],
    "body": "250 overdekte plekken onder het WTC Almere",
    "cta": "url",
    "figure": null
  },
  "caption": "...",
  "alt": "...",
  "hashtags": ["#ParkingYou", "#Almere", "#parkeren"],
  "price_check": true
}
```

`*text*` marks the key phrase (bold), as in the kit's `Rich`. Every location is referenced by its kennisbank `code`, never by free text alone, so facts can be checked.

## 4. Archetypes (phase 3, 8 to 12)

Starting from the 5 static templates (S1 to S5), the 15 posts and the GLOW set. Each has named slots, character limits, allowed grounds and allowed atoms, and a `feed` and a `2027` layout.

| Archetype | From | Slots | Typical items |
|---|---|---|---|
| `prijs` | S1 Prijsposter | headline, price, location, 0 to 3 facts, cta | IG-013, IG-015, IG-022, IG-027, IG-043 |
| `locatie` | S2 Locatiefoto | headline, media (photo or illustration in the bubble), location, 3 facts, price (optional) | IG-004, IG-011, IG-049 |
| `prijsvergelijk` | IG-019, R2 as still | headline, 2 or 3 price rows, saving | IG-017, IG-018, IG-019, IG-054 |
| `stappen` | R4 as still, GLOW post E | headline, 3 steps with illustration | IG-028, IG-029, IG-035 |
| `abonnement` | IG-055, IG-058 | headline, 1 to 3 subscription rows, note, cta | IG-055, IG-056, IG-058 |
| `evenement` | GLOW B and D, 2027 event template | eyebrow, headline, date, locations, price (optional), figure | IG-039, IG-042, IG-044 |
| `aftellen` | GLOW F, R6 as still | big number, headline, event line | IG-037, IG-041, IG-047 |
| `service` | IG-036 | headline, contact (phone), instruction line, sticker reference | IG-031, IG-036 |
| `typografisch` | S4 | headline, subline | IG-040, IG-065 |
| `foto-kop` | S5 | photo, headline, body | IG-058, IG-063 |
| `carrousel` | S3 | cover (hook), point slides (icon, title, text), CTA slide | IG-005, IG-006, IG-020, IG-026, IG-030 |

Reels stay the 7 existing templates (R1 to R7); `story-and-reel` renders them from an item JSON and adds a reel cover via the archetype of the same item.

## 5. Facts

The plugin cannot call Supabase from a script, so facts come in through the skill:

1. The skill runs the queries in `scripts/facts.sql` with the Supabase connector (`execute_sql`, read only) for the location codes in the spec.
2. It writes the result to `facts.json` next to the spec, with the date and the queries.
3. `check_facts.py` compares the spec with `facts.json`: reserve wording only at reservable locations, a facility only when it is `true`, every price in a slot or caption equal to a current `tarief` or `abonnementsvorm` row, `price_check` set when a price is shown.

Without the connector, `check_facts.py` fails with "no facts snapshot" instead of passing.

## 6. QA

`render.py` runs every check in order and writes `qa.json`:

| Check | How | Blocks on |
|---|---|---|
| Schema | `post-spec.schema.json` + the archetype's slot limits | Missing slot, slot over its limit, unknown element ID |
| Copy | `check_copy.py` with `copy-rules.txt` | Any non-`WARN` rule |
| Facts | `check_facts.py` with `facts.json` | Claim not backed by the snapshot |
| Brand | `check_brand.py` on the PNG, a text-hidden PNG of the same frame and `layout.json` (boxes, colours and logo variant measured in the browser) | Text contrast below AA on the real pixels, text or logo in a safe zone, logo under minimum size or wrong variant for the ground, a colour outside the theme palette, a third-party mark without approval |
| Visual review | Claude looks at every PNG with the checklist in `brand-check/SKILL.md` | Judgement: hierarchy, breaks, empty gaps, thumb stop |

## 7. Install

From the repo root, in Claude Code:

```
/plugin marketplace add ./
/plugin install parkingyou-social@py-assets
```

Requirements: Python 3 with Pillow; Node 22 and `npm ci` in `social/remotion`; Chromium (the Remotion download, or `/opt/pw-browsers` in cloud sessions). The plugin only works inside a checkout of py-assets (decision S11).

## 8. Deviations from the PM-138 prompt

| Prompt | Proposal | Why |
|---|---|---|
| Build script writes editable HTML per post | The editable source is `spec.json` (texts and choices) plus Remotion Studio for live preview with a props panel | Remotion renders from React, not standalone HTML; exporting HTML would be a second engine |
| A separate `campaign` template system | `campaign` is a skill that writes several specs with a shared eyebrow, dates and ground | The archetypes already cover campaign pieces (GLOW maps onto `evenement`, `aftellen`, `stappen`, `prijs`) |
| QA reads hex colours from files | QA measures the rendered page and the PNG | Gradients and drifting light make file-level colour checks meaningless |
