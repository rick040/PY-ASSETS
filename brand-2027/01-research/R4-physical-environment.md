## R4 Physical environment

### Key findings

- **Letter height.** Research for the US Access Board puts the legibility limit at about 35 ft per inch of letter height for an average viewer, but only 17 ft/in for the weakest 15% of older viewers [1]. The sign trade sizes at 1 inch per 10 ft [2]. ADA 703.5.5 asks for 51 mm (sign 1.78 to 3.05 m high) plus 3.2 mm per 305 mm beyond 4.57 m, measured on the uppercase "I", non-glare finish [3]. Cap height in mm:

| Distance | Limit, average viewer (LI 35) | Weak older viewer (LI 17) | Trade rule (1 in/10 ft) | ADA, sign 1.78 to 3.05 m | Proposed PY minimum (assumption) |
|---|---|---|---|---|---|
| 5 m | 12 | 25 | 42 | 56 | 50 |
| 10 m | 24 | 49 | 83 | 108 | 100 |
| 20 m | 48 | 98 | 167 | 213 | 200 |
| 30 m | 71 | 147 | 250 | 318 | 300 |

- **Reading time.** MUTCD: 1 s per word or 2 s per unit of information, whichever is less, never under 2 s [4]. At 20 km/h a sign legible from 20 m is in view for about 3.6 s, so about 3 words. At the posted 5 km/h on ParkingYou portals [5] it is about 14 s. My own calculation.
- **Contrast.** BS 8300 asks for at least 30 points of LRV difference, UNECE uses 60 for signage [6]. EN 17210 has clauses on visual contrast (6.3) and signage (6.6) but leaves the numbers to CEN/TR 17621 and national rules [7]. Approximate LRVs (assumption, sRGB luminance proxy): navy 4, gradient mid stop 17, aqua 40, orange 35, white 85 to 100. Aqua on white passes the LRV test but fails WCAG (2.34:1), so WCAG is the stricter rule.
- **Light levels.** NEN 2443:2013 asks for an average of 75 lux on lanes and bays (uniformity 0.5). Older garages were built to 40 lux (NEN 2443:2000), or 40 on lanes and 20 on bays (NPR 1978) [8]. NEN-EN 12464-1 asks for 300 lux at entrances by day [9]. NSVV (2019) adds vertical illuminance at 1.2 m, because NEN 2443 "is niet op led geschreven" [8]. NEN 2443 is still the 2013 edition; a revision is "nog achter de horizon" [10]. Signify's reference plan replaces TL-D fittings with 4000 K LED (/840) [9].
- **Colour under poor light.** Low-pressure sodium is close to monochromatic at 589 nm, so colours are hard to tell apart [11]. High-pressure sodium has a CRI of about 22 [12]. Below about 3 cd/m² (mesopic), reds darken and blues brighten relatively [13]. A navy panel at 20 to 75 lux sits at about 0.3 to 1 cd/m², which is mesopic (assumption, L = E x LRV / π). Under sodium, navy and aqua both read as dark and orange reads close to white (assumption). Only lightness contrast survives every lamp.
- **Norms.** Bbl art. 4.215: escape-route signs follow NEN 3011, meet the NEN-EN 1838 visibility requirements, and stay visible for 60 min within 15 s of a power cut [14]. NEN 2443 still refers to the withdrawn NEN 6088 pictograms; new builds use NEN 3011 [15]. The CROW Ontwerpwijzer parkeergarages contains the ESPA checklist, which scores clearly marked floors and sub-areas, "use of colours for wayfinding", an illuminated entrance sign, and more than 150 lux in parking areas [16].
- **EAA.** From 28 June 2025 it covers payment terminals and e-commerce services. Terminals already in use may stay up to 20 years where the member state allows [17]. Signage is not on the product list (Art. 2).
- **Production.** Cut vinyl cannot reproduce gradients [18]. Translucent cut film comes in fixed ranges: 3M 3630 has 57 standard colours, and printing needs the separate IJ3630-20 [19]; Oracal 8500 has about 55 [20]. Oracal 751 lasts 7 years in colour, 8 in black and white, 5 in metallic [21]. Fluorescent film lasts a year or less outdoors [22]. Printed backlit faces need double strike or heavier saturation, which looks darker by day [23].

### What this means for ParkingYou

