// Location data for the LocatieSpot template (one video per location).
// Source: the public location pages on parkingyou.nl (opened 25-11-2026), except where `bron` says otherwise.
// Rule from the Instagram strategy: every price with the location name, "vanaf" only for the lowest of several prices.
// Hourly prices are worked out from the published rate (for example €1,25 per 20 min = €3,75 per uur).

export type Kenmerk = [licht: string, vet: string];

export type Prijs = {
  /** Big text in the bubble, for example "€6,98" (cents are drawn small) or "Gratis". */
  bedrag: string;
  /** Small line under the amount, for example "per uur". */
  eenheid: string;
  /** Show "vanaf" above the amount (lowest of several published rates). */
  vanaf?: boolean;
};

export type Locatie = {
  slug: string;
  /** parkingyou.nl location id */
  id: number;
  stad: string;
  /** Name without the word "Parking", shown bold after a light "Parking". */
  naam: string;
  /** Hook screen: bold question (wraps to two lines) and a light line under it. */
  hook: string;
  subhook: string;
  /** Exactly four check rows: light part, bold part. */
  kenmerken: [Kenmerk, Kenmerk, Kenmerk, Kenmerk];
  prijs: Prijs;
  /** Photo in public/locaties (cropped to the right-hand panel). */
  foto: string;
  url: string;
  /** Where the published rate comes from, in words, so it can be checked. */
  bron: string;
  /** Open check before posting, if any. */
  check?: string;
};

const pagina = (pad: string) => `https://parkingyou.nl/nl/locaties/${pad}`;

