# Decisions log (social plugin)

Every conflict between sources that was settled for social. Rules in the other reference files cite these IDs.
Newest at the bottom. Change a decision by adding a new row that supersedes the old one; never edit history.

| ID | Date | Topic | Decision | Supersedes / sources |
|---|---|---|---|---|
| S1 | 2026-11-23 | URL in visuals and captions | `parkingyou.nl` everywhere. `voordeligparkeren.nl` is no longer used in new posts. | Posts and reels used `voordeligparkeren.nl` (`social/remotion/README.md`); GLOW, 2027 core spec and `strategy.md` §5 used `parkingyou.nl` |
| S2 | 2026-11-23 | Phone number for social | `085 401 16 47` (as on IG-036, Maashaven and the A3 storing poster). | `docs/print-rules.md` §7.2 lists `085 21 30 422` on the barrier banner as an open conflict |
| S3 | 2026-11-23 | Theme | Two themes on the same post spec: `feed` (current feed style, v2) is the default; `2027` is added after it and becomes the default when social switches to the 2027 identity. | `brand-parkingyou.md`, `brand-2027/02-build/core-spec.md` |
| S4 | 2026-11-23 | Render engine | The Remotion kit in `social/remotion/` renders statics (stills) as well as motion. No second engine. | `social/glow-2026/build.py` (Python to SVG) stays as an archived campaign build |
| S5 | 2026-11-23 | Formats | Instagram and Facebook feed 4:5, carousel 4:5, story 9:16, reel 9:16 with cover. LinkedIn 1:1 and 1.91:1 only for pillar P6 (business). No TikTok. | `strategy.md` §5 |
| S6 | 2026-11-23 | Backlog | `social/instagram/content-library.json` is the default backlog and the source for texts; Notion "ParkingYou Instagram contentbibliotheek" is the source for status and reach. | `social/instagram/README.md` |
| S7 | 2026-11-23 | Form of address | "je/jij" on every channel. | `strategy.md` §7, 2027 core spec §10 (they agree) |
| S8 | 2026-11-23 | Emoji | Only as markers at the start of a fact line in captions (📍 🅿️ 💶 🔌 🗓️). Never in a visual, a headline or a story frame, in both themes. | `strategy.md` §7 allows markers; 2027 core spec §10 says no emoji |
| S9 | 2026-11-23 | Dashes | No em dashes or spaced en dashes. Use a comma, period or colon. | `strategy.md` §7, 2027 core spec §10, Rick's writing rules |
| S10 | 2026-11-23 | Names of third parties | A venue name may appear as plain text when it names or locates our location (Plantage (Artis), Diergaarde Blijdorp, Philips Stadion, Pathé Ede are location names in the kennisbank). A partner-specific tariff or promotion (Artis-lid, Pathé-tarief, Glow Night Card) and any partner logo need the partner's approval and are flagged by QA until confirmed. | `strategy.md` §7, README "Third-party marks" |
| S11 | 2026-11-23 | Plugin location | `plugins/parkingyou-social/` in py-assets, reading the library directly, installed as a local plugin through a marketplace file in the repo. A claude.ai skill export is a later, optional step. | |
| S12 | 2026-11-23 | Base branch | `claude/parkingyou-social-plugin`, from `main` with `claude/zealous-cray-arlagn` merged in. `brand-2027/` comes in from `claude/parkingyou-brand-refresh-hz67bb` when the 2027 theme is built. | |

## Open (needs Rick or the kennisbank)

| Topic | Question | Blocks |
|---|---|---|
| Subscription prices | The kennisbank table comment says "inclusief btw en servicekosten", but `abonnementsvorm` has a separate `servicekosten_per_maand` column (5.00) and posts say "exclusief €5 servicekosten". Which is it? | Every P6 post with a price (IG-054, IG-055, IG-056, IG-058) |
| 2027 switch date | When does social move to the 2027 identity? | Which theme is the default (S3) |
| Reservation guarantee | Is a reservation a guaranteed spot when the display shows "vol"? | IG-051 and any "gegarandeerd" wording |
| Free first 2 hours in Zoetermeer | Confirmed for P1 Belgiëlaan only | IG-014 |
| Easter action | Terms of "gratis bij je volgende reservering" | IG-063 if reposted |
