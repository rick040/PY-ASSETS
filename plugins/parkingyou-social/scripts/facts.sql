-- Kennisbank queries for a post's facts snapshot (Supabase project parkingyou-platform, id qqzcmgzjtejvxmqltwns, schema kennisbank).
-- Run each block with the Supabase connector (execute_sql, read only). Replace :codes with the location codes of the spec,
-- for example ('HOF','PLA'). Save the four results in facts.json next to the spec:
--   { "date": "<YYYY-MM-DD>", "codes": [...], "locaties": [...], "tarieven": [...], "abonnementen": [...], "openingstijden": [...] }

-- locaties: identity, reservable, facilities
select l.code, l.naam, l.plaats, l.type, l.reserveren_mogelijk, l.status, l.website_url,
       s.plekken_totaal, s.doorrijhoogte_m, s.overdekt, s.camerabewaking, s.elektrisch_laden, s.lift,
       s.rolstoeltoegankelijk, s.betalen_pin, s.betalen_creditcard, s.betalen_easypark, s.gecontroleerd_op
from kennisbank.locatie l
left join kennisbank.locatie_specificatie s on s.locatie_id = l.id
where l.code in :codes;

-- tarieven: current prices only
select l.code, t.soort, t.variant, t.kanaal, t.prijs, t.eenheid, t.dag_van, t.dag_tot, t.tijd_van, t.tijd_tot,
       t.vanaf_minuut, t.tot_minuut, t.aantal_strippen, t.geldig_vanaf, t.geldig_tot, t.opmerking
from kennisbank.tarief t
join kennisbank.locatie l on l.id = t.locatie_id
where l.code in :codes and (t.geldig_tot is null or t.geldig_tot > now())
order by l.code, t.soort, t.kanaal, t.prijs;

-- abonnementen: current subscriptions only
select l.code, a.naam, a.prijs_per_maand, a.servicekosten_per_maand, a.btw_percentage, a.voorwaarde, a.toegang
from kennisbank.abonnementsvorm a
join kennisbank.locatie l on l.id = a.locatie_id
where l.code in :codes and (a.geldig_tot is null or a.geldig_tot > now())
order by l.code, a.naam;

-- openingstijden: day 1 = Monday ... 7 = Sunday; close earlier than open = past midnight; empty close = no fixed closing time
select l.code, o.*
from kennisbank.openingstijd o
join kennisbank.locatie l on l.id = o.locatie_id
where l.code in :codes;
