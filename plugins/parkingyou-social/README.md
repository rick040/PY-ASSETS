# parkingyou-social

On-brand ParkingYou social posts from the PY-ASSETS brand library: feed posts, carousels, stories, reel covers and campaigns,
with facts from the kennisbank and automatic copy, facts and brand checks. Status: phase 3 (all archetypes, both themes, all checks).

## Install

In Claude Code, from the root of a py-assets checkout:

```
/plugin marketplace add ./
/plugin install parkingyou-social@py-assets
```

Requirements: Python 3 (Pillow and jsonschema recommended), Node 22, Chromium (the Remotion download, or `/opt/pw-browsers` in cloud sessions).
`render.py` runs `npm ci` in `social/remotion` the first time.

## Skills

| Skill | For |
|---|---|
| `social-post` | One static post from an idea, a brief or a library item, in one or more formats |
| `carousel` | 2 to 10 slides with an arc |
| `story-and-reel` | Story frames, reels from the R1 to R7 templates, reel covers |
| `campaign` | A coordinated set for one event or action |
| `content-plan` | A week or month of posts from the content library |
| `brand-check` | QA on any post, batch or loose image |

## How it works

```
idea / IG-0NN ──> spec.json ──> render.py ──> schema check ──> copy check ──> facts check ──> Remotion (PY-Post) ──> brand check ──> social/posts/<date>-<id>-<slug>/
                    ▲                                                            ▲
             schema/*.json                                         facts.json (kennisbank via scripts/facts.sql)
```

- Rules: `references/` (start with `references/README.md`).
- Archetypes, slots, limits, grounds and formats: `schema/archetypes.json`. Layouts: `social/remotion/src/social/archetypes/`.
- Architecture and decisions: `docs/architecture.md`, `references/decisions.md`.

## Quick test

```
python3 plugins/parkingyou-social/scripts/render.py <spec.json> --out /tmp/py-test
```
