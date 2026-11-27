# Meta-campagneplan per locatie (Facebook en Instagram)

Versie 1, 27-11-2026. Een advies, geen accountwijziging: er gaat pas iets live na akkoord van Rick.
Bestanden: `campagneplan-per-locatie.csv` (34 locaties, 23 advertentiesets, met video's, landingspagina en UTM per locatie).

## 1. Doel en uitgangspunten

| | |
|---|---|
| Doel | Reserveringen bij de 15 boekbare locaties, bezoek (klik naar de locatiepagina) bij de andere 19 |
| Doelgroep | Automobilisten van 40 jaar en ouder in de regio van elke locatie |
| Budget | €5 per locatie per dag, dus €170 per dag en ongeveer €5.100 per maand bij volledige uitrol |
| Kanalen | Facebook en Instagram (Reels, Stories, Feed); Advantage+ plaatsingen |
| Creatives | De bestaande videoseries uit `remotion/out/` (zie paragraaf 4) |

**Bekend uit de Instagram-strategie (Notion):** reels halen ongeveer 2,7 keer zoveel bereik als statische posts. Concreet en
lokaal werkt het best: één locatie, één prijs, één reden. "Reserveer" en "zeker van je plek" alleen bij boekbare locaties.
Prijzen moeten na 1 februari opnieuw gecheckt worden.

**Onbekend (status `unknown`, nodig voor betrouwbare verwachtingen):**

- Meta-account: is er eerder geadverteerd, en met welk resultaat?
- Pixel en Conversions API: staat de Pixel op parkingyou.nl, en ook op de reserveringsstap?
- Conversiemeting: wordt een afgeronde reservering als event (met waarde) naar Meta gestuurd?
- Economie: gemiddelde opbrengst en marge per reservering, en hoeveel een nieuwe klant waard is.

Zolang deze punten onbekend zijn, doet dit plan geen voorspellingen over kosten per reservering. Het begint met meting en
een kleine pilot.

## 2. Opbouw (campagnes en advertentiesets)

Twee campagnes, met per locatie een eigen advertentieset en een eigen budget. Zo houd je de €5 per locatie vast en zie je per
locatie wat het oplevert.

| Campagne | Doel in Meta | Advertentiesets |
|---|---|---|
| `PY | Reserveren | NL` | Verkoop met het reserveringsevent zodra dat gemeten wordt; tot die tijd Verkeer (weergaven van landingspagina) | 13 sets voor de 15 boekbare locaties |
| `PY | Bezoek | NL` | Verkeer (weergaven van landingspagina) | 10 sets voor de 19 andere locaties |

**Locaties die vlak bij elkaar liggen, delen één advertentieset.** Anders bieden ze tegen elkaar op bij dezelfde mensen.
Het budget blijft €5 per locatie:

| Advertentieset | Locaties | Budget per dag |
|---|---|---|
| Zoetermeer Stadshart | P1, P2 Bovenlangs, P2 Onderlangs, P4, P5, P8, P9 | €35 |
| Eindhoven DLL | DLL (Garage), DLL parkeerdek | €10 |
| Eindhoven Philips | Philips Stadion, Philips Bedrijfsschool | €10 |
| Amsterdam Oostelijk Havengebied | Cruquius, Zeeburgerkade | €10 |
| Almere WTC | P1 Carlton, P2 Mandela | €10 |
| Heerhugowaard Middenwaard | P1 Zuidtangent, P2 Middenwaard | €10 |

Alle andere locaties hebben een eigen set van €5 per dag.

## 3. Doelgroep per advertentieset

- **Locatie:** een straal rond de parking. 25 km in Amsterdam, Rotterdam, Den Haag/Rijswijk en Eindhoven (mensen die
  de stad in rijden), 15 km in de kleinere steden. Instelling "mensen die hier wonen of onlangs waren".
- **Leeftijd:** 40 tot 65+. Advantage+ doelgroep mag uitbreiden binnen deze grens.
- **Uitsluiten:** bestaande abonnementhouders, als die lijst beschikbaar is (aangepaste doelgroep).
- **Philips Stadion en Bedrijfsschool:** niet inzetten rond wedstrijden en grote evenementen (dan niet beschikbaar).

## 4. Creatives per locatie

Per advertentieset draaien 3 tot 5 video's tegelijk. Meta verdeelt het budget over wat het best werkt. De volledige lijst
per locatie staat in de CSV (kolom `video_9x16`). Basisset:

| Rol | Serie | Voor wie |
|---|---|---|
| Stoppen met scrollen | Het lijstje, Het appje | Iedereen in de regio |
| Bestemming | Het kaartje (POI), Het bordje, Zoekvideo | Mensen die naar een plek of evenement gaan |
| Overtuigen op prijs | Vroeg boeken loont | Alleen de 10 locaties met drie dagtarieven |
| Locatie leren kennen | Locatiespot reel | Iedereen |
| Seizoen | Amsterdam Light (alleen Plantage) | Tot het einde van het lichtfestival |

**Tekst bij de advertentie** (sjabloon, per locatie invullen; prijzen uit de kennisbank):

- Primaire tekst (eerste 125 tekens tellen): `<vraag uit de video> Parking <naam>: <feit>. <prijs met locatienaam>. Reserveer online en sta zeker van je plek.`
  Voor niet-boekbare locaties: `... Bekijk tarieven en openingstijden op parkingyou.nl.`
- Kop (max. 40 tekens): `Parking <naam> vanaf <prijs>` of `<bestemming>? Parkeer om de hoek`
- Knop: "Nu boeken" (boekbaar) of "Meer informatie".

**Formaten:** de video's zijn 9:16 (Reels, Stories) en 16:9. Voor de Feed is 4:5 beter. Actie: een 4:5-versie renderen
met dezelfde templates (kleine aanpassing in Remotion).

## 5. Meting

1. **Pixel + Conversions API** op parkingyou.nl: `ViewContent` op de locatiepagina, `InitiateCheckout` op "Reserveer",
   `Purchase` (met waarde en locatie) bij een afgeronde reservering. Controleren in Events Manager met een testreservering.
2. **UTM per advertentie:** staat klaar in de CSV (`utm_campaign` per doel, `utm_content` per locatie en video).
3. **Weekoverzicht per locatie:** bereik, kosten, klikken, weergaven van landingspagina, reserveringen (uit het
   reserveringssysteem, gekoppeld via UTM) en kosten per reservering.
4. **Videometrics:** percentage dat 3 seconden kijkt (hook) en percentage dat tot het eind kijkt, per serie. Zo leer je
   welke serie per stad werkt.

## 6. Fasering

| Fase | Wanneer | Wat | Eigenaar | Klaar als | Terugdraaien als |
|---|---|---|---|---|---|
| 0. Meting | Week 1 | Pixel en CAPI controleren, reserveringsevent testen, UTM's en uitsluitingen klaarzetten, 4:5-versies renderen | Rick (account), Claude (video, CSV) | Testreservering zichtbaar in Events Manager met waarde | Event komt niet door: pilot draait op Verkeer |
| 1. Pilot | Week 2 t/m 4 | 8 advertentiesets: Plantage, Hofplein, Oostelijk Havengebied (€10, twee locaties), At the Park, TD-gebouw, Shopping Center, Zoetermeer Stadshart (verlaagd naar €5) en Almere WTC (verlaagd naar €5). €45 per dag, ongeveer €945 totaal | Rick | Per set minstens 1.000 vertoningen per video en een eerste kosten per landingspaginaweergave | Een set heeft na 2 weken geen enkele klik naar de pagina: video's wisselen of set stoppen |
| 2. Uitrol | Week 5 t/m 8 | Alle 23 sets, €170 per dag. Per set de 2 best kijkende series uit de pilot voorop | Rick | Kosten per reservering (boekbaar) en per paginaweergave (bezoek) per locatie bekend | Budget terug naar pilotniveau als de kosten per reservering hoger zijn dan de marge per reservering |
| 3. Bijsturen | Vanaf week 9 | Budget verschuiven van locaties die slecht presteren naar locaties die goed presteren (niet meer overal €5). Nieuwe series testen (Past mijn auto?, Droog naar binnen) | Rick, met maandelijkse review | Maandelijks verslag per locatie | |

**Over het budget per set:** €5 per dag is klein. Op conversies optimaliseren werkt pas goed met genoeg reserveringen per week.
Hoeveel dat er zijn, weten we pas na de pilot (vertrouwen: laag tot er cijfers zijn). Daarom eerst op paginaweergaven, en per
campagne overstappen op het reserveringsevent zodra er genoeg reserveringen binnenkomen.

## 7. Spelregels

- Geen speciale advertentiecategorie nodig (parkeren valt niet onder huisvesting, krediet of werk).
- Partnernamen (Artis, PSV, Pathé) alleen als tekst, geen logo's. De festivalnaam alleen na afstemming met de organisatie.
- Prijzen altijd met de locatienaam; "vanaf" alleen voor de laagste van meerdere prijzen. Na 1 februari alle prijsvideo's
  opnieuw renderen (`Vroeg boeken loont`, `Het lijstje`, `Het kaartje`, locatiespots).
- Open checks vóór livegang: IG-013 (P2 Mandela €6 per dag), IG-014 (2 uur gratis Zoetermeer), IG-024 (Lentse plas,
  naam Pathé), 15 laadpalen Plantage, IG-051 (is een reservering gegarandeerd als het display "vol" toont).
- Frequentie: zijn mensen een video meer dan 3 keer per week gezien, dan nieuwe video's in de set.
- Wedstrijddagen PSV: Philips-sets pauzeren.

## 8. Werkritme

- **Maandag:** weekoverzicht per locatie (Claude kan dit uit een Meta-export en het reserveringssysteem maken).
- **Elke 2 weken:** zwakste video per set vervangen door een nieuwe serie.
- **Maandelijks:** budgetverdeling herzien, seizoensmomenten plannen (kerstinkopen, koopzondagen, carnaval Eindhoven,
  Koningsdag).
