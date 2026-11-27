// "Parkeer en stap over" (OverstapSpot): park, walk to the station or metro, ride on. A line map like a metro map with three
// stops (parking, walk, station) and a departure board with the places the location page names. Every fact from the page.

export type Overstap = {
  slug: string;
  /** Location slug from locaties.ts. */
  locatie: string;
  vraag: string;
  sub: string;
  /** Price pill at the parking stop, for example "Hele dag vanaf €7". */
  prijs: string;
  /** Walking time to the station as the page states it; "naast de deur" when it is right next to it. */
  lopen: string;
  station: string;
  vervoer: 'trein' | 'metro' | 'bus';
  /** Places the page names as destinations; empty when the page names none (the board then shows the station only). */
  naar: string[];
  /** Condition to show small under the price, if any (for example a P+R rate). */
  voorwaarde?: string;
  bron: string;
};

export const overstappen: Overstap[] = [
  {
    slug: 'at-the-park',
    locatie: 'at-the-park',
    vraag: 'Met de trein naar Den Haag?',
    sub: 'Parkeer in Rijswijk en stap over:',
    prijs: 'Hele dag vanaf €7',
    lopen: '7 min.',
    station: 'Station Rijswijk',
    vervoer: 'trein',
    naar: ['Den Haag', 'Delft', 'Rotterdam'],
    bron:
      'Locatiepagina At the Park: "Je loopt vanaf de garage in zeven minuten naar het station" en "zet je auto hier neer voor € 7 tot € 9 per dag ' +
      'en reis met de trein door naar Den Haag, Delft of Rotterdam". Dagkaart €12, met reservering €9, vroegboekkorting €7.',
  },
  {
    slug: 'stationsweg-ypenburg',
    locatie: 'stationsweg-ypenburg',
    vraag: 'Met de trein naar Den Haag?',
    sub: 'Parkeer naast station Ypenburg en stap in:',
    prijs: 'Hele dag maximaal €23',
    lopen: 'naast de deur',
    station: 'Station Ypenburg',
    vervoer: 'trein',
    naar: ['Den Haag Centraal', 'Rotterdam', 'Delft'],
    voorwaarde: 'Open van 07:00 tot 01:00',
    bron: 'Locatiepagina: "direct naast station Ypenburg", "stap in de trein richting Den Haag Centraal, Rotterdam of Delft"; €1,25 per 20 min, max. dagtarief €23; open 07.00-01.00.',
  },
  {
    slug: 'pr-schiedam-centrum',
    locatie: 'pr-schiedam-centrum',
    vraag: 'Met de trein naar Rotterdam?',
    sub: 'Parkeer bij Schiedam Centraal en stap over:',
    prijs: 'P+R €3,64 per dag',
    lopen: '4 min.',
    station: 'Schiedam Centraal',
    vervoer: 'trein',
    naar: ['Rotterdam', 'Den Haag'],
    voorwaarde: 'Met OV-chipkaart, ma-vr bij inrijden 05:15-19:00',
    bron: 'Locatiepagina: "op vier minuten lopen van station Schiedam Centraal", "met de trein of de metro binnen een paar minuten in Rotterdam en met de Intercity snel richting Den Haag"; P+R-tarief €3,64 per dag met OV-chipkaart, NS-Business Card of e-ticket, alleen ma-vr bij inrijden 05:15-19:00.',
  },
  {
    slug: 'p1-carlton-wtc',
    locatie: 'p1-carlton-wtc',
    vraag: 'Met de trein verder?',
    sub: 'Parkeer bij Almere Centrum en stap over:',
    prijs: '€3,00 per uur',
    lopen: '4 min.',
    station: 'Station Almere Centrum',
    vervoer: 'trein',
    naar: [],
    bron: 'Locatiepagina: "station Almere Centrum ligt op korte afstand, dus je kunt hier je auto neerzetten en met de trein verder" (geen bestemmingen genoemd). Looproute OpenStreetMap 286 m (3,8 min).',
  },
  {
    slug: 'p2-mandela-wtc',
    locatie: 'p2-mandela-wtc',
    vraag: 'Met de trein verder?',
    sub: 'Parkeer bij Almere Centrum en stap over:',
    prijs: '€6,00 per dag',
    lopen: '3 min.',
    station: 'Station Almere Centrum',
    vervoer: 'trein',
    naar: [],
    bron: 'Locatiepagina: "Almere Centrum ligt op korte afstand, dus je kunt hier ook je auto neerzetten en met de trein doorreizen". Looproute OpenStreetMap 187 m (2,5 min). €6 per dag is een open check (IG-013).',
  },
  {
    slug: 'evoluon',
    locatie: 'evoluon',
    vraag: 'Met de bus verder?',
    sub: 'Parkeer bij het Evoluon en stap over:',
    prijs: 'Hele dag vanaf €9',
    lopen: 'naast de inrit',
    station: 'Bushalte Evoluon',
    vervoer: 'bus',
    naar: ['Strijp-S', 'Eindhoven centrum', 'Eindhoven Airport'],
    bron: 'Bushalte ongeveer 10 meter van de inrit; de ene kant op naar Strijp-S en Eindhoven centrum, de andere kant op naar Eindhoven Airport (Rick, 27-11-2026). Haltenaam "Evoluon" volgens OpenStreetMap. Dagtarief €10, met reservering €9.',
  },
];
