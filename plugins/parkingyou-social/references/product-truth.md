# Product truth: what a post may claim

The kennisbank is the only source for locations, prices, opening hours, subscriptions and facilities.
Supabase project `parkingyou-platform` (id `qqzcmgzjtejvxmqltwns`), schema `kennisbank`. Read only; never write to it from this plugin.
Everything else that a post claims must be in section 3 of this file. If it is not, leave it out or ask Rick.

## 1. How to fetch facts

Use the Supabase connector (`execute_sql`) or `scripts/facts.py` (phase 3). Always filter on current rows:
`geldig_tot is null or geldig_tot > now()`.

| Need | Table | Key columns | Note |
|---|---|---|---|
| Location, city, type, reservable | `locatie` | `code`, `naam`, `plaats`, `type`, `reserveren_mogelijk`, `status`, `website_url` | `code` is the short ID used in `content-library.json` (`PLA`, `HOF`) |
| Facilities | `locatie_specificatie` | `plekken_totaal`, `doorrijhoogte_m`, `overdekt`, `camerabewaking`, `elektrisch_laden`, `lift`, `rolstoeltoegankelijk`, `betalen_*`, `gecontroleerd_op` | Empty = unknown, `false` = checked and absent. **Only claim a facility when the value is `true`** |
| Drive-up, online and early-booking prices | `tarief` | `soort`, `variant`, `kanaal`, `prijs`, `eenheid`, `dag_van`/`dag_tot`, `tijd_van`/`tijd_tot`, `vanaf_minuut`/`tot_minuut`, `geldig_vanaf`, `geldig_tot` | Staffels via `vanaf_minuut`/`tot_minuut` (for example the first 120 minutes free) |
| Subscriptions | `abonnementsvorm` | `naam`, `prijs_per_maand`, `servicekosten_per_maand`, `btw_percentage`, `voorwaarde`, `toegang` | See open point "subscription prices" in `decisions.md` |
| Opening hours | `openingstijd` | day 1 = Monday ... 7 = Sunday | Close earlier than open = runs past midnight; empty close = no fixed closing time |
| Access rules | `toegangsregel` | | Match days, closed days |
| Charging details | `laadvoorziening` | | **Empty** (0 rows on 2026-11-23): never state a number of charging points or a power rating |

## 2. Snapshot and price check

- Every rendered post that shows a price, a count or a facility stores a facts snapshot next to it: the query, the values and the date (`renders/<id>/facts.json`).
- Prices are never final in a cache. A post with a price gets `price_check: true` and is checked against `tarief` on the day it is posted.
- Prices change every February (price change playbook). After 1 February every price item goes back to "Prijs check".

## 3. Stable facts (checked 2026-11-23)

### 3.1 Reservable locations (14)

`reserveren_mogelijk = true` in `locatie`:

| City | Locations |
|---|---|
| Amsterdam | Bos en Lommerplantsoen (`BLO`), Cruquius (`CRU`), Plantage (Artis) (`PLA`), Zeeburgerkade (`ZEE`) |
| Eindhoven | DLL garage (`DLLG`), DLL parkeerdek (`DLLP`), Evoluon (`EVO`), Philips Bedrijfsschool (`PBE`), Philips Stadion (`PSV`), TD Gebouw (`TDG`) |
| Rijswijk | Parking At the Park (`PAR2`) |
| Rotterdam | Europoint (`EUR`), Hofplein (`HOF`), Shopping Center (`SHO`) |

Re-check this list with a query before a campaign; it is cached here only so copy checks can run offline.

### 3.2 Network

- 46 active locations in Almere, Amsterdam, Den Haag, Dordrecht, Ede, Eindhoven, Heerhugowaard, Nijmegen, Rijswijk, Rotterdam, Schiedam, Tilburg, Utrecht and Zoetermeer (`locatie.status = 'actief'`).
- Do not state a total number of locations in a post without querying it that day.

### 3.3 Products and ways to pay

| Fact | Source | Note |
|---|---|---|
| Three price levels at most reservable locations: ter plaatse, online reserveren, vroegboeken | `tarief.kanaal` | Use the actual three prices of that location |
| Strippenkaart (10 or 25 days) | `tarief.aantal_strippen` | |
| Subscriptions: 24/7, Office, Avond/weekend, Bewoners, Bedrijf | `abonnementsvorm.naam` | Availability differs per location |
| Doelgroeptarieven (Artis, Pathé) | `tarief.variant` | Partner approval needed before naming the tariff (D S10) |
| P+R Schiedam Centrum, weekdays, with train travel | `tarief` for `SCE` | |
| Night rates (Hofplein, Plantage) | `tarief` | |
| Pay at the machine with pin and contactless; EasyPark at some locations | `locatie_specificatie.betalen_*` | EasyPark is a third-party mark |
| Phone number for help | `085 401 16 47` | D S2 |
| Website | `parkingyou.nl` | D S1 |

## 4. Do not claim

| Claim | Why | Status |
|---|---|---|
| "Gegarandeerd", "altijd plek", "garantie" | Not confirmed that a reservation is guaranteed when the display shows "vol" | Open (IG-051) |
| A number of charging points or a charging power | `laadvoorziening` is empty | Open (IG-048) |
| "Inclusief" or "exclusief" btw or servicekosten on subscriptions | Table comment and columns disagree | Open, see `decisions.md` |
| "De eerste 2 uur gratis" for all Zoetermeer garages | Confirmed for P1 Belgiëlaan only | Open (IG-014) |
| "Gratis" anything | Only with valid action terms | Ask per post |
| Numbers of customers, reviews, ratings, quotes | Not available, and not our style | Never |
| "Goedkoopste", "beste", "nummer 1" | No source | Never |
| A location is open on a holiday or event night | Check `openingstijd` and `toegangsregel` for that date | Per post (IG-043) |
| Reservation for a non-reservable location | Not possible | Never (section 3.1) |
| Prices of competitors or street parking | Need a dated source in the post notes | Per post (IG-009) |
| Anything a partner offers (Glow Night Card, Artis-lid rate, Pathé rate) | Partner approval | Per post (D S10) |
