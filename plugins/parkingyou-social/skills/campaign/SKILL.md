---
name: campaign
description: Maakt een samenhangende ParkingYou-campagneset voor één evenement of actie (bijvoorbeeld GLOW, Koningsdag, kerst, een nieuwe locatie): fases, posts, carrousel, aftellen, stories en reelkaarten met één look en één planning. Use for "campagne", "campaign", "contentreeks voor [evenement]", "posts voor GLOW", "actie aankondigen", "opening nieuwe locatie".
---

# ParkingYou campaign

The GLOW 2026 set (`social/glow-2026/README.md`, branch `glow-2026-social`) is the model: a brief per piece, phases with dates, and one look.

1. **Brief.** Event or action, dates, locations (kennisbank codes), offer, audience, budget for paid posts. Partner names, logos and deals need approval (`references/decisions.md` S10); ask before using them.
2. **Phases.** Usually: bekendheid (2 to 3 weeks before), reserveren (the last 2 weeks), live (during), nazorg or retargeting (after). Each phase gets 1 to 3 feed pieces and a story sequence.
3. **Plan the set** as a table: id (`<CAMPAIGN>-A`, `-B`, ...), phase, posting date, archetype, format, headline. Typical mix: `evenement` (announce), `stappen` or `carrousel` (how), `prijs` (offer), `aftellen` (one per day, last week), story frames, reel cover.
4. **Shared look.** Same ground, same eyebrow ("Glow · 7 t/m 14 november"), same CTA wording across the set. Put the shared values in every spec; never in a new template.
5. **Facts once.** One `facts.json` for all campaign locations; copy it next to every spec.
6. **Render the set** with one `render.py` call (all specs at once) and make a contact sheet (`scripts/contact_sheet.py`, phase 3) to review the set side by side.
7. **Deliver** the planning table, the contact sheet, the PNGs per phase, and the captions. Note per piece when it may go live (for example only on evenings when the garage has room).
