---
name: carousel
description: Maakt een ParkingYou-carrousel van 2 tot 10 slides (4:5) met een verhaallijn: hook, één punt per slide, slotslide met CTA. Use for "carrousel", "carousel", "swipe-post", "overzicht per stad", "uitleg in stappen als carrousel", "5 tips", or library items with format Carrousel (template S3).
---

# ParkingYou carousel

Follow `skills/social-post/SKILL.md` with these differences.

1. **Arc first.** Write the slides as a list before any design: slide 1 is the hook (it must work alone in the feed), slides 2 to n-1 make one point each, the last slide sums up and has the one CTA. 2 to 10 slides; fewer is better.
2. **Archetype `carrousel`.** Each entry in `slots.slides` has its own slide archetype (`carrousel-cover`, `carrousel-punt`, `carrousel-cta`) and limits in `schema/archetypes.json` → `slide_archetypes`.
3. **Rhythm.** Theme `feed`: alternate navy and light grounds per slide; a swipe cue on slide 1 only. Theme `2027`: navy and white.
4. **Facts per slide.** A city overview names locations by code, so `facts.json` covers all of them.
5. **Render** with `render.py`; slides come out as `feed-01.png`, `feed-02.png`, and so on. Check that slide 1 reads without the others and that the slides look like one set.
6. **Caption** repeats the hook and points to the swipe ("Swipe voor de zes plekken").
