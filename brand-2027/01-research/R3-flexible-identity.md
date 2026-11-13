## R3 Flexible identity best practice

### Key findings

1. **Systems that last fix one form and vary a few named parameters.** Systems that kept generating new logo forms were reined in.

| Case (agency, year) | Constant | Variables | Scale / physical |
|---|---|---|---|
| TfL roundels (Basic Elements Standard, issue 8) [1] | Roundel form, never redrawn | Mode colour and name in the bar; 12 roundels | Min. 12 mm wide, clear zone 0.25 × bar width |
| Hamburger Hochbahn (Strichpunkt, 2025-26) [2] | Red, word and logo mark | Divisible grid; "Stipples" modules from the logo circle, from icons to generative visuals | Service and information media |
| Transavia (Studio Dumbar/DEPT, Oct 2025) [3][4] | 2015 equity | Bolder logo acts as a cursor: "spinning, moving, highlighting key messages" | Motion mainly digital |
| Evri, ex-Hermes (Superunion + Monotype, Mar 2022) [5][6] | Hermes blue, name | Variable logo font with an "Expressive" axis; 194,481 combinations; generator can lock letters and save codes | Trucks, uniforms, slips |
| City of Melbourne (Landor, 2009) [7][8] | Faceted M | Fill and pattern per sub-brand | Still in use after 10 years |
| MIT Media Lab (TheGreenEyl 2011; Pentagram 2014) [9][10] | 2014: 7×7 grid | 2011: about 40,000 shapes × 12 colours; 2014: one monogram plus 23 group glyphs | The algorithm was dropped after 3 years |
| Visit Nordkyn (Neue, about 2010) [11] | Base mark | Live wind and temperature (-25 to 25 °C), updated every 5 minutes | Web only |

2. **How these systems avoid chaos:** a locked mark, minimum sizes and clear zones [1]; one grid unit taken from the mark [2][10]; and generators whose outputs can be locked and saved [6].
3. **Delivery is token-driven.** The Design Tokens spec became stable as version 2025.10 on 28 Oct 2025, with tooling in Style Dictionary, Tokens Studio and Terrazzo [12]. Figma variables switch contexts through "modes" [13]. A parametric logo can ship as a variable font plus a generator [6].
4. **Variable fonts are ready on screen but not in production.** Browser support is above 97% [14]. InDesign supports them, but PDF export writes static instances [15]. Outlined variable text can leave overlapping shapes, which cause problems on vinyl cutters [16]. Support in sign-making RIP software is unconfirmed (assumption: none).
5. **Ubuntu Sans is the direct successor to Ubuntu.** It shipped with Ubuntu 24.04 and was added to Google Fonts on 22 Mar 2024. Axes: wdth 75-100, wght 100-800. Licence: Ubuntu Font Licence 1.0. Designers: Dalton Maag, DJR and Dual Type [17][18]. Its letterforms are narrower than Ubuntu's [19].
6. **Alternatives** (free and variable [18]): Inter (OFL; wght 100-900, opsz 14-32); Atkinson Hyperlegible Next (OFL, 2025, built for low-vision readers; wght 200-800, 150+ languages [20]); IBM Plex Sans (OFL; wdth 75-100, wght 100-700); Mona Sans (OFL; wdth 75-125, wght 200-900). Satoshi is free for commercial use under the Fontshare/ITF licence, but redistribution is limited; check the licence text [21]. Paid contrast: FF Transit, a narrowed Frutiger made for BVG Berlin, needs a commercial licence [22]. The Dutch road-sign face ANWB-Uu has no public licence that we could find [23].
7. **Lasting principles vs trends:**

| Lasting | Why |
|---|---|
| One constant, few variables | TfL's 12 roundels and Melbourne's M are still in use [1][8] |
| Accessible design as standard | Agency leaders name it as the 2026 default [24] |
| Tokens as the single source of truth | It is infrastructure, not a style, and the spec is stable [12] |
| Motion with written rules | "Create the rules so they can recognise exactly which ones to break" [24] |
| Distinctiveness, evolution over reset | Cracker Barrel reverted its 2025 logo within two weeks after its stock fell more than 10% [25]; D&AD calls the sans-serif sameness trend one "in its last days" [26] |

| Likely to date by 2029 | Why |
|---|---|
| Motion-only logos ("static wordmarks are the new dinosaurs") [27][28] | Signs, vinyl and print stay static |
| Neo-brutalism, noise, analog texture [27] | A reaction to AI output that will swing back |
| "Curated maximalism" [24] | Already contested in the same survey [24] |
| AI-boosted mascots [27] | Tied to a tool hype cycle |
| Random generative marks | MIT 2011 lasted 3 years [9][10] |
| Serif revival against blanding [26] | A pendulum swing, not a principle |

### What this means for ParkingYou