- Fix a minimum cap height per product. A 200 mm route board holds about 70 to 80 mm caps (assumption), so it works up to about 10 m. Messages read at 20 to 30 m go on portals, lightboxes or level markers.
- White on PY-Blauw is the signage workhorse. Aqua and orange are accent fields and never carry meaning alone. No white text on aqua or on the aqua end of the gradient (level markers, Mindervaliden boards).
- Gradient only on printed Dibond and printed wall foil. Define a flat fallback for cut vinyl, RAL powder coat and translucent faces; keep blockout-plus-white lightbox faces.
- Keep ISO 7010 / NEN 3011 safety signs and RVV signs unbranded, and keep brand colours away from safety green and red (assumption).
- Matte laminate on every face. Test sample boards in one real garage under LED, TL and sodium light before colour sign-off.

### Open questions

- Which garages still have sodium or TL lighting, and what are the measured lux at sign positions?
- What do the NEN 2443:2013 wayfinding clauses say (paywalled)? One unsourced search summary claims pedestrian signs must differ in colour from vehicle signs; not verified.
- Is the NEN-EN 12464-1 Ra minimum for car parks 20 or 40? Not verified.
- Is there a backlit swatch match for aqua? RAL 6027 leans green.
- Which terminals were bought after 28 June 2025? Legal check needed.
- What are the real cap heights on current route boards and level markers? The handbook does not give them.

### Sources

1. [US Access Board, VMS legibility](https://www.access-board.gov/research/communication/variable-message-signing/vms-legibility/)
2. [Garvey, IJSW, parallel-mounted letter height](https://journals.shareok.org/ijsw/article/view/48)
3. [2010 ADA Standards 703.5](https://www.corada.com/documents/2010ADAStandards/703-5)
4. [MUTCD 2009, Section 2L.05](https://mutcd.fhwa.dot.gov/htm/2009/part2/part2l.htm)
5. `docs/phase1-inventory.md`, RVV cluster on the portals (repo)
6. [Light reflectance value (BS 8300, UNECE)](https://en.wikipedia.org/wiki/Light_reflectance_value)
7. [EN 17210 contents (STN)](https://normy.normoff.gov.sk/norma/132639/nahlad); [CEN/TR 17621](https://standards.iteh.ai/catalog/standards/cen/9ac3881a-305b-4b6a-836f-5f436fc1203c/cen-tr-17621-2021)
8. [Vexpan, NSVV aanbeveling](https://vexpan.nl/artikelen/aanbeveling-verlichting-parkeren-nsvv/); [Maas Hagoort](https://www.maashagoort.nl/kennisbank/parkeergarageverlichting/)
9. [Signify lichtplan parkeergarage](https://www.assets.signify.com/is/content/PhilipsLighting/Assets/philips-lighting/netherlands/20191104-lichtplan-parkeergarage.PDF)
10. [SPARK, NEN 2443 inzichten 2024](https://spark-parkeren.nl/artikel-nen-2443-nieuwe-inzichten-in-de-toepassing/)
11. [Sodium-vapor lamp](https://en.wikipedia.org/wiki/Sodium-vapor_lamp)
12. [ACRP, Airport Parking Garage Lighting Solutions](https://nap.nationalacademies.org/read/22180/chapter/3) (figure from search extract; PDF not read)
13. [Purkinje effect](https://en.wikipedia.org/wiki/Purkinje_effect)
14. [Bbl art. 4.215](https://www.inview.nl/openCitation/idc2f99204417349cb85d096383430041d/besluit-bouwwerken-leefomgeving-artikel-4-215)
15. [NVFN Praktijkblad PB-03 Parkeergarages](https://www.nvfn.nl/wp-content/uploads/2020/03/Praktijkblad-PB-03-Parkeergarages.pdf)
16. [CROW Ontwerpwijzer, ESPA-checklist](https://kennisbank.crow.nl/public/gastgebruiker/PARK/Ontwerpwijzer_parkeergarages/Bijlage_III_ESPA-checklist/18785)
17. [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj/eng)
18. [MPL Signage, print vs cut vinyl](https://mplsignage.com.au/blog/digital-print-vs-cut-vinyl/)
19. [3M 3630 product card](https://www.sirvisual.com/Attachment/100/Product%20Card%203630.pdf)
20. [Oracal 8500](https://orafol.com/en/europe/products/oracal-8500-translucent-cal)
21. [Oracal 751C](https://www.orafol.com/en/europe/products/oracal-751c-high-performance-cast)
22. [Oracal 7510 fluorescent](https://signwarehouse.com/products/oracal-7510-fluorescent-premium-cast-24-in-x-10-yds)
23. [Signs101, translucent double strike](https://www.signs101.com/threads/translucent-vinyl-double-strike.109778)
