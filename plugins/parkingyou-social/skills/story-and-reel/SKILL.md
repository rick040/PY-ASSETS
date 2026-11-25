---
name: story-and-reel
description: Maakt ParkingYou stories (9:16, een of meer frames) en reels met cover via de Remotion-kit (templates R1 tot R7). Use for "story", "storyreeks", "reel", "reelcover", "video voor Instagram", "maak IG-0NN als reel", "animatie", "9:16".
---

# ParkingYou stories and reels

## Stories (static frames)

1. Follow `skills/social-post/SKILL.md`, with format `story` (1080 x 1920). Safe zones: top 250 px, bottom 340 px, right 120 px (`references/platform-specs.md` §2).
2. A story sequence is several specs with the same `campaign` and ids ending in `-S1`, `-S2`. One message per frame; the last frame carries the CTA.
3. Polls and stickers are added in the Instagram app; leave room for them in the lower middle and say where in the reply.

## Reels (motion)

0. **Colour check first.** The reel kit's backgrounds (`social/remotion/src/v2/Backdrop.tsx`) still use drifting light, grain and the GLOW gradient, which decision S13 forbids. Until the kit is brought in line (open point in `references/decisions.md`), say so and ask before rendering a reel.
1. Reels use the seven templates in `social/remotion/` (R1 Locatiekaart, R2 Prijsrol, R3 Looproute, R4 Drie stappen, R5 Figuursketch, R6 Aftelkalender, R7 Kinetische tekst). Read `social/remotion/README.md` first.
2. An item becomes `social/remotion/src/items/IG-0NN.json` (copy the closest existing item and fill it from the library). Fetch every price and fact as in `skills/social-post/SKILL.md` step 4.
3. Run `python3 plugins/parkingyou-social/scripts/check_copy.py` on a spec that holds the reel texts and the caption, so reel copy passes the same rules.
4. Render stills across the timeline and look at them before the MP4: frame 0 never empty, nothing under the safe zones, headline on at most two lines.
5. Render the reel (`npm run render:...` or `npx remotion render PY-R<n>-<id>-Reel`); h264, BT.709.
6. Make the cover as a `story` post with the same headline, so it reads in the 4:5 feed crop and the 3:4 grid.
