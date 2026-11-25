// Search spots (ZoekSpot): a typed search, a carousel of the matching locations and a CTA.
// Every location from locaties.ts is in at least one search. Text between [ ] is typed in bold.
// The CTA says "reserveer" only when every location in the search has online booking (RESERVEERBAAR).

export type Zoekopdracht = {
  slug: string;
  zoek: string;
  /** Location slugs from locaties.ts, in carousel order (1 to 4). */
  locaties: string[];
  /** Why these locations, or what to check before posting. */
  noot?: string;
  /** Replaces the second pill on a card for this search (location slug to text), for example the distance to a venue. */
  kenmerk?: Record<string, string>;
};

export const zoekopdrachten: Zoekopdracht[] = [
  {
    slug: 'avondje-psv',
    zoek: 'Avondje [PSV]?',
    locaties: ['td-gebouw', 'dll-garage', 'dll-parkeerdek'],
    kenmerk: {'td-gebouw': '1,4 km naar het stadion', 'dll-garage': '1,8 km naar het stadion', 'dll-parkeerdek': '1,8 km naar het stadion'},
    noot:
      'Philips Stadion en Philips Bedrijfsschool zijn volgens de site niet beschikbaar tijdens wedstrijden en grote evenementen, daarom niet in deze zoekopdracht. DLL is ma-vr open vanaf 17:00. ' +
      'Afstanden: looproute via OpenStreetMap (25-11-2026) van Frederik van Eedenplein 1 (1379 m) en Kanaalstraat 2 (1841 m) naar het Philips Stadion.',
  },
  {slug: 'amsterdam', zoek: 'Voordelig parkeren in [Amsterdam]?', locaties: ['plantage', 'cruquius', 'zeeburgerkade', 'bos-en-lommerplantsoen']},
  {slug: 'amsterdam-west', zoek: 'Parkeren in Amsterdam [West]?', locaties: ['b-amsterdam-b1', 'bos-en-lommerplantsoen']},
  {slug: 'rotterdam', zoek: 'Dagje [Rotterdam]?', locaties: ['hofplein', 'shopping-center', 'europoint', 'maashaven']},
  {slug: 'eindhoven', zoek: 'Dagje [Eindhoven]?', locaties: ['evoluon', 'philips-stadion', 'philips-bedrijfsschool', 'victoriapark']},
  {slug: 'dierentuin', zoek: 'Naar de [dierentuin]?', locaties: ['plantage', 'diergaarde-blijdorp'], noot: 'Plantage ligt naast Artis, Blijdorp naast Diergaarde Blijdorp.'},
  {slug: 'film', zoek: 'Avondje naar de [film]?', locaties: ['stationsweg-ypenburg', 'pr-schiedam-centrum', 'lentse-plas', 'pathe-ede'], noot: 'Naam Pathé alleen als tekst, zonder logo (partnerregel).'},
  {slug: 'den-haag', zoek: 'Parkeren bij [Den Haag]?', locaties: ['at-the-park', 'stationsweg-ypenburg']},
  {slug: 'zoetermeer', zoek: 'Shoppen in [Zoetermeer]?', locaties: ['p1-belgielaan', 'p2-bovenlangs', 'p4-luxemburglaan', 'p5-amsterdamstraat']},
  {slug: 'zoetermeer-stadshart', zoek: 'Even naar het [Stadshart]?', locaties: ['p2-onderlangs', 'p8-nederlandlaan', 'p9-duitslandlaan']},
  {slug: 'almere', zoek: 'Dagje [Almere]?', locaties: ['p1-carlton-wtc', 'p2-mandela-wtc']},
  {slug: 'heerhugowaard', zoek: 'Shoppen in [Heerhugowaard]?', locaties: ['heerhugowaard-p1-zuidtangent', 'p2-middenwaard']},
  {slug: 'zaandam', zoek: 'Dagje [Zaandam]?', locaties: ['houthavenkade']},
];