export const locaties: Locatie[] = [
  // Amsterdam
  {
    slug: 'plantage',
    id: 35,
    stad: 'Amsterdam',
    naam: 'Plantage',
    hook: 'Dagje Amsterdam al duur genoeg?',
    subhook: 'Parkeer voordelig',
    kenmerken: [
      ['15', 'Laadpalen'],
      ['483', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['10 min.', 'van centrum'],
    ],
    prijs: {bedrag: '€6,98', eenheid: 'per uur'},
    foto: 'locaties/35.jpg',
    url: pagina('amsterdam/parking-plantage/id=35'),
    bron: 'Per uur overdag €6,98. Hook, 15 laadpalen en luchtfoto uit het Jitter-ontwerp.',
    check: 'Aantal laadpalen (15) staat niet op de site; komt uit het Jitter-ontwerp.',
  },
  {
    slug: 'cruquius',
    id: 27,
    stad: 'Amsterdam',
    naam: 'Cruquius',
    hook: 'Naar het Oostelijk Havengebied?',
    subhook: 'Parkeer aan de Entrepothaven',
    kenmerken: [
      ['24/7', 'Open'],
      ['', 'Overdekte garage'],
      ['€25', 'dagtarief'],
      ['', 'Lift en rolstoeltoegang'],
    ],
    prijs: {bedrag: '€2,60', eenheid: 'per uur', vanaf: true},
    foto: 'locaties/27.jpg',
    url: pagina('amsterdam/parking-cruquius/id=27'),
    bron: '€1,30 per 30 min (ma-za 21-09u en zondag); overdag €2,60 per 30 min.',
  },
  {
    slug: 'zeeburgerkade',
    id: 45,
    stad: 'Amsterdam',
    naam: 'Zeeburgerkade',
    hook: 'Dagje Amsterdam Oost?',
    subhook: 'Parkeer overdekt en voordelig',
    kenmerken: [
      ['120', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['', 'Overdekte garage'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€2,60', eenheid: 'per uur', vanaf: true},
    foto: 'locaties/45.jpg',
    url: pagina('amsterdam/parking-zeeburgerkade/id=45'),
    bron: '€1,30 per 30 min (ma-za 21-09u en zondag); overdag €2,60 per 30 min.',
  },
  {
    slug: 'bos-en-lommerplantsoen',
    id: 21,
    stad: 'Amsterdam',
    naam: 'Bos en Lommerplantsoen',
    hook: 'Amsterdam zonder parkeerstress?',
    subhook: 'Met de tram naar het centrum',
    kenmerken: [
      ['168', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['15 min.', 'tram naar centrum'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€5,00', eenheid: 'per uur'},
    foto: 'locaties/21.jpg',
    url: pagina('amsterdam/parking-bos-en-lommerplantsoen/id=21'),
    bron: '€2,50 per 30 minuten.',
  },
  {
    slug: 'b-amsterdam-b1',
    id: 23,
    stad: 'Amsterdam',
    naam: 'B. Amsterdam (B1)',
    hook: 'Naar B. Amsterdam?',
    subhook: 'Parkeer voordelig in Nieuw-West',
    kenmerken: [
      ['853', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['€15', 'max. per dag'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€2,50', eenheid: 'per uur'},
    foto: 'locaties/23.jpg',
    url: pagina('amsterdam/parking-b-amsterdam-b1/id=23'),
    bron: '€2,50 per 60 minuten, max. dagtarief €15.',
  },

  // Rotterdam
  {
    slug: 'hofplein',
    id: 9,
    stad: 'Rotterdam',
    naam: 'Hofplein',
    hook: 'Dagje Rotterdam al duur genoeg?',
    subhook: 'Parkeer voordelig',
    kenmerken: [
      ['8 min.', 'van centrum'],
      ['24/7', 'Open'],
      ['€15', 'weekenddagtarief'],
      ['', 'Overdekte garage'],
    ],
    prijs: {bedrag: '€4,00', eenheid: 'per uur'},
    foto: 'locaties/9.jpg',
    url: pagina('rotterdam/parking-hofplein/id=9'),
    bron: '€2,00 per 30 minuten, max. dagtarief za en zo €15.',
  },
  {
    slug: 'shopping-center',
    id: 1,
    stad: 'Rotterdam',
    naam: 'Shopping Center',
    hook: 'Dagje shoppen in Alexandrium?',
    subhook: 'Parkeer voordelig',
    kenmerken: [
      ['3 min.', 'van centrum'],
      ['24/7', 'Open'],
      ['€12,50', 'dagtarief'],
      ['', 'Overdekte garage'],
    ],
    prijs: {bedrag: '€1,00', eenheid: 'eerste uur'},
    foto: 'locaties/1.jpg',
    url: pagina('rotterdam/parking-shopping-center/id=1'),
    bron: 'Eerste uur €1,00, daarna €1,25 per 30 min.',
  },
  {
    slug: 'europoint',
    id: 11,
    stad: 'Rotterdam',
    naam: 'Europoint',
    hook: 'Tussen Rotterdam en Schiedam?',
    subhook: 'Parkeer bij The Lee Towers',
    kenmerken: [
      ['24/7', 'Open'],
      ['€15', 'max. per dag'],
      ['', 'Overdekte garage'],
      ['', 'Cameratoezicht'],
    ],
    prijs: {bedrag: '€3,00', eenheid: 'per uur'},
    foto: 'locaties/11.jpg',
    url: pagina('rotterdam/parking-europoint/id=11'),
    bron: '€1,50 per 30 minuten, max. dagtarief €15.',
  },
  {
    slug: 'diergaarde-blijdorp',
    id: 127,
    stad: 'Rotterdam',
    naam: 'Diergaarde Blijdorp',
    hook: 'Dagje naar Blijdorp?',
    subhook: 'Parkeer naast de dierentuin',
    kenmerken: [
      ['1200', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['2 min.', 'naar de dierentuin'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€12,50', eenheid: 'per dag'},
    foto: 'locaties/127.jpg',
    url: pagina('rotterdam/parking-diergaarde-blijdorp/id=127'),
    bron: 'Dagtarief €12,50.',
  },
  {
    slug: 'maashaven',
    id: 129,
    stad: 'Rotterdam',
    naam: 'Maashaven',
    hook: 'Feestje in de Maassilo?',
    subhook: 'Parkeer op 7 min. lopen',
    kenmerken: [
      ['95', 'Parkeerplaatsen'],
      ['7 min.', 'naar de Maassilo'],
      ['€25', 'per dag gereserveerd'],
      ['', 'Rolstoeltoegankelijk'],
    ],
    prijs: {bedrag: '€8,00', eenheid: 'per uur'},
    foto: 'locaties/129.jpg',
    url: pagina('rotterdam/parking-maashaven/id=129'),
    bron: '€8 per 60 minuten, dagtarief met reservering €25.',
  },

  // Eindhoven
  {
    slug: 'td-gebouw',
    id: 17,
    stad: 'Eindhoven',
    naam: 'TD-gebouw',
    hook: 'Dagje Eindhoven al duur genoeg?',
    subhook: 'Parkeer voordelig',
    kenmerken: [
      ['97', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['10 min.', 'van centrum'],
      ['€15', 'dagtarief'],
    ],
    prijs: {bedrag: '€4,50', eenheid: 'per uur'},
    foto: 'locaties/17.jpg',
    url: pagina('eindhoven/parking-td-gebouw/id=17'),
    bron: '€1,50 per 20 minuten.',
  },
  {
    slug: 'philips-stadion',
    id: 7,
    stad: 'Eindhoven',
    naam: 'Philips Stadion',
    hook: 'Goedkoop parkeren in Eindhoven?',
    subhook: 'Parkeer bij het Philips Stadion',
    kenmerken: [
      ['700', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['9 min.', 'van centrum'],
      ['€15', 'dagtarief'],
    ],
    prijs: {bedrag: '€3,00', eenheid: 'per uur'},
    foto: 'locaties/7.jpg',
    url: pagina('eindhoven/parking-philips-stadion/id=7'),
    bron: '€1,50 per 30 minuten. Tijdens wedstrijden en grote evenementen niet bereikbaar.',
  },
  {
    slug: 'philips-bedrijfsschool',
    id: 31,
    stad: 'Eindhoven',
    naam: 'Philips Bedrijfsschool',
    hook: 'Eindhoven op loopafstand?',
    subhook: 'Parkeer 24/7 voordelig',
    kenmerken: [
      ['176', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['10 min.', 'van centrum'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€1,95', eenheid: 'per uur', vanaf: true},
    foto: 'locaties/31.jpg',
    url: pagina('eindhoven/parking-philips-bedrijfsschool/id=31'),
    bron: '€0,65 per 20 min (21-09u); overdag €1,30 per 20 min.',
  },
  {
    slug: 'victoriapark',
    id: 25,
    stad: 'Eindhoven',
    naam: 'Victoriapark',
    hook: 'Avondje Eindhoven?',
    subhook: 'Parkeer midden in het centrum',
    kenmerken: [
      ['2 min.', 'van centrum'],
      ['24/7', 'Open'],
      ['€5', 'max. per nacht'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€1,00', eenheid: 'per uur na 18u'},
    foto: 'locaties/25.jpg',
    url: pagina('eindhoven/parking-victoriapark/id=25'),
    bron: 'Nachttarief 18:00-08:00 €1 per uur, max. €5 per nacht; overdag €4 per uur.',
  },
  {
    slug: 'dll-garage',
    id: 5,
    stad: 'Eindhoven',
    naam: 'DLL (Garage)',
    hook: 'Uit eten in Eindhoven?',
    subhook: 'Parkeer overdekt in het centrum',
    kenmerken: [
      ['284', 'Parkeerplaatsen'],
      ['4 min.', 'van centrum'],
      ['Ma-vr', 'vanaf 17:00 open'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€3,00', eenheid: 'per uur'},
    foto: 'locaties/5.jpg',
    url: pagina('eindhoven/parking-dll-garage/id=5'),
    bron: '€1,50 per 30 minuten. Ma-vr open 17:00-06:00 (niet tijdens kantooruren).',
  },
  {
    slug: 'dll-parkeerdek',
    id: 101,
    stad: 'Eindhoven',
    naam: 'DLL parkeerdek',
    hook: "'s Avonds de stad in?",
    subhook: 'Parkeer op 4 min. van het centrum',
    kenmerken: [
      ['125', 'Parkeerplaatsen'],
      ['4 min.', 'van centrum'],
      ['Ma-vr', 'vanaf 17:00 open'],
      ['€15', 'dagtarief'],
    ],
    prijs: {bedrag: '€3,00', eenheid: 'per uur'},
    foto: 'locaties/101.jpg',
    url: pagina('eindhoven/parking-dll-parkeerdek-centrum/id=101'),
    bron: '€1,50 per 30 minuten. Ma-vr open 17:00-06:00 (niet tijdens kantooruren).',
  },
  {
    slug: 'evoluon',
    id: 103,
    stad: 'Eindhoven',
    naam: 'Evoluon',
    hook: 'Naar het Evoluon?',
    subhook: 'Parkeer op 2 min. lopen',
    kenmerken: [
      ['350', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['€10', 'dagtarief'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€2,00', eenheid: 'per uur'},
    foto: 'locaties/103.jpg',
    url: pagina('eindhoven/parking-evoluon/id=103'),
    bron: 'Per uur €2, dagtarief €10.',
  },

  // Regio Zuid-Holland
  {
    slug: 'at-the-park',
    id: 53,
    stad: 'Rijswijk',
    naam: 'At the Park',
    hook: 'Naar Rijswijk?',
    subhook: 'Parkeer vlak bij het station',
    kenmerken: [
      ['7 min.', 'van station'],
      ['24/7', 'Open'],
      ['€12', 'dagtarief'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€1,85', eenheid: 'per uur'},
    foto: 'locaties/53.jpg',
    url: pagina('regio-zuid-holland/parking-at-the-park/id=53'),
    bron: 'Per uur €1,85, dagtarief €12.',
  },
  {
    slug: 'stationsweg-ypenburg',
    id: 57,
    stad: 'Den Haag',
    naam: 'Stationsweg Ypenburg',
    hook: 'Filmavond in Ypenburg?',
    subhook: 'Parkeer direct naast Pathé',
    kenmerken: [
      ['425', 'Parkeerplaatsen'],
      ['', 'Direct naast station'],
      ['€4,75', 'voor Pathé-bezoekers'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€3,75', eenheid: 'per uur'},
    foto: 'locaties/57.jpg',
    url: pagina('regio-zuid-holland/parkingyou-stationsweg-ypenburg/id=57'),
    bron: '€1,25 per 20 minuten; Pathé-bezoekers 0-4 uur €4,75. Open 07:00-01:00.',
  },
  {
    slug: 'pr-schiedam-centrum',
    id: 63,
    stad: 'Schiedam',
    naam: 'P+R Schiedam Centrum',
    hook: 'Met de trein verder?',
    subhook: 'Parkeer bij Schiedam Centraal',
    kenmerken: [
      ['4 min.', 'van station'],
      ['', 'Overdekte garage'],
      ['€23', 'max. per dag'],
      ['', 'Cameratoezicht'],
    ],
    prijs: {bedrag: '€3,75', eenheid: 'per uur'},
    foto: 'locaties/63.jpg',
    url: pagina('regio-zuid-holland/parkingyou-p-r-schiedam-centrum/id=63'),
    bron: '€1,25 per 20 minuten, max. dagtarief €23.',
  },

  // Regio Gelderland
  {
    slug: 'lentse-plas',
    id: 59,
    stad: 'Nijmegen',
    naam: 'Lentse plas',
    hook: 'Film of zwemmen in Nijmegen?',
    subhook: 'Parkeer naast de Lentse plas',
    kenmerken: [
      ['24/7', 'Open'],
      ['€3,75', 'voor Pathé-bezoekers'],
      ['€21,50', 'max. per dag'],
      ['', 'Naast Pathé Nijmegen'],
    ],
    prijs: {bedrag: '€3,30', eenheid: 'per uur'},
    foto: 'locaties/59.jpg',
    url: pagina('regio-gelderland/parking-lentse-plas/id=59'),
    bron: '€1,10 per 20 minuten; Pathé-bezoekers 0-4 uur €3,75.',
    check: 'IG-024 in de Instagram-strategie: naam Pathé en tarief Lentse plas nog bevestigen.',
  },
  {
    slug: 'pathe-ede',
    id: 61,
    stad: 'Ede',
    naam: 'Pathé Ede',
    hook: 'Naar de film in Ede?',
    subhook: 'Parkeer direct naast Pathé',
    kenmerken: [
      ['€4,50', 'voor Pathé-bezoekers'],
      ['€17,50', 'max. per dag'],
      ['', 'Vlak bij de A12'],
      ['', 'Elke dag open'],
    ],
    prijs: {bedrag: '€2,55', eenheid: 'per uur'},
    foto: 'locaties/61.jpg',
    url: pagina('regio-gelderland/parkingyou-pathe-ede-/id=61'),
    bron: '€0,85 per 20 minuten; Pathé-bezoekers max. 4 uur €4,50.',
  },

  // Heerhugowaard
  {
    slug: 'heerhugowaard-p1-zuidtangent',
    id: 105,
    stad: 'Heerhugowaard',
    naam: 'P1 Zuidtangent',
    hook: 'Shoppen in Middenwaard?',
    subhook: 'Parkeer direct bij de winkels',
    kenmerken: [
      ['', 'Direct bij winkelcentrum'],
      ['€9', 'max. per dag'],
      ['', 'Elektrisch laden'],
      ['', 'Cameratoezicht'],
    ],
    prijs: {bedrag: '€1,00', eenheid: 'per uur'},
    foto: 'locaties/105.jpg',
    url: pagina('heerhugowaard/parking-heerhugowaard-p1-zuidtangent-/id=105'),
    bron: '€0,20 per 12 minuten, max. dagtarief €9.',
  },
  {
    slug: 'p2-middenwaard',
    id: 107,
    stad: 'Heerhugowaard',
    naam: 'P2 Middenwaard',
    hook: 'Dagje Heerhugowaard?',
    subhook: 'Parkeer midden in het centrum',
    kenmerken: [
      ['24/7', 'Open'],
      ['', 'Direct bij winkelcentrum'],
      ['€9', 'max. per dag'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€1,00', eenheid: 'per uur'},
    foto: 'locaties/107.jpg',
    url: pagina('heerhugowaard/parking-p2-middenwaard/id=107'),
    bron: '€0,20 per 12 minuten, max. dagtarief €9.',
  },

  // Zoetermeer (eerste 2 uur gratis, daarna €3 per uur, dagtarief €16)
  ...(
    [
      ['p1-belgielaan', 109, 'P1 Belgielaan', 'Shoppen in het Stadshart?', 'parking-p1-belgielaan-/id=109', 'Elektrisch laden'],
      ['p2-bovenlangs', 111, 'P2 Bovenlangs', 'Dagje Zoetermeer?', 'parking-p2-bovenlangs/id=111', 'Elektrisch laden'],
      ['p2-onderlangs', 113, 'P2 Onderlangs', 'Even naar het Stadshart?', 'parking-p2-onderlangs/id=113', 'Elektrisch laden'],
      ['p4-luxemburglaan', 115, 'P4 Luxemburglaan', 'Boodschappen in Zoetermeer?', 'parking-p4-luxemburglaan/id=115', 'Elektrisch laden'],
      ['p5-amsterdamstraat', 117, 'P5 Amsterdamstraat', 'Shoppen in Zoetermeer?', 'parking-p5-amsterdamstraat-/id=117', 'Elektrisch laden'],
      ['p8-nederlandlaan', 119, 'P8 Nederlandlaan', 'Snel naar het Stadshart?', 'parking-p8-nederlandlaan/id=119', 'Uitrijden 24/7'],
      ['p9-duitslandlaan', 121, 'P9 Duitslandlaan', 'Middagje Stadshart?', 'parking-p9-duitslandlaan/id=121', 'Uitrijden 24/7'],
    ] as const
  ).map(
    ([slug, id, naam, hook, pad, vierde]): Locatie => ({
      slug,
      id,
      stad: 'Zoetermeer',
      naam,
      hook,
      subhook: 'Eerste 2 uur gratis parkeren',
      kenmerken: [
        ['2 min.', 'van Stadshart'],
        ['€3', 'per uur daarna'],
        ['€16', 'dagtarief'],
        ['', vierde],
      ],
      prijs: {bedrag: 'Gratis', eenheid: 'eerste 2 uur'},
      foto: `locaties/${id}.jpg`,
      url: pagina(`zoetermeer/${pad}`),
      bron: 'Eerste 2 uren gratis, daarna €3 per uur, dagtarief €16.',
      check: 'IG-014 in de Instagram-strategie: eerste 2 uur gratis bevestigen voor alle 7 Zoetermeerse garages.',
    }),
  ),

  // Almere
  {
    slug: 'p1-carlton-wtc',
    id: 123,
    stad: 'Almere',
    naam: 'P1 Carlton WTC',
    hook: 'Dagje Almere centrum?',
    subhook: 'Parkeer op 4 min. lopen',
    kenmerken: [
      ['125', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['4 min.', 'van centrum'],
      ['', 'Overdekte garage'],
    ],
    prijs: {bedrag: '€3,00', eenheid: 'per uur'},
    foto: 'locaties/123.jpg',
    url: pagina('almere/parking-p1-carlton-wtc/id=123'),
    bron: '€1,00 per 20 minuten, dagtarief €30.',
  },
  {
    slug: 'p2-mandela-wtc',
    id: 125,
    stad: 'Almere',
    naam: 'P2 Mandela WTC',
    hook: 'Hele dag in Almere?',
    subhook: 'Parkeer voordelig',
    kenmerken: [
      ['250', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['4 min.', 'van centrum'],
      ['', 'Overdekte garage'],
    ],
    prijs: {bedrag: '€6,00', eenheid: 'per dag'},
    foto: 'locaties/125.jpg',
    url: pagina('almere/parking-p2-mandela-wtc/id=125'),
    bron: 'Dagtarief €6,00; €1,00 per 20 minuten.',
    check: 'IG-013 in de Instagram-strategie: dagtarief €6 bij P2 Mandela WTC nog bevestigen.',
  },

  // Zaandam
  {
    slug: 'houthavenkade',
    id: 131,
    stad: 'Zaandam',
    naam: 'Houthavenkade',
    hook: 'Dagje Zaandam?',
    subhook: 'Parkeer vlak bij het centrum',
    kenmerken: [
      ['81', 'Parkeerplaatsen'],
      ['24/7', 'Open'],
      ['6 min.', 'van centrum'],
      ['', 'Elektrisch laden'],
    ],
    prijs: {bedrag: '€3,60', eenheid: 'per uur'},
    foto: 'locaties/131.jpg',
    url: pagina('zaandam/houthavenkade/id=131'),
    bron: '€1,20 per 20 min (09-18u); 18-09u €1,00 per uur.',
  },
];