- **The speech bubble becomes the constant**, like TfL's roundel. Variables are token-bound only: fill (solid, gradient, photo), colour, content (level "0", section "1A", price, arrow) and crop. The grid unit comes from the bubble ring (assumption).
- **Ubuntu Sans (variable) replaces Ubuntu.** It keeps the same DNA at no licence cost. The width axis fits long Dutch street names on narrow route boards and condensed reel captions. The current wordmark outlines stay unchanged (assumption).
- **Design with the variable font, produce from fixed files.** Freeze 4 to 6 named instances (for example 400/100, 700/100, 700/75). Signage suppliers get outlined artwork with overlapping contours merged.
- **One DTCG token file**, with Figma modes for "screen" and "print/signage", ends the parallel palettes (two blues, two aquas, two oranges).
- **The bubble points.** Following Transavia's cursor idea, the bubble's tail is a moving pointer in reels and a static direction marker on route boards.

### Open questions

- Does Ubuntu Sans hold up against today's Ubuntu at signage weights, and will Rick accept narrower letterforms? This needs a side-by-side test.
- Can All Jobs' cutters and RIP software take variable fonts, or only outlines?
- Should colour vary by city or garage (like TfL's modes), or stay as one fixed set?
- Should the wordmark be redrawn in Ubuntu Sans or kept?
- Who owns the `remotion/` templates and the token build?

### Sources

1. [TfL Basic elements standard, issue 8](https://content.tfl.gov.uk/tfl-basic-elements-standards-issue-08.pdf)
2. [Strichpunkt x Hamburger Hochbahn](https://www.strichpunkt-design.de/en/feed/post/neuer-markenauftritt-der-hamburger-hochbahn)
3. [Studio Dumbar: Transavia](https://studiodumbar.com/work/transavia)
4. [LBB: Transavia refresh](https://lbbonline.com/news/Transavia-Enters-New-Era-of-Travel-with-Brand-Refresh)
5. [Dezeen: Evri rebrand](https://www.dezeen.com/2022/04/12/hermes-variable-font-logo-rebrand-evri-design/)
6. [Monotype: Evri case study](https://enterprise.monotype.com/resources/case-studies/evri)
7. [Designboom: Landor rebrands Melbourne](https://www.designboom.com/design/landor-rebrand-melbourne)
8. [City Nation Place: Melbourne](https://www.citynationplace.com/what-melbournes-flexible-design-identity-shows-us-about-the-value-of-a-logo)
9. [The Next Web: MIT 40,000 variations](https://thenextweb.com/news/mit-media-labs-new-logo-has-40000-variations)
10. [Pentagram: MIT Media Lab](https://pentagram.com/news/mit-media-lab)
11. [Neue: Visit Nordkyn](https://neue.no/work/visit-nordkyn/)
12. [W3C DTCG: first stable version](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)
13. [Figma: design systems are semantic](https://www.figma.com/blog/the-future-of-design-systems-is-semantic/)
14. [caniuse: variable fonts](https://caniuse.com/variable-fonts)
15. [Adobe Community: variable fonts in InDesign](https://community.adobe.com/t5/indesign/variable-fonts-in-indesign/td-p/10718647)
16. [Adobe Community: outlining variable fonts for cutters](https://community.adobe.com/t5/indesign-discussions/adobe-indesign-how-to-convert-a-variable-font-inter-to-outline/m-p/15355859/highlight/true)
17. [Canonical: Ubuntu Sans fonts](https://github.com/canonical/Ubuntu-Sans-fonts)
18. [Google Fonts metadata (ufl/ubuntusans, ofl/inter, ofl/atkinsonhyperlegiblenext, ofl/ibmplexsans, ofl/monasans)](https://github.com/google/fonts)
19. [Wikipedia: Ubuntu (typeface)](https://en.wikipedia.org/wiki/Ubuntu_(typeface))
20. [LBB: Atkinson Hyperlegible Next](https://lbbonline.com/news/applied-design-launches-atkinson-hyperlegible-next-typeface)
21. [Fontshare ITF FFL](https://www.fontshare.com/licenses/itf-ffl)
22. [Fonts In Use: FF Transit](https://fontsinuse.com/typefaces/2598/ff-transit)
23. [typography.guru: Dutch traffic sign typefaces](https://typography.guru/journal/traffic-sign-typefaces-the-netherlands-r29/)
24. [Transform: predictions for 2026](https://www.transformmagazine.net/articles/2026/crystal-ball-transform-readers-predictions-for-2026/)
25. [Global News: Cracker Barrel scraps new logo](https://globalnews.ca/news/11351967/cracker-barrel-new-logo-scraps-rebrand)
26. [D&AD: Beyond the sans serif (Oct 2025)](https://www.dandad.org/insights/features/beyond-sans-serif-how-type-can-move-blanding-awards-insights)
27. [BUCK: 2026 predictions](https://pencilsdown.buck.co/p/looking-ahead-bucks-2026-predictions)
28. [The Dieline: LogoLounge 2026, motion as main theme](https://thedieline.com/logoloung-releases-its-2026-trend-report-and-everything-is-on-the-move/)
