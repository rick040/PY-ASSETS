---
name: brand-check
description: Controleert ParkingYou social content op merk, copy en feiten voordat het live gaat: een post-map, een batch, of een los aangeleverd beeld met tekst. Use for "check deze post", "mag dit online", "brand check", "QA", "klopt deze caption", "review de batch", "is dit on brand".
---

# ParkingYou brand check

## 1. Automatic checks

- A post folder or spec from this plugin: `python3 plugins/parkingyou-social/scripts/render.py <spec.json>` runs schema, copy, facts and brand checks and writes `qa.json`. Copy only: `python3 plugins/parkingyou-social/scripts/check_copy.py <post-dir>`.
- A loose image or text from elsewhere: put the copy in a minimal spec (caption, alt, `slots.headline`) and run `check_copy.py`; check the facts against the kennisbank by hand with `scripts/facts.sql`; the brand check of a loose image is the visual review below.

Severity: `block` = must be fixed before posting; `warn` = read it, fix it or explain why it stands; `info` = for the record.

## 2. Visual review (always, after the scripts)

Look at every PNG at full size and answer each line with yes or no:

1. One message: is it clear in one second what the post is about?
2. Hierarchy: headline first, then the visual, then the details?
3. Line breaks: no orphan word, no split name or price, key phrase on one line?
4. Space: no empty gap between headline and visual, nothing crowding the edges, the logo has its clear space?
5. Logo: the right version for the ground (`references/brand-visual.md` §3.2 or §4.2)?
6. Elements: theme `feed` at most one price badge; theme `2027` the logo plus at most two elements and exactly one parkeerder?
7. Formats: does the 4:5 feed version survive the 3:4 grid crop; does the story keep the safe zones?
8. Thumb stop: would this make someone stop scrolling? Would it stand next to the 15 posts in `social/remotion/renders/posts/`?
9. Truth: every price, count and facility backed by `facts.json` of today?

## 3. Report

Per post: status (klaar / aanpassen / niet plaatsen), the blocking findings, the warnings with a decision, and what to change. Short, in Dutch.
