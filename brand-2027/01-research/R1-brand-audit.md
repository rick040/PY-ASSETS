## R1 Brand audit

Audit 2026-11-07; site captured at 1440x900 and 390x844; WCAG 2.x contrast.

### Key findings

- **Recognition carriers hold across channels.** The beeldmerk (pin bubble, ring, aqua dot) plus "parking" regular / "you" bold appears on every touchpoint checked: site header, PWA icon, Mailchimp header, lightboxes, terminal stickers [1][4][6][8]. Also carrying: the solid navy field with white bold Ubuntu, the "P with roof" (already reused in Canva headlines and location pills), the bold-plus-regular line, and the convex curve (pyloon header, site hero wave) [2][3][4][8]. The 9 stick figures appear on signage only, not on web or social [3][4][8].
- **Three palettes, not two.** Handbook: #1A3580 / #32B9CD / #F08300 [1]. Live site CSS: #192AA2 (21 uses), #0AD3E6 (13), #FF8400 (10), plus #1129D5 and rgba(19,66,216) [5]. Canva social and posters: #344F9E / #76C8DB, close to the Design System values #374E9D / #79CADC [8]. The site logo SVG mixes #0AD3E6 and #32B9CD; the PWA icon is #181FC3 [5][6]. With 15 print blues [2], at least 20 blues are in use.
- **Contrast fails on the main conversion points.** Every primary CTA ("Direct reserveren", "Zoeken", "Reserveren", "Abonnement aanvragen") is white on #FF8400 at 2.46:1; nav grey #777 on white is 4.48:1 [4][5]. In Canva, white on the teal location pill (#76DBD5) is 1.63:1 and #76C8DB headlines on #344F9E are 4.01:1 [8].
- **The website has no token discipline (fact).** Buttons use 4px radius, not the 999px pills in the Design System README; cards use 10, 12 and 15px; buttons come in orange, navy and black (booking map page) [4][5]. Headings are all-italic Ubuntu at weight 800, but only 300 to 700 are loaded [5][7]. Inter is loaded and unused [7]. main.css has "poUbuntu" 17 times where "pointer" was meant (dead cursor and pointer-events rules), and `--dark-blue` holds an orange (#d68902) [5]. The stack is jQuery, jQuery UI and Slick (main.css dated 20250619), not the Next.js + Payload site the brief describes [5].
- **Imagery has no rules.** Site heroes are stock lifestyle photos under a blue colour overlay; news thumbnails are iStock (file names); one home slider image is AI generated (file name `gemini_generated_image`) [4][5]. Location pages use real garage photos [4]. Canva mixes event photos, seasonal clip art and a purple gradient (#8B57FE, SAIL 2025); SAIL and Herfstdeal carry no logo, and Herfstdeal pushes voordeligparkeren.nl [8].
- **Dated in 2026/2027 terms (taste, marked as such).** Stick figures with waving arms and shopping bags read as 2010s wayfinding clip art (taste). All-italic heavy headlines, a 🙌 emoji and a typing animation in the hero, colour-overlaid stock photos and wave dividers follow 2015 to 2019 landing-page habits (taste) [4]. Raster 72 ppi gradients are dated in production terms, not taste [2]. What still looks current: flat navy faces with large white type on lightboxes and portals (taste) [3].
- **Social is thin and mostly unreachable.** Instagram @parkingyou_bv and Facebook /parkingyouNL (linked from the site) redirect to a login wall or return 429; LinkedIn returns 403. Not audited [9][10][11]. YouTube: 12 subscribers, 18 videos, newest about 2 years old [12]. TikTok @parkingyou exists with 0 followers and 0 videos, not linked from the site; ownership unknown [13]. The real social output is in Canva: an 8-page 2026 post/reel series (white card on blurred photo, navy price bubble, teal pill). Brand kit kADdn_gTcyQ exposes only its id and a logo thumbnail via the tool [8].
- **Gaps: touchpoints with no rules.** Web UI (buttons, forms, radii, states, icons: the site uses Material Icons, not the 12 navy pictograms), social formats (9:16, 4:5), photography, motion, newsletter (the Mailchimp header is a logo only), PWA (manifest theme_color #ffffff, blue #181FC3 icon), Aeroparker booking screens, display states (VOL, gesloten), the storing contact (three patterns, two numbers) and side domains (voordeligparkeren.nl) [1][2][5][6][8].

### What this means for ParkingYou

- One colour set with a hex, CMYK and RAL value per colour, pushed into site CSS, the Canva brand kit and print templates, would remove most drift at low cost. All channels already use a deep blue, so a navy close to #1A3580 stays the core (evolution).
- Orange cannot carry white text in any of its three versions (#F08300 2.64:1, #FF8400 2.46:1, #EE7D2C 2.76:1) [1][5]. Dark text works (#1D1D1B on #FF8400 is 6.88:1) or the orange moves darker; this choice decides the booking CTA.
- Keep the beeldmerk, the navy field, the P-roof and the bold/regular line. The P-roof is already used modularly in Canva, so it is the natural building block. The stick figures and the heavy all-italic headings are the first candidates to retire or redraw (taste).
- Write rules first where none exist: digital components, Canva social templates and photography, where today's drift is made.

### Open questions

- Where does the Next.js + Payload site of the Design System live? parkingyou.nl does not run it.
- Who runs Instagram and Facebook, and can Rick share exports? Is TikTok @parkingyou ParkingYou's own account?
- Aeroparker hand-off: the GLOW and search forms post to `/nl/goto-product/` and redirected to the homepage in a headless session. Which booking screens can be styled? A test link would help.
- Is voordeligparkeren.nl a sub-brand to keep or fold in?
- Which storing number is current: 085 4011647 or 085 21 30 422 [2]?
- No photos of real garages under real light are in the repo; a site visit is needed to judge signage legibility.

### Sources

1. [brand-2027/00-intake/brief.md](../00-intake/brief.md)
2. [docs/print-rules.md](../../docs/print-rules.md), sections 1, 4, 6, 7, 9; [tokens.json](../../tokens.json) `observed`; [applications.json](../../applications.json) (38 print applications)
3. [docs/phase1-inventory.md](../../docs/phase1-inventory.md), sections 7 and 8; renders sheet-app.png, sheet-el-1.png, sheet-el-2.png (session scratchpad)
4. Live pages: [home](https://parkingyou.nl/nl), [Eindhoven](https://parkingyou.nl/nl/locaties/eindhoven/cid=3), [Parking Philips Stadion](https://parkingyou.nl/nl/locaties/eindhoven/parking-philips-stadion/id=7), [Abonnementen](https://parkingyou.nl/nl/abonnementen), [ParkingPass](https://parkingyou.nl/nl/strippenkaarten), [booking map](https://parkingyou.nl/nl/parkeren/location=101/city=3), [GLOW](https://parkingyou.nl/nl/campagnes/glow), [PSV](https://parkingyou.nl/nl/campagnes/psv), [Zakelijk](https://parkingyou.nl/nl/zakelijk). /nl/evenementen and /nl/parkingpass return 404.
5. [main.css](https://parkingyou.nl/resources/css/main.css?v=20250619), [logo.svg](https://parkingyou.nl/resources/images/logo.svg?v=3), home page source and computed styles
6. [site.webmanifest](https://parkingyou.nl/nl/site.webmanifest?v=15), [PWA icon](https://parkingyou.nl/resources/images/meta/favicon-512x512.png)
7. Google Fonts requests in the page head: [Ubuntu 300 to 700](https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap), [Inter](https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap)
8. Canva, read only: brand kit kADdn_gTcyQ; designs [Mailchimp header](https://www.canva.com/d/RFlU4aKZfIslxKP), [reel series](https://www.canva.com/d/QMvxYODVpmLKfmc), [Herfstdeal](https://www.canva.com/d/KE7fCllidUYUXRS), [Abonnement Mauritsstraat](https://www.canva.com/d/d80rhv37CeUKfYs), [SAIL 2025](https://www.canva.com/d/ZCxuJV3szPL-pwa)
9. [Instagram @parkingyou_bv](https://www.instagram.com/parkingyou_bv/) (login wall / 429)
10. [Facebook /parkingyouNL](https://www.facebook.com/parkingyouNL/) (login redirect)
11. [LinkedIn](https://nl.linkedin.com/company/parkingyou) (403)
12. [YouTube channel](https://www.youtube.com/channel/UCRcAS_fzq4EGhPOqZ5B9pzg/videos)
13. [TikTok @parkingyou](https://www.tiktok.com/@parkingyou)

### Screenshots

All in `brand-2027/01-research/r1-screens/`.

- `web-home-desktop.png`, `web-home-mobile.png`: hero with blue overlay, italic headline, orange CTA, wave edge
- `web-location-eindhoven-city-desktop.png`, `-mobile.png`: city page with location cards
- `web-location-philips-stadion-desktop.png`, `-mobile.png`: location page, real garage photo with signage
- `web-abonnementen-desktop.png`, `-mobile.png`: orange and navy buttons side by side
- `web-parkingpass-desktop.png`, `-mobile.png`: ParkingPass page, stock photo hero
- `web-booking-step1-desktop.png`, `-mobile.png`: booking map with black "Zoeken" button
- `web-booking-datepicker-desktop.png`: jQuery UI date picker
- `web-campagne-glow-desktop.png`, `-mobile.png`, `-desktop-full.png`: GLOW event page
- `web-campagne-psv-desktop.png`, `-mobile.png`: PSV event page
- `web-zakelijk-desktop.png`, `-mobile.png`: B2B page
- `pwa-icon-512.png`: PWA icon (#181FC3)
- `canva-newsletter-header-mailchimp.png`: newsletter header
- `canva-reel-glow-dll-p1.png`, `canva-reel-plantage-p2.png`: 9:16 reel pages
- `canva-poster-herfstdeal.png`: seasonal poster, no logo
- `canva-poster-abonnement-mauritsstraat.png`: subscription poster
- `canva-social-sail-2025.png`: event post with purple gradient
